<script setup>
import { RouterView } from 'vue-router'
import DitherDefs from './components/media/DitherDefs.vue'
import ToastHost from './components/ui/ToastHost.vue'
</script>

<template>
  <DitherDefs />
  <RouterView v-slot="{ Component }">
    <Transition name="page" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>
  <ToastHost />
</template>
