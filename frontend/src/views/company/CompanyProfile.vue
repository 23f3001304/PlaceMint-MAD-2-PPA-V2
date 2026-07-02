<script setup>
import { onMounted, reactive } from 'vue'

import * as companyApi from '../../api/endpoints/company'
import { setProfile } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastSuccess } from '../../store/ui'
import CompanyFields from '../../components/forms/registration/CompanyFields.vue'
import PageHeader from '../../components/layout/PageHeader.vue'

const { run } = useAsync()
const form = reactive({
  company_name: '', industry: '', location: '', hr_contact: '', website: '', description: '',
})

onMounted(async () => {
  const res = await run(companyApi.profile)
  Object.assign(form, res.data)
})

async function save() {
  const res = await run(() => companyApi.updateProfile({ ...form }))
  setProfile(res.data)
  toastSuccess('Profile saved')
}
</script>

<template>
  <div class="motion-fade-up" style="max-width: 720px">
    <PageHeader title="Company profile" subtitle="Keep your details current" />
    <div class="surface-card p-4">
      <form novalidate @submit.prevent="save">
        <CompanyFields :form="form" />
        <button class="btn btn-3d-accent mt-2">Save changes</button>
      </form>
    </div>
  </div>
</template>
