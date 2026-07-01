<script setup>
import { ui, dismissToast } from '../../store/ui'
</script>

<template>
  <div class="toast-host">
    <transition-group name="toast">
      <div
        v-for="t in ui.toasts" :key="t.id"
        class="toast-item" :class="`toast-${t.type}`"
        role="status" @click="dismissToast(t.id)"
      >
        {{ t.message }}
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-host {
  position: fixed; right: 1rem; bottom: 1rem; z-index: 1080;
  display: flex; flex-direction: column; gap: 0.5rem; max-width: min(360px, 90vw);
}
.toast-item {
  padding: 0.7rem 0.9rem; border-radius: 0.6rem; color: #fff; font-size: 0.9rem;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18); cursor: pointer; background: #14110f;
}
.toast-success { background: #1f6b3a; }
.toast-danger { background: #b0432b; }
.toast-info { background: #3a6f8f; }
.toast-enter-active, .toast-leave-active { transition: all 0.25s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(8px); }
</style>
