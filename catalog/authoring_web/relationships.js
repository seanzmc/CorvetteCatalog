'use strict';
const $ = id => document.getElementById(id);
const node = (tag, text) => { const el = document.createElement(tag); el.textContent = text; return el; };
let current = null, pending = null, dirty = false, busy = false;
const label = o => `${o.rpo || 'Uncoded'} · ${o.name}`;
const policyLabel = p => p === 'preserve_prior' ? 'Preserve the independent purchase' : 'Absorb it into the package';
function status(text, error = false) { $('status').textContent = text; $('status').className = error ? 'error' : ''; }
function setBusy(value) { busy = value; for (const id of ['model','relationship','target','reason','reload','review','save','cancel']) $(id).disabled = value; }
async function api(path, body) { const r = await fetch(path, body === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); const data = await r.json(); if (!r.ok) throw new Error(data.error || 'Request failed'); return data; }
function discard() { return !dirty || window.confirm('Discard your unsaved relationship changes?'); }
function render(data) {
  current = data; dirty = false; $('editor').hidden = false;
  const r = data.relationship;
  $('identity').textContent = `${r.source_rpo || 'Uncoded'} · ${r.source_name} includes ${r.target_rpo || 'Uncoded'} · ${r.target_name}`;
  $('policies').textContent = `Edit ${data.edit_version} · Included option: ${r.peer_policy === 'locked' ? 'locked to its source' : 'can yield to an explicit choice'} · ${policyLabel(r.intent_policy)}`;
  $('target').value = r.intent_policy; $('reason').value = '';
  $('scope').textContent = data.configurations.map(c => `${c.body} ${c.trim}`).join(', ');
  $('history').replaceChildren(...(data.history.length ? data.history.map(h => { const d=node('div',''); d.className='history-entry'; d.append(node('strong',`Edit ${h.edit_version} · ${new Date(h.saved_at).toLocaleString()}`),node('p',`${policyLabel(h.before.intent_policy)} → ${policyLabel(h.after.intent_policy)}`),node('p',h.reason)); return d; }) : [node('p','No saved edits for this relationship.')]));
  $('evidence').replaceChildren(...data.evidence.map(e => node('li',`${e.source_path} · ${e.locator} · ${e.fragment_key}`)));
}
async function load() { current = null; dirty = false; $('editor').hidden = true; if (!$('relationship').value) { status('No direct inclusions in this model.'); return; } render(await api(`/api/relationship?${new URLSearchParams({revision:$('model').value,relationship:$('relationship').value})}`)); status(''); }
async function list(preferred) { const data=await api(`/api/relationships?${new URLSearchParams({revision:$('model').value})}`); $('relationship').replaceChildren(...data.relationships.map(r => new Option(`${r.source_rpo} · ${r.source_name} → ${r.target_rpo} · ${r.target_name}`,r.id))); if (preferred) $('relationship').value=preferred; }
async function run(action) { if(busy) return; setBusy(true); try { await action(); } catch(e) {status(e.message,true);} finally {setBusy(false);} }
$('model').addEventListener('change', () => { if(!discard()) { $('model').value=current.relationship.revision_id; return; } run(async()=>{await list();await load();}); });
$('relationship').addEventListener('change', () => {if(!discard()) {$('relationship').value=current.relationship.id;return;}run(load);});
$('reload').addEventListener('click',()=>{if(discard())run(load);});
$('edit-form').addEventListener('input',()=>{dirty=true;});
function describe(before, after) {
  const lines=[];
  for (const phase of ['purchased','selected','removed']) {
    const b=before[phase], a=after[phase];
    lines.push(node('h3',phase==='purchased' ? 'Purchase the included option first' : phase==='selected' ? 'Then select the source package' : 'Then remove the source package'));
    lines.push(node('p',`Total: ${(b.total_minor/100).toFixed(2)} → ${(a.total_minor/100).toFixed(2)}`));
    const bids=new Set(b.resolved.map(o=>o.option_id)), aids=new Set(a.resolved.map(o=>o.option_id));
    const added=a.resolved.filter(o=>!bids.has(o.option_id)), removed=b.resolved.filter(o=>!aids.has(o.option_id));
    lines.push(node('p',`Added: ${added.map(o=>o.rpo || o.label).join(', ') || 'None'}. Removed: ${removed.map(o=>o.rpo || o.label).join(', ') || 'None'}.`));
    lines.push(node('p',`Independent purchases: ${a.intent.map(id => a.resolved.find(o => o.option_id === id)?.rpo || 'Uncoded option').join(', ') || 'None'}`));
    lines.push(node('p',`Resulting charges: ${a.charges.map(c=>`${c.label}: ${(c.amount_minor/100).toFixed(2)}`).join('; ')}`));
    if(a.missing_requirements.length) lines.push(node('p',`Incomplete choices: ${a.missing_requirements.join('; ')}`));
  }
  return lines;
}
$('edit-form').addEventListener('submit',event=>{event.preventDefault();run(async()=>{
  pending=await api('/api/relationship/preview',{revision_id:current.relationship.revision_id,acquisition_id:current.relationship.id,etag:current.etag,intent_policy:$('target').value,reason:$('reason').value,previous_token:pending?.token});
  $('summary').textContent=`${label(pending.source)} includes ${label(pending.target)}: ${policyLabel(pending.before.intent_policy)} → ${policyLabel(pending.after.intent_policy)}`; $('preview-reason').textContent=pending.reason;
  $('outcomes').replaceChildren(...pending.after_outcomes.map((a,i)=>{const d=node('details','');d.append(node('summary',`${a.body} ${a.trim}`),...describe(pending.before_outcomes[i],a));return d;}));
  $('preview').showModal();status('');
});});
async function cancel(){if(busy)return; const token=pending?.token;pending=null;$('preview').close();if(token)await run(async()=>{await api('/api/cancel',{token});status('Preview cancelled. Unsaved changes remain in the form.');});}
$('cancel').addEventListener('click',cancel);$('preview').addEventListener('cancel',e=>{e.preventDefault();cancel();});
$('save').addEventListener('click',()=>run(async()=>{try {const data=await api('/api/relationship/save',{token:pending.token});await list(data.relationship.id);render(data);status('Saved to the local authoring draft.');} finally {pending=null;$('preview').close();}}));
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
run(async()=>{const data=await api('/api/catalog');$('model').replaceChildren(...data.models.map(m=>new Option(m.name,m.revision_id)));await list();await load();});
