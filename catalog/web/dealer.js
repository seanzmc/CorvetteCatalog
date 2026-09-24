'use strict';
// Contact details stay in this page. Only the confirmed server build supplies
// order identities and prices; the existing dealer receiver verifies Turnstile.
window.catalogDealer = (() => {
  const byId = id => document.getElementById(id);
  let context, sending = false, token = '', widget, loading, activeBuild, receipt;
  const fields = ['Name', 'Email', 'Phone', 'Comments'];
  const message = text => { byId('dealerStatus').textContent = text; };
  const live = () => !!context.state().catalog?.dealer.enabled;
  const identity = () => { const s=context.state(); return `${s.buildToken}:${s.current?.version}`; };
  const textNode = (tag, text, parent) => { const n=document.createElement(tag); n.textContent=text; parent.append(n); return n; };

  function resetSecurity() {
    token = '';
    if (widget !== undefined && window.turnstile) window.turnstile.reset(widget);
  }
  function sync() {
    const state = context.state(), changed = activeBuild !== identity();
    if (changed) {
      activeBuild = identity(); receipt = null; resetSecurity();
      byId('dealerPreview').hidden = true; byId('dealerPayload').textContent = ''; message('');
    }
    byId('dealerOpen').textContent = live() ? (receipt ? 'View submission receipt' : 'Submit to dealer') : 'Preview dealer submission';
    byId('dealerOpen').disabled = sending || state.busy || !!state.pending || !state.current ||
      state.current.build.issues.some(i=>i!=='partial_catalog_not_submission_ready');
    byId('dealerClose').disabled = sending;
    byId('dealerSend').textContent = sending ? 'Please wait…' : live() ? 'Submit to dealer' : 'Preview submission';
    byId('dealerSend').disabled = sending || !!receipt || (live() && !token);
    fields.forEach(f=>{byId('dealer'+f).disabled = sending || !!receipt;});
  }
  async function security() {
    if (!live()) return;
    if (!window.turnstile) {
      if (!loading) loading = new Promise((resolve, reject) => {
        const script=document.createElement('script');
        script.src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
        script.onload=resolve;
        script.onerror=()=>{ script.remove(); loading=null; reject(new Error('Security check could not load. Close this window and try again.')); };
        document.head.append(script);
      });
      await loading;
    }
    if (widget === undefined) widget=window.turnstile.render(byId('dealerSecurity'), {
      sitekey:context.state().catalog.dealer.site_key,
      callback:value=>{token=value; message('Security check complete.'); sync();},
      'expired-callback':()=>{token=''; message('Security check expired. Please complete it again.'); sync();},
      'error-callback':()=>{token=''; message('Security check failed. Please try again.'); sync();}
    });
    else resetSecurity();
  }
  async function open() {
    const state = context.state();
    const order = await context.api('/api/dealer/review', {version:state.current.version});
    sync();
    const summary=byId('dealerSummary'); summary.replaceChildren();
    textNode('h3', order.vehicle.display_name, summary);
    textNode('p', `Total MSRP: ${order.msrp}`, summary);
    const details=textNode('details', '', summary); textNode('summary','Order details',details);
    for (const section of order.sections) {
      textNode('h4', section.section, details); const ul=textNode('ul','',details);
      section.items.forEach(item=>textNode('li', `${item.rpo} ${item.label}: ${new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(item.price)}`.trim(),ul));
    }
    byId('dealerMode').textContent = live()
      ? 'Form will be submitted to Stingray Chevrolet in Plant City, FL.'
      : 'Local preview only. Your contact details and build will not be sent to the dealership.';
    message(receipt || '');
    byId('dealerDialog').showModal();
    if (!receipt) {
      byId('dealerName').focus();
      try { await security(); } catch(error) { message(error.message); }
    }
    sync();
  }
  async function submit(event) {
    event.preventDefault();
    if (sending || receipt || !byId('dealerForm').reportValidity() || live() && !token) return;
    const state=context.state(), build=identity();
    sending=true; message(live() ? 'Sending your build…' : 'Preparing your preview…'); sync();
    let deliveryStarted=false;
    try {
      const customer={}; fields.forEach(f=>{customer[f.toLowerCase()]=byId('dealer'+f).value.trim();});
      const prepared=await context.api('/api/dealer/prepare', {version:state.current.version,customer,turnstile_token:token});
      if (build !== identity() || prepared.version !== state.current.version || prepared.release_id !== state.catalog.release_id ||
          prepared.revision_id !== state.current.build.revision_id)
        throw new Error('The build changed. Close this window and review the current build.');
      if (!live()) {
        byId('dealerPayload').textContent=JSON.stringify(prepared.payload,null,2);
        byId('dealerPreview').hidden=false; byId('dealerPreview').open=true;
        message('Preview ready. Nothing has been sent to the dealership.');
        return;
      }
      deliveryStarted=true;
      const controller=new AbortController(), timeout=setTimeout(()=>controller.abort(),30000);
      let response, result;
      try {
        response=await fetch(state.catalog.dealer.endpoint, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(prepared.payload),signal:controller.signal});
        try { result=await response.json(); } catch (error) {
          if (error.name === 'AbortError') throw error;
          throw new Error('The dealer returned an unreadable response.');
        }
      } finally { clearTimeout(timeout); }
      if (!response.ok || !result || result.success !== true) throw new Error(result?.message || 'The dealer could not confirm your submission.');
      receipt='Your build was submitted to Stingray Chevrolet.' + (result.entry_id ? ` Reference: ${result.entry_id}.` : '');
      message(receipt);
    } catch (error) {
      const reason=error.name === 'AbortError' ? 'The dealer response timed out.' : error.message;
      message(`${reason}${deliveryStarted ? ' Delivery may have completed; check with the dealership before retrying.' : ''}`);
    } finally {
      sending=false; if (live() && !receipt) resetSecurity(); sync();
    }
  }
  function close() { if (!sending) { byId('dealerDialog').close(); token=''; sync(); } }
  function init(value) {
    context=value;
    byId('dealerForm').addEventListener('submit', submit);
    byId('dealerClose').addEventListener('click', close);
    byId('dealerDialog').addEventListener('cancel', event=>{event.preventDefault(); close();});
  }
  return {init, open, sync};
})();
