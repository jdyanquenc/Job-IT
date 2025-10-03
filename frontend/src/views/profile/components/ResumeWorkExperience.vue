<script setup lang="ts">
import { ref } from "vue"
import { useCatalogueStore, useProfileStore } from "@/stores"
import { validate as isValidUUID } from 'uuid';
import {
    NForm, NFormItem, NInput, NDatePicker, NModal,
    NButton, NSpace, NCard, NSelect, NPopover
} from "naive-ui"

import { Add, Pencil, Trash } from "@vicons/ionicons5"
import type { WorkExperience } from "@/types"


const catalogueStore = useCatalogueStore()
const profileStore = useProfileStore()

const showModal = ref(false)
const tempExperience = ref<WorkExperience>(createExperience())


function createExperience(): WorkExperience {
    return {
        id: "",
        company_id: null,
        company_name: "",
        position: "",
        description: "",
        start_date: null,
        end_date: null
    }
}

function saveExperience() {
    if (!isValidUUID(tempExperience.value.company_id)) {
        tempExperience.value.company_name = tempExperience.value.company_id as string
        tempExperience.value.company_id = null
    }
    // If the experience has an ID, it's an edit; otherwise, it's a new entry
    if (!tempExperience.value.id) {
        profileStore.addWorkExperience(tempExperience.value)
    } else {
        profileStore.updateWorkExperience(tempExperience.value)
    }
    showModal.value = false
}

function newExperience() {
    tempExperience.value = createExperience()
    catalogueStore.fetchCompanies("")
    showModal.value = true
}

function editExperience(id: string) {
    tempExperience.value = { ...profileStore.profile.work_experiences.find(exp => exp.id === id) } as WorkExperience
    catalogueStore.fetchCompanies(tempExperience.value.company_name)
    showModal.value = true
}

function removeExperience(id: string) {
    profileStore.deleteWorkExperience(id)
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
            <n-card v-for="experience in profileStore.profile.work_experiences" :key="experience.id" class="mb-2">
                <div>
                    <p class="font-semibold">{{ experience.company_name }}</p>
                    <p>{{ experience.position }}</p>
                    <p>
                        <span>
                            {{ formatDate(experience.start_date) }} -
                            {{ experience.end_date ? formatDate(experience.end_date) : "Actualidad" }}
                        </span>
                    </p>
                </div>
                <div class="flex items-center justify-between">
                    <div>
                        <p class="mt-1 text-gray-500">{{ experience.description }}</p>
                    </div>
                    <div class="flex gap-2">
                        <n-popover trigger="hover">
                            <template #trigger>
                                <n-button quaternary type="warning" size="small" title="Editar"
                                    @click="editExperience(experience.id)">
                                    <template #icon>
                                        <Pencil />
                                    </template>
                                </n-button>
                            </template>
                            <span>Editar</span>
                        </n-popover>
                        <n-popover trigger="hover">
                            <template #trigger>
                                <n-button quaternary type="error" size="small" title="Eliminar"
                                    @click="removeExperience(experience.id)">
                                    <template #icon>
                                        <Trash />
                                    </template>
                                </n-button>
                            </template>
                            <span>Eliminar</span>
                        </n-popover>
                    </div>
                </div>
            </n-card>

            <!-- Botón para abrir modal -->
            <n-button type="primary" @click="newExperience()" ghost size="medium">
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
                <n-select v-model:value="tempExperience.company_id" :options="catalogueStore.companies" filterable tag
                    :loading="catalogueStore.loadingCompanies" :clearable="true"
                    placeholder="Selecciona o escribe para buscar" :on-search="catalogueStore.fetchCompanies"
                    :on-create="(label) => ({ label, value: label })" />
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

<style scoped>
.n-card {
    background-color: #fff;

}

.n-card:hover {
    background-color: #f7fafa;
}
</style>