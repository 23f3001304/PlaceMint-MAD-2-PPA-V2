<script setup>
// Reusable add-item editor for {title, <secondKey>, period, description} entries.
// Used for Experience (secondKey "org") and Projects (secondKey "link").
import Icon from '../Icon.vue'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  max: { type: Number, default: 6 },
  titlePlaceholder: { type: String, default: 'Role / title (e.g. SDE Intern)' },
  secondKey: { type: String, default: 'org' },
  secondPlaceholder: { type: String, default: 'Organization' },
  addLabel: { type: String, default: 'Add experience' },
})
const emit = defineEmits(['update:modelValue'])

function edit(i, key, value) {
  emit('update:modelValue', props.modelValue.map((x, idx) => (idx === i ? { ...x, [key]: value } : x)))
}
function add() {
  if (props.modelValue.length < props.max) {
    emit('update:modelValue', [...props.modelValue, { title: '', [props.secondKey]: '', period: '', description: '' }])
  }
}
function remove(i) {
  emit('update:modelValue', props.modelValue.filter((_, idx) => idx !== i))
}
</script>

<template>
  <div class="d-flex flex-column gap-3">
    <div v-for="(x, i) in modelValue" :key="i" class="exp-item">
      <div class="d-flex gap-2 mb-2">
        <input class="form-control" :value="x.title" :placeholder="titlePlaceholder" @input="edit(i, 'title', $event.target.value)" />
        <button type="button" class="btn btn-outline-secondary" title="Remove" @click="remove(i)">
          <Icon name="plus" :size="16" style="transform: rotate(45deg)" />
        </button>
      </div>
      <div class="row gx-2 mb-2">
        <div class="col-7"><input class="form-control" :value="x[secondKey]" :placeholder="secondPlaceholder" @input="edit(i, secondKey, $event.target.value)" /></div>
        <div class="col-5"><input class="form-control" :value="x.period" placeholder="e.g. May-Jul 2024" @input="edit(i, 'period', $event.target.value)" /></div>
      </div>
      <textarea class="form-control" :value="x.description" rows="2" placeholder="What you did, tech used, impact..." @input="edit(i, 'description', $event.target.value)"></textarea>
    </div>
    <div>
      <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="modelValue.length >= max" @click="add">
        <Icon name="plus" :size="14" /> {{ addLabel }}
      </button>
      <span class="small text-muted ms-2">{{ modelValue.length }} / {{ max }}</span>
    </div>
  </div>
</template>

<style scoped>
.exp-item { border: 1px solid var(--ppa-border); border-radius: 0.7rem; padding: 0.9rem; background: var(--ppa-surface-sunk); }
</style>
