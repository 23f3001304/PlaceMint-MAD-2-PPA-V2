<script setup>
// Custom select: a styled trigger + popover list that replaces the native
// <select> (whose option list can't be themed). Options are strings or
// { value, label }. Closes on outside click or Escape.
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import Icon from '../Icon.vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: 'Select...' },
  block: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue'])

const open = ref(false)
const root = ref(null)

const opts = computed(() => props.options.map((o) => (typeof o === 'object' ? o : { value: o, label: String(o) })))
const current = computed(() => opts.value.find((o) => o.value === props.modelValue))

function choose(o) { emit('update:modelValue', o.value); open.value = false }
function onDocClick(e) { if (root.value && !root.value.contains(e.target)) open.value = false }
function onKey(e) { if (e.key === 'Escape') open.value = false }

onMounted(() => { document.addEventListener('click', onDocClick); document.addEventListener('keydown', onKey) })
onBeforeUnmount(() => { document.removeEventListener('click', onDocClick); document.removeEventListener('keydown', onKey) })
</script>

<template>
  <div ref="root" class="sel" :class="{ open, block }">
    <button type="button" class="sel-btn" @click="open = !open">
      <span :class="{ 'text-muted': !current }">{{ current?.label ?? placeholder }}</span>
      <Icon name="chevron" :size="16" class="sel-caret" />
    </button>
    <ul v-if="open" class="sel-menu" role="listbox">
      <li
        v-for="o in opts" :key="o.value" role="option" :aria-selected="o.value === modelValue"
        class="sel-item" :class="{ on: o.value === modelValue }" @click="choose(o)"
      >{{ o.label }}</li>
    </ul>
  </div>
</template>

<style scoped>
.sel { position: relative; display: inline-block; }
.sel.block { display: block; }
.sel.block .sel-btn { width: 100%; min-width: 0; }
.sel-btn {
  display: inline-flex; align-items: center; justify-content: space-between; gap: 0.6rem;
  min-width: 11rem; padding: 0.55rem 0.85rem; cursor: pointer; font-weight: 500;
  background: var(--ppa-surface); color: var(--ppa-ink);
  border: 1px solid var(--ppa-border); border-radius: 0.6rem;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.sel-btn:hover { border-color: rgba(20, 17, 15, 0.26); }
.sel.open .sel-btn { border-color: var(--ppa-accent); box-shadow: 0 0 0 3px rgba(31, 107, 58, 0.16); }
.sel-caret { color: var(--ppa-muted); transition: transform 0.15s ease; }
.sel.open .sel-caret { transform: rotate(180deg); }
.sel-menu {
  position: absolute; z-index: 20; top: calc(100% + 6px); left: 0; min-width: 100%;
  margin: 0; padding: 0.3rem; list-style: none; background: var(--ppa-surface);
  border: 1px solid var(--ppa-border); border-radius: 0.6rem;
  box-shadow: 0 16px 40px -12px rgba(20, 17, 15, 0.24);
}
.sel-item { padding: 0.5rem 0.7rem; border-radius: 0.4rem; cursor: pointer; white-space: nowrap; font-weight: 500; }
.sel-item:hover { background: var(--ppa-surface-sunk); }
.sel-item.on { background: var(--ppa-accent); color: #fff; }
</style>
