"""Card photos for options the workbook baseline has no photo for.

Run: python -m catalog.photos refresh [--bundle DIR] [--library DIR]   # read the site, write the index, report
     python -m catalog.photos report [--bundle DIR] [--library DIR]    # report from the saved index

The existing form's photos come from its asset_map, which 27vette's
sync_asset_map.py fills from the dealership site's /pictures/27vette/ media by
file name. This catalog keeps that frozen asset_map (the September 6 baseline)
and adds nothing over it. For an option with no baseline photo, refresh applies
the same file-name rules to the site's current media and records the result in
catalog/web/photos/index.json, which the form uses only when the baseline has
no photo. Per model and RPO, the first rule with exactly one file wins:

1. the model's own prefix: c- Stingray, e- Grand Sport, g- Grand Sport X,
   h- Z06, r- ZR1, s- ZR1X (h-vk3.png);
2. the smallest shared-prefix group that includes the model (r-s-etv.jpg);
3. the fallback models' own prefix: Grand Sport uses Stingray; Grand Sport X
   uses Grand Sport, then Stingray; ZR1 and ZR1X use Z06;
4. a file without a prefix, for every model (cf8.png).

Two files at the winning rule are a tie: neither is used, and the report names
them. For each still-missing RPO the report lists site images outside
/pictures/27vette/ (refresh only) and, with --library, local files whose names
contain it, with the name to give a copy in /pictures/27vette/. --bundle limits the
still-missing list to cards a built static bundle actually shows.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlencode, urlparse
from urllib.request import Request, urlopen

from catalog import foundation as f

SITE = 'https://stingraychevroletcorvette.com'
MEDIA_ENDPOINT = SITE + '/wp-json/wp/v2/media'
PATH_FILTER = '/wp-content/uploads/pictures/27vette/'
INDEX = Path(__file__).with_name('web') / 'photos' / 'index.json'
AGENT = 'Mozilla/5.0 CorvetteCatalog-photo-step/1.0'
PREFIX = {'c': 'stingray', 'e': 'grand_sport', 'g': 'grand_sport_x', 'h': 'z06', 'r': 'zr1', 's': 'zr1x'}
CODE = {model: code for code, model in PREFIX.items()}
FALLBACKS = {'grand_sport': ('stingray',), 'grand_sport_x': ('grand_sport', 'stingray'), 'zr1': ('z06',), 'zr1x': ('z06',)}
LANES = {'stingray': 'stingray', 'grand_sport': 'grand-sport', 'grand_sport_x': 'grand-sport-x',
         'z06': 'z06', 'zr1': 'zr1', 'zr1x': 'zr1x'}
IMAGE = ('.png', '.jpg', '.jpeg', '.webp')


def stem(url):
    name = os.path.splitext(unquote(os.path.basename(urlparse(url).path)))[0].lower()
    return re.sub(r'^imgi_\d+_', '', name)


def first_code(text):
    code = re.split(r'[-_]', text)[0]
    return code.upper() if re.fullmatch(r'[0-9a-z]{3}', code) else None


class Media:
    """Site media URLs indexed by the three file-name forms."""

    def __init__(self, urls):
        self.own, self.shared, self.bare = defaultdict(list), defaultdict(list), defaultdict(list)
        for url in sorted(set(urls)):
            name = stem(url)
            group = re.match(r'^([cehrsg](?:-[cehrsg])+)-(.+)$', name)
            single = re.match(r'^([cehrsg])-(.+)$', name)
            if group:
                codes = group[1].split('-')
                rpo = first_code(group[2])
                if rpo and len(set(codes)) == len(codes):
                    self.shared[group[1], rpo].append(url)
            elif single:
                if rpo := first_code(single[2]):
                    self.own[PREFIX[single[1]], rpo].append(url)
            elif rpo := first_code(name):
                self.bare[rpo].append(url)

    def resolve(self, model, rpo):
        """(url, rule) for the first rule with candidates; url is None on a tie."""
        rpo = rpo.upper()
        if found := self.own[model, rpo]:
            return (found[0] if len(found) == 1 else None), 'own', found
        groups = [(len(g.split('-')), urls) for (g, code), urls in self.shared.items()
                  if code == rpo and CODE[model] in g.split('-')]
        if groups:
            size = min(n for n, _ in groups)
            found = [u for n, urls in groups if n == size for u in urls]
            return (found[0] if len(found) == 1 else None), 'shared', found
        for other in FALLBACKS.get(model, ()):
            if found := self.own[other, rpo]:
                return (found[0] if len(found) == 1 else None), 'fallback:' + other, found
        if found := self.bare[rpo]:
            return (found[0] if len(found) == 1 else None), 'bare', found
        return None, None, []


def fetch_media(timeout=60):
    """Every image URL in the site's public media list."""
    urls, page = [], 1
    while True:
        query = urlencode(dict(per_page=100, page=page, media_type='image', _fields='source_url'))
        try:
            with urlopen(Request(f'{MEDIA_ENDPOINT}?{query}', headers={'User-Agent': AGENT}), timeout=timeout) as response:
                batch = json.load(response)
        except OSError as error:
            if getattr(error, 'code', None) == 400 and page > 1:
                break  # past the last page
            raise
        if not batch:
            break
        urls += [item['source_url'] for item in batch if item.get('source_url')]
        page += 1
    return sorted(set(urls))


def targets(source_dir=f.ROOT / 'docs'):
    """Per model: {RPO: (label, shown)} for options without a baseline photo.
    shown marks the options a customer can choose (the report's coverage)."""
    result = {}
    for model, lane in LANES.items():
        data = json.loads((Path(source_dir) / f'{lane}-structured-records.json').read_text())
        rows = data['baseline_rows']
        review = json.loads((Path(source_dir) / f'{lane}-owner-decisions.json').read_text())['owner_review']
        photographed = {r['target_id'] for r in rows['asset_map'] if r['target_type'] == 'option'
                        and str(r['active']).lower() == 'true' and r.get('image_url')}
        labels, shown, covered = {}, set(), set()
        for row in rows[data['sheet_roles']['options']]:
            rpo = (row['rpo'] or '').upper()
            # Inactive workbook rows are kept: owner decisions reactivate some of them.
            if not re.fullmatch(r'[0-9A-Z]{3}', rpo):
                continue
            labels.setdefault(rpo, row['option_name'])
            if (str(row['active']).lower() == 'true' and row['selectable']
                    and row['display_behavior'] not in ('hidden', 'auto_only', 'display_only')):
                shown.add(rpo)
            if row['option_id'] in photographed:
                covered.add(rpo)
        for addition in review['accepted_additions']:
            labels.setdefault(addition['rpo'].upper(), '')  # the card's own label is the alt text
            shown.add(addition['rpo'].upper())
        result[model] = {rpo: (labels[rpo], rpo in shown) for rpo in sorted(labels) if rpo not in covered}
    return result


def shown_cards(bundle):
    """Per model: {RPO: label} of the customer-selectable cards a built static
    bundle shows in any configuration, the report's exact coverage."""
    from catalog.browser import Form
    form, result = Form(bundle), {}
    for model in form.models:
        form.load(model)
        catalog = form.builds.catalogs[model]
        cards = result.setdefault(model, {})
        for configuration in sorted(catalog.ev.configs):
            steps = [s['step_key'] for s in catalog.card_steps(configuration)]
            for card in catalog.cards(catalog.ev.state(configuration), steps)['options']:
                if card['rpo'] and catalog.ev.options[card['option_id']]['customer_selectable']:
                    cards.setdefault(card['rpo'].upper(), card['label'])
    return result


def build(urls, wanted):
    """The index and the report rows: (model, rpo, label, shown, url, rule, candidates)."""
    media, models, report = Media(urls), {}, []
    for model, options in wanted.items():
        for rpo, (label, shown) in options.items():
            url, rule, found = media.resolve(model, rpo)
            report.append((model, rpo, label, shown, url, rule, found))
            if url:
                models.setdefault(model, {})[rpo] = dict(image_url=url, image_alt=label, image_fit='cover',
                                                         image_position='center', rule=rule)
    return models, report


def name_matches(names, codes):
    """Image paths or URLs whose file names contain one of the RPOs, by RPO."""
    found = defaultdict(list)
    for name in sorted(names, key=str):
        base = os.path.basename(urlparse(str(name)).path)
        stem_, suffix = os.path.splitext(unquote(base))
        if suffix.lower() in IMAGE and not re.search(r'-\d+x\d+$|-scaled$', stem_):
            for code in codes & {t.upper() for t in re.split(r'[^A-Za-z0-9]+', stem_) if t}:
                found[code].append(name)
    return found


def print_report(report, library=None, cards=None, elsewhere=()):
    def models_of(rows):
        return ', '.join(sorted({m for m, *_ in rows}))
    used = [r for r in report if r[4]]
    ties = [r for r in report if not r[4] and r[6]]
    missing = defaultdict(list)
    for r in report:
        visible = r[1] in cards.get(r[0], {}) if cards is not None else r[3]
        if not r[4] and not r[6] and visible:
            missing[r[1]].append(r)
    print(f'{len(used)} model photos found for {len({r[1] for r in used})} RPOs')
    for rpo in sorted({r[1] for r in used}):
        rows = [r for r in used if r[1] == rpo]
        print(f'  {rpo}  {models_of(rows)}: ' + '; '.join(sorted({f"{urlparse(r[4]).path.removeprefix(PATH_FILTER)} ({r[5]})" for r in rows})))
    if ties:
        print(f'{len(ties)} ties (keep one file at that rule):')
        for model, rpo, _, _, _, rule, found in ties:
            print(f'  {model} {rpo} {rule}: ' + ', '.join(urlparse(u).path.removeprefix(PATH_FILTER) for u in found))
    print(f'{len(missing)} customer-visible RPOs still without a photo:')
    site = name_matches(elsewhere, set(missing))
    local = name_matches((p for p in Path(library).rglob('*') if p.is_file()), set(missing)) if library else {}
    for rpo, rows in sorted(missing.items()):
        label = next((cards[m][rpo] for m in sorted({r[0] for r in rows}) if cards and rpo in cards.get(m, {})), rows[0][2])
        print(f'  {rpo}  {label}  ({models_of(rows)})')
        models = sorted({m for m, *_ in rows})
        name = rpo.lower() if len(models) == len(LANES) else '-'.join(CODE[m] for m in models) + '-' + rpo.lower()
        for url in site.get(rpo, [])[:5]:
            print(f'      site: {urlparse(url).path.removeprefix("/wp-content/uploads/")}  ->  27vette/.../{name}{os.path.splitext(url)[1].lower()}')
        for path in local.get(rpo, [])[:5]:
            print(f'      local: {path}  ->  27vette/.../{name}{path.suffix.lower()}')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=('refresh', 'report'))
    parser.add_argument('--library', type=Path, help='Local image folder to search for still-missing RPOs')
    parser.add_argument('--bundle', type=Path, help='Built static bundle: count only the cards customers see')
    args = parser.parse_args()
    wanted = targets()
    if args.command == 'refresh':
        everything = fetch_media()
        urls = [u for u in everything if PATH_FILTER in u]
        elsewhere = [u for u in everything if PATH_FILTER not in u]
        models, report = build(urls, wanted)
        INDEX.parent.mkdir(exist_ok=True)
        INDEX.write_text(json.dumps(dict(
            format='catalog-option-photos-v1', source=MEDIA_ENDPOINT + ' (' + PATH_FILTER + ')',
            fetched_at=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), media_count=len(urls),
            models=models), indent=2, sort_keys=True) + '\n')
        print(f'{len(urls)} site images under {PATH_FILTER}; wrote {INDEX.relative_to(f.ROOT)}')
    else:
        index = json.loads(INDEX.read_text())
        urls = sorted({p['image_url'] for photos in index['models'].values() for p in photos.values()})
        _, report = build(urls, wanted)
        elsewhere = []
        print(f'From the saved index (site read {index["fetched_at"]}); ties and other site folders need refresh.')
    print_report(report, args.library, shown_cards(args.bundle) if args.bundle else None, elsewhere)


if __name__ == '__main__':
    main()
