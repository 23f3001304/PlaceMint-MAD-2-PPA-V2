<script setup>
import { computed } from 'vue'

import { authState } from '../../store/auth'
import Icon from '../Icon.vue'

defineEmits(['toggle'])

const displayName = computed(
  () => authState.profile?.name || authState.profile?.company_name || authState.user?.email || 'Account',
)
const roleLabel = computed(() => (authState.user?.role || '').toUpperCase())
</script>

<template>
  <header class="app-navbar d-flex align-items-center justify-content-between">
    <button class="btn btn-sm d-lg-none nav-toggle" aria-label="Open menu" @click="$emit('toggle')">
      <Icon name="dashboard" :size="20" />
    </button>
    <div class="flex-grow-1"></div>
    <div class="d-flex align-items-center gap-2">
      <span class="text-muted small d-none d-sm-inline text-mono">{{ roleLabel }}</span>
      <span class="avatar">{{ (displayName[0] || 'U').toUpperCase() }}</span>
      <span class="fw-semibold small d-none d-md-inline">{{ displayName }}</span>
    </div>
  </header>
</template>

<style scoped>
.app-navbar {
  height: 60px; padding: 0 clamp(1rem, 3vw, 2.5rem); background: var(--ppa-bg);
  border-bottom: 1px solid var(--ppa-border); position: sticky; top: 0; z-index: 1020;
}
.avatar {
  width: 32px; height: 32px; border-radius: 50%; background: var(--ppa-accent); color: #fff;
  display: grid; place-items: center; font-weight: 700; font-size: 0.85rem;
}
.nav-toggle { border: 1px solid var(--ppa-border); }
</style>
