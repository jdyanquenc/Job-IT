<script setup lang="ts">
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia';
import { timeAgo } from '@/helpers';
import { useJobsStore } from '@/stores';
import { useJobApplication } from '@/composables/useJobApplication'
import { useRoute } from 'vue-router'

import { NAlert, NCard, NImage, NText, NSkeleton, NDivider, NButton, NGrid, NGi, NIcon } from "naive-ui"
import {
    CallOutline, MailOutline, LocationOutline, TimeOutline, BriefcaseOutline,
    CashOutline, BarChartOutline, CalendarOutline,
} from "@vicons/ionicons5"


const route = useRoute()
const jobsStore = useJobsStore()

const id = route.params.id

const hover = ref(false)
const { handleApply } = useJobApplication()
const { job, relatedJobs } = storeToRefs(jobsStore);

async function loadJobData() {
    await Promise.all([
        jobsStore.getById(id as string),
        jobsStore.getRelatedJobs(id as string)
    ]);
}

scrollTo(0, 0)
loadJobData()

watch(() => id, () => {
    loadJobData()
})

const company = {
    name: "AliThemes",
    location: "New York, US",
    jobsOpen: 2,
    address: "205 North Michigan Avenue, Suite 810 Chicago, 60601, USA",
    phone: "(123) 456-7890",
    email: "contact@Evara.com",
    mapEmbed: "https://maps.google.com/maps?q=chicago%20michigan%20avenue&t=&z=13&ie=UTF8&iwloc=&output=embed"
}


</script>

<template>
    <div class="w-full">

        <n-alert type="success" v-if="job && job.has_applied" show-icon>
            Ya te encuentras postulado a esta oferta.
        </n-alert>

        <div class="flex mt-4 ml-2">
            <h2 class="text-2xl font-bold mb-2">{{ job.job_title }}</h2>
        </div>

        <hr class="mt-2 mb-2" />

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 ml-5 flex-1 basis-2/3">

                <n-card class="mb-10" bordered>

                    <n-grid cols="1 640:2" x-gap="24" y-gap="16">
                        <!--
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BusinessOutline" />
                                <n-text strong>Industry:</n-text>
                                <n-text>{{ employmentInfo.industry }}</n-text>
                            </div>
                        </n-gi>
-->
                        <!--
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="PersonOutline" />
                                <n-text strong>Job level:</n-text>
                                <n-text>{{ employmentInfo.jobLevel }}</n-text>
                            </div>
                        </n-gi>
-->

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="CashOutline" />
                                <n-text strong>Rango salarial:</n-text>
                                <n-text>{{ (Number(job.salary_min || 0) / 1000) }}k - {{ (Number(job.salary_max || 0)
                                    / 1000) }}k {{ job.currency_code }}</n-text>
                            </div>
                        </n-gi>

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BarChartOutline" />
                                <n-text strong>Experiencia:</n-text>
                                <n-text>{{ job.experience_min_years }} años</n-text>
                            </div>
                        </n-gi>

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BriefcaseOutline" />
                                <n-text strong>Tipo de trabajo:</n-text>
                                <n-text>{{ job.employment_type }}</n-text>
                            </div>
                        </n-gi>

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="CalendarOutline" />
                                <n-text strong>Fecha límite:</n-text>
                                <n-text>{{ job.expires_at ? new Date(job.expires_at).toLocaleDateString() : 'N/A'
                                    }}</n-text>
                            </div>
                        </n-gi>

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="TimeOutline" />
                                <n-text strong>Actualizado:</n-text>
                                <n-text>{{ new Date(job.updated_at || job.created_at).toLocaleDateString() }}</n-text>
                            </div>
                        </n-gi>

                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="LocationOutline" />
                                <n-text strong>Ubicación:</n-text>
                                <n-text>{{ job.location }}</n-text>
                            </div>
                        </n-gi>
                    </n-grid>
                </n-card>

                <article class="prose prose-gray">
                    <h2>Descripción</h2>
                    <p>
                        <span v-if="!job.job_description" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.job_description">{{ job.job_description }}</n-text>
                    </p>

                    <h2>Responsabilidades</h2>
                    <p>
                        <span v-if="!job.responsibilities" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.responsibilities">{{ job.responsibilities }}</n-text>
                    </p>

                    <h2>Beneficios</h2>
                    <p>
                        <span v-if="!job.benefits" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.benefits">{{ job.benefits }}</n-text>
                    </p>

                    <div v-if="job.tags && job.tags.length">
                        <h2>Etiquetas</h2>
                        <ul>
                            <li v-for="(tag, index) in job.tags" :key="index">{{ tag }}</li>
                        </ul>
                    </div>

                    <div class="flex justify-center">
                        <n-button type="primary" :ghost="!hover" @click="handleApply(job.id)"
                            :disabled="job.has_applied">
                            {{ job.has_applied ? 'Postulado' : 'Postularme' }}
                        </n-button>
                    </div>
                </article>


            </main>

            <!-- Sidebar -->

            <div class="p-2 mr-2 basis-1/3 flex flex-col gap-6">

                <n-card>
                    <div class="flex items-center space-x-3">
                        <n-image :src="job.company_image_url || '/images/template/icons/logo-default.svg'" width="80" />

                        <div>
                            <n-text strong>{{ job.company_name }}</n-text>
                            <div class="text-gray-500 text-sm flex items-center space-x-1">
                                <n-icon :component="LocationOutline" /> <span>{{ job.location }}</span>, <span>{{
                                    job.country_code }}</span>
                            </div>
                            <n-button quaternary size="small" type="primary">
                                {{ company.jobsOpen }} oportunidades de empleo
                            </n-button>
                        </div>
                    </div>

                    <n-divider />

                    <!-- Map -->
                    <iframe :src="company.mapEmbed" class="w-full h-40 rounded-lg" style="border:0" allowfullscreen
                        loading="lazy"></iframe>

                    <n-divider />

                    <!-- Contact Info -->
                    <div class="space-y-3 text-sm">
                        <div class="flex items-center space-x-2">
                            <n-icon :component="LocationOutline" />
                            <span>{{ company.address }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <n-icon :component="CallOutline" />
                            <span>{{ company.phone }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <n-icon :component="MailOutline" />
                            <span>{{ company.email }}</span>
                        </div>
                    </div>
                </n-card>

                <!-- Similar Jobs -->
                <n-card title="Trabajos similares">
                    <div class="space-y-4">
                        <div v-for="(job, index) in relatedJobs" :key="index" class="flex items-start space-x-3">

                            <n-image width="60"
                                :src="job.company_image_url || '/images/template/icons/logo-default.svg'"
                                class="flex-shrink-0" />
                            <div>
                                <n-text strong>{{ job.job_title.substring(0, 35) }}</n-text>
                                <div class="flex items-center text-sm text-gray-500 space-x-2">
                                    <n-icon :component="BriefcaseOutline" /> <span>{{ job.employment_type }}</span>
                                    <n-icon :component="TimeOutline" /> <span>{{ timeAgo(job.created_at?.toString() ||
                                        '') }}</span>

                                </div>

                                <div class="flex justify-between text-sm text-gray-500 space-x-2">
                                    <span class="text-primary-500 font-semibold"
                                        v-if="Number(job.salary_max) > 0">{{ (Number(job.salary_max) / 1000) }}k {{
                                        job.currency_code }}</span>
                                    <span class="text-primary-500 font-semibold" v-else>A convenir</span>
                                    <n-icon class="items-right" :component="LocationOutline" /> <span>{{ job.location
                                    }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </n-card>
            </div>
        </div>

    </div>
</template>