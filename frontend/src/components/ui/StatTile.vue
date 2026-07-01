<script setup>
import Icon from '../Icon.vue'

defineProps({
  label: String,
  value: { type: [Number, String], default: 0 },
  icon: { type: String, default: '' },
})
</script>

<template>
  <div class="stat-tile d-flex align-items-center justify-content-between motion-fade-up">
    <div>
      <div class="stat-value">{{ value }}</div>
      <div class="stat-label mt-1">{{ label }}</div>
    </div>
    <span v-if="icon" class="stat-ic"><Icon :name="icon" :size="26" /></span>
  </div>
</template>

<style scoped>
.stat-ic { color: var(--ppa-accent); opacity: 0.85; }
</style>
