// A module worker (strict by default): Pyodide's module build needs one.
// Runs the release's Python engine (catalog.browser.Form) in Pyodide. Messages
// are handled one at a time; files are fetched with the release as a query so a
// cache can never mix two releases.
const ROOT = '/bundle';
let pyodide, form, bundle, started, queue = Promise.resolve();

async function fetchBytes(path) {
  const response = await fetch(`${path}?v=${bundle.release_id}`);
  if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
  return new Uint8Array(await response.arrayBuffer());
}
function write(path, data) {
  const parts = path.split('/'); let folder = ROOT;
  for (const part of parts.slice(0, -1)) { folder += '/' + part; if (!pyodide.FS.analyzePath(folder).exists) pyodide.FS.mkdir(folder); }
  pyodide.FS.writeFile(`${ROOT}/${path}`, data);
}
async function start(text) {
  bundle = JSON.parse(text);
  const base = `https://cdn.jsdelivr.net/npm/pyodide@${bundle.pyodide}/`;
  const {loadPyodide} = await import(base + 'pyodide.mjs');
  const [py, engine, manifest] = await Promise.all([
    loadPyodide({indexURL: base}),
    Promise.all(bundle.engine.map(path => fetchBytes(path).then(data => [path, data]))),
    fetchBytes(bundle.artwork_manifest)]);
  pyodide = py; pyodide.FS.mkdir(ROOT);
  write('bundle.json', text); write(bundle.artwork_manifest, manifest);
  for (const [path, data] of engine) write(path, data);
  pyodide.runPython(`import sys; sys.path.insert(0, '${ROOT}/engine')`);
  form = pyodide.pyimport('catalog.browser').Form(ROOT);
}
async function ensure(path, text) {
  const needed = form.needs(path, text);
  if (needed) write(needed, await fetchBytes(needed));
}
async function handle(message) {
  // A failed start fails every later call with its reason.
  if (message.type === 'start') return started = start(message.bundle);
  await started;
  if (message.type === 'warm') {
    const text = JSON.stringify({model: message.model});
    await ensure('/api/session', text);
    return form.load(message.model);
  }
  await ensure(message.path, message.body);
  return JSON.parse(form.call(message.path, message.body));
}
self.onmessage = ({data}) => {
  queue = queue.then(() => handle(data)).then(
    value => self.postMessage({id: data.id, value: value === undefined ? null : value}),
    error => self.postMessage({id: data.id, error: String(error.message || error)}));
};
