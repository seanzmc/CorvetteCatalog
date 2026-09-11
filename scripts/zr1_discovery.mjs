// Read-only behavior discovery against the immutable browser baseline.
// Usage: node scripts/zr1_discovery.mjs OUTPUT_DIRECTORY [REFERENCE_REPO]
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
  for(const [model,key] of [['zr1','zr1']]) {
    const file=path.join(output,model+'-runtime.json');assert(!fs.existsSync(file),'Refusing to overwrite '+file);
    const rt=loadRuntime();rt.activateModel(key,{shouldRender:false});
    const records=JSON.parse(fs.readFileSync(path.join(root,'docs/zr1-structured-records.json')));
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
    const middle='3LZ';
    const prohibited={DUE:['GTR'],DUW:['GTR'],DTC:['GTR'],DPB:['GTR'],DPC:['GBK'],DT0:['GBK'],DPG:['G26'],DSY:['G26'],DPL:['GKZ','GPH'],DSZ:['GKZ','GPH'],DUK:['GKZ','GPH']};
    for(const body of ['coupe','convertible']) {
      for(const [stripe,paints] of Object.entries(prohibited))for(const paint of paints)
        for(const reverse of [false,true])run('stripe/paint prohibition',body,middle,reverse?[stripe,paint]:[paint,stripe]);
      for(const graphic of ['SB9','SFZ','R88'])for(const stripe of ['DPB','DPC','DPG','DPL','DPT','DSY','DSZ','DT0','DTC','DTH','DUB','DUE','DUK','DUW','EYK'])
        for(const reverse of [false,true])run('graphic conflict',body,middle,reverse?[stripe,graphic]:[graphic,stripe]);
      for(const [pkg,child] of [['PCQ','VWE'],['PEF','CAV'],['PDY','RYT']]) {
        run('child before package and removal',body,middle,[child,pkg,pkg]);
        run('package before child and removal',body,middle,[pkg,child,pkg]);
      }
      for(const cover of ['RWJ','WKR']) {
        for(const aero of ['TOM','ZTK']) {
          run('cover then aero',body,middle,[cover,aero,aero]);
          run('aero then cover',body,middle,[aero,cover,aero]);
        }
      }
      for(const [a,b] of [['SFZ','SB9'],['R88','SFZ'],['FA5','BAZ']])for(const actions of [[a,b],[b,a]])run('additional grouped interaction',body,middle,actions);
      run('mirror multiple causes',body,middle,['5JR','ZYC','5JR','ZYC']);
      run('mirror reverse cause loss',body,middle,['ZYC','5JR','ZYC','5JR']);
      run('mirror paint conflict',body,middle,['ZYC','GBA']);
      run('paint mirror conflict',body,middle,['GBA','ZYC']);
      run('delivery and plaque',body,middle,['BV4','R8C','BV4','R8C']);
      run('exhaust restoration',body,middle,['NWI','NWI']);
      run('wheel hardware',body,middle,['SPY','SPZ','SPY','S47','SU1','SFE']);
      run('carbon wheels first',body,middle,['SU1','S47','SFE','SPY','SPZ','SOJ']);
      run('independent accessory groups',body,middle,['RWH','WKR','RWJ','5ZD','5ZC','RIN','RIK','SL8','SXB','SXR','SXT']);
    }
    for(const v of variants) {
      for(const actions of [
        ['ZTK','T0E','J58','ZTK'],['TOM','ZTK','ZTK','T0E'],['J59','J58'],
        ['SIG','TOM','T0E','SIG'],['J6O','ZTK','ZTK'],['SOF','SOG','SOH','SU1','SOJ'],
        ['E60','E60'],['PBC','PBC'],['FA5','FA6','FA6'],['UQT'],
        ['SLN'],['ETV','ETV'],['B6P','ZZ3'],['PCQ','VWT','R88'],
      ])run('ZR1 foundation and dependency round trip',v.body_style,v.trim_level,actions);
    }
    for(const trim of ['1LZ','3LZ']) {
      run('dual roof and independent pouch','coupe',trim,['SC7','SBT','SBT']);
      run('dual roof first','coupe',trim,['SBT','SC7','SBT']);
    }
    const interiorContexts=[],priceComparisons=[],paintStates=[],beltStates=[],causeSequences=[];
    const interiors=plain(rt.data.interiors),paints=['G26','G4Z','G8G','GBA','GBK','GEC','GKA','GKZ','GPH','GTR'],belts=['719','379','3N9','3A9','3F9','3M9'];
    const expectedPaint=new Set(records.source_reconciliation.interior_reconciliation.color_expected.map(x=>x.join('|')));
    function setInterior(i,body='coupe') {
      start(body,i.trim_level,false);choose('G8G');
      if(!rt.state.selected.has(row(i.seat_code).option_id))choose(i.seat_code);
      rt.handleInterior(i);assert.equal(rt.state.selectedInterior,i.interior_id);
    }
    for(const i of interiors) {
      for(const body of ['coupe','convertible']) {setInterior(i,body);interiorContexts.push({id:i.interior_id,body,state:snapshot()});}
      setInterior(i);
      const seatRate=i.trim_level==='1LZ'?(i.seat_code==='AE4'?1095:0):({AH2:0,AE4:595,AUP:350}[i.seat_code]);
      const extras=(i.interior_components||[]).filter(x=>x.component_type!=='seat').reduce((n,x)=>n+x.price,0);
      const actual=rt.lineItems().filter(x=>x.type==='interior_component'||x.type==='selected_interior'||x.step_key==='seat').reduce((n,x)=>n+x.price,0);
      priceComparisons.push({id:i.interior_id,seatRate,componentTotal:extras,expected:seatRate+extras,actual,difference:actual-seatRate-extras});
      for(const paint of paints) {setInterior(i);choose(paint);paintStates.push({id:i.interior_id,paint,expected_d30:expectedPaint.has(i.interior_id+'|'+paint),actual_d30:[...rt.computeAutoAdded().keys()].map(rpo).includes('D30'),total:rt.currentOrder().pricing.total_msrp});}
      for(const belt of belts) {setInterior(i);const action=choose(belt);beltStates.push({id:i.interior_id,belt,action,selected:[...rt.state.selected].map(rpo),automatic:[...rt.computeAutoAdded().keys()].map(rpo),items:plain(rt.lineItems()).filter(x=>belts.includes(x.rpo)||x.rpo==='D30').map(x=>({rpo:x.rpo,price:x.price}))});}
    }
    for(const actions of [['G26','379','G8G','3F9'],['G26','379','3F9','G8G']]) {
      const i=interiors.find(x=>x.interior_code==='HUQ'&&x.trim_level==='1LZ');setInterior(i);
      const states=[];for(const code of actions)states.push({action:choose(code),state:snapshot()});causeSequences.push({name:'D30 independent paint and belt causes',actions,states});
    }
    start('coupe','3LZ');choose('ZTK');const beforeReset=snapshot();rt.setBodyAndTrim('convertible','1LZ');const contextReset={before:beforeReset,after:snapshot()};
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
    assert.equal(interiors.length,90);
    assert.equal(options.length,800);
    assert.deepEqual([...new Set(options.map(x=>x.id))].sort(),records.baseline_rows.zr1_options.filter(x=>x.active&&x.display_behavior!=='hidden').map(x=>x.option_id).sort());
    assert(paintStates.every(x=>x.expected_d30===x.actual_d30));
    assert.deepEqual(priceComparisons.filter(x=>x.difference).map(x=>[x.id,x.difference]),[
      ['3LZ_R6X_AE4_HUU',-595],['3LZ_R6X_AE4_HU0_38S',-595],['3LZ_R6X_AE4_HZP_N2Z',-595],['3LZ_R6X_AE4_HXO_N2Z_38S',-595]]);
    assert(sequences.filter(x=>x.name==='stripe/paint prohibition').every(x=>x.states[1].action.outcome==='not_selectable'));
    for(const c of sequences.filter(x=>x.name==='dual roof first'))assert.equal(c.states[0].state.total-c.initial.total,2720);
    for(const c of sequences.filter(x=>x.states.map(y=>y.action.code).join(',')==='ZTK,T0E,J58,ZTK')) {
      assert.equal(c.states[0].state.total-c.initial.total,18990);
      assert.deepEqual(c.states[0].state.automatic,['FEJ','J59','XFS','TOM']);
      assert.equal(c.states[3].state.total,c.initial.total);
      assert.equal(c.states[3].state.missing.length,0);
    }

    const data={model_key:records.model_key,role:'Supplemental frozen-baseline discovery; not corrected target verification',
      provenance:{reference_commit:manifest.reference_commit,workbook_sha256:records.sources.workbook_sha256,
        guide_sha256:records.sources.guide_sha256,...sourceHashes,original_harness_sha256:hash(originalHarness),
        exposed_harness_sha256:hash(harness),probe_sha256:hash(fs.readFileSync(path.join(root,'scripts/zr1_discovery.mjs')))},
      projection:'Snapshots retain actual selected/automatic identities, item prices/types/routing, order pricing/section item projections, compact recap and informational equipment IDs. Copy and images remain in baseline_rows; no live customer data.',
      interiorContexts,priceComparisons,paintStates,beltStates,causeSequences,contextReset,foundations,starting_choice_observations:options,connected_sequences:sequences,not_applicable: notApplicable,seat_transitions:seatTransitions,required_interior_rejection:rejection,live_requests:rt.fetchCalls.length};
    fs.writeFileSync(file,'{\n'+Object.entries(data).map(([k,v])=>'  '+JSON.stringify(k)+': '+(Array.isArray(v)?'[\n'+v.map(x=>'    '+JSON.stringify(x)).join(',\n')+'\n  ]':JSON.stringify(v))).join(',\n')+'\n}\n');
    console.log(model,options.length,'choice observations;',options.filter(x=>x.attempted).length,'actions;',sequences.length,'connected cases;', rejection.length,'rejection cases; zero requests');
  }
} finally {process.chdir(prior);fs.rmSync(scratch,{recursive:true,force:true});}
