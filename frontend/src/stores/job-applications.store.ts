import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { JobApplication } from '@/types/JobApplication'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs`

export const useJobApplicationsStore = defineStore('jobit-applications', {
  state: () => ({
    job_applications: [] as JobApplication[],
  }),
  actions: {
    async find(query: string = '', page: number = 1) {
      try {
        console.log('Fetching applications with query:', baseUrl, query)
        const url = new URL(`${baseUrl}/applications/`)
        const params = {
          query,
          page: page.toString(),
        }
        url.search = new URLSearchParams(params).toString()
        this.job_applications = await http.get(url.toString())
      } catch (error) {
        this.job_applications = []
        console.error('Error fetching applications:', error)
      }
    },
  },
})
