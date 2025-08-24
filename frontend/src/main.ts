import './assets/main.css'
import 'vfonts/Lato.css'
import 'vfonts/FiraCode.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { router } from './router'
import App from './App.vue'

// setup fake backend
import { fakeBackend } from './helpers'
fakeBackend()

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
