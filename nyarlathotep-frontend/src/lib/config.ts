// Backend base URL. Set VITE_BACKEND_URL in env for production (e.g. http://nyarlathotep-backend:8080)
// If empty, frontend will use relative paths (works with dev proxy).
export const BACKEND_BASE = import.meta.env.VITE_BACKEND_URL || "";

export function apiUrl(path: string): string {
  if (!path.startsWith("/")) path = "/" + path;
  return BACKEND_BASE ? `${BACKEND_BASE}${path}` : path;
}
