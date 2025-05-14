<template>

    <div class="bg-white rounded-lg shadow-md p-8 w-full mx-auto my-16 max-w-md">
        <h2 class="text-2xl font-semibold text-blue-600 mb-6">Sign In</h2>
        <form @submit.prevent="signIn">
            <div class="mb-4">
                <label for="email" class="block text-sm font-medium text-gray-600">Email</label>
                <input v-model="model.email" type="email" id="email" name="email" class="mt-1 p-2 w-full border rounded-md text-gray-800">
            </div>
            <div class="mb-6">
                <label for="password" class="block text-sm font-medium text-gray-600">Password</label>
                <input v-model="model.password" type="password" id="password" name="password" class="mt-1 p-2 w-full border rounded-md text-gray-800">
            </div>
            <button type="submit" class="w-full p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Sign In</button>
        </form>
    </div>
  
  </template>
  
  
  <script >
  import axios from 'axios'
  
  export default {
  name: 'sign-in',
  components: {},
  data () {
      return {
          page_title: 'Sign In',
          model: {}
      }
  },
  methods: {
    signIn: async function () {
      let url = 'http://127.0.0.1:8000/api/v1/auth/token/login/'
      axios.post(url, this.model).then(response => {
        localStorage.setItem('authToken', response.data.auth_token)
        localStorage.setItem('email', this.model.email)
        alert('You have logged in successfully')
        this.$router.push({ name: 'dashboard' })
      })
        .catch(error => {
          console.log(error)
        })
    }
  
  }
  }
  </script>