'use strict';
const el = id => document.getElementById(id);
let catalog, model, buildToken, current, pending, busy = false, activeStep, interiorPath = null, refocus = null;
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
  body={cards_for:pricing(activeStep),interiors_for:activeStep==='interior'?shownInteriors():[],...body};
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
    // A choice applied without a dialog returns focus to its re-rendered card.
    if(refocus && !pending) document.querySelector(`[data-choice="${CSS.escape(refocus)}"] button`)?.focus();
    refocus=null;
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
    if(cls)img.className=cls;img.addEventListener('error',()=>cls?img.remove():frame(box));box.append(img);};
  add(row.image_url,row.image_alt||alt);
  if(row.hover_image_url) add(row.hover_image_url,'','hover-media');
}
// The change to the build total, led by the amount so it reads at a glance.
function priceLine(card,selected,delta) {
  if(delta===null||delta===undefined) return;
  const amount=delta===0?'No price change':`${delta>0?'+':'−'}${money(Math.abs(delta))}`, p=node('p','',card);p.className='price-line';
  if(selected)p.textContent=`Removing: ${delta===0?'no price change':`${amount} to total`}`;
  else if(delta){node('strong',amount,p);p.append(' to total');}
  else p.textContent=amount;
}
// Cards in a grid share one layout: where some have a photo, the others get a
// plain frame with their code, so every card has the same shape.
// A photo that fails to load leaves the same frame, so its card keeps its shape.
function evenMedia(grid) {
  if(!grid.querySelector('.choice-media')) return;
  for(const card of grid.children) if(!card.querySelector('.choice-media')) {
    const box=document.createElement('span');card.prepend(box);frame(box);
  }
}
function frame(box) {
  box.className='choice-media placeholder';box.setAttribute('aria-hidden','true');
  box.textContent=box.parentElement?.querySelector('.rpo')?.textContent||'';
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
  await run(async()=>{
    if(key==='interior')interiorPath=null;
    current=await api('/api/cards',{cards_for:pricing(key),interiors_for:key==='interior'?shownInteriors():[]});activeStep=key;el('search').value='';moved=true;
  });
  if(moved){el('stepTitle').focus();el('stepTitle').scrollIntoView({block:'start',behavior:'smooth'});}
}
// A new or reopened build opens on its first step, priced.
async function openBuild(result) {
  current=result;activeStep=steps()[0].key;interiorPath=null;
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
  const parent=el('options');
  choiceCards().filter(c=>c.step_key===activeStep && `${c.rpo} ${c.label}`.toLowerCase().includes(query)).forEach(c=>{
    if(!groups.has(c.section_id)){const section=node('section','',parent);section.className='option-section';node('h3',c.section_label,section);const grid=node('div','',section);grid.className='cards';groups.set(c.section_id,grid);}
    const card=node('article','',groups.get(c.section_id));card.className=`choice-card ${c.selected?'selected':''}`;card.dataset.choice=c.option_id;
    media(photos.get(c.option_id),c.label,card);node('span',c.rpo||'Option',card).className='rpo';node('h4',c.label,card);
    if(c.selected)node('p','Selected',card).className='selected-label';
    if(c.selectable)priceLine(card,c.selected,c.delta_minor);
    // Another trim's options, options another choice unlocks and factory-unavailable
    // ones say so on the card itself.
    const plain=c.available_on?.length || c.unlocked_by?.length || c.reason==='Unavailable at this time';
    if(c.description || c.detail_raw || c.reason && !plain){const d=node('details','',card);node('summary','Option details',d);for(const text of new Set([c.description,c.detail_raw,plain?'':c.reason].filter(Boolean)))node('p',text,d);}
    if(!c.selectable&&!c.selected)node('p',plain?c.reason:'Unavailable with your current build',card).className=plain?'trim-note':'';
    button(card,c.selected?(c.selectable?'Remove':'Included'):(c.selectable?'Select':'Unavailable'),()=>run(()=>preview(c.selected?'remove':'select',c.option_id,c.label)),!c.selectable);
  });
  for(const grid of groups.values()){evenMedia(grid);node('span',`${grid.children.length} ${grid.children.length===1?'option':'options'}`,grid.previousSibling).className='section-count';}
  // A step with several sections opens with shortcuts to each.
  if(groups.size>1) {
    const jumps=document.createElement('nav');jumps.className='section-jumps';jumps.setAttribute('aria-label','Sections in this step');parent.prepend(jumps);
    for(const grid of groups.values()){const heading=grid.previousSibling;heading.tabIndex=-1;
      const b=button(jumps,heading.firstChild.textContent,()=>{heading.scrollIntoView({behavior:'smooth',block:'start'});heading.focus({preventScroll:true});});b.className='ghost-button';b.disabled=false;}
  }
  if(!groups.size && activeStep!=='interior' && activeStep!=='summary')node('p',query?'No matching options in this step.':'No options in this step.',el('options'));
}
// Interiors are chosen by tapping through their catalog hierarchy (seats, then
// color, then material or finish) until a few exact leaves remain; the trail
// steps back. interiorPath null means "open where the build's interior is".
function interiorView(rows,path) {
  let matches=rows;
  for(let depth=0;;depth++) {
    const leaves=depth>0 && matches.length<=6 || matches.every(r=>r.levels.length<=depth+1);
    if(leaves || depth>=path.length) return {depth,matches,leaves};
    const next=matches.filter(r=>r.levels[depth]===path[depth]);
    if(!next.length) return {depth,matches,leaves,stale:true};
    matches=next;
  }
}
function interiorRows() {
  // Order leaves, and so each level's values, as the existing form's interior display order.
  const rank=h=>[h.interior_group_display_order,h.interior_material_display_order,h.interior_choice_display_order].map(v=>Number(v||0));
  return current.cards.interiors.map(c=>{const h=model.interiors[c.interior_id].hierarchy;return {...c,rank:rank(h),levels:JSON.parse(h.interior_hierarchy_levels).slice(1)};})
    .sort((a,b)=>a.rank[0]-b.rank[0]||a.rank[1]-b.rank[1]||a.rank[2]-b.rank[2]||a.label.localeCompare(b.label));
}
function currentInteriorView(rows) {
  if(interiorPath===null) {
    const mine=rows.find(r=>r.interior_id===current.build.interior_id);interiorPath=[];
    // Descend to the level that shows the build's interior as a card.
    while(mine){const v=interiorView(rows,interiorPath);if(v.leaves||v.depth<interiorPath.length)break;const sibling=v.matches.filter(r=>r.levels[v.depth]===mine.levels[v.depth]);if(sibling.length<2)break;interiorPath.push(mine.levels[v.depth]);}
  }
  const view=interiorView(rows,interiorPath);
  if(!view.stale) return view;
  interiorPath=interiorPath.slice(0,view.depth);return interiorView(rows,interiorPath);
}
// The interiors shown as selectable cards: the only ones priced.
function shownInteriors() {
  if(!current) return [];
  const {depth,matches,leaves}=currentInteriorView(interiorRows());
  if(leaves) return matches.map(r=>r.interior_id);
  const counts=new Map();matches.forEach(r=>counts.set(r.levels[depth],(counts.get(r.levels[depth])||0)+1));
  return depth===0?[]:matches.filter(r=>counts.get(r.levels[depth])===1).map(r=>r.interior_id);
}
function renderInteriors() {
  const rows=interiorRows(), trail=el('interiorTrail'), choices=el('interiorChoices');trail.replaceChildren();choices.replaceChildren();
  const {depth,matches,leaves}=currentInteriorView(rows), photos=assetsFor(model).option;
  const seats=choiceCards().filter(c=>c.step_key==='seat'), seatFor=v=>seats.find(c=>c.rpo===v.split(' ')[0]);
  // Moving between levels prices the interiors the new level shows.
  const move=async path=>{
    interiorPath=path;
    const priced=new Set(current.cards.interiors.filter(i=>i.delta_minor!==null&&i.delta_minor!==undefined||!i.selectable).map(i=>i.interior_id));
    if(shownInteriors().every(id=>priced.has(id)))renderInteriors();else await run(async()=>{current=await api('/api/cards',{});});
    el('interiorHeading').focus();
  };
  // The trail names each chosen level; each earlier level is a way back.
  if(interiorPath.length) {
    const all=button(trail,'All seats',()=>move([]));all.className='ghost-button';all.disabled=false;
    interiorPath.slice(0,depth).forEach((v,i)=>{node('span','›',trail).setAttribute('aria-hidden','true');
      if(i<depth-1){const b=button(trail,seatFor(v)&&i===0?seatFor(v).label:v,()=>move(interiorPath.slice(0,i+1)));b.className='ghost-button';b.disabled=false;}
      else node('span',i===0&&seatFor(v)?seatFor(v).label:v,trail).setAttribute('aria-current','location');});
  }
  const title=leaves?'Choose your interior':['Choose your seats','Choose an interior color','Choose a material','Choose a finish'][depth]||'Choose an interior';
  const heading=node('h3',title,choices);heading.id='interiorHeading';heading.tabIndex=-1;
  const grid=node('div','',choices);grid.className='cards';
  function unoffered(seat) {
    const card=node('article','',grid);card.className='choice-card';
    media(photos.get(seat.option_id),seat.label,card);node('span',seat.rpo||'Seat',card).className='rpo';node('h4',seat.label,card);
    if(seat.reason)node('p',seat.reason,card).className=seat.available_on?.length||seat.reason==='Unavailable at this time'?'trim-note':'';
    button(card,'Unavailable',()=>{},true);
  }
  const leaf=row=>{
    const selected=current.build.interior_id===row.interior_id, card=node('article','',grid);card.className=`choice-card ${selected?'selected':''}`;card.dataset.choice=row.interior_id;
    const source=model.interiors[row.interior_id].source, rest=row.levels.slice(depth), name=rest.at(-1)||row.label;
    media(swatch(source),name,card);
    node('span',source['Interior Code']||'Interior',card).className='rpo';node('h4',name,card);
    // Levels still above the leaf (a material), less any the name already says.
    const details=[...rest.slice(0,-1).filter(t=>!name.startsWith(t)),source.Stitch&&`Stitching: ${source.Stitch}`,source.Suede&&`Suede: ${source.Suede}`].filter(Boolean);
    if(details.length)node('p',details.join(' · '),card);
    if(selected)node('p','Selected',card).className='selected-label';
    if(row.selectable)priceLine(card,selected,row.delta_minor);
    if(!row.selectable)node('p',row.reason,card);
    button(card,selected?'Remove interior':'Select interior',()=>run(()=>preview('interior',selected?null:row.interior_id,selected?'no interior':name)),!row.selectable);
  };
  if(leaves){matches.forEach(leaf);evenMedia(grid);return;}
  // One card per value of this level; a value with a single interior is that interior.
  const groups=new Map();matches.forEach(r=>{const v=r.levels[depth];if(!groups.has(v))groups.set(v,[]);groups.get(v).push(r);});
  // Seats follow the seat options' order; one this trim does not offer stays in
  // its place, marked with the trims that do.
  let values=[...groups.keys()];
  if(depth===0){const offered=new Set(values.map(seatFor));values=[...seats.map(c=>offered.has(c)?values.find(v=>seatFor(v)===c):c),...values.filter(v=>!seatFor(v))];}
  for(const v of values) {
    if(typeof v!=='string'){unoffered(v);continue;}
    const members=groups.get(v), seat=depth===0?seatFor(v):null;
    if(!seat&&members.length===1){leaf(members[0]);continue;}
    const card=node('article','',grid), mine=members.find(r=>r.interior_id===current.build.interior_id);
    card.className=`choice-card ${mine?'selected':''}`;
    // A color shows its first interior's swatch.
    if(seat)media(photos.get(seat.option_id),seat.label,card);
    else media(swatch(model.interiors[members[0].interior_id].source),v,card);
    node('span',seat?.rpo||['Seats','Color','Material','Finish'][depth]||'Interior',card).className='rpo';
    node('h4',seat?.label||v,card);
    node('p',`${members.length} ${members.length===1?'choice':'choices'}`,card);
    if(mine)node('p',`Your interior: ${mine.levels.slice(depth+1).at(-1)||mine.levels.at(-1)}`,card).className='selected-label';
    button(card,`See ${members.length===1?'this choice':`${members.length} choices`}`,()=>move([...interiorPath.slice(0,depth),v])).className='ghost-button';
  }
  evenMedia(grid);
}
function renderSummary() {
  // Selections by summary section (as the existing form's summary), then charges
  // the shopper did not choose, then everything the trim includes in one list,
  // then the rest of the standard equipment, collapsed.
  const b=current.build, recap=el('recap'), cfg=model.configurations[b.configuration_id];recap.replaceChildren();
  const price=new Map(b.charges.filter(c=>c.owner_kind==='option').map(c=>[c.owner_id,c.amount_minor]));
  const line=(item,parent)=>{const li=node('li','',parent);node('span',`${item.rpo?item.rpo+' ':''}${item.label}`,li);const m=price.get(item.option_id);if(m)node('span',money(m),li).className='recap-price';};
  const group=(title,items,parent=recap)=>{if(!items.length)return;node('h4',title,parent);const ul=node('ul','',parent);ul.className='recap-list';items.forEach(i=>line(i,ul));};
  const chosen=b.summary_items.filter(i=>i.step_key!=='standard_equipment');
  // Z06/ZR1/ZR1X map their standard equipment into the summary bucket; the
  // other models do not, so fall back to the build's standard-equipment
  // projection instead of leaving their review without any standard items.
  // The option contexts still mark trim equipment for those models, so the
  // projection is classified the same way (step and trim-equipment group).
  const ctx=contexts();
  const standard=b.summary_items.some(i=>i.step_key==='standard_equipment') ? b.summary_items.filter(i=>i.step_key==='standard_equipment')
    : (b.informational_standard_equipment||[]).map(i=>({...i,...ctx.get(i.option_id)})).filter(i=>i.step_key==='standard_equipment');
  for(const section of model.presentation.order_summary_sections.filter(r=>active(r.active)).sort((a,c)=>a.display_order-c.display_order)) {
    const items=chosen.filter(i=>i.summary_section_id===section.section_key);
    if(section.section_key==='seats_interior' && b.selected_interior) {
      const levels=JSON.parse(model.interiors[b.interior_id].hierarchy.interior_hierarchy_levels).slice(1);
      group(section.section_label,[{label:`Interior: ${[...new Set(levels)].join(' · ')}`,rpo:null,option_id:null},...items]);
    } else group(section.section_label,items);
  }
  const shown=new Set(chosen.map(i=>i.option_id));
  group('Charges',standard.filter(i=>price.get(i.option_id)));
  group(`${cfg.trim_level.toUpperCase()} equipment`,standard.filter(i=>i.standard_equipment_group_type==='trim_equipment'));
  const rest=standard.filter(i=>i.standard_equipment_group_type!=='trim_equipment' && !price.get(i.option_id) && !shown.has(i.option_id));
  if(rest.length){const d=node('details','',recap);node('summary',`Standard equipment (${rest.length})`,d);const ul=node('ul','',d);ul.className='recap-list';rest.forEach(i=>line(i,ul));}
  el('requirements').replaceChildren();b.missing_requirements.forEach(text=>node('li',text,el('requirements')));el('requirementsPanel').hidden=!b.missing_requirements.length;
  el('exportHint').textContent=b.missing_requirements.length?'Complete the required selections above to download your build or continue to the dealer form.':'Download saves a build file. The dealer form lets you review your request before sending.';
}
// Each option's section and step in the chosen configuration.
function contexts() {
  const cfg=current.build.configuration_id;
  return new Map(model.option_contexts.filter(c=>c.configuration_id===cfg).map(c=>[c.option_id,c]));
}
// Ask first only when a choice takes away equipment outside its own section, or
// an option changes the interior. Ending independent ownership (a package takes
// over an earlier separate purchase) keeps the equipment in the build, so it
// never asks by itself. Everything else applies at once, like the existing form,
// with a notice that names what came along and offers Undo.
function asks(action,target,c) {
  if(action==='revert') return false;
  if(action!=='interior' && c.interior.before!==c.interior.after) return true;
  const ctx=contexts(), own=ctx.get(target)?.section_id;
  return c.removed.some(i=>{
    if(i.option_id===target) return false;
    const where=ctx.get(i.option_id);
    return action==='interior' ? !['seat','base_interior'].includes(where?.step_key) : where?.section_id!==own;
  });
}
let noticeTimer;
function dismissNotice() { clearTimeout(noticeTimer); el('notice').replaceChildren(); el('notice').style.transform=''; }
function announce(action,label,c) {
  const names=items=>items.map(i=>i.label).join(', ');
  const others=items=>items.filter(i=>i.label!==label);
  const price=c.delta_minor===0?'no price change':`${c.delta_minor>0?'+':'−'}${money(Math.abs(c.delta_minor))}`;
  const parts=[action==='revert'?'Undid your last change':action==='remove'?`Removed ${label}`:action==='interior'?`Interior: ${label}`:`Added ${label}`, price];
  if(others(c.removed).length && action!=='remove' && action!=='revert')parts.push(`replaces ${names(others(c.removed))}`);
  // Dependent removals that do not ask (same-section package children) still
  // leave the build, so the automatic notice names them too.
  if(action==='remove' && others(c.removed).length)parts.push(`also removes ${names(others(c.removed))}`);
  // Ended ownership matters only when the item stays in the build.
  const gone=new Set(c.removed.map(i=>i.option_id)), kept=others(c.removed_independent_ownership).filter(i=>!gone.has(i.option_id));
  if(kept.length)parts.push(`ends separate ownership of ${names(kept)}`);
  if(others(c.added).length && action!=='revert')parts.push(`also adds ${names(others(c.added))}`);
  showNotice(parts.join(' · '),action!=='revert');
}
// Every notice can be closed or swiped away and hides itself after a moment.
function showNotice(text,undoable) {
  const box=el('notice');dismissNotice();node('span',text,box);
  if(undoable){const undo=button(box,'Undo',()=>run(()=>preview('revert',null)));undo.className='notice-undo';undo.disabled=false;}
  const close=button(box,'×',dismissNotice);close.className='notice-close';close.disabled=false;close.setAttribute('aria-label','Dismiss');
  noticeTimer=setTimeout(()=>{if(!box.contains(document.activeElement))dismissNotice();},6000);
}
// Swipe the notice away (sideways or down) so it never blocks the step controls.
(()=>{
  const box=el('notice');let start=null;
  box.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;start={x:e.clientX,y:e.clientY};box.setPointerCapture(e.pointerId);clearTimeout(noticeTimer);});
  box.addEventListener('pointermove',e=>{if(!start)return;const dx=e.clientX-start.x,dy=Math.max(0,e.clientY-start.y);box.style.transform=`translate(calc(-50% + ${dx}px), ${dy}px)`;});
  const end=e=>{if(!start)return;const dx=e.clientX-start.x,dy=e.clientY-start.y;start=null;
    if(Math.abs(dx)>60||dy>30)dismissNotice();else{box.style.transform='';noticeTimer=setTimeout(dismissNotice,6000);}};
  box.addEventListener('pointerup',end);box.addEventListener('pointercancel',end);
})();
async function preview(action,target,label) {
  pending=null;el('changes').replaceChildren();
  const result=await api('/api/preview',{action,target,version:current.version}), w=result.warning,c=w.changes;
  if(!asks(action,target,c)) {
    current=await api('/api/confirm',{token:result.token,warning_sha256:result.warning_sha256,version:result.version});
    announce(action,label,c);refocus=action==='interior'?(target||current.build.interior_id):target;return;
  }
  el('warningTitle').textContent=action==='revert'?'Undo your last change?':`${action==='remove'?'Remove':'Select'} ${label}?`;
  // One plain list: what the choice takes away (the reason for asking), kept items
  // whose price changes, then what it adds. The server still confirms the exact
  // full change record; the relationship detail stays out of the customer view.
  const charges=new Map(c.charge_changes.filter(x=>(x.after||x.before).owner_kind==='option').map(x=>[(x.after||x.before).owner_id,x]));
  const amount=m=>m?money(m):'included';
  const name=item=>`${item.label}${item.rpo?` (${item.rpo})`:''}`, seen=new Set([target]);
  for(const item of c.removed) {
    if(seen.has(item.option_id))continue;seen.add(item.option_id);node('li',`Removes ${name(item)}`,el('changes'));
  }
  for(const item of c.removed_independent_ownership) {
    if(seen.has(item.option_id))continue;seen.add(item.option_id);
    node('li',`Ends separate ownership of ${name(item)}; it stays in your build`,el('changes'));
  }
  if(c.interior.before!==c.interior.after)node('li',`Interior: ${current.cards.interiors.find(i=>i.interior_id===c.interior.after)?.label||'No interior selected'}`,el('changes'));
  const added=new Set(c.added.map(i=>i.option_id));
  for(const [id,x] of charges) {
    if(seen.has(id)||added.has(id)||!x.before||!x.after||x.before.amount_minor===x.after.amount_minor)continue;
    node('li',`${model.options[id]?.name||'Price'}: ${amount(x.before.amount_minor)} → ${amount(x.after.amount_minor)}`,el('changes'));
  }
  // Factory equipment the choice swaps out (e.g. Z51 replaces G0J, JL9, M1L, XFN).
  const swapped=c.installed_removed.filter(i=>!seen.has(i.option_id)&&!c.removed.some(r=>r.option_id===i.option_id));
  if(swapped.length)node('li',`Replaces standard equipment: ${swapped.map(name).join(', ')}`,el('changes'));
  const extra=c.added.filter(item=>item.option_id!==target);
  const included=c.installed_added.filter(i=>i.option_id!==target&&!added.has(i.option_id));
  const adds=[...extra,...included];
  if(adds.length){const li=node('li','',el('changes')),d=node('details','',li);node('summary',`Also adds ${adds.length} item${adds.length===1?'':'s'}`,d);const ul=node('ul','',d);
    adds.forEach(item=>{const x=charges.get(item.option_id)?.after;node('li',name(item)+(x?.amount_minor?` · ${money(x.amount_minor)}`:''),ul);});}
  for(const line of w.lines.filter(line=>line.startsWith('Selecting this hash mark')))node('li',line,el('changes'));
  el('priceChange').textContent=`Total MSRP ${money(c.total_after_minor)} (${c.delta_minor===0?'no price change':`${c.delta_minor>0?'+':'−'}${money(Math.abs(c.delta_minor))}`})`;
  pending={...result,choice:{action,label,target}};el('warning').showModal();el('cancel').focus();
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
  const {choice,warning}=pending;current=await api('/api/confirm',{token:pending.token,warning_sha256:pending.warning_sha256,version:pending.version});pending=null;el('warning').close();announce(choice.action,choice.label,warning.changes);el('stepTitle').focus();
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
    if(r.notice)showNotice(r.notice);
  } catch(e) {
    // A build that cannot be replayed on this catalog starts over; an outage keeps it for later.
    if(e.message===UNAVAILABLE) throw e;
    keep(null);showNotice('Your saved build could not be reopened. Please start a new build.');
  }
}
// Interior material swatches (swatches/interior/index.json), keyed by interior
// code plus any stitching and two-tone codes (HTE-36S, HU1-TU7, HU0-38S-TU7);
// the most specific one wins, and an interior without any keeps the framed code.
let swatches={};
fetch('swatches/interior/index.json').then(r=>r.ok?r.json():null).then(d=>{
  swatches=d?.swatches||{};if(current&&activeStep==='interior')renderInteriors();
}).catch(()=>{});
function swatch(source) {
  const code=source['Interior Code'], stitch=source.Stitch, tone=source['Two Tone'];
  const keys=[[code,stitch,tone].filter(Boolean).join('-'),tone&&`${code}-${tone}`,stitch&&`${code}-${stitch}`,code];
  const s=keys.map(k=>k&&swatches[k]).find(Boolean);
  return s&&{image_url:`swatches/interior/${s.file}`,image_fit:'cover'};
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
