<script setup>
defineProps({
  eyebrow: String,
  title: String,
  highlight: String,
  body: String,
  bullets: { type: Array, default: () => [] },
  image: String,
  tint: { type: String, default: 'tint-mint' },
  reverse: Boolean,
})
</script>

<template>
  <section class="feature" :class="{ reverse }">
    <div v-reveal class="feature-text">
      <div v-if="eyebrow" class="eyebrow">{{ eyebrow }}</div>
      <h2 class="feature-title">{{ title }} <span v-if="highlight" class="hl">{{ highlight }}</span></h2>
      <p class="text-muted mb-1">{{ body }}</p>
      <ul class="feature-list">
        <li v-for="b in bullets" :key="b">{{ b }}</li>
      </ul>
    </div>
    <div v-reveal="{ delay: '100ms' }" class="feature-visual" :class="tint">
      <img :src="image" :alt="eyebrow" class="shot" loading="lazy" />
    </div>
  </section>
</template>

<style scoped>
.feature { display: grid; grid-template-columns: 1fr; border-top: 1px solid var(--ppa-border); }
@media (min-width: 900px) {
  .feature { grid-template-columns: 5fr 6fr; }
  .feature.reverse .feature-text { order: 2; }
  .feature.reverse .feature-visual { order: 1; }
}
.feature-text { padding: clamp(2rem, 5vw, 4.5rem); display: flex; flex-direction: column; justify-content: center; gap: 1rem; }
.eyebrow { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.72rem; font-weight: 700; color: var(--ppa-accent); }
.feature-title { font-family: var(--ppa-font-display); font-weight: 800; font-size: clamp(1.7rem, 3vw, 2.5rem); line-height: 1.08; letter-spacing: -0.015em; margin: 0; }
.feature-list { list-style: none; padding: 0; margin: 0; }
.feature-list li { position: relative; padding: 0.5rem 0 0.5rem 1.5rem; color: var(--ppa-muted); font-size: 0.95rem; }
.feature-list li::before { content: ''; position: absolute; left: 0; top: 0.85rem; width: 8px; height: 8px; border-radius: 2px; background: var(--ppa-accent); }
.feature-visual { padding: clamp(2rem, 4vw, 3.5rem); display: grid; place-items: center; border-top: 1px solid var(--ppa-border); }
@media (min-width: 900px) {
  .feature-visual { border-top: 0; border-left: 1px solid var(--ppa-border); }
  .feature.reverse .feature-visual { border-left: 0; border-right: 1px solid var(--ppa-border); }
}
.shot { width: 100%; max-width: 620px; border-radius: 0.9rem; border: 1px solid var(--ppa-border); box-shadow: 0 26px 60px -24px rgba(20, 71, 42, 0.4); display: block; }
</style>
