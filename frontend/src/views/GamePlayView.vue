<template>
  <NavBar></NavBar>

  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 flex flex-col items-center justify-center p-4 text-gray-100">
    <div class="bg-slate-800 shadow-2xl rounded-xl p-6 md:p-10 w-full max-w-2xl">
      <h1 class="text-3xl md:text-4xl font-bold text-center text-sky-400 mb-2">Speed Bump Challenge</h1>
      <p class="text-center text-gray-400 mb-6">Adaptive math &amp; logic — difficulty adjusts to your accuracy</p>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center py-10">
        <svg class="animate-spin h-10 w-10 text-sky-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="mt-4 text-lg">Preparing your challenge...</p>
      </div>

      <!-- Not authenticated -->
      <div v-else-if="!authenticated" class="text-center py-10">
        <p class="text-xl text-gray-300 mb-4">You need to sign in to play.</p>
        <button @click="$router.push({ name: 'sign-in' })" class="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg">
          Sign In
        </button>
      </div>

      <!-- Start screen -->
      <div v-else-if="!sessionStarted" class="text-center py-10 space-y-6">
        <div class="flex justify-center gap-6">
          <div class="text-center">
            <p class="text-4xl font-bold text-sky-400">{{ roundsPlayed }}</p>
            <p class="text-sm text-gray-400">Rounds</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-bold text-emerald-400">{{ score }}</p>
            <p class="text-sm text-gray-400">Points</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-bold text-amber-400">{{ bestStreak }}</p>
            <p class="text-sm text-gray-400">Best Streak</p>
          </div>
        </div>
        <div class="flex justify-center gap-4">
          <button @click="startGame('math')" class="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg shadow-md transition-colors duration-150">
            Start Math Challenge
          </button>
          <button @click="startGame('logic')" class="px-6 py-3 bg-violet-500 hover:bg-violet-600 text-white font-semibold rounded-lg shadow-md transition-colors duration-150">
            Start Logic Challenge
          </button>
        </div>
      </div>

      <!-- Active question -->
      <div v-else-if="currentChallenge" class="space-y-6">
        <div class="flex items-center justify-between">
          <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                :class="challengeType === 'logic' ? 'bg-violet-500/20 text-violet-300' : 'bg-sky-500/20 text-sky-300'">
            {{ challengeType }} · Level {{ currentDifficulty }}
          </span>
          <span class="text-sm text-gray-400">Round {{ roundsPlayed + 1 }}</span>
        </div>

        <div class="text-center">
          <p class="text-2xl md:text-3xl font-semibold text-gray-200 leading-snug">{{ currentChallenge.prompt }}</p>
        </div>

        <div class="space-y-3">
          <button v-for="option in currentOptions" :key="option" @click="selectOption(option)" :disabled="isAnswered"
                  class="w-full text-left p-4 rounded-lg border-2 transition-all duration-150 focus:outline-none"
                  :class="getOptionClasses(option)">
            <span class="font-medium text-lg">{{ option }}</span>
          </button>
        </div>

        <div v-if="isAnswered" class="mt-6 text-center">
          <p class="text-xl font-semibold mb-2" :class="lastFeedback.is_correct ? 'text-green-400' : 'text-red-400'">
            {{ lastFeedback.is_correct ? 'Correct!' : 'Incorrect!' }}
          </p>
          <p v-if="!lastFeedback.is_correct && lastFeedback.correct_answer" class="text-gray-300">
            The correct answer was: <span class="font-semibold text-green-400">{{ lastFeedback.correct_answer }}</span>
          </p>
          <p class="text-sm text-gray-400 mt-1">
            +{{ lastFeedback.points_awarded }} points · current streak {{ currentStreak }}
          </p>
          <button @click="nextChallenge" class="mt-4 px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg shadow-md transition-colors duration-150">
            Next Challenge
          </button>
        </div>
      </div>

      <!-- Session complete -->
      <div v-else class="text-center py-10 space-y-6">
        <h2 class="text-3xl font-bold text-green-400">Session Complete!</h2>
        <div class="flex justify-center gap-6">
          <div class="text-center">
            <p class="text-4xl font-bold text-sky-400">{{ roundsPlayed }}</p>
            <p class="text-sm text-gray-400">Rounds</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-bold text-emerald-400">{{ score }}</p>
            <p class="text-sm text-gray-400">Points</p>
          </div>
          <div class="text-center">
            <p class="text-4xl font-bold text-amber-400">{{ currentStreak }}</p>
            <p class="text-sm text-gray-400">Streak</p>
          </div>
        </div>
        <div class="flex justify-center gap-4">
          <button @click="startGame(challengeType)" class="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg">
            Play Again
          </button>
          <button @click="$router.push({ name: 'game-list' })" class="px-6 py-3 bg-gray-600 hover:bg-gray-500 text-white font-semibold rounded-lg">
            Back to Games
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
  name: 'GamePlayView',
  components: { NavBar },
  data() {
    return {
      authenticated: false,
      isLoading: false,
      sessionStarted: false,
      sessionId: null,
      challengeType: 'math',
      currentChallenge: null,
      currentOptions: [],
      currentDifficulty: 1,
      roundsPlayed: 0,
      score: 0,
      currentStreak: 0,
      bestStreak: 0,
      isAnswered: false,
      selectedOption: null,
      lastFeedback: {},
      roundStartTime: null,
    };
  },
  computed: {
    // Placeholder to keep template reactive while no question is active
    sessionComplete() {
      return this.sessionStarted && !this.currentChallenge;
    }
  },
  methods: {
    async fetchChallenge() {
      this.isLoading = true;
      this.isAnswered = false;
      this.selectedOption = null;
      this.lastFeedback = {};
      this.roundStartTime = Date.now();
      try {
        const challenge = await api.getChallenge(this.challengeType);
        this.currentChallenge = challenge;
        this.currentOptions = challenge.options || [];
        this.currentDifficulty = challenge.difficulty || 1;
      } catch (error) {
        console.error('Error fetching challenge:', error);
        this.currentChallenge = null;
        this.sessionStarted = false;
        alert('Could not load a challenge. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },
    async startGame(type) {
      this.challengeType = type;
      this.roundsPlayed = 0;
      this.score = 0;
      this.currentStreak = 0;
      this.bestStreak = 0;
      this.isLoading = true;
      try {
        const session = await api.startGameSession(window.location.href);
        this.sessionId = session.id;
        this.sessionStarted = true;
        await this.fetchChallenge();
      } catch (error) {
        console.error('Error starting game session:', error);
        alert('Could not start a game session. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },
    async selectOption(option) {
      if (this.isAnswered) return;
      this.selectedOption = option;
      this.isAnswered = true;

      const timeTakenS = (Date.now() - this.roundStartTime) / 1000;

      const payload = {
        challenge_type: this.challengeType,
        prompt: this.currentChallenge.prompt,
        options: this.currentOptions,
        answer: this.currentChallenge.answer,
        user_answer: option,
        difficulty: this.currentDifficulty,
        time_taken_s: Math.round(timeTakenS * 10) / 10,
      };

      try {
        const result = await api.submitGameAnswer(this.sessionId, payload);
        this.lastFeedback = result;
        this.score += result.points_awarded || 0;
        if (result.is_correct) {
          this.currentStreak++;
          this.bestStreak = Math.max(this.bestStreak, this.currentStreak);
        } else {
          this.currentStreak = 0;
        }
      } catch (error) {
        console.error('Error submitting answer:', error);
        this.lastFeedback = { is_correct: false, points_awarded: 0 };
      }
    },
    async nextChallenge() {
      this.roundsPlayed++;
      await this.fetchChallenge();
    },
    getOptionClasses(option) {
      if (!this.isAnswered) {
        return 'border-slate-600 bg-slate-700 hover:bg-slate-600 hover:border-sky-500 cursor-pointer';
      }

      if (option === this.currentChallenge.answer) {
        return 'bg-green-500 border-green-700 text-white cursor-not-allowed';
      }
      if (option === this.selectedOption) {
        return 'bg-red-500 border-red-700 text-white cursor-not-allowed';
      }
      return 'bg-slate-700 border-slate-600 text-gray-400 cursor-not-allowed opacity-70';
    }
  },
  mounted() {
    this.authenticated = !!localStorage.getItem('accessToken');
  }
};
</script>

<style scoped>
</style>
