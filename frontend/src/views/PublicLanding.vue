<script setup>
import LandingHero from '../components/landing/LandingHero.vue'
import FeatureSection from '../components/landing/FeatureSection.vue'
import FinalCta from '../components/landing/FinalCta.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'

const FEATURES = [
  {
    eyebrow: 'Placement Cell',
    title: 'Oversight without the',
    highlight: 'spreadsheets.',
    body: 'Approve companies and drives, moderate accounts, and watch institute-wide numbers update in real time.',
    bullets: [
      'Approve or reject companies and drives',
      'Blacklist or deactivate any account',
      'Live counts and charts across the season',
    ],
    image: '/img/ui-admin.png', tint: 'tint-mint', reverse: false,
  },
  {
    eyebrow: 'Companies',
    title: 'Post, review, and',
    highlight: 'hire.',
    body: 'Register once, post drives after approval, and move applicants from shortlist to offer with feedback and interviews.',
    bullets: [
      'Post job drives with eligibility criteria',
      'Review applicants with full profiles and resumes',
      'Schedule interviews and record placements',
    ],
    image: '/img/ui-company.png', tint: 'tint-blue', reverse: true,
  },
  {
    eyebrow: 'Students',
    title: "Find drives you're",
    highlight: 'eligible for.',
    body: 'Complete a profile once, browse only the drives that fit, and apply in a click with every outcome tracked.',
    bullets: [
      'Eligibility from branch, CGPA and year',
      'One-click apply with duplicate protection',
      'Track status, interviews and offer letters',
    ],
    image: '/img/ui-student.png', tint: 'tint-cream', reverse: false,
  },
]
</script>

<template>
  <div class="landing">
    <LandingHero />
    <FeatureSection v-for="f in FEATURES" :key="f.eyebrow" v-bind="f" />
    <FinalCta />
    <LandingFooter />
  </div>
</template>

<style scoped>
.landing { background: var(--ppa-surface); }
</style>
