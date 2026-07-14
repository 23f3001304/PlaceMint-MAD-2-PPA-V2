<script setup>
// Avatar preview + "upload a file" and "paste a URL" controls. The parent owns
// the upload API call (emits 'file'); the URL is v-model-bound.
defineProps({
  modelValue: { type: String, default: '' },
  src: { type: String, default: '' },
  initial: { type: String, default: '?' },
  uploading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'file'])

function onFile(e) {
  const file = e.target.files[0]
  if (file) emit('file', file)
}
</script>

<template>
  <div class="d-flex align-items-center gap-3">
    <span class="av" :class="{ 'has-img': src }">
      <img v-if="src" :src="src" alt="" />
      <template v-else>{{ initial }}</template>
    </span>
    <div class="flex-grow-1">
      <label class="btn btn-outline-secondary btn-sm mb-2">
        {{ uploading ? 'Uploading...' : 'Upload photo' }}
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden @change="onFile" />
      </label>
      <input
        class="form-control" :value="modelValue" placeholder="Or paste a photo URL"
        @input="emit('update:modelValue', $event.target.value)"
      />
    </div>
  </div>
</template>

<style scoped>
.av {
  width: 64px; height: 64px; border-radius: 50%; background: var(--ppa-accent); color: #fff; flex: none; overflow: hidden;
  display: grid; place-items: center; font-weight: 800; font-size: 1.5rem; font-family: var(--ppa-font-display);
}
.av.has-img { background: #fff; border: 1px solid var(--ppa-border); }
.av img { width: 100%; height: 100%; object-fit: cover; }
</style>
