<script setup lang="ts">
import { ref } from "vue"
import { useCompanyStore } from "@/stores/company.store"
import {
    NForm, NFormItem, NInput, NDatePicker, NModal,
    NButton, NSpace, NCard, NSelect
} from "naive-ui"

const companyStore = useCompanyStore()

import { Add, Pencil, Trash } from "@vicons/ionicons5"

export interface WorkExperience {
    company: string
    position: string
    description: string
    startDate: number | null
    endDate: number | null
}


const props = defineProps({
    modelValue: { type: Array<WorkExperience>, required: true }
})
const emit = defineEmits(["update:modelValue"])

const showModal = ref(false)
const tempExperience = ref<WorkExperience>(createExperience())



function createExperience(): WorkExperience {
    return {
        company: "",
        position: "",
        description: "",
        startDate: null,
        endDate: null
    }
}

function saveExperience() {
    emit("update:modelValue", [...props.modelValue, { ...tempExperience.value }])
    tempExperience.value = createExperience()
    showModal.value = false
}

function editExperience(index: number) {
    tempExperience.value = { ...props.modelValue[index] }
    showModal.value = true
}

function removeExperience(index: number) {
    const updated = [...props.modelValue]
    updated.splice(index, 1)
    emit("update:modelValue", updated)
}

function formatDate(date: number | null) {
    if (!date) return ""
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
}
</script>

<template>
    <div class="w-full mb-4">

        <h5>Experiencia Laboral</h5>

        <n-space vertical class="w-full">
            <!-- Lista de experiencias -->
            <n-card v-for="(experience, index) in modelValue" :key="index" class="mb-2">
                <div class="flex justify-between">
                    <div>
                        <p class="font-semibold">{{ experience.company }}</p>
                        <p>{{ experience.position }}</p>
                        <p>
                            <span>
                                {{ formatDate(experience.startDate) }} -
                                {{ experience.endDate ? formatDate(experience.endDate) : "Actualidad" }}
                            </span>
                        </p>
                        <p class="mt-1 text-gray-500">{{ experience.description }}</p>
                    </div>
                    <n-button quaternary type="warning" size="small" @click="editExperience(index)">
                        <template #icon>
                            <Pencil />
                        </template>
                    </n-button>
                    <n-button quaternary type="error" size="small" @click="removeExperience(index)">
                        <template #icon>
                            <Trash />
                        </template>
                    </n-button>
                </div>
            </n-card>

            <!-- Botón para abrir modal -->
            <n-button type="primary" @click="showModal = true" ghost size="medium">
                <template #icon>
                    <Add />
                </template>
                Agregar experiencia
            </n-button>
        </n-space>
    </div>

    <!-- Modal de registro -->
    <n-modal v-model:show="showModal" preset="dialog" title="Agregar Experiencia Laboral">
        <n-form :model="tempExperience" label-placement="top">
            <n-form-item label="Empresa">
                <n-select v-model:value="tempExperience.company" :options="companyStore.options" filterable tag
                    :loading="companyStore.loading" :clearable="true" placeholder="Selecciona o escribe para buscar"
                    :on-search="companyStore.fetchOptions" :on-create="(label) => ({ label, value: label })" />
            </n-form-item>
            <n-form-item label="Cargo">
                <n-input v-model:value="tempExperience.position" />
            </n-form-item>
            <n-form-item label="Descripción">
                <n-input v-model:value="tempExperience.description" type="textarea" />
            </n-form-item>
            <n-form-item label="Fecha de inicio">
                <n-date-picker v-model:value="tempExperience.startDate" type="month" />
            </n-form-item>
            <n-form-item label="Fecha de finalización">
                <n-date-picker v-model:value="tempExperience.endDate" type="month" />
            </n-form-item>
        </n-form>

        <template #action>
            <n-space>
                <n-button @click="showModal = false">Cancelar</n-button>
                <n-button type="primary" @click="saveExperience">Guardar</n-button>
            </n-space>
        </template>
    </n-modal>
</template>
