<script setup>
import { authState } from '../../store/auth'
</script>

<template>
  <div class="motion-fade-up">
    <h1 class="h3 mb-1">Placement overview</h1>
    <p class="text-muted">Signed in as {{ authState.user?.email }}</p>
    <div class="surface-card p-4 mt-3 text-muted">Institute statistics load here.</div>
  </div>
</template>
