<script setup lang="ts">

import { ref } from "vue"

import { NCard, NButton, NTag, NIcon, NText } from "naive-ui";

import {
    BriefcaseOutline,
    TimeOutline
} from "@vicons/ionicons5"

import type { Job } from "@/types";

const props = defineProps({
    job: {
        type: Object as () => Job,
        required: true
    }
})

const hover = ref(false)



</script>

<template>
    <n-card class="w-full rounded-2xl shadow-md p-2" @mouseenter="hover = true" @mouseleave="hover = false">

        <!-- Job Title -->
        <div class="mb-2">

            <div class="flex justify-between">
                <h4 class="text-lg font-bold">
                    <router-link :to="{ name: 'JobDetail', params: { id: props.job.id } }">
                        {{ props.job.job_title }}
                    </router-link>
                </h4>
                <div class="flex gap-4 text-sm text-gray-500">
                    <div class="flex items-center">
                        <n-icon :component="BriefcaseOutline" />
                        <n-text class="ml-1"> {{ props.job.employment_type }}</n-text>
                    </div>

                    <div class="flex items-center">
                        <n-icon :component="TimeOutline" />
                        <n-text class="ml-2"> {{ new Date(props.job.created_at).toLocaleDateString() }}</n-text>
                    </div>
                </div>
            </div>
        </div>

        <!-- Description -->
        <p class="text-gray-600 text-sm mb-3 overflow-hidden text-ellipsis">
            <router-link :to="{ name: 'JobDetail', params: { id: props.job.id } }">
                {{ props.job.job_short_description }}
            </router-link>
        </p>

        <!-- Skills -->
        <div class="flex flex-wrap gap-2 mb-3">
            <n-tag v-for="skill in props.job.tags" :key="skill" :type="hover ? 'success' : 'default'" round>{{ skill
            }}</n-tag>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between">
            <div>
                <span class="font-bold text-lg">{{ props.job.salary_range }}</span>
            </div>
            <div class="flex gap-2">
                <n-button type="primary" :ghost="!hover"
                    @click="$router.push({ name: 'ApplicantList', params: { id: props.job.id } })">
                    Ver Postulantes
                </n-button>
                <n-button type="warning" :ghost="!hover"
                    @click="$router.push({ name: 'CompanyJobEdit', params: { id: props.job.id } })">
                    Editar
                </n-button>
                <n-button type="error" :ghost="!hover">
                    Eliminar
                </n-button>
            </div>
        </div>
    </n-card>
</template>

<style scoped>
.n-card {
    background-color: #f7fafa;
}

.n-card:hover {
    background-color: #fff;
}
</style>