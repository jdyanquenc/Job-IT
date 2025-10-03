<script setup lang="ts">
import InlineEditableInput from "@/components/InlineEditableInput.vue"
import { useProfileStore } from "@/stores"

const profileStore = useProfileStore()

</script>


<template>

    <InlineEditableInput v-model="profileStore.profile.title" label="Título" type="text"
        placeholder="Ingresa tu título profesional" @save="profileStore.updateTitle" />

    <InlineEditableInput v-model="profileStore.profile.description" label="Acerca de Mi" type="textarea"
        placeholder="Cuéntanos sobre ti, tu perfil profesional y tus metas. Haz clic para editar"
        @save="profileStore.updateDescription" />

</template>
