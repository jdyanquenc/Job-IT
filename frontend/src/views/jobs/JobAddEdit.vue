<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'


import { NButton, NCol, NForm, NFormItem, NInput, NSelect, NDynamicTags, NRow, NTimeline, NTimelineItem, useMessage } from 'naive-ui'

import {
    MapOutline, CallOutline, MailOutline, LocationOutline, TimeOutline, BriefcaseOutline,
    CashOutline, BusinessOutline, BarChartOutline, CalendarOutline, PersonOutline,
} from "@vicons/ionicons5"


import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia';
import type { RegisterJob, EmploymentType } from '@/types';

import { useJobsStore } from '@/stores';
import { useLoadingBar } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'


const route = useRoute()
const router = useRouter()
const message = useMessage();
const loadingBar = useLoadingBar()
const jobsStore = useJobsStore();

const { job } = storeToRefs(jobsStore);

const editMode = ref(false);
const isLoading = ref(false)
const isSubmitting = ref(false)

const id = route.params.id as string | undefined;

const formRef = ref<FormInst | null>(null)

const model = ref<RegisterJob>({
    job_title: '',
    job_description: '',
    skills: '',
    responsibilities: '',
    experience: '',
    benefits: '',
    salary_range: '',
    location: '',
    country_code: '',
    remote: false,
    tags: [],
    employment_type: 'Full-time',
    expires_at: new Date(new Date().setDate(new Date().getDate() + 30))
})

const experience_options = [
    { label: 'Sin experiencia', value: 'No experience' },
    { label: '1 año', value: '1 year' },
    { label: '2 años', value: '2 years' },
    { label: '3 años', value: '3 years' },
    { label: '4 años', value: '4 years' },
    { label: '5 años', value: '5 years' },
    { label: '6 años', value: '6 years' },
    { label: '7 años', value: '7 years' },
    { label: '8 años', value: '8 years' },
    { label: '9 años', value: '9 years' },
    { label: '10+ años', value: '10+ years' }
]

const salary_range_options = [
    { label: 'Menos de $20,000', value: 'Less than $20,000' },
    { label: '$20,000 - $40,000', value: '$20,000 - $40,000' },
    { label: '$40,000 - $60,000', value: '$40,000 - $60,000' },
    { label: '$60,000 - $80,000', value: '$60,000 - $80,000' },
    { label: '$80,000 - $100,000', value: '$80,000 - $100,000' },
    { label: 'Más de $100,000', value: 'More than $100,000' }
]

const countries = [
    { label: 'United States', value: 'US' },
    { label: 'Canada', value: 'CA' },
    { label: 'United Kingdom', value: 'UK' },
    { label: 'Australia', value: 'AU' },
    { label: 'Germany', value: 'DE' },
    { label: 'France', value: 'FR' },
    { label: 'Spain', value: 'ES' },
    { label: 'Italy', value: 'IT' },
    { label: 'Mexico', value: 'MX' },
    { label: 'Brazil', value: 'BR' },
    { label: 'Argentina', value: 'AR' },
    { label: 'Colombia', value: 'CO' },
    { label: 'Chile', value: 'CL' },
    { label: 'Peru', value: 'PE' },
    { label: 'Venezuela', value: 'VE' },
    { label: 'Other', value: 'OT' }
]



const rules: FormRules = {
    job_title: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    job_description: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    responsibilities: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    skills: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    experience: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    benefits: {
        required: false
    },
    salary_range: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    tags: {
        type: 'array',
        required: true,
        message: 'Debe ingresar al menos una etiqueta',
        trigger: 'blur'
    },
    employment_type: {
        type: 'enum',
        enum: ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship'] as EmploymentType[],
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    expires_at: {
        type: 'date',
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    location: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    },
    country_code: {
        required: true,
        message: 'Este campo es requerido',
        trigger: 'blur'
    }
};

if (id) {
    isLoading.value = true;
    loadJobData(id)
    editMode.value = true;
    model.value.job_title = job.value.job_title;
    model.value.job_description = job.value.job_description;
    model.value.skills = job.value.skills;
    model.value.responsibilities = job.value.responsibilities;
    model.value.experience = job.value.experience;
    model.value.benefits = job.value.benefits;
    model.value.salary_range = job.value.salary_range;
    model.value.remote = job.value.remote;
    model.value.tags = job.value.tags;
    model.value.employment_type = job.value.employment_type;
    model.value.expires_at = job.value.expires_at;
    isLoading.value = false;
}

async function loadJobData(id: string) {
    loadingBar.start()
    try {
        await jobsStore.getById(id)
        loadingBar.finish()
    } catch (error) {
        isLoading.value = false;
        loadingBar.error()
        router.push('/company-jobs')
        message.error('Cannot load job data');
    }
}

watch(() => id, () => {
    loadJobData(id as string)
})


function handleValidateButtonClick(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate(
        (errors: Array<FormValidationError> | undefined) => {
            if (!errors) {
                onSubmit()
            }
            else {
                message.error('Verifica los campos en rojo y vuelve a intentarlo.');
            }
        }
    )
}

function handleCancelButtonClick(e: MouseEvent) {
    e.preventDefault()
    router.push('/company-jobs')
}

async function onSubmit() {
    const jobsStore = useJobsStore();
    const registerJob: RegisterJob = model.value;

    try {
        isSubmitting.value = true;
        if (editMode.value && id) {
            // Update existing job
            await jobsStore.update(id, registerJob);
            message.success('Oferta actualizada exitosamente');
        } else {
            // Register new job
            await jobsStore.register(registerJob);
            message.success('Oferta registrada exitosamente');
        }
        await router.push('/company-jobs');
    }
    catch (error: any) {
        console.error('Registration failed:', error);
    }
    finally {
        isSubmitting.value = false;
    }
}

</script>

<template>

    <div class="w-full">

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 flex-1 basis-3/4">

                <n-form ref="formRef" :model="model" :rules="rules">
                    <n-form-item path="job_title" label="Título">
                        <n-input v-model:value="model.job_title" placeholder="Título de la oferta" />
                    </n-form-item>

                    <n-form-item path="job_description" label="Descripción">
                        <n-input v-model:value="model.job_description" type="textarea"
                            placeholder="Ingresa una descripción para la oferta" />
                    </n-form-item>

                    <n-form-item path="responsibilities" label="Responsabilidades">
                        <n-input v-model:value="model.responsibilities" type="textarea"
                            placeholder="Indica las responsabilidades del cargo" />
                    </n-form-item>

                    <n-form-item path="skills" label="Habilidades">
                        <n-input v-model:value="model.skills" type="textarea"
                            placeholder="Ingresa las habilidades requeridas" />
                    </n-form-item>

                    <n-form-item path="benefits" label="Beneficios">
                        <n-input v-model:value="model.benefits" type="textarea"
                            placeholder="Indica los beneficios que ofrece la empresa" />
                    </n-form-item>

                    <n-form-item path="experience" label="Experiencia">
                        <n-select v-model:value="model.experience" :options="experience_options"
                            placeholder="Selecciona la experiencia requerida" />
                    </n-form-item>

                    <n-form-item path="salary_range" label="Rango salarial">
                        <n-select v-model:value="model.salary_range" :options="salary_range_options"
                            placeholder="Selecciona el rango salarial" />
                    </n-form-item>

                    <n-form-item path="country_code" label="País">
                        <n-select v-model:value="model.country_code" :options="countries"
                            placeholder="Selecciona el país" />
                    </n-form-item>

                    <n-form-item path="location" label="Lugar">
                        <n-input v-model:value="model.location" placeholder="Ciudad o lugar de trabajo" />
                    </n-form-item>

                    <n-form-item path="tags" label="Etiquetas">
                        <n-dynamic-tags v-model:value="model.tags" />
                    </n-form-item>

                    <n-row :gutter="[0, 24]">
                        <n-col :span="24">
                            <div style="display: flex; justify-content: flex-end">
                                <n-button type="primary" @click="handleValidateButtonClick" :disabled="isSubmitting">
                                    {{ editMode ? 'Actualizar Oferta' : 'Registrar Oferta' }}
                                </n-button>
                                &nbsp;&nbsp;
                                <n-button type="default" @click="handleCancelButtonClick" :disabled="isSubmitting">
                                    Cancelar
                                </n-button>
                            </div>
                        </n-col>
                    </n-row>
                </n-form>


            </main>

            <!-- Sidebar -->

            <div class="p-2 basis-1/4">

                <n-timeline item-placement="right" size="large">
                    <n-timeline-item type="default" title="Titulo" />
                    <n-timeline-item type="success" title="Descripción" />
                    <n-timeline-item type="error" title="Habilidades" />
                    <n-timeline-item type="warning" title="Responsabilidades" />
                    <n-timeline-item type="info" title="Experiencia" />
                </n-timeline>

            </div>

        </div>
    </div>

</template>

<style scoped>
.n-timeline .n-timeline-item {
    height: 70px;
}
</style>