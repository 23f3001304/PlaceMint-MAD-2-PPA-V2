// Route guard: enforces authentication and role, and keeps signed-in users out
// of the login/register pages.
import { authState } from '../store/auth'

export const HOME_BY_ROLE = {
  admin: '/admin',
  company: '/company',
  student: '/student',
}

export function homeFor(role) {
  return HOME_BY_ROLE[role] || '/login'
}

export function installGuards(router) {
  router.beforeEach((to) => {
    const isAuth = !!authState.token && !!authState.user
    const role = authState.user?.role

    if (to.meta.guestOnly && isAuth) return homeFor(role)
    if (to.meta.public) return true
    if (!isAuth) return { path: '/login', query: { redirect: to.fullPath } }
    if (to.meta.roles && !to.meta.roles.includes(role)) return homeFor(role)
    return true
  })
}
