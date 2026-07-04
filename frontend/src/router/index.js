import { createRouter, createWebHistory } from 'vue-router'

import { installGuards } from './guards'

const AppShell = () => import('../components/layout/AppShell.vue')

const routes = [
  { path: '/', name: 'landing', component: () => import('../views/PublicLanding.vue'), meta: { public: true } },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { public: true, guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { public: true, guestOnly: true },
  },
  {
    path: '/admin',
    component: AppShell,
    meta: { roles: ['admin'] },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('../views/admin/AdminDashboard.vue') },
      { path: 'companies', name: 'admin-companies', component: () => import('../views/admin/AdminCompanies.vue') },
      { path: 'students', name: 'admin-students', component: () => import('../views/admin/AdminStudents.vue') },
      { path: 'drives', name: 'admin-drives', component: () => import('../views/admin/AdminDrives.vue') },
    ],
  },
  {
    path: '/company',
    component: AppShell,
    meta: { roles: ['company'] },
    children: [
      { path: '', name: 'company-dashboard', component: () => import('../views/company/CompanyDashboard.vue') },
      { path: 'drives', name: 'company-drives', component: () => import('../views/company/CompanyDrives.vue') },
      { path: 'applicants', name: 'company-applicants', component: () => import('../views/company/CompanyApplicants.vue') },
      { path: 'profile', name: 'company-profile', component: () => import('../views/company/CompanyProfile.vue') },
      { path: 'ats', name: 'company-ats', component: () => import('../views/ResumeScreener.vue') },
    ],
  },
  {
    path: '/student',
    component: AppShell,
    meta: { roles: ['student'] },
    children: [
      { path: '', name: 'student-dashboard', component: () => import('../views/student/StudentDashboard.vue') },
      { path: 'drives', name: 'student-drives', component: () => import('../views/student/StudentDrives.vue') },
      { path: 'applications', name: 'student-applications', component: () => import('../views/student/StudentApplications.vue') },
      { path: 'profile', name: 'student-profile', component: () => import('../views/student/StudentProfile.vue') },
      { path: 'ats', name: 'student-ats', component: () => import('../views/ResumeScreener.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })
installGuards(router)

export default router
