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
const verdict = computed(() => {
  const s = result.value?.score ?? 0
  return s >= 70 ? 'Strong match' : s >= 40 ? 'Partial match' : 'Needs work'
})
</script>

<template>
  <div class="motion-fade-up" style="max-width: 960px">
    <PageHeader title="Resume screener" subtitle="ATS-style keyword match between a resume and a job description" />

    <div class="row g-3">
      <div class="col-md-6">
        <div class="surface-card p-3 h-100">
          <label class="form-label fw-semibold small mb-2">Resume text</label>
          <textarea v-model="resume" class="form-control screener-input" placeholder="Paste the resume text here..."></textarea>
        </div>
      </div>
      <div class="col-md-6">
        <div class="surface-card p-3 h-100">
          <label class="form-label fw-semibold small mb-2">Job description / required skills</label>
          <textarea v-model="jd" class="form-control screener-input" placeholder="Paste the job description or list the required skills..."></textarea>
        </div>
      </div>
    </div>
    <button class="btn btn-3d-accent mt-3 px-4" :disabled="!resume || !jd" @click="screen">Screen resume</button>

    <div v-if="result" class="result-card surface-card mt-4 motion-fade-up">
      <div class="result-head">
        <div class="score-ring" :style="{ '--pct': result.score, '--c': scoreColor }">
          <span class="score-num">{{ result.score }}<small>%</small></span>
        </div>
        <div class="flex-grow-1">
          <div class="h5 mb-1">{{ verdict }}</div>
          <div class="text-muted small mb-2">{{ result.matched.length }} of {{ result.total }} keywords found in the resume.</div>
          <div class="match-bar"><span :style="{ width: result.score + '%', background: scoreColor }"></span></div>
        </div>
      </div>

      <div class="row g-4 mt-1">
        <div class="col-md-6">
          <h3 class="h6 kw-head"><span class="dot ok"></span> Matched ({{ result.matched.length }})</h3>
          <div class="kw-wrap">
            <span v-for="k in result.matched" :key="k" class="kw kw-ok">{{ k }}</span>
            <span v-if="!result.matched.length" class="text-muted small">None</span>
          </div>
        </div>
        <div class="col-md-6">
          <h3 class="h6 kw-head"><span class="dot no"></span> Missing ({{ result.missing.length }})</h3>
          <div class="kw-wrap">
            <span v-for="k in result.missing" :key="k" class="kw kw-no">{{ k }}</span>
            <span v-if="!result.missing.length" class="text-muted small">None</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.screener-input { border: 0; resize: vertical; min-height: 240px; background: transparent; padding: 0; }
.screener-input:focus { box-shadow: none; }
.result-card { padding: 1.5rem; }
.result-head { display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap; }
.score-ring {
  --pct: 0; width: 108px; height: 108px; border-radius: 50%; display: grid; place-items: center; flex-shrink: 0;
  position: relative; background: conic-gradient(var(--c) calc(var(--pct) * 1%), var(--ppa-surface-sunk) 0);
  transition: background 0.8s ease;
}
.score-ring::before { content: ''; position: absolute; inset: 10px; background: var(--ppa-surface); border-radius: 50%; }
.score-num { position: relative; font-family: var(--ppa-font-display); font-weight: 800; font-size: 1.8rem; }
.score-num small { font-size: 0.9rem; font-weight: 600; }
.match-bar { height: 8px; background: var(--ppa-surface-sunk); border-radius: 999px; overflow: hidden; max-width: 340px; }
.match-bar span { display: block; height: 100%; border-radius: 999px; transition: width 0.8s ease; }
.kw-head { display: flex; align-items: center; gap: 0.5rem; }
.dot { width: 9px; height: 9px; border-radius: 50%; }
.dot.ok { background: #1f6b3a; }
.dot.no { background: #b0432b; }
.kw-wrap { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.kw { font-size: 0.78rem; font-weight: 600; padding: 0.25rem 0.6rem; border-radius: 999px; }
.kw-ok { background: #d6ecdd; color: #1f6b3a; }
.kw-no { background: #f2d8cf; color: #94371f; }
</style>
