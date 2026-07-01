import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Dev server proxies /api to Flask so the SPA and API share an origin (no CORS).
// Production build lands in dist/, which Flask serves directly.
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:5000',
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Bootstrap 5.3 still ships @import-based Sass; silence the Dart Sass
        // deprecation noise until Bootstrap 6 moves to the module system.
        quietDeps: true,
        silenceDeprecations: ['import', 'global-builtin', 'color-functions', 'mixed-decls'],
      },
    },
  },
})
