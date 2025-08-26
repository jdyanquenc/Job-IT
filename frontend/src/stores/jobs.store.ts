import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { RegisterJob, Job } from '@/types'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs/`

export const useJobsStore = defineStore('jobit-jobs', {
  state: () => ({
    jobs: [] as Job[],
    job: {} as Job,
  }),
  actions: {
    async register(request: RegisterJob) {
      await http.post(`${baseUrl}`, request)
    },

    async find(query: string = '', page: number = 1) {
      try {
        console.log('Fetching jobs with query:', baseUrl, query);
        const url = new URL(baseUrl)
        const params: any = {
          query,
          page,
        }
        url.search = new URLSearchParams(params).toString();
        this.jobs = await http.get(url.toString())
      } catch (error) {
        this.jobs = []
        console.error('Error fetching users:', error)
      }
    },

    async getById(id: string) {
      try {
        this.job = await http.get(`${baseUrl}/${id}`)
      } catch (error) {
        this.job = {} as Job
        console.error(`Error fetching job with id ${id}:`, error)
      }
    },

    async update(id: string, params: any) {
      await http.put(`${baseUrl}/${id}`, params)
    },

    async delete(id: string) {
      
      await http.delete(`${baseUrl}/${id}`)

      // remove job from list after deleted
      this.jobs = this.jobs.filter((x: Job) => x.id !== id)
    },
  },
})
