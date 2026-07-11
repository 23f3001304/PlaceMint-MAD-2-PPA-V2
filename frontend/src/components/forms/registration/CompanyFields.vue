<script setup>
import FormField from '../FormField.vue'
import { INDUSTRIES } from '../../../data/options'

defineProps({ form: { type: Object, required: true } })
</script>

<template>
  <div class="row gx-2">
    <div class="col-12"><FormField id="cn" v-model="form.company_name" label="Company name" placeholder="e.g. TechNova" required /></div>
    <div class="col-sm-6">
      <FormField id="ind" v-model="form.industry" label="Industry" type="select" :options="INDUSTRIES" />
    </div>
    <div class="col-sm-6"><FormField id="loc" v-model="form.location" label="Location" placeholder="e.g. Bengaluru" /></div>
    <div class="col-sm-6"><FormField id="hr" v-model="form.hr_contact" label="HR contact" placeholder="hr@company.com" /></div>
    <div class="col-sm-6"><FormField id="web" v-model="form.website" label="Website" placeholder="https://company.com" /></div>
    <div class="col-12"><FormField id="desc" v-model="form.description" label="About the company" type="textarea" placeholder="What you do, your culture, and who you hire..." /></div>
  </div>
</template>
