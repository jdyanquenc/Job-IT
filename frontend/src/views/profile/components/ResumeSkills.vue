<script setup lang="ts">
import InlineEditTags from "@/components/InlineEditableTags.vue"
import { useProfileStore } from "@/stores"

const profileStore = useProfileStore()

</script>

<template>

    <InlineEditTags v-model="profileStore.profile.skills" label="Habilidades"
        placeholder="Agrega una habilidad y presiona Enter" />

    <div class="text-sm text-white">
        {{ profileStore.profile.skills }}
    </div>

</template>
