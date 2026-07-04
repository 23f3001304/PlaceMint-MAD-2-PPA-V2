<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { publicStats } from '../api/shared/public'
import { authState } from '../store/auth'
import { homeFor } from '../router/guards'
import { toChartData } from '../data/charts'
import ChartCanvas from '../components/charts/ChartCanvas.vue'
import DitherImage from '../components/media/DitherImage.vue'

const stats = ref(null)
onMounted(async () => {
  try {
    stats.value = (await publicStats()).data
  } catch {
    stats.value = null
  }
})

const ROLES = [
  { name: 'Placement Cell', text: 'Approve companies and drives, moderate accounts, and watch institute-wide numbers in real time.' },
  { name: 'Companies', text: 'Register, post drives once approved, review applicants, schedule interviews and record hires.' },
  { name: 'Students', text: 'Complete a profile, browse drives you are eligible for, apply in a click, and track every outcome.' },
]
</script>

<template>
  <div class="landing silk-bg">
    <header class="hero">
      <DitherImage src="/img/team.jpg" alt="" tint="green" class="hero-bg" />
      <nav class="hero-nav">
        <span class="brand-mark text-white fs-4">PlaceMint</span>
        <div class="d-flex gap-2">
          <RouterLink v-if="authState.user" :to="homeFor(authState.user.role)" class="btn btn-light btn-sm">
            Go to dashboard
          </RouterLink>
          <template v-else>
            <RouterLink to="/login" class="btn btn-outline-light btn-sm">Sign in</RouterLink>
            <RouterLink to="/register" class="btn btn-light btn-sm">Register</RouterLink>
          </template>
        </div>
      </nav>
      <div class="hero-content">
        <h1 class="hero-title text-white">Campus placements,<br />run like clockwork.</h1>
        <p class="hero-sub text-white">
          One portal for the placement cell, companies, and students. Approvals, drives,
          applications and offers, all in one place.
        </p>
        <div class="d-flex gap-2 flex-wrap">
          <RouterLink to="/register" class="btn btn-3d-accent btn-lg">Get started</RouterLink>
          <RouterLink to="/login" class="btn btn-light btn-lg">Sign in</RouterLink>
        </div>
      </div>
    </header>

    <section class="band">
      <div v-for="item in [
        { k: 'students', label: 'Students' }, { k: 'companies', label: 'Companies' },
        { k: 'drives', label: 'Drives' }, { k: 'applications', label: 'Applications' },
        { k: 'placements', label: 'Placed' }]" :key="item.k" class="band-item">
        <div class="band-num">{{ stats ? stats[item.k] : 0 }}</div>
        <div class="band-cap">{{ item.label }}</div>
      </div>
    </section>

    <section class="container py-5">
      <div class="row g-4">
        <div v-for="role in ROLES" :key="role.name" class="col-md-4 role-col">
          <h2 class="h4 mb-2">{{ role.name }}</h2>
          <p class="text-muted mb-0">{{ role.text }}</p>
        </div>
      </div>
    </section>

    <section v-if="stats" class="container pb-5">
      <div class="surface-card p-4">
        <h2 class="h5 mb-3">Applications this season</h2>
        <ChartCanvas type="bar" :data="toChartData(stats.applications_by_status, 'Applications')" />
      </div>
    </section>

    <footer class="footer">
      <span class="brand-mark">PlaceMint</span>
      <span class="text-white-50 small">Institute Placement Cell</span>
    </footer>
  </div>
</template>

<style scoped>
.hero { position: relative; overflow: hidden; min-height: 82vh; display: flex; flex-direction: column; padding: 1.5rem clamp(1rem, 5vw, 4rem); }
.hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-nav { position: relative; z-index: 1; display: flex; justify-content: space-between; align-items: center; }
.hero-content { position: relative; z-index: 1; margin-top: auto; max-width: 720px; }
.hero-title { font-size: clamp(2.4rem, 6vw, 4.2rem); font-weight: 800; line-height: 1.02; letter-spacing: -0.02em; }
.hero-sub { font-size: 1.15rem; max-width: 34rem; margin: 1rem 0 1.6rem; opacity: 0.92; }
.band { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1px; background: var(--ppa-border); border-bottom: 1px solid var(--ppa-border); }
@media (min-width: 768px) { .band { grid-template-columns: repeat(5, 1fr); } }
.band-item { background: var(--ppa-surface); padding: 1.6rem 1rem; text-align: center; }
.band-num { font-family: var(--ppa-font-display); font-size: 2.4rem; font-weight: 800; color: var(--ppa-accent); line-height: 1; }
.band-cap { color: var(--ppa-muted); text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.75rem; margin-top: 0.35rem; }
.role-col + .role-col { border-left: 1px solid var(--ppa-border); padding-left: 1.5rem; }
@media (max-width: 767px) { .role-col + .role-col { border-left: 0; padding-left: 0.75rem; } }
.footer { background: var(--ppa-ink); color: #fff; padding: 2rem clamp(1rem, 5vw, 4rem); display: flex; justify-content: space-between; align-items: center; }
</style>
