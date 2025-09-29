<script setup lang="ts">
import { NInput } from "naive-ui"

defineProps({
    modelValue: String
})
const emit = defineEmits(["update:modelValue"])
</script>


<template>
    <div class="w-full mb-4">
        <span class="font-medium mb-2">Descripción Personal</span>
        <n-input :value="modelValue" type="textarea" placeholder="Cuéntanos sobre ti, tu perfil profesional y tus metas"
            rows="4" @update:value="emit('update:modelValue', $event)" />
    </div>
</template>
