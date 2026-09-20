'use strict';
const $ = id => document.getElementById(id);
const node = (tag, text) => {const el=document.createElement(tag);el.textContent=text;return el;};
const money = value => (value/100).toFixed(2);
let current=null,pending=null,dirty=false,busy=false;
function status(text,error=false){$('status').textContent=text;$('status').className=error?'error':'';}
function setBusy(value){busy=value;for(const id of ['model','rate','price','reason','reload','review','save','cancel'])$(id).disabled=value;}
async function api(path,body){const r=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();if(!r.ok)throw new Error(data.error||'Request failed');return data;}
function discard(){return !dirty||window.confirm('Discard your unsaved shared-price changes?');}
function render(data){
  current=data;dirty=false;$('editor').hidden=false;
  const r=data.rate;
  $('identity').textContent=`${r.code} · ${r.kind.replaceAll('_',' ')} · ${r.body} ${r.trim} · Edit ${data.edit_version}`;
  $('price-label').textContent=`Component price (${data.currency})`;$('price').value=money(r.amount_minor);$('reason').value='';
  $('scope').textContent=`${data.members.length} interior choices share this one ${data.currency} price in ${r.body} ${r.trim}.`;
  $('members').replaceChildren(...data.members.map(m=>{const tr=node('tr','');tr.append(node('td',m.label),node('td',m.interior_id));return tr;}));
  $('history').replaceChildren(...(data.history.length?data.history.map(h=>{const d=node('div','');d.className='history-entry';d.append(node('strong',`Edit ${h.edit_version} · ${new Date(h.saved_at).toLocaleString()}`),node('p',`${data.currency} ${money(h.before.amount_minor)} → ${money(h.after.amount_minor)}`),node('p',h.reason));return d;}):[node('p','No saved edits for this shared price.')]));
  $('evidence').replaceChildren(...data.evidence.map(e=>node('li',`${e.source_path} · ${e.locator} · ${e.fragment_key}`)));
}
async function load(){current=null;dirty=false;$('editor').hidden=true;if(!$('rate').value){status('No shared component prices in this model.');return;}const [component,configuration]=JSON.parse($('rate').value);render(await api(`/api/component-rate?${new URLSearchParams({revision:$('model').value,component,configuration})}`));status('');}
async function list(){const data=await api(`/api/component-rates?${new URLSearchParams({revision:$('model').value})}`);$('rate').replaceChildren(...data.rates.map(r=>new Option(`${r.code} · ${r.kind.replaceAll('_',' ')} · ${r.body} ${r.trim} · ${r.member_count} interiors`,JSON.stringify([r.component_id,r.configuration_id]))));}
async function run(action){if(busy)return;setBusy(true);try{await action();}catch(e){status(e.message,true);}finally{setBusy(false);}}
$('model').addEventListener('change',()=>{if(!discard()){$('model').value=current.rate.revision_id;return;}run(async()=>{await list();await load();});});
$('rate').addEventListener('change',()=>{if(!discard()){$('rate').value=JSON.stringify([current.rate.component_id,current.rate.configuration_id]);return;}run(load);});
$('reload').addEventListener('click',()=>{if(discard())run(load);});
$('edit-form').addEventListener('input',()=>{dirty=true;});
$('edit-form').addEventListener('submit',e=>{e.preventDefault();run(async()=>{
  pending=await api('/api/component-rate/preview',{revision_id:current.rate.revision_id,component_id:current.rate.component_id,configuration_id:current.rate.configuration_id,etag:current.etag,price:$('price').value.trim(),reason:$('reason').value,previous_token:pending?.token});
  $('summary').textContent=`${pending.code} · ${pending.body} ${pending.trim}: ${pending.currency} ${money(pending.before.amount_minor)} → ${money(pending.after.amount_minor)} across ${pending.after_outcomes.length} interiors.`;$('preview-reason').textContent=pending.reason;
  $('outcomes').replaceChildren(...pending.after_outcomes.map((a,i)=>{const tr=node('tr','');tr.append(node('td',`${a.label} (${a.interior_id})`),node('td',money(pending.before_outcomes[i].total_minor)),node('td',money(a.total_minor)));return tr;}));
  $('preview').showModal();status('');
});});
async function cancel(){if(busy)return;const token=pending?.token;pending=null;$('preview').close();if(token)await run(async()=>{await api('/api/cancel',{token});status('Preview cancelled. Unsaved changes remain in the form.');});}
$('cancel').addEventListener('click',cancel);$('preview').addEventListener('cancel',e=>{e.preventDefault();cancel();});
$('save').addEventListener('click',()=>run(async()=>{try{render(await api('/api/component-rate/save',{token:pending.token}));status('Saved to the local authoring draft.');}finally{pending=null;$('preview').close();}}));
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
run(async()=>{const data=await api('/api/catalog');$('model').replaceChildren(...data.models.map(m=>new Option(m.name,m.revision_id)));await list();await load();});
