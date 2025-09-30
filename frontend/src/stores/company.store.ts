import { defineStore } from 'pinia'

import { http } from '@/helpers'

const baseUrl = `${import.meta.env.VITE_API_URL}/companies`

export const useCompanyStore = defineStore('jobit-companies', {
  state: () => ({
    options: [],
    loading: false,
  }),
  actions: {
    async fetchOptions(query: string) {
      if (!query) {
        this.options = []
        return
      }

      this.loading = true
      try {
        const url = new URL(`${baseUrl}/search`)
        const params = {
          query,
        }
        url.search = new URLSearchParams(params).toString()

        const data = await http.get(url.toString())
        this.options = data.map((item: { id: string; name: string }) => ({
          label: item.name,
          value: item.id,
        }))
      } catch (err) {
        console.error('Error al cargar opciones:', err)
        this.options = []
      } finally {
        this.loading = false
      }
    },
  },
})
