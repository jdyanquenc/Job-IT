<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore } from '@/stores';
import List from '@/views/jobs/List.vue';

const authStore = useAuthStore();
const { user } = storeToRefs(authStore);
</script>

<template>

    <div class="container">
        <List />
    </div>

</template>
