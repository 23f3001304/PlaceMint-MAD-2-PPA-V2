<script setup>
import DitherImage from '../../components/media/DitherImage.vue'

defineProps({ title: String, subtitle: String, wide: Boolean })
</script>

<template>
  <div class="auth-wrap">
    <aside class="auth-brand d-none d-lg-block">
      <DitherImage src="/img/auth-campus.jpg" alt="" tint="green" class="auth-brand-bg" />
      <div class="auth-brand-inner">
        <div>
          <div class="brand-mark display-5 text-white mb-3">PlaceMint</div>
          <p class="lead text-white mb-0" style="max-width: 22rem; opacity: 0.9">
            Campus placements without the spreadsheets. One place for the cell,
            companies, and students.
          </p>
        </div>
        <div class="text-white small" style="opacity: 0.75">Institute Placement Cell</div>
      </div>
    </aside>

    <main class="auth-form-col silk-bg">
      <div class="auth-inner motion-fade-up" :style="{ maxWidth: wide ? '640px' : '400px' }">
        <div class="d-lg-none mb-4"><span class="brand-mark fs-2">PlaceMint</span></div>
        <h1 class="h3 mb-1">{{ title }}</h1>
        <p class="text-muted mb-4">{{ subtitle }}</p>
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-wrap { min-height: 100vh; display: grid; grid-template-columns: 1fr; }
@media (min-width: 992px) { .auth-wrap { grid-template-columns: 44% 56%; } }
.auth-brand { position: relative; overflow: hidden; padding: 3rem; background: #14472a; min-height: 100vh; }
.auth-brand-bg { position: absolute; inset: 0; z-index: 0; }
.auth-brand-inner {
  position: relative; z-index: 1; height: 100%;
  display: flex; flex-direction: column; justify-content: space-between;
}
.auth-form-col {
  display: flex; align-items: center; justify-content: center;
  padding: 3rem 1.75rem;
}
.auth-inner { width: 100%; }
</style>
