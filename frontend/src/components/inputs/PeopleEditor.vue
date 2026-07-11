<script setup>
// Edits a capped list of key people { name, role, url } (a company's CEO,
// investor, founder). Emits a fresh array so it works with v-model.
import Icon from '../Icon.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  max: { type: Number, default: 2 },
})
const emit = defineEmits(['update:modelValue'])

function edit(i, key, value) {
  emit('update:modelValue', props.modelValue.map((p, idx) => (idx === i ? { ...p, [key]: value } : p)))
}
function add() {
  if (props.modelValue.length < props.max) emit('update:modelValue', [...props.modelValue, { name: '', role: '', url: '' }])
}
function remove(i) {
  emit('update:modelValue', props.modelValue.filter((_, idx) => idx !== i))
}
</script>

<template>
  <div class="d-flex flex-column gap-2">
    <div v-for="(person, i) in modelValue" :key="i" class="person-row">
      <input class="form-control" :value="person.name" placeholder="Name" @input="edit(i, 'name', $event.target.value)" />
      <input class="form-control" :value="person.role" placeholder="Role (CEO, Investor)" @input="edit(i, 'role', $event.target.value)" />
      <input class="form-control" :value="person.url" placeholder="LinkedIn / profile URL" @input="edit(i, 'url', $event.target.value)" />
      <button type="button" class="btn btn-outline-secondary" title="Remove" @click="remove(i)">
        <Icon name="plus" :size="16" style="transform: rotate(45deg)" />
      </button>
    </div>
    <div>
      <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="modelValue.length >= max" @click="add">
        <Icon name="plus" :size="14" /> Add person
      </button>
      <span class="small text-muted ms-2">{{ modelValue.length }} / {{ max }}</span>
    </div>
  </div>
</template>

<style scoped>
.person-row { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) minmax(0, 1.4fr) auto; gap: 0.5rem; align-items: center; }
@media (max-width: 640px) { .person-row { grid-template-columns: 1fr; } }
</style>
