<script setup lang="ts">

import { watch } from 'vue'
import { storeToRefs } from 'pinia';

import { useProfileStore } from '@/stores';
import { useLoadingBar } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'

import { NCard, NSpace, NText, NSkeleton, NDivider, NButton, NIcon } from "naive-ui"
import { BriefcaseOutline, CashOutline, GlobeOutline, SchoolOutline, MailOutline, CallOutline } from "@vicons/ionicons5"



const route = useRoute()
const router = useRouter()
const profileStore = useProfileStore()
const loadingBar = useLoadingBar()


const id = route.params.id

const { profile } = storeToRefs(profileStore);

const degree_options = [
    { label: 'Bachillerato', value: 'HighSchool' },
    { label: 'Técnico', value: 'Associate' },
    { label: 'Pregrado', value: 'Bachelor' },
    { label: 'Especialización', value: 'Specialization' },
    { label: 'Maestría', value: 'Master' },
    { label: 'Doctorado', value: 'Doctorate' },
    { label: 'Otro', value: 'Other' },
]

async function loadProfileData() {
    loadingBar.start()
    try {
        await profileStore.load(id as string)
        loadingBar.finish()
    } catch {
        loadingBar.error()
        router.push("404")
    }
}

function translateDegree(degree: string) {
    const option = degree_options.find(opt => opt.value === degree)
    return option ? option.label : degree
}

function formatDate(date: number | null) {
    if (!date) return ""
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
}

watch(() => id, () => {
    loadProfileData()
})

loadProfileData()


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
                    <h1 class="text-2xl font-bold">{{ profile.full_name }}</h1>
                    <div class="text-gray-500">
                        <span>{{ profile.title }}</span> <span>{{ profile.location }}</span>
                    </div>

                    <h2>Acerca de Mi</h2>
                    <p>
                        <span v-if="!profile.description" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                        <n-text v-if="profile.description">{{ profile.description }}</n-text>
                    </p>

                    <h2>Educación</h2>
                    <p>
                        <span v-if="!profile.education_experiences" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                    </p>
                    <div v-if="profile.education_experiences">
                        <p v-for="education in profile.education_experiences" :key="education.id" class="mb-2">
                            <span class="font-semibold">{{ education.institution_name }}</span><br />
                            <span class="mt-1 text-gray-500">{{ translateDegree(education.degree) }} -
                                {{ education.field_of_study }}</span>
                        </p>
                    </div>

                    <h2>Experiencia Laboral</h2>
                    <p>
                        <span v-if="!profile.work_experiences" class="mb-2">
                            <n-skeleton text :repeat="2" /> <n-skeleton text style="width: 60%" />
                        </span>
                    </p>
                    <div v-if="profile.work_experiences">
                        <p v-for="experience in profileStore.profile.work_experiences" :key="experience.id">
                            <span class="font-semibold">{{ experience.company_name }}</span><br />
                            <span class="mt-1 text-gray-500">{{ experience.position }}</span><br />
                            <span>
                                {{ formatDate(experience.start_date) }} -
                                {{ experience.end_date ? formatDate(experience.end_date) : "Actualidad" }}
                            </span>
                        </p>
                    </div>

                    <div v-if="profile.skills && profile.skills.length">
                        <h2>Habilidades</h2>
                        <ul>
                            <li v-for="(skill, index) in profile.skills" :key="index">{{ skill }}</li>
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
                            <span><strong>Salario Esperado</strong>: $26k - $30k</span>
                        </n-space>

                        <n-space>
                            <n-icon size="20">
                                <GlobeOutline />
                            </n-icon>
                            <span><strong>Idiomas</strong>: Español, Inglés</span>
                        </n-space>

                        <n-space>
                            <n-icon size="20">
                                <SchoolOutline />
                            </n-icon>
                            <span><strong>Nivel Educativo</strong>: Especialización</span>
                        </n-space>
                    </n-space>

                    <n-divider />

                    <n-space vertical size="medium">
                        <n-space>
                            <span>Bogotá, Colombia</span>
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
                            <span>candidato@yopmail.com</span>
                        </n-space>
                    </n-space>

                    <div class="mt-4">
                        <n-button type="primary" block>
                            <n-icon size="18" class="mr-2">
                                <MailOutline />
                            </n-icon>
                            Enviar mensaje
                        </n-button>
                    </div>
                </n-card>

            </div>
        </div>

    </div>
</template>