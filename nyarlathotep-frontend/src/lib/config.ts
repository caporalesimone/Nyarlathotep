// Backend base URL with /api prefix for nginx routing
// Set VITE_BACKEND_URL in env for development (empty for unified container)
export const BACKEND_BASE = import.meta.env.VITE_BACKEND_URL || "";

export function apiUrl(path: string): string {
  if (!path.startsWith("/")) path = "/" + path;
  
  // Add /api prefix for unified container (nginx routing)
  if (BACKEND_BASE) {
    // Development mode with separate backend
    return `${BACKEND_BASE}${path}`;
  } else {
    // Production mode with unified container (nginx /api proxy)
    return `/api${path}`;
  }
}
