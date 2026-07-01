<script setup>
import FormField from './FormField.vue'
import { BRANCHES, GRAD_YEARS } from '../../data/options'

defineProps({ form: { type: Object, required: true } })
</script>

<template>
  <div class="row gx-2">
    <div class="col-12"><FormField id="name" v-model="form.name" label="Full name" required /></div>
    <div class="col-sm-6"><FormField id="roll" v-model="form.roll_no" label="Roll number" required /></div>
    <div class="col-sm-6">
      <FormField id="branch" v-model="form.branch" label="Branch" type="select" :options="BRANCHES" required />
    </div>
    <div class="col-sm-6"><FormField id="degree" v-model="form.degree" label="Degree" placeholder="B.Tech" /></div>
    <div class="col-6 col-sm-3"><FormField id="cgpa" v-model="form.cgpa" label="CGPA" type="number" min="0" step="0.01" /></div>
    <div class="col-6 col-sm-3">
      <FormField id="gy" v-model="form.grad_year" label="Grad year" type="select" :options="GRAD_YEARS" required />
    </div>
    <div class="col-sm-6"><FormField id="phone" v-model="form.phone" label="Phone" /></div>
    <div class="col-sm-6">
      <FormField id="skills" v-model="form.skills" label="Skills" placeholder="Python, SQL" hint="Comma separated" />
    </div>
    <div class="col-12">
      <FormField id="exp" v-model="form.experience" label="Experience" type="textarea" placeholder="Internships, projects..." />
    </div>
  </div>
</template>
