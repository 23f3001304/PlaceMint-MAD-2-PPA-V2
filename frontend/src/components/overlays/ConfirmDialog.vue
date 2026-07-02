<script setup>
import AppModal from './AppModal.vue'

defineProps({
  modelValue: Boolean,
  title: { type: String, default: 'Are you sure?' },
  message: String,
  confirmLabel: { type: String, default: 'Confirm' },
  danger: Boolean,
})
const emit = defineEmits(['update:modelValue', 'confirm'])

function accept() {
  emit('confirm')
  emit('update:modelValue', false)
}
</script>

<template>
  <AppModal :model-value="modelValue" :title="title" @update:model-value="emit('update:modelValue', $event)">
    <p class="mb-0 text-muted">{{ message }}</p>
    <template #footer>
      <button class="btn btn-outline-secondary" @click="emit('update:modelValue', false)">Cancel</button>
      <button class="btn" :class="danger ? 'btn-danger' : 'btn-3d-accent'" @click="accept">{{ confirmLabel }}</button>
    </template>
  </AppModal>
</template>
