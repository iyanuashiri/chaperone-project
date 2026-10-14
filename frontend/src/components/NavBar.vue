<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const email = localStorage.getItem('email') || 'Your account'
const initials = computed(() => email.trim().charAt(0).toUpperCase() || 'C')

const navigation = [
  { name: 'game-list', label: 'Overview', symbol: '⌂' },
  { name: 'game-play', label: 'Challenge', symbol: '＋' },
  { name: 'analytics', label: 'Analytics', symbol: '↗' },
  { name: 'settings', label: 'Settings', symbol: '⚙' }
]

function isActive(name) {
  return route.name === name || (name === 'game-list' && route.name === 'game-play')
}

function signOut() {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('email')
  router.push({ name: 'sign-in' })
}
</script>

<template>
  <aside class="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-stone-200 bg-white px-5 py-6 lg:flex">
    <RouterLink to="/" class="mb-12 flex items-center gap-3 px-2 text-lg font-bold tracking-tight text-stone-900">
      <span class="grid h-9 w-9 place-items-center rounded-xl bg-violet-600 text-xl italic text-white">c</span>
      <span>chaperone<span class="text-violet-600">.</span></span>
    </RouterLink>

    <p class="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-stone-400">Your space</p>
    <nav class="flex flex-col gap-1" aria-label="Main navigation">
      <RouterLink
        v-for="item in navigation"
        :key="item.name"
        :to="{ name: item.name }"
        class="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold transition-colors"
        :class="isActive(item.name) ? 'bg-violet-50 text-violet-700' : 'text-stone-500 hover:bg-stone-50 hover:text-stone-900'"
      >
        <span class="grid h-7 w-7 place-items-center rounded-lg bg-white text-base" :class="isActive(item.name) ? 'text-violet-600' : 'text-stone-400'">{{ item.symbol }}</span>
        {{ item.label }}
        <span v-if="isActive(item.name)" class="ml-auto h-1.5 w-1.5 rounded-full bg-violet-600"></span>
      </RouterLink>
    </nav>

    <div class="mt-auto rounded-2xl bg-stone-50 p-4">
      <div class="flex items-center gap-3">
        <span class="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-lime-200 text-sm font-bold text-stone-800">{{ initials }}</span>
        <span class="min-w-0 truncate text-xs font-semibold text-stone-700">{{ email }}</span>
      </div>
      <button
        type="button"
        class="mt-4 w-full rounded-lg px-3 py-2 text-left text-xs font-semibold text-stone-500 transition hover:bg-white hover:text-stone-900"
        @click="signOut"
      >
        Sign out <span aria-hidden="true" class="float-right">↗</span>
      </button>
    </div>
  </aside>

  <header class="sticky top-0 z-30 border-b border-stone-200 bg-white/95 px-4 py-3 backdrop-blur lg:hidden">
    <div class="flex items-center justify-between gap-3">
      <RouterLink to="/" class="flex items-center gap-2 text-base font-bold tracking-tight text-stone-900">
        <span class="grid h-8 w-8 place-items-center rounded-lg bg-violet-600 text-lg italic text-white">c</span>
        chaperone<span class="text-violet-600">.</span>
      </RouterLink>
      <button type="button" class="rounded-lg px-3 py-2 text-xs font-semibold text-stone-500 hover:bg-stone-100" @click="signOut">
        Sign out
      </button>
    </div>
    <nav class="mt-3 flex gap-1 overflow-x-auto pb-0.5" aria-label="Main navigation">
      <RouterLink
        v-for="item in navigation"
        :key="item.name"
        :to="{ name: item.name }"
        class="shrink-0 rounded-full px-3 py-2 text-xs font-semibold transition-colors"
        :class="isActive(item.name) ? 'bg-violet-600 text-white' : 'bg-stone-100 text-stone-600'"
      >
        {{ item.label }}
      </RouterLink>
    </nav>
  </header>
</template>
