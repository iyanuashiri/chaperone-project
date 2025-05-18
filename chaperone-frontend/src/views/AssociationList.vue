<template>
  <NavBar></NavBar>
  
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 flex flex-col items-center justify-center p-4 text-gray-100">
    <div class="bg-slate-800 shadow-2xl rounded-xl p-6 md:p-10 w-full max-w-2xl">
      <h1 class="text-3xl md:text-4xl font-bold text-center text-sky-400 mb-8">Vocabulary Quiz</h1>

      <div v-if="isLoading" class="text-center py-10">
        <svg class="animate-spin h-10 w-10 text-sky-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="mt-4 text-lg">Loading questions...</p>
      </div>

      <!-- #### -->
      <div v-else-if="currentAssociation" class="space-y-6">
        <div class="text-center">
          <p class="text-sm text-gray-400 mb-1">Question {{ currentQuestionIndex + 1 }} of {{ associations.length }}</p>
          <p class="text-xl md:text-2xl font-semibold text-gray-200">What is the meaning of:</p>
          <p class="text-3xl md:text-4xl font-bold text-sky-400 my-3">{{ currentAssociation.vocabulary.word }}</p>
        </div>

        <div class="space-y-3">
          <button v-for="option in currentAssociation.options" :key="option.id" @click="selectOption(option)" :disabled="isAnswered" class="w-full text-left p-4 rounded-lg border-2 transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-opacity-50" :class="getOptionClasses(option)">
            <span class="font-medium">{{ option.option }}</span>
            <span v-if="option.meaning" class="text-sm text-gray-400 block ml-1"> ({{ option.meaning }})</span>
          </button>
        </div>

        <div v-if="isAnswered" class="mt-6 text-center">
          <p class="text-xl font-semibold mb-2" :class="feedbackMessage.startsWith('Correct') ? 'text-green-400' : 'text-red-400'">{{ feedbackMessage }}</p>
          <p v-if="!selectedOptionIsCorrect" class="text-gray-300">The correct answer was: <span class="font-semibold text-green-400">{{ correctAnswerText }}</span></p>
          <button @click="nextQuestion" class="mt-4 px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg shadow-md transition-colors duration-150">{{ currentQuestionIndex === associations.length - 1 ? 'Finish Quiz' : 'Next Question' }}</button>
        </div>
      </div>
      
    </div>

  </div>
</template>


<script>
import NavBar from '../components/NavBar.vue';
import api from '../api.js';


export default {
  name: 'association-list',
  components: {
    NavBar,
  },
  data() {
    return {
      currentQuestionIndex: 0,
      selectedOption: null,
      isAnswered: false,
      feedbackMessage: '',
      isLoading: true,
      score: 0,

      associations: []
    };
  },
  computed: {
    currentAssociation() {
      if (this.associations.length > 0 && this.currentQuestionIndex < this.associations.length) {
        return this.associations[this.currentQuestionIndex];
      }
      return null;
    },
    selectedOptionIsCorrect() {
      return this.selectedOption ? this.selectedOption.is_correct : false;
    },
    correctAnswerText() {
      if (!this.currentAssociation || !this.isAnswered) return '';
      const correctOpt = this.currentAssociation.options.find(opt => opt.is_correct);
      return correctOpt ? correctOpt.option : 'N/A';
    }
  },
  methods: {
    async fetchAssociations() {
      this.isLoading = true;
      this.currentQuestionIndex = 0;
      try {
        const response = await api.getAssociations();
        this.associations = response;
        // Optional: Shuffle or filter
        // this.associations = response.data.filter(a => a.status === 'PENDING').sort(() => Math.random() - 0.5);
      } catch (error) {

        console.error("Error fetching associations:", error);
        this.associations = [];
      } finally {
        this.isLoading = false;
        this.resetQuestionState();
      }
    },
    async selectOption(option) {
      if (this.isAnswered) return;

      this.selectedOption = option;
      this.isAnswered = true;
      const associationId = this.currentAssociation.id;

      if (option.is_correct) {
        this.feedbackMessage = 'Correct!';
        try {
          await api.updateCorrectAssociation(associationId);
        } catch (error) {
          console.error("Error updating association to correct:", error);
          this.feedbackMessage = 'Correct! (But failed to save progress)';
        }
      } else {
        this.feedbackMessage = 'Incorrect!';
        try {
          await api.updateIncorrectAssociation(associationId);
        } catch (error) {
          console.error("Error updating association to incorrect:", error);
        }
      }
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.associations.length - 1) {
        this.currentQuestionIndex++;
        this.resetQuestionState();
      } else {
        
      }
    },
    resetQuestionState() {
      this.selectedOption = null;
      this.isAnswered = false;
      this.feedbackMessage = '';
    },
    getOptionClasses(option) {
      let classes = 'border-slate-600 bg-slate-700 hover:bg-slate-600 hover:border-sky-500'; // Default

      if (this.isAnswered) {
        if (option.is_correct) {
          classes = 'bg-green-500 border-green-700 text-white cursor-not-allowed';
        } else if (option.id === this.selectedOption?.id && !option.is_correct) {
          classes = 'bg-red-500 border-red-700 text-white cursor-not-allowed';
        } else {
          classes = 'bg-slate-700 border-slate-600 text-gray-400 cursor-not-allowed opacity-70';
        }
      } else {
        classes += ' cursor-pointer';
      }
      return classes;
    }
    
  },
  mounted() {
    this.fetchAssociations();
  }
};
</script>

<style scoped>

</style>