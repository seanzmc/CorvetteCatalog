"""Execute the page's real review, photo lookup and Markdown against catalog builds."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

from catalog import dealer
from catalog.consumers import ConsumerSession
from catalog.evaluator import EvaluationError
import test_consumers as base

ROOT = Path(__file__).resolve().parents[1]
CHECK = r"""
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const data=JSON.parse(fs.readFileSync(0,'utf8'));
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.dataset={};this.style={};this.textContent='';}
  append(child){this.children.push(child);}
  replaceChildren(){this.children=[];}
  setAttribute(){} addEventListener(){} querySelector(){return null;}
}
const elements=new Map();
const el=id=>{if(!elements.has(id))elements.set(id,new Element('div'));return elements.get(id);};
const context=vm.createContext({console,Intl,URL,Blob,setTimeout,clearTimeout,data,
  document:{getElementById:el,createElement:tag=>new Element(tag)},
  localStorage:{getItem:()=>null},fetch:()=>new Promise(()=>{}),
  catalogDealer:{init(){}},catalogEngine:{call:()=>new Promise(()=>{})}});
vm.runInContext(fs.readFileSync('catalog/web/app.js','utf8'),context);
const text=n=>[n.textContent,...n.children.map(c=>typeof c==='string'?c:text(c))].join(' ');
const rows=n=>n.children.flatMap(c=>typeof c==='string'?[]:c.tag==='li'?[c]:rows(c));
for(const fixture of data.cases){
  context.fixture=fixture;
  vm.runInContext('model=data.models[fixture.key]; current={build:fixture.build}; renderSummary()',context);
  const reviewRows=rows(el('recap'));
  const charged=reviewRows.filter(r=>r.children.some(n=>n.className==='recap-price'));
  const amounts=charged.map(r=>Number(r.children.find(n=>n.className==='recap-price').textContent.replace(/[$,]/g,''))*100);
  const expected=fixture.build.charges.filter(c=>c.owner_kind!=='configuration'&&c.amount_minor);
  assert.equal(amounts.reduce((a,b)=>a+b,0),expected.reduce((a,b)=>a+b.amount_minor,0),fixture.label);
  assert.equal(charged.length,expected.length,'each charge occurs once: '+fixture.label);
  for(const c of expected.filter(c=>c.owner_kind==='component')){
    const part=fixture.build.selected_interior.configured_components.find(p=>p.component?.id===c.owner_id);
    assert.equal(charged.filter(r=>text(r).includes(part.component.code)).length,1,fixture.label+' '+part.component.code);
  }
  const md=vm.runInContext('buildMarkdown(fixture.order,model.presentation.model_master[0])',context);
  assert.ok(md.includes('- Model base MSRP: '+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0}).format(fixture.order.vehicle.base_price)));
  assert.ok(md.includes('- Total MSRP: '+fixture.order.msrp));
}
// A display-only brake remains visible before and after the engine includes it.
context.fixture=data.brakes;
vm.runInContext('model=data.models.zr1; current={cards:{options:fixture.cards}}',context);
const brakeCards=vm.runInContext('choiceCards()',context);
const brake=brakeCards.find(c=>c.rpo==='J59');
assert.ok(brake);assert.equal(brake.selectable,false);assert.equal(brake.section_label,'Performance Brakes');
// A correction must win over even a populated, wrong baseline row; other photos retain their precedence.
vm.runInContext(`catalog={models:{zr1:model}};correctedPhotos={zr1:{J59:{image_url:'correct.jpg'}}};
  model.presentation.asset_map=[{target_type:'option',target_id:fixture.id,image_url:'wrong.jpg'},
  {target_type:'option',target_id:'untouched',image_url:'kept.jpg'}];`,context);
assert.equal(vm.runInContext('assetsFor(model).option.get(fixture.id).image_url',context),'correct.jpg');
assert.equal(vm.runInContext("assetsFor(model).option.get('untouched').image_url",context),'kept.jpg');
assert.match(vm.runInContext("buildMarkdown({vehicle:{base_price:108745},sections:[],msrp:'$108,745'},{model_year:2027,model_label:'Grand Sport'})",context),/Model base MSRP: \$108,745/);
console.log(data.cases.length+' real build recaps reconcile; base price, display-only brake and photo precedence pass');
"""


@unittest.skipUnless(shutil.which('node'), 'Node required for real page checks')
class FormReviewTests(unittest.TestCase):
    setUpClass = classmethod(base.ConsumerTests.setUpClass.__func__)
    tearDownClass = classmethod(base.ConsumerTests.tearDownClass.__func__)

    def test_review_download_and_photo_resolution(self):
        cases=[]
        for key,cat in self.catalogs.items():
            paint=next(o['id'] for o in cat.ev.options.values() if o['rpo']=='GBA')
            for cfg in cat.ev.configs:
                candidates=[]
                for iid in cat.ev.interiors:
                    if (iid,cfg) not in cat.ev.interior_scopes: continue
                    try:
                        state=cat.ev.state(cfg,(paint,),iid)
                    except EvaluationError: continue
                    if set(state.issues)-{'partial_catalog_not_submission_ready'}: continue
                    candidates.append(state)
                # Exercise the most expensive component combination in every body/trim.
                state=max(candidates,key=lambda s:sum(c.amount_minor for c in s.charges if c.owner_kind=='component'))
                session=ConsumerSession(cat,cfg,'test')
                for action,target in [('select',paint),('interior',state.interior_id)]:
                    p=session.preview(action,target,session.version);session.confirm(p['token'],p['warning_sha256'],p['version'])
                cases.append(dict(key=key,label=key+' '+cfg,build=session.order(),order=dealer.review(session,session.version)))
        cat=self.catalogs['zr1']; cfg=next(iter(cat.ev.configs));oid=next(o['id'] for o in cat.ev.options.values() if o['rpo']=='J59')
        data=dict(models={k:c.contract() for k,c in self.catalogs.items()},cases=cases,
                  brakes=dict(id=oid,cards=cat.cards(cat.ev.state(cfg),['packages_performance'])['options']))
        result=subprocess.run(['node','-e',CHECK],input=json.dumps(data),capture_output=True,text=True,cwd=ROOT,timeout=30)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

if __name__=='__main__': unittest.main()
