<template>
    <NavBar></NavBar>  

    <div class="bg-gray-100 p-8 w-full mr-4 ml-auto my-16 max-w-screen-lg">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-8">Our Games</h1>
        <div class="ml-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <GameCard v-for="game in games" :key="game.id" :title="game.title" :description="game.description" :gamePath="game.path" />
        </div>
    </div>    
</template>

<script>
import NavBar from '../components/NavBar.vue';
import GameCard from '../components/GameCard.vue'; 

export default {
  name: 'game-list',
  components: {
    NavBar,
    GameCard 
  },
  data() {
    return {
      games: [
        {
          id: 1,
          title: 'Association',
          description: 'Test your vocabulary by associating words. A fun way to learn new terms!',
          path: '/association-list' 
        },
        {
          id: 2,
          title: 'Agility',
          description: 'Reinforce the new vocabularies by practicing. ',
          path: '/association-list' 
        },
        {
          id: 3,    
          title: 'Memory',
          description: 'Test your vocabulary by associating words. A fun way to learn new terms!',
          path: '/association-list' 
        },
        {
          id: 4,
          title: 'Association',
          description: 'Test your vocabulary by associating words. A fun way to learn new terms!',
          path: '/association-list' 
        },
      ]
    };
  },
  methods: {
    
  },
  mounted() {
   
  }
};
</script>

<style scoped>
</style>