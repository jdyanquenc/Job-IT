import { defineStore } from 'pinia'

import { http } from '@/helpers'
import { router } from '@/router'

const userKey = 'jobit-user'
const baseUrl = `${import.meta.env.VITE_API_URL}/users`

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem(userKey) || 'null'),
    returnUrl: null as string | null,
  }),
  actions: {
    async login(username: string, password: string) {
      try {
        const user = await http.post(`${baseUrl}/authenticate`, { username, password })

        // update pinia state
        this.user = user

        // store user details and jwt in local storage to keep user logged in between page refreshes
        localStorage.setItem(userKey, JSON.stringify(user))

        // redirect to previous url or default to home page
        router.push(this.returnUrl || '/')
      } catch (error: any) {
        if (error.response && error.response.status === 401) {
          throw new Error('Username or password is incorrect')
        }
        throw error
      }
    },
    logout() {
      this.user = null
      localStorage.removeItem(userKey)
      router.push('/account/login')
    },
  },
})
