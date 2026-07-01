<script setup>
// Renders a lifecycle status (application / drive / company) as a tinted pill.
defineProps({ status: { type: String, default: '' } })
</script>

<template>
  <span class="status-badge" :class="`st-${status}`">{{ status }}</span>
</template>
