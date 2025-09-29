<script setup lang="ts">
import { ref } from "vue"
import {
    NForm, NFormItem, NInput, NDatePicker, NModal,
    NButton, NSpace, NCard
} from "naive-ui"

import { Add } from "@vicons/ionicons5"

const props = defineProps({
    modelValue: { type: Array, required: true }
})
const emit = defineEmits(["update:modelValue"])

const showModal = ref(false)
const tempExperience = ref(createExperience())

function createExperience() {
    return {
        company: "",
        position: "",
        description: "",
        start_date: null,
        end_date: null
    }
}

function saveExperience() {
    emit("update:modelValue", [...props.modelValue, { ...tempExperience.value }])
    tempExperience.value = createExperience()
    showModal.value = false
}

function removeExperience(index: number) {
    const updated = [...props.modelValue]
    updated.splice(index, 1)
    emit("update:modelValue", updated)
}

function formatDate(date: string | null) {
    if (!date) return ""
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
}
</script>

<template>
    <div class="w-full mb-4">
        <span class="font-medium mb-2">Experiencia Laboral</span>

        <n-space vertical class="w-full">
            <!-- Lista de experiencias -->
            <n-card v-for="(experience, index) in modelValue" :key="index" class="mb-2">
                <div class="flex justify-between">
                    <div>
                        <p class="font-semibold">{{ experience.company }}</p>
                        <p>{{ experience.position }}</p>
                        <small>
                            {{ formatDate(experience.start_date) }} -
                            {{ experience.end_date ? formatDate(experience.end_date) : "Actualidad" }}
                        </small>
                        <p class="mt-1 text-gray-500">{{ experience.description }}</p>
                    </div>
                    <n-button quaternary type="error" size="small" @click="removeExperience(index)">
                        Eliminar
                    </n-button>
                </div>
            </n-card>

            <!-- Botón para abrir modal -->
            <n-button type="primary" @click="showModal = true" ghost>
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
                <n-input v-model:value="tempExperience.company" />
            </n-form-item>
            <n-form-item label="Cargo">
                <n-input v-model:value="tempExperience.position" />
            </n-form-item>
            <n-form-item label="Descripción">
                <n-input v-model:value="tempExperience.description" type="textarea" />
            </n-form-item>
            <n-form-item label="Fecha de inicio">
                <n-date-picker v-model:value="tempExperience.start_date" type="month" />
            </n-form-item>
            <n-form-item label="Fecha de finalización">
                <n-date-picker v-model:value="tempExperience.end_date" type="month" />
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
