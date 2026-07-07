<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { authState } from '../../store/auth'
import { homeFor } from '../../router/guards'
import BrandMark from '../BrandMark.vue'
import DitherImage from '../media/DitherImage.vue'

const bg = ref(null)
let raf = 0

function onScroll() {
  if (raf) return
  raf = requestAnimationFrame(() => {
    if (bg.value) bg.value.style.transform = `translateY(${window.scrollY * 0.28}px)`
    raf = 0
  })
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header class="hero">
    <div ref="bg" class="hero-parallax"><DitherImage src="/img/mountains.jpg" alt="" tint="green" class="hero-bg" /></div>

    <nav class="hero-nav">
      <BrandMark :size="34" class="text-white" />
      <div class="d-flex gap-2 align-items-center">
        <RouterLink v-if="authState.user" :to="homeFor(authState.user.role)" class="nav-pill nav-pill-solid">Dashboard</RouterLink>
        <template v-else>
          <RouterLink to="/login" class="nav-pill">Sign in</RouterLink>
          <RouterLink to="/register" class="nav-pill nav-pill-solid">Register</RouterLink>
        </template>
      </div>
    </nav>

    <div class="hero-content">
      <h1 class="hero-title text-white">Campus placements,<br />run like <span class="hl">clockwork.</span></h1>
      <p class="hero-sub text-white">
        One portal for the placement cell, companies, and students. Approvals, drives,
        applications and offers, all in one place.
      </p>
    </div>

    <div class="scroll-cue" aria-hidden="true"><span></span></div>
  </header>
</template>

<style scoped>
.hero { position: relative; overflow: hidden; min-height: 100vh; display: flex; flex-direction: column; padding: 1.5rem clamp(1rem, 5vw, 4rem); }
.hero-parallax { position: absolute; inset: -12% 0 0 0; z-index: 0; will-change: transform; }
.hero-bg { position: absolute; inset: 0; height: 118%; }
.hero-nav { position: relative; z-index: 1; display: flex; justify-content: space-between; align-items: center; }
.nav-pill { color: #fff; text-decoration: none; font-weight: 600; font-size: 0.92rem; padding: 0.5rem 1.15rem; border-radius: 999px; border: 1px solid rgba(255, 255, 255, 0.32); transition: background 0.15s ease, border-color 0.15s ease; }
.nav-pill:hover { background: rgba(255, 255, 255, 0.14); border-color: rgba(255, 255, 255, 0.55); }
.nav-pill-solid { background: #fff; color: var(--ppa-ink); border-color: #fff; }
.nav-pill-solid:hover { background: #ece6d6; border-color: #ece6d6; color: var(--ppa-ink); }
.hero-content { position: relative; z-index: 1; margin-top: auto; margin-bottom: 3rem; max-width: 760px; }
.hero-title { font-size: clamp(2.6rem, 7vw, 5rem); font-weight: 800; line-height: 1; letter-spacing: -0.025em; }
.hero-sub { font-size: 1.15rem; max-width: 34rem; margin: 1.2rem 0 1.8rem; opacity: 0.92; }
.hero-cta { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.scroll-cue { position: absolute; bottom: 1.2rem; left: 50%; transform: translateX(-50%); z-index: 1; width: 24px; height: 38px; border: 2px solid rgba(255, 255, 255, 0.5); border-radius: 12px; }
.scroll-cue span { display: block; width: 4px; height: 8px; background: #fff; border-radius: 2px; margin: 6px auto; animation: cue 1.6s infinite; }
@keyframes cue { 0% { opacity: 0; transform: translateY(0); } 40% { opacity: 1; } 100% { opacity: 0; transform: translateY(12px); } }
</style>
