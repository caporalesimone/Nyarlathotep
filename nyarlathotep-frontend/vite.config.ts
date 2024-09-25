import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

/*
export default defineConfig({
	plugins: [sveltekit()]
});
*/

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/workstations_status': {
        target: 'http://localhost:8080/workstations_status',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/workstations_status/, '')
      }
    }
  }
});