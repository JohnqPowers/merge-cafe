/* Noa's Bean Trail – Service Worker (nur Web-Version): Netz zuerst, damit neue Versionen sofort ankommen.
   Der Cache dient nur als Offline-Reserve. Ändert sich dieser Name, werden alte Caches beim Aktivieren gelöscht. */
const C = 'mergecafe-v3';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(C).then(c => Promise.all(SHELL.map(u => c.add(new Request(u, { cache: 'reload' }))))).catch(() => {}));
  self.skipWaiting();
});
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(k => Promise.all(k.filter(x => x !== C).map(x => caches.delete(x)))).then(() => self.clients.claim())
));
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;           // Fremdes (Schriften, Werbung) fasst der Worker nicht an
  const fresh = r.mode === 'navigate' || /(\.html|\.webmanifest|\/)$/.test(u.pathname);
  e.respondWith(
    fetch(r, fresh ? { cache: 'no-cache' } : undefined)
      .then(res => { if (res.ok) { const c = res.clone(); caches.open(C).then(ch => ch.put(r, c)).catch(() => {}); } return res; })
      .catch(() => caches.match(r, { ignoreSearch: true }).then(m => m || (r.mode === 'navigate' ? caches.match('index.html') : null)).then(m => m || Response.error()))
  );
});
