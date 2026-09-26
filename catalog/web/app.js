'use strict';
const el = id => document.getElementById(id);
let catalog, model, buildToken, current, pending, busy = false, activeStep, interiorPath = [];
const UNAVAILABLE = 'The build form is temporarily unavailable. Please try again in a few minutes.';
// The signed build token lets a reload continue the same build. Storage can be
// unavailable (private windows, blocked site data); the form works without it.
const saved = {
  get() { try { return localStorage.getItem('corvette-build'); } catch { return null; } },
  set(value) { try { value ? localStorage.setItem('corvette-build', value) : localStorage.removeItem('corvette-build'); } catch {} },
};
function keep(token) { buildToken = token || null; saved.set(buildToken); }
const money = n => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(n/100);
const active = value => String(value).toLowerCase() === 'true';
function node(tag, text, parent) { const n=document.createElement(tag); n.textContent=text; if(parent) parent.append(n); return n; }
function option(parent, value, label) { const n=node('option',label,parent); n.value=value; }
function button(parent, label, action, disabled=false) {
  const b=node('button',label,parent); b.disabled=disabled || busy || !!pending; b.addEventListener('click',action); return b;
}
// Only the shown step's cards are priced: pricing every card takes about half a
// second on a phone when the engine runs in the browser.
function pricing(step) { return step==='interior'?['seat','base_interior']:step&&step!=='summary'?[step]:[]; }
async function api(path, body) {
  let status, result;
  body={cards_for:pricing(activeStep),...body};
  try { ({status,result}=await catalogEngine.call(path,path==='/api/session'?body:{...body,build_token:buildToken})); }
  catch(error) { console.error(error); throw new Error(UNAVAILABLE); }
  if(status>=500) throw new Error(UNAVAILABLE);
  if(status<200 || status>=300) throw new Error(result.error);
  if(result.build_token) keep(result.build_token);
  return result;
}
async function run(action) {
  if(busy) return; busy=true; el('error').textContent=''; el('notice').textContent='';
  const disabled = [...document.querySelectorAll('button,select,input')].map(n=>[n,n.disabled]);
  disabled.forEach(([n])=>n.disabled=true);
  try { await action(); } catch(error) { el('error').textContent=error.message; }
  finally {
    busy=false; disabled.forEach(([n,value])=>n.disabled=value);
    if(current) render();
    el('cancel').disabled=false; el('confirm').disabled=!pending;
    if(pending) el('cancel').focus();
  }
}
// Card photos come from the catalog's source asset rows; a failed image is
// hidden and never affects what can be selected.
function assetsFor(m) {
  const rows=m.presentation.asset_map||[];
  return {option:new Map(rows.filter(r=>r.target_type==='option').map(r=>[r.target_id,r])),
          context:new Map(rows.filter(r=>r.target_type==='context_choice').map(r=>[r.target_id,r])),
          model:rows.find(r=>r.target_type==='model')};
}
function media(row, alt, parent, eager=false) {
  if(!row?.image_url) return;
  const box=node('span','',parent);box.className='choice-media';box.dataset.fit=row.image_fit==='contain'?'contain':'cover';
  const add=(url,text,cls)=>{const img=document.createElement('img');img.src=url;img.alt=text||'';img.loading=eager?'eager':'lazy';img.decoding='async';img.draggable=false;
    if(/^[\w\s.%/-]+$/.test(row.image_position||''))img.style.objectPosition=row.image_position;
    if(cls)img.className=cls;img.addEventListener('error',()=>box.remove());box.append(img);};
  add(row.image_url,row.image_alt||alt);
  if(row.hover_image_url) add(row.hover_image_url,'','hover-media');
}
// Cards are rebuilt after each choice; focus returns to the activated card so
// keyboard users continue from it rather than from the top of the page.
function setupCards(focus) {
  el('modelCards').replaceChildren();
  Object.entries(catalog.models).sort((a,b)=>a[1].display_order-b[1].display_order).forEach(([key,m])=>{
    const master=m.presentation.model_master[0], b=node('button','',el('modelCards'));b.type='button';b.className='setup-card';b.dataset.value=key;
    b.setAttribute('aria-pressed',String(key===el('model').value));media(assetsFor(m).model,`Corvette ${master.model_label}`,b,true);
    node('span',master.model_label,b);if(master.setup_card_subtitle)node('small',master.setup_card_subtitle,b);
    // Reselecting the current choice changes nothing, as with the former select.
    b.addEventListener('click',()=>{if(key===el('model').value)return;el('model').value=key;configurations({group:'modelCards',value:key});});
  });
  el('bodyCards').replaceChildren();
  const assets=assetsFor(model);
  [...el('bodyStyle').options].forEach(o=>{
    const b=node('button','',el('bodyCards'));b.type='button';b.className='setup-card';b.dataset.value=o.value;b.setAttribute('aria-pressed',String(o.value===el('bodyStyle').value));
    media(assets.context.get(`body_style__${o.value}`),`Corvette ${model.presentation.model_master[0].model_label} ${o.textContent}`,b,true);node('span',o.textContent,b);
    b.addEventListener('click',()=>{if(o.value===el('bodyStyle').value)return;el('bodyStyle').value=o.value;trims();setupCards({group:'bodyCards',value:o.value});});
  });
  if(focus?.group)[...el(focus.group).children].find(c=>c.dataset.value===focus.value)?.focus();
}
function configurations(focus) {
  model=catalog.models[el('model').value]; el('bodyStyle').replaceChildren(); catalogEngine.warm(el('model').value);
  // The existing form names itself after the chosen model.
  document.title=el('appTitle').textContent=`${model.presentation.model_master[0].model_label} Order Form`;
  const bodies=[...new Set(Object.values(model.configurations).filter(c=>active(c.active)).sort((a,b)=>a.display_order-b.display_order).map(c=>c.body_style))];
  bodies.forEach(body=>option(el('bodyStyle'),body,body[0].toUpperCase()+body.slice(1))); trims(); setupCards(focus);
}
function trims() {
  el('configuration').replaceChildren();
  Object.entries(model.configurations).filter(([,c])=>active(c.active)&&c.body_style===el('bodyStyle').value).sort((a,b)=>a[1].display_order-b[1].display_order).forEach(([id,c])=>option(el('configuration'),id,c.trim_level.toUpperCase()));
  startingPrice();
}
function startingPrice() { el('startingPrice').textContent=`Starting MSRP ${money(model.configurations[el('configuration').value].base_price*100)}`; }
function choiceCards() { return current.cards.options.filter(c=>model.options[c.option_id].customer_selectable); }
function steps() {
  // Every step with cards is known without pricing them (card_steps, in card order).
  const result=[], seen=new Set(), present=new Map(current.card_steps.map(s=>[s.step_key,s.section_label]));
  for(const s of model.presentation.runtime_steps.filter(s=>active(s.active)).sort((a,b)=>a.runtime_order-b.runtime_order)) {
    let key=s.step_key, label=s.step_label;
    if(['body_style','trim_level','summary'].includes(key)) continue;
    if(['seat','base_interior'].includes(key)) { key='interior'; label='Seats & interior'; }
    if(seen.has(key) || (key!=='interior' && !present.has(key))) continue;
    seen.add(key); result.push({key,label});
  }
  // Keep any newly authored sections reachable even without step metadata.
  for(const [key,label] of present) if(!seen.has(key) && !['seat','base_interior'].includes(key)) {
    seen.add(key);result.push({key,label:key==='standard_equipment'?'Additional equipment':label});
  }
  result.push({key:'summary',label:'Review build'});return result;
}
async function go(key) {
  // The step changes only once its cards are priced.
  let moved=false;
  await run(async()=>{current=await api('/api/cards',{cards_for:pricing(key)});activeStep=key;el('search').value='';moved=true;});
  if(moved){el('stepTitle').focus();el('stepTitle').scrollIntoView({block:'start',behavior:'smooth'});}
}
// A new or reopened build opens on its first step, priced.
async function openBuild(result) {
  current=result;activeStep=steps()[0].key;interiorPath=[];
  current=await api('/api/cards',{});
}
function render() {
  const b=current.build, cfg=model.configurations[b.configuration_id], list=steps();
  if(!list.some(s=>s.key===activeStep)) activeStep=list[0].key;
  const index=list.findIndex(s=>s.key===activeStep), reviewing=activeStep==='summary';
  el('setup').hidden=true; el('build').hidden=false; el('buildActions').hidden=false;
  el('vehicleName').textContent=cfg.display_name;
  el('total').textContent=money(b.total_minor); el('basePrice').textContent=money(cfg.base_price*100); el('optionsPrice').textContent=money(b.total_minor-cfg.base_price*100);
  el('selectionCount').textContent=b.missing_requirements.length ? `${b.missing_requirements.length} required selection${b.missing_requirements.length===1?'':'s'} remaining` : 'Ready to review';
  el('revert').disabled=!!pending || !current.revertible;
  el('export').disabled=!!pending || b.issues.some(i=>i!=='partial_catalog_not_submission_ready');
  el('stepRail').replaceChildren();el('stepSelect').replaceChildren();
  list.forEach((s,i)=>{const btn=button(el('stepRail'),'',()=>go(s.key));btn.className='step-link';node('span',String(i+1).padStart(2,'0'),btn).className='step-index';node('span',s.label,btn);if(s.key===activeStep)btn.setAttribute('aria-current','step');option(el('stepSelect'),s.key,s.label);});
  el('stepSelect').value=activeStep;el('stepCount').textContent=`Step ${index+1} of ${list.length}`;el('stepTitle').textContent=list[index].label;
  el('stepHint').textContent=reviewing?'Check your selections and total before downloading or contacting the dealer.':'Select an option to see its price and any changes needed for your build.';
  el('previous').disabled=index===0 || !!pending;el('next').hidden=reviewing;el('next').disabled=!!pending;
  el('next').textContent=index===list.length-2?'Review build':'Continue';
  el('artwork').hidden=reviewing;
  catalogArtwork.render(b.visualizer);
  el('interiorPanel').hidden=activeStep!=='interior'; if(activeStep==='interior') renderInteriors();
  el('searchLabel').hidden=reviewing || activeStep==='interior';el('buildReview').hidden=!reviewing;
  renderOptions();renderSummary();catalogDealer.sync();
}
function renderOptions() {
  el('options').replaceChildren();const groups=new Map(), query=el('search').value.toLowerCase(), photos=assetsFor(model).option;
  let parent=el('options');
  if(activeStep==='interior') { parent=node('details','',parent);node('summary','Individual seat options',parent); }
  choiceCards().filter(c=>(c.step_key===activeStep || activeStep==='interior' && ['seat','base_interior'].includes(c.step_key)) && `${c.rpo} ${c.label}`.toLowerCase().includes(query)).forEach(c=>{
    if(!groups.has(c.section_id)){const section=node('section','',parent);node('h3',c.section_label,section);const grid=node('div','',section);grid.className='cards';groups.set(c.section_id,grid);}
    const card=node('article','',groups.get(c.section_id));card.className=`choice-card ${c.selected?'selected':''}`;
    media(photos.get(c.option_id),c.label,card);node('span',c.rpo||'Option',card).className='rpo';node('h4',c.label,card);
    if(c.selected)node('p','Selected',card).className='selected-label';
    if(c.selectable && c.delta_minor!==undefined)node('p',`${c.selected?'Removing':'Selecting'}: ${c.delta_minor===0?'no price change':`${c.delta_minor>0?'+':'−'}${money(Math.abs(c.delta_minor))} to build total`}`,card);
    if(c.description || c.detail_raw || c.reason){const d=node('details','',card);node('summary','Option details',d);for(const text of new Set([c.description,c.detail_raw,c.reason].filter(Boolean)))node('p',text,d);}
    if(!c.selectable)node('p',c.selected?'Included with your current build':'Unavailable with your current build',card);
    button(card,c.selected?(c.selectable?'Remove':'Included'):(c.selectable?'Select':'Unavailable'),()=>run(()=>preview(c.selected?'remove':'select',c.option_id,c.label)),!c.selectable);
  });
  if(!groups.size && activeStep!=='interior' && activeStep!=='summary')node('p',query?'No matching options in this step.':'No options in this step.',el('options'));
}
function renderInteriors() {
  const rows=current.cards.interiors.map(c=>({...c,levels:JSON.parse(model.interiors[c.interior_id].hierarchy.interior_hierarchy_levels).slice(1)}));
  el('interiorFilters').replaceChildren();el('interiorChoices').replaceChildren();
  let matches=rows;
  // Narrow the existing interior hierarchy without changing its exact catalog leaves.
  for(let depth=0; matches.length && matches.every(r=>r.levels.length>depth+1);depth++) {
    if(depth>0 && matches.length<=6) break;
    const values=[...new Set(matches.map(r=>r.levels[depth]).filter(Boolean))];
    if(!values.includes(interiorPath[depth])) interiorPath=interiorPath.slice(0,depth);
    const title=['Seat style','Interior color','Material','Finish'][depth]||'Interior detail';
    const label=node('label',title,el('interiorFilters')), select=node('select','',label);
    option(select,'','Choose '+title.toLowerCase()); values.forEach(v=>option(select,v,v));select.value=interiorPath[depth]||'';
    select.addEventListener('change',()=>{interiorPath=interiorPath.slice(0,depth);if(select.value)interiorPath.push(select.value);renderInteriors();});
    if(!interiorPath[depth]) return;
    matches=matches.filter(r=>r.levels[depth]===interiorPath[depth]);
  }
  for(const row of matches) {
    const selected=current.build.interior_id===row.interior_id, card=node('article','',el('interiorChoices'));card.className=`choice-card ${selected?'selected':''}`;
    node('h4',row.levels.slice(interiorPath.length).join(' · ')||row.label,card);
    const source=model.interiors[row.interior_id].source;
    node('p',[source.Material,source.Stitch && `Stitching: ${source.Stitch}`,source.Suede && `Suede: ${source.Suede}`].filter(Boolean).join(' · '),card);
    if(selected)node('p','Selected',card).className='selected-label';
    button(card,selected?'Remove interior':'Select interior',()=>run(()=>preview('interior',selected?null:row.interior_id,selected?'no interior':row.label)));
  }
}
function renderSummary() {
  const b=current.build;el('recap').replaceChildren();
  if(b.selected_interior)node('p',current.cards.interiors.find(i=>i.interior_id===b.interior_id)?.label || b.selected_interior.key,el('recap'));
  const sections=new Map();for(const item of b.summary_items) {
    if(!sections.has(item.section_label)){node('h4',item.section_label,el('recap'));sections.set(item.section_label,node('ul','',el('recap')));}
    node('li',`${item.rpo||''} ${item.label}`,sections.get(item.section_label));
  }
  for(const [label,items] of [['Installed equipment',b.installed_equipment],['Standard equipment',b.informational_standard_equipment]]) {
    const d=node('details','',el('recap'));node('summary',`${label} (${items.length})`,d);const ul=node('ul','',d);items.forEach(i=>node('li',`${i.rpo||''} ${i.label}`,ul));
  }
  el('requirements').replaceChildren();b.missing_requirements.forEach(text=>node('li',text,el('requirements')));el('requirementsPanel').hidden=!b.missing_requirements.length;
  el('exportHint').textContent=b.missing_requirements.length?'Complete the required selections above to download your build or continue to the dealer form.':'Download saves a build file. The dealer form lets you review your request before sending.';
}
async function preview(action,target,label) {
  pending=null;el('changes').replaceChildren();el('technicalChanges').replaceChildren();
  const result=await api('/api/preview',{action,target,version:current.version}), w=result.warning,c=w.changes;
  el('warningTitle').textContent=action==='revert'?'Undo your last change?':`${action==='remove'?'Remove':'Select'} ${label}?`;
  const displayed=new Set();
  for(const [field,prefix] of [['removed','Remove'],['added','Add'],['installed_removed','Remove equipment'],['installed_added','Include equipment']])for(const item of c[field]) {
    if(displayed.has(item.option_id))continue;displayed.add(item.option_id);node('li',`${prefix}: ${item.label}${item.rpo?` (${item.rpo})`:''}`,el('changes'));
  }
  if(c.interior.before!==c.interior.after)node('li',`Interior: ${current.cards.interiors.find(i=>i.interior_id===c.interior.after)?.label||'No interior selected'}`,el('changes'));
  for(const change of c.charge_changes) {
    const charge=change.after||change.before;
    if((change.before?.amount_minor||0)===(change.after?.amount_minor||0))continue;
    const name=charge.owner_kind==='option'?model.options[charge.owner_id]?.name:w.candidate.charges.find(i=>i.owner_kind===charge.owner_kind&&i.owner_id===charge.owner_id)?.label || current.build.charges.find(i=>i.owner_kind===charge.owner_kind&&i.owner_id===charge.owner_id)?.label;
    node('li',`${name||'Price'}: ${change.before?money(change.before.amount_minor):'Not in build'} → ${change.after?money(change.after.amount_minor):'Removed'}`,el('changes'));
  }
  // Retain all supporting relationships and disclosures with the exact server warning.
  for(const line of w.lines)node('li',line,el('technicalChanges'));
  for(const line of w.lines.filter(line=>line.startsWith('Selecting this hash mark')))node('li',line,el('changes'));
  if(!el('changes').children.length)node('li','Update your selection; your equipment stays the same.',el('changes'));
  el('priceChange').textContent=`Total MSRP ${money(c.total_after_minor)} (${c.delta_minor===0?'no price change':`${c.delta_minor>0?'+':'−'}${money(Math.abs(c.delta_minor))}`})`;
  el('technicalChanges').parentElement.open=false;
  pending=result;el('warning').showModal();el('cancel').focus();
}
async function cancel() {current=await api('/api/cancel',{version:current.version});pending=null;el('warning').close();el('stepTitle').focus();}
el('model').addEventListener('change',configurations);el('bodyStyle').addEventListener('change',trims);el('configuration').addEventListener('change',startingPrice);
el('start').addEventListener('click',()=>run(async()=>{activeStep=null;await openBuild(await api('/api/session',{model:el('model').value,configuration_id:el('configuration').value}));}));
el('search').addEventListener('input',renderOptions);el('stepSelect').addEventListener('change',()=>go(el('stepSelect').value));
el('previous').addEventListener('click',()=>{const list=steps();go(list[list.findIndex(s=>s.key===activeStep)-1].key);});
el('next').addEventListener('click',()=>{const list=steps();go(list[list.findIndex(s=>s.key===activeStep)+1].key);});
for(const id of ['review','summaryReview'])el(id).addEventListener('click',()=>go('summary'));
el('cancel').addEventListener('click',()=>run(cancel));el('warning').addEventListener('cancel',event=>{event.preventDefault();run(cancel);});
el('confirm').addEventListener('click',()=>run(async()=>{
  if(!pending)throw new Error('No selection to apply');
  current=await api('/api/confirm',{token:pending.token,warning_sha256:pending.warning_sha256,version:pending.version});pending=null;el('warning').close();el('notice').textContent='Your build has been updated.';el('stepTitle').focus();
}));
el('revert').addEventListener('click',()=>run(()=>preview('revert',null)));
el('reset').addEventListener('click',()=>el('resetDialog').showModal());el('resetCancel').addEventListener('click',()=>el('resetDialog').close());
el('resetConfirm').addEventListener('click',()=>{current=null;keep(null);pending=null;el('build').hidden=true;el('buildActions').hidden=true;el('setup').hidden=false;el('notice').textContent='';el('resetDialog').close();el('start').disabled=false;el('model').focus();});
// Same Markdown summary as the existing form's Download Build, from the confirmed order.
// Whole dollars as in the existing form, but never round away cents: an edited
// price such as $61.25 must reconcile with the total (same rule as dealer.money).
const dollars = n => { const c=Math.round(Number(n||0)*100); return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:c%100?2:0,maximumFractionDigits:c%100?2:0}).format(c/100); };
function buildMarkdown(order, master) {
  const lines=[`# ${master.model_year} Corvette ${master.model_label}`,'',`Generated: ${new Date().toISOString()}`,'','### Variant','',`- ${order.vehicle.display_name||''}`,''];
  for(const section of order.sections){
    if(!section.items.length)continue;
    lines.push(`### ${section.section}`,'');
    for(const item of section.items)lines.push(`- ${item.rpo?`${item.rpo} `:''}${item.label||''}: ${dollars(item.price)}`);
    lines.push('');
  }
  lines.push('### MSRP','',`- Total MSRP: ${order.msrp}`,'');
  return lines.join('\n').replace(/\n{3,}/g,'\n\n');
}
el('export').addEventListener('click',()=>run(async()=>{
  const order=await api('/api/dealer/review',{version:current.version}), master=model.presentation.model_master[0];
  const url=URL.createObjectURL(new Blob([buildMarkdown(order,master)],{type:'text/markdown'}));
  const a=node('a','');a.href=url;a.download=`${master.export_slug||'corvette'}-build.md`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}));
catalogDealer.init({api,state:()=>({catalog,current,pending,buildToken,busy})});el('dealerOpen').addEventListener('click',()=>run(()=>catalogDealer.open()));
async function restore() {
  buildToken=saved.get(); if(!buildToken) return;
  try {
    activeStep=null;const r=await api('/api/restore',{});
    el('model').value=r.model;configurations();el('bodyStyle').value=model.configurations[r.configuration_id].body_style;trims();setupCards();el('configuration').value=r.configuration_id;
    await openBuild(r);render();
    if(r.notice)el('notice').textContent=r.notice;
  } catch(e) {
    // A build that cannot be replayed on this catalog starts over; an outage keeps it for later.
    if(e.message===UNAVAILABLE) throw e;
    keep(null);el('notice').textContent='Your saved build could not be reopened. Please start a new build.';
  }
}
(async()=>{
  try{
    let r;
    try { r=await catalogEngine.call('/api/catalog');catalog=r.result; } catch { throw new Error(UNAVAILABLE); }
    if(r.status!==200)throw new Error(r.status>=500?UNAVAILABLE:catalog.error);
    el('release').textContent=`Release ${catalog.release_id}`;el('deliveryMode').textContent=catalog.dealer.enabled?'Build requests are sent to Stingray Chevrolet.':'Preview mode · Build requests are not sent to the dealership.';Object.entries(catalog.models).sort((a,b)=>a[1].display_order-b[1].display_order).forEach(([key,c])=>option(el('model'),key,c.presentation.model_master[0].model_label));el('model').value=catalog.default_model;configurations();el('start').disabled=false;
    await restore();
  }catch(e){el('error').textContent=e.message;}
})();
