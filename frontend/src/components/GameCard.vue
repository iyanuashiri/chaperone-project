<template>
  <div class="bg-white shadow-lg rounded-lg overflow-hidden transform hover:scale-105 transition-transform duration-300 ease-in-out">
    <div class="p-6">
      <h3 class="text-2xl font-semibold text-gray-800 mb-2">{{ title }}</h3>
      <p class="text-gray-600 text-sm mb-4">{{ description }}</p>
      <button @click="navigateToGame" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition-colors duration-300">
        Play Game
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameCard',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    gamePath: {
      type: String, // Or Object if using named routes with params
      required: true
    }
  },
  methods: {
    navigateToGame() {
      // Assuming you are using Vue Router
      // You might need to adjust this based on your routing setup
      this.$router.push(this.gamePath);
    }
  }
};
</script>

<style scoped>
/* Add any specific styles for the game card here if needed */
/* Tailwind CSS classes are used primarily for styling */
</style>
