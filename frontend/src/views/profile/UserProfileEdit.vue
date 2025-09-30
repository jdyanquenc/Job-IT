<script setup lang="ts">
import { ref } from "vue"
import {
    NButton, NTimeline, NTimelineItem
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
/*
function handleSubmit() {
    console.log("CV data:", form.value)
    // Aquí envías los datos a tu API
}
*/
function handleBack() {
    window.history.back()
}

</script>

<template>

    <div class="w-full">

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 flex-1 basis-3/4">

                <h2 class="text-2xl mb-2">Jesus Yanquen</h2>

                <hr class="mt-2 mb-4" />

                <resume-description v-model="form.description" />

                <resume-education v-model="form.education" />

                <resume-work-experience v-model="form.work_experience" />

                <resume-preferences v-model="form.preferences" />

                <resume-skills v-model="form.skills" />


                <div class="mt-6 flex justify-center">
                    <n-button type="default" @click="handleBack()">Volver</n-button>
                </div>

            </main>

            <!-- Sidebar -->

            <div class="p-2 basis-1/4">

                <n-timeline item-placement="right" size="large">
                    <n-timeline-item type="default" title="Perfil profesional" />
                    <n-timeline-item type="success" title="Educación" />
                    <n-timeline-item type="error" title="Experiencia Laboral" />
                    <n-timeline-item type="warning" title="Preferencias" />
                    <n-timeline-item type="info" title="Habilidades" />
                </n-timeline>

            </div>

        </div>
    </div>

</template>

<style scoped>
.n-timeline .n-timeline-item {
    height: 100px;
}
</style>