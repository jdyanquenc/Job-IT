<script setup lang="ts">
import InlineEditableInput from "@/components/InlineEditableInput.vue"
import { useProfileStore } from "@/stores"
import { useRoute } from "vue-router"

const route = useRoute()
const profileStore = useProfileStore()

const id = route.params.id
profileStore.load(id as string)

</script>


<template>

    <InlineEditableInput v-model="profileStore.profile.description" label="Acerca de Mi" type="textarea"
        placeholder="Cuéntanos sobre ti, tu perfil profesional y tus metas. Haz clic para editar"
        @save="profileStore.updateDescription" />

</template>
