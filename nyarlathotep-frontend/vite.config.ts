import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

/*
export default defineConfig({
	plugins: [sveltekit()]
});
*/

// export default defineConfig({
//   plugins: [sveltekit()],
//   server: {
//     proxy: {
//       '/workstations_status': {
//         target: 'http://localhost:8080/workstations_status',
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/workstations_status/, '')
//       }
//     }
//   }
// });

// Usa NODE_ENV per determinare l'URL del backend
const backendUrl =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:8080'
    : 'http://nyarlathotep-backend:8080';

// Environment variable
console.log("Backend URL: " + backendUrl);
export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/workstations_status': {
        target: backendUrl + '/workstations_status',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/workstations_status/, '')
      },
      '/client_update': {
        target: backendUrl + '/client_update',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/client_update/, '')
      }
    }
  }
});