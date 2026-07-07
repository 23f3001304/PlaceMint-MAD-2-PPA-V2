<script setup>
// Leaf-P logo (icon + wordmark). Wordmark colour inherits from the parent, so
// wrap with `text-white` on dark surfaces.
defineProps({ size: { type: Number, default: 30 }, wordmark: { type: Boolean, default: true } })
</script>

<template>
  <span class="brand d-inline-flex align-items-center gap-2">
    <svg :width="size" :height="size" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <rect width="512" height="512" rx="104" fill="#1f6b3a" />
      <path d="M150 150h104a88 88 0 0 1 0 176h-56v80h-48V150zm48 48v80h56a40 40 0 0 0 0-80h-56z" fill="#ffffff" />
      <path d="M298 150c34-78 128-96 156-100-2 46-18 132-118 148-26 4-44-16-38-48z" fill="#7fce97" />
      <path d="M312 178c40-52 104-96 140-120" stroke="#1f6b3a" stroke-width="9" fill="none" stroke-linecap="round" />
    </svg>
    <span v-if="wordmark" class="brand-word">PlaceMint</span>
  </span>
</template>

<style scoped>
.brand-word { font-family: var(--ppa-font-display); font-weight: 800; letter-spacing: -0.02em; font-size: 1.25rem; }
</style>
