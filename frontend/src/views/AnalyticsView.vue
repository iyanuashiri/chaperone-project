<template>
  <NavBar />

  <main class="min-h-screen bg-[#f7f6f1] px-5 py-8 text-stone-900 sm:px-8 lg:ml-64 lg:px-12 lg:py-11">
    <div class="mx-auto max-w-6xl">
      <div class="mb-9 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Your journey</p>
          <h1 class="text-3xl font-semibold tracking-tight sm:text-4xl">Progress, at your pace.</h1>
          <p class="mt-2 text-sm text-stone-500">A look at the pauses and practice you’ve made time for.</p>
        </div>
        <RouterLink
          :to="{ name: 'game-play' }"
          class="rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-700"
        >
          Take a math pause <span aria-hidden="true" class="ml-2">→</span>
        </RouterLink>
      </div>

      <div v-if="isLoading" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <div v-for="item in 6" :key="item" class="h-32 animate-pulse rounded-2xl border border-stone-200 bg-white"></div>
      </div>

      <div v-else-if="!authenticated" class="rounded-2xl border border-stone-200 bg-white p-8">
        <p class="font-semibold">Sign in to see your progress.</p>
        <RouterLink :to="{ name: 'sign-in' }" class="mt-4 inline-flex rounded-full bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-violet-700">
          Sign in
        </RouterLink>
      </div>

      <div v-else-if="errorMessage" role="alert" class="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-sm text-rose-800">
        <p>{{ errorMessage }}</p>
        <button type="button" class="mt-3 font-bold underline" @click="fetchAnalytics">Try again</button>
      </div>

      <div v-else-if="summary" class="space-y-6">
        <section class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Challenges answered</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-violet-50 text-violet-700">✳</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ summary.total_attempts }}</p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Correct answers</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-lime-100 text-stone-800">✓</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ summary.total_correct }}</p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Accuracy</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-sky-50 text-sky-700">%</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ (summary.accuracy * 100).toFixed(0) }}<span class="ml-0.5 text-2xl text-stone-400">%</span></p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Current streak</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-orange-50 text-orange-600">↗</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ summary.current_streak }}<span class="ml-2 text-sm font-medium text-stone-400">days</span></p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Points earned</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-amber-50 text-amber-700">✦</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ summary.total_points }}</p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-xs font-semibold text-stone-500">Practice sessions</p>
              <span class="grid h-9 w-9 place-items-center rounded-xl bg-stone-100 text-stone-700">◷</span>
            </div>
            <p class="mt-5 text-4xl font-semibold tracking-tight">{{ summary.total_sessions }}</p>
          </article>
        </section>

        <section class="rounded-2xl border border-stone-200 bg-white p-5 sm:p-7">
          <div class="mb-6 flex flex-wrap items-end justify-between gap-3">
            <div>
              <p class="text-xs font-bold uppercase tracking-[0.14em] text-violet-600">Consistency, not perfection</p>
              <h2 class="mt-1 text-xl font-semibold tracking-tight">Daily activity</h2>
            </div>
            <span class="text-xs text-stone-400">Last 14 days · challenges answered</span>
          </div>

          <div v-if="last14Days.length" class="flex h-44 items-end gap-1.5 sm:gap-3">
            <div v-for="(day, index) in last14Days" :key="day.date || index" class="flex h-full min-w-0 flex-1 flex-col items-center justify-end gap-2">
              <span v-if="day.attempts" class="text-[10px] font-semibold text-stone-500">{{ day.attempts }}</span>
              <div
                class="w-full max-w-10 rounded-t-md transition-all"
                :class="day.attempts > 0 ? 'bg-violet-500' : 'bg-stone-100'"
                :style="{ height: barHeight(day.attempts) }"
                :title="`${day.date}: ${day.attempts} challenges, ${day.correct} correct`"
              ></div>
              <span class="text-[9px] font-medium text-stone-400 sm:text-[10px]">{{ dayLabel(day.date, index) }}</span>
            </div>
          </div>
          <div v-else class="rounded-xl bg-stone-50 p-5 text-sm text-stone-500">
            No challenge activity yet. <RouterLink :to="{ name: 'game-play' }" class="font-semibold text-violet-700 hover:text-violet-900">Try a quick math challenge.</RouterLink>
          </div>
        </section>

        <section v-if="siteStats.length" class="rounded-2xl border border-stone-200 bg-white p-5 sm:p-7">
          <div class="mb-5">
            <p class="text-xs font-bold uppercase tracking-[0.14em] text-violet-600">Your browsing</p>
            <h2 class="mt-1 text-xl font-semibold tracking-tight">Where you paused</h2>
          </div>
          <ul class="divide-y divide-stone-100">
            <li v-for="site in siteStats" :key="site.site_url" class="flex flex-wrap items-center justify-between gap-2 py-3">
              <span class="truncate text-sm font-semibold text-stone-800">{{ siteLabel(site.site_url) }}</span>
              <span class="text-xs text-stone-500">{{ site.sessions }} session{{ site.sessions === 1 ? '' : 's' }} · {{ site.attempts }} challenge{{ site.attempts === 1 ? '' : 's' }}</span>
            </li>
          </ul>
        </section>
      </div>
    </div>
  </main>
</template>

<script>
import { RouterLink } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

export default {
  name: 'AnalyticsView',
  components: { NavBar, RouterLink },
  data() {
    return {
      authenticated: false,
      isLoading: true,
      summary: null,
      dailyStats: [],
      siteStats: [],
      errorMessage: '',
    }
  },
  computed: {
    last14Days() {
      if (!this.dailyStats.length) return []
      return this.dailyStats.slice(-14)
    },
  },
  methods: {
    barHeight(attempts) {
      const max = Math.max(1, ...this.last14Days.map(day => day.attempts))
      const percentage = (attempts / max) * 100
      return `${Math.max(percentage, attempts > 0 ? 8 : 4)}%`
    },
    dayLabel(date, index) {
      if (!date) return index + 1
      const parsedDate = new Date(`${date}T00:00:00`)
      return Number.isNaN(parsedDate.getTime())
        ? index + 1
        : parsedDate.toLocaleDateString(undefined, { weekday: 'short' }).slice(0, 2)
    },
    siteLabel(url) {
      if (!url || url === '(unknown)') return 'Unknown site'
      try {
        return new URL(url).hostname.replace(/^www\./, '')
      } catch {
        return url
      }
    },
    async fetchAnalytics() {
      this.isLoading = true
      this.errorMessage = ''
      try {
        this.summary = await api.getStatsSummary()
        this.dailyStats = await api.getDailyStats(30)
        this.siteStats = await api.getSiteStats()
      } catch (error) {
        console.error('Error fetching analytics:', error)
        if (error.response?.status === 401) {
          this.authenticated = false
        } else {
          this.errorMessage = 'Your analytics could not be loaded. Please try again.'
        }
      } finally {
        this.isLoading = false
      }
    },
  },
  mounted() {
    this.authenticated = !!localStorage.getItem('accessToken')
    if (this.authenticated) {
      this.fetchAnalytics()
    } else {
      this.isLoading = false
    }
  },
}
</script>
