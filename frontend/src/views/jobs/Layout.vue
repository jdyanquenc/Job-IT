<script setup>

import { NMessageProvider } from 'naive-ui';

</script>

<template>
    <div class="container">
        <n-message-provider>
            <router-view />
        </n-message-provider>
    </div>
</template>
