console.log("Content script loaded");

// Function to check if the content script is already injected
function isContentScriptInjected() {
  return window.chaperoneContentScriptInjected === true;
}

// Mark this content script as injected
window.chaperoneContentScriptInjected = true;

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Message received in content script:", message);
  if (message.action === "showModal") {
    showModal(message.timeLimit, message.tabId, message.vocabularyData);
  }
});

async function showModal(timeLimit, tabId, vocabularyData) {
  console.log("Showing modal with vocabulary data:", vocabularyData);
  
  // Check if modal already exists and remove it
  const existingModal = document.getElementById('chaperone-modal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // Create overlay container
  const modal = document.createElement('div');
  modal.id = 'chaperone-modal';
  modal.style.cssText = `position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; background-color: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); z-index: 2147483647; padding: 1rem;`; // Maximum z-index

  // Create modal content container
  const modalContent = document.createElement('div');
  modalContent.style.cssText = `background-color: white; border-radius: 0.75rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); width: 100%; max-width: 28rem; overflow: hidden;`;
  modal.appendChild(modalContent);

  // Stage 1: Vocabulary Challenge
  function showVocabularyChallenge() {
    modalContent.innerHTML = '';

    // Header
    const header = document.createElement('div');
    header.style.cssText = `
      padding: 1rem;
      border-bottom: 1px solid #e5e7eb;
      background-color: #f9fafb;
    `;

    const title = document.createElement('h2');
    title.textContent = 'Time Limit Reached';
    title.style.cssText = `
      font-size: 1.25rem;
      font-weight: 600;
      color: #111827;
      margin: 0;
    `;
    header.appendChild(title);
    modalContent.appendChild(header);

    // Body
    const body = document.createElement('div');
    body.style.cssText = 'padding: 1.5rem;';

    const message = document.createElement('p');
    message.textContent = `Your time limit of ${timeLimit / 60000} minutes has been reached. Solve this to continue:`;
    message.style.cssText = `
      color: #4b5563;
      margin-bottom: 1rem;
    `;
    body.appendChild(message);

    const questionDisplay = document.createElement('div');
    questionDisplay.style.cssText = `
      margin-bottom: 1.5rem;
    `;

    const questionText = document.createElement('p');
    questionText.textContent = 'Select the synonym of:';
    questionText.style.cssText = `
      color: #4b5563;
      margin-bottom: 0.5rem;
    `;

    const wordDisplay = document.createElement('div');
    wordDisplay.textContent = vocabularyData.vocabulary.word;
    wordDisplay.style.cssText = `
      font-size: 1.5rem;
      font-weight: 600;
      color: #111827;
      text-align: center;
      padding: 0.5rem;
      border-radius: 0.5rem;
      background-color: #f3f4f6;
    `;

    questionDisplay.appendChild(questionText);
    questionDisplay.appendChild(wordDisplay);
    body.appendChild(questionDisplay);

    // Create option buttons
    const optionsContainer = document.createElement('div');
    optionsContainer.style.cssText = `
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    `;

    // Find the correct answer
    let correctAnswer = null;
    vocabularyData.options.forEach(option => {
      if (option.is_correct) {
        correctAnswer = option.option;
      }
    });

    // Shuffle options
    const shuffledOptions = [...vocabularyData.options].sort(() => Math.random() - 0.5);

    shuffledOptions.forEach(option => {
      const optionButton = document.createElement('button');
      optionButton.textContent = option.option;
      optionButton.style.cssText = `
        padding: 0.75rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        background-color: white;
        color: #374151;
        font-weight: 500;
        transition: all 0.15s ease;
        cursor: pointer;
      `;
      optionButton.addEventListener('mouseover', () => {
        optionButton.style.backgroundColor = '#f3f4f6';
      });
      optionButton.addEventListener('mouseout', () => {
        optionButton.style.backgroundColor = 'white';
      });
      optionButton.addEventListener('click', () => {
        if (option.is_correct) {
          clearTimeout(modalTimer);
          // Send message to background to update correct count
          browser.runtime.sendMessage({
            action: "answerCorrect",
            associationId: vocabularyData.id
          });
          showPostponementOptions();
        } else {
          // Send message to background to update incorrect count
          browser.runtime.sendMessage({
            action: "answerIncorrect",
            associationId: vocabularyData.id
          });
          showIncorrectAnswerMessage();
        }
      });
      optionsContainer.appendChild(optionButton);
    });

    body.appendChild(optionsContainer);

    // Buttons container
    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = `
      display: flex;
      gap: 0.75rem;
      justify-content: flex-end;
    `;

    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close Tab';
    closeButton.style.cssText = `
      background-color: #ef4444;
      color: white;
      padding: 0.75rem 1.5rem;
      border-radius: 0.5rem;
      font-weight: 500;
      transition: background-color 0.15s ease;
      cursor: pointer;
      border: none;
    `;
    closeButton.addEventListener('mouseover', () => {
      closeButton.style.backgroundColor = '#dc2626';
    });
    closeButton.addEventListener('mouseout', () => {
      closeButton.style.backgroundColor = '#ef4444';
    });
    closeButton.addEventListener('click', () => {
      browser.runtime.sendMessage({ action: "closeTab", tabId });
      modal.remove();
    });

    buttonContainer.appendChild(closeButton);
    body.appendChild(buttonContainer);
    modalContent.appendChild(body);

    function showIncorrectAnswerMessage() {
      let incorrectMessage = modal.querySelector('.incorrect-message');
      if (!incorrectMessage) {
        incorrectMessage = document.createElement('p');
        incorrectMessage.classList.add('incorrect-message');
        incorrectMessage.style.cssText = `
          color: #dc2626;
          margin-bottom: 1rem;
          font-size: 0.875rem;
          text-align: center;
        `;
        optionsContainer.insertAdjacentElement('afterend', incorrectMessage);
      }
      incorrectMessage.textContent = 'Incorrect answer. Try again.';
    }
  }

  // Stage 2: Postponement Selection
  function showPostponementOptions() {
    modalContent.innerHTML = '';

    // Header
    const header = document.createElement('div');
    header.style.cssText = `
      padding: 1rem;
      border-bottom: 1px solid #e5e7eb;
      background-color: #f9fafb;
    `;

    const title = document.createElement('h2');
    title.textContent = 'Select Postponement Time';
    title.style.cssText = `
      font-size: 1.25rem;
      font-weight: 600;
      color: #111827;
      margin: 0;
    `;
    header.appendChild(title);
    modalContent.appendChild(header);

    // Body
    const body = document.createElement('div');
    body.style.cssText = 'padding: 1.5rem;';

    const message = document.createElement('p');
    message.textContent = 'How long would you like to postpone?';
    message.style.cssText = `
      color: #4b5563;
      margin-bottom: 1rem;
    `;
    body.appendChild(message);

    // Quick selection buttons
    const buttonGrid = document.createElement('div');
    buttonGrid.style.cssText = `
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.75rem;
      margin-bottom: 1rem;
    `;

    const postponementTimes = [1, 2, 5, 10];
    postponementTimes.forEach(minutes => {
      const button = document.createElement('button');
      button.textContent = `${minutes} min`;
      button.style.cssText = `
        padding: 0.75rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        color: #374151;
        font-weight: 500;
        transition: all 0.15s ease;
        cursor: pointer;
        background-color: white;
      `;
      button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#f3f4f6';
      });
      button.addEventListener('mouseout', () => {
        button.style.backgroundColor = 'white';
      });
      button.addEventListener('click', () => {
        modal.remove();
        browser.runtime.sendMessage({ 
          action: "postpone", 
          tabId: tabId, 
          delay: minutes * 60000 
        });
      });
      buttonGrid.appendChild(button);
    });
    body.appendChild(buttonGrid);

    // Custom time input
    const customTimeContainer = document.createElement('div');
    customTimeContainer.style.cssText = `
      display: flex;
      gap: 0.75rem;
      margin-bottom: 1rem;
    `;

    const customTimeInput = document.createElement('input');
    customTimeInput.type = 'number';
    customTimeInput.placeholder = 'Custom (min)';
    customTimeInput.style.cssText = `
      flex: 1;
      padding: 0.75rem 1rem;
      border: 1px solid #e5e7eb;
      border-radius: 0.5rem;
      font-size: 1rem;
      outline: none;
      transition: border-color 0.15s ease;
    `;
    customTimeInput.addEventListener('focus', () => {
      customTimeInput.style.borderColor = '#6366f1';
      customTimeInput.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
    });
    customTimeInput.addEventListener('blur', () => {
      customTimeInput.style.borderColor = '#e5e7eb';
      customTimeInput.style.boxShadow = 'none';
    });

    const customTimeButton = document.createElement('button');
    customTimeButton.textContent = 'Set';
    customTimeButton.style.cssText = `
      background-color: #6366f1;
      color: white;
      padding: 0.75rem 1.5rem;
      border-radius: 0.5rem;
      font-weight: 500;
      transition: background-color 0.15s ease;
      cursor: pointer;
      border: none;
    `;
    customTimeButton.addEventListener('mouseover', () => {
      customTimeButton.style.backgroundColor = '#4f46e5';
    });
    customTimeButton.addEventListener('mouseout', () => {
      customTimeButton.style.backgroundColor = '#6366f1';
    });
    customTimeButton.addEventListener('click', () => {
      const customMinutes = parseInt(customTimeInput.value, 10);
      if (!isNaN(customMinutes) && customMinutes > 0) {
        modal.remove();
        browser.runtime.sendMessage({ 
          action: "postpone", 
          tabId: tabId, 
          delay: customMinutes * 60000 
        });
      }
    });

    customTimeContainer.appendChild(customTimeInput);
    customTimeContainer.appendChild(customTimeButton);
    body.appendChild(customTimeContainer);

    // Close button
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close Tab';
    closeButton.style.cssText = `
      width: 100%;
      background-color: #ef4444;
      color: white;
      padding: 0.75rem 1.5rem;
      border-radius: 0.5rem;
      font-weight: 500;
      transition: background-color 0.15s ease;
      cursor: pointer;
      border: none;
    `;
    closeButton.addEventListener('mouseover', () => {
      closeButton.style.backgroundColor = '#dc2626';
    });
    closeButton.addEventListener('mouseout', () => {
      closeButton.style.backgroundColor = '#ef4444';
    });
    closeButton.addEventListener('click', () => {
      browser.runtime.sendMessage({ action: "closeTab", tabId });
      modal.remove();
    });
    body.appendChild(closeButton);

    modalContent.appendChild(body);
  }

  // Initial setup
  document.body.appendChild(modal);
  showVocabularyChallenge();

  // 60-second timer for the initial modal
  function closeTab(tabId) {
    browser.runtime.sendMessage({ action: "closeTab", tabId });
    modal.remove();
  }

  let modalTimer = setTimeout(() => closeTab(tabId), 60000);
}