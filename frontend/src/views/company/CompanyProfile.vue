<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import * as companyApi from '../../api/endpoints/company'
import { setProfile } from '../../store/auth'
import { useAsync } from '../../composables/useAsync'
import { toastError, toastSuccess } from '../../store/ui'
import AppModal from '../../components/overlays/AppModal.vue'
import CompanyFields from '../../components/forms/registration/CompanyFields.vue'
import FormField from '../../components/forms/FormField.vue'
import { avatarTint } from '../../data/avatar'
import Icon from '../../components/Icon.vue'
import LinksEditor from '../../components/forms/LinksEditor.vue'
import PeopleEditor from '../../components/inputs/PeopleEditor.vue'
import PageHeader from '../../components/layout/PageHeader.vue'
import StatusBadge from '../../components/ui/StatusBadge.vue'

const { run } = useAsync()
const profile = ref({})
const editing = ref(false)
const form = reactive({ company_name: '', industry: '', location: '', hr_contact: '', website: '', description: '', logo_url: '', links: [], people: [] })

const initial = computed(() => (profile.value.company_name || '?')[0].toUpperCase())
const logoUploading = ref(false)
const logoV = ref(0)
const logoSrc = computed(() => (profile.value.has_logo
  ? `/api/documents/logo/${profile.value.id}?v=${logoV.value}`
  : profile.value.logo_url || ''))

onMounted(async () => { profile.value = (await run(companyApi.profile)).data })

async function onLogo(e) {
  const file = e.target.files[0]
  if (!file) return
  logoUploading.value = true
  try {
    const fd = new FormData()
    fd.append('logo', file)
    const { data } = await companyApi.uploadLogo(fd)
    profile.value = data
    setProfile(data)
    logoV.value++
    toastSuccess('Logo updated')
  } catch (err) {
    toastError(err.message)
  } finally {
    logoUploading.value = false
  }
}

function openEdit() {
  const p = profile.value
  Object.assign(form, {
    company_name: p.company_name, industry: p.industry || '', location: p.location || '',
    hr_contact: p.hr_contact || '', website: p.website || '', description: p.description || '',
    logo_url: p.logo_url || '',
    links: (p.links || []).map((l) => ({ ...l })),
    people: (p.people || []).map((x) => ({ ...x })),
  })
  editing.value = true
}
async function save() {
  const p = (await run(() => companyApi.updateProfile({ ...form }))).data
  profile.value = p
  setProfile(p)
  editing.value = false
  toastSuccess('Profile updated')
}
</script>

<template>
  <div class="motion-fade-up" style="max-width: 820px">
    <PageHeader title="Company profile" subtitle="Your public details on the portal">
      <template #actions><button class="btn btn-3d-accent" @click="openEdit">Edit profile</button></template>
    </PageHeader>

    <div class="surface-card p-4 mb-3">
      <div class="d-flex align-items-center gap-3 mb-3">
        <span class="avatar-lg" :class="{ 'has-logo': logoSrc }" :style="logoSrc ? {} : { background: avatarTint(profile.company_name) }">
          <img v-if="logoSrc" :src="logoSrc" alt="" class="logo-img" />
          <template v-else>{{ initial }}</template>
        </span>
        <div>
          <h2 class="h4 mb-0">{{ profile.company_name }}</h2>
          <div class="small text-muted">{{ profile.industry || 'Industry not set' }}<span v-if="profile.location"> · {{ profile.location }}</span></div>
        </div>
        <StatusBadge v-if="profile.approval_status" :status="profile.approval_status" class="ms-auto" />
      </div>
      <dl class="row small mb-0">
        <dt class="col-4 col-sm-3 text-muted">Login email</dt><dd class="col-8 col-sm-9">{{ profile.email }}</dd>
        <dt class="col-4 col-sm-3 text-muted">HR contact</dt><dd class="col-8 col-sm-9">{{ profile.hr_contact || 'Not set' }}</dd>
        <dt class="col-4 col-sm-3 text-muted">Website</dt>
        <dd class="col-8 col-sm-9">
          <a v-if="profile.website" :href="profile.website" target="_blank" rel="noopener">{{ profile.website }}</a>
          <span v-else>Not set</span>
        </dd>
        <dt class="col-4 col-sm-3 text-muted">Drives</dt><dd class="col-8 col-sm-9">{{ profile.drive_count }}</dd>
      </dl>
      <div v-if="(profile.links || []).length" class="d-flex flex-wrap gap-2 mt-3">
        <a v-for="l in profile.links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="link-chip">
          <Icon name="link" :size="13" /> {{ l.label }}
        </a>
      </div>
    </div>

    <div v-if="(profile.people || []).length" class="surface-card p-4 mb-3">
      <h3 class="sec-head"><span class="sec-ico"><Icon name="users" :size="15" /></span>Key people</h3>
      <div class="d-flex flex-wrap gap-3">
        <div v-for="person in profile.people" :key="person.name" class="person-card">
          <span class="person-avatar">{{ (person.name || '?')[0].toUpperCase() }}</span>
          <div>
            <div class="fw-semibold">{{ person.name }}</div>
            <div class="small text-muted">{{ person.role }}</div>
            <a v-if="person.url" :href="person.url" target="_blank" rel="noopener" class="small">View profile</a>
          </div>
        </div>
      </div>
    </div>

    <div class="surface-card p-4">
      <h3 class="h6 mb-2">About</h3>
      <p class="mb-0" :class="{ 'text-muted': !profile.description }" style="white-space: pre-line">
        {{ profile.description || 'No description added yet.' }}
      </p>
    </div>

    <AppModal v-model="editing" title="Edit company profile" size="lg">
      <div class="d-flex align-items-center gap-3 mb-3">
        <span class="avatar-lg" :class="{ 'has-logo': logoSrc }" :style="logoSrc ? {} : { background: avatarTint(profile.company_name) }">
          <img v-if="logoSrc" :src="logoSrc" alt="" class="logo-img" />
          <template v-else>{{ initial }}</template>
        </span>
        <label class="btn btn-outline-secondary btn-sm mb-0">
          {{ logoUploading ? 'Uploading...' : (profile.has_logo ? 'Replace logo' : 'Upload logo') }}
          <input type="file" accept="image/png,image/jpeg,image/webp,image/svg+xml" hidden @change="onLogo" />
        </label>
      </div>
      <FormField
        id="logurl" v-model="form.logo_url" label="Logo URL" type="url"
        placeholder="https://yourcompany.com/logo.png" hint="Paste a link to your logo image, or upload a file above."
      />
      <CompanyFields :form="form" />
      <div class="mt-3">
        <label class="form-label">Links <span class="text-muted small">(website, LinkedIn, careers page) - up to 4</span></label>
        <LinksEditor v-model="form.links" :max="4" />
      </div>
      <div class="mt-3">
        <label class="form-label">Key people <span class="text-muted small">(CEO, investor, founder) - up to 2</span></label>
        <PeopleEditor v-model="form.people" :max="2" />
      </div>
      <template #footer>
        <button class="btn btn-outline-secondary" @click="editing = false">Cancel</button>
        <button class="btn btn-3d-accent" @click="save">Save changes</button>
      </template>
    </AppModal>
  </div>
</template>

<style scoped>
.avatar-lg {
  width: 56px; height: 56px; border-radius: 16px; background: var(--ppa-accent); color: #fff; overflow: hidden;
  display: grid; place-items: center; font-weight: 700; font-size: 1.4rem; font-family: var(--ppa-font-display); flex: none;
}
.avatar-lg.has-logo { background: #fff; border: 1px solid var(--ppa-border); }
.logo-img { width: 100%; height: 100%; object-fit: contain; padding: 4px; }
</style>
