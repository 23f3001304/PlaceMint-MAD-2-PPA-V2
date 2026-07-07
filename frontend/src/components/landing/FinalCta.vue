<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section v-reveal class="cta-wrap">
    <div class="cta-banner">
      <span class="cta-badge" aria-hidden="true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M7 17 17 7M17 7H8M17 7v9" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
      <div class="cta-inner">
        <p class="cta-eyebrow"><span class="cta-square"></span>Placement season, sorted</p>
        <h2 class="cta-title">Run placements <span class="cta-em">without the chaos.</span></h2>
        <p class="cta-sub">Set up your institute, invite companies, and open the season in minutes.</p>
        <div class="cta-actions">
          <RouterLink to="/register" class="cta-btn cta-primary">Get started</RouterLink>
          <RouterLink to="/login" class="cta-btn cta-ghost">Sign in</RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-wrap { padding: clamp(1rem, 4vw, 3rem); }
.cta-banner {
  position: relative; overflow: hidden; isolation: isolate;
  padding: clamp(2.5rem, 7vw, 5.5rem) clamp(1.5rem, 6vw, 5rem);
  border-radius: 1.5rem; color: #f4f0e8;
  background:
    radial-gradient(130% 130% at 100% 0%, rgba(46, 138, 77, 0.55), transparent 55%),
    linear-gradient(155deg, #1f6b3a, #0f4624);
  box-shadow: 0 40px 80px -40px rgba(15, 70, 36, 0.7);
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
.cta-badge {
  position: absolute; top: clamp(1.25rem, 3vw, 2rem); right: clamp(1.25rem, 3vw, 2rem);
  width: 2.75rem; height: 2.75rem; display: grid; place-items: center;
  background: #7fce97; color: #0f4624; border-radius: 0.7rem;
}
.cta-inner { position: relative; max-width: 42rem; }
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
</style>
