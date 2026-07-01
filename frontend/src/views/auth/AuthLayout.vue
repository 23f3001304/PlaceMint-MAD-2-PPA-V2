<script setup>
defineProps({ title: String, subtitle: String })
</script>

<template>
  <div class="auth-wrap">
    <aside class="auth-brand d-none d-lg-flex bg-grid-dots">
      <div>
        <div class="brand-mark display-5 text-white mb-3">PlaceMint</div>
        <p class="lead text-white-50 mb-0" style="max-width: 22rem">
          Campus placements without the spreadsheets. One place for the cell,
          companies, and students.
        </p>
      </div>
      <div class="text-white-50 small">Institute Placement Cell</div>
    </aside>

    <main class="auth-form-col">
      <div class="auth-card motion-fade-up">
        <h1 class="h3 mb-1">{{ title }}</h1>
        <p class="text-muted mb-4">{{ subtitle }}</p>
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.auth-wrap { min-height: 100vh; display: grid; grid-template-columns: 1fr; }
@media (min-width: 992px) { .auth-wrap { grid-template-columns: 42% 58%; } }
.auth-brand {
  background: linear-gradient(160deg, #1f6b3a, #14472a); color: #fff; padding: 3rem;
  flex-direction: column; justify-content: space-between;
}
.auth-form-col { display: grid; place-items: center; padding: 2rem 1.25rem; background: var(--ppa-bg); }
.auth-card {
  width: 100%; max-width: 440px; background: var(--ppa-surface);
  border: 1px solid var(--ppa-border); border-radius: 1rem; padding: 2rem;
}
</style>
