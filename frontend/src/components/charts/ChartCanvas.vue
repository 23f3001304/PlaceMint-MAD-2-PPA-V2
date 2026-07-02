<script setup>
import { Chart, registerables } from 'chart.js'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

Chart.register(...registerables)

const props = defineProps({
  type: { type: String, default: 'bar' },
  data: { type: Object, required: true },
  options: Object,
})

const el = ref(null)
let chart = null

function baseOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12 } } },
  }
}

function render() {
  if (chart) chart.destroy()
  if (!el.value) return
  chart = new Chart(el.value, {
    type: props.type,
    data: props.data,
    options: props.options || baseOptions(),
  })
}

onMounted(render)
watch(() => props.data, render, { deep: true })
onBeforeUnmount(() => chart && chart.destroy())
</script>

<template>
  <div class="chart-wrap"><canvas ref="el"></canvas></div>
</template>

<style scoped>
.chart-wrap { position: relative; height: 260px; }
</style>
