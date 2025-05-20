import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CommunityView from '@/views/CommunityView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/humidity',
      name: 'humidity',
      component: () => import('../views/HumidityView.vue')
    },
    {
      path: '/pain-check',
      name: 'painCheck',
      component: () => import('../views/PainCheckView.vue'),
    },
    {
      path: '/sport-suggestion/:level',
      name: 'sportSuggestion',
      component: () => import('../views/SportSuggestionView.vue'),
    },
    {
      path: '/symptom-prediction',
      name: 'symptomPrediction',
      component: () => import('../views/SymptomPredictionView.vue'),
    },
    {
      path: '/user-profile',
      name: 'userProfile',
      component: () => import('../views/UserProfileView.vue')
    },
    {
      path: '/body-prediction',
      name: 'bodyPrediction',
      component: () => import('../views/BodyPredictionView.vue')
    }
  ]
})

export default router
