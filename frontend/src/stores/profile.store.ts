import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { EducationExperience, Profile, WorkExperience } from '@/types/Profile'

const baseUrl = `${import.meta.env.VITE_API_URL}/profiles`

export const useProfileStore = defineStore('jobit-profile', {
  state: () => ({
    profile: {} as Profile,
    loading: false,
  }),
  actions: {
    async load(id: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${id}`)
        const data = await http.get(url.toString())
        this.profile = {
          ...this.profile,
          ...data,
          skills: Array.isArray(data.skills) ? data.skills : [],
        }
      } catch (err) {
        console.error('Error al cargar perfil:', err)
        this.profile = {} as {
          id: string
          full_name: string
          title: string
          description: string
          location: string
          salary_range: string
          modality: string
          skills: string[]
          education_experiences: EducationExperience[]
          work_experiences: WorkExperience[]
        }
      } finally {
        this.loading = false
      }
    },

    async updateTitle(newTitle: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { title: newTitle })
        this.profile.title = newTitle
      } catch (err) {
        console.error('Error al actualizar el título:', err)
        this.profile.title = ''
      } finally {
        this.loading = false
      }
    },

    async updateDescription(newDescription: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { description: newDescription })
        this.profile.description = newDescription
      } catch (err) {
        console.error('Error al actualizar la descripción:', err)
        this.profile.description = ''
      } finally {
        this.loading = false
      }
    },

    async updateLocation(newLocation: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { location: newLocation })
        this.profile.location = newLocation
      } catch (err) {
        console.error('Error al actualizar la ubicación:', err)
        this.profile.location = ''
      } finally {
        this.loading = false
      }
    },

    async updateSalaryRange(newSalaryRange: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { salary_range: newSalaryRange })
        this.profile.salary_range = newSalaryRange
      } catch (err) {
        console.error('Error al actualizar el rango salarial:', err)
        this.profile.salary_range = ''
      } finally {
        this.loading = false
      }
    },

    async updateModality(newModality: string) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { modality: newModality })
        this.profile.modality = newModality
      } catch (err) {
        console.error('Error al actualizar la modalidad:', err)
        this.profile.modality = ''
      } finally {
        this.loading = false
      }
    },

    async updateSkills(newSkills: string[]) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}`)
        await http.put(url.toString(), { skills: newSkills })
        this.profile.skills = newSkills
      } catch (err) {
        console.error('Error al actualizar las habilidades:', err)
        this.profile.skills = []
      } finally {
        this.loading = false
      }
    },

    async addWorkExperience(newWork: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}/work-experiences`)
        const createdExperience = await http.post(url.toString(), newWork)
        this.profile.work_experiences.push(createdExperience)
      } catch (err) {
        console.error('Error al agregar experiencia laboral:', err)
      } finally {
        this.loading = false
      }
    },

    async updateWorkExperience(updatedWork: WorkExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}/work-experiences/${updatedWork.id}`)
        await http.put(url.toString(), updatedWork)
        const index = this.profile.work_experiences.findIndex((exp) => exp.id === updatedWork.id)
        if (index !== -1) {
          this.profile.work_experiences[index] = updatedWork
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
        const url = new URL(`${baseUrl}/${this.profile.id}/work-experiences/${workExperienceId}`)
        await http.delete(url.toString())

        this.profile.work_experiences = this.profile.work_experiences.filter(
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
        const url = new URL(`${baseUrl}/${this.profile.id}/educations`)
        const createdEducation = await http.post(url.toString(), newEducation)
        this.profile.education_experiences.push(createdEducation)
      } catch (err) {
        console.error('Error al agregar educación:', err)
      } finally {
        this.loading = false
      }
    },

    async updateEducation(updatedEducation: EducationExperience) {
      this.loading = true
      try {
        const url = new URL(`${baseUrl}/${this.profile.id}/educations/${updatedEducation.id}`)
        await http.put(url.toString(), updatedEducation)
        const index = this.profile.education_experiences.findIndex(
          (edu) => edu.id === updatedEducation.id,
        )
        if (index !== -1) {
          this.profile.education_experiences[index] = updatedEducation
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
        const url = new URL(`${baseUrl}/${this.profile.id}/educations/${educationId}`)
        await http.delete(url.toString())
        this.profile.education_experiences = this.profile.education_experiences.filter(
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
