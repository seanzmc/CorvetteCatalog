// Read-only behavior discovery against the immutable browser baseline.
// Usage: node scripts/discovery_catchup.mjs OUTPUT_DIRECTORY [REFERENCE_REPO]
// Existing observations are never overwritten by default; choose a new output directory.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const root=path.resolve(import.meta.dirname,'..');
assert(process.argv[2], 'Supply a new output directory');
const output=path.resolve(process.argv[2]);
const reference=process.argv[3] || '/Users/seandm/Projects/27vette';
const manifest=JSON.parse(fs.readFileSync(path.join(root,'baselines/2026-09-06/manifest.json')));
const hash=x=>createHash('sha256').update(x).digest('hex');
const plain=x=>JSON.parse(JSON.stringify(x));
const scratch=fs.mkdtempSync(path.join(os.tmpdir(),'discovery-catchup-'));
const prior=process.cwd();
fs.mkdirSync(output,{recursive:true});
try {
  fs.mkdirSync(path.join(scratch,'form-app'));
  const sourceHashes={};
  for(const name of ['app.js','data.js']) {
    const member='form-app/'+name;
    const bytes=execFileSync('tar',['-xOf',path.join(root,'baselines/2026-09-06',manifest.archive.path),member],{maxBuffer:20*1024*1024});
    assert.equal(hash(bytes),manifest.files.find(x=>x.path===member).sha256);
    sourceHashes[member]=hash(bytes);fs.writeFileSync(path.join(scratch,member),bytes);
  }
  const originalHarness=execFileSync('git',['-C',reference,'show',manifest.reference_commit+':tests/lib/runtime-harness.mjs']);
  const harness=originalHarness.toString().replace('  activeChoiceRows,','  activeChoiceRows, setBodyAndTrim, lineItems, standardEquipmentRows, handleInterior, disableReasonForInterior, validInteriorsForSelectedSeat, shouldHideChoice,');
  assert.notEqual(harness,originalHarness.toString());
  fs.writeFileSync(path.join(scratch,'harness.mjs'),harness);
  process.chdir(scratch);
  const {loadRuntime}=await import(pathToFileURL(path.join(scratch,'harness.mjs')));
  for(const [model,key] of [['stingray','stingray'],['grand-sport','grandSport'],['grand-sport-x','grand_sport_x'],['z06','z06']]) {
    const file=path.join(output,model+'-runtime.json');assert(!fs.existsSync(file),'Refusing to overwrite '+file);
    const rt=loadRuntime();rt.activateModel(key,{shouldRender:false});
    const records=JSON.parse(fs.readFileSync(path.join(root,'docs',model+'-structured-records.json')));
    const rpo=id=>rt.data.choices.find(x=>x.option_id===id)?.rpo || id;
    const row=code=>rt.activeChoiceRows().find(x=>x.rpo===code);
    function choose(code) {
      const r=row(code);
      if(!r)return {code,outcome:'absent_from_active_model'};
      const hidden=rt.shouldHideChoice(r), reason=rt.disableReasonForChoice(r);
      if(hidden || reason || r.selectable!=='True')return {code,id:r.option_id,hidden,reason,outcome:'not_selectable'};
      rt.handleChoice(r);return {code,id:r.option_id,outcome:'attempted'};
    }
    function start(body,trim,complete=true) {
      trim=trim.toUpperCase();
      rt.setBodyAndTrim(body,trim);
      if(complete) {
        choose('G8G');
        const code=trim.startsWith('1')?'HTA':trim.startsWith('2')?'H1Y':'HTE';
        const interior=rt.validInteriorsForSelectedSeat().find(x=>x.interior_code===code);
        assert(interior,`${model} ${body} ${trim}: ordinary interior missing`);
        rt.handleInterior(interior);assert.equal(rt.missingRequired().length,0);
      }
    }
    function snapshot() {
      const order=plain(rt.currentOrder()),compact=plain(rt.compactOrder());
      const item=x=>Object.fromEntries(['id','rpo','price','type','section_key','step_key'].filter(k=>k in x).map(k=>[k,x[k]]));
      return {selected:[...rt.state.selected].map(rpo),automatic:[...rt.computeAutoAdded().keys()].map(rpo),
        interior:rt.state.selectedInterior,items:plain(rt.lineItems()).map(item),total:order.pricing.total_msrp,
        missing:plain(rt.missingRequired()),submit_disabled:rt.elements.get('#submitDealerButton')?.disabled,
        informational_equipment:plain(rt.standardEquipmentRows()).map(x=>x.equipment_id),
        order:{variant_id:order.vehicle.variant_id,pricing:order.pricing,sections:order.sections.map(s=>({section_key:s.section_key,section_total:s.section_total,items:s.items.map(item)}))},compact};
    }
    const variants=records.baseline_rows.variant_master;
    const options=[],foundations=[],sequences=[],notApplicable=[];
    const modelCodes=new Set(records.offering_dispositions.map(x=>x.rpo));
    for(const v of variants) {
      const body=v.body_style,trim=v.trim_level;
      start(body,trim,false);foundations.push({variant_id:v.variant_id,body,trim,state:snapshot()});
      for(const c of plain(rt.activeChoiceRows())) {
        start(body,trim,false);
        const hidden=rt.shouldHideChoice(c),reason=rt.disableReasonForChoice(c);
        const attempted=!hidden&&!reason&&c.selectable==='True';
        if(attempted)rt.handleChoice(c);
        options.push({variant_id:v.variant_id,id:c.option_id,rpo:c.rpo,status:c.status,hidden,reason,attempted,
          selected:[...rt.state.selected].map(rpo),automatic:[...rt.computeAutoAdded().keys()].map(rpo),missing:plain(rt.missingRequired())});
      }
    }
    function run(name,body,trim,actions) {
      const absent=actions.filter(c=>!modelCodes.has(c));
      if(absent.length){notApplicable.push({name,body,trim,actions,absent_codes:[...new Set(absent)],reason:'No such baseline offering in this model; no cross-model identity inferred'});return;}
      start(body,trim);const initial=snapshot(),states=[];
      for(const code of actions)states.push({action:choose(code),state:snapshot()});
      const anchors=records.offering_dispositions.filter(r=>actions.includes(r.rpo)).flatMap(r=>r.guide_anchors);
      sequences.push({id:`${model}-C${String(sequences.length+1).padStart(3,'0')}`,name,body,trim,source_anchors:[...new Set(anchors)],initial,states});
    }
    const middle=model==='z06'?'2LZ':'2LT';
    // Complete listed stripe/paint prohibitions: different models still retain their own anchors/results.
    const prohibited={DUE:['GTR'],DPB:['GTR'],DPC:['GBK'],DT0:['GBK'],DZU:['GBK'],DPG:['G26'],DSY:['G26'],DPL:['GKZ','GPH'],DSZ:['GKZ','GPH'],DUK:['GKZ','GPH'],DZX:['GKZ','GPH']};
    for(const body of ['coupe','convertible']) {
      for(const [stripe,paints] of Object.entries(prohibited))for(const paint of paints)
        for(const reverse of [false,true])run('stripe/paint prohibition',body,middle,reverse?[stripe,paint]:[paint,stripe]);
      if(model==='grand-sport-x')for(const reverse of [false,true])run('existing DTC/paint prohibition',body,middle,reverse?['DTC','GTR']:['GTR','DTC']);
      for(const [packageCode,child] of [[model==='stingray'?'PCU':'PCQ','VWE'],['PEF','CAV'],['PDY','RYT'],['PDA','SNE']]) {
        run('independent child before package and removal',body,middle,[child,packageCode,packageCode]);
        run('package before child and removal',body,middle,[packageCode,child,packageCode]);
      }
      for(const roof of ['D84','D86'])if(body==='convertible') {
        run('roof then conflicting paint',body,middle,[roof,'GBA']);
        run('paint then conflicting roof',body,middle,['GBA',roof]);
      }
      for(const accent of ['EFY','EDU']) {
        run('accent then paint',body,middle,[accent,'GBA']);
        run('paint then accent',body,middle,['GBA',accent]);
      }
      if(body==='coupe') {
        run('independent pouch before dual roof',body,middle,['SC7','SBT','SBT']);
        run('dual roof before pouch',body,middle,['SBT','SC7','SBT']);
      }
      for(const graphic of ['VPW','VPO','SFZ']) {
        run('graphic then stripe',body,middle,[graphic,'DPB']);
        run('stripe then graphic',body,middle,['DPB',graphic]);
      }
    }
    // Multiple causes must survive loss of either supplier, then disappear on last-cause loss.
    for(const order of [['5JR','ZYC','5JR','ZYC'],['ZYC','5JR','ZYC','5JR']])
      run('mirror multiple causes','coupe',model==='z06'?'3LZ':'3LT',order);
    if(model!=='z06')for(const cover of ['BC4','BCP','BCS']) {
      run('cover before appearance package','coupe',middle,[cover,'B6P','B6P',cover]);
      run('appearance package before cover','coupe',middle,['B6P',cover,'B6P',cover]);
      run('convertible prerequisite acquisition and loss','convertible',middle,[cover,'ZZ3',cover,'ZZ3']);
    }
    if(model==='stingray') {
      for(const v of variants)run('Z51 equipment and removal',v.body_style,v.trim_level,['Z51','FE4','Z51']);
      run('PCX paid alternatives and removal','coupe',middle,['PCX','5DO','SHW','PCX']);
      run('PDV independent cap and removal','coupe',middle,['5ZD','PDV','PDV']);
    } else if(model==='grand-sport') {
      for(const v of variants) {
        run('track package supply and removal',v.body_style,v.trim_level,['FEY','FEY']);
        run('sport package brake dependency loss',v.body_style,v.trim_level,['FEB','J57','T0F','FEB']);
      }
    } else if(model==='grand-sport-x') {
      for(const v of variants)run('FED equipment round trip',v.body_style,v.trim_level,['FED','FED']);
    } else {
      for(const v of variants)run('Z07 equipment round trip',v.body_style,v.trim_level,['Z07','J6D','Z07']);
      run('PCZ content acquisition and removal','coupe',middle,['5DK','PCZ','SFZ','SHT','VPO','PCZ']);
      run('convertible engine prerequisites','convertible',middle,['BCW','ZZ3','BCW','PBC','ZZ3']);
    }
    const rejection=[],seatTransitions=[];
    for(const v of variants) {
      start(v.body_style,v.trim_level);const seatAction=choose('AE4');
      seatTransitions.push({variant_id:v.variant_id,seatAction,state:snapshot()});
      start(v.body_style,v.trim_level,false);choose('G8G');
      assert(rt.missingRequired().includes('Interior Color'));
      await rt.elements.get('#dealerSubmitForm').listeners.submit({preventDefault(){}});
      rejection.push({variant_id:v.variant_id,missing:plain(rt.missingRequired()),requests:rt.fetchCalls.length});
    }
    assert.equal(rt.fetchCalls.length,0);
    const data={model_key:records.model_key,role:'Supplemental frozen-baseline discovery; not corrected target verification',
      provenance:{reference_commit:manifest.reference_commit,workbook_sha256:records.sources.workbook_sha256,
        guide_sha256:records.sources.guide_sha256,...sourceHashes,original_harness_sha256:hash(originalHarness),
        exposed_harness_sha256:hash(harness),probe_sha256:hash(fs.readFileSync(path.join(root,'scripts/discovery_catchup.mjs')))},
      projection:'Snapshots retain actual selected/automatic identities, item prices/types/routing, order pricing/section item projections, compact recap and informational equipment IDs. Copy and images remain in baseline_rows; no live customer data.',
      foundations,starting_choice_observations:options,connected_sequences:sequences,not_applicable: notApplicable,seat_transitions:seatTransitions,required_interior_rejection:rejection,live_requests:rt.fetchCalls.length};
    fs.writeFileSync(file,JSON.stringify(data,null,2)+'\n');
    console.log(model,options.length,'choice observations;',options.filter(x=>x.attempted).length,'actions;',sequences.length,'connected cases; 6 rejection cases; zero requests');
  }
} finally {process.chdir(prior);fs.rmSync(scratch,{recursive:true,force:true});}
