import { createRouter, createWebHistory } from 'vue-router'

import { authState } from '../store/auth'
import { homeFor, installGuards } from './guards'

const AppShell = () => import('../components/layout/AppShell.vue')

const routes = [
  { path: '/', redirect: () => (authState.user ? homeFor(authState.user.role) : '/login') },
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
    ],
  },
  {
    path: '/company',
    component: AppShell,
    meta: { roles: ['company'] },
    children: [
      { path: '', name: 'company-dashboard', component: () => import('../views/company/CompanyDashboard.vue') },
    ],
  },
  {
    path: '/student',
    component: AppShell,
    meta: { roles: ['student'] },
    children: [
      { path: '', name: 'student-dashboard', component: () => import('../views/student/StudentDashboard.vue') },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({ history: createWebHistory(), routes })
installGuards(router)

export default router
