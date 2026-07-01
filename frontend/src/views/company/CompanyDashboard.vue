<script setup>
import { authState } from '../../store/auth'
import StatusBadge from '../../components/ui/StatusBadge.vue'
</script>

<template>
  <div class="motion-fade-up">
    <h1 class="h3 mb-1">{{ authState.profile?.company_name }}</h1>
    <p class="text-muted mb-3">Company dashboard</p>

    <div class="surface-card p-4">
      <div class="d-flex align-items-center gap-2 mb-2">
        <span class="fw-semibold">Approval status</span>
        <StatusBadge :status="authState.profile?.approval_status" />
      </div>
      <p v-if="authState.profile?.approval_status !== 'approved'" class="text-muted mb-0">
        Your registration is awaiting admin approval. You can post job drives once approved.
      </p>
      <p v-else class="text-muted mb-0">You are approved. Post drives from the sidebar.</p>
    </div>
  </div>
</template>
