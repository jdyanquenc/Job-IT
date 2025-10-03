<script setup lang="ts">

import { ref, watch } from 'vue';
import { useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores';

import { NDropdown, NAvatar, NText } from 'naive-ui';

const route = useRoute();
const authStore = useAuthStore();


// Opciones del menú
const options = [
    { key: "settings", label: "Configuración" },
    { key: "password", label: "Cambiar contraseña" },
    { key: "logout", label: "Cerrar sesión" },
]

// Manejo de acción al seleccionar
const handleSelect = (key: string) => {
    if (key === "logout") {
        authStore.logout()
    }
}

const palette = [
    "#18A058", // verde principal
    "#2C4658", // azul oscuro
    "#6B7982", // gris azulado
    "#97C7AC", // verde claro
    "#2C4658", // azul oscuro sobrio
    "#1F3342", // azul casi negro
    "#6B7982", // gris azulado medio
]

// Función para obtener iniciales (primer y última palabra)
function getInitials(name = '') {
    const trimmed = (name || '').trim()
    if (!trimmed) return ''
    const parts = trimmed.split(/\s+/)
    if (parts.length === 1) {
        return parts[0].slice(0, 2).toUpperCase()
    }
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

// Función para elegir color según iniciales
const getColorFromName = (name: string) => {
    let hash = 0
    for (let i = 0; i < name.length; i++) {
        hash += name.charCodeAt(i)
    }
    return palette[hash % palette.length]
}

const redirectToProfile = () => {
    if (authStore.isCandidate()) {
        return `/profile/edit/${authStore.getUserId()}`
    } else if (authStore.isCompanyManager()) {
        return "/company-profile"
    } else {
        return "/"
    }
}

// Computed values
const userName = ref(authStore.getTokenData()?.name || "Usuario Anónimo")
const initials = ref(getInitials(userName.value))
const avatarColor = ref(getColorFromName(userName.value))
const isAccountRoute = ref(route.path.startsWith("/accounts/"));

watch(() => authStore.isTokenValid, () => {
    // Si el token cambia (login/logout), recalcular iniciales y color
    userName.value = authStore.getTokenData()?.name || "Usuario Anónimo"
    initials.value = getInitials(userName.value)
    avatarColor.value = getColorFromName(userName.value)
})

watch(() => route.path, () => {
    // Si la ruta cambia, verificar si es una ruta de cuenta
    // Esto afecta la visibilidad de los enlaces de registro/inicio de sesión
    isAccountRoute.value = route.path.startsWith("/accounts/")
})

</script>

<template>
    <nav class="bg-white shadow">
        <div class="max-w-screen-xl mx-auto">
            <div class="flex justify-between items-center">

                <!-- Logo -->
                <div class="flex justify-center items-center py-2 logo-container">
                    <RouterLink to="/"><img src="/images/template/jobit-logo.svg" alt="Logo" class="h-11 w-auto" />
                    </RouterLink>
                </div>

                <!-- Menu -->
                <ul class="md:flex items-center gap-6 text-sm text-gray-700 menu-container"
                    v-if="authStore.isLoggedIn()">
                    <RouterLink to="/">Inicio ▾</RouterLink>

                    <RouterLink v-if="authStore.isCandidate()" to="/jobs">Ofertas ▾</RouterLink>
                    <RouterLink v-if="authStore.isCandidate()" :to="redirectToProfile()">Mi Hoja de
                        Vida ▾</RouterLink>
                    <RouterLink v-if="authStore.isCandidate()" to="/jobs/applications">Mis postulaciones ▾</RouterLink>
                    <RouterLink v-if="authStore.isCandidate()" to="/jobs/recommendations">Mis recomendaciones ▾
                    </RouterLink>

                    <RouterLink v-if="authStore.isCompanyManager()" to="/jobs">Ofertas ▾</RouterLink>
                    <RouterLink v-if="authStore.isCompanyManager()" to="/company-jobs">Mis ofertas ▾</RouterLink>
                    <RouterLink v-if="authStore.isCompanyManager()" to="/company-profile">Mi empresa ▾</RouterLink>

                    <RouterLink v-if="authStore.isAdmin()" to="/users">Usuarios ▾</RouterLink>
                    <RouterLink v-if="authStore.isAdmin()" to="/companies">Empresas ▾</RouterLink>
                </ul>

                <!-- Actions -->
                <div class="flex items-center gap-4 text-sm text-gray-700 action-container">
                    <RouterLink to="/accounts/register" class="hover:underline"
                        v-if="!authStore.isLoggedIn() && !isAccountRoute">
                        Regístrarse
                    </RouterLink>
                    <RouterLink to="/accounts/login" class="hover:underline"
                        v-if="!authStore.isLoggedIn() && !isAccountRoute">
                        Iniciar sesión
                    </RouterLink>

                    <n-dropdown v-if="authStore.isLoggedIn()" :options="options" trigger="click" @select="handleSelect"
                        placement="bottom-end">
                        <div class="flex items-center gap-2 cursor-pointer">
                            <n-text class="hidden md:inline text-capitalize">{{ userName }}</n-text>
                            <n-avatar round :style="{ color: 'white', backgroundColor: avatarColor }">
                                {{ initials }}
                            </n-avatar>
                        </div>
                    </n-dropdown>

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