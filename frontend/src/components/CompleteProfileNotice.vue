<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="surface-card p-5 text-center motion-fade-up">
    <h3 class="h5 mb-1">Complete your profile first</h3>
    <p class="text-muted mb-3" style="max-width: 30rem; margin-inline: auto">
      Add your CGPA and skills so we can show which drives you are actually eligible for.
    </p>
    <RouterLink to="/student/onboarding" class="btn btn-3d-accent px-4">Complete profile</RouterLink>
  </div>
</template>
