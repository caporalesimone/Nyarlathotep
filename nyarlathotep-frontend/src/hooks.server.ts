import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Silently handle well-known requests that Chrome DevTools tries to fetch
  if (event.url.pathname.startsWith('/.well-known/')) {
    return new Response(null, { status: 200 });
  }

  return resolve(event);
};
