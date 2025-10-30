<template>
    <NavBar></NavBar>
    <div class="bg-gray-100 p-8 w-full mr-4 ml-auto my-16 max-w-screen-lg">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">URL Management</h1>

        <div class="ml-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

            <form @submit.prevent="createUrl">
                <div class="mb-4">
                    <label for="url" class="block text-sm font-medium text-gray-700 mb-2">URL</label>
                    <input v-model="model.url" id="url"  type="url" placeholder="https://example.com" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" required/>
                </div>
                
                <div class="flex gap-3">
                    <button type="submit" class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200">Add URL</button>
                </div>
            </form>
        </div>
   
    </div>    
</template>    


<script>

import NavBar from '@/components/NavBar.vue';
import api from '@/api';


export default {
  name: 'UrlCreateView',
  components: {
    NavBar
  },
  data() {
    return {
      model: {}
    };
  },
  methods: {
    createUrl: async function () {
      api.createUrl(this.model)
      .then(response => {
        console.log(response)
        alert('URL has been created successfully')
        this.$router.push({ name: 'url-list' })
      })
      return 
    }
  }
};
</script>