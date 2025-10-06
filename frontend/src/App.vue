<script setup lang="ts">

import { NMessageProvider, NLoadingBarProvider, NConfigProvider, NDialogProvider, NBackTop, esAR } from 'naive-ui';
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
import { setLoadingBar, setMessageProvider } from '@/helpers'

const loadingBarProvider = ref(null)
const messageProvider = ref(null)

onMounted(() => {
  if (loadingBarProvider.value) {
    setLoadingBar(loadingBarProvider.value)
  }
  if (messageProvider.value) {
    setMessageProvider(messageProvider.value)
  }
})

</script>

<template>
  <n-config-provider :locale="customLocale">
    <n-loading-bar-provider ref="loadingBarProvider">
      <n-dialog-provider>
        <n-message-provider ref="messageProvider">
          <div>
            <header>
              <Navbar />
            </header>
            <main>
              <div class="max-w-screen-xl mx-auto mt-5 mb-5">
                <div class="flex justify-between items-center main-container">
                  <RouterView />
                </div>
              </div>
            </main>
            <footer>
              <FooterPanel />
            </footer>
          </div>
        </n-message-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
    <n-back-top :right="100" />
  </n-config-provider>
</template>
