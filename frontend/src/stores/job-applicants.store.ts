import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { JobApplicant as JobApplicant } from '@/types/JobApplicant'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs`

export const useJobApplicantsStore = defineStore('jobit-applicants', {
  state: () => ({
    job_applicants: [] as JobApplicant[],
  }),
  actions: {
    async find(id: string, query: string = '', page: number = 1) {
      try {
        console.log('Fetching applicants with query:', baseUrl, query)
        const url = new URL(`${baseUrl}/${id}/applicants`)
        const params = {
          query,
          page: page.toString(),
        }
        url.search = new URLSearchParams(params).toString()
        this.job_applicants = await http.get(url.toString())
      } catch (error) {
        this.job_applicants = []
        console.error('Error fetching applicants:', error)
      }
    },
  },
})
