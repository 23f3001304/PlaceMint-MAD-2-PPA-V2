<script setup>
import { RouterLink } from 'vue-router'

import DitherImage from '../media/DitherImage.vue'
</script>

<template>
  <footer class="footer">
    <DitherImage src="/img/hero.jpg" alt="" tint="green" class="footer-bg" />
    <div class="footer-overlay"></div>
    <div class="footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="brand-mark text-white fs-3 mb-2">PlaceMint</div>
          <p class="mb-0 muted" style="max-width: 24rem">
            Campus placements without the spreadsheets. One place for the cell, companies, and students.
          </p>
        </div>
        <div class="footer-cols">
          <div class="fcol">
            <div class="fhead">Get started</div>
            <RouterLink to="/register" class="flink">Register</RouterLink>
            <RouterLink to="/login" class="flink">Sign in</RouterLink>
          </div>
          <div class="fcol">
            <div class="fhead">Built for</div>
            <span class="muted">Placement cell</span>
            <span class="muted">Companies</span>
            <span class="muted">Students</span>
          </div>
        </div>
      </div>

      <div class="footer-word brand-mark">PlaceMint</div>

      <div class="footer-base">
        <span class="muted small">Institute Placement Cell</span>
        <span class="muted small">Built with Flask · Vue · Bootstrap</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer { position: relative; overflow: hidden; color: #fff; padding-top: clamp(3rem, 6vw, 5rem); }
.footer-bg { position: absolute; inset: 0; z-index: 0; }
.footer-overlay { position: absolute; inset: 0; z-index: 1; background: linear-gradient(180deg, rgba(0, 0, 0, 0.38), rgba(0, 0, 0, 0.58)); }
.footer-content { position: relative; z-index: 2; padding: 0 clamp(1.5rem, 5vw, 4rem); }
.footer-top { display: flex; justify-content: space-between; gap: 2.5rem; flex-wrap: wrap; }
.footer-brand { max-width: 26rem; }
.footer-cols { display: flex; gap: clamp(2.5rem, 6vw, 5rem); flex-wrap: wrap; }
.fcol { display: flex; flex-direction: column; gap: 0.5rem; }
.fhead { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.7rem; font-weight: 700; opacity: 0.85; margin-bottom: 0.2rem; }
.flink { color: #fff; text-decoration: none; opacity: 0.9; }
.flink:hover { opacity: 1; text-decoration: underline; }
.muted { color: rgba(255, 255, 255, 0.78); }
.footer-word {
  text-align: center; font-size: clamp(4rem, 18vw, 15rem); line-height: 0.8; letter-spacing: -0.04em;
  color: rgba(255, 255, 255, 0.14); margin-top: 1.5rem; user-select: none; pointer-events: none;
}
.footer-base {
  border-top: 1px solid rgba(255, 255, 255, 0.2); padding: 1.2rem 0;
  display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
}
</style>
