<script setup lang="ts">

import { watch } from 'vue'
import { storeToRefs } from 'pinia';

import { useJobsStore } from '@/stores';
import { useLoadingBar } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'

import { NCard, NSpace, NText, NSkeleton, NDivider, NButton, NIcon } from "naive-ui"
import { BriefcaseOutline, CashOutline, GlobeOutline, SchoolOutline, MailOutline, CallOutline } from "@vicons/ionicons5"


const route = useRoute()
const router = useRouter()
const jobsStore = useJobsStore();
const loadingBar = useLoadingBar()

const id = route.params.id

const { job } = storeToRefs(jobsStore);


async function loadJobData() {
    loadingBar.start()
    try {
        await jobsStore.getById(id as string)
        loadingBar.finish()
    } catch {
        loadingBar.error()
        router.push('/404')
    }
}

loadJobData()


watch(() => id, () => {
    loadJobData()
})


</script>

<template>
    <div class="w-full">

        <div class="flex mt-4 ml-2">
            <h2 class="text-2xl font-bold mb-2">{{ }}</h2>
        </div>

        <hr class="mt-2 mb-2" />

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 ml-5 flex-1 basis-2/3">

                <article class="prose prose-gray">
                    <h2>Acerca de Mi</h2>
                    <p>
                        <span v-if="!job.job_description" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.job_description">{{ job.job_description }}</n-text>
                    </p>

                    <h2>Educación</h2>
                    <p>
                        <span v-if="!job.responsibilities" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.responsibilities">{{ job.responsibilities }}</n-text>
                    </p>

                    <h2>Experiencia Laboral</h2>
                    <p>
                        <span v-if="!job.benefits" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="job.benefits">{{ job.benefits }}</n-text>
                    </p>

                    <div v-if="job.tags && job.tags.length">
                        <h2>Habilidades</h2>
                        <ul>
                            <li v-for="(tag, index) in job.tags" :key="index">{{ tag }}</li>
                        </ul>
                    </div>

                </article>


            </main>

            <!-- Sidebar -->

            <div class="p-2 mr-2 basis-1/3 flex flex-col gap-6">

                <n-card class="max-w-md rounded-xl">
                    <h3 class="text-lg font-semibold mb-2">Overview</h3>
                    <n-divider />

                    <n-space vertical size="large">
                        <n-space>
                            <n-icon size="20">
                                <BriefcaseOutline />
                            </n-icon>
                            <span><strong>Experiencia</strong>: 12 años</span>
                        </n-space>

                        <n-space>
                            <n-icon size="20">
                                <CashOutline />
                            </n-icon>
                            <span><strong>Salario Esperado</strong>: $26k – $30k</span>
                        </n-space>

                        <n-space>
                            <n-icon size="20">
                                <GlobeOutline />
                            </n-icon>
                            <span><strong>Idiomas</strong>: Inglés, Alemán</span>
                        </n-space>

                        <n-space>
                            <n-icon size="20">
                                <SchoolOutline />
                            </n-icon>
                            <span><strong>Nivel Educativo</strong>: Master</span>
                        </n-space>
                    </n-space>

                    <n-divider />

                    <n-space vertical size="medium">
                        <n-space>
                            <span>205 North Michigan Avenue, Suite 810 Chicago, 60601, USA</span>
                        </n-space>
                        <n-space>
                            <n-icon size="20">
                                <CallOutline />
                            </n-icon>
                            <span>(123) 456-7890</span>
                        </n-space>
                        <n-space>
                            <n-icon size="20">
                                <MailOutline />
                            </n-icon>
                            <span>contact@Evara.com</span>
                        </n-space>
                    </n-space>

                    <div class="mt-4">
                        <n-button type="primary" block>
                            <n-icon size="18" class="mr-2">
                                <MailOutline />
                            </n-icon>
                            Send Message
                        </n-button>
                    </div>
                </n-card>

            </div>
        </div>

    </div>
</template>