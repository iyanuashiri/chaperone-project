<template>
    <section>
      <div class="bg-white rounded-lg shadow-md p-8 w-full mx-auto my-16 max-w-md">
          <h2 class="text-2xl font-semibold text-blue-600 mb-6">Sign Up</h2>
          <form>
            <div class="mb-4">
                <label for="name" class="block text-sm font-medium text-gray-600">Name</label>
                <input type="text" id="name" name="name" class="mt-1 p-2 w-full border rounded-md text-gray-800">
            </div>
              <div class="mb-4">
                  <label for="email" class="block text-sm font-medium text-gray-600">Email</label>
                  <input type="email" id="email" name="email" class="mt-1 p-2 w-full border rounded-md text-gray-800">
              </div>
              <div class="mb-6">
                  <label for="password" class="block text-sm font-medium text-gray-600">Password</label>
                  <input type="password" id="password" name="password" class="mt-1 p-2 w-full border rounded-md text-gray-800">
              </div>
              <button type="submit" class="w-full p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Sign Up</button>
          </form>
      </div>
  
    </section>
  
  </template>
  
  
  <script >
  import axios from 'axios'
  
  export default {
    name: 'sign-up',
    components: {},
    data () {
        return {
            page_title: 'Sign Up',
            model: {}
        }
    },
    methods: {
      signUp: async function () {
              let url = 'http://127.0.0.1:8000/api/auth/users/create/'
              axios.post(url, this.model).then(response => {
                  alert('Your account has been created successfully')
                  this.$router.push({ name: 'sign-in' })
              })
              .catch(error => {
                console.log(error)
              })
          }
  
    }
  }
  </script>