<script setup>
defineProps({ title: String, subtitle: String })
</script>

<template>
  <div class="d-flex flex-wrap justify-content-between align-items-end gap-2 mb-4">
    <div>
      <h1 class="h3 mb-1">{{ title }}</h1>
      <p v-if="subtitle" class="text-muted mb-0">{{ subtitle }}</p>
    </div>
    <div class="d-flex gap-2 flex-wrap"><slot name="actions" /></div>
  </div>
</template>
