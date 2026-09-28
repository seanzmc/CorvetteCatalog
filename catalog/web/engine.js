'use strict';
// Where the form's answers come from. Served by catalog.consumer_server, the page
// calls its API. Opened from a static bundle (bundle.json beside this page), the
// release's own engine runs in this browser: a Web Worker starts Python (Pyodide)
// while the shopper chooses a model, and each call gives the same answer the
// server would. Both return {status, result} with the server's HTTP statuses.
window.catalogEngine = (() => {
  let worker, bundle, next = 0;
  const waiting = new Map();
  // Hosts may send the form page without caching rules, so a browser can keep
  // the previous page, and with it the previous release, after a switch. The
  // page published by catalog.static_site sits beside current.json (never cached
  // here); when that names another release, refresh the page and reload. The
  // host's edge cache can answer that refresh with the previous page too, so
  // the reload is retried a few times, spaced out, and the attempt budget is
  // only spent while this page is off the release current.json names.
  (async () => {
    const own = document.baseURI.match(/\/releases\/([^/]+)\/$/)?.[1];
    if (!own) return;
    try {
      const current = await (await fetch(new URL('current.json', location.href), {cache: 'no-cache'})).json();
      if (!current.folder || current.folder === own) {
        sessionStorage.removeItem('corvette-follow-attempts');  // reached it: budget back for the next switch
        return;
      }
      const attempts = Number(sessionStorage.getItem('corvette-follow-attempts')) || 0;
      if (attempts >= 3) return;  // bounded: never reload in a loop
      if (attempts) await new Promise(resolve => setTimeout(resolve, 2000));  // let the edge cache catch up
      sessionStorage.setItem('corvette-follow-attempts', attempts + 1);
      await fetch(location.href, {cache: 'reload'});
      location.reload();
    } catch {}  // unreachable pointer or storage: keep the page as it is
  })();
  const mode = (async () => {
    let response;
    try { response = await fetch('bundle.json', {cache: 'no-cache'}); } catch { return 'server'; }
    if (!response.ok) return 'server';
    bundle = await response.json();
    worker = new Worker(`engine-worker.js?v=${bundle.release_id}`, {type: 'module'});
    worker.onmessage = ({data}) => {
      const call = waiting.get(data.id); waiting.delete(data.id);
      if (data.error) call.reject(new Error(data.error)); else call.resolve(data.value);
    };
    worker.onerror = event => {
      for (const call of waiting.values()) call.reject(new Error(event.message || 'Engine failed'));
      waiting.clear();
    };
    post('start', {bundle: JSON.stringify(bundle)}).catch(() => {});  // later calls report it
    post('warm', {model: bundle.default_model}).catch(() => {});
    return 'browser';
  })();
  function post(type, message) {
    const id = ++next;
    return new Promise((resolve, reject) => { waiting.set(id, {resolve, reject}); worker.postMessage({...message, id, type}); });
  }
  // A host may already have removed the gzip layer (Content-Encoding).
  async function gunzip(response) {
    const raw = new Uint8Array(await response.arrayBuffer());
    if (raw[0] !== 0x1f || raw[1] !== 0x8b) return raw;
    return new Uint8Array(await new Response(new Blob([raw]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
  }
  async function call(path, body) {
    if (await mode === 'server') {
      const response = await fetch(path, body === undefined ? {} :
        {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
      return {status: response.status, result: await response.json()};
    }
    if (path === '/api/catalog') {
      // Version the catalog by its own digest: bundle.json (fetched no-cache)
      // lists it, so rebuilding the same release in the other dealer mode gets
      // a different cache key instead of a stale opposite-mode copy.
      const response = await fetch(`${bundle.contract}?v=${bundle.files[bundle.contract]}`);
      if (!response.ok) return {status: response.status, result: {error: 'Catalog not found'}};
      return {status: 200, result: JSON.parse(new TextDecoder().decode(await gunzip(response)))};
    }
    return post('call', {path, body: JSON.stringify(body)});
  }
  // Load a model's catalog before the shopper starts a build with it.
  async function warm(model) { if (await mode === 'browser') post('warm', {model}).catch(() => {}); }
  return {call, warm};
})();
