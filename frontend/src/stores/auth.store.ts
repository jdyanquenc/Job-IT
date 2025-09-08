import { defineStore } from 'pinia'

import { http } from '@/helpers'
import { router } from '@/router'

const userKey = 'jobit-user'
const baseUrl = `${import.meta.env.VITE_API_URL}`

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    user: JSON.parse(localStorage.getItem(userKey) || 'null'),
    returnUrl: null as string | null,
  }),
  actions: {
    async login(email: string, password: string) {
      try {
        // The OAuth2 specification states that the username and password should be sent
        const user = await http.form('POST', `${baseUrl}/auth/token`, { username: email, password: password })

        // update pinia state
        this.user = user

        // store user details and jwt in local storage to keep user logged in between page refreshes
        localStorage.setItem(userKey, JSON.stringify(user))

        // redirect to previous url or default to home page
        router.push(this.returnUrl || '/')
      } catch (error: any) {
        if (error.response && error.response.status === 401) {
          throw new Error('Verifica tus credenciales e intenta de nuevo.')
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
