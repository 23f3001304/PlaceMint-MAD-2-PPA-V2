<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { register } from '../../store/auth'
import { homeFor } from '../../router/guards'
import { toastError, toastSuccess } from '../../store/ui'
import AuthLayout from './AuthLayout.vue'
import FormField from '../../components/forms/FormField.vue'
import StudentFields from '../../components/forms/registration/StudentFields.vue'
import CompanyFields from '../../components/forms/registration/CompanyFields.vue'

const role = ref('student')
const busy = ref(false)
const router = useRouter()

const form = reactive({
  email: '', password: '',
  name: '', roll_no: '', branch: '', degree: '', cgpa: '', grad_year: '', phone: '', skills: '', experience: '',
  company_name: '', industry: '', location: '', hr_contact: '', website: '', description: '',
})

const STUDENT_KEYS = ['name', 'roll_no', 'branch', 'degree', 'cgpa', 'grad_year', 'phone', 'skills', 'experience']
const COMPANY_KEYS = ['company_name', 'industry', 'location', 'hr_contact', 'website', 'description']

function payloadFor(keys) {
  return keys.reduce((acc, key) => ({ ...acc, [key]: form[key] }), {})
}

async function submit() {
  if (busy.value) return
  busy.value = true
  try {
    const extras = role.value === 'student' ? payloadFor(STUDENT_KEYS) : payloadFor(COMPANY_KEYS)
    const user = await register({ role: role.value, email: form.email.trim(), password: form.password, ...extras })
    toastSuccess('Account created')
    router.push(homeFor(user.role))
  } catch (e) {
    toastError(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <AuthLayout title="Create your account" subtitle="Register as a student or a company." wide>
    <div class="role-toggle mb-4">
      <button type="button" class="role-btn" :class="{ active: role === 'student' }" @click="role = 'student'">
        Student
      </button>
      <button type="button" class="role-btn" :class="{ active: role === 'company' }" @click="role = 'company'">
        Company
      </button>
    </div>

    <form novalidate @submit.prevent="submit">
      <div class="row gx-3">
        <div class="col-md-6"><FormField id="remail" v-model="form.email" label="Email" type="email" required autocomplete="email" /></div>
        <div class="col-md-6"><FormField id="rpass" v-model="form.password" label="Password" type="password" hint="At least 6 characters" required autocomplete="new-password" /></div>
      </div>
      <Transition name="swap" mode="out-in">
        <StudentFields v-if="role === 'student'" key="student" :form="form" />
        <CompanyFields v-else key="company" :form="form" />
      </Transition>
      <button class="btn btn-3d-accent w-100 py-2 mt-2" :disabled="busy">
        {{ busy ? 'Creating...' : 'Create account' }}
      </button>
    </form>

    <p class="text-center text-muted small mt-4 mb-0">
      Already registered? <RouterLink to="/login">Sign in</RouterLink>
    </p>
  </AuthLayout>
</template>

<style scoped>
.role-toggle {
  display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem;
  background: var(--ppa-surface-sunk); padding: 0.3rem; border-radius: 999px;
}
.role-btn {
  border: 0; background: transparent; border-radius: 999px; padding: 0.5rem;
  font-weight: 600; color: var(--ppa-muted); transition: all 0.18s ease;
}
.role-btn.active { background: var(--ppa-accent); color: #fff; box-shadow: 0 2px 6px rgba(15, 70, 36, 0.3); }
.role-btn:not(.active):hover { color: var(--ppa-ink); }
</style>

