"""Every model lane's handoff files must conform to docs/discovery/handoff-schema.json."""
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_handoffs  # noqa: E402

SCHEMA = json.loads(validate_handoffs.SCHEMA_PATH.read_text())


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = validate_handoffs.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class HandoffContractTests(unittest.TestCase):
    def test_all_lanes_conform(self):
        code, out, err = run()
        self.assertEqual(code, 0, err)
        for lane in SCHEMA['lanes']['models']:
            self.assertIn(lane, out)

    def test_every_lane_has_every_contract_file(self):
        for lane in SCHEMA['lanes']['models']:
            for kind, pattern in SCHEMA['lanes']['files'].items():
                with self.subTest(lane=lane, kind=kind):
                    self.assertTrue((ROOT / pattern.format(lane=lane)).exists())

    def test_unknown_key_is_rejected(self):
        errors = []
        validate_handoffs.check(SCHEMA['$defs']['decisions']['properties']['owner_review']['properties']['records'],
                                [{'decision_id': 'X-D01', 'baseline_issue': None, 'target': 't', 'review_state': 'accepted',
                                  'authority': 'a', 'evidence_and_expected_sequence': None, 'decision_document': 'd',
                                  'target_rule_removals': [], 'surprise': 1}], 'records', SCHEMA, errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("unexpected key 'surprise'", errors[0])

    def test_enum_and_required_are_enforced(self):
        errors = []
        validate_handoffs.check(SCHEMA['$defs']['records']['properties']['offering_dispositions'],
                                [{'record_id': 'x', 'workbook_row': 2, 'rpo': 'ABC', 'source_classification': 'made_up',
                                  'guide_anchors': []}], 'dispositions', SCHEMA, errors)
        self.assertEqual(sorted(e.split(': ', 1)[1][:12] for e in errors), ["'made_up' no", 'missing requ'])

    def test_rule_source_fields_match_in_every_lane(self):
        original_load = validate_handoffs.load
        for lane in SCHEMA['lanes']['models']:
            for field in ('source_row', 'rule_id', 'source_id', 'rule_type', 'target_id'):
                with self.subTest(lane=lane, field=field):
                    def changed_load(path):
                        data = original_load(path)
                        if path == f'docs/discovery/{lane}-accounting.json':
                            row = data['direct_rule_translation'][0]
                            row[field] = row[field] + (1 if field == 'source_row' else '_changed')
                        return data
                    with patch.object(validate_handoffs, 'load', side_effect=changed_load):
                        code, _, err = run('--lane', lane)
                    self.assertEqual(code, 1)
                    self.assertIn(f'direct_rule_translation[0].{field} differs', err)

    def test_duplicate_translation_cannot_replace_another_row(self):
        original_load = validate_handoffs.load
        def changed_load(path):
            data = original_load(path)
            if path == 'docs/discovery/zr1-accounting.json':
                data['direct_rule_translation'][1] = data['direct_rule_translation'][0]
            return data
        with patch.object(validate_handoffs, 'load', side_effect=changed_load):
            code, _, err = run('--lane', 'zr1')
        self.assertEqual(code, 1)
        self.assertIn('direct_rule_translation[1].source_row differs', err)

    def test_schema_errors_are_reported_across_files_and_lanes(self):
        original_load = validate_handoffs.load
        def changed_load(path):
            data = original_load(path)
            if path == 'docs/stingray-owner-decisions.json':
                del data['owner_review']
            elif path == 'docs/discovery/stingray-accounting.json':
                del data['option_prices']
            elif path == 'docs/discovery/zr1-runtime.json':
                return []
            return data
        with patch.object(validate_handoffs, 'load', side_effect=changed_load):
            code, _, err = run()
        self.assertEqual(code, 1)
        self.assertIn("missing required key 'owner_review'", err)
        self.assertIn("missing required key 'option_prices'", err)
        self.assertIn("docs/discovery/zr1-runtime.json: expected ['object'], got list", err)
        self.assertIn('3 handoff contract violation(s)', err)

    def test_unknown_lane_is_rejected(self):
        code, _, err = run('--lane', 'zr1x')
        self.assertEqual(code, 1)
        self.assertIn('zr1x: not listed', err)

    def test_runtime_frozen_exception_is_limited_to_listed_keys(self):
        runtime = json.loads((ROOT / 'docs/discovery/zr1-runtime.json').read_text())
        extra = set(runtime) - set(SCHEMA['$defs']['runtime']['properties'])
        self.assertEqual(extra, set(SCHEMA['lanes']['frozen_exceptions']['docs/discovery/zr1-runtime.json']['extra_top_level_keys']))


if __name__ == '__main__':
    unittest.main()
