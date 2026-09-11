"""Every model lane's handoff files must conform to docs/discovery/handoff-schema.json."""
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import sys
import unittest

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
