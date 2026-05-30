const CACHE_NAME = 'taxessaver-v1';
const STATIC_ASSETS = [
  '/static/css/output.css',
  '/static/js/htmx.min.js',
  '/static/js/alpine.min.js',
  '/offline/',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Cache-first for static assets
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then(cached => cached || fetch(request).then(res => {
        const clone = res.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        return res;
      }))
    );
    return;
  }

  // Network-first for pages — fall back to cache
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(request) || caches.match('/'))
    );
  }
});
