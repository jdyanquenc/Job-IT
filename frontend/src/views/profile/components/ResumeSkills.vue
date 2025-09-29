<script setup lang="ts">
import { computed } from "vue"
import { NDynamicTags, NFormItem } from "naive-ui"

const props = defineProps({
    modelValue: { type: Array, required: true }
})
const emit = defineEmits(["update:modelValue"])

const localValue = computed({
    get: () => props.modelValue,
    set: (val) => emit("update:modelValue", val)
})
</script>

<template>
    <n-form-item label="Habilidades Técnicas">
        <n-dynamic-tags v-model:value="localValue" placeholder="Agrega una habilidad y presiona Enter" />
    </n-form-item>
</template>
