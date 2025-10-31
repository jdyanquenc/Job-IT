<script setup lang="ts">
import { ref } from 'vue'
import { watch } from 'vue';
import { storeToRefs } from 'pinia';

import { useJobsStore } from '@/stores';
import { NSelect, NPagination } from 'naive-ui'

import SearchBar from '@/components/SearchBar.vue'
import FilterGroup from '@/components/FilterGroup.vue'
import JobCard from '@/views/jobs/JobCard.vue'


const jobsStore = useJobsStore();
const { jobs } = storeToRefs(jobsStore);
const { jobCountBySector } = storeToRefs(jobsStore);


const country_code = ref('US')
const sort = ref('relevance')
const page = ref(1)
const page_size = ref(12)
const total = ref(10)

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



const salaryOptions = [
    { id: 1, name: '$0k - $20k', count: 12 },
    { id: 2, name: '$20k - $40k', count: 23 },
    { id: 3, name: '$40k - $60k', count: 43 },
    { id: 4, name: '$60k - $80k', count: 65 },
    { id: 5, name: '$80k - $100k', count: 76 },
    { id: 6, name: '> $100k', count: 10 },
]


async function handleSearch(value: string, pageNumber: number = page.value) {
    await jobsStore.find(value, pageNumber, page_size.value, country_code.value, sort.value, selectedIndustries.value)
    await jobsStore.loadJobCountBySector(value, country_code.value)
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onPageSizeChange(new_page_size: number) {
    page_size.value = new_page_size
    handleSearch(searchText.value)
}

handleSearch('')

// Calcular el total  sumando el conteo de cada sector en un watch

watch(jobCountBySector,
    (newVal) => {
        total.value = newVal?.map(sector => sector.count).reduce((a, b) => a + b, 0) || 0
    },
    { immediate: true }
);



</script>

<template>
    <div class="w-full mx-auto">

        <div class="flex mb-4">
            <SearchBar v-model="searchText" @search="handleSearch(searchText, 1)"
                placeholder="Descubre nuevos retos para ti..." />
        </div>

        <div class="flex flex-col md:flex-row items-start gap-4">

            <!-- Sidebar -->
            <aside class="p-2 w-full md:w-1/4">
                <nav>
                    <div class="mt-2">
                        <span><strong>Filtros avanzados</strong></span>
                    </div>

                    <hr class="mt-4 mb-3" />

                    <FilterGroup title="Industria" :options="jobCountBySector" v-model="selectedIndustries"
                        :showAllOption="false" />

                    <hr class="mt-4 mb-3" />

                    <FilterGroup title="Rango salarial" :options="salaryOptions" v-model="selectedSalaries"
                        :showAllOption="false" />
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
                            <n-select :options="pageSizes" v-model:value="page_size" :consistent-menu-width="false" />

                            <span>Orden:</span>
                            <n-select :options="sortOptions" v-model:value="sort" :consistent-menu-width="false"
                                @update:value="handleSearch(searchText, 1)" />
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
                        <n-pagination v-if="jobs.length !== 0" v-model:page="page" :page-size="page_size"
                            :item-count="total" :page-sizes="pageSizes.map(o => o.value)"
                            @update:page="handleSearch(searchText)" @update:page-size="onPageSizeChange"
                            class="mt-4 flex justify-center" />
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>
