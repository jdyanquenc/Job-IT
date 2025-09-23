<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia';

import { useJobsStore } from '@/stores';
import { NSelect, NPagination } from 'naive-ui'
import { useLoadingBar } from 'naive-ui'

import SearchBar from '@/components/SearchBar.vue'
import FilterGroup from '@/components/FilterGroup.vue'
import JobCard from '@/views/jobs/JobCard.vue'


const jobsStore = useJobsStore();
const { jobs } = storeToRefs(jobsStore);

const loadingBar = useLoadingBar()
const sort = ref('relevance')
const page = ref(1)
const pageSize = ref(12)
const total = ref(200)

const selectedIndustries = ref([])
const selectedSalaries = ref([])
const searchText = ref('')



const sortOptions = [
    { label: 'Relevancia', value: 'relevance' },
    { label: 'Fecha de publicación', value: 'date' },
    { label: 'Salario', value: 'salary' }
]

const pageSizes = [
    { label: '12 / pág', value: 12 },
    { label: '24 / pág', value: 24 },
    { label: '36 / pág', value: 36 }
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


function handleSearch(value) {
    loadingBar.start()
    jobsStore.find(value).finally(() => {
        loadingBar.finish()
    })
}

</script>

<template>
    <div class="w-full mx-auto">

        <div class="flex mb-4">
            <SearchBar v-model="searchText" @search="handleSearch" placeholder="Descubre nuevos retos para ti..." />
        </div>

        <div class="flex flex-col md:flex-row items-start gap-4">

            <!-- Sidebar -->
            <aside class="p-2 w-full md:w-1/4">
                <nav>
                    <div class="mt-2">
                        <span><strong>Filtros avanzados</strong></span>
                    </div>

                    <hr class="mt-4 mb-3" />

                    <FilterGroup title="Industry" :options="industryOptions" v-model="selectedIndustries"
                        allOptionLabel="Todos" />

                    <hr class="mt-4 mb-3" />

                    <FilterGroup title="Salary Range" :options="salaryOptions" v-model="selectedSalaries"
                        allOptionLabel="Todos" />
                </nav>
            </aside>

            <!-- Main content -->
            <main class="p-2 w-full md:w-3/4">
                <div class="flex justify-between items-center">
                    <div class="flex items-center md:block hidden">
                        <span>Mostrando <strong>41-60 </strong>de <strong>944 </strong>ofertas</span>
                    </div>
                    <div class="flex items-center">
                        <div class="flex items-center gap-3">
                            <span>Mostrar:</span>
                            <n-select :options="pageSizes" v-model:value="pageSize" :consistent-menu-width="false" />

                            <span>Orden:</span>
                            <n-select :options="sortOptions" v-model:value="sort" :consistent-menu-width="false" />
                        </div>
                    </div>
                </div>

                <hr class="mt-3 mb-3" />

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 place-items-center gap-4">
                    <JobCard v-for="job in jobs" :key="job.id" :job="job" class="hover-up" />

                    <div class="col-span-1 md:col-span-2 lg:col-span-3 text-gray-500">
                        <p v-if="jobs.length === 0" class="text-center">
                            No se encontraron ofertas de trabajo.
                        </p>
                        <n-pagination v-if="jobs.length !== 0" v-model:page="page" :page-size="pageSize"
                            :item-count="total" :page-sizes="pageSizes.map(o => o.value)"
                            class="mt-4 flex justify-center" />
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>
