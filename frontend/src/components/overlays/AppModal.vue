<script setup>
// Vue-controlled modal (no Bootstrap JS). Teleported to body, closes on
// backdrop click or the close button.
defineProps({ modelValue: Boolean, title: String, size: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])
const close = () => emit('update:modelValue', false)
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="ppa-backdrop" @click.self="close">
        <div class="ppa-modal surface-card motion-fade-up" :class="size">
          <div class="d-flex justify-content-between align-items-center p-3 border-bottom">
            <h2 class="h5 mb-0">{{ title }}</h2>
            <button class="btn-close" aria-label="Close" @click="close"></button>
          </div>
          <div class="ppa-modal-body p-3"><slot /></div>
          <div v-if="$slots.footer" class="p-3 border-top d-flex justify-content-end gap-2">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.ppa-backdrop {
  position: fixed; inset: 0; background: rgba(20, 17, 15, 0.5);
  display: grid; place-items: center; z-index: 1090; padding: 1rem;
}
.ppa-modal { background: var(--ppa-surface); width: 100%; max-width: 520px; max-height: 90vh; display: flex; flex-direction: column; }
.ppa-modal.lg { max-width: 760px; }
.ppa-modal-body { overflow: auto; }
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
