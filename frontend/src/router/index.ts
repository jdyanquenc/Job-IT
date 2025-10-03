import { createRouter, createWebHistory } from 'vue-router'

import { HomeView } from '@/views'
import { useAuthStore } from '@/stores'
import accountRoutes from './account.routes'
import usersRoutes from './users.routes'
import jobsRoutes from './jobs.routes'
import companyJobsRoutes from './company-jobs.routes'
import profileRoutes from './profile.routes'
import applicantsRoutes from './applicants.routes'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  routes: [
    { path: '/', component: HomeView },
    { ...accountRoutes },
    { ...usersRoutes },
    { ...jobsRoutes },
    { ...companyJobsRoutes },
    { ...profileRoutes },
    { ...applicantsRoutes },
    // catch all redirect to home page
    { path: '/:pathMatch(.*)*', redirect: '/jobs' },
  ],
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPagesPatterns: RegExp[] = [
    /\/accounts\/login/,
    /\/accounts\/register/,
    /\/accounts\/register-company/,
    /\/jobs\/.*/,
    /\/jobs/,
    /\/$/,
  ]
  const authRequired = !publicPagesPatterns.some((pattern) => pattern.test(to.path))
  const authStore = useAuthStore()

  if (authRequired && !authStore.userToken) {
    authStore.returnUrl = to.fullPath
    return '/accounts/login'
  }
})
