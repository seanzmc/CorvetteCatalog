"""Generate the frozen form contract directly from typed candidate relations.

Compatibility algorithms are independently implemented against the pinned
27vette revision documented in catalog/README.md. No workbook, evidence JSON,
reference code or saved runtime contract is read by this module.
"""
from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
import argparse
import os
import shutil
import tempfile
import json
from pathlib import Path
import re
import sqlite3

from catalog.schema import TABLES

IMAGE_FIELDS = ('image_url', 'image_alt', 'image_fit', 'image_position',
                'hover_image_url', 'hover_image_alt', 'hover_image_position')
MODE_LABELS = {'single_select_req': 'Required single choice',
               'single_select_opt': 'Optional single choice',
               'multi_select_opt': 'Optional multiple choice', 'display_only': 'Display only'}
BODY_ORDER = {'coupe': 1, 'convertible': 2}


def text(value):
    return '' if value is None else str(value).strip()


def flag(value):
    return '' if value is None else 'True' if value else 'False'


def money(value):
    # Preserve the pinned consumer's whole-dollar, ties-to-even conversion.
    return int(round(float(value))) if value is not None else 0


def matches(scope, value):
    return not scope or scope == '*' or value in scope.split('|')


def display(status, selectable, active, behavior):
    if behavior == 'auto_only':
        return 'unavailable', 'False', 'False'
    if behavior == 'hidden':
        return 'unavailable', 'False', 'True'
    if behavior == 'display_only':
        return 'standard' if status == 'standard' else 'available', 'False', 'True'
    return status, selectable, active


class Catalog:
    def __init__(self, db):
        self.db = db
        # Explicit typed tables only. Loading in one transaction gives all six
        # models a consistent revision and permits evidence-free generation.
        self.tables = {t: [dict(r) for r in db.execute(f'SELECT * FROM {t} ORDER BY sequence,id')]
                       for t in TABLES}
        self.by_id = {r['id']: r for rows in self.tables.values() for r in rows}
        self.legacy = {r['id']: r['legacy_id'] for rows in self.tables.values()
                       for r in rows if 'legacy_id' in r}
        self.sections = {r['id']: r for r in self.tables['section']}
        self.children = {}
        for table, field in [('scope_member', 'scope_id'), ('group_member', 'group_id'),
                             ('exclusive_member', 'group_id'), ('interior_component', 'interior_id'),
                             ('interior_hierarchy_member', 'interior_id')]:
            grouped = defaultdict(list)
            for row in self.tables[table]:
                grouped[row[field]].append(row)
            self.children[table] = grouped
        self.axes = {(r['owner_id'], r['axis']): r for r in self.tables['scope_axis']}
        self.assets = {}
        for row in sorted(self.tables['asset_assignment'], key=lambda r: r['source_scope']=='model'):
            if row['active'] and row['image_url']:
                self.assets[row['target_id']] = {f: text(row[f]) for f in IMAGE_FIELDS}

    def rows(self, table, mid):
        return [r for r in self.tables[table] if r['model_id'] == mid]

    def indexed(self, table, mid, field):
        return {r[field]: r for r in self.rows(table, mid)}

    def scopes(self, owner):
        result = {}
        for axis, field in [('body','body_style_scope'), ('trim','trim_level_scope'), ('variant','variant_scope')]:
            row = self.axes.get((owner, axis))
            if row is None:
                result[field] = ''
            elif row['mode'] == 'all':
                result[field] = text(row['all_token'])
            else:
                members = sorted(self.children['scope_member'][row['id']], key=lambda r:r['position'])
                result[field] = '|'.join(r['token'] for r in members)
        return result

    def groups(self, mid):
        groups, exclusive = [], []
        for row in self.rows('group_rule',mid):
            if not row['active']:
                continue
            members = sorted(self.children['group_member'][row['id']], key=lambda r:r['display_order'] or 0)
            groups.append(dict(group_id=row['legacy_id'], display_label=text(row['display_label']),
                group_type=row['effect'], source_id=self.legacy[row['source_id']],
                target_ids=[self.legacy[r['target_id']] for r in members if r['active']],
                **self.scopes(row['id']), disabled_reason=text(row['explanation']), active=flag(row['active']), notes=text(row['notes'])))
        for row in self.rows('exclusive_group',mid):
            if not row['active']:
                continue
            members = sorted(self.children['exclusive_member'][row['id']], key=lambda r:r['display_order'] or 0)
            exclusive.append(dict(group_id=row['legacy_id'], display_label=text(row['display_label']),
                option_ids=[self.legacy[r['offering_id']] for r in members if r['active']],
                selection_mode={'at_most_one':'single_within_group','exactly_one':'required_single_within_group'}[row['selection_mode']],
                active=flag(row['active']), notes=text(row['notes'])))
        return groups, exclusive

    def defaults(self, mid):
        result = []
        for row in self.rows('default_rule',mid):
            if not row['active']:
                continue
            condition = row['condition_code']
            if row['condition_section_id']:
                condition = self.sections[row['condition_section_id']]['section_key']
            if row['condition_offering_id']:
                condition = self.legacy[row['condition_offering_id']]
            result.append(dict(rule_id=row['legacy_id'], target_option_id=self.legacy[row['target_id']],
                condition_type=row['condition_kind'], condition_id=text(condition), **self.scopes(row['id']),
                priority=row['priority'] or 0, notes=text(row['notes'])))
        return sorted(result, key=lambda r:(r['priority'],r['rule_id']))

    def interiors(self, mid, model, presentation):
        result = []
        views = self.indexed('interior_presentation',mid,'interior_id')
        rates = {(r['component_type'],r['trim_scope'],r['code']):money(r['amount']) for r in self.tables['component_rate']}
        # Legacy interior output follows definition order, not scope sheet order.
        rows = sorted(self.rows('model_interior',mid), key=lambda r:self.by_id[r['definition_id']]['sequence'])
        for row in rows:
            if not row['active']:
                continue
            definition, view = self.by_id[row['definition_id']], views[row['id']]
            trim, key = text(definition['price_trim']), row['legacy_id']
            price = money(definition['stored_price'])
            if 'R6X' in trim or 'R6X' in key:
                rtrim = trim if 'R6X' in trim else trim+'_R6X'
                base = rtrim.replace('_R6X','').replace('_',' ')
                upgrade = rates.get(('seat',rtrim.replace('_',' '),definition['seat']))
                if upgrade is not None:
                    price += max(0,upgrade-rates.get(('seat',base,definition['seat']),0))
            components = []
            for c in sorted(self.children['interior_component'][row['id']], key=lambda r:(r['display_order'] or 0,r['code'],r['component_type'])):
                if not c['active']:
                    continue
                amount = money(self.by_id[c['rate_id']]['amount']) if c['rate_id'] else 0
                if amount or c['code']=='R6X':
                    components.append(dict(rpo=c['code'],label=text(c['label']),price=amount,component_type=c['component_type']))
            levels = [self.by_id[h['node_id']]['label'] for h in sorted(self.children['interior_hierarchy_member'][row['id']],key=lambda r:r['position'])]
            item = dict(interior_id=key, source_sheet=presentation['interior_source_sheet'],
                active_for_stingray=model=='stingray', **({f'active_for_{model}':True} if model!='stingray' else {}),
                requires_z25=flag(self.legacy.get(row['requires_offering_id'])=='opt_z25_001'),
                trim_level=text(row['trim_level']), requires_r6x=flag('_R6X' in trim or key.endswith('_R6X')),
                seat_code=text(definition['seat']), interior_code=text(definition['interior_code']),
                interior_name=text(definition['name']),material=text(definition['material']),price=price,
                suede=text(definition['suede']),stitch=text(definition['stitch']),two_tone=text(definition['two_tone']),
                section_id=self.sections[definition['section_id']]['section_key'],color_overrides_raw=text(definition['color_overrides_raw']),
                source_note=text(definition['source_note']),interior_components=components,
                interior_components_json=json.dumps(components,separators=(',',':')))
            for f in ('seat_label','color_family','material_family','variant_label','parent_group_label','leaf_label'):
                item['interior_'+f]=text(view[f])
            for f in ('group_display_order','material_display_order','choice_display_order','reference_order'):
                item['interior_'+f]=view[f] or 0
            item.update(interior_trim_level=levels[0] if levels else item['trim_level'],
                interior_seat_code=text(view['seat_label']).split(' ',1)[0] or item['seat_code'],
                interior_hierarchy_levels=json.dumps(levels,ensure_ascii=False),interior_hierarchy_path=' > '.join(levels))
            item['interior_variant_label'] = item['interior_variant_label'] or item['interior_leaf_label']
            item['interior_parent_group_label'] = item['interior_parent_group_label'] or item['interior_seat_label']
            result.append(item)
        return result

    def generate(self, model, generated_at):
        mid = model['id']
        presentation = self.rows('model_presentation',mid)[0]
        groups, exclusive = self.groups(mid)
        defaults = self.defaults(mid)
        variants = [dict(variant_id=r['legacy_id'],model_year=model['year'],model=model['label'],trim_level=text(r['trim_level']).upper(),
            body_style=text(r['body_style']).lower(),display_name=text(r['display_name']),base_price=money(r['base_price']),
            display_order=r['display_order'] or 0,source_active=flag(r['active']),preview_included=True)
            for r in sorted(self.rows('variant',mid),key=lambda r:(r['membership_order'] or 0,r['legacy_id'])) if r['membership_active']]
        if len(variants)!=model['expected_variant_count']:
            raise ValueError(f"Incomplete variants for {model['model_key']}")
        var_ids = {r['legacy_id']:r['id'] for r in self.rows('variant',mid)}
        section_views = {r['section_id']:r for r in self.rows('section_presentation',mid) if r['active']}
        policies = self.indexed('offering_policy',mid,'offering_id')
        prices = self.indexed('offering_price',mid,'offering_id')
        views = self.indexed('offering_presentation',mid,'offering_id')
        codes = self.indexed('offering_code',mid,'offering_id')
        availability = {(r['offering_id'],r['variant_id']):r['status'] for r in self.rows('availability',mid)}
        overrides = {(r['offering_id'],r['variant_id']):r for r in self.rows('variant_override',mid) if r['active']}
        default_views = {r['legacy_id']:r for r in self.rows('default_rule',mid) if r['active']}
        exclusive_ids = {i for g in exclusive if len(g['option_ids'])>=2 for i in g['option_ids']}
        section_ids, options, choices = set(), {}, []
        preview_count = 0
        for offering in self.rows('offering',mid):
            if not offering['active']:
                continue
            oid, key = offering['id'],offering['legacy_id']
            policy, view = policies[oid],views[oid]
            preview = {}
            for variant in variants:
                override = overrides.get((oid,var_ids[variant['variant_id']]),{})
                sid = override.get('section_id') or view['section_id']
                section, sv = self.sections[sid],section_views.get(sid,{})
                behavior = text(override.get('display_behavior') or policy['display_behavior'])
                selectable = flag(override['selectable'] if override.get('selectable') is not None else policy['selectable'])
                active = flag(override.get('active',offering['active']))
                status,selectable,active = display(availability[(oid,var_ids[variant['variant_id']])],selectable,active,behavior)
                if status not in ('standard','available') and behavior!='auto_only':
                    continue
                item = dict(option_id=key,rpo=text(codes.get(oid,{}).get('code')),label=text(view['label']),description=text(view['description']),
                    section_id=section['section_key'],section_name=text(sv.get('display_label') or section['name']),
                    standard_equipment_group_type=text(sv.get('standard_equipment_group_type')),auto_added_summary_required=bool(sv.get('auto_added_bucket')),
                    step_key=text(sv.get('step_key') or section['step_key']),status=status,selectable=selectable,active=active,
                    base_price=money(prices[oid]['amount']),display_order=view['display_order'] or 0)
                if not behavior and status=='standard' and selectable==active=='True' and key in exclusive_ids:
                    for rule in defaults:
                        if (rule['target_option_id']==key and default_views[rule['rule_id']]['display_behavior']=='default_selected'
                            and rule['condition_type'] in ('always','unless_selected_rpo')
                            and all(matches(rule[f],variant[v]) for f,v in [('body_style_scope','body_style'),('trim_level_scope','trim_level'),('variant_scope','variant_id')])):
                            behavior='default_selected'
                            break
                if behavior:
                    item['display_behavior']=behavior
                preview[variant['variant_id']]=item
                section_ids.add(sid)
            if not preview:
                continue
            first = next(iter(preview.values()))
            options[key]=first
            first_order=preview_count+1
            preview_count+=len(preview)
            for variant in variants:
                item = dict(preview.get(variant['variant_id'],first))
                if variant['variant_id'] not in preview:
                    item['status'],item['selectable'],item['active'] = display('unavailable',first['selectable'],first['active'],first.get('display_behavior',''))
                    # The legacy fallback omits the preview-only equipment tag.
                    item['standard_equipment_group_type']=''
                item.update(choice_id=f"{variant['variant_id']}__{key}",variant_id=variant['variant_id'],body_style=variant['body_style'],trim_level=variant['trim_level'])
                item['status_label']={'standard':'Standard','available':'Available','unavailable':'Not Available'}[item['status']]
                item['display_order']=item['display_order'] or first_order
                item.update(self.assets.get(oid,{}))
                choices.append(item)
        steps = [dict(step_key=r['step_key'],step_label=r['label'],runtime_order=r['runtime_order'],source=text(r['source']) or 'workbook')
                 for r in self.rows('runtime_step',mid) if r['active'] and r['navigable']]
        steps.sort(key=lambda r:(r['runtime_order'],r['step_key']))
        step_order={r['step_key']:i for i,r in enumerate(steps)}
        step_labels={r['step_key']:r['step_label'] for r in steps}
        step_labels['standard_equipment']='Standard Equipment'
        sections = [dict(context_type=r['context_type'],section_id=r['section_key'],section_name=text(r['name']),selection_mode=r['selection_mode'],
                    choice_mode=text(r['choice_mode']),is_required=flag(r['is_required']),standard_behavior=text(r['standard_behavior']),
                    section_display_order=r['display_order'],step_key=r['step_key'],step_label=r['step_label'],selection_mode_label=MODE_LABELS[r['selection_mode']])
                    for r in self.rows('context_section',mid) if r['active']]
        sections.sort(key=lambda r:(r['section_display_order'],r['section_id']))
        product_sections=[]
        for sid in section_ids:
            section,sv=self.sections[sid],section_views.get(sid,{})
            mode=section['selection_mode']
            step=text(sv.get('step_key') or section['step_key'])
            product_sections.append(dict(section_id=section['section_key'],section_name=text(sv.get('display_label') or section['name']),
                source_section_name=text(section['name']),selection_mode=mode,selection_mode_label=MODE_LABELS[mode],
                choice_mode='single' if mode.startswith('single') else 'multi' if mode.startswith('multi') else 'display',
                is_required=flag(section['is_required']),standard_behavior=text(section['standard_behavior']),
                section_display_order=sv.get('display_order') if sv.get('display_order') is not None else section['display_order'] or 0,
                step_key=step,step_label=step_labels[step]))
        product_sections.sort(key=lambda r:(r['section_display_order'],step_order.get(r['step_key'],9999),r['section_id']))
        sections.extend(product_sections)
        for step in steps:
            step['section_ids']='|'.join(sorted(r['section_id'] for r in sections if r['step_key']==step['step_key']))
        interiors = self.interiors(mid,model['model_key'],presentation)
        rules = self.rules(mid,options,interiors,sections,groups)
        price_rules = [dict(price_rule_id=r['legacy_id'],condition_option_id=self.legacy[r['condition_id']],target_option_id=self.legacy[r['target_id']],
                       price_rule_type=r['effect'],price_value=money(r['amount']),**self.scopes(r['id']),notes=text(r['notes'])) for r in self.rows('price_rule',mid)]
        interior_ids={r['interior_id'] for r in interiors}
        colors=[]
        for r in self.rows('color_rule',mid):
            if self.legacy[r['interior_id']] in interior_ids and self.legacy[r['condition_id']] in options and self.legacy[r['added_id']] in options:
                colors.append(dict(override_id=f'co_{len(colors)+1:03d}',interior_id=self.legacy[r['interior_id']],option_id=self.legacy[r['condition_id']],
                    rule_type=r['effect'],adds_rpo=self.legacy[r['added_id']],notes='Exterior/interior pairing requires the listed override RPO.'))
        equipment = [dict(equipment_id='std_'+c['choice_id'],**{f:c[f] for f in ('variant_id','body_style','trim_level','option_id','rpo','label','description','section_id','section_name','standard_equipment_group_type','display_order')}) for c in choices if c['status']=='standard']
        summary = dict(sections=sorted([dict(section_key=r['section_key'],section_label=r['label'],display_order=r['display_order'],notes=text(r['notes']))
                      for r in self.rows('summary_section',mid) if r['active']],key=lambda r:(r['display_order'],r['section_key'])),
                      stepMap={self.by_id[r['step_id']]['step_key']:self.by_id[r['section_id']]['section_key'] for r in self.rows('step_summary',mid) if r['active']})
        label=model['label']
        checks=[('active_variants','variant',f'{len(variants)} configured {label} variants included by model config; workbook active flags are unchanged.'),
                ('availability_rows','availability',f'{len(choices)} draft choice rows exported from the {label} variant matrix.'),
                ('rules','rule',f"{len(rules)} active compatibility rules exported from {presentation['rule_mapping_sheet']}."),
                ('interior_contract','interior',f'{len(interiors)} model-scoped {label} LT interiors exported.'),
                ('price_rules','price_rule',f"{len(price_rules)} active price rules exported from {presentation['price_rules_sheet']}."),
                ('color_overrides','color_override',f"{len(colors)} color override rows exported from {presentation['color_overrides_sheet']}.")]
        return dict(dataset=dict(name=presentation['dataset_name'],model=label,model_year=str(model['year']),source_workbook=presentation['source_workbook'],
                    source_sheet=presentation['source_option_sheet'],generated_at=generated_at,status='runtime_active'),variants=variants,steps=steps,sections=sections,
                    contextChoices=self.context(mid,variants),orderSummary=summary,choices=choices,standardEquipment=equipment,ruleGroups=groups,exclusiveGroups=exclusive,
                    rules=rules,priceRules=price_rules,interiors=interiors,colorOverrides=colors,defaultSelectionRules=defaults,
                    validation=[dict(check_id=c,severity='pass',entity_type=t,entity_id='',message=m) for c,t,m in checks])

    def context(self, mid, variants):
        copy = self.rows('context_copy',mid)
        contexts = {(r['context_type'],r['value']):r['id'] for r in self.rows('context_choice',mid)}
        def tooltip(kind,value,body):
            matches = [r for r in copy if r['active'] and text(r['context_type']).lower()==kind
                       and text(r['value']).lower()==value.lower() and text(r['body_scope']).lower() in ('','*',body) and r['info_tooltip']]
            matches.sort(key=lambda r:text(r['body_scope']).lower()==body,reverse=True)
            return text(matches[0]['info_tooltip']) if matches else ''
        result=[]
        for body in sorted({v['body_style'] for v in variants},key=lambda b:BODY_ORDER[b]):
            result.append(dict(context_choice_id='body_style__'+body,context_type='body_style',value=body,label=body.title(),
                description=f"{sum(v['body_style']==body for v in variants)} trims available",info_tooltip=tooltip('body_style',body,body),
                section_id='sec_context_body_style',step_key='body_style',body_style=body,trim_level='',variant_id='',base_price='',
                display_order=BODY_ORDER[body],**self.assets.get(contexts[('body_style',body)],{})))
        for v in variants:
            result.append(dict(context_choice_id=f"trim_level__{v['body_style']}__{v['trim_level'].lower()}",context_type='trim_level',value=v['trim_level'],
                label=v['trim_level'],description=v['display_name'],info_tooltip=tooltip('trim_level',v['trim_level'],v['body_style']),
                section_id='sec_context_trim_level',step_key='trim_level',body_style=v['body_style'],trim_level=v['trim_level'],
                variant_id=v['variant_id'],base_price=v['base_price'],display_order=v['display_order']))
        return result

    def rules(self, mid, options, interiors, sections, groups):
        interior_map={r['interior_id']:r for r in interiors}
        entities={**options,**interior_map}
        section_map={r['section_id']:r for r in sections}
        grouped={(g['source_id'],t) for g in groups if g['group_type']=='requires_any' for t in g['target_ids']}
        def label(key):
            r=entities[key]
            return (text(r.get('rpo'))+' '+r['label']).strip() if key in options else next(text(r[f]) for f in ('interior_leaf_label','interior_name','interior_code','interior_id') if r.get(f))
        def meta(source,target):
            result={}
            for prefix,key in [('source',source),('target',target)]:
                sid=entities[key]['section_id']
                result.update({prefix+'_type':'interior' if key in interior_map else 'option',prefix+'_section':sid,
                               prefix+'_selection_mode':section_map.get(sid,{}).get('selection_mode','')})
            return result
        result=[]
        for r in self.rows('direct_rule',mid):
            source,target=self.legacy[r['source_id']],self.legacy[r['target_id']]
            if source not in entities or target not in entities or (r['effect']=='requires' and (source,target) in grouped):
                continue
            metadata=meta(source,target)
            replace=r['runtime_action']=='replace'
            redundant=(r['effect']=='excludes' and metadata['source_section']==metadata['target_section']
                       and metadata['source_selection_mode'].startswith('single') and metadata['target_selection_mode'].startswith('single') and not replace)
            reason=text(r['explanation'])
            if not reason:
                if replace: reason=f'{label(source)} removes {label(target)}.'
                elif r['effect']=='excludes': reason=f'Blocked by {label(source)}.'
                elif r['effect']=='requires': reason=f'Requires {label(target)}.'
                else: reason=f'Included with {label(source)}.'
            note=re.sub(r'\s+',' ',text(r['source_note'])).strip()
            if len(note)>500: note=note[:499].rstrip()+'...'
            result.append(dict(rule_id=r['legacy_id'],source_id=source,rule_type=r['effect'],target_id=target,**metadata,
                body_style_scope=self.scopes(r['id'])['body_style_scope'],disabled_reason=reason,auto_add=flag(r['effect']=='includes'),
                active=flag(not redundant),runtime_action='replace' if replace else 'omit_redundant_same_section_exclude' if redundant else 'active',source_note=note))
        # The candidate owns emission permissions; graph mechanics alone cannot
        # authorize additional replacements. Preserve authored-pair precedence.
        graph=defaultdict(list)
        for r in result:
            if r['active']=='True' and r['rule_type']=='includes' and r['target_id'] not in graph[r['source_id']]:
                graph[r['source_id']].append(r['target_id'])
        primitives=[r for r in result if r['active']=='True' and r['rule_type']=='excludes' and r['runtime_action']!='replace']
        authored={(r['source_id'],r['target_id']) for r in result if r['active']=='True' and r['rule_type']=='excludes'}
        candidates=[]
        for source in sorted(graph):
            queue,seen=deque([source]),{source}
            while queue:
                for target in graph.get(queue.popleft(),[]):
                    if target not in seen:
                        seen.add(target);queue.append(target)
            for r in primitives:
                if r['target_id'] in seen-{source} and source not in (r['source_id'],r['target_id']):
                    candidates.append((source,r['source_id'],r['target_id']))
        permissions=set()
        for permission in self.rows('derivation_permission',mid):
            if permission['method']!='includes_closure_approved_replace':
                raise ValueError(f"Unsupported derivation permission method: {permission['method']!r}")
            permissions.add((self.legacy[permission['source_id']],self.legacy[permission['target_id']]))
        if permissions-{(s,t) for s,t,_ in candidates}:
            raise ValueError('Stale derivation permission; no includes-closure candidate')
        emitted=set()
        for source,target,via in sorted(candidates):
            pair=source,target
            if pair not in permissions or pair in authored or pair in emitted:
                continue
            result.append(dict(rule_id=f'derived_{source}_replaces_{target}',source_id=source,rule_type='excludes',target_id=target,
                disabled_reason=f'{label(target)} was removed: {label(source)} includes {label(via)}, which replaces it.',
                auto_add='False',active='True',runtime_action='replace',body_style_scope='',source_note='',**meta(source,target)))
            emitted.add(pair)
        return result


    def registry(self, contracts):
        models, aliases, defaults = {}, {}, []
        promotions = sorted(self.tables['publication'], key=lambda r:(r['display_order'] or 0,r['registry_key']))
        for row in promotions:
            if not (row['active'] and row['promoted_to_runtime']):
                continue
            model = self.by_id[row['model_id']]
            p = self.rows('model_presentation',model['id'])[0]
            key = row['registry_key']
            if key in models:
                raise ValueError('Duplicate registry key')
            models[key] = dict(key=key,label=model['label'],modelName='Corvette '+model['label'],exportSlug=p['export_slug'],
                vehicleSetup=dict(cardSubtitle=p['setup_card_subtitle'],eyebrow=p['setup_eyebrow'],title=p['setup_title'],description=p['setup_description'],
                    facts=[r['text'] for r in sorted(self.rows('model_fact',model['id']),key=lambda r:r['position'])]),
                data=contracts[model['model_key']],**self.assets.get(p['id'],{}))
            if row['default_model']:
                defaults.append(key)
            if row['legacy_alias']:
                alias=row['legacy_alias']
                if not re.fullmatch(r'[A-Za-z_$][A-Za-z0-9_$]*',alias) or alias in aliases:
                    raise ValueError('Invalid or duplicate registry alias')
                aliases[alias]=key
        if len(defaults)!=1 or not models:
            raise ValueError('Registry requires exactly one promoted default model')
        return dict(defaultModelKey=defaults[0],models=models), aliases


def generate_bundle(database, generated_at=None):
    """Read one candidate snapshot for both contracts and their browser registry."""
    db=sqlite3.connect(Path(database).resolve().as_uri()+'?mode=ro',uri=True)
    db.row_factory=sqlite3.Row
    try:
        db.execute('BEGIN')
        metadata=dict(db.execute('SELECT key,value FROM import_metadata'))
        if metadata.get('schema_version')!='2' or metadata.get('authority')!='disposable_candidate':
            raise ValueError('Rebuild the disposable candidate with the current importer (schema 2)')
        if db.execute('PRAGMA foreign_key_check').fetchone():
            raise ValueError('Candidate contains invalid references')
        catalog=Catalog(db)
        stamp=generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        contracts={m['model_key']:catalog.generate(m,stamp) for m in catalog.tables['model'] if m['active']}
        registry,aliases=catalog.registry(contracts)
        return contracts,registry,aliases
    finally:
        db.close()


def generate(database, generated_at=None):
    return generate_bundle(database,generated_at)[0]


def registry_script(registry, aliases):
    script='window.CORVETTE_FORM_DATA = '+json.dumps(registry,indent=2)+';\n'
    for alias,key in aliases.items():
        script+=f'window.{alias} = window.CORVETTE_FORM_DATA.models[{json.dumps(key)}].data;\n'
    return script


def write_bundle(database, output, generated_at=None):
    """Publish a complete disposable directory; never overwrite an existing one."""
    output=Path(output)
    if os.path.lexists(output):
        raise FileExistsError(f'Choose a new output directory; refusing to overwrite {output}')
    contracts,registry,aliases=generate_bundle(database,generated_at)
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=Path(tempfile.mkdtemp(prefix='.contracts-',dir=output.parent))
    try:
        runtime=temporary/'form-output/runtime'
        runtime.mkdir(parents=True)
        for key,contract in contracts.items():
            if not re.fullmatch(r'[a-z0-9_]+',key):
                raise ValueError('Invalid model key')
            (runtime/(key.replace('_','-')+'-runtime-contract.json')).write_text(json.dumps(contract,indent=2)+'\n')
        (temporary/'form-app').mkdir()
        (temporary/'form-app/data.js').write_text(registry_script(registry,aliases))
        # rename is atomic on this filesystem; the output is a disposable path.
        if os.path.lexists(output):
            raise FileExistsError(f'Output appeared during generation: {output}')
        os.rename(temporary,output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return contracts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--generated-at',help='Optional fixed timestamp for reproducible comparisons')
    args=parser.parse_args()
    contracts=write_bundle(args.database,args.output,args.generated_at)
    print(json.dumps({'output':str(args.output),'models':list(contracts)},indent=2))


if __name__=='__main__':
    main()
