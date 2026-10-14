<template>
  <NavBar />

  <main class="min-h-screen bg-[#f7f6f1] px-5 py-8 text-stone-900 sm:px-8 lg:ml-64 lg:px-12 lg:py-11">
    <div class="mx-auto max-w-4xl">
      <div class="mb-9">
        <p class="mb-2 text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Make it yours</p>
        <h1 class="text-3xl font-semibold tracking-tight sm:text-4xl">Your settings</h1>
        <p class="mt-2 max-w-xl text-sm leading-6 text-stone-500">Choose when Chaperone checks in, which challenge you prefer, and where to pause.</p>
      </div>

      <div v-if="isLoading" class="rounded-2xl border border-stone-200 bg-white p-8 text-sm text-stone-500">
        Loading your settings…
      </div>

      <div v-else-if="!authenticated" class="rounded-2xl border border-stone-200 bg-white p-8">
        <p class="font-semibold">Sign in to manage your settings.</p>
        <button
          type="button"
          class="mt-4 rounded-full bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-violet-700"
          @click="$router.push({ name: 'sign-in' })"
        >
          Sign in
        </button>
      </div>

      <div v-else class="space-y-5">
        <section class="rounded-2xl border border-stone-200 bg-white p-6 sm:p-8">
          <div class="flex items-start gap-4">
            <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-violet-50 text-lg text-violet-700">◷</span>
            <div>
              <h2 class="text-lg font-semibold tracking-tight">Browsing time limit</h2>
              <p class="mt-1 text-sm leading-6 text-stone-500">How long to browse a site before Chaperone offers a quick speed-bump challenge.</p>
            </div>
          </div>

          <div class="mt-6 flex max-w-lg flex-col gap-3 sm:flex-row">
            <label for="time-limit" class="sr-only">Browsing time limit</label>
            <input
              id="time-limit"
              v-model="timeLimit"
              type="number"
              min="1"
              step="1"
              required
              :placeholder="timeUnit === 'minutes' ? 'Enter minutes' : 'Enter seconds'"
              class="min-h-12 min-w-0 flex-1 rounded-xl border border-stone-300 bg-white px-4 text-sm text-stone-900 outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
            >
            <label for="time-unit" class="sr-only">Time unit</label>
            <select
              id="time-unit"
              v-model="timeUnit"
              class="min-h-12 rounded-xl border border-stone-300 bg-white px-4 text-sm font-medium text-stone-700 outline-none focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
            >
              <option value="minutes">minutes</option>
              <option value="seconds">seconds</option>
            </select>
          </div>
          <p class="mt-2 text-xs text-stone-400">You can change this any time. The limit is stored in seconds.</p>
        </section>

        <section class="rounded-2xl border border-stone-200 bg-white p-6 sm:p-8">
          <div class="flex items-start gap-4">
            <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-lime-100 text-lg text-stone-800">✳</span>
            <div>
              <h2 class="text-lg font-semibold tracking-tight">Your speed-bump challenge</h2>
              <p class="mt-1 text-sm leading-6 text-stone-500">Choose the kind of quick pause you’ll see in the app and browser extension.</p>
            </div>
          </div>

          <label for="challenge-mode" class="sr-only">Challenge type</label>
          <select
            id="challenge-mode"
            v-model="challengeMode"
            class="mt-6 min-h-12 w-full max-w-lg rounded-xl border border-stone-300 bg-white px-4 text-sm font-medium text-stone-700 outline-none focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
          >
            <option value="math">Math challenge</option>
            <option value="synonym">Synonym challenge (AI-generated)</option>
          </select>
          <p class="mt-2 text-xs text-stone-400">Synonym challenges are generated on the server using Amazon Bedrock.</p>
        </section>

        <section class="rounded-2xl border border-stone-200 bg-white p-6 sm:p-8">
          <div class="flex items-start gap-4">
            <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-lime-100 text-lg text-stone-800">◎</span>
            <div>
              <h2 class="text-lg font-semibold tracking-tight">Websites to pause on</h2>
              <p class="mt-1 text-sm leading-6 text-stone-500">Add the sites where a thoughtful pause would be helpful.</p>
            </div>
          </div>

          <div v-if="urls.length" class="mt-6 divide-y divide-stone-100 border-y border-stone-100">
            <div v-for="item in urls" :key="item.id" class="flex items-center justify-between gap-4 py-3">
              <div class="min-w-0">
                <span class="block truncate text-sm font-semibold text-stone-800">{{ displayUrl(item.url) }}</span>
                <span v-if="item.title" class="mt-0.5 block truncate text-xs text-stone-400">{{ item.title }}</span>
              </div>
              <button
                type="button"
                class="shrink-0 rounded-full px-3 py-2 text-xs font-semibold text-rose-600 transition hover:bg-rose-50"
                @click="removeUrl(item.id)"
              >
                Remove
              </button>
            </div>
          </div>
          <p v-else class="mt-6 rounded-xl bg-stone-50 px-4 py-3 text-sm text-stone-500">
            No websites yet. Add one below to choose where Chaperone should check in.
          </p>

          <div class="mt-5 flex flex-col gap-3 sm:flex-row">
            <label for="new-url" class="sr-only">Website address</label>
            <input
              id="new-url"
              v-model="newUrl"
              type="text"
              @keydown.enter.prevent="addUrl"
              placeholder="e.g. instagram.com"
              class="min-h-12 min-w-0 flex-1 rounded-xl border border-stone-300 bg-white px-4 text-sm text-stone-900 outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
            >
            <button
              type="button"
              class="min-h-12 rounded-xl bg-stone-900 px-5 text-sm font-semibold text-white transition hover:bg-violet-700 disabled:cursor-wait disabled:opacity-60"
              :disabled="!newUrl.trim()"
              @click="addUrl"
            >
              Add website <span aria-hidden="true" class="ml-2">+</span>
            </button>
          </div>
          <p v-if="urlError" role="alert" class="mt-3 text-sm text-rose-600">{{ urlError }}</p>
        </section>

        <div class="flex flex-col items-start justify-between gap-4 border-t border-stone-200 pt-5 sm:flex-row sm:items-center">
          <p v-if="saveMessage" role="status" class="text-sm" :class="saveError ? 'text-rose-600' : 'text-emerald-700'">{{ saveMessage }}</p>
          <span v-else class="text-xs text-stone-400">Your settings are saved to your account.</span>
          <button
            type="button"
            :disabled="isSaving"
            class="min-h-12 rounded-full bg-violet-600 px-6 text-sm font-bold text-white transition hover:bg-violet-700 disabled:cursor-wait disabled:opacity-60"
            @click="saveSettings"
          >
            {{ isSaving ? 'Saving…' : 'Save settings' }} <span v-if="!isSaving" aria-hidden="true" class="ml-2">→</span>
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import NavBar from '../components/NavBar.vue'
import api from '../api.js'

export default {
  name: 'SettingsView',
  components: { NavBar },
  data() {
    return {
      authenticated: false,
      isLoading: true,
      isSaving: false,
      saveMessage: '',
      saveError: false,
      timeLimit: 15,
      timeUnit: 'minutes',
      challengeMode: 'math',
      urls: [],
      newUrl: '',
      urlError: '',
    }
  },
  methods: {
    displayUrl(url) {
      return url.replace(/^https?:\/\//, '').replace(/\/$/, '')
    },
    async loadSettings() {
      this.isLoading = true
      try {
        const me = await api.getMe()
        this.challengeMode = me.challenge_mode || 'math'
        const seconds = me.time_limit_seconds || 900
        if (seconds % 60 === 0) {
          this.timeUnit = 'minutes'
          this.timeLimit = seconds / 60
        } else {
          this.timeUnit = 'seconds'
          this.timeLimit = seconds
        }
        this.urls = await api.getUrls()
      } catch (error) {
        console.error('Error loading settings:', error)
        if (error.response && error.response.status === 401) {
          this.authenticated = false
        } else {
          this.saveError = true
          this.saveMessage = 'Could not load settings.'
        }
      } finally {
        this.isLoading = false
      }
    },
    normalizeUrl(input) {
      let url = input.trim()
      if (!/^https?:\/\//i.test(url)) {
        url = `https://${url}`
      }
      return url
    },
    async addUrl() {
      if (!this.newUrl.trim()) return
      this.urlError = ''
      try {
        await api.createUrl({ url: this.normalizeUrl(this.newUrl) })
        this.newUrl = ''
        this.urls = await api.getUrls()
      } catch (error) {
        console.error('Error adding URL:', error)
        this.urlError = 'Could not add that website. Please check the address and try again.'
      }
    },
    async removeUrl(id) {
      try {
        await api.deleteUrl(id)
        this.urls = this.urls.filter(url => url.id !== id)
      } catch (error) {
        console.error('Error removing URL:', error)
        this.urlError = 'Could not remove that website.'
      }
    },
    async saveSettings() {
      const value = parseInt(this.timeLimit, 10)
      if (!value || value <= 0) {
        this.saveError = true
        this.saveMessage = 'Please enter a valid time limit greater than zero.'
        return
      }
      const seconds = this.timeUnit === 'minutes' ? value * 60 : value
      this.isSaving = true
      this.saveMessage = ''
      try {
        await api.updateMeSettings(seconds, this.challengeMode)
        this.saveError = false
        this.saveMessage = 'Your settings have been saved.'
        setTimeout(() => { this.saveMessage = '' }, 3000)
      } catch (error) {
        console.error('Error saving settings:', error)
        this.saveError = true
        this.saveMessage = 'Could not save settings. Please try again.'
      } finally {
        this.isSaving = false
      }
    },
  },
  mounted() {
    this.authenticated = !!localStorage.getItem('accessToken')
    if (this.authenticated) {
      this.loadSettings()
    } else {
      this.isLoading = false
    }
  },
}
</script>
