"""Hash-pinned Photoshop paint and spoiler proofs for confirmed catalog state."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).with_name('web') / 'artwork'
EMPTY = {'assets': [], 'coverage': 'art_not_bound'}


def load(root=ROOT):
    root = Path(root)
    try:
        manifest = json.loads((root / 'manifest.json').read_text())
        if manifest['format'] != 'catalog-artwork-v1':
            raise ValueError('Unsupported artwork manifest')
        assets = manifest['assets']
        ids = [a['id'] for a in assets]
        files = [a['file'] for a in assets] + [manifest['evidence']['file']]
        if len(ids) != len(set(ids)) or len(files) != len(set(files)):
            raise ValueError('Duplicate artwork identity')
        for entry in [*assets, manifest['evidence']]:
            name = entry['file']
            if Path(name).name != name or not name or name in ('.', '..'):
                raise ValueError('Invalid artwork path')
            path = root / name
            if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('Artwork or evidence was altered: ' + name)
        if len({(a['width'], a['height']) for a in assets}) != 1:
            raise ValueError('Artwork planes must share one canvas')
        if any(not a['file'].endswith('.webp') or type(a['width']) is not int or type(a['height']) is not int or
               a['width'] <= 0 or a['height'] <= 0 for a in assets):
            raise ValueError('Invalid artwork image metadata')
        indexed = {a['id']: a for a in assets}
        if any(indexed[p['base_asset_id']]['stack_order'] != 0 or
               indexed[p['foreground_asset_id']]['stack_order'] != 30 for p in manifest['paints']):
            raise ValueError('Invalid fixed artwork order')
        if any(indexed[c['asset_id']]['stack_order'] != 20 for c in manifest['choices']):
            raise ValueError('Invalid spoiler artwork order')
        evidence = json.loads((root / manifest['evidence']['file']).read_text())
        paint_specific = evidence['schema'] == '27vette-paint-specific-spoiler-family-v1'
        if evidence['schema'] not in ('27vette-paint-spoiler-family-v1', '27vette-paint-specific-spoiler-family-v1'):
            raise ValueError('Unsupported native artwork proof')
        source_hash = evidence['source']['sourceSha256'] if paint_specific else evidence['source']['sha256']
        if source_hash != manifest['evidence']['source_sha256']:
            raise ValueError('Artwork source evidence mismatch')
        if (manifest['scene_id'], manifest['model_key'], manifest['model_year'], manifest['body'], manifest['trim']) != (
                evidence['id'], evidence['catalogModelKey'], evidence['modelYear'], evidence['body'], evidence['trim']):
            raise ValueError('Artwork model ownership mismatch')
        expected_paints = [dict(option_id=p['optionId'], rpo=p['rpo'], label=p['name'],
            base_asset_id='paint-'+p['rpo'].lower()+'-back',
            foreground_asset_id='paint-'+p['rpo'].lower()+'-foreground') for p in evidence['paints']]
        if manifest['paints'] != expected_paints:
            raise ValueError('Artwork paint binding mismatch')
        if paint_specific:
            native_choices = [dict(c, assetId='spoiler-'+c['rpo'].lower()+'-'+p['rpo'].lower(), paintRpo=p['rpo'])
                              for p in evidence['paints'] for c in p['choices']]
            if any(c['rpo'] != evidence['choiceEvidence']['rpo'] or c['optionId'] != evidence['choiceEvidence']['optionId'] or
                   c['paintRpo'] not in evidence['choiceEvidence']['allowedPaints'] for c in native_choices):
                raise ValueError('Artwork choice differs from catalog evidence')
        else:
            native_choices = evidence['choices']
        expected_choices = {(c['optionId'], c['rpo'], c['assetId'], c.get('paintRpo')) for c in native_choices}
        actual_choices = [(c['option_id'], c['rpo'], c['asset_id'], c.get('paint_rpo')) for c in manifest['choices']]
        if len(actual_choices) != len(expected_choices) or set(actual_choices) != expected_choices:
            raise ValueError('Artwork option binding mismatch')
        source_assets = {}
        for paint in evidence['paints']:
            source_assets['paint-'+paint['rpo'].lower()+'-back'] = paint['back']
            source_assets['paint-'+paint['rpo'].lower()+'-foreground'] = paint['foreground']
        source_assets.update({c['assetId']: c['webAsset'] for c in native_choices})
        expected_assets = [dict(id=i, file=Path(a['path']).name, sha256=a['sha256'],
            width=a['width'], height=a['height'], stack_order=a['stackOrder']) for i, a in source_assets.items()]
        if assets != expected_assets:
            raise ValueError('Artwork differs from the native export proof')
        return manifest
    except (OSError, KeyError, TypeError, StopIteration, json.JSONDecodeError) as error:
        raise ValueError('Incomplete artwork package: ' + str(error)) from error


def load_collection(root=ROOT):
    """An explicit index adds scenes while old single-scene bundles stay valid."""
    root = Path(root)
    index = root / 'index.json'
    if not index.exists():
        return [load(root)]
    try:
        if index.is_symlink():
            raise ValueError('Invalid artwork index')
        record = json.loads(index.read_text())
        folders = record['scenes']
        if record['format'] != 'catalog-artwork-collection-v1' or not isinstance(folders, list) or not folders:
            raise ValueError('Invalid artwork collection')
        if len(folders) != len(set(folders)):
            raise ValueError('Duplicate artwork scene directory')
        scenes = []
        for folder in folders:
            if not isinstance(folder, str) or folder and (Path(folder).name != folder or folder in ('.', '..')):
                raise ValueError('Invalid artwork scene path')
            directory = root / folder
            if directory.is_symlink():
                raise ValueError('Invalid artwork scene directory')
            scene = load(directory)
            if folder:
                scene['asset_prefix'] = folder + '/'
            scenes.append(scene)
        scopes = [(s['model_key'], s['model_year'], s['body'], s['trim']) for s in scenes]
        if len(scopes) != len(set(scopes)) or len({s['scene_id'] for s in scenes}) != len(scenes):
            raise ValueError('Overlapping artwork scenes require a reviewed view selector')
        return scenes
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError('Incomplete artwork collection: ' + str(error)) from error


def catalog_contract(catalog, manifest):
    if isinstance(manifest, list):
        owned = [scene for scene in manifest if scene['model_key'] == catalog.model_key]
        scenes = [catalog_contract(catalog, scene) for scene in owned]
        if not scenes:
            return dict(EMPTY)
        if len(scenes) == 1:
            return scenes[0]
        # Keep invalid scene scope visible to projection so another body never
        # substitutes for it. Other independently qualified scenes remain usable.
        return dict(coverage='component_preview', assets=[], scenes=[dict(result, body=source['body'],
            trim=source['trim'], model_year=source['model_year']) for result, source in zip(scenes, owned)])
    # Equal option IDs in another model never establish artwork ownership.
    if catalog.model_key != manifest['model_key']:
        return dict(EMPTY)
    for binding in [*manifest['paints'], *manifest['choices']]:
        option = catalog.ev.options.get(binding['option_id'])
        if not option or option['rpo'] != binding['rpo'] or option['lifecycle'] != 'active':
            return dict(assets=[], coverage='art_not_available', reason='Artwork bindings need review for this catalog.')
    result = dict(coverage='component_preview', scene_id=manifest['scene_id'], model_key=manifest['model_key'],
                model_year=manifest['model_year'], body=manifest['body'], trim=manifest['trim'],
                paints=manifest['paints'], choices=manifest['choices'], assets=manifest['assets'],
                notice=manifest['notice'], limitations=manifest['limitations'], evidence=manifest['evidence'])
    if 'asset_prefix' in manifest:
        result['asset_prefix'] = manifest['asset_prefix']
    return result


def project(catalog, state):
    cfg = catalog.ev.configs[state.configuration_id]
    copy = catalog.maps['configuration'][state.configuration_id]
    contract = catalog.artwork
    if 'scenes' in contract:
        matches = [s for s in contract['scenes'] if (s['body'], s['trim'], s['model_year']) ==
                   (cfg['body'], cfg['trim'], copy['model_year'])]
        if len(matches) != 1:
            return dict(assets=[], coverage='art_not_available', reason='Artwork is not available for this body style and trim yet.')
        contract, = matches
    if contract['coverage'] != 'component_preview':
        return dict(assets=[], coverage=contract['coverage'], reason=contract.get('reason', 'Artwork is not available for this model yet.'))
    available = cfg['body'] == contract['body'] and cfg['trim'] == contract['trim'] and copy['model_year'] == contract['model_year']
    paints = [p for p in contract['paints'] if p['option_id'] in state.installed]
    selected = [c for c in contract['choices'] if c['option_id'] in state.installed and
                (not c.get('paint_rpo') or len(paints) == 1 and c['paint_rpo'] == paints[0]['rpo'])]
    if not available or len(paints) != 1 or len(selected) != 1:
        return dict(assets=[], coverage='art_not_available',
            reason='Artwork is not available for this body style, trim, paint and spoiler combination yet.')
    choice, = selected
    paint, = paints
    ids = [paint['base_asset_id'], choice['asset_id'], paint['foreground_asset_id']]
    assets = {a['id']: a for a in contract['assets']}
    return dict(coverage='component_preview', scene_id=contract['scene_id'], component='spoiler',
        option_id=choice['option_id'], rpo=choice['rpo'], label=catalog.option(choice['option_id'])['label'],
        paint_rpo=paint['rpo'], paint_label=catalog.option(paint['option_id'])['label'],
        notice=contract['notice'], limitations=contract['limitations'],
        assets=[dict(assets[i], url='/artwork/' + contract.get('asset_prefix', '') + assets[i]['file']) for i in ids])


def release_media(root=ROOT):
    scenes = load_collection(root)
    prefix = 'runtime/catalog/web/artwork/'
    if (Path(root) / 'index.json').exists():
        return dict(coverage='component_preview', index=prefix+'index.json',
            scenes=[dict(scene_id=s['scene_id'], manifest=prefix+s.get('asset_prefix','')+'manifest.json',
                         evidence=prefix+s.get('asset_prefix','')+s['evidence']['file']) for s in scenes],
            assets=[dict(id=s['scene_id']+'/'+a['id'], path=prefix+s.get('asset_prefix','')+a['file'],
                         sha256=a['sha256']) for s in scenes for a in s['assets']])
    manifest, = scenes
    return dict(coverage='component_preview', scene_id=manifest['scene_id'],
        manifest=prefix + 'manifest.json', evidence=prefix + manifest['evidence']['file'],
        assets=[dict(id=a['id'], path=prefix+a['file'], sha256=a['sha256']) for a in manifest['assets']])


def asset_path(url, root=ROOT):
    for scene in load_collection(root):
        for asset in scene['assets']:
            path = scene.get('asset_prefix', '') + asset['file']
            if url == '/artwork/' + path:
                return Path(root) / path
    return None
