import { defineStore } from 'pinia'

import { http } from '@/helpers'
import { router } from '@/router'
import { jwtDecode } from 'jwt-decode'

const userKey = 'jobit-user'
const tokenDataKey = 'jobit-token-data'
const baseUrl = `${import.meta.env.VITE_API_URL}`

type DecodedToken = {
  sub: string
  email: string
  exp: number
  jti: string
  name: string
  role: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // initialize state from local storage to enable user to stay logged in
    userToken: JSON.parse(localStorage.getItem(userKey) || 'null'),
    returnUrl: null as string | null,
    isTokenValid: false,
  }),
  actions: {
    async login(email: string, password: string) {
      try {
        // The OAuth2 specification states that the username and password should be sent
        const userToken = await http.form('POST', `${baseUrl}/auth/token`, {
          username: email,
          password: password,
        })

        // update pinia state
        this.userToken = userToken

        // store user details and jwt in local storage to keep user logged in between page refreshes
        localStorage.setItem(userKey, JSON.stringify(userToken))

        // redirect to previous url or default to home page
        router.push(this.returnUrl || '/')
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (error: any) {
        if (error.response && error.response.status === 401) {
          throw new Error('Verifica tus credenciales e intenta de nuevo.')
        }
        throw error
      }
    },
    getTokenData(): DecodedToken | null {
      try {
        if (localStorage.getItem(tokenDataKey) === null) {
          const token = this.userToken?.access_token
          const tokenData = jwtDecode<DecodedToken>(token)
          localStorage.setItem(tokenDataKey, JSON.stringify(tokenData))
        }
        return JSON.parse(localStorage.getItem(tokenDataKey) || 'null')
      } catch {
        return null
      }
    },
    isLoggedIn() {
      this.isTokenValid = (this.getTokenData()?.exp || 0) * 1000 > Date.now()
      if (this.userToken && !this.isTokenValid) {
        this.logout()
      }
      return this.isTokenValid
    },
    getUserId() {
      return this.getTokenData()?.sub || null
    },
    isAdmin() {
      return this.getTokenData()?.role === 'ADMIN'
    },
    isCandidate() {
      return this.getTokenData()?.role === 'CANDIDATE'
    },
    isCompanyManager() {
      return this.getTokenData()?.role === 'COMPANY_MANAGER'
    },
    logout() {
      this.userToken = null
      localStorage.removeItem(userKey)
      localStorage.removeItem(tokenDataKey)
      router.push('/accounts/login')
    },
  },
})
