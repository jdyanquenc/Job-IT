<template>
    <div class="w-full flex justify-center">
        <div class="flex w-full max-w-2xl items-center gap-2 p-2">

            <n-input type="text" size="large" v-model="keyword" placeholder="Ingresa la plabra clave..." 
                @keyup.enter="searchJobs" />

            <!-- Icon -->
            <n-button type="primary" size="large" @click="searchJobs">
                <template #icon>
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 21l-4.35-4.35M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z" />
                        </svg>
                    </n-icon>
                </template>
                Buscar
            </n-button>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { NInput, NButton, NIcon } from "naive-ui"

const keyword = ref("")

function searchJobs() {
    if (keyword.value.trim()) {
        // Replace with your API call or router push
        console.log("Searching jobs for:", keyword.value)
    }
}
</script>