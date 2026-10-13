<template>
  <NavBar></NavBar>

  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 p-4 text-gray-100">
    <div class="max-w-4xl mx-auto py-8">
      <h1 class="text-3xl md:text-4xl font-bold text-center text-sky-400 mb-8">Your Digital Wellbeing Analytics</h1>

      <div v-if="isLoading" class="text-center py-16">
        <svg class="animate-spin h-10 w-10 text-sky-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="mt-4 text-lg">Loading your stats...</p>
      </div>

      <div v-else-if="!authenticated" class="text-center py-16">
        <p class="text-xl text-gray-300 mb-4">Sign in to see your analytics.</p>
        <button @click="$router.push({ name: 'sign-in' })" class="px-6 py-3 bg-sky-500 hover:bg-sky-600 text-white font-semibold rounded-lg">
          Sign In
        </button>
      </div>

      <div v-else-if="summary" class="space-y-8">
        <!-- Summary cards -->
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-sky-400">{{ summary.total_sessions }}</p>
            <p class="text-sm text-gray-400 mt-1">Speed-Bump Sessions</p>
          </div>
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-emerald-400">{{ summary.total_attempts }}</p>
            <p class="text-sm text-gray-400 mt-1">Challenges Solved</p>
          </div>
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-violet-400">{{ (summary.accuracy * 100).toFixed(0) }}%</p>
            <p class="text-sm text-gray-400 mt-1">Accuracy</p>
          </div>
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-amber-400">{{ summary.current_streak }}</p>
            <p class="text-sm text-gray-400 mt-1">Day Streak</p>
          </div>
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-green-400">{{ summary.total_points }}</p>
            <p class="text-sm text-gray-400 mt-1">Total Points</p>
          </div>
          <div class="bg-slate-800 rounded-xl p-6 text-center">
            <p class="text-4xl font-bold text-pink-400">{{ summary.total_correct }}</p>
            <p class="text-sm text-gray-400 mt-1">Correct Answers</p>
          </div>
        </div>

        <!-- Daily activity bar chart (pure CSS) -->
        <div class="bg-slate-800 rounded-xl p-6">
          <h2 class="text-xl font-semibold text-gray-200 mb-4">Last 14 Days</h2>
          <div v-if="dailyStats.length" class="flex items-end gap-1 h-40">
            <div v-for="(day, i) in last14Days" :key="i" class="flex-1 flex flex-col items-center">
              <span class="text-xs text-gray-400 mb-1">{{ day.attempts }}</span>
              <div class="w-full rounded-t"
                   :style="{ height: barHeight(day.attempts) }"
                   :class="day.attempts > 0 ? 'bg-sky-500' : 'bg-slate-700'"
                   :title="`${day.date}: ${day.attempts} attempts, ${day.correct} correct`"></div>
            </div>
          </div>
          <p v-else class="text-gray-400 text-sm">No activity recorded yet. Play the <router-link :to="{ name: 'game-play' }" class="text-sky-400 underline">Speed Bump game</router-link> to build your streak!</p>
        </div>

        <!-- Top sites -->
        <div v-if="siteStats.length" class="bg-slate-800 rounded-xl p-6">
          <h2 class="text-xl font-semibold text-gray-200 mb-4">Where You Use Chaperone</h2>
          <ul class="space-y-2">
            <li v-for="site in siteStats" :key="site.site_url" class="flex items-center justify-between bg-slate-700 rounded-lg px-4 py-3">
              <span class="text-gray-200 truncate">{{ siteLabel(site.site_url) }}</span>
              <span class="text-sm text-gray-400">{{ site.sessions }} session{{ site.sessions === 1 ? '' : 's' }} · {{ site.attempts }} attempt{{ site.attempts === 1 ? '' : 's' }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import api from '../api.js';

export default {
  name: 'AnalyticsView',
  components: { NavBar },
  data() {
    return {
      authenticated: false,
      isLoading: true,
      summary: null,
      dailyStats: [],
      siteStats: [],
    };
  },
  computed: {
    last14Days() {
      if (!this.dailyStats.length) return [];
      // Backend returns the last N days oldest→newest; take the last 14
      return this.dailyStats.slice(-14);
    }
  },
  methods: {
    barHeight(attempts) {
      const max = Math.max(1, ...this.last14Days.map(d => d.attempts));
      const pct = (attempts / max) * 100;
      return `${Math.max(pct, attempts > 0 ? 8 : 4)}%`;
    },
    siteLabel(url) {
      if (!url || url === '(unknown)') return 'Unknown site';
      try {
        return new URL(url).hostname.replace(/^www\./, '');
      } catch (e) {
        return url;
      }
    },
    async fetchAnalytics() {
      this.isLoading = true;
      try {
        this.summary = await api.getStatsSummary();
        this.dailyStats = await api.getDailyStats(30);
        this.siteStats = await api.getSiteStats();
      } catch (error) {
        console.error('Error fetching analytics:', error);
        if (error.response && error.response.status === 401) {
          this.authenticated = false;
        }
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    this.authenticated = !!localStorage.getItem('accessToken');
    if (this.authenticated) {
      this.fetchAnalytics();
    } else {
      this.isLoading = false;
    }
  }
};
</script>

<style scoped>
</style>
