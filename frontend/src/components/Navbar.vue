<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useAuthStore } from '@/stores';
import { RouterLink } from 'vue-router'

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);

</script>

<template>
    <nav class="bg-white shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="flex justify-between items-center">

                <!-- Logo -->
                <div class="flex justify-center items-center py-2 logo-container">
                    <img src="/images/template/jobit-logo.svg" alt="Logo" class="h-11 w-auto" />
                </div>

                <!-- Menu -->
                <ul class="md:flex items-center gap-6 text-sm text-gray-700 menu-container" v-if="user !== null">
                    <RouterLink to="/">Inicio ▾</RouterLink>
                    <RouterLink to="/users">Usuarios ▾</RouterLink>
                    <RouterLink to="/jobs">Ofertas ▾</RouterLink>
                    <RouterLink to="/company-jobs">Mis ofertas ▾</RouterLink>
                </ul>

                <!-- Actions -->
                <div class="flex items-center gap-4 text-sm text-gray-700 action-container">
                    <RouterLink to="/account/register" class="hover:underline" v-if="user === null">Regístrate</RouterLink>
                    <RouterLink to="/account/login" class="hover:underline" v-if="user === null">Inicia sesión</RouterLink>
                    <RouterLink to="#" class="hover:underline" v-if="user !== null" @click="authStore.logout()">Cierra sesión</RouterLink>
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>

.logo-container {
    width: 20%;
}

.menu-container {
    width: 60%;
    justify-content: center;
}

.action-container {
    width: 20%;
    justify-content: flex-end;
}

</style>