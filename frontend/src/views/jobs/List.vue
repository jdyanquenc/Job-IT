<script setup>
import { ref } from 'vue'
import FilterGroup from '@/components/FilterGroup.vue'
import JobCard from '@/components/JobCard.vue'
import SearchBar from '@/views/jobs/SearchBar.vue'

import { NSelect, NPagination } from 'naive-ui'

const sort = ref('relevance')
const page = ref(1)
const pageSize = ref(10)
const total = ref(200)

const selectedIndustries = ref([])
const selectedSalaries = ref([])

const sortOptions = [
  { label: 'Relevancia', value: 'relevance' },
  { label: 'Fecha de publicación', value: 'date' },
  { label: 'Salario', value: 'salary' }
]

const pageSizes = [
  { label: '10 / pág', value: 10 },
  { label: '20 / pág', value: 20 },
  { label: '30 / pág', value: 30 }
]

const industryOptions = [
    { id: 1, name: 'Software', count: 12 },
    { id: 2, name: 'Finance', count: 23 },
    { id: 3, name: 'Recruting', count: 43 },
    { id: 4, name: 'Management', count: 65 },
    { id: 5, name: 'Advertising', count: 76 },
]

const salaryOptions = [
    { id: 1, name: '$0k - $20k', count: 12 },
    { id: 2, name: '$20k - $40k', count: 23 },
    { id: 3, name: '$40k - $60k', count: 43 },
    { id: 4, name: '$60k - $80k', count: 65 },
    { id: 5, name: '$80k - $100k', count: 76 },
    { id: 6, name: '> $100k', count: 10 },
]
</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-12 gap-4 min-h-screen">

        <div class="md:col-span-12 p-2">
            <h4 class="w-full flex justify-center mb-3">
                Descubre el trabajo que mejor se adapta a ti
            </h4>
            <SearchBar />
        </div>

        <!-- Sidebar -->
        <aside class="md:col-span-3 p-3">
            <nav>

                <div class="mt-2 mb-3">
                    <span><strong>Filtros avanzados</strong></span>
                </div>

                <hr />

                <FilterGroup title="Industry" :options="industryOptions" v-model="selectedIndustries" allOptionLabel="Todos" />

                <hr />

                <FilterGroup title="Salary Range" :options="salaryOptions" v-model="selectedSalaries" allOptionLabel="Todos" />
            </nav>
        </aside>

        <!-- Main content -->
        <main class="md:col-span-9 p-3">

            <div class="flex justify-between items-center">
                <div class="text-left">
                    <span>Mostrando <strong>41-60 </strong>de <strong>944 </strong>ofertas</span>
                </div>
                <div class="text-right">
                    <div class="flex items-center gap-3">
                        <span>Mostrar:</span>
                        <n-select
                            :options="pageSizes"
                            v-model:value="pageSize"
                            :consistent-menu-width="false"
                        />

                        <span class="ml-4">Orden:</span>
                        <n-select
                            :options="sortOptions"
                            v-model:value="sort"
                            :consistent-menu-width="false"
                        />
                    </div>
                </div>
            </div>

            <hr />

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <JobCard v-for="i in 12" :key="i" class="hover-up" />

                <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center text-gray-500">
                    <!-- <p>No hay resultados para tu búsqueda</p> -->
                    <n-pagination
                        v-model:page="page"
                        :page-size="pageSize"
                        :item-count="total"
                        :page-sizes="pageSizes.map(o => o.value)"
                        class="mt-4 flex justify-center"
                    />
                </div>
                
            </div>
        </main>
    </div>
</template>
