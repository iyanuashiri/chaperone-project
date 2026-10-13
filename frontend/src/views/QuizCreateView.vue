<template>
    <NavBar></NavBar>
    <div class="bg-gray-100 min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-2xl">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Create a New Quiz</h1>
            <form @submit.prevent="createQuiz">
                <div class="mb-4">
                    <label for="content" class="block text-sm font-medium text-gray-700 mb-2">Content</label>
                    <textarea v-model="model.content" id="content" placeholder="Paste the text you want to create a quiz from..." rows="10" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500" required></textarea>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label for="questions" class="block text-sm font-medium text-gray-700 mb-2">Number of Questions</label>
                        <input v-model.number="model.number_of_questions" id="questions" type="number" min="1" max="20" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500" required/>
                    </div>
                    <div>
                        <label for="options" class="block text-sm font-medium text-gray-700 mb-2">Options per Question</label>
                        <input v-model.number="model.number_of_options" id="options" type="number" min="2" max="6" class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-500" required/>
                    </div>
                </div>
                <div class="flex">
                    <button type="submit" :disabled="isSubmitting" class="w-full bg-sky-600 text-white py-3 px-4 rounded-md hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 transition duration-200 disabled:bg-gray-400">
                        {{ isSubmitting ? 'Generating Quiz...' : 'Generate Quiz' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import api from '@/api';

export default {
  name: 'QuizCreateView',
  components: { NavBar },
  data() {
    return {
      model: {
        content: '',
        number_of_questions: 5,
        number_of_options: 4
      },
      isSubmitting: false
    };
  },
  methods: {
    async createQuiz() {
      this.isSubmitting = true;
      try {
        await api.createQuiz(this.model);
        alert('Quiz has been created successfully!');
        this.$router.push({ name: 'quiz-list' });
      } catch (error) {
        console.error("Failed to create quiz:", error);
        alert('Failed to create quiz. Please try again.');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>