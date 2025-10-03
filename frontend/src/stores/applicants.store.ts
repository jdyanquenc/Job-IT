import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { Applicant } from '@/types/Applicant'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs`

export const useApplicantsStore = defineStore('jobit-applicants', {
  state: () => ({
    applicants: [] as Applicant[],
  }),
  actions: {
    async find(id: string, query: string = '', page: number = 1) {
      try {
        console.log('Fetching applicants with query:', baseUrl, query)
        const url = new URL(`${baseUrl}/${id}/applications`)
        const params = {
          query,
          page: page.toString(),
        }
        url.search = new URLSearchParams(params).toString()
        this.applicants = await http.get(url.toString())
      } catch (error) {
        this.applicants = []
        console.error('Error fetching applicants:', error)
      }
    },
  },
})
