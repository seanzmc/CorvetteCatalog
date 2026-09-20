'use strict';
const $ = id => document.getElementById(id);
let models = [], current = null, pending = null, dirty = false, busy = false, loadSequence = 0;
const priceText = amount => amount === null ? 'No separate purchase charge' : (amount / 100).toFixed(2);
function setBusy(value) {
  busy = value;
  for (const id of ['model','search','option','reload','name','reason','review','save','cancel']) $(id).disabled = value;
  $('price').disabled = value || !current?.price_editable;
}
function status(message, error = false) { $('status').textContent = message; $('status').className = error ? 'error' : ''; }
async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Request failed');
  return data;
}
function node(tag, text, className) { const el = document.createElement(tag); el.textContent = text; if (className) el.className = className; return el; }
function permitDiscard() { return !dirty || window.confirm('Discard your unsaved option changes?'); }
function fillOptions(preferred) {
  const model = models.find(m => m.revision_id === $('model').value);
  const query = $('search').value.trim().toLowerCase();
  const options = model.options.filter(o => `${o.rpo || ''} ${o.name}`.toLowerCase().includes(query));
  $('option').replaceChildren(...options.map(o => new Option(`${o.rpo || 'Uncoded'} · ${o.name}`, o.id)));
  if (options.some(o => o.id === preferred)) $('option').value = preferred;
}
function render(data) {
  current = data; dirty = false; $('editor').hidden = false;
  const row = data.option;
  models.find(m => m.revision_id === row.revision_id).options.find(o => o.id === row.id).name = row.name;
  const selected = Array.from($('option').options).find(o => o.value === row.id);
  if (selected) selected.textContent = `${row.rpo || 'Uncoded'} · ${row.name}`;
  $('name').value = row.name; $('price').value = data.price_editable ? priceText(row.purchase_amount_minor) : '';
  $('price').disabled = !data.price_editable; $('reason').value = '';
  $('identity').textContent = `${row.rpo || 'Uncoded'} · ${row.lifecycle} · Revision edit ${data.edit_version}`;
  $('price-note').textContent = data.price_editable
    ? `${data.currency} base price. Contextual rates and package inclusion can change the final charge; this does not edit those rules.`
    : 'This option has no editable base purchase price. Its existing charge meaning is preserved.';
  $('scope').replaceChildren(...data.configurations.map(c => {const tr = document.createElement('tr'); tr.append(node('td', c.body),node('td', c.trim),node('td', c.status)); return tr;}));
  $('rates').textContent = data.contextual_rates.length
    ? `Existing contextual prices remain: ${data.contextual_rates.map(r => `${r.configuration_id}: ${priceText(r.amount_minor)} (priority ${r.priority})`).join('; ')}.`
    : 'No contextual price overrides are recorded for this option. Inclusion and ownership rules still determine whether it is charged.';
  $('history').replaceChildren(...(data.history.length ? data.history.map(change => {
    const el = node('div', '', 'history-entry');
    el.append(node('strong', `Edit ${change.edit_version} · ${new Date(change.saved_at).toLocaleString()}`), node('p', change.reason));
    el.append(node('p', `Name: ${change.before.name} → ${change.after.name}`), node('p', `Base price: ${priceText(change.before.purchase_amount_minor)} → ${priceText(change.after.purchase_amount_minor)}`)); return el;
  }) : [node('p', 'No saved edits for this option.')]));
  $('evidence').replaceChildren(...data.evidence.map(e => node('li', `${e.source_path} · ${e.locator} · ${e.fragment_key}`)));
}
async function load() {
  const sequence = ++loadSequence;
  const revision = $('model').value, option = $('option').value;
  current = null; dirty = false; $('editor').hidden = true;
  if (!option) { status('No matching options.'); return; }
  try {
    const data = await api(`/api/option?${new URLSearchParams({revision,option})}`);
    if (sequence !== loadSequence) return;
    render(data); status('');
  } catch (error) { if (sequence === loadSequence) status(error.message, true); }
}
$('model').addEventListener('change', () => {
  if (!permitDiscard()) { $('model').value = current.option.revision_id; return; }
  $('search').value = ''; fillOptions(); load();
});
$('option').addEventListener('change', () => { if (!permitDiscard()) { $('option').value = current.option.id; return; } load(); });
$('search').addEventListener('change', () => { if (!permitDiscard()) return; fillOptions(current?.option.id); load(); });
$('reload').addEventListener('click', () => { if (permitDiscard()) load(); });
$('edit-form').addEventListener('input', () => { dirty = true; });
$('edit-form').addEventListener('submit', async event => {
  event.preventDefault(); if (busy || !current) return;
  setBusy(true);
  try {
    pending = await api('/api/preview', {revision_id:current.option.revision_id,option_id:current.option.id,etag:current.etag,
      name:$('name').value,price:current.price_editable ? $('price').value.trim() : null,reason:$('reason').value,previous_token:pending?.token});
    const rows = [];
    if (pending.before.name !== pending.after.name) rows.push(node('p', `Name: ${pending.before.name} → ${pending.after.name}`));
    if (pending.before.purchase_amount_minor !== pending.after.purchase_amount_minor) rows.push(node('p', `Base price (${pending.currency}): ${priceText(pending.before.purchase_amount_minor)} → ${priceText(pending.after.purchase_amount_minor)}`));
    rows.push(node('p', `Reason: ${pending.reason}`)); $('change-summary').replaceChildren(...rows);
    $('preview-scope').textContent = `Scope: ${pending.configurations.map(c => `${c.body} ${c.trim} (${c.status})`).join(', ')}. Contextual prices, availability and ownership rules are unchanged.`;
    $('preview').showModal(); status('');
  } catch (error) { status(error.message, true); }
  finally { setBusy(false); if ($('preview').open) $('cancel').focus(); }
});
async function cancel() {
  if (busy) return;
  $('preview').close(); const token = pending?.token; pending = null;
  if (token) { try { await api('/api/cancel', {token}); status('Preview cancelled. Your unsaved edits are still in the form.'); } catch (error) { status(error.message, true); } }
}
$('cancel').addEventListener('click', cancel);
$('preview').addEventListener('cancel', event => { event.preventDefault(); cancel(); });
$('save').addEventListener('click', async () => {
  if (busy || !pending) return;
  setBusy(true);
  try {
    const saved = await api('/api/save', {token:pending.token});
    render(saved);
    // Keep the saved option selected even when its new name no longer matches the search.
    $('search').value = ''; fillOptions(saved.option.id); status('Saved to the local authoring draft.');
  } catch (error) { status(error.message, true); }
  finally { pending = null; $('preview').close(); setBusy(false); }
});
window.addEventListener('beforeunload', event => { if (dirty) { event.preventDefault(); event.returnValue = ''; } });
api('/api/catalog').then(data => { models = data.models; $('model').replaceChildren(...models.map(m => new Option(m.name,m.revision_id))); fillOptions(); return load(); }).catch(error => status(error.message,true));
