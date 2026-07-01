<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'

import AppSidebar from './AppSidebar.vue'
import AppNavbar from './AppNavbar.vue'

const sidebarOpen = ref(false)
</script>

<template>
  <div class="app-shell">
    <AppSidebar :open="sidebarOpen" @close="sidebarOpen = false" />
    <div v-if="sidebarOpen" class="sidebar-backdrop d-lg-none" @click="sidebarOpen = false"></div>

    <div class="app-main">
      <AppNavbar @toggle="sidebarOpen = !sidebarOpen" />
      <main class="app-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
