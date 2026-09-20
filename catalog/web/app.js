'use strict';
const el = id => document.getElementById(id);
let catalog, model, sessionId, current, pending, busy = false;
const money = n => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(n/100);
function node(tag, text, parent) { const n=document.createElement(tag); n.textContent=text; if(parent) parent.append(n); return n; }
async function api(path, body) {
  const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json',...(sessionId?{'X-Catalog-Session':sessionId}:{})},body:JSON.stringify(body)});
  const result=await response.json(); if(!response.ok) throw new Error(result.error); return result;
}
async function run(action) {
  if(busy) return; busy=true; el('error').textContent='';
  document.querySelectorAll('button').forEach(b=>b.disabled=true);
  try { await action(); } catch(error) { el('error').textContent=error.message; }
  finally { busy=false; if(current) render(); else el('start').disabled=false;
    el('cancel').disabled=false; el('confirm').disabled=!pending; }
}
function configurations() {
  model=catalog.models[el('model').value]; el('configuration').replaceChildren();
  Object.entries(model.configurations).filter(([,c])=>String(c.active).toLowerCase()==='true').sort((a,b)=>a[1].display_order-b[1].display_order).forEach(([id,c])=>{const o=node('option',c.display_name,el('configuration'));o.value=id;});
}
function interiorDescription() {
  el('interiorDescription').textContent=el('interior').value?el('interior').selectedOptions[0].textContent:'';
}
function render() {
  const b=current.build; el('setup').hidden=true; el('build').hidden=false;
  el('total').textContent=money(b.total_minor); el('requirements').textContent=b.missing_requirements.join(' · ');
  el('revert').disabled=!!pending;el('export').disabled=!!pending||b.issues.some(i=>i!=='partial_catalog_not_submission_ready');el('chooseInterior').disabled=!!pending;
  el('recap').replaceChildren();
  for(const [label,items] of [['Resolved choices',b.resolved],['Installed equipment',b.installed_equipment],['Informational standard equipment',b.informational_standard_equipment]]) {
    const d=node('details','',el('recap'));node('summary',`${label} (${items.length})`,d);const ul=node('ul','',d);items.forEach(i=>node('li',`${i.rpo||''} ${i.label}`,ul));
  }
  el('interior').replaceChildren(); const empty=node('option','No interior selected',el('interior'));empty.value='';
  current.cards.interiors.forEach(i=>{const o=node('option',i.label,el('interior'));o.value=i.interior_id;});el('interior').value=b.interior_id||'';
  interiorDescription();
  el('options').replaceChildren();const groups=new Map();const query=el('search').value.toLowerCase();
  current.cards.options.filter(c=>`${c.rpo} ${c.label}`.toLowerCase().includes(query)).forEach(c=>{
    if(!groups.has(c.section_id)){const section=node('section','',el('options'));node('h3',c.section_label,section);const grid=node('div','',section);grid.className='cards';groups.set(c.section_id,grid);}
    const card=node('article','',groups.get(c.section_id));card.className=`card ${c.selected?'selected':''} ${c.conflict?'conflict':''}`;
    node('h4',`${c.rpo||''} ${c.label}`,card);if(c.description)node('p',c.description,card);if(c.detail_raw&&c.detail_raw!==c.description)node('p',c.detail_raw,card);
    if(c.reason)node('p',c.reason,card);else if(c.conflict)node('p','Compatibility change — review required',card);
    const button=node('button',c.selected?'Review removal':'Review selection',card);button.disabled=!!pending||!c.selectable;
    button.addEventListener('click',()=>run(()=>preview(c.selected?'remove':'select',c.option_id)));
  });
}
async function preview(action,target) {
  // Never render candidate state into the current build. Only the warning uses it.
  pending=null;el('changes').replaceChildren();
  const result=await api('/api/preview',{action,target,version:current.version});
  for(const line of result.warning.lines)node('li',line,el('changes'));
  // Enable confirmation only after every warning line is in the dialog.
  pending=result;el('warning').showModal();el('cancel').focus();
}
async function cancel() { current=await api('/api/cancel',{version:current.version});pending=null;el('warning').close(); }
el('model').addEventListener('change',configurations);
el('interior').addEventListener('change',interiorDescription);
el('start').addEventListener('click',()=>run(async()=>{const r=await api('/api/session',{model:el('model').value,configuration_id:el('configuration').value});sessionId=r.session_id;current=r;}));
el('chooseInterior').addEventListener('click',()=>run(()=>preview('interior',el('interior').value||null)));
el('search').addEventListener('input',()=>{if(!busy)render();});
el('cancel').addEventListener('click',()=>run(cancel));
el('warning').addEventListener('cancel',event=>{event.preventDefault();run(cancel);});
el('confirm').addEventListener('click',()=>run(async()=>{
  if(!pending)throw new Error('No preview to confirm');
  current=await api('/api/confirm',{token:pending.token,warning_sha256:pending.warning_sha256,version:pending.version});
  pending=null;el('warning').close();
}));
el('revert').addEventListener('click',()=>run(()=>preview('revert',null)));
el('export').addEventListener('click',()=>run(async()=>{const order=await api('/api/order',{});const url=URL.createObjectURL(new Blob([JSON.stringify(order,null,2)],{type:'application/json'}));const a=node('a','');a.href=url;a.download='corvette-build.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}));
(async()=>{try{const r=await fetch('/api/catalog');catalog=await r.json();if(!r.ok)throw new Error(catalog.error);el('release').textContent=`Release ${catalog.release_id}`;Object.entries(catalog.models).sort((a,b)=>a[1].display_order-b[1].display_order).forEach(([key,c])=>{const o=node('option',c.presentation.model_master[0].model_label,el('model'));o.value=key;});el('model').value=catalog.default_model;configurations();}catch(e){el('error').textContent=e.message;el('start').disabled=true;}})();
