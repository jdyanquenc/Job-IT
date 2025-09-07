<script setup>
import { ref, watch } from 'vue'
import { storeToRefs } from 'pinia';

import { useJobsStore } from '@/stores';
import { useLoadingBar } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'

import { NCard, NAvatar, NText, NDivider, NButton, NGrid, NGi, NIcon } from "naive-ui"
import {
    MapOutline, CallOutline, MailOutline, LocationOutline, TimeOutline, BriefcaseOutline,
    CashOutline, BusinessOutline, BarChartOutline, CalendarOutline, PersonOutline,
} from "@vicons/ionicons5"


const route = useRoute()
const router = useRouter()
const jobsStore = useJobsStore();
const loadingBar = useLoadingBar()

const id = route.params.id

const { job } = storeToRefs(jobsStore);

async function loadJobData() {
    loadingBar.start()
    try {
        await jobsStore.getById(id)
        loadingBar.finish()
    } catch (error) {
        loadingBar.error()
        router.push('/404')
    }
}

loadJobData()


watch(() => id, () => {
    loadJobData()
})



const employmentInfo = {
    industry: "Mechanical",
    jobLevel: "Experienced (Non - Manager)",
    location: "Dallas, Texas Remote Friendly",
}

const company = {
    name: "AliThemes",
    location: "New York, US",
    jobsOpen: 2,
    address: "205 North Michigan Avenue, Suite 810 Chicago, 60601, USA",
    phone: "(123) 456-7890",
    email: "contact@Evara.com",
    mapEmbed: "https://maps.google.com/maps?q=chicago%20michigan%20avenue&t=&z=13&ie=UTF8&iwloc=&output=embed"
}

const similarJobs = [
    {
        title: "UI / UX Designer fulltime",
        salary: "$250/Hour",
        type: "Fulltime",
        time: "3 mins ago",
        location: "New York, US",
        logo: "https://via.placeholder.com/40x40.png?text=UI"
    },
    {
        title: "Java Software Engineer",
        salary: "$500/Hour",
        type: "Fulltime",
        time: "5 mins ago",
        location: "Tokyo, Japan",
        logo: "https://via.placeholder.com/40x40.png?text=JS"
    }
]




</script>

<template>
    <div class="w-full">

        <div class="flex mt-4 ml-2">
            <h2 class="text-2xl font-bold mb-2">{{ job.job_title }}</h2>
        </div>

        <hr class="mt-2 mb-2" />

        <div class="flex flex-col lg:flex-row w-full gap-6">

            <!-- Main content -->
            <main class="p-2 flex-1 basis-3/4">

                <n-card class="mb-10" bordered>

                    <n-grid cols="1 640:2" x-gap="24" y-gap="16">
<!--
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BusinessOutline" />
                                <n-text strong>Industry:</n-text>
                                <n-text>{{ employmentInfo.industry }}</n-text>
                            </div>
                        </n-gi>
-->
<!--
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="PersonOutline" />
                                <n-text strong>Job level:</n-text>
                                <n-text>{{ employmentInfo.jobLevel }}</n-text>
                            </div>
                        </n-gi>
-->
                        <!-- Salary -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="CashOutline" />
                                <n-text strong>Salary:</n-text>
                                <n-text>{{ job.salary_range }}</n-text>
                            </div>
                        </n-gi>

                        <!-- Experience -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BarChartOutline" />
                                <n-text strong>Experience:</n-text>
                                <n-text>{{ job.experience }}</n-text>
                            </div>
                        </n-gi>

                        <!-- Job type -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="BriefcaseOutline" />
                                <n-text strong>Job type:</n-text>
                                <n-text>{{ job.employment_type }}</n-text>
                            </div>
                        </n-gi>

                        <!-- Deadline -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="CalendarOutline" />
                                <n-text strong>Deadline:</n-text>
                                <n-text>{{ new Date(job.expires_at).toLocaleDateString() }}</n-text>
                            </div>
                        </n-gi>

                        <!-- Updated -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="TimeOutline" />
                                <n-text strong>Updated:</n-text>
                                <n-text>{{ new Date(job.updated_at || job.created_at).toLocaleDateString() }}</n-text>
                            </div>
                        </n-gi>

                        <!-- Location -->
                        <n-gi>
                            <div class="flex items-center space-x-2">
                                <n-icon :component="LocationOutline" />
                                <n-text strong>Location:</n-text>
                                <n-text>{{ employmentInfo.location }}</n-text>
                            </div>
                        </n-gi>
                    </n-grid>
                </n-card>
                
                <article class="prose prose-gray">
                    <h2>Job Description</h2>
                    <p>
                        {{ job.job_description }}
                    </p>

                    <h3>Qualifications</h3>
                    <p>
                        {{ job.qualifications }}
                    </p>

                    <h3>Responsibilities</h3>
                    <p>
                        {{ job.responsibilities }}
                    </p>

                    <h3>Benefits</h3>
                    <p>
                        {{ job.benefits }}
                    </p>

                    <h3>Tags</h3>
                    <ul>
                        <li v-for="(skill, index) in job.skills_required" :key="index">{{ skill }}</li>
                    </ul>
                </article>

            </main>


            <!-- Sidebar -->

            <div class="p-2 basis-1/4">

                <n-card>
                    <div class="flex items-center space-x-3">
                        <n-avatar size="large" src="https://via.placeholder.com/80x80.png?text=Logo" />
                        <div>
                            <n-text strong>{{ company.name }}</n-text>
                            <div class="text-gray-500 text-sm flex items-center space-x-1">
                                <n-icon :component="LocationOutline" /> <span>{{ company.location }}</span>
                            </div>
                            <n-button quaternary size="small" type="primary">
                                {{ company.jobsOpen }} Open Jobs
                            </n-button>
                        </div>
                    </div>

                    <n-divider />

                    <!-- Map -->
                    <iframe :src="company.mapEmbed" class="w-full h-40 rounded-lg" style="border:0" allowfullscreen
                        loading="lazy"></iframe>

                    <n-divider />

                    <!-- Contact Info -->
                    <div class="space-y-3 text-sm">
                        <div class="flex items-center space-x-2">
                            <n-icon :component="LocationOutline" />
                            <span>{{ company.address }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <n-icon :component="CallOutline" />
                            <span>{{ company.phone }}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <n-icon :component="MailOutline" />
                            <span>{{ company.email }}</span>
                        </div>
                    </div>
                </n-card>

                <!-- Similar Jobs -->
                <n-card title="Similar jobs">
                    <div class="space-y-4">
                        <div v-for="(job, index) in similarJobs" :key="index" class="flex items-start space-x-3">
                            <n-avatar size="large" :src="job.logo" />
                            <div>
                                <n-text strong>{{ job.title }}</n-text>
                                <div class="flex items-center text-sm text-gray-500 space-x-2">
                                    <n-icon :component="BriefcaseOutline" /> <span>{{ job.type }}</span>
                                    <n-icon :component="TimeOutline" /> <span>{{ job.time }}</span>
                                    <n-icon :component="LocationOutline" /> <span>{{ job.location }}</span>
                                </div>
                                <div class="text-primary-500 font-semibold">{{ job.salary }}</div>
                            </div>
                        </div>
                    </div>
                </n-card>

            </div>

        </div>

    </div>
</template>