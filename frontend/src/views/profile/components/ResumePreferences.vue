<script setup lang="ts">
import { useProfileStore } from "@/stores"
import InlineEditableInput from "@/components/InlineEditableInput.vue"
import InlineEditableSelect from "@/components/InlineEditableSelect.vue";
import {
    NSpace
} from "naive-ui"

const profileStore = useProfileStore()

const salaryOptions = [
    { label: "$10k - $15k", value: "1" },
    { label: "$15k - $20k", value: "2" },
    { label: "$20k - $25k", value: "3" },
    { label: "$25k - $30k", value: "4" }
]

const modalityOptions = [
    { label: "Remoto", value: "remote" },
    { label: "Presencial", value: "onsite" },
    { label: "Híbrido", value: "hybrid" }
]

</script>


<template>
    <n-space vertical>

        <InlineEditableSelect v-model="profileStore.profile.modality" label="Tipo de empleo preferido"
            :options="modalityOptions" placeholder="Selecciona una modalidad" @save="profileStore.updateModality" />

        <InlineEditableInput v-model="profileStore.profile.location" label="Lugar de Residencia" type="text"
            placeholder="Ej: Bogotá, Colombia" @save="profileStore.updateLocation" />

        <InlineEditableSelect v-model="profileStore.profile.salary_range" label="Rango Salarial Estimado"
            :options="salaryOptions" placeholder="Selecciona un rango salarial"
            @save="profileStore.updateSalaryRange" />

    </n-space>
</template>
