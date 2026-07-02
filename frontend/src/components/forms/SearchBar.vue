<script setup>
import Icon from '../Icon.vue'

defineProps({ modelValue: String, placeholder: { type: String, default: 'Search...' } })
const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="search-bar">
    <Icon name="search" :size="16" class="search-ic" />
    <input
      :value="modelValue" :placeholder="placeholder" class="form-control"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </div>
</template>

<style scoped>
.search-bar { position: relative; min-width: 220px; }
.search-ic { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: var(--ppa-muted); }
.search-bar .form-control { padding-left: 34px; border-radius: 999px; }
</style>
