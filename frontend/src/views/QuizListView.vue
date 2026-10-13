<template>
  <NavBar></NavBar>
  <div class="bp-8 w-full mr-4 ml-auto my-16 max-w-screen-lg">
    <!-- <div class="max-w-screen-lg mx-auto"> -->
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Quiz Management</h1>
      
      <div v-if="isLoading" class="text-center py-10">
        <p>Loading quizzes...</p>
      </div>
      
      <div v-else class="ml-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <NewQuizCard />
        <QuizCard 
          v-for="quiz in quizzes" 
          :key="quiz.id" 
          :title="quiz.content" 
          :questionCount="quiz.questions.length"
          :quizId="quiz.id"
        />
      </div>
    <!-- </div> -->
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import NewQuizCard from '@/components/NewQuizCard.vue';
import QuizCard from '@/components/QuizCard.vue';
import api from '../api.js';

export default {
  name: 'QuizListView',
  components: { 
    NavBar,
    NewQuizCard,
    QuizCard
  },
  data() {
    return {
      quizzes: [],
      isLoading: true,
    };
  },
  async mounted() {
    try {
      this.quizzes = await api.getQuizzes();
    } catch (error) {
      console.error("Failed to fetch quizzes:", error);
    } finally {
      this.isLoading = false;
    }
  },
};
</script>