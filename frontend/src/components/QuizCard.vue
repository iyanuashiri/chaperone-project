<template>
  <div class="bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
    <div class="p-6 flex-grow">
      <h3 class="text-xl font-semibold text-gray-800 mb-2 truncate">{{ title }}</h3>
      <p class="text-gray-600 text-sm mb-4">{{ questionCount }} Questions</p>
    </div>
    <div class="p-4 bg-gray-50">
      <router-link :to="{ name: 'quiz-play', params: { id: quizId } }" class="w-full text-center bg-sky-500 hover:bg-sky-600 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200 block">
        Play Quiz
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuizCard',
  props: {
    title: {
      type: String,
      required: true
    },
    questionCount: {
      type: Number,
      required: true
    },
    quizId: {
      type: Number,
      required: true
    }
  }
};
</script>