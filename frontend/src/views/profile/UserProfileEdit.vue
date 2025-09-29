<script setup lang="ts">
import { ref } from "vue"
import {
    NButton
} from "naive-ui"

import ResumeDescription from "./components/ResumeDescription.vue"
import ResumeEducation from "./components/ResumeEducation.vue"
import ResumeWorkExperience from "./components/ResumeWorkExperience.vue"
import ResumeSkills from "./components/ResumeSkills.vue"
//import ResumeLanguages from "./components/ResumeLanguages.vue"
import ResumePreferences from "./components/ResumePreferences.vue"

const form = ref({
    description: "",
    education: [],
    work_experience: [],
    skills: [],
    languages: [],
    preferences: {
        salary_range: null,
        job_type: null,
        location: ""
    }
})

function handleSubmit() {
    console.log("CV data:", form.value)
    // Aquí envías los datos a tu API
}
</script>

<template>

    <div class="w-full">

        <div class="flex mt-4 ml-2">
            <h2 class="text-2xl font-bold mb-2">Registro de Curriculum</h2>

        </div>

        <hr class="mt-2 mb-8" />

        <resume-description v-model="form.description" />

        <resume-education v-model="form.education" />

        <resume-work-experience v-model="form.work_experience" />

        <resume-preferences v-model="form.preferences" />

        <resume-skills v-model="form.skills" />

        <div class="mt-6 flex justify-center">
            <n-button type="primary" @click="handleSubmit">Guardar CV</n-button>
        </div>

    </div>

</template>
