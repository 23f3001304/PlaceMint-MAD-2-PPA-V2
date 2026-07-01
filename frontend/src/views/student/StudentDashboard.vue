<script setup>
import { authState } from '../../store/auth'
</script>

<template>
  <div class="motion-fade-up">
    <h1 class="h3 mb-1">Hi {{ authState.profile?.name }}</h1>
    <p class="text-muted mb-3">Student dashboard</p>

    <div class="surface-card p-4">
      <div class="text-mono small text-muted mb-2">
        {{ authState.profile?.roll_no }} · {{ authState.profile?.branch }} · CGPA {{ authState.profile?.cgpa }}
      </div>
      <p class="mb-0 text-muted">Browse approved drives and track your applications from the sidebar.</p>
    </div>
  </div>
</template>
