import { defineStore } from 'pinia'

import { http } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}/catalogues`

export const useCatalogueStore = defineStore('jobit-catalogues', {
  state: () => ({
    companies: [],
    loadingCompanies: false,

    institutions: [],
    loadingInstitutions: false,
  }),
  actions: {
    async fetchCompanies(query: string) {
      if (!query) {
        this.companies = []
        return
      }

      this.loadingCompanies = true
      try {
        const url = new URL(`${baseUrl}/companies/search`)
        const params = {
          query,
        }
        url.search = new URLSearchParams(params).toString()

        const data = await http.get(url.toString())
        this.companies = data.map((item: { id: string; name: string }) => ({
          label: item.name,
          value: item.id,
        }))
      } catch (err) {
        console.error('Error al cargar compañías:', err)
        this.companies = []
      } finally {
        this.loadingCompanies = false
      }
    },

    async fetchInstitutions(query: string) {
      if (!query) {
        this.institutions = []
        return
      }
      this.loadingInstitutions = true
      try {
        const url = new URL(`${baseUrl}/institutions/search`)
        const params = {
          query,
        }
        url.search = new URLSearchParams(params).toString()

        const data = await http.get(url.toString())
        this.institutions = data.map((item: { id: string; name: string }) => ({
          label: item.name,
          value: item.id,
        }))
      } catch (err) {
        console.error('Error al cargar instituciones:', err)
        this.institutions = []
      } finally {
        this.loadingInstitutions = false
      }
    },
  },
})
