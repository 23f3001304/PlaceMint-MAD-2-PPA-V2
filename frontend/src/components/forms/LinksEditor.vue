<script setup>
// Edits a capped list of { label, url } links (student 3, company 4). Emits a
// fresh array on every change so it works with v-model.
import Icon from '../Icon.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  max: { type: Number, default: 3 },
})
const emit = defineEmits(['update:modelValue'])

function edit(i, key, value) {
  emit('update:modelValue', props.modelValue.map((l, idx) => (idx === i ? { ...l, [key]: value } : l)))
}
function add() {
  if (props.modelValue.length < props.max) emit('update:modelValue', [...props.modelValue, { label: '', url: '' }])
}
function remove(i) {
  emit('update:modelValue', props.modelValue.filter((_, idx) => idx !== i))
}
</script>

<template>
  <div class="d-flex flex-column gap-2">
    <div v-for="(link, i) in modelValue" :key="i" class="link-row">
      <input class="form-control" :value="link.label" placeholder="Label (LinkedIn, X, Portfolio)" @input="edit(i, 'label', $event.target.value)" />
      <input class="form-control" :value="link.url" placeholder="https://..." @input="edit(i, 'url', $event.target.value)" />
      <button type="button" class="btn btn-outline-secondary link-del" title="Remove" @click="remove(i)">
        <Icon name="plus" :size="16" style="transform: rotate(45deg)" />
      </button>
    </div>
    <div>
      <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="modelValue.length >= max" @click="add">
        <Icon name="plus" :size="14" /> Add link
      </button>
      <span class="small text-muted ms-2">{{ modelValue.length }} / {{ max }}</span>
    </div>
  </div>
</template>

<style scoped>
.link-row { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr) auto; gap: 0.5rem; align-items: center; }
.link-del { display: inline-flex; align-items: center; }
</style>
