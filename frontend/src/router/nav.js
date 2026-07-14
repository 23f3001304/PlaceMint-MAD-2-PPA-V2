// Sidebar navigation per role. Grows as feature routes are added per milestone.
const NAV = {
  admin: [
    { to: '/admin', label: 'Dashboard', icon: 'dashboard' },
    { to: '/admin/companies', label: 'Companies', icon: 'building' },
    { to: '/admin/students', label: 'Students', icon: 'users' },
    { to: '/admin/drives', label: 'Drives', icon: 'briefcase' },
  ],
  company: [
    { to: '/company', label: 'Dashboard', icon: 'dashboard' },
    { to: '/company/drives', label: 'Job Drives', icon: 'briefcase' },
    { to: '/company/applicants', label: 'Applicants', icon: 'users' },
    { to: '/company/profile', label: 'Company Profile', icon: 'building' },
  ],
  student: [
    { to: '/student', label: 'Dashboard', icon: 'dashboard' },
    { to: '/student/drives', label: 'Browse Drives', icon: 'briefcase' },
    { to: '/student/applications', label: 'My Applications', icon: 'file' },
    { to: '/student/profile', label: 'My Profile', icon: 'user' },
    { to: '/student/ats', label: 'Resume Screener', icon: 'chart' },
  ],
}

export function navFor(role) {
  return NAV[role] || []
}
