<script setup lang="ts">

import type {
    FormInst,
    FormRules,
    FormValidationError
} from 'naive-ui'


import { NButton, NCol, NSpin, NForm, NFormItem, NInput, NRow, NTimeline, NTimelineItem, useMessage } from 'naive-ui'
import { NText, NDivider, NGrid, NGi, NIcon } from "naive-ui"

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
    qualifications: '',
    responsibilities: '',
    experience: '',
    benefits: '',
    salary_range: '',
    remote: false,
    tags: [''],
    employment_type: 'Full-time',
    expires_at: new Date(new Date().setDate(new Date().getDate() + 30))
})


const rules: FormRules = {
    job_title: {
        required: true,
        message: 'Job title is required',
        trigger: 'blur'
    },
    job_description: {
        required: true,
        message: 'Job description is required',
        trigger: 'blur'
    },
    qualifications: {
        required: true,
        message: 'Qualifications are required',
        trigger: 'blur'
    },
    responsibilities: {
        required: !editMode.value,
        message: 'Responsibilities are required',
        trigger: 'blur'
    },
    experience: {
        required: true,
        message: 'Experience is required',
        trigger: 'blur'
    },
    benefits: {
        required: false
    },
    salary_range: {
        required: true,
        message: 'Salary range is required',
        trigger: 'blur'
    },
    skills_required: {
        type: 'array',
        required: true,
        message: 'At least one skill is required',
        trigger: 'blur'
    },
    employment_type: {
        type: 'enum',
        enum: ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship'] as EmploymentType[],
        required: true,
        message: 'Employment type is required',
        trigger: 'blur'
    },
    expires_at: {
        type: 'date',
        required: true,
        message: 'Expiration date is required',
        trigger: 'blur'
    }
};

if (id) {
    isLoading.value = true;
    loadJobData(id)
    editMode.value = true;
    model.value.job_title = job.value.job_title;
    model.value.job_description = job.value.job_description;
    model.value.qualifications = job.value.qualifications;
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
                message.error('Please fix the errors before submitting.')
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
            message.success('Job updated successfully');
        } else {
            // Register new job
            await jobsStore.register(registerJob);
            message.success('Job registered successfully');
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

/*

model.value.job_title = job.value.job_title;
model.value.job_description = job.value.job_description;
model.value.qualifications = job.value.qualifications;
model.value.responsibilities = job.value.responsibilities;
model.value.experience = job.value.experience;
model.value.benefits = job.value.benefits;
model.value.salary_range = job.value.salary_range;
model.value.remote = job.value.remote;
model.value.skills_required = job.value.skills_required;
model.value.employment_type = job.value.employment_type;
model.value.expires_at = job.value.expires_at;
isLoading.value = false;

*/


</script>

<template>

    <div class="w-full">

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 flex-1 basis-3/4">

                <n-form ref="formRef" :model="model" :rules="rules">
                    <n-form-item path="job_title" label="Title">
                        <n-input v-model:value="model.job_title" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="job_description" label="Description">
                        <n-input v-model:value="model.job_description" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="qualifications" label="Qualifications">
                        <n-input v-model:value="model.qualifications" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="responsibilities" label="Responsibilities">
                        <n-input v-model:value="model.responsibilities" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="experience" label="Experience">
                        <n-input v-model:value="model.experience" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="benefits" label="Benefits">
                        <n-input v-model:value="model.benefits" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-form-item path="salary_range" label="Salary range">
                        <n-input v-model:value="model.salary_range" type="textarea" @keydown.enter.prevent />
                    </n-form-item>

                    <n-row :gutter="[0, 24]">
                        <n-col :span="24">
                            <div style="display: flex; justify-content: flex-end">
                                <n-button type="primary" @click="handleValidateButtonClick" :disabled="isSubmitting">
                                    {{ editMode ? 'Update' : 'Register' }}
                                </n-button>
                                <n-button type="default" @click="handleCancelButtonClick" :disabled="isSubmitting">
                                    Cancel
                                </n-button>
                            </div>
                        </n-col>
                    </n-row>
                </n-form>


            </main>

            <!-- Sidebar -->

            <div class="p-2 basis-1/4">

                <n-timeline item-placement="right" size="large">
                    <n-timeline-item type="default" title="Title"  />
                    <n-timeline-item type="success" title="Description"/>
                    <n-timeline-item type="error"   title="Qualifications"/>
                    <n-timeline-item type="warning" title="Responsibilities"/>
                    <n-timeline-item type="info"    title="Experience" />
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