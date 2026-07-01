<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { login } from '../../store/auth'
import { homeFor } from '../../router/guards'
import { toastError } from '../../store/ui'
import AuthLayout from './AuthLayout.vue'
import FormField from '../../components/forms/FormField.vue'

const form = reactive({ email: '', password: '' })
const busy = ref(false)
const route = useRoute()
const router = useRouter()

async function submit() {
  if (busy.value) return
  busy.value = true
  try {
    const user = await login(form.email.trim(), form.password)
    router.push(route.query.redirect || homeFor(user.role))
  } catch (e) {
    toastError(e.message)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <AuthLayout title="Welcome back" subtitle="Sign in to your placement dashboard.">
    <form novalidate @submit.prevent="submit">
      <FormField
        id="email" v-model="form.email" label="Email" type="email"
        placeholder="you@college.edu" required autocomplete="email"
      />
      <FormField
        id="password" v-model="form.password" label="Password" type="password"
        placeholder="Your password" required autocomplete="current-password"
      />
      <button class="btn btn-3d-accent w-100 py-2 mt-2" :disabled="busy">
        {{ busy ? 'Signing in...' : 'Sign in' }}
      </button>
    </form>

    <p class="text-center text-muted small mt-4 mb-0">
      New here? <RouterLink to="/register">Create an account</RouterLink>
    </p>
    <p class="text-center text-muted small mt-2 mb-0 text-mono">
      demo admin: admin@ppa.local / admin123
    </p>
  </AuthLayout>
</template>
