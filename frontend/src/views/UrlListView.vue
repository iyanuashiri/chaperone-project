<template>
  <NavBar></NavBar>

  <div class="bg-gray-100 p-8 w-full mr-4 ml-auto my-16 max-w-screen-lg">
    <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">URL Management</h1>
    <div class="ml-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <NewUrl title="Add New URL" description="This is a description" url="new-url" />
      <UrlCard v-for="url in urls" :key="url.id" :title="url.title" :description="url.description" />
    </div>
  </div>
</template>

<script>

import NavBar from '../components/NavBar.vue';
import UrlCard from '../components/URLCard.vue';
import NewUrl from '@/components/NewUrl.vue';
import api from '../api';

export default {
  name: 'UrlList',
  components: {
    // UrlForm,
    NewUrl,
    NavBar,
    UrlCard
  },
  data() {
    return {
      showForm: false,
      urls: []
    };
  },
  methods: {
    getUrls: async function () {
      this.urls = await api.getUrls()
    },
  },
  mounted() {
    this.getUrls()
  }
};
</script>

<style scoped>
</style>