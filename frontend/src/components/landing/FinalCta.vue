<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section v-reveal class="cta-banner">
    <div class="cta-inner">
      <span class="cta-tag">Placement season, sorted</span>
      <h2 class="cta-title">Run placements <span class="cta-em">without the chaos.</span></h2>
      <p class="cta-sub">Bring Mint University's companies and students into one portal, and open the season in minutes.</p>
      <div class="cta-actions">
        <RouterLink to="/register" class="cta-btn cta-primary">Get started</RouterLink>
        <RouterLink to="/login" class="cta-btn cta-ghost">Sign in</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-banner {
  position: relative; overflow: hidden;
  padding: clamp(3rem, 8vw, 6rem) clamp(1.5rem, 6vw, 5rem);
  background: #1c6e3c; color: #f4f0e8;
  border-top: 4px solid #0f4624;
}
.cta-banner::before {
  content: ''; position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background-image:
    linear-gradient(rgba(244, 240, 232, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(244, 240, 232, 0.08) 1px, transparent 1px);
  background-size: 46px 46px;
}
.cta-inner { position: relative; z-index: 1; max-width: 44rem; }
.cta-tag {
  display: inline-block; margin: 0 0 1.1rem; padding: 0.32rem 0.62rem;
  background: #7fce97; color: #0f4624;
  font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.72rem;
}
.cta-title {
  font-family: var(--ppa-font-display); font-weight: 800; letter-spacing: -0.03em;
  font-size: clamp(2.4rem, 6vw, 4.4rem); line-height: 1.0; margin: 0 0 1.2rem;
}
.cta-em {
  background: #7fce97; color: #0f4624; padding: 0 0.35rem;
  -webkit-box-decoration-break: clone; box-decoration-break: clone;
}
.cta-sub { font-size: 1.12rem; color: rgba(244, 240, 232, 0.9); max-width: 32rem; margin: 0 0 2rem; }
.cta-actions { display: flex; gap: 0.85rem; flex-wrap: wrap; }
.cta-btn {
  display: inline-flex; align-items: center; font-weight: 800; text-decoration: none;
  padding: 0.85rem 1.7rem; transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.1s ease;
}
.cta-primary { background: #f4f0e8; color: #14110f; }
.cta-primary:hover { transform: translate(-3px, -3px); box-shadow: 5px 5px 0 #0f4624; color: #14110f; }
.cta-ghost { background: transparent; color: #f4f0e8; border: 2px solid #f4f0e8; }
.cta-ghost:hover { background: #f4f0e8; color: #14110f; }
</style>
