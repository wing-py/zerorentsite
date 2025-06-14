import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  build:{
    outDir:'../mysite/vue-build',
    // assetsDir:'.',
    // rollupOptions:{
    //   output:{
    //     entryFileNames:'[name].js',
    //     chunkFileNames:'[name].js',
    //     assetFileNames:'[name].[ext]'
    //   }
    // }
  },
  base:'./',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/apis': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/apis/, '')
      }
    }
  }
})
