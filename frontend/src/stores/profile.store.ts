import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { EducationExperience, Profile, WorkExperience } from '@/types/Profile'

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
          education_experiences: EducationExperience[]
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

    async addWorkExperience(newWork: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/work-experiences`)
        const createdExperience = await http.post(url.toString(), newWork)
        this.profileData.work_experiences.push(createdExperience)
      } catch (err) {
        console.error('Error al agregar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async updateWorkExperience(updatedWork: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/work-experiences/${updatedWork.id}`)
        await http.put(url.toString(), updatedWork)
        const index = this.profileData.work_experiences.findIndex(
          (exp) => exp.id === updatedWork.id,
        )
        if (index !== -1) {
          this.profileData.work_experiences[index] = updatedWork
        }
      } catch (err) {
        console.error('Error al actualizar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async deleteWorkExperience(workExperienceId: string) {
      this.loading = true
      try {
        const url = new URL(
          `${baseUrl}/${this.profileData.id}/work-experiences/${workExperienceId}`,
        )
        await http.delete(url.toString())

        this.profileData.work_experiences = this.profileData.work_experiences.filter(
          (exp) => exp.id !== workExperienceId,
        )
      } catch (err) {
        console.error('Error al eliminar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async addEducation(newEducation: EducationExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/educations`)
        const createdEducation = await http.post(url.toString(), newEducation)
        this.profileData.education_experiences.push(createdEducation)
      } catch (err) {
        console.error('Error al agregar educación:', err)
      } finally {
        this.loading = false
      }
    },

    async updateEducation(updatedEducation: EducationExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/educations/${updatedEducation.id}`)
        await http.put(url.toString(), updatedEducation)
        const index = this.profileData.education_experiences.findIndex(
          (edu) => edu.id === updatedEducation.id,
        )
        if (index !== -1) {
          this.profileData.education_experiences[index] = updatedEducation
        }
      } catch (err) {
        console.error('Error al actualizar educación:', err)
      } finally {
        this.loading = false
      }
    },

    async deleteEducation(educationId: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profileData.id}/educations/${educationId}`)
        await http.delete(url.toString())
        this.profileData.education_experiences = this.profileData.education_experiences.filter(
          (edu) => edu.id !== educationId,
        )
      } catch (err) {
        console.error('Error al eliminar educación:', err)
      } finally {
        this.loading = false
      }
    },
  },
})
