<script setup>

import { NMessageProvider } from 'naive-ui';

</script>

<template>
    <div class="p-4">
        <div class="container">
            <n-message-provider>
                <router-view />
            </n-message-provider>
        </div>
    </div>
</template>
