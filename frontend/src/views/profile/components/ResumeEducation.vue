<script setup lang="ts">
import { ref } from "vue"
import {
    NForm, NFormItem, NInput, NDatePicker, NModal,
    NButton, NSpace, NCard
} from "naive-ui"

import { Add } from "@vicons/ionicons5"


export interface Education {
    institution: string
    degree: string
    start_date: string | null
    end_date: string | null
}

const props = defineProps({
    modelValue: { type: Array<Education>, required: true }
})
const emit = defineEmits(["update:modelValue"])

const showModal = ref(false)
const tempEducation = ref(createEducation())

function createEducation() {
    return {
        institution: "",
        degree: "",
        start_date: null,
        end_date: null
    }
}

function saveEducation() {
    emit("update:modelValue", [...props.modelValue, { ...tempEducation.value }])
    tempEducation.value = createEducation()
    showModal.value = false
}

function removeEducation(index: number) {
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
        <h5>Educación</h5>


        <n-space vertical class="w-full">
            <!-- Lista de estudios guardados -->
            <n-card v-for="(education, index) in modelValue" :key="index" class="mb-2">
                <div class="flex justify-between">
                    <div>
                        <p class="font-semibold">{{ education.institution }}</p>
                        <p>{{ education.degree }}</p>
                        <small>
                            {{ formatDate(education.start_date) }} -
                            {{ education.end_date ? formatDate(education.end_date) : "Actualidad" }}
                        </small>
                    </div>
                    <n-button quaternary type="error" size="small" @click="removeEducation(index)">
                        Eliminar
                    </n-button>
                </div>
            </n-card>

            <!-- Botón para abrir modal -->
            <n-button type="primary" @click="showModal = true" ghost size="medium">
                <template #icon>
                    <Add />
                </template>
                Agregar estudio
            </n-button>
        </n-space>

    </div>


    <!-- Modal de registro -->
    <n-modal v-model:show="showModal" preset="dialog" title="Agregar Estudio">
        <n-form :model="tempEducation" label-placement="top">
            <n-form-item label="Institución">
                <n-input v-model:value="tempEducation.institution" />
            </n-form-item>
            <n-form-item label="Título o grado">
                <n-input v-model:value="tempEducation.degree" />
            </n-form-item>
            <n-form-item label="Fecha de inicio">
                <n-date-picker v-model:value="tempEducation.start_date" type="month" />
            </n-form-item>
            <n-form-item label="Fecha de finalización">
                <n-date-picker v-model:value="tempEducation.end_date" type="month" />
            </n-form-item>
        </n-form>

        <template #action>
            <n-space>
                <n-button @click="showModal = false">Cancelar</n-button>
                <n-button type="primary" @click="saveEducation">Guardar</n-button>
            </n-space>
        </template>
    </n-modal>
</template>
