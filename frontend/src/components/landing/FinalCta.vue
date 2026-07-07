<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section v-reveal class="cta-banner">
    <div class="cta-inner">
      <p class="cta-eyebrow"><span class="cta-square"></span>Placement season, sorted</p>
      <h2 class="cta-title">Run placements <span class="cta-em">without the chaos.</span></h2>
      <p class="cta-sub">Set up your institute, invite companies, and open the season in minutes.</p>
      <div class="cta-actions">
        <RouterLink to="/register" class="cta-btn cta-primary">Get started</RouterLink>
        <RouterLink to="/login" class="cta-btn cta-ghost">Sign in</RouterLink>
      </div>
    </div>

    <svg class="cta-pixels" viewBox="0 0 150 120" fill="#7fce97" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="30" height="30" opacity="0.9" />
      <rect x="60" y="0" width="30" height="30" opacity="0.5" />
      <rect x="120" y="0" width="30" height="30" opacity="0.8" />
      <rect x="30" y="30" width="30" height="30" opacity="0.6" />
      <rect x="90" y="30" width="30" height="30" opacity="0.95" />
      <rect x="0" y="60" width="30" height="30" opacity="0.5" />
      <rect x="60" y="60" width="30" height="30" opacity="0.85" />
      <rect x="120" y="60" width="30" height="30" opacity="0.55" />
      <rect x="30" y="90" width="30" height="30" opacity="0.8" />
      <rect x="90" y="90" width="30" height="30" opacity="0.45" />
    </svg>
  </section>
</template>

<style scoped>
.cta-banner {
  position: relative; overflow: hidden; isolation: isolate;
  padding: clamp(3rem, 8vw, 6rem) clamp(1.5rem, 6vw, 5rem);
  color: #f4f0e8;
  background:
    radial-gradient(130% 130% at 100% 0%, rgba(46, 138, 77, 0.5), transparent 55%),
    linear-gradient(155deg, #1f6b3a, #0f4624);
}
.cta-banner::before {
  content: ''; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background-image:
    linear-gradient(rgba(244, 240, 232, 0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(244, 240, 232, 0.07) 1px, transparent 1px);
  background-size: 46px 46px;
  -webkit-mask-image: radial-gradient(120% 110% at 0% 100%, #000, transparent 72%);
  mask-image: radial-gradient(120% 110% at 0% 100%, #000, transparent 72%);
}
.cta-inner { position: relative; z-index: 1; max-width: 42rem; }
.cta-eyebrow {
  display: inline-flex; align-items: center; gap: 0.5rem; margin: 0 0 1rem;
  text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.72rem; font-weight: 700;
  color: rgba(244, 240, 232, 0.82);
}
.cta-square { width: 0.6rem; height: 0.6rem; background: #7fce97; border-radius: 2px; }
.cta-title {
  font-family: var(--ppa-font-display); font-weight: 800; letter-spacing: -0.03em;
  font-size: clamp(2.2rem, 5.5vw, 4rem); line-height: 1.02; margin: 0 0 1rem;
}
.cta-em { color: #7fce97; }
.cta-sub { font-size: 1.1rem; color: rgba(244, 240, 232, 0.85); max-width: 32rem; margin: 0 0 2rem; }
.cta-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.cta-btn {
  display: inline-flex; align-items: center; font-weight: 700; text-decoration: none;
  padding: 0.8rem 1.6rem; border-radius: 999px;
  transition: transform 0.12s ease, background 0.12s ease, border-color 0.12s ease;
}
.cta-primary { background: #f4f0e8; color: #14110f; box-shadow: 0 12px 30px -12px rgba(0, 0, 0, 0.55); }
.cta-primary:hover { transform: translateY(-2px); background: #fff; color: #14110f; }
.cta-ghost { color: #f4f0e8; border: 1px solid rgba(244, 240, 232, 0.4); }
.cta-ghost:hover { background: rgba(244, 240, 232, 0.12); border-color: rgba(244, 240, 232, 0.7); color: #f4f0e8; }
.cta-pixels {
  position: absolute; z-index: 0; right: clamp(1.5rem, 5vw, 5rem); top: 50%;
  transform: translateY(-50%); width: clamp(140px, 18vw, 220px); height: auto; pointer-events: none;
}
@media (max-width: 860px) { .cta-pixels { display: none; } }
</style>
