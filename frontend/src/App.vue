<script setup lang="ts">

import { NMessageProvider, NLoadingBarProvider, NConfigProvider, NBackTop, esAR } from 'naive-ui';
import { RouterView } from 'vue-router'
import Navbar from '@/components/NavBar.vue';
import FooterPanel from '@/components/FooterPanel.vue';

const customLocale = {
  ...esAR, // heredas de español
  DatePicker: {
    ...esAR.DatePicker,
    confirm: 'Aceptar',
    clear: 'Borrar',
    now: 'Ahora',
    today: 'Hoy'
  }
}

import { onMounted, ref } from 'vue'
import { setLoadingBar } from '@/helpers/loading-bar'

const loadingBarProvider = ref(null)

onMounted(() => {
  if (loadingBarProvider.value) {
    setLoadingBar(loadingBarProvider.value)
  }
})

</script>

<template>
  <n-config-provider :locale="customLocale">
    <n-loading-bar-provider ref="loadingBarProvider">
      <div>
        <header>
          <Navbar />
        </header>
        <main>
          <div class="max-w-screen-xl mx-auto mt-5 mb-5">
            <div class="flex justify-between items-center main-container">
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
    </n-loading-bar-provider>
    <n-back-top :right="100" />
  </n-config-provider>
</template>
