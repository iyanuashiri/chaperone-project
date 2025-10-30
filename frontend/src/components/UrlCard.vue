<template>
  <div class="bg-white shadow-lg rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 ease-in-out">
    <div class="p-6">
      <h3 class="text-2xl font-semibold text-gray-800 mb-2">{{ title }}</h3>
      <p class="text-gray-600 text-sm mb-4">{{ description }}</p>
    </div>
  </div>
</template>

  
  <script>
  export default {
    name: 'URLCard',
    props: {
      title: {
        type: String,
        required: true
      },
      description: {
        type: String,
        required: true
      },
    },
    
  };
  </script>
  
  
  