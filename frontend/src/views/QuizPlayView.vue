<template>
  <NavBar></NavBar>
  
  
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 flex flex-col items-center justify-center p-4 text-gray-100">
    <div class="bg-slate-800 shadow-2xl rounded-xl p-6 md:p-10 w-full max-w-2xl">
      <h1 class="text-3xl md:text-4xl font-bold text-center text-sky-400 mb-8">Quiz in Progress</h1>

      <div v-if="isLoading" class="text-center py-10">
        <p>Loading Quiz...</p>
      </div>

      <div v-else-if="isQuizFinished" class="text-center">
        <h2 class="text-3xl font-bold text-green-400">Quiz Complete!</h2>
        <p class="text-xl mt-4">Your Score: {{ score }} out of {{ quiz.questions.length }}</p>
        <button @click="$router.push('/quiz-list')" class="mt-6 px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg">
          Back to Quizzes
        </button>
      </div>

      <div v-else-if="currentQuestion" class="space-y-6">
        <div class="text-center">
          <p class="text-sm text-gray-400 mb-1">Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}</p>
          <p class="text-xl md:text-2xl font-semibold text-gray-200">{{ currentQuestion.question }}</p>
        </div>

        <div class="space-y-3">
          <!-- Use the corrected 'options' field -->
          <button v-for="option in currentQuestion.question_options" :key="option.id" @click="selectOption(option)" :disabled="isAnswered" class="w-full text-left p-4 rounded-lg border-2 transition-all duration-150" :class="getOptionClasses(option)">
            <span class="font-medium">{{ option.option }}</span>
          </button>
        </div>

        <div v-if="isAnswered" class="mt-6 text-center">
          <p class="text-xl font-semibold mb-2" :class="feedback.is_correct ? 'text-green-400' : 'text-red-400'">
            {{ feedback.is_correct ? 'Correct!' : 'Incorrect!' }}
          </p>
          <p v-if="!feedback.is_correct" class="text-gray-300">The correct answer was: <span class="font-semibold text-green-400">{{ correctAnswerText }}</span></p>
          <button @click="nextQuestion" class="mt-4 px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg">
            {{ currentQuestionIndex === quiz.questions.length - 1 ? 'Finish Quiz' : 'Next Question' }}
          </button>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import api from '../api.js';

export default {
  name: 'QuizPlayView',
  components: { NavBar },
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      quiz: null,
      isLoading: true,
      currentQuestionIndex: 0,
      selectedOption: null,
      isAnswered: false,
      feedback: {}, // { is_correct: bool, correct_option_id: int }
      score: 0,
      isQuizFinished: false,
    };
  },
  computed: {
    currentQuestion() {
      return this.quiz?.questions[this.currentQuestionIndex];
    },
    correctAnswerText() {
      if (!this.isAnswered || !this.currentQuestion) return '';
      // Use the corrected 'options' field
      const correctOpt = this.currentQuestion.question_options.find(opt => opt.id === this.feedback.correct_option_id);
      return correctOpt ? correctOpt.option : 'N/A';
    }
  },
  methods: {
    async fetchQuiz() {
      this.isLoading = true;
      try {
        // This is inefficient but works without a dedicated 'get quiz by id' endpoint.
        const quizzes = await api.getQuizzes();
        this.quiz = quizzes.find(q => q.id == this.id);
        if (!this.quiz) {
          alert("Quiz not found.");
          this.$router.push('/quiz-list');
        }
      } catch (error) {
        console.error("Failed to fetch quiz:", error);
      } finally {
        this.isLoading = false;
      }
    },
    async selectOption(option) {
      if (this.isAnswered) return;

      this.selectedOption = option;
      this.isAnswered = true;
      
      try {
        const result = await api.selectQuizOption(this.quiz.id, this.currentQuestion.id, option.id);
        this.feedback = result;
        if (result.is_correct) {
          this.score++;
        }
      } catch (error) {
        console.error("Error selecting option:", error);
        alert("There was an error submitting your answer. Please try again.");
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.quiz.questions.length - 1) {
        this.currentQuestionIndex++;
        this.resetQuestionState();
      } else {
        this.isQuizFinished = true;
      }
    },
    resetQuestionState() {
      this.selectedOption = null;
      this.isAnswered = false;
      this.feedback = {};
    },
    getOptionClasses(option) {
      if (!this.isAnswered) {
        return 'border-slate-600 bg-slate-700 hover:bg-slate-600 hover:border-sky-500 cursor-pointer';
      }
      
      if (option.id === this.feedback.correct_option_id) {
        return 'bg-green-500 border-green-700 text-white cursor-not-allowed';
      }
      if (option.id === this.selectedOption.id) { // Incorrectly selected
        return 'bg-red-500 border-red-700 text-white cursor-not-allowed';
      }
      return 'bg-slate-700 border-slate-600 text-gray-400 cursor-not-allowed opacity-70';
    }
  },
  mounted() {
    this.fetchQuiz();
  }
};
</script>