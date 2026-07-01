<script setup>
// Labelled input supporting text/number/email/password/textarea/select, with
// Bootstrap validation styling. Two-way bound via v-model.
defineProps({
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
  step: [String, Number],
})
const emit = defineEmits(['update:modelValue'])
const onInput = (e) => emit('update:modelValue', e.target.value)
</script>

<template>
  <div class="mb-3">
    <label v-if="label" :for="id" class="form-label fw-semibold small">
      {{ label }} <span v-if="required" class="text-danger">*</span>
    </label>

    <textarea
      v-if="type === 'textarea'" :id="id" class="form-control" :class="{ 'is-invalid': error }"
      :value="modelValue" :placeholder="placeholder" :required="required" rows="3" @input="onInput"
    ></textarea>

    <select
      v-else-if="type === 'select'" :id="id" class="form-select" :class="{ 'is-invalid': error }"
      :value="modelValue" :required="required" @change="onInput"
    >
      <option value="" disabled>{{ placeholder || 'Select...' }}</option>
      <option v-for="o in options" :key="o.value ?? o" :value="o.value ?? o">{{ o.label ?? o }}</option>
    </select>

    <input
      v-else :id="id" :type="type" class="form-control" :class="{ 'is-invalid': error }"
      :value="modelValue" :placeholder="placeholder" :required="required"
      :autocomplete="autocomplete" :min="min" :step="step" @input="onInput"
    />

    <div v-if="hint && !error" class="form-text">{{ hint }}</div>
    <div v-if="error" class="invalid-feedback d-block">{{ error }}</div>
  </div>
</template>
