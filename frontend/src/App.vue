<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores';
import { NButton } from 'naive-ui';

const authStore = useAuthStore();

</script>

<template>
  <div>
    <header class="header sticky-bar">
      <div class="container">
        <div class="main-header">
          <div class="header-left">
            <div class="header-logo">
              <a href="/"><span class="d-flex"><img alt="job IT" src="/images/template/jobit-logo.svg"></span></a>
            </div>
          </div>
          <div class="header-nav">
            <nav class="nav-main-menu">
              <RouterLink to="/">Home</RouterLink>
              <RouterLink to="/users">Users</RouterLink>
              <RouterLink to="/jobs">Jobs</RouterLink>
            </nav>
            <div class="burger-icon burger-icon-white "><span class="burger-icon-top"></span><span
                class="burger-icon-mid"></span><span class="burger-icon-bottom"></span></div>
          </div>
          <div class="header-right">
            <div class="block-signin">
              <n-button @click="authStore.logout()">Logout</n-button>
            </div>
          </div>
        </div>
      </div>
    </header>
    <main class="main">
      <RouterView />
    </main>
    <footer class="footer mt-50">
      <div class="container">
        <div class="footer-bottom mt-50">
          <div class="row">
            <div class="col-md-6">
              <span class="font-xs color-text-paragraph">Copyright © 2025. Job IT. Todos los derechos reservados</span>
            </div>
            <div class="col-md-6 text-md-end text-start">
              <div class="footer-social">
                <a class="font-xs color-text-paragraph" href="#">Política de privacidad</a>
                <a class="font-xs color-text-paragraph mr-30 ml-30" href="#">Términos &amp; Condiciones</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
