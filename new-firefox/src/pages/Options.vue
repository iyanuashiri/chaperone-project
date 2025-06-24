<template>
  <div class="bg-gray-50 min-h-screen py-12">
    <div class="max-w-2xl mx-auto bg-white rounded-xl shadow-sm p-8">
      <div class="space-y-8">
        <!-- Header -->
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Chaperone Settings</h1>
          <p class="mt-2 text-gray-600">Customize your browsing time limits and website restrictions.</p>
        </div>

        <!-- Time Limit Section -->
        <div class="space-y-4">
          <label class="block">
            <span class="text-gray-700 font-medium">Time Limit</span>
            <div class="mt-1 flex space-x-3">
              <input 
                type="number" 
                v-model="timeLimit" 
                min="1" 
                class="flex-1 px-4 py-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent" 
                placeholder="Enter minutes"
              >
              <span class="inline-flex items-center px-4 rounded-lg bg-gray-50 text-gray-500 border border-gray-200">
                minutes
              </span>
            </div>
          </label>
        </div>

        <!-- URLs Section -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-gray-700 font-medium">Restricted Websites</span>
          </div>

          <!-- URL List -->
          <ul class="space-y-2">
            <li 
              v-for="(url, index) in urls" 
              :key="index"
              class="flex items-center justify-between p-3 mb-2 rounded-lg border border-gray-200 bg-white"
            >
              <span class="text-gray-600">{{ url }}</span>
              <button 
                @click="removeUrl(index)"
                class="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
              >
                Remove
              </button>
            </li>
          </ul>

          <!-- Add URL Input -->
          <div class="flex space-x-3">
            <input 
              type="text" 
              v-model="newUrl"
              @keypress="handleKeyPress"
              class="flex-1 px-4 py-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent" 
              placeholder="Enter website URL"
            >
            <button 
              @click="addUrl"
              class="px-6 py-3 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-200"
            >
              Add URL
            </button>
          </div>
        </div>

        <!-- Save Button -->
        <button 
          @click="saveSettings"
          class="w-full px-6 py-3 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-200"
        >
          Save Changes
        </button>
      </div>
    </div>

    <!-- Success Message -->
    <div 
      v-if="showSuccessMessage"
      class="fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg"
    >
      Settings saved successfully!
    </div>
  </div>
</template>


<script>
import browser from 'webextension-polyfill'

export default {
  data() {
    return {
      timeLimit: 1, // in minutes
      urls: [],
      newUrl: '',
      showSuccessMessage: false,
      DEFAULT_SETTINGS: {
        timeLimit: 6000, // 1 minute - for testing
        urls: ["*://*.twitter.com/*", "*://*.facebook.com/*", "*://*.instagram.com/*", "*://*.youtube.com/*"]
      }
    }
  },
  mounted() {
    this.loadSettings()
  },
  methods: {
    loadSettings() {
      // Load existing settings from browser storage
      if (typeof browser !== 'undefined' && browser.storage) {
        browser.storage.sync.get(this.DEFAULT_SETTINGS, (settings) => {
          this.timeLimit = settings.timeLimit / 60000 // Convert to minutes
          this.urls = [...settings.urls]
        })
      } else {
        // Fallback for testing without browser extension context
        this.timeLimit = this.DEFAULT_SETTINGS.timeLimit / 60000
        this.urls = [...this.DEFAULT_SETTINGS.urls]
      }
    },
    formatUrl(url) {
      // Remove whitespace
      url = url.trim()
      
      // Remove http:// or https:// if present
      url = url.replace(/^https?:\/\//, '')
      
      // Remove www. if present
      url = url.replace(/^www\./, '')
      
      // Remove trailing slash if present
      url = url.replace(/\/$/, '')
      
      // Add wildcard pattern
      return `*://*.${url}/*`
    },
    addUrl() {
      if (this.newUrl.trim()) {
        const formattedUrl = this.formatUrl(this.newUrl)
        this.urls.push(formattedUrl)
        this.newUrl = ''
      }
    },
    removeUrl(index) {
      this.urls.splice(index, 1)
    },
    handleKeyPress(event) {
      if (event.key === 'Enter' && this.newUrl.trim()) {
        this.addUrl()
      }
    },
    saveSettings() {
      const timeLimitMs = parseInt(this.timeLimit, 10) * 60000
      const settings = {
        timeLimit: timeLimitMs,
        urls: [...this.urls]
      }

      if (typeof browser !== 'undefined' && browser.storage) {
        browser.storage.sync.set(settings, () => {
          // Notify background script that settings were updated
          if (browser.runtime) {
            browser.runtime.sendMessage({ action: "settingsUpdated" })
          }
          
          this.showSuccessMessage = true
          
          // Hide success message after 3 seconds
          setTimeout(() => {
            this.showSuccessMessage = false
          }, 3000)
        })
      } else {
        // Fallback for testing without browser extension context
        console.log('Settings would be saved:', settings)
        this.showSuccessMessage = true
        setTimeout(() => {
          this.showSuccessMessage = false
        }, 3000)
      }
    }
  }
}
</script>


<style>
/* Tailwind classes are used in template, but you can add custom styles here if needed */
</style>