"""Read-only comparison of candidate output to the immutable six-model baseline."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile

from catalog.contracts import generate_bundle

BASELINE=Path(__file__).resolve().parents[1]/'baselines/2026-09-06'


def business(value):
    value=json.loads(json.dumps(value))
    value['dataset'].pop('generated_at')
    return value


def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def differences(before, after, path=''):
    """Every changed value/type, missing key and ordered list position."""
    if type(before) is not type(after):
        yield path
    elif isinstance(before,dict):
        for key in sorted(before.keys()|after.keys()):
            child=path+'/'+key.replace('~','~0').replace('/','~1')
            if key not in before or key not in after:
                yield child
            else:
                yield from differences(before[key],after[key],child)
    elif isinstance(before,list):
        if len(before)!=len(after):
            yield path+'/length'
        for i,(left,right) in enumerate(zip(before,after)):
            yield from differences(left,right,path+'/'+str(i))
    elif before!=after:
        yield path


def compare(database, baseline=BASELINE):
    baseline=Path(baseline)
    manifest=json.loads((baseline/'manifest.json').read_text())
    archive=baseline/manifest['archive']['path']
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=manifest['archive']['sha256']:
        raise ValueError('Baseline archive hash mismatch')
    contracts,registry,aliases=generate_bundle(database)
    report=dict(baseline_id=manifest['baseline_id'],reference_commit=manifest['reference_commit'],
                workbook_sha256=next(f['sha256'] for f in manifest['files'] if f['path']=='stingray_master.xlsx'),
                excluded_paths=['/dataset/generated_at'],models={},registry_differences=[])
    members={f['path']:f['sha256'] for f in manifest['files']}
    with tarfile.open(archive) as tar:
        def read(name):
            raw=tar.extractfile(name).read()
            if hashlib.sha256(raw).hexdigest()!=members[name]:
                raise ValueError('Baseline member hash mismatch: '+name)
            return raw.decode()
        expected_models={r['model'] for r in manifest['verification']['contracts']}
        if contracts.keys()!=expected_models:
            raise ValueError('Generated model coverage differs from baseline')
        for key,contract in contracts.items():
            original=json.loads(read('form-output/runtime/'+key.replace('_','-')+'-runtime-contract.json'))
            left,right=business(original),business(contract)
            report['models'][key]=dict(differences=list(differences(left,right)),business_content_sha256=fingerprint(right),
                counts={k:len(v) for k,v in contract.items() if isinstance(v,list)})
        script=read('form-app/data.js')
        expected,_=json.JSONDecoder().raw_decode(script.removeprefix('window.CORVETTE_FORM_DATA = '))
        if list(expected['models'])!=list(registry['models']):
            report['registry_differences'].append('/models/order')
        for record in expected['models'].values():
            record['data']=business(record['data'])
        for record in registry['models'].values():
            record['data']=business(record['data'])
        report['registry_differences'].extend(differences(expected,registry))
        for alias,key in aliases.items():
            if f'window.{alias} = window.CORVETTE_FORM_DATA.models.{key}.data;' not in script:
                report['registry_differences'].append('/aliases/'+alias)
        expected_alias_count=script.count(' = window.CORVETTE_FORM_DATA.models.')
        if expected_alias_count!=len(aliases):
            report['registry_differences'].append('/aliases/count')
    report['passed']=not report['registry_differences'] and all(not r['differences'] for r in report['models'].values())
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    args=parser.parse_args()
    report=compare(args.database)
    print(json.dumps(report,indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
