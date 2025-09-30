import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { Profile } from '@/types/Profile'

const baseUrl = `${import.meta.env.VITE_API_URL}/profiles`

export const useProfileStore = defineStore('jobit-profile', {
  state: () => ({
    profileData: {} as Profile,
    loading: false,
  }),
  actions: {
    async load(id: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${id}`)
        const data = await http.get(url.toString())
        this.profileData = data
      } catch (err) {
        console.error('Error al cargar perfil:', err)
        this.profileData = {} as { id: string; description: string }
      } finally {
        this.loading = false
      }
    },

    async updateDescription(newDescription: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}`)
        await http.put(url.toString(), { description: newDescription })
        this.profileData.description = newDescription
      } catch (err) {
        console.error('Error al actualizar la descripción:', err)
        this.profileData.description = ''
      } finally {
        this.loading = false
      }
    },
  },
})
