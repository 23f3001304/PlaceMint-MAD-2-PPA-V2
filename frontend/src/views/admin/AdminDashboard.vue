<script setup>
import { onMounted, ref } from 'vue'

import * as adminApi from '../../api/endpoints/admin'
import { toChartData } from '../../data/charts'
import ChartCanvas from '../../components/charts/ChartCanvas.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatTile from '../../components/ui/StatTile.vue'

const counts = ref({})
const chartData = ref(null)

onMounted(async () => {
  const [s, c] = await Promise.all([adminApi.stats(), adminApi.charts()])
  counts.value = s.data
  chartData.value = c.data
})
</script>

<template>
  <div class="motion-fade-up">
    <PageHeader title="Placement overview" subtitle="Institute-wide snapshot" />

    <div class="row g-3 mb-3">
      <div class="col-6 col-lg-3"><StatTile label="Students" :value="counts.students ?? 0" icon="users" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Companies" :value="counts.companies ?? 0" icon="building" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Drives" :value="counts.drives ?? 0" icon="briefcase" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Applications" :value="counts.applications ?? 0" icon="file" /></div>
    </div>
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3"><StatTile label="Placements" :value="counts.placements ?? 0" icon="award" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Pending companies" :value="counts.pending_companies ?? 0" icon="building" /></div>
      <div class="col-6 col-lg-3"><StatTile label="Pending drives" :value="counts.pending_drives ?? 0" icon="briefcase" /></div>
    </div>

    <div v-if="chartData" class="row g-3">
      <div class="col-lg-6">
        <div class="surface-card p-3 h-100">
          <h2 class="h6 mb-3">Applications by status</h2>
          <ChartCanvas type="doughnut" :data="toChartData(chartData.applications_by_status)" />
        </div>
      </div>
      <div class="col-lg-6">
        <div class="surface-card p-3 h-100">
          <h2 class="h6 mb-3">Students by branch</h2>
          <ChartCanvas type="bar" :data="toChartData(chartData.students_by_branch, 'Students')" />
        </div>
      </div>
    </div>
  </div>
</template>
