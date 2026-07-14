<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { authState, logout } from '../../store/auth'
import { avatarTint } from '../../data/avatar'
import Icon from '../Icon.vue'

defineEmits(['toggle'])

const router = useRouter()
const open = ref(false)
const root = ref(null)

const name = computed(
  () => authState.profile?.name || authState.profile?.company_name || authState.user?.email || 'Account',
)
const role = computed(() => authState.user?.role || '')
const roleLabel = computed(() => role.value.charAt(0).toUpperCase() + role.value.slice(1))
const initial = computed(() => (name.value[0] || 'U').toUpperCase())

// Company chips mirror the profile avatar: uploaded logo, then logo URL, then a
// deterministic brand-tile colour behind the initial.
const logoSrc = computed(() => {
  const p = authState.profile
  if (!p) return ''
  if (role.value === 'company') return p.has_logo ? `/api/documents/logo/${p.id}` : p.logo_url || ''
  if (role.value === 'student') return p.has_photo ? `/api/documents/photo/${p.id}` : p.photo_url || ''
  return ''
})
const tint = computed(() =>
  (role.value === 'company' && authState.profile ? avatarTint(authState.profile.company_name) : ''),
)

function onDocClick(e) {
  if (root.value && !root.value.contains(e.target)) open.value = false
}
onMounted(() => document.addEventListener('click', onDocClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))

function goProfile() {
  open.value = false
  router.push(`/${role.value}/profile`)
}
function signOut() {
  open.value = false
  logout()
  router.push('/login')
}
</script>

<template>
  <header class="app-navbar">
    <button class="btn btn-sm d-lg-none nav-toggle" aria-label="Open menu" @click="$emit('toggle')">
      <Icon name="dashboard" :size="20" />
    </button>
    <div class="flex-grow-1"></div>

    <div ref="root" class="user-menu">
      <button class="user-chip" @click="open = !open">
        <span class="avatar" :class="{ 'has-logo': logoSrc }" :style="!logoSrc && tint ? { background: tint } : {}">
          <img v-if="logoSrc" :src="logoSrc" alt="" class="avatar-img" :class="{ photo: role === 'student' }" />
          <template v-else>{{ initial }}</template>
        </span>
        <span class="who d-none d-sm-flex">
          <span class="who-name">{{ name }}</span>
          <span class="who-role">{{ roleLabel }}</span>
        </span>
        <Icon name="chevron" :size="14" class="chev" :class="{ up: open }" />
      </button>

      <transition name="pop">
        <div v-if="open" class="menu">
          <button v-if="role !== 'admin'" class="menu-item" @click="goProfile">
            <Icon name="user" :size="15" /> Profile
          </button>
          <button class="menu-item danger" @click="signOut">
            <Icon name="logout" :size="15" /> Sign out
          </button>
        </div>
      </transition>
    </div>
  </header>
</template>

<style scoped>
.app-navbar {
  height: 62px; padding: 0 clamp(1rem, 3vw, 2.5rem); background: var(--ppa-bg);
  border-bottom: 1px solid var(--ppa-border); position: sticky; top: 0; z-index: 1020; display: flex; align-items: center;
}
.user-menu { position: relative; }
.user-chip {
  display: flex; align-items: center; gap: 0.6rem; padding: 0.28rem 0.7rem 0.28rem 0.3rem;
  border: 1px solid var(--ppa-border); border-radius: 999px; background: var(--ppa-surface); cursor: pointer;
}
.user-chip:hover { background: var(--ppa-surface-sunk); }
.avatar {
  width: 34px; height: 34px; border-radius: 50%; color: #fff; display: grid; place-items: center; overflow: hidden;
  font-weight: 700; font-size: 0.9rem; font-family: var(--ppa-font-display);
  background: linear-gradient(180deg, var(--ppa-accent-rim), var(--ppa-accent));
}
.avatar.has-logo { background: #fff; border: 1px solid var(--ppa-border); }
.avatar-img { width: 100%; height: 100%; object-fit: contain; padding: 2px; }
.avatar-img.photo { object-fit: cover; padding: 0; }
.who { flex-direction: column; line-height: 1.12; text-align: left; }
.who-name { font-weight: 600; font-size: 0.85rem; }
.who-role { color: var(--ppa-muted); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; }
.chev { color: var(--ppa-muted); transition: transform 0.15s ease; }
.chev.up { transform: rotate(180deg); }
.menu {
  position: absolute; right: 0; top: calc(100% + 8px); min-width: 184px; background: var(--ppa-surface);
  border: 1px solid var(--ppa-border); border-radius: 0.7rem; box-shadow: 0 14px 40px rgba(20, 17, 15, 0.14); padding: 0.4rem; z-index: 1050;
}
.menu-item {
  display: flex; align-items: center; gap: 0.55rem; width: 100%; text-align: left; border: 0; background: transparent;
  padding: 0.5rem 0.6rem; border-radius: 0.5rem; font-size: 0.9rem; color: var(--ppa-ink);
}
.menu-item:hover { background: var(--ppa-surface-sunk); }
.menu-item.danger { color: var(--ppa-danger); }
.nav-toggle { border: 1px solid var(--ppa-border); margin-right: 0.5rem; }
.pop-enter-active, .pop-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.pop-enter-from, .pop-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
