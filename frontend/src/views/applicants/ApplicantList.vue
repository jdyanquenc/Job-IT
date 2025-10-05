<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia';

import { useApplicantsStore } from '@/stores';
import { NSelect, NPagination } from 'naive-ui'

import SearchBar from '@/components/SearchBar.vue'
import ApplicantCard from './ApplicantCard.vue';
import { useRoute } from 'vue-router';


const applicantsStore = useApplicantsStore();
const { applicants } = storeToRefs(applicantsStore);

const route = useRoute()
const sort = ref('relevance')
const page = ref(1)
const pageSize = ref(12)
const total = ref(200)

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


const id = String(route.params.id)



async function handleSearch(id: string, value: string) {
    await applicantsStore.find(id, value)
}

watch(() => id, () => {
    handleSearch(id, searchText.value)
})

handleSearch(id, '')

</script>

<template>
    <div class="w-full mx-auto">

        <div class="flex mb-4">
            <SearchBar v-model="searchText" @search="handleSearch" placeholder="Ingresa palabras clave..." />
        </div>

        <div class="flex flex-col md:flex-row items-start gap-4">

            <!-- Main content -->
            <main class="p-2 w-full">
                <div class="flex justify-between items-center">
                    <div class="flex items-center md:block hidden">
                        <span>Mostrando <strong>1-10 </strong>de <strong>20 </strong>postulantes</span>
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

                <div class="flex flex-col gap-4">

                    <ApplicantCard v-for="applicant in applicants" :key="applicant.user_id" :applicant="applicant"
                        class="hover-up" />

                    <div class="col-span-1 md:col-span-2 lg:col-span-3 text-gray-500">
                        <p v-if="applicants.length === 0" class="text-center">
                            No se encontraron postulantes.
                        </p>
                        <n-pagination v-if="applicants.length !== 0" v-model:page="page" :page-size="pageSize"
                            :item-count="total" :page-sizes="pageSizes.map(o => o.value)"
                            class="mt-4 flex justify-center" />
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>
