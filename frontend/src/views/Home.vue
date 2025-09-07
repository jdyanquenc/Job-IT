<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore } from '@/stores';
import JobList from '@/views/jobs/JobList.vue';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
</script>

<template>
    <JobList />
</template>
