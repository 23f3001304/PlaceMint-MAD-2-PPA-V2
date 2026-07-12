<script setup>
// Labelled input (text/number/email/password/tel/textarea/select). Selects use
// the custom SelectMenu; other inputs get inline type + pattern validation shown
// on blur. The backend re-validates and sanitizes, so this is UX, not the gate.
import { computed, ref } from 'vue'
import SelectMenu from '../inputs/SelectMenu.vue'

const props = defineProps({
  label: String,
  modelValue: { type: [String, Number], default: '' },
  type: { type: String, default: 'text' },
  required: Boolean,
  error: String,
  hint: String,
  placeholder: String,
  options: { type: Array, default: () => [] },
  id: String,
  autocomplete: String,
  min: [String, Number],
  max: [String, Number],
  step: [String, Number],
  pattern: String,
  inputmode: String,
  maxlength: [String, Number],
  title: String,
})
const emit = defineEmits(['update:modelValue'])
const onInput = (e) => emit('update:modelValue', e.target.value)

const touched = ref(false)
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

const localError = computed(() => {
  const v = String(props.modelValue ?? '').trim()
  if (props.required && !v) return `${props.label || 'This field'} is required`
  if (!v) return ''
  if (props.type === 'email' && !EMAIL_RE.test(v)) return 'Enter a valid email address'
  if (props.type === 'number') {
    const n = Number(v)
    if (Number.isNaN(n)) return 'Enter a number'
    if (props.min != null && n < Number(props.min)) return `Must be at least ${props.min}`
    if (props.max != null && n > Number(props.max)) return `Must be at most ${props.max}`
  }
  if (props.pattern && !new RegExp(`^(?:${props.pattern})$`).test(v)) return props.title || 'Please match the required format'
  return ''
})
const shownError = computed(() => props.error || (touched.value ? localError.value : ''))
</script>

<template>
  <div class="mb-3">
    <label v-if="label" :for="id" class="form-label fw-semibold small">
      {{ label }} <span v-if="required" class="text-danger">*</span>
    </label>

    <textarea
      v-if="type === 'textarea'" :id="id" class="form-control" :class="{ 'is-invalid': shownError }"
      :value="modelValue" :placeholder="placeholder" :required="required" :maxlength="maxlength" rows="3"
      @input="onInput" @blur="touched = true"
    ></textarea>

    <SelectMenu
      v-else-if="type === 'select'" :model-value="modelValue" :options="options" block
      :placeholder="placeholder || 'Select...'"
      @update:model-value="(v) => { emit('update:modelValue', v); touched = true }"
    />

    <input
      v-else :id="id" :type="type" class="form-control" :class="{ 'is-invalid': shownError }"
      :value="modelValue" :placeholder="placeholder" :required="required" :autocomplete="autocomplete"
      :min="min" :max="max" :step="step" :inputmode="inputmode" :maxlength="maxlength"
      @input="onInput" @blur="touched = true"
    />

    <div v-if="hint && !shownError" class="form-text">{{ hint }}</div>
    <div v-if="shownError" class="invalid-feedback d-block">{{ shownError }}</div>
  </div>
</template>
