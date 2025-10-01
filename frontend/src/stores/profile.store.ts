import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { Profile, WorkExperience } from '@/types/Profile'

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
        this.profileData = {} as {
          id: string
          description: string
          work_experiences: WorkExperience[]
        }
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

    async addWorkExperience(newExperience: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/work-experiences`)
        const createdExperience = await http.post(url.toString(), newExperience)
        this.profileData.work_experiences.push(createdExperience)
      } catch (err) {
        console.error('Error al agregar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async updateWorkExperience(updatedExperience: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(
          `${baseUrl}/${this.profileData.id}/work-experiences/${updatedExperience.id}`,
        )
        await http.put(url.toString(), updatedExperience)
        const index = this.profileData.work_experiences.findIndex(
          (exp) => exp.id === updatedExperience.id,
        )
        if (index !== -1) {
          this.profileData.work_experiences[index] = updatedExperience
        }
      } catch (err) {
        console.error('Error al actualizar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async deleteWorkExperience(experienceId: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/work-experiences/${experienceId}`)
        await http.delete(url.toString())

        this.profileData.work_experiences = this.profileData.work_experiences.filter(
          (exp) => exp.id !== experienceId,
        )
      } catch (err) {
        console.error('Error al eliminar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },
  },
})
