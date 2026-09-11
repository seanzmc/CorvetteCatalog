"""Regression coverage for the reproduction verifier's generated-directory input."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('stingray', 'grand-sport', 'grand-sport-x', 'z06')


class DiscoveryComparisonTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.local'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        for model in MODELS:
            shutil.copyfile(ROOT / f'docs/discovery/{model}-runtime.json',
                            self.output / f'{model}-runtime.json')

    def verify(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts/verify_discovery_catchup.py'), *map(str, args)],
            cwd=ROOT, capture_output=True, text=True, timeout=120)

    def change(self, model, mutate):
        path = self.output / f'{model}-runtime.json'
        data = json.loads(path.read_text())
        mutate(data)
        path.write_text(json.dumps(data, sort_keys=True))

    def test_timestamp_changes_and_key_order_pass_full_verifier(self):
        def timestamps(data):
            snapshots = [row['state'] for row in data['foundations'] + data['seat_transitions']]
            for case in data['connected_sequences']:
                snapshots.append(case['initial'])
                snapshots.extend(step['state'] for step in case['states'])
            for snapshot in snapshots:
                snapshot['compact']['submitted_at'] = '2000-01-01T00:00:00.000Z'
        for model in MODELS:
            self.change(model, timestamps)
        result = self.verify(self.output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count('reproduced observations match'), len(MODELS))

    def test_changed_observation_in_each_model_fails(self):
        for model in MODELS:
            with self.subTest(model=model):
                self.change(model, lambda data: data['foundations'][0]['state'].__setitem__('total', -1))
                result = self.verify(self.output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f'{model}-runtime.json: reproduced observations differ', result.stderr)
                shutil.copyfile(ROOT / f'docs/discovery/{model}-runtime.json',
                                self.output / f'{model}-runtime.json')

    def test_types_order_and_provenance_are_not_normalized_away(self):
        mutations = [
            lambda data: data.__setitem__('live_requests', False),
            lambda data: data['foundations'].reverse(),
            lambda data: data['provenance'].__setitem__('reference_commit', 'changed'),
            lambda data: data.__setitem__('submitted_at', 'unexpected field'),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                self.change('stingray', mutate)
                result = self.verify(self.output)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('reproduced observations differ', result.stderr)
                shutil.copyfile(ROOT / 'docs/discovery/stingray-runtime.json',
                                self.output / 'stingray-runtime.json')

    def test_missing_output_fails(self):
        (self.output / 'z06-runtime.json').unlink()
        result = self.verify(self.output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('z06-runtime.json', result.stderr)

    def test_directory_argument_is_required(self):
        result = self.verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('generated_directory', result.stderr)


if __name__ == '__main__':
    unittest.main()
