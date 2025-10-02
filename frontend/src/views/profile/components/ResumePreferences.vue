<script setup lang="ts">
import { computed } from "vue"
import { useProfileStore } from "@/stores"
import InlineEditableInput from "@/components/InlineEditableInput.vue"
import {
    NSelect, NRadioGroup, NRadio, NFormItem, NSpace, NInput
} from "naive-ui"
import { storeToRefs } from "pinia"

const props = defineProps({
    modelValue: { type: Object, required: true }
})

const profileStore = useProfileStore()

const { profile } = storeToRefs(profileStore)

const emit = defineEmits(["update:modelValue"])

// Proxy reactivo para evitar mutar directamente el prop
const localValue = computed(() => props.modelValue)

function updateField(field: string, value: unknown) {
    emit("update:modelValue", { ...props.modelValue, [field]: value })
}

const salaryOptions = [
    { label: "$10k - $15k", value: "10-15" },
    { label: "$15k - $20k", value: "15-20" },
    { label: "$20k - $25k", value: "20-25" },
    { label: "$25k - $30k", value: "25-30" }
]
</script>


<template>
    <n-space vertical>

        <n-form-item label="Tipo de empleo preferido">
            <n-radio-group :value="localValue.job_type" @update:value="updateField('job_type', $event)">
                <n-space>
                    <n-radio value="remote">Remoto</n-radio>
                    <n-radio value="onsite">Presencial</n-radio>
                    <n-radio value="hybrid">Híbrido</n-radio>
                </n-space>
            </n-radio-group>
        </n-form-item>

        <inline-editable-input v-model="profile.location" label="Lugar de Residencia" type="text"
            placeholder="Ej: Bogotá, Colombia" @save="profileStore.updateLocation" />

        <n-form-item label="Lugar de Residencia Old">
            <n-input :value="localValue.location" placeholder="Ej: Ciudad de México, CDMX"
                @update:value="updateField('location', $event)" />
        </n-form-item>

        <n-form-item label="Rango Salarial Estimado">
            <n-select :value="localValue.salary_range" :options="salaryOptions" placeholder="Selecciona rango"
                @update:value="updateField('salary_range', $event)" />
        </n-form-item>
    </n-space>
</template>
