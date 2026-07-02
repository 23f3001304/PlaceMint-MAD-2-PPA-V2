<script setup>
// Generic table. Each column can be custom-rendered via a `cell-<key>` slot,
// receiving { row, value }.
defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  loading: Boolean,
  empty: { type: String, default: 'Nothing here yet.' },
})
</script>

<template>
  <div class="table-responsive surface-card">
    <table class="table table-hover align-middle mb-0">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :class="col.class" class="text-muted small text-uppercase">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="columns.length" class="text-center text-muted py-4">Loading...</td>
        </tr>
        <tr v-else-if="!rows.length">
          <td :colspan="columns.length" class="text-center text-muted py-4">{{ empty }}</td>
        </tr>
        <tr v-for="(row, i) in rows" v-else :key="row.id ?? i">
          <td v-for="col in columns" :key="col.key" :class="col.class">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">{{ row[col.key] }}</slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
