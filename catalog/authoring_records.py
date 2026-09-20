"""Typed catalog editing: coupled changes, immutable evidence, reviewed row history."""
from datetime import datetime, timezone
from dataclasses import asdict
import json
from uuid import uuid4

from catalog import foundation as f
from catalog.foundation_schema import SCOPES, IDENTITY_RELATIONS
from catalog.consumers import ConsumerCatalog, digest, encode, plain, validate_mappings
from catalog.evaluator import EvaluationError
from catalog.releases import database_hash

# Deliberate product/editor surface. System identity, source and translation
# tables are never client-writable. SQL identifiers only come from this list.
FIELDS = {
    'configuration': 'body trim enabled chooser_order starting_amount_minor basis_id',
    'option': 'rpo name customer_selectable lifecycle purchase_amount_minor basis_id charge_mode',
    'option_configuration': 'status',
    'option_presentation_override': 'customer_selectable',
    'interior': 'seat_option_id code enabled',
    'interior_configuration': '',
    'interior_part': 'option_id component_id role display_order',
    'component': 'kind code',
    'component_rate': 'amount_minor basis_id',
    'condition': 'mode',
    'condition_clause': 'mode',
    'condition_member': 'option_id interior_id group_id state',
    'requirement': 'source_option_id source_interior_id activation_condition_id satisfaction_condition_id source_state loss_policy',
    'acquisition': 'condition_id target_option_id origin_kind peer_policy intent_policy priority',
    'conflict': 'source_option_id source_interior_id activation_condition_id',
    'conflict_member': 'option_id interior_id',
    'choice_group': 'minimum maximum peer_policy',
    'choice_group_member': '',
    'replacement_plan': 'condition_id requested_option_id',
    'replacement_action': 'option_id action intent_effect',
    'option_rate': 'condition_id target_option_id priority amount_minor basis_id',
    'equipment_substitution': 'condition_id removed_option_id replacement_option_id',
    'content_aspect': 'name',
    'content_effect': 'condition_id aspect_id effect_kind value precedence',
    'consumer_option': 'presentation',
    'consumer_option_context': 'presentation',
    'consumer_configuration': 'presentation',
    'consumer_interior': 'presentation',
    'consumer_model': 'presentation display_order is_default',
}
FIELDS.update({t + '_configuration': '' for t in SCOPES})
FIELDS = {t: fields.split() for t, fields in FIELDS.items()}
LABELS = {
    'configuration': 'Body, trim and starting prices', 'option': 'Options and lifecycle',
    'option_configuration': 'Option availability', 'option_presentation_override': 'Selection overrides',
    'interior': 'Interior choices', 'interior_configuration': 'Interior availability',
    'interior_part': 'Interior equipment and components', 'component': 'Component definitions',
    'component_rate': 'Component prices', 'condition': 'Conditions',
    'condition_clause': 'Condition clauses', 'condition_member': 'Condition members',
    'requirement': 'Continuing prerequisites', 'acquisition': 'Inclusions and defaults',
    'conflict': 'Conflicts', 'conflict_member': 'Conflict members', 'choice_group': 'Choice groups',
    'choice_group_member': 'Choice group members', 'replacement_plan': 'Replacement plans',
    'replacement_action': 'Replacement actions', 'option_rate': 'Contextual option prices',
    'equipment_substitution': 'Equipment substitutions', 'content_aspect': 'Equipment descriptions',
    'content_effect': 'Conditional equipment descriptions', 'consumer_option': 'Option copy and order codes',
    'consumer_option_context': 'Option sections and summaries', 'consumer_configuration': 'Configuration copy',
    'consumer_interior': 'Interior copy and hierarchy', 'consumer_model': 'Steps, sections and model copy',
}
ENUMS = {
    'lifecycle': ['active','factory_unavailable','retired'], 'charge_mode': ['priced','no_separate_charge'],
    'status': ['standard','available','unavailable'], 'origin_kind': ['standard','default','included','dependency'],
    'intent_policy': ['preserve_prior','absorb_prior'], 'loss_policy': ['remove_source_with_notice_revert'],
    'source_state': ['resolved_selection','chosen'], 'state': ['explicit_intent','resolved_selection','chosen','occupied'],
    'effect_kind': ['add','replace'], 'action': ['add','remove'], 'intent_effect': ['commit_purchase'],
}


def prepare(db):
    with db:
        db.execute('''CREATE TABLE IF NOT EXISTS authoring_record_change (
            change_id TEXT PRIMARY KEY, revision_id TEXT NOT NULL REFERENCES catalog_revision(revision_id),
            edit_version INTEGER NOT NULL, saved_at TEXT NOT NULL, reason TEXT NOT NULL,
            operations_json TEXT NOT NULL, evidence_json TEXT NOT NULL, scenarios_json TEXT NOT NULL,
            UNIQUE(revision_id,edit_version))''')


def schema(db, table):
    if table not in FIELDS:
        raise ValueError('Unknown editor')
    columns = [dict(r) for r in db.execute(f'PRAGMA table_info("{table}")')]
    keys = [r['name'] for r in sorted(columns, key=lambda c:c['pk']) if r['pk']]
    refs = {r['from']: (r['table'], r['to']) for r in db.execute(f'PRAGMA foreign_key_list("{table}")')
            if r['from'] not in ('revision_id','model_year_id','evidence_set_id','decision_set_id')}
    fields = []
    for c in columns:
        name = c['name']
        if name not in FIELDS[table] and name not in keys:
            continue
        options = ENUMS.get(name)
        if name == 'mode':
            options = ['always','conjunction'] if table == 'condition' else ['any_present','none_present']
        if name == 'peer_policy':
            options = ['replace'] if table == 'choice_group' else ['locked','yield_to_explicit']
        fields.append(dict(name=name, integer='INT' in c['type'], nullable=not c['notnull'],
                           key=name in keys, options=options, reference=refs.get(name)))
    return dict(table=table, label=LABELS.get(table, LABELS.get(table.removesuffix('_configuration'), table) + ' scope'),
                keys=keys, fields=fields)


def row_key(db, table, row):
    # Also used for internal identity and translation patches during replay.
    cols = sorted(db.execute(f'PRAGMA table_info("{table}")'), key=lambda r:r['pk'])
    return {c['name']:row[c['name']] for c in cols if c['pk']}


def lookup(db, table, key):
    clause = ' AND '.join('"' + k + '" IS ?' for k in key)
    row = db.execute(f'SELECT * FROM "{table}" WHERE {clause}', tuple(key.values())).fetchone()
    return dict(row) if row is not None else None


def patch_row(db, operation, reverse=False):
    table, key = operation['table'], operation['key']
    allowed=set(FIELDS) | {t+'_identity' for t in IDENTITY_RELATIONS} | {t+'_translation' for t in FIELDS}
    if table not in allowed: raise ValueError('Uneditable history table')
    columns={r['name'] for r in db.execute(f'PRAGMA table_info("{table}")')}
    if set(key)!=set(row_key(db,table,{c:None for c in columns})): raise ValueError('Invalid history key')
    for row in (operation['before'],operation['after']):
        if row is not None and (set(row)!=columns or row_key(db,table,row)!=key):
            raise ValueError('Invalid history row')
    before, after = operation['before'], operation['after']
    if reverse:
        before, after = after, before
    if lookup(db, table, key) != before:
        raise ValueError('Recorded change does not match ' + table + ': ' + encode(key))
    clause = ' AND '.join('"' + k + '" IS ?' for k in key)
    if after is None:
        db.execute(f'DELETE FROM "{table}" WHERE {clause}', tuple(key.values()))
    elif before is None:
        f._insert(db, table, after)
    else:
        assignments = ','.join('"' + k + '"=?' for k in after)
        db.execute(f'UPDATE "{table}" SET {assignments} WHERE {clause}', (*after.values(), *key.values()))


def evidence(db, rows):
    sets = {row['evidence_set_id'] for row in rows if row and row.get('evidence_set_id')}
    result = {}
    for sid in sets:
        for r in db.execute('''SELECT d.content_sha256,d.source_path,a.locator,a.fragment_key
            FROM evidence_member e JOIN source_anchor a USING(anchor_id)
            JOIN source_document d USING(document_id) WHERE e.set_id=?''',(sid,)):
            result[encode(dict(r))] = dict(r)
    return [result[k] for k in sorted(result)]


def new_record(db,revision,table):
    if table.startswith('consumer_') or table in ('configuration','option','interior'):
        return None
    owner=db.execute('SELECT y.model_year_id,m.evidence_set_id,m.decision_set_id FROM catalog_revision r JOIN model_year y USING(model_year_id) JOIN model m USING(model_id) WHERE r.revision_id=?',(revision,)).fetchone()
    if not owner: raise ValueError('Unknown model revision')
    values={r['name']:None for r in db.execute(f'PRAGMA table_info("{table}")')}
    values.update({k:v for k,v in dict(owner).items() if k in values})
    values['revision_id']=revision
    if 'id' in values: values['id']=str(uuid4())
    for field in schema(db,table)['fields']:
        if field['options'] and not field['nullable']: values[field['name']]=field['options'][0]
    return values


def listing(db, revision, table):
    spec = schema(db, table)
    rows = [dict(r) for r in db.execute(f'SELECT * FROM "{table}" WHERE revision_id=?', (revision,))]
    rows.sort(key=lambda r:encode(row_key(db,table,r)))
    refs = {}
    for field in spec['fields']:
        if not field['reference']:
            continue
        target, key = field['reference']
        columns = {r['name'] for r in db.execute(f'PRAGMA table_info("{target}")')}
        values = db.execute(f'SELECT * FROM "{target}"' + (' WHERE revision_id=?' if 'revision_id' in columns else ''),
                            (revision,) if 'revision_id' in columns else ())
        refs[field['name']] = [dict(value=r[key], label=' · '.join(str(r[n]) for n in
            ('rpo','name','body','trim','code','kind','currency','amount_meaning') if n in r.keys() and r[n]) or str(r[key])) for r in values]
    return dict(**spec, rows=rows, references=refs, etag=database_hash(db),new_record=new_record(db,revision,table),
                editable_copy_paths=[copy_paths(table,json.loads(row['presentation'])) if 'presentation' in row else [] for row in rows],
                evidence=evidence(db,rows), history=[dict(r) for r in db.execute(
                    'SELECT * FROM authoring_record_change WHERE revision_id=? ORDER BY edit_version DESC',(revision,))])


def copy_editable(table,path):
    name=path[-1]
    if table=='consumer_option': return name in ('description','detail_raw','display_order','display_behavior','projection','emit_code')
    if table=='consumer_configuration': return name=='display_name'
    if table=='consumer_option_context': return True
    if table=='consumer_interior':
        if path[0]=='source': return name in ('Interior Name','Detail from Disclosure','Material','Stitch','Two Tone','Color Overrides')
        if path[0]=='components': return name in ('label','notes')
        return name.endswith(('_label','_display_order')) or name in ('interior_hierarchy_levels','interior_color_family','interior_material_family','notes')
    return name not in ('_row','model_key','model_year','year','step_key','section_key') and not name.endswith('_id')


def copy_paths(table,value,path=()):
    if isinstance(value,(dict,list)):
        items=value.items() if isinstance(value,dict) else enumerate(value)
        return [p for k,v in items for p in copy_paths(table,v,(*path,str(k)))]
    return [list(path)] if copy_editable(table,path) else []


def _presentation(table, before, after):
    if not isinstance(after,str) or len(after)>250000:
        raise ValueError('Invalid presentation')
    old, new = json.loads(before), json.loads(after)
    # Preserve typed field structure and retained identities. Copy/layout fields
    # remain editable. Adding new product identities uses the clone operation.
    def visit(a,b,path=()):
        if a==b and type(a) is type(b): return
        if isinstance(a,dict):
            if not isinstance(b,dict) or a.keys()!=b.keys():
                raise ValueError('Presentation fields must be retained: '+' / '.join(path))
            for k in a:
                visit(a[k],b[k],(*path,k))
        elif isinstance(a,list):
            if not isinstance(b,list) or len(a)!=len(b):
                raise ValueError('Presentation entries must be retained: '+' / '.join(path))
            for i,(x,y) in enumerate(zip(a,b)): visit(x,y,(*path,str(i)))
        elif b is not None and (not isinstance(b,(str,int,bool)) or a is not None and type(a) is not type(b)):
            raise ValueError('Invalid presentation value type: '+' / '.join(path))
        elif a!=b and not copy_editable(table,path):
            raise ValueError('Use the owning product editor for '+' / '.join(path))
    visit(old,new)
    return encode(new)


def operations(db, revision, requests):
    if not isinstance(requests,list) or not 1<=len(requests)<=200:
        raise ValueError('Queue 1–200 related record edits')
    result=[]
    seen=set()
    def add(table,before,after):
        key=row_key(db,table,before or after)
        identity=table,encode(key)
        if identity in seen: raise ValueError('A record can be changed only once per review')
        seen.add(identity)
        result.append(dict(table=table,key=key,before=before,after=after))
    for request in requests:
        table=request['table']; spec=schema(db,table)
        key=request['key']
        if set(key)!=set(spec['keys']) or key.get('revision_id')!=revision:
            raise ValueError('Record key must belong to the selected model')
        action=request.get('action','update')
        before=lookup(db,table,key)
        if action=='create':
            if before is not None: raise ValueError('This record already exists')
            before=new_record(db,revision,table)
            if before is None: raise ValueError('Clone an existing product or edit its owned copy')
            before.update(key)
        elif before is None: raise ValueError('Choose an existing record or clone a record')
        values=request.get('values',{})
        allowed=set(FIELDS[table])
        if action in ('clone','create'): allowed |= set(spec['keys'])-{'revision_id'}
        if not isinstance(values,dict) or set(values)-allowed:
            raise ValueError('Identity, source evidence and system fields are read-only')
        for field in spec['fields']:
            if field['name'] in values and values[field['name']] is not None:
                value=values[field['name']]
                if field['integer'] and type(value) is not int:
                    raise ValueError(field['name']+' requires an integer')
                if not field['integer'] and not isinstance(value,str):
                    raise ValueError(field['name']+' requires text')
        after=before | values
        if 'presentation' in values: after['presentation']=_presentation(table,before['presentation'],values['presentation'])
        if action=='create':
            if table in IDENTITY_RELATIONS:
                identity={k:after[k] for k in ('model_year_id','id','evidence_set_id','decision_set_id')}
                identity.update(predecessor_model_year_id=None,predecessor_id=None)
                add(table+'_identity',None,identity)
            add(table,None,after)
        elif action=='delete':
            if table in ('configuration','option','option_configuration','interior','component','consumer_model') or table.startswith('consumer_'):
                raise ValueError('Retire or disable product records; their identity and history are retained')
            # Typed translation links describe the original source. Archive the
            # removed link in this edit instead of leaving a dangling FK.
            target=table+'_translation'
            if db.execute('SELECT 1 FROM sqlite_master WHERE type="table" AND name=?',(target,)).fetchone():
                refs=[r for r in db.execute(f'PRAGMA foreign_key_list("{target}")') if r['table']==table]
                keys={r['from']:before[r['to']] for r in refs}
                clause=' AND '.join(k+'=?' for k in keys)
                for row in db.execute(f'SELECT * FROM "{target}" WHERE {clause}',tuple(keys.values())):
                    add(target,dict(row),None)
            add(table,before,None)
        elif action=='clone':
            if table.startswith('consumer_'): raise ValueError('Clone the owning product instead')
            if table in IDENTITY_RELATIONS:
                after['id']=request.get('new_id') or str(uuid4())
                identity={k:after[k] for k in ('model_year_id','id','evidence_set_id','decision_set_id')}
                identity.update(predecessor_model_year_id=None,predecessor_id=None)
                add(table+'_identity',None,identity)
            if row_key(db,table,after)==key: raise ValueError('A new membership needs a different key')
            add(table,None,after)
            # Clone complete owned context for a new option/interior/rule. Other
            # rules still refer to their original endpoints until explicitly edited.
            children=[]
            if table=='option': children=[('option_configuration','option_id'),('option_presentation_override','option_id'),('consumer_option','option_id'),('consumer_option_context','option_id')]
            if table=='interior': children=[('interior_configuration','interior_id'),('interior_part','interior_id'),('consumer_interior','interior_id')]
            if table in SCOPES: children=[(table+'_configuration',SCOPES[table])]
            children += {'condition':[('condition_clause','condition_id'),('condition_member','condition_id')],
                         'conflict':[('conflict_member','conflict_id')],
                         'choice_group':[('choice_group_member','group_id')],
                         'replacement_plan':[('replacement_action','plan_id')],
                         'component':[('component_rate','component_id')]}.get(table,[])
            if table=='configuration': raise ValueError('Configuration creation requires a new model foundation; edit existing body/trim records here')
            for child,column in children:
                for row in db.execute(f'SELECT * FROM "{child}" WHERE revision_id=? AND {column}=?',(revision,before['id'])):
                    cloned=dict(row);cloned[column]=after['id']
                    if 'consumer_key' in cloned:
                        cloned['consumer_key']=after['id'];cloned['source_locator']='authoring/clone/'+before['id']
                    if child=='consumer_option':
                        payload=json.loads(cloned['presentation']);payload.update(name=after['name'],rpo=after['rpo'])
                        cloned['presentation']=encode(payload)
                    add(child,None,cloned)
        elif action=='update':
            if before==after: raise ValueError('No changes to '+table)
            add(table,before,after)
        else: raise ValueError('Unknown edit action')
    return result


def synchronize(db,revision,patches):
    """Update duplicated consumer fields owned by typed product records."""
    for kind in ('option','configuration','interior'):
        ids={op['after']['id'] for op in patches if op['table']==kind and op['after']}
        for identifier in ids:
            row=lookup(db,kind,dict(revision_id=revision,id=identifier))
            key=dict(revision_id=revision,**{kind+'_id':identifier})
            mapping=lookup(db,'consumer_'+kind,key)
            if mapping is None: continue  # validation reports a missing mapping
            payload=json.loads(mapping['presentation'])
            if kind=='option': payload.update(name=row['name'],rpo=row['rpo'])
            if kind=='configuration':
                payload.update(body_style=row['body'],trim_level=row['trim'],active=bool(row['enabled']),
                               display_order=row['chooser_order'],base_price=row['starting_amount_minor']/100)
            if kind=='interior':
                payload['source']['Interior Code']=row['code']
                payload['source']['Seat']=lookup(db,'option',dict(revision_id=revision,id=row['seat_option_id']))['rpo']
                # Source row locations remain evidence; the cloned product's
                # own identity must be what its consumers receive.
                payload['source']['interior_id']=identifier
                payload['hierarchy']['interior_id']=identifier
                for component in payload['components']: component['interior_id']=identifier
            after=mapping|dict(presentation=encode(payload))
            if after==mapping: continue
            op=dict(table='consumer_'+kind,key=key,before=mapping,after=after)
            patch_row(db,op)
            existing=next((p for p in patches if p['table']==op['table'] and p['key']==key),None)
            if existing: existing['after']=after
            else: patches.append(op)


def validate_candidate(db,revision):
    validate_mappings(db)
    cat=ConsumerCatalog(db,revision);ev=cat.ev
    for condition in ev.rows['condition']:
        clauses=ev.clauses[condition['id']]
        if (condition['mode']=='always') != (not clauses):
            raise ValueError('Always conditions have no clauses; conjunctions require clauses')
        if any(not ev.condition_members[condition['id'],c['clause_id']] for c in clauses):
            raise ValueError('A condition clause needs at least one member')
    for table in SCOPES:
        required=[field['name'] for field in schema(db,table)['fields'] if field['options']]
        if any(row[name] is None for row in ev.rows[table] for name in required):
            raise ValueError('Executable '+table+' policies must be explicit')
        if any(not any(r['id']==rid for rid,c in ev.scopes[table]) for r in ev.rows[table]):
            raise ValueError('Every '+table+' needs a configuration scope')
    for table,field in (('acquisition','priority'),('content_effect','precedence'),('content_effect','value')):
        if any(row[field] is None for row in ev.rows[table]):
            raise ValueError(table+' requires '+field)
    for table,child,parent in (('replacement_plan','replacement_action','plan_id'),('conflict','conflict_member','conflict_id'),('choice_group','choice_group_member','group_id')):
        if any(not any(m[parent]==row['id'] for m in ev.rows[child]) for row in ev.rows[table]):
            raise ValueError('A '+table+' needs at least one member or action')
    for opt in ev.rows['option']:
        if not opt['name'].strip() or (opt['charge_mode']=='priced' and opt['purchase_amount_minor'] is None):
            raise ValueError('Options need a name and an explicit charge basis')
        mapped=cat.maps['option'][opt['id']]
        if mapped['name']!=opt['name'] or mapped['rpo']!=opt['rpo']:
            raise ValueError('Option copy must retain the owned name and RPO')
    if not any(c['enabled'] for c in ev.configs.values()): raise ValueError('Keep at least one enabled configuration per model')
    for view in cat.maps['option'].values():
        if type(view['emit_code']) is not bool or view['projection'] not in ('resolved_selection','installed_equipment'):
            raise ValueError('Invalid order-code emission or projection')
    for view in cat.maps['interior'].values():
        hierarchy=json.loads(view['hierarchy']['interior_hierarchy_levels'])
        if not isinstance(hierarchy,list) or not hierarchy or any(not isinstance(x,str) for x in hierarchy):
            raise ValueError('Interior hierarchy must be a nonempty list of labels')
    for cfg,cfg_row in ev.configs.items():
        if not cfg_row['enabled']: continue
        if not any(c==cfg and ev.interiors[i]['enabled'] for i,c in ev.interior_scopes):
            raise ValueError('An enabled configuration needs an enabled interior')
        cat.project(ev.state(cfg),'authoring-preview')
    return cat


def project(cat,state):
    return cat.project(state,'authoring-preview') | dict(ownership=[plain(asdict(c)) for c in state.causes])


def projections(db,revision,scenarios):
    cat=ConsumerCatalog(db,revision)
    result=[]
    for cfg,row in cat.ev.configs.items():
        if not row['enabled']:
            result.append(dict(label=row['body']+' '+row['trim'],configuration_id=cfg,steps=[dict(refused='Configuration disabled')]))
            continue
        state=cat.ev.state(cfg)
        result.append(dict(label=row['body']+' '+row['trim']+' · initial build',configuration_id=cfg,
                           steps=[project(cat,state)]))
    for scenario in scenarios:
        cfg=scenario['configuration_id'];state=cat.ev.state(cfg);steps=[project(cat,state)]
        actions=scenario['actions']
        if not isinstance(actions,list) or len(actions)>30: raise ValueError('Use at most 30 build actions')
        for action in actions:
            try:
                state=cat.ev.transition(state,action['action'],action.get('target'))
                steps.append(project(cat,state))
            except EvaluationError as exc:
                steps.append(dict(refused=str(exc)));break
        result.append(dict(label=scenario.get('label','Reviewed build sequence'),configuration_id=cfg,steps=steps))
    return result


def connected(db, revision, patches, strict=False):
    """Show actual condition witnesses and their charges for affected owners.

    Release qualification still runs the complete overlap audit. Draft previews
    name missing witnesses rather than claiming an unexercised rule passed.
    """
    from catalog.semantic_validation import Audit, endpoint, findings
    ids={v for op in patches for row in (op['before'],op['after']) if row
         for k,v in row.items() if (k=='id' or k.endswith('_id')) and isinstance(v,str)
         and k not in ('revision_id','model_year_id','evidence_set_id','decision_set_id','basis_id')}
    rule_tables=set(SCOPES)|{'condition','condition_clause','condition_member','conflict_member','replacement_action','choice_group_member'}
    affected_tables={op['table'] for op in patches}
    cat=ConsumerCatalog(db,revision);result=[]
    if affected_tables & rule_tables or any(t.endswith('_configuration') and t.removesuffix('_configuration') in SCOPES for t in affected_tables):
        audit=Audit(db,revision)
        affected=set()
        for table in SCOPES:
            for rule in audit.ev.rows[table]:
                if not ids.intersection(str(v) for k,v in rule.items() if k=='id' or k.endswith('_id')):
                    continue
                affected.add((table,rule['id']))
                for rid,cfg in sorted(audit.ev.scopes[table]):
                    if rid!=rule['id']: continue
                    condition=rule.get('condition_id') or rule.get('activation_condition_id')
                    wanted=[endpoint(rule)] if table in ('requirement','conflict') else []
                    state=next(audit.conditioned(cfg,condition,wanted),None) if condition else audit.witness(cfg,sorted(audit.ev.members[rule['id']])[:1])
                    if table=='replacement_plan' and state is not None:
                        try:
                            state=cat.ev.transition(state,'select',rule['requested_option_id'])
                        except EvaluationError as exc:
                            if strict:
                                audit._disjoint.cache_clear()
                                raise ValueError('Cannot execute affected replacement: '+str(exc)) from exc
                            state=None
                    if state is None and strict:
                        missing=audit.unavailable_witness(cfg,condition,wanted) if condition else {'status':'unresolved'}
                        if missing['status'] in ('unresolved','no_witness','failed'):
                            audit._disjoint.cache_clear()
                            raise ValueError('Cannot verify affected '+table+' '+rule['id']+' in '+cfg+': '+encode(missing))
                    result.append(dict(label=LABELS[table]+' · '+rule['id'], configuration_id=cfg,
                        state=project(cat,state) if state else None,
                        coverage='Condition witness found' if state else 'No valid witness found; release audit remains required'))
        if strict:
            overlaps=audit.overlaps(affected)
            problems=findings({'lanes':{revision:{'overlaps':overlaps}}})
            if problems:
                audit._disjoint.cache_clear()
                raise ValueError('Affected relationships have unresolved or conflicting overlaps: '+encode(problems[:3]))
        audit._disjoint.cache_clear()
    for cfg,cfg_row in cat.ev.configs.items():
        if not cfg_row['enabled']: continue
        for oid in sorted(ids & cat.ev.options.keys()):
            try:
                state=cat.ev.transition(cat.ev.state(cfg),'select',oid)
                result.append(dict(label='Select '+cat.option(oid)['label'],configuration_id=cfg,state=project(cat,state)))
            except EvaluationError as exc:
                result.append(dict(label='Select '+cat.option(oid)['label'],configuration_id=cfg,refused=str(exc)))
        interiors=set(ids & cat.ev.interiors.keys())
        interiors.update(r['interior_id'] for r in cat.ev.rows['interior_part'] if r['component_id'] in ids or r['option_id'] in ids)
        for iid in sorted(interiors):
            if (iid,cfg) not in cat.ev.interior_scopes or not cat.ev.interiors[iid]['enabled']: continue
            state=cat.ev.transition(cat.ev.state(cfg),'interior',iid)
            result.append(dict(label='Interior '+iid,configuration_id=cfg,state=project(cat,state)))
    return result


def preview(db,revision,etag,requests,reason,scenarios=None):
    if database_hash(db)!=etag: raise ValueError('Stale edit: reload and review again')
    if not isinstance(reason,str) or not 1<=len(reason.strip())<=2000: raise ValueError('A change reason is required')
    state=db.execute('SELECT state FROM catalog_revision WHERE revision_id=?',(revision,)).fetchone()
    if not state or state[0]!='draft': raise ValueError('Choose a draft model revision')
    scenarios=scenarios or []
    if not isinstance(scenarios,list) or len(scenarios)>32: raise ValueError('Use at most 32 build sequences')
    requests=json.loads(encode(requests))
    for req in requests:
        if req.get('action')=='clone' and req['table'] in IDENTITY_RELATIONS:
            req.setdefault('new_id',str(uuid4()))
    patches=operations(db,revision,requests)
    before=projections(db,revision,scenarios)
    connected_before=connected(db,revision,patches)
    db.execute('SAVEPOINT record_preview')
    try:
        db.execute('PRAGMA defer_foreign_keys=ON')
        for op in patches: patch_row(db,op)
        synchronize(db,revision,patches)
        validate_candidate(db,revision)
        after=projections(db,revision,scenarios)
        connected_after=connected(db,revision,patches,strict=True)
        prior={(item['label'],item['configuration_id']):item for item in connected_before}
        for item in connected_after:
            old=prior.get((item['label'],item['configuration_id']))
            if old and old.get('state') and not item.get('state') and 'coverage' in item:
                raise ValueError('Previously active relationship has no valid witness: '+item['label']+' in '+item['configuration_id']+'; revise its scope or dependencies')
    finally:
        db.execute('ROLLBACK TO record_preview');db.execute('RELEASE record_preview')
    return dict(kind='records',revision_id=revision,etag=etag,requests=requests,operations=patches,
                reason=reason.strip(),scenarios=scenarios,before_outcomes=before,after_outcomes=after,
                connected_before=connected_before,connected_after=connected_after,
                evidence=evidence(db,[op['before'] or op['after'] for op in patches]))


def save(db,change):
    if db.in_transaction: raise ValueError('Finish the current transaction before saving')
    with db:
        db.execute('BEGIN IMMEDIATE')
        reviewed=preview(db,change['revision_id'],change['etag'],change['requests'],change['reason'],change['scenarios'])
        if reviewed!=change:
            raise ValueError('Preview changed; review again')
        db.execute('PRAGMA defer_foreign_keys=ON')
        for op in change['operations']: patch_row(db,op)
        validate_candidate(db,change['revision_id'])
        db.execute('UPDATE catalog_revision SET edit_version=edit_version+1 WHERE revision_id=?',(change['revision_id'],))
        version=db.execute('SELECT edit_version FROM catalog_revision WHERE revision_id=?',(change['revision_id'],)).fetchone()[0]
        db.execute('INSERT INTO authoring_record_change VALUES (?,?,?,?,?,?,?,?)',
                   (str(uuid4()),change['revision_id'],version,datetime.now(timezone.utc).isoformat(),change['reason'],
                    encode(change['operations']),encode(change['evidence']),encode(change['scenarios'])))
    return dict(saved=True,edit_version=version,etag=database_hash(db))
