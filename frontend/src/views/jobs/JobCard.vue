<script setup lang="ts">

import { ref } from "vue"
import { NCard, NButton, NImage, NTag } from "naive-ui";
import IconJobType from "@/components/icons/IconJobType.vue";
import IconJobPosted from "@/components/icons/IconJobPosted.vue";

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
                <h3 class="font-semibold text-lg">{{ props.job.company.name }}</h3>
                <p class="text-gray-500 text-sm">{{ props.job.company.location }}, {{ props.job.company.country_code }}</p>
            </div>
        </div>

        <!-- Job Title -->
        <div class="mb-2">
            <h2 class="text-lg font-bold">{{ props.job.job_title }}</h2>
            <div class="flex items-center justify-between text-sm text-gray-500">
                <IconJobType /><span class="mr-17">  {{ props.job.employment_type }}</span>
                <IconJobPosted /><span>{{ new Date(props.job.created_at).toLocaleDateString() }}</span>
            </div>
        </div>

        <!-- Description -->
        <p class="text-gray-600 text-sm mb-3">
            {{ props.job.job_short_description }}
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