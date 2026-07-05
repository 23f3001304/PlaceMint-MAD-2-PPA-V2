<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section v-reveal class="final-cta">
    <h2 class="cta-title">Run placements <span class="hl">without the chaos.</span></h2>
    <p class="text-muted mb-4">Set up your institute, invite companies, and open the season in minutes.</p>
    <div class="d-flex gap-2 justify-content-center flex-wrap">
      <RouterLink to="/register" class="btn btn-3d-accent btn-lg">Get started</RouterLink>
      <RouterLink to="/login" class="btn btn-outline-secondary btn-lg">Sign in</RouterLink>
    </div>
  </section>
</template>

<style scoped>
.final-cta { border-top: 1px solid var(--ppa-border); padding: clamp(3rem, 8vw, 6rem) 1.5rem; text-align: center; }
.cta-title { font-family: var(--ppa-font-display); font-weight: 800; font-size: clamp(1.8rem, 4vw, 3rem); letter-spacing: -0.02em; margin: 0 auto 0.6rem; max-width: 22ch; }
</style>
