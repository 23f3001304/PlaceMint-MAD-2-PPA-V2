<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { register } from '../../store/auth'
import { homeFor } from '../../router/guards'
import { toastError, toastSuccess } from '../../store/ui'
import AuthLayout from './AuthLayout.vue'
import FormField from '../../components/forms/FormField.vue'
import StudentFields from '../../components/forms/StudentFields.vue'
import CompanyFields from '../../components/forms/CompanyFields.vue'

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
  <AuthLayout title="Create your account" subtitle="Register as a student or a company.">
    <div class="btn-group w-100 mb-4" role="group" aria-label="Account type">
      <button type="button" class="btn" :class="role === 'student' ? 'btn-3d-accent' : 'btn-outline-secondary'" @click="role = 'student'">
        Student
      </button>
      <button type="button" class="btn" :class="role === 'company' ? 'btn-3d-accent' : 'btn-outline-secondary'" @click="role = 'company'">
        Company
      </button>
    </div>

    <form novalidate @submit.prevent="submit">
      <FormField id="remail" v-model="form.email" label="Email" type="email" required autocomplete="email" />
      <FormField id="rpass" v-model="form.password" label="Password" type="password" hint="At least 6 characters" required autocomplete="new-password" />
      <StudentFields v-if="role === 'student'" :form="form" />
      <CompanyFields v-else :form="form" />
      <button class="btn btn-3d-accent w-100 py-2 mt-2" :disabled="busy">
        {{ busy ? 'Creating...' : 'Create account' }}
      </button>
    </form>

    <p class="text-center text-muted small mt-4 mb-0">
      Already registered? <RouterLink to="/login">Sign in</RouterLink>
    </p>
  </AuthLayout>
</template>
