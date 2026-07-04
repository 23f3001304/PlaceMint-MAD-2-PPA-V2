<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import * as studentApi from '../api/endpoints/student'
import { authState, setProfile } from '../store/auth'
import { useAsync } from '../composables/useAsync'
import { toastError, toastSuccess } from '../store/ui'
import FormField from '../components/forms/FormField.vue'

const { run } = useAsync()
const router = useRouter()
const form = reactive({ degree: '', cgpa: '', phone: '', skills: '', experience: '' })
const uploading = ref(false)
const hasResume = ref(false)

onMounted(() => {
  const p = authState.profile
  if (p) {
    Object.assign(form, {
      degree: p.degree || '', cgpa: p.cgpa || '', phone: p.phone || '',
      skills: (p.skills || []).join(', '), experience: p.experience || '',
    })
    hasResume.value = p.has_resume
  }
})

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
  toastSuccess('Profile complete')
  router.push('/student')
}
</script>

<template>
  <div class="onb silk-bg">
    <div class="onb-card motion-fade-up">
      <div class="brand-mark fs-4 mb-1">PlaceMint</div>
      <h1 class="h3 mb-1">Complete your profile</h1>
      <p class="text-muted mb-4">Add your academic details and skills so companies can find you, then start applying.</p>

      <form novalidate @submit.prevent="finish">
        <div class="row gx-3">
          <div class="col-sm-6"><FormField id="odeg" v-model="form.degree" label="Degree" placeholder="B.Tech" /></div>
          <div class="col-6 col-sm-3"><FormField id="ocgpa" v-model="form.cgpa" label="CGPA" type="number" step="0.01" /></div>
          <div class="col-6 col-sm-3"><FormField id="ophone" v-model="form.phone" label="Phone" /></div>
          <div class="col-12"><FormField id="oskills" v-model="form.skills" label="Skills" hint="Comma separated" placeholder="Python, SQL" /></div>
          <div class="col-12"><FormField id="oexp" v-model="form.experience" label="Experience" type="textarea" placeholder="Internships, projects, prior work..." /></div>
        </div>

        <div class="upload-zone my-3">
          <label class="btn btn-outline-secondary mb-0">
            {{ uploading ? 'Uploading...' : (hasResume ? 'Replace resume' : 'Upload resume') }}
            <input type="file" accept=".pdf,.doc,.docx" hidden @change="onResume" />
          </label>
          <span v-if="hasResume" class="text-success small ms-2">Resume uploaded</span>
          <div class="small text-muted mt-2">Optional. PDF or Word, up to 5 MB.</div>
        </div>

        <div class="d-flex gap-2 mt-2 align-items-center">
          <button class="btn btn-3d-accent">Finish and continue</button>
          <button type="button" class="btn btn-link text-muted" @click="finish">Skip for now</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.onb { min-height: 100vh; display: grid; place-items: center; padding: 2rem 1rem; }
.onb-card {
  width: 100%; max-width: 640px; background: var(--ppa-surface); border: 1px solid var(--ppa-border);
  border-radius: 1rem; padding: 2rem clamp(1.5rem, 3vw, 2.5rem); box-shadow: 0 18px 50px rgba(20, 17, 15, 0.08);
}
.upload-zone { border: 1.5px dashed var(--ppa-border); border-radius: 0.75rem; padding: 1rem 1.25rem; text-align: center; background: var(--ppa-surface-sunk); }
</style>
