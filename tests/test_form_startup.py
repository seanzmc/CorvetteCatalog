"""Execute the real page startup with a delayed restore and a minimal DOM."""
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECK = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const mode = process.argv[1];
const html = fs.readFileSync('catalog/web/index.html', 'utf8');
class Element {
  constructor(tag) { this.tag=tag; this.children=[]; this.dataset={}; this.style={}; this.disabled=false; this.inert=false; this.selected=''; }
  get value() { return this.selected || this.children[0]?.value || ''; }
  set value(value) { this.selected=value; }
  get options() { return this.children; }
  append(child) { this.children.push(child); }
  replaceChildren() { this.children=[]; this.selected=''; }
  setAttribute() {}
  addEventListener() {}
  querySelector() { return null; }
  focus() {}
}
const elements=new Map();
for (const match of html.matchAll(/<(\w+)\b([^>]*\bid="([^"]+)"[^>]*)>/g)) {
  const element=new Element(match[1]);
  element.disabled=/\bdisabled\b/.test(match[2]);
  element.inert=/\binert\b/.test(match[2]);
  elements.set(match[3],element);
}
const pageModel=(label,prefix)=>({display_order:1,options:{},presentation:{asset_map:[],runtime_steps:[],model_master:[{model_label:label}]},
  configurations:{[prefix+'1']:{active:true,body_style:'coupe',trim_level:'1lt',base_price:74595,display_order:1},
                  [prefix+'2']:{active:true,body_style:'coupe',trim_level:'2lt',base_price:81795,display_order:2}}});
const catalog={release_id:'test',default_model:'stingray',dealer:{enabled:false},
  models:{stingray:pageModel('Stingray','st'),grand_sport:pageModel('Grand Sport','gs')}};
const restored={model:'grand_sport',configuration_id:'gs2',build:{configuration_id:'gs2'},card_steps:[],cards:{options:[],interiors:[]}};
let stored=mode==='fresh'?null:'saved-build', resolveRestore, restoreCalls=0;
const delayed=new Promise(resolve=>resolveRestore=resolve);
const context=vm.createContext({console,Intl,URL,Blob,setTimeout:()=>0,clearTimeout:()=>{},
  document:{getElementById:id=>elements.get(id),createElement:tag=>new Element(tag)},
  localStorage:{getItem:()=>stored,setItem:(_,value)=>stored=value,removeItem:()=>stored=null},
  fetch:async()=>({ok:false}), catalogDealer:{init(){}},
  catalogEngine:{warm(){},async call(path){
    if(path==='/api/catalog')return {status:200,result:catalog};
    if(path==='/api/restore'){restoreCalls++;return delayed;}
    if(path==='/api/cards')return {status:200,result:restored};
    throw new Error('Unexpected startup request: '+path);
  }}});
vm.runInContext(fs.readFileSync('catalog/web/app.js','utf8'),context);
// Rendering is outside this startup test; model/trim setup and restoration are real.
vm.runInContext('render=()=>{}',context);
const tick=()=>new Promise(resolve=>setImmediate(resolve));
(async()=>{
  await tick();
  if(mode==='fresh'){
    assert.equal(restoreCalls,0);
    assert.equal(elements.get('setup').inert,false);
    assert.equal(elements.get('start').disabled,false);
    return;
  }
  assert.equal(restoreCalls,1);
  assert.equal(elements.get('setup').inert,true,'setup must not accept a competing model choice');
  assert.equal(elements.get('start').disabled,true,'a new session must wait for restore');
  resolveRestore(mode==='outage'?{status:503,result:{}}:mode==='stale'?{status:400,result:{error:'stale build'}}:{status:200,result:restored});
  await tick();
  if(mode==='outage'){
    assert.equal(elements.get('setup').inert,true);
    assert.equal(elements.get('start').disabled,true);
    assert.equal(stored,'saved-build');
    assert.match(elements.get('error').textContent,/temporarily unavailable/);
  }else{
    assert.equal(elements.get('setup').inert,false);
    assert.equal(elements.get('start').disabled,false);
    if(mode==='stale')assert.equal(stored,null);
    else{
      assert.equal(elements.get('model').value,'grand_sport');
      assert.equal(elements.get('configuration').value,'gs2');
      assert.equal(elements.get('startingPrice').textContent,'Starting MSRP $81,795.00');
    }
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
"""


@unittest.skipUnless(shutil.which('node'), 'Node is required to execute page JavaScript')
class FormStartupTests(unittest.TestCase):
    def test_startup_and_saved_build_outcomes(self):
        for mode in ('fresh', 'restored', 'stale', 'outage'):
            with self.subTest(mode=mode):
                result = subprocess.run(['node', '-e', CHECK, mode], cwd=ROOT,
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
