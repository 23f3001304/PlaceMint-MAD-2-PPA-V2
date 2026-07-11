<script setup>
import FormField from '../FormField.vue'
import { BRANCHES, GRAD_YEARS } from '../../../data/options'

defineProps({ form: { type: Object, required: true } })
</script>

<template>
  <!-- Registration stays light; CGPA, skills, experience and resume are
       collected in the post-login onboarding step. -->
  <div class="row gx-2">
    <div class="col-12"><FormField id="name" v-model="form.name" label="Full name" placeholder="Your full name" required /></div>
    <div class="col-sm-6"><FormField id="roll" v-model="form.roll_no" label="Roll number" placeholder="e.g. 23f3001304" required /></div>
    <div class="col-sm-6">
      <FormField id="branch" v-model="form.branch" label="Branch" type="select" :options="BRANCHES" required />
    </div>
    <div class="col-sm-6">
      <FormField id="gy" v-model="form.grad_year" label="Graduation year" type="select" :options="GRAD_YEARS" required />
    </div>
  </div>
</template>
