<template>
  <NavBar />

  <main class="min-h-screen bg-[#f7f6f1] px-5 py-8 text-stone-900 sm:px-8 lg:ml-64 lg:px-12 lg:py-11">
    <div class="mx-auto max-w-5xl">
      <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p class="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-violet-600">A mindful minute</p>
          <h1 class="text-3xl font-semibold tracking-tight sm:text-4xl">
            {{ challengeMode === 'synonym' ? 'Synonym challenge' : 'Math challenge' }}
          </h1>
          <p class="mt-2 text-sm text-stone-500">A quick brain break to bring you back to the moment.</p>
        </div>
        <RouterLink :to="{ name: 'game-list' }" class="text-sm font-semibold text-stone-500 hover:text-violet-700">
          <span aria-hidden="true">←</span> Overview
        </RouterLink>
      </div>

      <div v-if="isLoading" class="rounded-3xl border border-stone-200 bg-white px-6 py-20 text-center">
        <div class="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-violet-100 border-t-violet-600"></div>
        <p class="mt-5 text-sm font-medium text-stone-500">Preparing a fresh challenge…</p>
      </div>

      <div v-else-if="!authenticated" class="rounded-3xl border border-stone-200 bg-white px-6 py-16 text-center">
        <span class="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-violet-50 text-2xl text-violet-700">＋</span>
        <h2 class="mt-5 text-2xl font-semibold tracking-tight">Sign in to start a challenge.</h2>
        <p class="mt-2 text-sm text-stone-500">Your practice and progress are saved to your account.</p>
        <RouterLink :to="{ name: 'sign-in' }" class="mt-6 inline-flex rounded-full bg-violet-600 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-700">
          Sign in
        </RouterLink>
      </div>

      <div v-else-if="sessionFinished" class="rounded-3xl border border-stone-200 bg-white p-7 sm:p-10">
        <span class="inline-flex rounded-full bg-lime-100 px-3 py-1.5 text-xs font-bold text-lime-900">NICE WORK</span>
        <h2 class="mt-5 text-3xl font-semibold tracking-tight">You made space to pause.</h2>
        <p class="mt-2 text-sm text-stone-500">Here’s what you did in this practice session.</p>
        <div class="mt-8 grid gap-3 sm:grid-cols-3">
          <div class="rounded-2xl bg-stone-50 p-5">
            <p class="text-xs font-semibold text-stone-500">Challenges answered</p>
            <p class="mt-3 text-3xl font-semibold">{{ roundsPlayed }}</p>
          </div>
          <div class="rounded-2xl bg-stone-50 p-5">
            <p class="text-xs font-semibold text-stone-500">Points earned</p>
            <p class="mt-3 text-3xl font-semibold">{{ score }}</p>
          </div>
          <div class="rounded-2xl bg-stone-50 p-5">
            <p class="text-xs font-semibold text-stone-500">Best streak</p>
            <p class="mt-3 text-3xl font-semibold">{{ bestStreak }}</p>
          </div>
        </div>
        <div class="mt-8 flex flex-wrap gap-3">
          <button type="button" class="rounded-full bg-violet-600 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-700" @click="startGame">
            Practice again <span aria-hidden="true">→</span>
          </button>
          <RouterLink :to="{ name: 'analytics' }" class="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700 hover:bg-stone-50">
            View analytics
          </RouterLink>
        </div>
      </div>

      <div v-else-if="!sessionStarted" class="grid overflow-hidden rounded-3xl border border-stone-200 bg-white lg:grid-cols-[1fr_300px]">
        <div class="p-7 sm:p-10">
          <span class="inline-flex items-center gap-2 rounded-full bg-violet-50 px-3 py-1.5 text-xs font-bold text-violet-700">
            <span class="h-1.5 w-1.5 rounded-full bg-violet-500"></span>
            {{ challengeMode === 'synonym' ? 'AI-GENERATED SYNONYM' : 'ADAPTIVE MATH' }}
          </span>
          <h2 class="mt-6 max-w-xl text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">Give your attention a quick reset.</h2>
          <p class="mt-4 max-w-xl text-sm leading-7 text-stone-500">
            <template v-if="challengeMode === 'synonym'">
              Find the closest synonym in a fresh, AI-generated word challenge. Each answer builds your session score.
            </template>
            <template v-else>
              Solve short math challenges at your own pace. The difficulty responds to how you’re doing, and each answer builds your session score.
            </template>
          </p>
          <button
            type="button"
            class="mt-8 inline-flex min-h-12 items-center gap-4 rounded-full bg-stone-900 px-6 text-sm font-bold text-white transition hover:-translate-y-0.5 hover:bg-violet-700"
            @click="startGame"
          >
            Start a challenge <span aria-hidden="true" class="text-lg">→</span>
          </button>
        </div>
        <div class="flex min-h-64 flex-col justify-center bg-[#28252f] p-7 text-white sm:p-10 lg:p-8">
          <p class="text-xs font-bold uppercase tracking-[0.15em] text-lime-200">A sample pause</p>
          <template v-if="challengeMode === 'synonym'">
            <p class="my-8 text-center text-3xl font-semibold tracking-tight">A fresh word</p>
            <p class="rounded-xl bg-white/10 py-3 text-center text-sm text-stone-200">Generated when your challenge begins</p>
          </template>
          <template v-else>
            <p class="my-8 text-center text-5xl font-semibold tracking-tight">8 × 7 <span class="text-lime-200">= ?</span></p>
            <div class="grid grid-cols-3 gap-2 text-center text-sm">
              <span class="rounded-xl border border-white/15 py-3 text-stone-300">54</span>
              <span class="rounded-xl bg-lime-200 py-3 font-bold text-stone-900">56</span>
              <span class="rounded-xl border border-white/15 py-3 text-stone-300">64</span>
            </div>
          </template>
        </div>
      </div>

      <section v-else-if="currentChallenge" class="grid gap-5 lg:grid-cols-[1fr_290px]">
        <div class="rounded-3xl border border-stone-200 bg-white p-6 sm:p-9">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <span class="inline-flex items-center gap-2 rounded-full bg-violet-50 px-3 py-1.5 text-xs font-bold text-violet-700">
              <span class="h-1.5 w-1.5 rounded-full bg-violet-500"></span>
              {{ challengeType === 'synonym' ? 'SYNONYM' : 'MATH' }} · LEVEL {{ currentDifficulty }}
            </span>
            <span class="text-xs font-semibold text-stone-400">Challenge {{ roundsPlayed + 1 }}</span>
          </div>

          <div class="my-10 border-y border-stone-100 py-10 text-center sm:my-12 sm:py-12">
            <p class="mb-3 text-xs font-bold uppercase tracking-[0.15em] text-stone-400">Take a moment</p>
            <h2 class="text-3xl font-semibold leading-snug tracking-tight sm:text-4xl">{{ currentChallenge.prompt }}</h2>
          </div>

          <div class="grid gap-3 sm:grid-cols-2">
            <button
              v-for="(option, index) in currentOptions"
              :key="option"
              type="button"
              :disabled="isAnswered"
              class="flex min-h-14 items-center gap-4 rounded-xl border px-4 text-left transition disabled:cursor-default"
              :class="getOptionClasses(option)"
              @click="selectOption(option)"
            >
              <span class="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-stone-100 text-xs font-bold text-stone-500">{{ String.fromCharCode(65 + index) }}</span>
              <span class="font-semibold">{{ option }}</span>
            </button>
          </div>

          <div v-if="isAnswered" class="mt-6 rounded-2xl p-5" :class="lastFeedback.is_correct ? 'bg-lime-50' : 'bg-rose-50'">
            <p class="font-bold" :class="lastFeedback.is_correct ? 'text-lime-900' : 'text-rose-800'">
              {{ lastFeedback.is_correct ? 'That’s right. Nice work.' : 'Not quite this time.' }}
            </p>
            <p v-if="!lastFeedback.is_correct && lastFeedback.correct_answer" class="mt-1 text-sm text-stone-600">
              The correct answer is <b>{{ lastFeedback.correct_answer }}</b>.
            </p>
            <p v-if="answerError" role="alert" class="mt-2 text-sm text-rose-700">{{ answerError }}</p>
            <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
              <span class="text-xs font-semibold text-stone-600">+{{ lastFeedback.points_awarded || 0 }} points · {{ currentStreak }} in a row</span>
              <button type="button" class="rounded-full bg-stone-900 px-4 py-2.5 text-xs font-bold text-white hover:bg-violet-700" @click="nextChallenge">
                Next challenge <span aria-hidden="true">→</span>
              </button>
            </div>
          </div>

          <p v-if="errorMessage" role="alert" class="mt-5 rounded-xl bg-rose-50 p-4 text-sm text-rose-700">{{ errorMessage }}</p>
          <div v-if="!isAnswered" class="mt-6 flex justify-end">
            <button type="button" class="text-xs font-semibold text-stone-400 hover:text-stone-700" @click="finishSession">
              Finish practice
            </button>
          </div>
        </div>

        <aside class="flex flex-col gap-4">
          <div class="rounded-3xl bg-[#28252f] p-6 text-white">
            <p class="text-xs font-bold uppercase tracking-[0.15em] text-stone-400">This session</p>
            <div class="mt-6 grid grid-cols-2 gap-4">
              <div>
                <p class="text-3xl font-semibold">{{ score }}</p>
                <p class="mt-1 text-xs text-stone-400">Points</p>
              </div>
              <div>
                <p class="text-3xl font-semibold">{{ currentStreak }}</p>
                <p class="mt-1 text-xs text-stone-400">Current streak</p>
              </div>
              <div>
                <p class="text-3xl font-semibold">{{ roundsPlayed }}</p>
                <p class="mt-1 text-xs text-stone-400">Answered</p>
              </div>
              <div>
                <p class="text-3xl font-semibold">{{ bestStreak }}</p>
                <p class="mt-1 text-xs text-stone-400">Best streak</p>
              </div>
            </div>
          </div>
          <div class="rounded-3xl border border-stone-200 bg-white p-6">
            <p class="text-xs font-bold uppercase tracking-[0.15em] text-stone-400">A gentle reminder</p>
            <p class="mt-3 text-sm leading-6 text-stone-600">This is a pause, not a test. Take your time and choose what feels right next.</p>
            <RouterLink :to="{ name: 'settings' }" class="mt-4 inline-flex text-xs font-bold text-violet-700 hover:text-violet-900">
              Adjust your limits <span aria-hidden="true" class="ml-2">→</span>
            </RouterLink>
          </div>
        </aside>
      </section>

      <p v-if="!isLoading && authenticated && errorMessage && !currentChallenge" role="alert" class="mt-5 rounded-xl bg-rose-50 p-4 text-sm text-rose-700">
        {{ errorMessage }}
        <button type="button" class="ml-2 font-bold underline" @click="startGame">Try again</button>
      </p>
    </div>
  </main>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

export default {
  name: 'GamePlayView',
  components: { NavBar },
  data() {
    return {
      authenticated: false,
      isLoading: false,
      sessionStarted: false,
      sessionFinished: false,
      sessionId: null,
      challengeType: 'math',
      challengeMode: 'math',
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
      errorMessage: '',
      answerError: '',
    }
  },
  methods: {
    async fetchChallenge() {
      this.isLoading = true
      this.isAnswered = false
      this.selectedOption = null
      this.lastFeedback = {}
      this.errorMessage = ''
      this.answerError = ''
      this.roundStartTime = Date.now()
      try {
        const challenge = await api.getChallenge()
        this.currentChallenge = challenge
        this.challengeType = challenge.type
        this.challengeMode = challenge.type
        this.currentOptions = challenge.options || []
        this.currentDifficulty = challenge.difficulty || 1
      } catch (error) {
        console.error('Error fetching challenge:', error)
        this.currentChallenge = null
        this.sessionStarted = false
        this.errorMessage = 'Could not load a challenge. Check your connection and try again.'
      } finally {
        this.isLoading = false
      }
    },
    async startGame() {
      this.roundsPlayed = 0
      this.score = 0
      this.currentStreak = 0
      this.bestStreak = 0
      this.sessionFinished = false
      this.errorMessage = ''
      this.isLoading = true
      try {
        const session = await api.startGameSession(window.location.href)
        this.sessionId = session.id
        this.sessionStarted = true
        await this.fetchChallenge()
      } catch (error) {
        console.error('Error starting challenge session:', error)
        this.errorMessage = 'Could not start a challenge session. Check your connection and try again.'
      } finally {
        this.isLoading = false
      }
    },
    async selectOption(option) {
      if (this.isAnswered) return
      this.selectedOption = option
      this.isAnswered = true
      this.answerError = ''

      const timeTakenS = (Date.now() - this.roundStartTime) / 1000
      const payload = {
        challenge_type: this.challengeType,
        prompt: this.currentChallenge.prompt,
        options: this.currentOptions,
        answer: this.currentChallenge.answer,
        user_answer: option,
        difficulty: this.currentDifficulty,
        time_taken_s: Math.round(timeTakenS * 10) / 10,
      }

      try {
        const result = await api.submitGameAnswer(this.sessionId, payload)
        this.lastFeedback = result
        this.score += result.points_awarded || 0
        this.roundsPlayed++
        if (result.is_correct) {
          this.currentStreak++
          this.bestStreak = Math.max(this.bestStreak, this.currentStreak)
        } else {
          this.currentStreak = 0
        }
      } catch (error) {
        console.error('Error submitting math challenge answer:', error)
        this.answerError = 'Your answer could not be saved. Please try the next challenge.'
        this.lastFeedback = { is_correct: false, points_awarded: 0 }
      }
    },
    async nextChallenge() {
      await this.fetchChallenge()
    },
    finishSession() {
      this.sessionFinished = true
      this.sessionStarted = false
      this.currentChallenge = null
    },
    getOptionClasses(option) {
      if (!this.isAnswered) {
        return 'border-stone-200 bg-white text-stone-800 hover:border-violet-400 hover:bg-violet-50'
      }
      if (option === this.currentChallenge.answer) {
        return 'border-lime-400 bg-lime-50 text-stone-900'
      }
      if (option === this.selectedOption) {
        return 'border-rose-300 bg-rose-50 text-rose-800'
      }
      return 'border-stone-100 bg-stone-50 text-stone-400 opacity-70'
    },
  },
  mounted() {
    this.authenticated = !!localStorage.getItem('accessToken')
    if (this.authenticated) {
      api.getMe()
        .then(user => {
          this.challengeMode = user.challenge_mode || 'math'
          this.challengeType = this.challengeMode
        })
        .catch(error => {
          console.error('Error loading challenge preference:', error)
        })
    }
  },
}
</script>
