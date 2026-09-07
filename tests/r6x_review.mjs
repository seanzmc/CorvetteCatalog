// Diagnostic acceptance review: exit 1 means a business discrepancy, not a pass.
// node tests/r6x_review.mjs SOURCE_CASES.json CANDIDATE_DATA.js [REFERENCE_REPO]
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const root = path.resolve(import.meta.dirname, '..');
const input = JSON.parse(fs.readFileSync(process.argv[2]));
const candidate = path.resolve(process.argv[3]);
const reference = process.argv[4] || '/Users/seandm/Projects/27vette';
const baseline = path.join(root, 'baselines/2026-09-06');
const manifest = JSON.parse(fs.readFileSync(path.join(baseline, 'manifest.json')));
assert.equal(input.workbook_sha256, manifest.files.find(f => f.path === 'stingray_master.xlsx').sha256);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const plain = value => JSON.parse(JSON.stringify(value));
const scratch = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-r6x-'));
const originalCwd = process.cwd();
const results = [], transitions = [];
try {
  fs.mkdirSync(path.join(scratch, 'form-app'));
  for (const name of ['app.js', 'data.js']) {
    const member = 'form-app/' + name;
    const bytes = execFileSync('tar', ['-xOf', path.join(baseline, manifest.archive.path), member], {maxBuffer: 20 * 1024 * 1024});
    assert.equal(hash(bytes), manifest.files.find(f => f.path === member).sha256);
    fs.writeFileSync(path.join(scratch, member), bytes);
  }
  const harness = execFileSync('git', ['-C', reference, 'show', manifest.reference_commit + ':tests/lib/runtime-harness.mjs']);
  fs.writeFileSync(path.join(scratch, 'harness.mjs'), harness.toString().replace(
    '  activeChoiceRows,', '  activeChoiceRows, handleInterior, disableReasonForInterior, validInteriorsForSelectedSeat, lineItems, setBodyAndTrim,'));
  process.chdir(scratch);
  const {loadRuntime, loadDataWindow} = await import(pathToFileURL(path.join(scratch, 'harness.mjs')));
  const registry = loadDataWindow(candidate).CORVETTE_FORM_DATA;
  const registryKey = model => input.registry_keys[model];
  for (const [model, key] of Object.entries(input.registry_keys)) {
    const expected = input.cases.filter(c => c.model === model);
    const interiors = registry.models[key].data.interiors.filter(i => i.interior_components.some(v => v.rpo === 'R6X'));
    assert.deepEqual([...new Set(expected.map(c => c.interior_id))].sort(), plain(interiors.map(i => i.interior_id)).sort());
  }
  const runtimes = [loadRuntime({dataPath: path.join(scratch, 'form-app/data.js')}), loadRuntime({dataPath: candidate})];

  function setup(runtime, c) {
    assert.ok(registryKey(c.model), c.model);
    runtime.activateModel(registryKey(c.model), {shouldRender: false});
    runtime.state.bodyStyle = c.body;
    runtime.state.trimLevel = c.trim;
    runtime.resetDefaults(); runtime.reconcileSelections();
    const seat = runtime.activeChoiceRows().find(r => r.option_id === c.seat_option_id);
    assert.ok(seat, c.variant_id);
    assert.equal(runtime.disableReasonForChoice(seat), '');
    if (!runtime.state.selected.has(seat.option_id)) runtime.handleChoice(seat);
    assert.ok(runtime.state.selected.has(seat.option_id));
    assert.equal(runtime.optionPrice(seat.option_id), c.seat_price);
  }

  function select(runtime, c) {
    const interior = runtime.validInteriorsForSelectedSeat().find(i => i.interior_id === c.interior_id);
    assert.ok(interior, c.interior_id);
    assert.equal(runtime.disableReasonForInterior(interior), '');
    runtime.handleInterior(interior);
    assert.equal(runtime.state.selectedInterior, c.interior_id);
    assert.ok(runtime.state.selected.has(c.seat_option_id));
    assert.equal(runtime.optionPrice(c.seat_option_id), c.seat_price);
  }

  function snapshot(runtime) {
    const order = plain(runtime.currentOrder());
    delete order.metadata.dataset.generated_at;
    const compact = runtime.compactOrder(); compact.submitted_at = '2026-09-07T00:00:00.000Z';
    return plain({order, compact, payload: runtime.dealerSubmissionPayload(compact), items: runtime.lineItems()});
  }

  for (const c of input.cases) {
    for (const runtime of runtimes) { setup(runtime, c); select(runtime, c); }
    const old = snapshot(runtimes[0]), current = snapshot(runtimes[1]);
    assert.deepEqual(current, old, 'Frozen/candidate drift: ' + c.interior_id);
    const items = current.items;
    const affected = items.filter(i => i.type === 'selected_interior' || i.type === 'interior_component' || i.id === c.seat_option_id);
    const actual = affected.reduce((sum, i) => sum + i.price, 0);
    const r6x = items.filter(i => i.rpo === 'R6X');
    const expected = c.expected_seat_and_interior;
    const expectedTotal = current.order.pricing.total_msrp - actual + expected;
    // Only the affected subtotal is independently priced. Other selected/default
    // items are held constant; this is not an independent whole-catalog oracle.
    assert.equal(current.order.pricing.base_price, c.base_price);
    assert.equal(current.compact.msrp, current.order.pricing.total_msrp);
    const expectedComponents = c.expected_interior_components.map(i => [i.rpo, i.price]).sort();
    const actualComponents = items.filter(i => i.type === 'interior_component').map(i => [i.rpo, i.price]).sort();
    const componentMatch = JSON.stringify(expectedComponents) === JSON.stringify(actualComponents);
    results.push({...c, actual_items: affected.map(i => ({rpo:i.rpo, price:i.price, type:i.type})),
      actual_seat_and_interior: actual, shortfall: expected - actual,
      actual_total: current.order.pricing.total_msrp, expected_total_holding_other_items_fixed: expectedTotal,
      r6x_once: r6x.length === 1 && r6x[0].price === 995, components_match: componentMatch,
      seat_line_present: items.some(i => i.id === c.seat_option_id),
      passed: actual === expected && r6x.length === 1 && r6x[0].price === 995 && componentMatch});
  }

  // Each model/seat: remove/reapply via interior, seat, trim, body, reset and
  // model changes. Both applicable body variants are covered by cases above.
  const representatives = [...new Map(input.cases.map(c => [c.model + '/' + c.seat, c])).values()];
  const runtime = runtimes[1];
  for (const c of representatives) {
    function check(action, count) {
      const rows = runtime.lineItems().filter(i => i.rpo === 'R6X');
      const passed = rows.length === count && rows.every(i => i.price === 995);
      transitions.push({model:c.model, seat:c.seat, action, expected_r6x_count:count, actual_r6x_count:rows.length, passed});
    }
    setup(runtime, c); select(runtime, c);
    const ordinary = runtime.validInteriorsForSelectedSeat().find(i =>
      !i.interior_components.some(v => v.rpo === 'R6X') && !runtime.disableReasonForInterior(i));
    assert.ok(ordinary);
    runtime.handleInterior(ordinary); check('nonqualifying interior', 0);
    select(runtime, c); check('reapply qualifying interior', 1);
    const otherSeat = runtime.activeChoiceRows().find(i => i.step_key === 'seat' &&
      ['AH2','AE4'].includes(i.rpo) && i.rpo !== c.seat && !runtime.disableReasonForChoice(i));
    assert.ok(otherSeat); runtime.handleChoice(otherSeat); check('switch seat clears incompatible interior', 0);
    setup(runtime, c); select(runtime, c);
    runtime.setBodyAndTrim(c.body === 'coupe' ? 'convertible' : 'coupe', c.trim);
    check('switch body resets interior', 0);
    setup(runtime, c); select(runtime, c);
    runtime.setBodyAndTrim(c.body, runtime.data.variants.find(v => v.trim_level !== c.trim).trim_level);
    check('switch trim resets interior', 0);
    setup(runtime, c); select(runtime, c); runtime.resetDefaults(); runtime.reconcileSelections(); check('reset', 0);
    setup(runtime, c); select(runtime, c);
    const otherModel = input.cases.find(v => v.model !== c.model).model;
    runtime.activateModel(registryKey(otherModel), {shouldRender:false}); check('switch model', 0);
    setup(runtime, c); select(runtime, c); check('return and reapply', 1);
  }
  assert.ok(runtimes.every(r => r.fetchCalls.length === 0));
  const failures = results.filter(r => !r.passed);
  const transitionFailures = transitions.filter(r => !r.passed);
  console.log(JSON.stringify({reference_commit:manifest.reference_commit, workbook_sha256:input.workbook_sha256,
    harness_sha256:hash(harness), candidate_data_sha256:hash(fs.readFileSync(candidate)),
    summary:{cases:results.length, price_failures:failures.length, transitions:transitions.length,
      transition_failures:transitionFailures.length, frozen_candidate_equal:true, live_requests:0,
      passed:failures.length === 0 && transitionFailures.length === 0}, results, transitions}, null, 2));
  process.exitCode = failures.length || transitionFailures.length ? 1 : 0;
} finally {
  process.chdir(originalCwd);
  fs.rmSync(scratch, {recursive:true, force:true});
}
