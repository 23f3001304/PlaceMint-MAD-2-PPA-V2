<script setup>
defineProps({ drive: { type: Object, required: true } })
const emit = defineEmits(['apply', 'view'])
</script>

<template>
  <div class="surface-card p-3 h-100 d-flex flex-column">
    <div class="d-flex justify-content-between align-items-start gap-2">
      <div>
        <div class="fw-semibold">{{ drive.job_title }}</div>
        <div class="small text-muted">
          {{ drive.company_name }}<span v-if="drive.location"> · {{ drive.location }}</span>
        </div>
      </div>
      <span v-if="drive.package_lpa" class="badge text-bg-light text-mono">{{ drive.package_lpa }} LPA</span>
    </div>

    <div v-if="(drive.skills_required || []).length" class="my-2 d-flex flex-wrap gap-1">
      <span v-for="s in drive.skills_required.slice(0, 4)" :key="s" class="badge text-bg-light">{{ s }}</span>
    </div>

    <div class="small text-muted mb-2">Apply by {{ drive.deadline }}</div>

    <div class="mt-auto d-flex gap-2 align-items-center flex-wrap">
      <button class="btn btn-sm btn-outline-secondary" @click="emit('view', drive)">Details</button>
      <button v-if="drive.applied" class="btn btn-sm btn-outline-success" disabled>Applied</button>
      <button v-else-if="drive.eligible" class="btn btn-sm btn-3d-accent" @click="emit('apply', drive)">Apply</button>
      <span
        v-else class="status-badge st-rejected"
        :title="(drive.ineligibility_reasons || []).join(', ')"
      >Not eligible</span>
    </div>
  </div>
</template>
