<script setup lang="ts">

import { ref } from "vue"

import { NCard, NButton, NImage, NTag, NIcon, NText } from "naive-ui";

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
    <n-card class="max-w-sm rounded-2xl shadow-md p-2" @mouseenter="hover = true" @mouseleave="hover = false">
        <!-- Header -->
        <div class="flex items-center justify-between mb-2">
            <n-image :src="props.job.company.logo_url || '/images/template/icons/logo-default.svg'" width="100" />
            <div>
                <h4 class="font-semibold text-lg">{{ props.job.company.name }}</h4>
                <p class="text-gray-500 text-sm">{{ props.job.company.location }}, {{ props.job.company.country_code }}</p>
            </div>
        </div>

        <!-- Job Title -->
        <div class="mb-2">
            
                <h4 class="text-lg font-bold">
                    <router-link :to="{ name: 'JobDetail', params: { id: props.job.id } }">
                        {{ props.job.job_title }}
                    </router-link>
                </h4>
            <div class="flex justify-between text-sm text-gray-500">

                <div class="flex items-center space-x-2">
                    <n-icon :component="BriefcaseOutline" />
                    <n-text class="ml-1"> {{ props.job.employment_type }}</n-text>
                </div>

                <div class="flex items-center">
                    <n-icon :component="TimeOutline" />
                    <n-text class="ml-2"> {{ new Date(props.job.created_at).toLocaleDateString() }}</n-text>
                </div>
            </div>
        </div>

        <!-- Description -->
        <p class="text-gray-600 text-sm mb-3">
            <router-link :to="{ name: 'JobDetail', params: { id: props.job.id } }">
                {{ props.job.job_short_description }}
            </router-link>
        </p>

        <!-- Skills -->
        <div class="flex flex-wrap gap-2 mb-3">
            <n-tag v-for="skill in props.job.skills_required" :type="hover ? 'success' : 'default'" round>{{ skill }}</n-tag>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between">
            <div>
                <span class="font-bold text-lg">{{ props.job.salary_range }}</span>
            </div>
            <n-button type="primary" :ghost="!hover">
                Apply Now
            </n-button>
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