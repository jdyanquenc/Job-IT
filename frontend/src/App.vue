<script setup lang="ts">

import { NMessageProvider } from 'naive-ui';
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue';
import FooterPanel from '@/components/FooterPanel.vue';

</script>

<template>
  <div>
    <header>
      <Navbar />
    </header>
    <main>
      <div class="max-w-screen-xl mx-auto mt-5 mb-5">
        <div class="flex justify-between items-center">
          <n-message-provider>
            <RouterView />
          </n-message-provider>
        </div>
      </div>
    </main>
    <footer>
      <FooterPanel />
    </footer>
  </div>
</template>
