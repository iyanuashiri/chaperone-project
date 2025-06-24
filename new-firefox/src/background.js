import browser from "webextension-polyfill";

console.log("Hello from the background!");

browser.runtime.onInstalled.addListener((details) => {
  console.log("Extension installed:", details);
});





const DEFAULT_SETTINGS = {
  timeLimit: 1000, // Changed to 10 seconds for testing (from 6 seconds)
  urls: ["://.x.com/", "://.twitter.com/", "://.facebook.com/", "://.instagram.com/", "://.youtube.com/", "*://*.youtube.com/*", "*://*.x.com/*"],
};

// API client setup
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/';


let timers = {};
let currentSettings = DEFAULT_SETTINGS;
let vocabularyData = [];

// Function to load settings from browser storage
function loadSettings(callbackFunction) {
  function handleStorageResult(savedSettings) {
    // Ensure we have all the required settings
    currentSettings = Object.assign({}, DEFAULT_SETTINGS, savedSettings);
    console.log("Settings loaded and merged:", currentSettings);
    callbackFunction(currentSettings);
  }

  browser.storage.sync.get(DEFAULT_SETTINGS, handleStorageResult);
}

// Check if a URL matches any pattern in the settings
function isUrlRestricted(url) {
  if (!url) return false;
  
  return currentSettings.urls.some(pattern => {
    // Make the pattern a proper regex
    // Convert * to .*
    const regexPattern = pattern.replace(/\*/g, '.*');
    // Console log for debugging
    const matches = url.match(new RegExp(regexPattern));
    console.log(`Checking URL ${url} against pattern ${pattern} (regex: ${regexPattern}): ${matches ? 'MATCH' : 'NO MATCH'}`);
    return matches;
  });
}

// Fetch vocabulary data from API
async function fetchVocabularyData() {

  try {
    const result = await browser.storage.local.get(['accessToken', 'email'])
    const API_TOKEN = result.accessToken;

    console.log("Using API token:", API_TOKEN);

    console.log("Fetching vocabulary data from API...");
    const response = await fetch(`${API_BASE_URL}associations/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${API_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Association data:", data);
    const validData = data
    console.log("Fetched vocabulary data:", validData);
    return validData;
  } catch (error) {
    console.error("Error fetching vocabulary data:", error);
    // Return fallback data if API fails
    return [{
      id: 0,
      vocabulary: { word: "test", meaning: "An examination of someone's knowledge or proficiency" },
      options: [
        { id: 1, option: "EXAMINATION", meaning: "A detailed inspection or study", is_correct: true },
        { id: 2, option: "practice", meaning: "Repeated exercise to improve skill", is_correct: false },
        { id: 3, option: "ignore", meaning: "To pay no attention to something", is_correct: false }
      ],
      status: "pending"
    }];
  }
}

// Update the correctness status of an association
async function updateAssociationStatus(id, isCorrect) {
  try {

    const result = await browser.storage.local.get(['accessToken', 'email'])
    const API_TOKEN = result.accessToken; 
    // Don't try to update associations with ID 0 (fallback data)
    if (id === 0) {
      console.log("Skipping API update for fallback association");
      return;
    }
    
    const endpoint = isCorrect ? 
      `${API_BASE_URL}associations/${id}/correct/` : 
      `${API_BASE_URL}associations/${id}/incorrect/`;

    const response = await fetch(endpoint, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${API_TOKEN}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`Association ${id} updated to ${isCorrect ? 'correct' : 'incorrect'}:`, data);
    return data;
  } catch (error) {
    console.error(`Error updating association ${id}:`, error);
  }
}

async function wakeUpShowModal(tabId, timeLimit) {
  console.log("Modal timer triggered for tab:", tabId);
  
  try {
    // First check if tab is still available
    let tab;
    try {
      tab = await browser.tabs.get(tabId);
      console.log("Tab still exists:", tab);
    } catch (error) {
      console.log("Tab no longer exists, cancelling modal:", error);
      delete timers[tabId];
      return;
    }
    
    // Get vocabulary data
    let vocabItems = vocabularyData;
    
    // If no data or need to refresh, fetch from API
    if (vocabItems.length === 0) {
      vocabItems = await fetchVocabularyData();
      vocabularyData = vocabItems; // Update the cached data
    }
    
    // If still no data after fetching, use a fallback
    if (vocabItems.length === 0) {
      console.warn("No vocabulary data available, using fallback");
      const fallbackVocab = {
        id: 0,
        vocabulary: { word: "test", meaning: "An examination of someone's knowledge or proficiency" },
        options: [
          { id: 1, option: "EXAMINATION", meaning: "A detailed inspection or study", is_correct: true },
          { id: 2, option: "practice", meaning: "Repeated exercise to improve skill", is_correct: false },
          { id: 3, option: "ignore", meaning: "To pay no attention to something", is_correct: false }
        ],
        status: "correct"
      };
      vocabItems = [fallbackVocab];
    }
    
    // Get a random vocabulary item
    const randomIndex = Math.floor(Math.random() * vocabItems.length);
    const selectedVocab = vocabItems[randomIndex];
    
    console.log("Sending modal message with vocabulary:", selectedVocab);
    try {
      await browser.tabs.sendMessage(tabId, {
        action: "showModal",
        timeLimit: timeLimit,
        tabId: tabId,
        vocabularyData: selectedVocab
      });
      console.log("Modal message sent successfully");
    } catch (error) {
      console.error("Error sending message to tab:", error);
      // Try to inject the content script if it's not loaded
      try {
        await browser.tabs.executeScript(tabId, { file: "content_scripts/content_scripts.js" });
        console.log("Content script injected, trying to send modal again");
        await browser.tabs.sendMessage(tabId, {
          action: "showModal",
          timeLimit: timeLimit,
          tabId: tabId,
          vocabularyData: selectedVocab
        });
      } catch (injectionError) {
        console.error("Failed to inject content script:", injectionError);
      }
    }
  } catch (error) {
    console.error("Error in wakeUpShowModal:", error);
  }
  
  delete timers[tabId];
}

function startTimer(tabId, timeLimit) {
  console.log(`Starting timer for tab ${tabId} with time limit ${timeLimit}ms`);
  
  if (timers[tabId]) {
    console.log(`Clearing existing timer for tab ${tabId}`);
    clearTimeout(timers[tabId]);
  }

  timers[tabId] = setTimeout(() => wakeUpShowModal(tabId, timeLimit), timeLimit);
  console.log(`Timer set for tab ${tabId}, will trigger in ${timeLimit}ms`);
}

// Check and update all open tabs when settings change
async function updateAllTabs() {
  console.log("Updating all tabs with current settings");
  const tabs = await browser.tabs.query({});
  console.log(`Found ${tabs.length} tabs to check`);

  tabs.forEach(tab => {
    if (tab.url && isUrlRestricted(tab.url)) {
      console.log(`Tab ${tab.id} (${tab.url}) is restricted, starting timer`);
      startTimer(tab.id, currentSettings.timeLimit);
    } else if (timers[tab.id]) {
      console.log(`Tab ${tab.id} is not restricted, clearing timer`);
      clearTimeout(timers[tab.id]);
      delete timers[tab.id];
    }
  });
}


// Listen for tab updates
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  console.log(`Tab ${tabId} updated:`, changeInfo);
  
  if (changeInfo.status === 'complete' && tab.url) {
    console.log(`Tab ${tabId} completed loading: ${tab.url}`);
    
    if (isUrlRestricted(tab.url)) {
      console.log(`Tab ${tabId} URL is restricted, starting timer`);
      startTimer(tabId, currentSettings.timeLimit);
    } else if (timers[tabId]) {
      console.log(`Tab ${tabId} URL is not restricted, clearing timer`);
      clearTimeout(timers[tabId]);
      delete timers[tabId];
    }
  }
});

// Clean up timers when tabs are closed
browser.tabs.onRemoved.addListener((tabId) => {
  console.log(`Tab ${tabId} removed`);
  
  if (timers[tabId]) {
    console.log(`Clearing timer for removed tab ${tabId}`);
    clearTimeout(timers[tabId]);
    delete timers[tabId];
  }
});

// Handle messages from content script and options page
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received:", message);
  
  switch (message.action) {
    case "closeTab":
      console.log(`Closing tab ${message.tabId}`);
      browser.tabs.remove(message.tabId);
      break;
    case "postpone":
      console.log(`Postponing tab ${message.tabId} for ${message.delay}ms`);
      startTimer(message.tabId, message.delay);
      break;
    case "settingsUpdated":
      console.log("Settings updated, reloading");
      loadSettings(() => {
        updateAllTabs();
      });
      break;
    case "answerCorrect":
      console.log(`Answer correct for association ${message.associationId}`);
      updateAssociationStatus(message.associationId, true);
      break;
    case "answerIncorrect":
      console.log(`Answer incorrect for association ${message.associationId}`);
      updateAssociationStatus(message.associationId, false);
      break;
    case "testModal":
      // For testing the modal directly
      console.log(`Testing modal on tab ${message.tabId}`);
      wakeUpShowModal(message.tabId, currentSettings.timeLimit);
      break;
  }
});



// For debugging - force timer to trigger in content script
function debugForceModalShow() {
  browser.tabs.query({active: true, currentWindow: true})
    .then(tabs => {
      if (tabs.length > 0) {
        wakeUpShowModal(tabs[0].id, currentSettings.timeLimit);
      }
    });
}

// Initialize the extension
async function initialize() {
  console.log("Initializing extension...");
  
  // Load settings first
  await new Promise((resolve) => {
    loadSettings((settings) => {
      console.log("Settings loaded:", settings);
      resolve(settings);
    });
  });
  
  // Fetch vocabulary data
  try {
    const data = await fetchVocabularyData();
    vocabularyData = data;
    console.log(`Loaded ${vocabularyData.length} vocabulary items`);
  } catch (error) {
    console.error("Failed to load vocabulary data:", error);
  }
  
  // Update all open tabs
  await updateAllTabs();
  console.log("Extension initialization complete");
}

// Start the extension
initialize();

// Expose debugging functions to browser console
window.debugChaperone = {
  forceModalShow: debugForceModalShow,
  checkAllTabs: updateAllTabs,
  getSettings: () => currentSettings,
  getVocabularyData: () => vocabularyData
};