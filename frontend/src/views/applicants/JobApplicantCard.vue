<script setup lang="ts">

import { ref } from "vue"

import { NCard, NImage, NTag, NRate } from "naive-ui";


import type { JobApplicant } from "@/types";

const props = defineProps({
    applicant: {
        type: Object as () => JobApplicant,
        required: true
    }
})

const hover = ref(false)


</script>

<template>
    <n-card class="max-w-sm min-h-[300px] rounded-2xl shadow-md p-2" @mouseenter="hover = true"
        @mouseleave="hover = false">
        <!-- Header -->
        <div class="flex items-center justify-between mb-2">
            <n-image :src="props.applicant.photo_url || '/images/template/icons/photo-default.svg'" width="100" />
            <div>
                <h4 class="font-semibold text-lg">{{ props.applicant.first_name }} {{ props.applicant.last_name }}</h4>
                <n-rate readonly :default-value="4" />
            </div>
        </div>

        <!-- Job Title -->
        <div class="mb-2">

            <h4 class="text-lg font-bold">
                <router-link :to="{ name: 'UserProfileDetail', params: { id: props.applicant.user_id } }">
                    {{ props.applicant.title }}
                </router-link>
            </h4>

        </div>

        <!-- Description -->
        <p class="h-[95px] text-gray-600 text-sm mb-3 overflow-hidden text-ellipsis">
            <router-link :to="{ name: 'UserProfileDetail', params: { id: props.applicant.user_id } }">
                {{ props.applicant.description }}
            </router-link>
        </p>

        <!-- Skills -->
        <div class="flex flex-wrap gap-2 mb-3">
            <n-tag v-for="skill in props.applicant.skills" :key="skill" :type="hover ? 'success' : 'default'" round>
                {{ skill }}
            </n-tag>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between">
            <div>
                <span class="font-bold text-lg">{{ props.applicant.location }}</span>
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