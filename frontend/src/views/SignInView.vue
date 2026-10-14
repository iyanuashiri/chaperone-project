<template>
  <main class="grid min-h-screen bg-[#f7f6f1] text-stone-900 lg:grid-cols-[1fr_0.92fr]">
    <section class="flex flex-col px-6 py-6 sm:px-10 lg:px-16">
      <RouterLink to="/" class="flex w-fit items-center gap-3 text-lg font-bold tracking-tight">
        <span class="grid h-9 w-9 place-items-center rounded-xl bg-violet-600 text-xl italic text-white">c</span>
        chaperone<span class="-ml-3 text-violet-600">.</span>
      </RouterLink>

      <div class="mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-14">
        <span class="text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Welcome back</span>
        <h1 class="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">Pick up where you left off.</h1>
        <p class="mt-3 text-sm leading-6 text-stone-500">Sign in to continue building a more intentional browsing routine.</p>

        <form class="mt-9 space-y-5" @submit.prevent="signIn">
          <div>
            <label for="email" class="mb-2 block text-sm font-semibold text-stone-700">Email address</label>
            <input
              id="email"
              v-model="model.email"
              type="email"
              name="email"
              autocomplete="email"
              required
              class="min-h-12 w-full rounded-xl border border-stone-300 bg-white px-4 text-sm outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
              placeholder="you@example.com"
            >
          </div>
          <div>
            <label for="password" class="mb-2 block text-sm font-semibold text-stone-700">Password</label>
            <input
              id="password"
              v-model="model.password"
              type="password"
              name="password"
              autocomplete="current-password"
              required
              class="min-h-12 w-full rounded-xl border border-stone-300 bg-white px-4 text-sm outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
              placeholder="Your password"
            >
          </div>
          <p v-if="errorMessage" role="alert" class="rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">{{ errorMessage }}</p>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="flex min-h-12 w-full items-center justify-center gap-3 rounded-xl bg-stone-900 px-5 text-sm font-bold text-white transition hover:bg-violet-700 disabled:cursor-wait disabled:opacity-60"
          >
            {{ isSubmitting ? 'Signing in…' : 'Sign in' }}
            <span v-if="!isSubmitting" aria-hidden="true">→</span>
          </button>
        </form>

        <p class="mt-7 text-center text-sm text-stone-500">
          New to Chaperone?
          <RouterLink to="/sign-up" class="font-bold text-violet-700 hover:text-violet-900">Create an account</RouterLink>
        </p>
      </div>

      <RouterLink to="/" class="text-sm font-semibold text-stone-500 hover:text-violet-700">← Back to Chaperone</RouterLink>
    </section>

    <aside class="relative hidden overflow-hidden bg-[#28252f] p-12 text-white lg:flex lg:flex-col lg:justify-between lg:p-16">
      <div class="absolute -right-36 -top-20 h-[520px] w-[520px] rounded-full border border-lime-200/20 shadow-[0_0_0_45px_rgba(201,250,116,0.04),0_0_0_90px_rgba(201,250,116,0.025)]"></div>
      <p class="relative text-xs font-bold uppercase tracking-[0.18em] text-lime-200">A little pause. A lot more on purpose.</p>
      <div class="relative max-w-lg">
        <span class="text-5xl text-lime-200">“</span>
        <p class="mt-2 text-4xl font-medium leading-tight tracking-tight">Your attention is yours. Make room to choose where it goes.</p>
        <p class="mt-8 text-sm text-stone-400">A more mindful internet starts with one moment.</p>
      </div>
      <p class="relative text-xs text-stone-500">Chaperone · Browse with intention</p>
    </aside>
  </main>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
  name: 'sign-in',
  components: { RouterLink },
  data() {
    return {
      model: {},
      errorMessage: '',
      isSubmitting: false,
    }
  },
  methods: {
    async signIn() {
      this.errorMessage = ''
      this.isSubmitting = true
      const url = 'http://127.0.0.1:8000/api/v1/auth/login/'
      const formData = new FormData()
      formData.append('email', this.model.email)
      formData.append('password', this.model.password)
      try {
        const response = await axios.post(url, formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        })
        localStorage.setItem('accessToken', response.data.access_token)
        localStorage.setItem('email', this.model.email)
        this.$router.push({ name: 'game-list' })
      } catch (error) {
        console.error('Sign in failed:', error)
        const detail = error.response?.data?.detail
        this.errorMessage = detail || 'Invalid email or password. Please try again.'
      } finally {
        this.isSubmitting = false
      }
    },
  },
}
</script>
