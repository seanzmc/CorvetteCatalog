"""Print the Tests workflow matrix as `shards=<json>` for $GITHUB_OUTPUT.

Every test file under tests/ runs in exactly one job:
- SPLIT files are divided by test method into N jobs using unittest -k filters;
- SEPARATE files get one job each;
- all other files are dealt round-robin into REMAINING_JOBS jobs.
The planner loads each split file and checks that its filters select exactly
the assigned tests, so a filter can neither miss nor duplicate a test.
"""
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / 'tests'


def split_config():
    config = {}
    for item in os.environ.get('SPLIT', '').split():
        name, _, count = item.partition('=')
        config[name] = int(count)
    return config


def test_ids(module):
    """Fully qualified test IDs, loaded the same way `discover` runs them."""
    directory = TESTS / Path(module).parent
    loader = unittest.TestLoader()
    return [test.id() for test in iterate(loader.discover(str(directory), pattern=Path(module).name))]


def iterate(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iterate(item)
        else:
            yield item


def selected(module, patterns):
    directory = TESTS / Path(module).parent
    loader = unittest.TestLoader()
    # Same wrapping unittest applies to a -k value without wildcards.
    loader.testNamePatterns = [f'*{p}*' for p in patterns]
    return [test.id() for test in iterate(loader.discover(str(directory), pattern=Path(module).name))]


def main():
    sys.path.insert(0, str(ROOT))
    present = sorted(str(p.relative_to(TESTS)) for p in TESTS.rglob('test_*.py'))
    split = split_config()
    separate = os.environ.get('SEPARATE', '').split()
    remaining_jobs = int(os.environ.get('REMAINING_JOBS', '1'))
    named = list(split) + separate
    missing = [m for m in named if m not in present]
    if missing or len(named) != len(set(named)):
        raise SystemExit(f'Split/separate names must be distinct test files: {named}')
    if remaining_jobs < 1 or any(count < 1 for count in split.values()):
        raise SystemExit('Job counts must be at least 1; a zero count would drop tests')

    shards = []
    for module, count in split.items():
        ids = test_ids(module)
        if any(i.startswith('unittest.loader._FailedTest') for i in ids):
            raise SystemExit(f'{module} failed to import: {ids}')
        buckets = [ids[i::count] for i in range(count) if ids[i::count]]
        for number, bucket in enumerate(buckets, 1):
            # Class.method is unique within a file and never a prefix of another.
            patterns = ['.'.join(i.split('.')[-2:]) for i in bucket]
            if sorted(selected(module, patterns)) != sorted(bucket):
                raise SystemExit(f'Filters for {module} part {number} do not select exactly its tests')
            shards.append(dict(name=f'{Path(module).stem} {number}/{len(buckets)}',
                               modules=module, filters=' '.join(patterns)))
    shards += [dict(name=Path(m).stem, modules=m, filters='') for m in separate]
    rest = [m for m in present if m not in named]
    for number in range(remaining_jobs):
        part = rest[number::remaining_jobs]
        if part:
            shards.append(dict(name=f'remaining {number + 1}/{remaining_jobs}', modules=' '.join(part), filters=''))
    print('shards=' + json.dumps(shards))


if __name__ == '__main__':
    main()
