<script setup lang="ts">
import {
    NTimeline, NTimelineItem
} from "naive-ui"

import ResumeDescription from "./components/ResumeDescription.vue"
import ResumeEducation from "./components/ResumeEducation.vue"
import ResumeWorkExperience from "./components/ResumeWorkExperience.vue"
import ResumeSkills from "./components/ResumeSkills.vue"
//import ResumeLanguages from "./components/ResumeLanguages.vue"
import ResumePreferences from "./components/ResumePreferences.vue"

import { useRoute } from "vue-router"
import { useProfileStore } from "@/stores"
import { watch } from "vue"
import { storeToRefs } from "pinia"

const route = useRoute()
const profileStore = useProfileStore()
const { profile } = storeToRefs(profileStore)

const id = route.params.id


watch(() => id, () => {
    profileStore.load(id as string)
})

profileStore.load(id as string)

</script>

<template>

    <div class="w-full">

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 flex-1 basis-3/4">

                <h2 class="text-2xl mb-2"> {{ profile.full_name }} </h2>

                <hr class="mt-2 mb-4" />

                <resume-description />

                <resume-education />

                <resume-work-experience />

                <resume-preferences />

                <resume-skills />

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