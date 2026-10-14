<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

const email = localStorage.getItem('email') || ''
const firstName = computed(() => email.split('@')[0]?.split(/[._-]/)[0] || 'there')
const authenticated = ref(!!localStorage.getItem('accessToken'))
const isLoading = ref(false)
const summary = ref(null)
const challengeMode = ref('math')
const errorMessage = ref('')

async function loadOverview() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    summary.value = await api.getStatsSummary()
    try {
      const user = await api.getMe()
      challengeMode.value = user.challenge_mode || 'math'
    } catch (error) {
      console.error('Error loading challenge preference:', error)
    }
  } catch (error) {
    console.error('Error loading your overview:', error)
    if (error.response?.status === 401) {
      authenticated.value = false
    } else {
      errorMessage.value = 'Your overview could not be loaded. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (authenticated.value) loadOverview()
})
</script>

<template>
  <NavBar />

  <main class="min-h-screen bg-[#f7f6f1] px-5 py-8 text-stone-900 sm:px-8 lg:ml-64 lg:px-12 lg:py-11">
    <div class="mx-auto max-w-6xl">
      <div class="mb-9 flex flex-wrap items-end justify-between gap-5">
        <div>
          <p class="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Your Chaperone</p>
          <h1 class="text-3xl font-semibold tracking-tight sm:text-4xl">A more mindful browser, {{ firstName }}.</h1>
          <p class="mt-2 text-sm text-stone-500">Take a breath. Make the next scroll a choice.</p>
        </div>
        <RouterLink
          :to="{ name: 'settings' }"
          class="rounded-full border border-stone-300 bg-white px-4 py-2.5 text-sm font-semibold text-stone-700 transition hover:border-violet-300 hover:text-violet-700"
        >
          Adjust your limits <span aria-hidden="true" class="ml-2">↗</span>
        </RouterLink>
      </div>

      <section class="relative overflow-hidden rounded-3xl bg-[#28252f] p-7 text-white sm:p-10">
        <div class="pointer-events-none absolute -right-16 -top-36 h-96 w-96 rounded-full border border-lime-200/20 shadow-[0_0_0_38px_rgba(201,250,116,0.04),0_0_0_76px_rgba(201,250,116,0.03)]"></div>
        <div class="relative grid items-center gap-9 lg:grid-cols-[1fr_280px]">
          <div class="max-w-2xl">
            <span class="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-[10px] font-bold uppercase tracking-[0.16em] text-lime-200">
              <span class="h-1.5 w-1.5 rounded-full bg-lime-300"></span>
              Your daily speed bump
            </span>
            <h2 class="mt-6 text-4xl font-semibold leading-[1.03] tracking-tight sm:text-5xl">
              Give your focus<br class="hidden sm:block" /> a quick workout.
            </h2>
            <p class="mt-4 max-w-lg text-sm leading-7 text-stone-300">
              <template v-if="challengeMode === 'synonym'">
                Try a fresh synonym challenge. Each answer helps you pause, reset, and choose what you want to do next.
              </template>
              <template v-else>
                Try a short adaptive math challenge. Each answer helps you pause, reset, and choose what you want to do next.
              </template>
            </p>
            <RouterLink
              :to="{ name: 'game-play' }"
              class="mt-7 inline-flex min-h-12 items-center gap-4 rounded-full bg-lime-200 px-5 text-sm font-bold text-stone-900 transition hover:-translate-y-0.5 hover:bg-lime-100"
            >
              Start a challenge <span aria-hidden="true" class="text-lg">→</span>
            </RouterLink>
          </div>
          <div class="hidden rounded-2xl border border-white/10 bg-white/[0.06] p-5 lg:block">
            <div class="flex items-center justify-between text-xs text-stone-300">
              <span>Quick brain break</span>
              <span class="rounded-md bg-violet-400/20 px-2 py-1 text-violet-200">{{ challengeMode === 'synonym' ? 'SYNONYM' : 'MATH' }}</span>
            </div>
            <template v-if="challengeMode === 'synonym'">
              <p class="my-8 text-center text-3xl font-semibold tracking-tight">A fresh word</p>
              <p class="rounded-lg bg-white/10 px-3 py-3 text-center text-xs text-stone-200">Generated for each pause</p>
            </template>
            <template v-else>
              <p class="my-8 text-center text-4xl font-semibold tracking-tight">8 × 7 <span class="text-lime-200">= ?</span></p>
              <div class="grid grid-cols-3 gap-2 text-center text-xs">
                <span class="rounded-lg border border-white/10 py-2 text-stone-300">54</span>
                <span class="rounded-lg bg-lime-200 py-2 font-bold text-stone-900">56</span>
                <span class="rounded-lg border border-white/10 py-2 text-stone-300">64</span>
              </div>
            </template>
            <p class="mt-4 text-center text-[10px] font-medium text-stone-400">A pause that puts you back in control.</p>
          </div>
        </div>
      </section>

      <section class="mt-8">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-stone-400">Your progress</p>
            <h2 class="mt-1 text-xl font-semibold tracking-tight">Small steps add up.</h2>
          </div>
          <RouterLink :to="{ name: 'analytics' }" class="text-sm font-semibold text-violet-700 hover:text-violet-900">
            View analytics <span aria-hidden="true">→</span>
          </RouterLink>
        </div>

        <div v-if="isLoading" class="grid gap-4 sm:grid-cols-3">
          <div v-for="item in 3" :key="item" class="h-32 animate-pulse rounded-2xl border border-stone-200 bg-white"></div>
        </div>

        <div v-else-if="!authenticated" class="rounded-2xl border border-stone-200 bg-white p-7">
          <p class="font-semibold">Sign in to see your progress.</p>
          <RouterLink :to="{ name: 'sign-in' }" class="mt-4 inline-flex rounded-full bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-violet-700">
            Sign in
          </RouterLink>
        </div>

        <div v-else-if="errorMessage" role="alert" class="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-sm text-rose-800">
          <p>{{ errorMessage }}</p>
          <button class="mt-3 font-bold underline" type="button" @click="loadOverview">Try again</button>
        </div>

        <div v-else-if="summary" class="grid gap-4 sm:grid-cols-3">
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <p class="text-xs font-semibold text-stone-500">Challenges answered</p>
            <p class="mt-4 text-4xl font-semibold tracking-tight">{{ summary.total_attempts }}</p>
            <p class="mt-1 text-xs text-stone-400">Every pause is progress.</p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <p class="text-xs font-semibold text-stone-500">Points earned</p>
            <p class="mt-4 text-4xl font-semibold tracking-tight">{{ summary.total_points }}</p>
            <p class="mt-1 text-xs text-stone-400">Keep showing up for yourself.</p>
          </article>
          <article class="rounded-2xl border border-stone-200 bg-white p-5">
            <p class="text-xs font-semibold text-stone-500">Current streak</p>
            <p class="mt-4 text-4xl font-semibold tracking-tight">{{ summary.current_streak }}<span class="ml-1 text-base font-medium text-stone-500">days</span></p>
            <p class="mt-1 text-xs text-stone-400">Consistency over perfection.</p>
          </article>
        </div>

        <div v-else class="rounded-2xl border border-stone-200 bg-white p-6 text-sm text-stone-500">
          Your progress summary is not available yet.
        </div>
      </section>

      <div class="mt-7 flex flex-wrap gap-x-6 gap-y-3 border-t border-stone-200 pt-5 text-xs text-stone-500">
        <RouterLink :to="{ name: 'game-play' }" class="font-semibold hover:text-violet-700">Practice a challenge</RouterLink>
        <RouterLink :to="{ name: 'settings' }" class="font-semibold hover:text-violet-700">Manage your websites and limits</RouterLink>
        <RouterLink :to="{ name: 'analytics' }" class="font-semibold hover:text-violet-700">Explore your activity</RouterLink>
      </div>
    </div>
  </main>
</template>
