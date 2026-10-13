import { createRouter, createWebHistory } from 'vue-router'
import SignInView from '../views/SignInView.vue'
import SignUpView from '../views/SignUpView.vue'
import HomeView from '../views/HomeView.vue'
import GameListView from '../views/GameList.vue'
import AssociationListView from '../views/AssociationList.vue'
import UrlListView from '../views/UrlListView.vue'
import UrlCreateView from '@/views/UrlCreateView.vue'
import QuizListView from '@/views/QuizListView.vue'
import QuizPlayView from '@/views/QuizPlayView.vue'
import QuizCreateView from '@/views/QuizCreateView.vue'
import GamePlayView from '@/views/GamePlayView.vue'
import AnalyticsView from '@/views/AnalyticsView.vue'

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
    {
      path: '/game-list',
      name: 'game-list',
      component: GameListView,
    },
    {
      path: '/game-play',
      name: 'game-play',
      component: GamePlayView,
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: AnalyticsView,
    },
    {
      path: '/association-list',
      name: 'association-list',
      component: AssociationListView,
    },
    {
      path: '/url-list',
      name: 'url-list',
      component: UrlListView,
    },
    {
      path: '/url-create',
      name: 'url-create',
      component: UrlCreateView,
    },
    {
      path: '/quiz/:id',
      name: 'quiz-play',
      component: QuizPlayView,
      props: true
    },
    {
      path: '/quiz-list/',
      name: 'quiz-list',
      component: QuizListView,
      // props: true
    },
    {
      path: '/quiz-create/',
      name: 'quiz-create',
      component: QuizCreateView,

    }

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
