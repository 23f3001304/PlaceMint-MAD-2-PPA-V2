<script setup>
// Multi-step profile wizard, used both for first-time onboarding and for the
// full "Edit profile" flow (?edit=1) so the two stay identical.
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import * as studentApi from '../api/endpoints/student'
import { authState, setProfile } from '../store/auth'
import { useAsync } from '../composables/useAsync'
import { toastError, toastSuccess } from '../store/ui'
import FormField from '../components/forms/FormField.vue'
import LinksEditor from '../components/forms/LinksEditor.vue'
import ExperienceEditor from '../components/inputs/ExperienceEditor.vue'
import { BRANCHES, GRAD_YEARS } from '../data/options'

const { run } = useAsync()
const router = useRouter()
const route = useRoute()
const editing = computed(() => !!route.query.edit)

const STEPS = ['Basics', 'Skills', 'Experience', 'Links', 'Resume']
const step = ref(0)
const isLast = computed(() => step.value === STEPS.length - 1)

const form = reactive({
  name: '', branch: '', degree: '', cgpa: '', grad_year: '', phone: '',
  skills: '', experiences: [], links: [],
})
const uploading = ref(false)
const hasResume = ref(false)

onMounted(() => {
  const p = authState.profile
  if (!p) return
  Object.assign(form, {
    name: p.name || '', branch: p.branch || '', degree: p.degree || '', cgpa: p.cgpa || '',
    grad_year: p.grad_year || '', phone: p.phone || '',
    skills: (p.skills || []).join(', '),
    experiences: (p.experiences || []).map((x) => ({ ...x })),
    links: (p.links || []).map((l) => ({ ...l })),
  })
  hasResume.value = p.has_resume
})

function next() { if (step.value < STEPS.length - 1) step.value++ }
function back() { if (step.value > 0) step.value-- }

async function onResume(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('resume', file)
    const { data } = await studentApi.uploadResume(fd)
    hasResume.value = data.has_resume
    setProfile(data)
    toastSuccess('Resume uploaded')
  } catch (err) {
    toastError(err.message)
  } finally {
    uploading.value = false
  }
}

async function finish() {
  const p = (await run(() => studentApi.updateProfile({ ...form, onboarded: true }))).data
  setProfile(p)
  toastSuccess(editing.value ? 'Profile updated' : 'Profile saved')
  router.push(editing.value ? '/student/profile' : '/student')
}
function cancelOrSkip() {
  if (editing.value) router.push('/student/profile')
  else finish()
}
</script>

<template>
  <div class="onb silk-bg">
    <div class="onb-card motion-fade-up">
      <div class="brand-mark fs-4 mb-1">PlaceMint</div>
      <h1 class="h4 mb-1">{{ editing ? 'Edit your profile' : 'Set up your profile' }}</h1>
      <p class="text-muted mb-4">A complete profile unlocks drive eligibility and helps companies find you.</p>

      <ol class="stepper mb-4">
        <li v-for="(s, i) in STEPS" :key="s" class="step" :class="{ done: i < step, active: i === step }">
          <span class="dot">{{ i < step ? '✓' : i + 1 }}</span>
          <span class="lbl">{{ s }}</span>
        </li>
      </ol>

      <div v-show="step === 0" class="row gx-3">
        <div class="col-12"><FormField id="oname" v-model="form.name" label="Full name" required /></div>
        <div class="col-md-6"><FormField id="obranch" v-model="form.branch" label="Branch" type="select" :options="BRANCHES" /></div>
        <div class="col-md-6"><FormField id="odeg" v-model="form.degree" label="Degree" placeholder="B.Tech" /></div>
        <div class="col-6"><FormField id="ocgpa" v-model="form.cgpa" label="CGPA" type="number" step="0.01" min="0" max="10" hint="Out of 10, checks eligibility" /></div>
        <div class="col-6"><FormField id="ogy" v-model="form.grad_year" label="Grad year" type="select" :options="GRAD_YEARS" /></div>
        <div class="col-12">
          <FormField
            id="ophone" v-model="form.phone" label="Phone" type="tel" inputmode="tel"
            placeholder="10-digit mobile" pattern="(\+91[- ]?)?[6-9]\d{9}"
            title="Enter a valid Indian mobile number (10 digits starting 6-9)"
          />
        </div>
      </div>
      <div v-show="step === 1">
        <FormField id="oskills" v-model="form.skills" label="Your skills" type="textarea" hint="Comma separated" placeholder="Python, SQL, React, Machine Learning" />
      </div>
      <div v-show="step === 2">
        <label class="form-label">Experience <span class="text-muted small">(internships, projects, roles)</span></label>
        <ExperienceEditor v-model="form.experiences" :max="6" />
      </div>
      <div v-show="step === 3">
        <label class="form-label">Links <span class="text-muted small">(portfolio, LinkedIn, X, GitHub)</span></label>
        <LinksEditor v-model="form.links" :max="3" />
      </div>
      <div v-show="step === 4" class="upload-zone">
        <label class="btn btn-outline-secondary mb-0">
          {{ uploading ? 'Uploading...' : (hasResume ? 'Replace resume' : 'Upload resume') }}
          <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
        </label>
        <span v-if="hasResume" class="text-success small ms-2">Uploaded</span>
        <div class="small text-muted mt-2">Optional. PDF or Word, up to 5 MB.</div>
      </div>

      <div class="d-flex justify-content-between align-items-center mt-4">
        <button class="btn btn-link text-muted p-0" :disabled="step === 0" @click="back">Back</button>
        <div class="d-flex gap-3 align-items-center">
          <button class="btn btn-link text-muted p-0" @click="cancelOrSkip">{{ editing ? 'Cancel' : 'Skip for now' }}</button>
          <button v-if="!isLast" class="btn btn-3d-accent px-4" @click="next">Continue</button>
          <button v-else class="btn btn-3d-accent px-4" @click="finish">{{ editing ? 'Save' : 'Finish' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.onb { min-height: 100vh; display: grid; place-items: center; padding: 2rem 1rem; }
.onb-card {
  width: 100%; max-width: 620px; background: var(--ppa-surface); border: 1px solid var(--ppa-border);
  border-radius: 1rem; padding: 2rem clamp(1.5rem, 3vw, 2.5rem); box-shadow: 0 18px 50px rgba(20, 17, 15, 0.08);
}
.stepper { list-style: none; display: flex; gap: 0.5rem; padding: 0; margin: 0; }
.step { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 0.35rem; position: relative; }
.step + .step::before {
  content: ''; position: absolute; top: 13px; left: -50%; width: 100%; height: 2px; background: var(--ppa-border);
}
.step.done + .step::before, .step.active::before { background: var(--ppa-accent); }
.dot {
  width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; font-size: 0.85rem;
  font-weight: 700; background: var(--ppa-surface-sunk); color: var(--ppa-muted); border: 1px solid var(--ppa-border); z-index: 1;
}
.step.active .dot { background: var(--ppa-accent); color: #fff; border-color: var(--ppa-accent); }
.step.done .dot { background: #d6ecdd; color: #1f6b3a; border-color: #a9d7b8; }
.lbl { font-size: 0.75rem; color: var(--ppa-muted); }
.step.active .lbl { color: var(--ppa-ink); font-weight: 600; }
.upload-zone { border: 1.5px dashed var(--ppa-border); border-radius: 0.75rem; padding: 1.25rem; text-align: center; background: var(--ppa-surface-sunk); }
</style>
