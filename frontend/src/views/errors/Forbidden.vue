<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useRouter } from 'vue-router'
import { NResult, NButton } from 'naive-ui'

const router = useRouter()

function goHome() {
    router.push({ path: '/' })
}
</script>

<template>
    <div class="w-full mx-auto">
        <div class="flex flex-col items-center justify-center h-screen text-center">
            <n-result status="403" title="Acceso denegado" description="No tienes permiso para acceder a esta página.">
                <template #footer>
                    <n-button type="primary" @click="goHome">
                        Volver al inicio
                    </n-button>
                </template>
            </n-result>
        </div>
    </div>
</template>

<style scoped>
body {
    background-color: #f7fafa;
}
</style>
