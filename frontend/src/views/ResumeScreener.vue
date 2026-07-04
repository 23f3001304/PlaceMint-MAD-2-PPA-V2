<script setup>
import { computed, ref } from 'vue'

import PageHeader from '../components/layout/PageHeader.vue'

const resume = ref('')
const jd = ref('')
const result = ref(null)

const STOP = new Set(
  ('a an the and or of to in for with on at by is are be as we you your our their they this that from will'
    + ' can into using use experience work team role job skills strong etc across able about have has plus'
    + ' need needs knowledge familiar good prior looking seeking who want years year must should')
    .split(' '),
)

function keywords(text) {
  const words = (text.toLowerCase().match(/[a-z][a-z+.#]*/g) || []).map((w) => w.replace(/\.+$/, ''))
  return [...new Set(words)].filter((w) => w.length > 2 && !STOP.has(w))
}

function screen() {
  const wanted = keywords(jd.value)
  const haystack = resume.value.toLowerCase()
  const matched = wanted.filter((k) => haystack.includes(k))
  const missing = wanted.filter((k) => !haystack.includes(k))
  const score = wanted.length ? Math.round((matched.length / wanted.length) * 100) : 0
  result.value = { score, matched, missing, total: wanted.length }
}

const scoreColor = computed(() => {
  const s = result.value?.score ?? 0
  return s >= 70 ? '#1f6b3a' : s >= 40 ? '#c98a1a' : '#b0432b'
})
</script>

<template>
  <div class="motion-fade-up" style="max-width: 940px">
    <PageHeader title="Resume screener" subtitle="Paste a resume and a job description to see the keyword match (ATS-style)" />

    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label fw-semibold small">Resume text</label>
        <textarea v-model="resume" class="form-control" rows="12" placeholder="Paste the resume text here..."></textarea>
      </div>
      <div class="col-md-6">
        <label class="form-label fw-semibold small">Job description / required skills</label>
        <textarea v-model="jd" class="form-control" rows="12" placeholder="Paste the job description or list the required skills..."></textarea>
      </div>
    </div>
    <button class="btn btn-3d-accent mt-3" :disabled="!resume || !jd" @click="screen">Screen resume</button>

    <div v-if="result" class="surface-card p-4 mt-4">
      <div class="d-flex align-items-center gap-3 mb-3">
        <div class="score-ring" :style="{ '--c': scoreColor }"><span>{{ result.score }}%</span></div>
        <div>
          <div class="fw-semibold">{{ result.matched.length }} of {{ result.total }} keywords matched</div>
          <div class="text-muted small">A higher score means a closer fit to the role.</div>
        </div>
      </div>
      <h3 class="h6">Matched keywords</h3>
      <div class="mb-3">
        <span v-for="k in result.matched" :key="k" class="status-badge st-approved me-1 mb-1 d-inline-block">{{ k }}</span>
        <span v-if="!result.matched.length" class="text-muted small">None</span>
      </div>
      <h3 class="h6">Missing keywords</h3>
      <div>
        <span v-for="k in result.missing" :key="k" class="status-badge st-rejected me-1 mb-1 d-inline-block">{{ k }}</span>
        <span v-if="!result.missing.length" class="text-muted small">None</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.score-ring {
  width: 72px; height: 72px; border-radius: 50%; display: grid; place-items: center;
  font-weight: 800; color: #fff; background: var(--c); font-family: var(--ppa-font-display);
}
</style>
