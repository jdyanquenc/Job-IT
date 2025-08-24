<script setup>

import { NCard, NButton, NIcon, NTag } from "naive-ui";

import { ref } from "vue"

const hover = ref(false)

</script>

<template>
    <n-card class="max-w-sm rounded-2xl shadow-md p-2" @mouseenter="hover = true" @mouseleave="hover = false">
        <!-- Header -->
        <div class="flex items-center justify-between mb-2">
            <n-button quaternary circle>
                <template #icon>
                    <n-icon>
                        
                    </n-icon>
                </template>
            </n-button>
            <div>
                <h3 class="font-semibold text-lg">LinkedIn</h3>
                <p class="text-gray-500 text-sm">New York, US</p>
            </div>
        </div>

        <!-- Job Title -->
        <div class="mb-2">
            <h2 class="text-lg font-bold">UI / UX Designer fulltime</h2>
            <div class="flex gap-4 text-sm text-gray-500">
                <span>Fulltime</span>
                <span>4 minutes ago</span>
            </div>
        </div>

        <!-- Description -->
        <p class="text-gray-600 text-sm mb-3">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Recusandae architecto eveniet, dolor quo repellendus pariatur
        </p>

        <!-- Skills -->
        <div class="flex flex-wrap gap-2 mb-3">
            <n-tag type="default" round>Adobe XD</n-tag>
            <n-tag type="default" round>Figma</n-tag>
            <n-tag type="default" round>Photoshop</n-tag>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between">
            <span class="text-emerald-600 font-bold text-lg">$500</span>
            <span class="text-gray-500">/Hour</span>

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