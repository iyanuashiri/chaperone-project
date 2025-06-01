import { createRouter, createWebHistory } from 'vue-router'
import SignInView from '../views/SignInView.vue'
import SignUpView from '../views/SignUpView.vue'
import HomeView from '../views/HomeView.vue'
// import DashboardView from '../views/Dashboard.vue'
import GameListView from '../views/GameList.vue'
import AssociationListView from '../views/AssociationList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignInView
    },
    {
      path: '/sign-up',
      name: 'sign-up',
      component: SignUpView
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // {
    //   path: '/dashboard',
    //   name: 'dashboard',
    //   component: DashboardView,
    // },
    {
      path: '/game-list',
      name: 'game-list',
      component: GameListView,
    },
    {
      path: '/association-list',
      name: 'association-list',
      component: AssociationListView,
    },
    
    
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],

  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    } else if (savedPosition) {
      return savedPosition;
    }
    return { left: 0, top: 0 }
  }
})

export default router
