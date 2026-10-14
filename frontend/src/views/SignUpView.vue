<template>
  <main class="grid min-h-screen bg-[#f7f6f1] text-stone-900 lg:grid-cols-[1fr_0.92fr]">
    <section class="flex flex-col px-6 py-6 sm:px-10 lg:px-16">
      <RouterLink to="/" class="flex w-fit items-center gap-3 text-lg font-bold tracking-tight">
        <span class="grid h-9 w-9 place-items-center rounded-xl bg-violet-600 text-xl italic text-white">c</span>
        chaperone<span class="-ml-3 text-violet-600">.</span>
      </RouterLink>

      <div class="mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-12">
        <span class="text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Make it yours</span>
        <h1 class="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">A fresh start for your focus.</h1>
        <p class="mt-3 text-sm leading-6 text-stone-500">Create your account to set your boundaries and keep track of your progress.</p>

        <form class="mt-8 space-y-4" @submit.prevent="signUp">
          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label for="first_name" class="mb-2 block text-sm font-semibold text-stone-700">First name</label>
              <input
                id="first_name"
                v-model="model.first_name"
                type="text"
                name="first_name"
                autocomplete="given-name"
                required
                class="min-h-12 w-full rounded-xl border border-stone-300 bg-white px-4 text-sm outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
                placeholder="First name"
              >
            </div>
            <div>
              <label for="last_name" class="mb-2 block text-sm font-semibold text-stone-700">Last name</label>
              <input
                id="last_name"
                v-model="model.last_name"
                type="text"
                name="last_name"
                autocomplete="family-name"
                required
                class="min-h-12 w-full rounded-xl border border-stone-300 bg-white px-4 text-sm outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
                placeholder="Last name"
              >
            </div>
          </div>
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
              autocomplete="new-password"
              required
              class="min-h-12 w-full rounded-xl border border-stone-300 bg-white px-4 text-sm outline-none transition placeholder:text-stone-400 focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
              placeholder="Create a password"
            >
          </div>
          <p v-if="errorMessage" role="alert" class="rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">{{ errorMessage }}</p>
          <p v-if="successMessage" role="status" class="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">{{ successMessage }}</p>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="flex min-h-12 w-full items-center justify-center gap-3 rounded-xl bg-stone-900 px-5 text-sm font-bold text-white transition hover:bg-violet-700 disabled:cursor-wait disabled:opacity-60"
          >
            {{ isSubmitting ? 'Creating your account…' : 'Create account' }}
            <span v-if="!isSubmitting" aria-hidden="true">→</span>
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-stone-500">
          Already have an account?
          <RouterLink to="/sign-in" class="font-bold text-violet-700 hover:text-violet-900">Sign in</RouterLink>
        </p>
      </div>

      <RouterLink to="/" class="text-sm font-semibold text-stone-500 hover:text-violet-700">← Back to Chaperone</RouterLink>
    </section>

    <aside class="relative hidden overflow-hidden bg-[#28252f] p-12 text-white lg:flex lg:flex-col lg:justify-between lg:p-16">
      <div class="absolute -right-36 -top-20 h-[520px] w-[520px] rounded-full border border-lime-200/20 shadow-[0_0_0_45px_rgba(201,250,116,0.04),0_0_0_90px_rgba(201,250,116,0.025)]"></div>
      <p class="relative text-xs font-bold uppercase tracking-[0.18em] text-lime-200">A little pause. A lot more on purpose.</p>
      <div class="relative max-w-lg">
        <span class="text-5xl text-lime-200">“</span>
        <p class="mt-2 text-4xl font-medium leading-tight tracking-tight">Build a browser routine that gives your attention back to you.</p>
        <p class="mt-8 text-sm text-stone-400">Small moments can make room for meaningful change.</p>
      </div>
      <p class="relative text-xs text-stone-500">Chaperone · Browse with intention</p>
    </aside>
  </main>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
  name: 'sign-up',
  components: { RouterLink },
  data() {
    return {
      model: {},
      errorMessage: '',
      successMessage: '',
      isSubmitting: false,
    }
  },
  methods: {
    async signUp() {
      this.errorMessage = ''
      this.successMessage = ''
      this.isSubmitting = true
      const url = 'http://127.0.0.1:8000/api/v1/users/'
      try {
        await axios.post(url, this.model)
        this.successMessage = 'Your account is ready. Taking you to sign in…'
        setTimeout(() => this.$router.push({ name: 'sign-in' }), 900)
      } catch (error) {
        console.error('Sign up failed:', error)
        const detail = error.response?.data?.detail
        this.errorMessage = detail || 'Something went wrong. Please try again.'
      } finally {
        this.isSubmitting = false
      }
    },
  },
}
</script>
