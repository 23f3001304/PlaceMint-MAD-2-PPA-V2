<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { authState, logout } from '../../store/auth'
import { navFor } from '../../router/nav'
import BrandMark from '../BrandMark.vue'
import Icon from '../Icon.vue'

defineProps({ open: Boolean })
const emit = defineEmits(['close'])

const router = useRouter()
const links = computed(() => navFor(authState.user?.role))

function signOut() {
  logout()
  router.push('/login')
}
</script>

<template>
  <aside class="app-sidebar" :class="{ 'is-open': open }">
    <div class="px-2 mb-4 mt-1">
      <BrandMark :icon="false" class="text-white" />
    </div>

    <nav class="d-flex flex-column gap-1 flex-grow-1">
      <RouterLink
        v-for="l in links" :key="l.to" :to="l.to" class="side-link"
        exact-active-class="router-link-active" @click="emit('close')"
      >
        <Icon :name="l.icon" :size="18" /><span>{{ l.label }}</span>
      </RouterLink>
    </nav>

    <button class="side-link border-0 bg-transparent w-100 text-start" @click="signOut">
      <Icon name="logout" :size="18" /><span>Sign out</span>
    </button>
  </aside>
</template>
