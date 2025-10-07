/* eslint-disable @typescript-eslint/no-explicit-any */
import { defineStore } from 'pinia'

import { http } from '@/helpers'
import { useAuthStore } from '@/stores'
import type { RegisterCompanyUser, RegisterUser, User } from '@/types'

const baseUrl = `${import.meta.env.VITE_API_URL}/users`

export const useUsersStore = defineStore('jobit-users', {
  state: () => ({
    users: [] as User[],
    user: {} as User,
  }),
  actions: {
    async checkEmailAvailability(email: string): Promise<{ available: boolean }> {
      const url = new URL(`${baseUrl}/check-email`)
      url.search = new URLSearchParams({ email }).toString()
      return await http.get(url.toString())
    },

    async registerCandidate(request: RegisterUser) {
      await http.post(`${baseUrl}/candidates`, request)
    },

    async registerCompany(request: RegisterCompanyUser) {
      await http.post(`${baseUrl}/companies`, request)
    },

    async getAll() {
      try {
        this.users = await http.get(baseUrl)
      } catch (error) {
        this.users = []
        console.error('Error fetching users:', error)
      }
    },

    async getById(id: number) {
      try {
        this.user = await http.get(`${baseUrl}/${id}`)
      } catch (error) {
        this.user = {} as User
        console.error(`Error fetching user with id ${id}:`, error)
      }
    },

    async update(id: number, params: any) {
      await http.put(`${baseUrl}/${id}`, params)

      // update stored user if the logged in user updated their own record
      const authStore = useAuthStore()
      if (id === authStore.userToken.id) {
        // update local storage
        const user = { ...authStore.userToken, ...params }
        localStorage.setItem('jobit-user', JSON.stringify(user))

        // update auth user in pinia state
        authStore.userToken = user
      }
    },

    async delete(id: number) {
      // add isDeleting prop to user being deleted
      this.users.find((x: User) => x.id === id)!.isDeleting = true

      await http.delete(`${baseUrl}/${id}`)

      // remove user from list after deleted
      this.users = this.users.filter((x: User) => x.id !== id)

      // auto logout if the logged in user deleted their own record
      const authStore = useAuthStore()
      if (id === authStore.userToken.id) {
        authStore.logout()
      }
    },
  },
})
