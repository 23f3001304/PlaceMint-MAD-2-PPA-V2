import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import { loadSession } from './store/auth'
import './styles/theme.scss'
import './styles/app.css'

// Restore any saved session (validate the token via /me) before the first
// route resolves, so guards see the real auth state and don't flash /login.
loadSession().finally(() => {
  createApp(App).use(router).mount('#app')
})
