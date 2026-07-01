<script setup>
// Photo rendered as an on-brand duotone with a halftone-dot overlay.
// `tint="green"` adds a forest-green wash so text sits legibly on top.
defineProps({
  src: String,
  alt: { type: String, default: '' },
  tint: { type: String, default: 'green' },
})
</script>

<template>
  <div class="dither" :class="`dither-${tint}`">
    <img :src="src" :alt="alt" class="dither-img" />
    <span class="dither-dots" aria-hidden="true"></span>
  </div>
</template>

<style scoped>
.dither { position: relative; overflow: hidden; background: #14472a; }
.dither-img {
  width: 100%; height: 100%; object-fit: cover; display: block;
  filter: url(#ppa-duotone) contrast(1.04);
}
.dither-dots {
  position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(rgba(10, 20, 12, 0.55) 0.5px, transparent 0.7px);
  background-size: 3px 3px; mix-blend-mode: soft-light; opacity: 0.55;
}
.dither-green::after {
  content: ''; position: absolute; inset: 0; mix-blend-mode: multiply;
  background: linear-gradient(160deg, rgba(20, 71, 42, 0.72), rgba(31, 107, 58, 0.5) 55%, rgba(14, 50, 28, 0.82));
}
</style>
