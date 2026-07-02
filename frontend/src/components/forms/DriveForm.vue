<script setup>
import FormField from './FormField.vue'

defineProps({ form: { type: Object, required: true } })
</script>

<template>
  <div class="row gx-3">
    <div class="col-md-7"><FormField id="dtitle" v-model="form.job_title" label="Job title" required /></div>
    <div class="col-md-5"><FormField id="dname" v-model="form.drive_name" label="Drive name" placeholder="Summer SDE 2026" /></div>
    <div class="col-12"><FormField id="ddesc" v-model="form.job_description" label="Job description" type="textarea" required /></div>
    <div class="col-md-4"><FormField id="dloc" v-model="form.location" label="Location" /></div>
    <div class="col-md-4"><FormField id="dpkg" v-model="form.package_lpa" label="Package (LPA)" type="number" min="0" step="0.1" /></div>
    <div class="col-md-4"><FormField id="dexp" v-model="form.min_experience" label="Min experience (yrs)" type="number" min="0" step="0.5" /></div>
    <div class="col-12"><FormField id="dskills" v-model="form.skills_required" label="Skills required" placeholder="Python, React" hint="Comma separated" /></div>
    <div class="col-md-6"><FormField id="dbranch" v-model="form.eligible_branches" label="Eligible branches" placeholder="CSE, ECE" hint="Comma separated" /></div>
    <div class="col-md-3"><FormField id="dcgpa" v-model="form.min_cgpa" label="Min CGPA" type="number" min="0" step="0.1" /></div>
    <div class="col-md-3"><FormField id="dyears" v-model="form.eligible_years" label="Grad years" placeholder="2026, 2027" hint="Comma separated" /></div>
    <div class="col-md-6"><FormField id="dbenefits" v-model="form.benefits" label="Benefits" /></div>
    <div class="col-md-6"><FormField id="ddeadline" v-model="form.deadline" label="Application deadline" type="date" required /></div>
  </div>
</template>
