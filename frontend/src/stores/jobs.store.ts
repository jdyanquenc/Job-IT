import { defineStore } from 'pinia'

import { http } from '@/helpers'
import type { RegisterJob, Job, JobDetail, JobCountBySector, JobCountBySalary } from '@/types'

const baseUrl = `${import.meta.env.VITE_API_URL}/jobs`

export const useJobsStore = defineStore('jobit-jobs', {
  state: () => ({
    jobs: [] as Job[],
    job: {} as JobDetail,
    jobCountBySector: [] as JobCountBySector[],
    jobCountBySalary: [] as JobCountBySalary[],
  }),
  actions: {
    async register(request: RegisterJob) {
      await http.post(`${baseUrl}`, request)
    },

    async find(
      query: string = '',
      page: number,
      page_size: number,
      country_code: string,
      sort: string,
      sector_ids: string[] = [],
      salary_ids: string[] = [],
    ) {
      const url = new URL(`${baseUrl}/search`)
      const params = {
        query,
        page: page.toString(),
        page_size: page_size.toString(),
        country_code,
        sort_by: sort,
        sector_ids: sector_ids.join(','),
        salary_ranges: salary_ids.join(','),
      }
      url.search = new URLSearchParams(params).toString()
      this.jobs = await http.get(url.toString())
    },

    async loadJobCountBySector(
      query: string = '',
      country_code: string = '',
      sector_ids: string[] = [],
      salary_ids: string[] = [],
    ) {
      const url = new URL(`${baseUrl}/sectors/counts`)
      const params = {
        query,
        country_code,
        sector_ids: sector_ids.join(','),
        salary_ranges: salary_ids.join(','),
      }
      url.search = new URLSearchParams(params).toString()
      this.jobCountBySector = await http.get(url.toString())
    },

    async loadJobCountBySalary(
      query: string = '',
      country_code: string = '',
      sector_ids: string[] = [],
      salary_ids: string[] = [],
    ) {
      const url = new URL(`${baseUrl}/salaries/counts`)
      const params = {
        query,
        country_code,
        sector_ids: sector_ids.join(','),
        salary_ranges: salary_ids.join(','),
      }
      url.search = new URLSearchParams(params).toString()
      this.jobCountBySalary = await http.get(url.toString())
    },

    async getById(id: string) {
      this.job = await http.get(`${baseUrl}/${id}`)
    },

    async update(id: string, params: Partial<RegisterJob>) {
      await http.put(`${baseUrl}/${id}`, params)
    },

    async delete(id: string) {
      await http.delete(`${baseUrl}/${id}`)

      // remove job from list after deleted
      this.jobs = this.jobs.filter((x: Job) => x.id !== id)
    },

    async applyToJob(id: string) {
      await http.post(`${baseUrl}/${id}/apply`)
      this.jobs = this.jobs.map((job) => {
        if (job.id === id) {
          return { ...job, has_applied: true }
        }
        return job
      })
    },
  },
})
