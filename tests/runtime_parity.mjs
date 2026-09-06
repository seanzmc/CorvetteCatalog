// Execute the same frozen browser consumer against baseline and candidate data.
// The pinned reference harness supplies DOM/download/fetch stubs only; no live
// submission, live workbook, generator or deployed application is invoked.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const root=path.resolve(import.meta.dirname,'..');
const candidate=path.resolve(process.argv[2]);
const reference=process.argv[3] || '/Users/seandm/Projects/27vette';
const baseline=path.join(root,'baselines/2026-09-06');
const manifest=JSON.parse(fs.readFileSync(path.join(baseline,'manifest.json')));
const scratch=fs.mkdtempSync(path.join(os.tmpdir(),'catalog-runtime-'));
const originalCwd=process.cwd();
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const plain=value=>JSON.parse(JSON.stringify(value));
try {
  fs.mkdirSync(path.join(scratch,'form-app'));
  for (const name of ['app.js','data.js']) {
    const member='form-app/'+name;
    const bytes=execFileSync('tar',['-xOf',path.join(baseline,manifest.archive.path),member],{maxBuffer:20*1024*1024});
    assert.equal(hash(bytes),manifest.files.find(f=>f.path===member).sha256);
    fs.writeFileSync(path.join(scratch,member),bytes);
  }
  const harness=execFileSync('git',['-C',reference,'show',manifest.reference_commit+':tests/lib/runtime-harness.mjs']);
  fs.writeFileSync(path.join(scratch,'runtime-harness.mjs'),harness.toString().replace('  activeChoiceRows,','  activeChoiceRows, handleInterior, disableReasonForInterior, validInteriorsForSelectedSeat, buildMarkdown,'));
  process.chdir(scratch);
  const {loadRuntime,loadDataWindow}=await import(pathToFileURL(path.join(scratch,'runtime-harness.mjs')));
  const baselinePath=path.join(scratch,'form-app/data.js');
  const registry=loadDataWindow(baselinePath).CORVETTE_FORM_DATA;
  const old=loadRuntime({dataPath:baselinePath}), fresh=loadRuntime({dataPath:candidate});
  const report={reference_commit:manifest.reference_commit,harness_sha256:hash(harness),variants:0,transitions:0,interior_transitions:0,models:{}};
  function snapshot(runtime, detailed) {
    const order=plain(runtime.currentOrder());
    delete order.metadata.dataset.generated_at;
    const compact=runtime.compactOrder();
    compact.submitted_at='2026-09-06T00:00:00.000Z';
    return plain({order,payload:runtime.dealerSubmissionPayload(compact),missing:runtime.missingRequired(),
      selected:[...runtime.state.selected],interior:runtime.state.selectedInterior,
      autoAdded:[...runtime.computeAutoAdded()],
      choices:detailed ? runtime.activeChoiceRows().map(c=>({id:c.choice_id,reason:runtime.disableReasonForChoice(c),price:runtime.optionPrice(c.option_id)})) : []});
  }
  function check(label, detailed=false) {assert.deepEqual(snapshot(fresh,detailed),snapshot(old,detailed),label);}
  for (const [key,entry] of Object.entries(registry.models)) {
    const modelReport={variants:0,transitions:0};
    const started=Date.now();
    report.models[key]=modelReport;
    for (const variant of entry.data.variants) {
      for (const runtime of [old,fresh]) {
        runtime.activateModel(key);
        runtime.state.bodyStyle=variant.body_style;
        runtime.state.trimLevel=variant.trim_level;
        runtime.resetDefaults();runtime.reconcileSelections();
      }
      check(key+'/'+variant.variant_id+'/defaults',true);
      report.variants++;modelReport.variants++;
      // Baseline-driven selection: one available selectable option per section
      // covers non-LPO choices, paint, wheels, packages and accessories.
      const sections=new Set();
      const choices=modelReport.variants===1 ? old.activeChoiceRows().filter(c=>{
        if (c.selectable!=='True' || c.active!=='True' || c.status==='unavailable' || sections.has(c.section_id)) return false;
        sections.add(c.section_id);return true;
      }) : [];
      for (const choice of choices) {
        if (old.disableReasonForChoice(choice)) continue;
        const before=JSON.stringify([...old.state.selected]);
        for (const runtime of [old,fresh]) runtime.handleChoice(runtime.activeChoiceRows().find(c=>c.choice_id===choice.choice_id));
        check(key+'/'+variant.variant_id+'/'+choice.option_id);
        if (JSON.stringify([...old.state.selected])!==before) {report.transitions++;modelReport.transitions++;}
      }
      // Restore a known valid seat/trim context before the independent interior case.
      for (const runtime of [old,fresh]) {runtime.resetDefaults();runtime.reconcileSelections();}
      check(key+'/'+variant.variant_id+'/before-interior');
      const interior=old.validInteriorsForSelectedSeat().find(i=>i.interior_id!==old.state.selectedInterior && !old.disableReasonForInterior(i));
      if (interior) {
        for (const runtime of [old,fresh]) runtime.handleInterior(runtime.data.interiors.find(i=>i.interior_id===interior.interior_id));
        assert.equal(old.state.selectedInterior,interior.interior_id);
        check(key+'/'+variant.variant_id+'/interior/'+interior.interior_id);
        report.interior_transitions++;
        const a=old.compactOrder(),b=fresh.compactOrder();
        a.submitted_at=b.submitted_at='2026-09-06T00:00:00.000Z';
        assert.equal(fresh.buildMarkdown(b),old.buildMarkdown(a));
      }
      for (const runtime of [old,fresh]) {runtime.resetDefaults();runtime.reconcileSelections();}
      check(key+'/'+variant.variant_id+'/reset');
    }
    modelReport.elapsed_ms=Date.now()-started;
    console.error(`${key}: ${modelReport.variants} variants, ${modelReport.transitions} transitions passed (${modelReport.elapsed_ms} ms)`);
  }
  assert.equal(report.variants,32);
  assert.ok(report.transitions>60);
  assert.equal(report.interior_transitions,32);
  assert.equal(old.fetchCalls.length,0);assert.equal(fresh.fetchCalls.length,0);
  report.passed=true;report.live_requests=0;
  console.log(JSON.stringify(report,null,2));
} finally {
  process.chdir(originalCwd);
  fs.rmSync(scratch,{recursive:true,force:true});
}
