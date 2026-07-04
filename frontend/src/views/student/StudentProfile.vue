<script setup>
import { onMounted, reactive, ref } from 'vue'

import * as studentApi from '../../api/endpoints/student'
import { openDoc } from '../../api/client'
import { authState, setProfile } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastError, toastSuccess } from '../../store/ui'
import FormField from '../../components/forms/FormField.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import { BRANCHES, GRAD_YEARS } from '../../data/options'

const { run } = useAsync()
const form = reactive({ name: '', branch: '', degree: '', cgpa: '', grad_year: '', phone: '', skills: '', experience: '' })
const rollNo = ref('')
const hasResume = ref(false)
const uploading = ref(false)

onMounted(async () => {
  const p = (await run(studentApi.profile)).data
  Object.assign(form, {
    name: p.name, branch: p.branch, degree: p.degree, cgpa: p.cgpa,
    grad_year: p.grad_year, phone: p.phone, skills: (p.skills || []).join(', '), experience: p.experience,
  })
  rollNo.value = p.roll_no
  hasResume.value = p.has_resume
})

async function save() {
  const p = (await run(() => studentApi.updateProfile({ ...form }))).data
  setProfile(p)
  toastSuccess('Profile saved')
}
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
function viewResume() { openDoc(`/documents/resume/${authState.profile.id}`) }
</script>

<template>
  <div class="motion-fade-up" style="max-width: 780px">
    <PageHeader title="My profile" subtitle="Keep your details and resume current" />

    <div class="surface-card p-4 mb-3">
      <form novalidate @submit.prevent="save">
        <div class="row gx-3">
          <div class="col-md-8"><FormField id="pname" v-model="form.name" label="Full name" required /></div>
          <div class="col-md-4 mb-3">
            <label class="form-label fw-semibold small">Roll number</label>
            <input class="form-control" :value="rollNo" disabled />
          </div>
          <div class="col-md-4"><FormField id="pbranch" v-model="form.branch" label="Branch" type="select" :options="BRANCHES" /></div>
          <div class="col-md-4"><FormField id="pdeg" v-model="form.degree" label="Degree" /></div>
          <div class="col-6 col-md-2"><FormField id="pcgpa" v-model="form.cgpa" label="CGPA" type="number" step="0.01" /></div>
          <div class="col-6 col-md-2"><FormField id="pgy" v-model="form.grad_year" label="Grad year" type="select" :options="GRAD_YEARS" /></div>
          <div class="col-md-6"><FormField id="pphone" v-model="form.phone" label="Phone" /></div>
          <div class="col-md-6"><FormField id="pskills" v-model="form.skills" label="Skills" hint="Comma separated" /></div>
          <div class="col-12"><FormField id="pexp" v-model="form.experience" label="Experience" type="textarea" /></div>
        </div>
        <button class="btn btn-3d-accent mt-2">Save changes</button>
      </form>
    </div>

    <div class="surface-card p-4">
      <h2 class="h6 mb-2">Resume</h2>
      <div class="d-flex align-items-center gap-3 flex-wrap">
        <label class="btn btn-outline-secondary mb-0">
          {{ uploading ? 'Uploading...' : 'Upload resume' }}
          <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
        </label>
        <button v-if="hasResume" class="btn btn-outline-secondary" @click="viewResume">View current</button>
        <span v-else class="text-muted small">No resume uploaded yet.</span>
      </div>
    </div>
  </div>
</template>
