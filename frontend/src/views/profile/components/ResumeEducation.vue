<script setup lang="ts">
import { ref } from "vue"
import { useCatalogueStore, useProfileStore } from "@/stores"
import { validate as isValidUUID } from 'uuid';
import {
    NForm, NFormItem, NInput, NDatePicker, NModal,
    NButton, NSpace, NCard, NSelect
} from "naive-ui"

import { Add, Pencil, Trash } from "@vicons/ionicons5"
import type { EducationExperience } from "@/types";


const catalogueStore = useCatalogueStore()
const profileStore = useProfileStore()

const showModal = ref(false)
const tempEducation = ref(<EducationExperience>(createEducation()))


const degree_options = [
    { label: 'Bachillerato', value: 'HighSchool' },
    { label: 'Técnico', value: 'Associate' },
    { label: 'Pregrado', value: 'Bachelor' },
    { label: 'Especialización', value: 'Specialization' },
    { label: 'Maestría', value: 'Master' },
    { label: 'Doctorado', value: 'Doctorate' },
    { label: 'Otro', value: 'Other' },
]

function createEducation(): EducationExperience {
    return {
        id: "",
        institution_id: null,
        institution_name: "",
        degree: "",
        field_of_study: "",
        start_date: null,
        end_date: null
    }
}

function saveEducation() {
    if (!isValidUUID(tempEducation.value.institution_id)) {
        tempEducation.value.institution_name = tempEducation.value.institution_id as string
        tempEducation.value.institution_id = null
    }
    if (!tempEducation.value.id) {
        profileStore.addEducation(tempEducation.value)
    } else {
        profileStore.updateEducation(tempEducation.value)
    }
    showModal.value = false
}

function newEducation() {
    tempEducation.value = createEducation()
    catalogueStore.fetchInstitutions("")
    showModal.value = true
}

function editEducation(id: string) {
    tempEducation.value = { ...profileStore.profileData.education_experiences.find(education => education.id === id) } as EducationExperience
    catalogueStore.fetchInstitutions(tempEducation.value.institution_name)
    showModal.value = true
}

function removeEducation(id: string) {
    profileStore.deleteEducation(id)
}

function formatDate(date: number | null) {
    if (!date) return ""
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
}

function translateDegree(degree: string) {
    const option = degree_options.find(opt => opt.value === degree)
    return option ? option.label : degree
}

</script>


<template>

    <div class="w-full mb-4">

        <h5>Educación</h5>

        <n-space vertical class="w-full">
            <!-- Lista de estudios guardados -->
            <n-card v-for="education in profileStore.profileData.education_experiences" :key="education.id"
                class="mb-2">
                <div>
                    <p class="font-semibold">{{ education.institution_name }}</p>
                    <p class="mt-1 text-gray-500">{{ translateDegree(education.degree) }} - {{
                        education.field_of_study }}</p>

                </div>
                <div class="flex items-center justify-between">
                    <div>
                        <p>
                            <span>
                                {{ formatDate(education.start_date) }} -
                                {{ education.end_date ? formatDate(education.end_date) : "Actualidad" }}
                            </span>
                        </p>
                    </div>
                    <div class="flex gap-2">
                        <n-button quaternary type="warning" size="small" title="Editar"
                            @click="editEducation(education.id)">
                            <template #icon>
                                <Pencil />
                            </template>
                        </n-button>
                        <n-button quaternary type="error" size="small" title="Eliminar"
                            @click="removeEducation(education.id)">
                            <template #icon>
                                <Trash />
                            </template>
                        </n-button>
                    </div>
                </div>
            </n-card>

            <!-- Botón para abrir modal -->
            <n-button type="primary" @click="newEducation()" ghost size="medium">
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
                <n-select v-model:value="tempEducation.institution_id" :options="catalogueStore.institutions" filterable
                    tag :loading="catalogueStore.loadingInstitutions" :clearable="true"
                    placeholder="Selecciona o escribe para buscar" :on-search="catalogueStore.fetchInstitutions"
                    :on-create="(label) => ({ label, value: label })" />
            </n-form-item>
            <n-form-item label="Título o grado">
                <n-select v-model:value="tempEducation.degree" :options="degree_options"
                    placeholder="Selecciona el título o grado" />
            </n-form-item>
            <n-form-item label="Programa">
                <n-input v-model:value="tempEducation.field_of_study" />
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

<style scoped>
.n-card {
    background-color: #fff;

}

.n-card:hover {
    background-color: #f7fafa;
}
</style>