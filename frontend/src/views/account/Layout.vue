<script setup>
import { useAuthStore } from '@/stores';
import { router } from '@/router';

import { NMessageProvider } from 'naive-ui';

// redirect home if already logged in
const authStore = useAuthStore();
if (authStore.user) {
    router.push('/');
}
</script>

<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-8 offset-sm-2 mt-5">
                <n-message-provider>
                    <router-view />
                </n-message-provider>
            </div>
        </div>
    </div>
</template>
