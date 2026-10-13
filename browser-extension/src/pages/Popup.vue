<template>
  <div class="bg-gray-100">
    <div class="w-80 p-4">
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-4 bg-indigo-600">
          <h1 class="text-xl font-bold text-white">Chaperone</h1>
          <p class="text-indigo-200 text-sm">Browsing time manager</p>
        </div>
        
        <!-- Login Form -->
        <div v-if="!isAuthenticated" class="p-4">
          <div 
            v-if="showError" 
            class="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded"
          >
            {{ errorMessage }}
          </div>
          
          <form @submit="handleLogin" class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <input 
                type="email" 
                v-model="email"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                placeholder="Enter your email"
              >
            </div>
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
              <input type="password" v-model="password" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" placeholder="Enter your password" >
            </div>
            <button type="submit" :disabled="isLoading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50">
              {{ loginButtonText }}
            </button>
          </form>
        </div>
        
        <!-- Authenticated View -->
        <div v-if="isAuthenticated" class="p-4">
          <div class="text-center">
            <p class="text-gray-700 mb-4">Welcome, {{ userEmail }}!</p>
            <button 
              @click="handleLogout"
              class="text-sm text-indigo-600 hover:text-indigo-800"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from 'axios'
// import { browser } from 'webextension-polyfill'
import browser from "webextension-polyfill";


export default {
  data() {
    return {
      email: '',
      password: '',
      isAuthenticated: false,
      userEmail: '',
      showError: false,
      errorMessage: '',
      loginButtonText: 'Sign In',
      isLoading: false
    }
  },
  mounted() {
    this.checkAuthStatus()
  },
  methods: {
    async checkAuthStatus() {
      try {
        console.log('Checking auth status...')
        const result = await browser.storage.local.get(['accessToken', 'email'])
        console.log('Storage result:', result)
        if (result.accessToken && result.email) {
          this.showAuthenticatedView(result.email)
        } else {
          this.showLoginView()
        }
      } catch (error) {
        console.error('Error checking auth status:', error)
        this.showErrorMessage('Error checking authentication status')
      }
    },

    showLoginView() {
      console.log('Showing login view')
      this.isAuthenticated = false
    },

    showAuthenticatedView(email) {
      console.log('Showing authenticated view for:', email)
      this.isAuthenticated = true
      this.userEmail = email
    },

    showErrorMessage(message) {
      console.error('Showing error:', message)
      this.errorMessage = message
      this.showError = true
      setTimeout(() => {
        this.showError = false
      }, 10000) // Show error for 10 seconds
    },
        
    // async handleLogin(event) {
    //   event.preventDefault()
    //   console.log('Login form submitted')

    //   if (!this.email || !this.password) {
    //     this.showErrorMessage('Please enter both email and password')
    //     return
    //   }

    //   this.isLoading = true
    //   this.loginButtonText = 'Signing in...'

    //   try {
    //     console.log('Preparing login request...')
    //     const formData = new URLSearchParams()
    //     formData.append('username', this.email)
    //     formData.append('password', this.password)

    //     console.log('Sending request to backend...')
    //     const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login/', {
    //       method: 'POST',
    //       headers: {
    //         'Content-Type': 'application/x-www-form-urlencoded',
    //         'Accept': 'application/json'
    //       },
    //       body: formData,
    //       credentials: 'include'
    //     })

    //     console.log('Login response status:', response.status)
    //     const data = await response.json()
    //     console.log('Login response data:', data)

    //     if (response.ok && data.access_token) {
    //       console.log('Login successful, storing token...')
    //       await browser.storage.local.set({
    //         accessToken: data.access_token,
    //         email: this.email
    //       })
          
    //       this.showAuthenticatedView(this.email)
    //       this.email = ''
    //       this.password = ''
    //     } else {
    //       console.error('Login failed:', data)
    //       this.showErrorMessage(data.detail || 'Login failed. Please check your credentials.')
    //     }
    //   } catch (error) {
    //     console.error('Login error:', error)
        
    //     let errorMessage = 'Login failed. Please check your credentials and try again.'
    //     if (error.message === 'Failed to fetch') {
    //       errorMessage = 'Cannot connect to the server. Please check your connection.'
    //     }
        
    //     this.showErrorMessage(errorMessage)
    //   } finally {
    //     this.isLoading = false
    //     this.loginButtonText = 'Sign In'
    //   }
    // },

    async handleLogin(event) {

      event.preventDefault()
      console.log('Login form submitted')

      if (!this.email || !this.password) {
        this.showErrorMessage('Please enter both email and password')
        return
      }

      this.isLoading = true
      this.loginButtonText = 'Signing in...'

      try {
        console.log('Preparing login request...')
        const url = 'http://127.0.0.1:8000/api/v1/auth/login/'
        const formData = new FormData()
        formData.append('email', this.email) // Note: keeping 'username' as per original
        formData.append('password', this.password)

        console.log('Sending request to backend...')
        const response = await axios.post(url, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
          },
          withCredentials: true // axios equivalent of credentials: 'include'
        })

        console.log('Login response status:', response.status)
        console.log('Login response data:', response.data)

        if (response.data.access_token) {
          console.log('Login successful, storing token...')
          await browser.storage.local.set({
            accessToken: response.data.access_token,
            email: this.email
          })
          
          this.showAuthenticatedView(this.email)
          this.email = ''
          this.password = ''
        } else {
          console.error('Login failed:', response.data)
          this.showErrorMessage(response.data.detail || 'Login failed. Please check your credentials.')
        }
      } catch (error) {
        console.error('Login error:', error)
        
        let errorMessage = 'Login failed. Please check your credentials and try again.'
        
        // Handle axios-specific error structure
        if (error.response) {
          // Server responded with error status
          errorMessage = error.response.data?.detail || `Server error: ${error.response.status}`
        } else if (error.request) {
          // Request was made but no response received
          errorMessage = 'Cannot connect to the server. Please check your connection.'
        } else {
          // Something else happened
          errorMessage = error.message || errorMessage
        }
        
        this.showErrorMessage(errorMessage)
      } finally {
        this.isLoading = false
        this.loginButtonText = 'Sign In'
      }
    },

    async handleLogout() {
      try {
        console.log('Logging out...')
        await browser.storage.local.remove(['accessToken', 'email'])
        this.showLoginView()
        this.userEmail = ''
      } catch (error) {
        console.error('Logout error:', error)
        this.showErrorMessage('Failed to log out. Please try again.')
      }
    }
  }
}
</script>


<style>
/* Tailwind classes are used in template, but you can add custom styles here if needed */
</style>





<!-- <script setup>
console.log("Hello from the popup!");
</script>

<template>
  <div>
    <img src="/icon-with-shadow.svg" />
    <h1>vite-plugin-web-extension</h1>
    <p>
      Template: <code>vue-js</code>
    </p>
  </div>
</template>

<style>
html,
body {
  width: 300px;
  height: 400px;
  padding: 0;
  margin: 0;
}

body {
  background-color: rgb(36, 36, 36);
}

body > div {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  justify-content: center;
}

img {
  width: 200px;
  height: 200px;
}

h1 {
  font-size: 18px;
  color: white;
  font-weight: bold;
  margin: 0;
}

p {
  color: white;
  opacity: 0.7;
  margin: 0;
}

code {
  font-size: 12px;
  padding: 2px 4px;
  background-color: #ffffff24;
  border-radius: 2px;
}
</style> -->
