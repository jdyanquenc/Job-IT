import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { JobRecommendation } from '@/types/JobRecommendation'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs`

export const useJobRecommendationsStore = defineStore('jobit-recommendations', {
  state: () => ({
    job_recommendations: [] as JobRecommendation[],
  }),
  actions: {
    async find(query: string = '', page: number = 1) {
      try {
        console.log('Fetching recommendations with query:', baseUrl, query)
        const url = new URL(`${baseUrl}/recommendations/`)
        const params = {
          query,
          page: page.toString(),
        }
        url.search = new URLSearchParams(params).toString()
        this.job_recommendations = await http.get(url.toString())
      } catch (error) {
        this.job_recommendations = []
        console.error('Error fetching recommendations:', error)
      }
    },
  },
})
