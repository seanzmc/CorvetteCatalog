'use strict';
window.catalogArtwork = (() => {
  let signature = '', generation = 0;
  const el = id => document.getElementById(id);
  async function render(view) {
    const next=JSON.stringify([view.release_id,view.coverage,view.scene_id,view.rpo,view.label,view.paint_rpo,view.paint_label,
      view.notice,view.limitations,view.assets,view.reason]);
    if(next===signature) return;
    signature=next; const version=++generation;
    const stage=el('artworkStage'); stage.replaceChildren(); stage.hidden=true;
    el('artworkLimitations').replaceChildren();
    el('artworkLimitations').parentElement.hidden = !view.limitations?.length;
    if(view.coverage!=='component_preview') {
      el('artworkStatus').textContent=view.reason || 'Artwork is not available for this build yet.';
      return;
    }
    el('artworkStatus').textContent='Loading spoiler artwork…';
    for(const text of view.limitations) {
      const li=document.createElement('li');li.textContent=text;el('artworkLimitations').append(li);
    }
    try {
      const images=await Promise.all(view.assets.map(async asset=>{
        const image=new Image(asset.width,asset.height);
        image.alt=''; image.src=asset.url.replace(/^\//,''); // relative: a static bundle may sit in a folder
        await image.decode(); return image;
      }));
      if(version!==generation) return;
      stage.setAttribute('aria-label',`${view.rpo} ${view.label}. ${view.paint_label}. ${view.notice}`);
      stage.replaceChildren(...images); stage.hidden=false;
      el('artworkStatus').textContent=`${view.paint_label}. ${view.rpo} — ${view.label}. ${view.notice}`;
    } catch (_) {
      if(version!==generation) return;
      signature='';
      stage.replaceChildren();stage.hidden=true;
      el('artworkStatus').textContent='Spoiler artwork could not load. Your confirmed build is unchanged.';
    }
  }
  return {render};
})();
