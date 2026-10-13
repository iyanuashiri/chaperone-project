<template>
  <router-link :to="{ name: 'quiz-create' }" class="bg-white shadow-lg rounded-lg p-6 flex flex-col items-center justify-center text-center border-2 border-dashed border-gray-300 hover:border-sky-500 hover:bg-sky-50 transition-colors duration-300 cursor-pointer">
    <div class="text-sky-500 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </div>
    <h3 class="text-xl font-semibold text-gray-700">{{ title }}</h3>
    <p class="text-gray-500 text-sm mt-1">{{ description }}</p>
  </router-link>
</template>

<script>
export default {
  name: 'NewQuizCard',
  props: {
    title: {
      type: String,
      default: 'Create New Quiz'
    },
    description: {
      type: String,
      default: 'Generate a quiz from text'
    }
  }
};
</script>