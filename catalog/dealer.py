"""Existing dealer wire contract, built only from confirmed catalog state.

This module constructs a payload; it never contacts the dealership or stores
customer details. Transport and Turnstile verification retain the existing route.
"""
from datetime import datetime, timezone
from html import escape
import re

from catalog.consumers import active, digest
from catalog.evaluator import EvaluationError

ENDPOINT = 'https://stingraychevroletcorvette.com/wp-json/corvette-build/v1/submit'
SITE_KEY = '0x4AAAAAADQDIWu6RmhF8_wH'
CUSTOMER_LIMITS = dict(name=200, email=254, phone=80, address=1000, comments=4000)


def money(amount_minor):
    whole, fraction = divmod(amount_minor, 100)
    return f'${whole:,}' + (f'.{fraction:02d}' if fraction else '')


def customer_details(value):
    if not isinstance(value, dict) or set(value) - CUSTOMER_LIMITS.keys():
        raise ValueError('Provide customer contact fields only')
    customer = {}
    for field, limit in CUSTOMER_LIMITS.items():
        text = value.get(field, '')
        if not isinstance(text, str) or len(text) > limit or '\x00' in text:
            raise ValueError('Invalid customer ' + field)
        customer[field] = text.strip()
    if not customer['name']:
        raise ValueError('Name is required.')
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', customer['email']):
        raise ValueError('Enter a valid email address.')
    if not customer['comments']:
        del customer['comments']
    return customer


def review(session, version):
    session._version(version)
    build = session.order()  # Refuses pending changes and incomplete builds.
    cat = session.catalog
    cfg = cat.maps['configuration'][build['configuration_id']]
    charges = {(c['owner_kind'], c['owner_id']): c['amount_minor'] for c in build['charges']}
    allocated = set()
    summary = sorted((r for r in cat.model['presentation']['order_summary_sections'] if active(r['active'])),
                     key=lambda r: r['display_order'])
    sections = {r['section_key']: dict(section=r['section_label'], items=[]) for r in summary
                if r['section_key'] not in ('vehicle', 'pricing_summary')}

    def add(section, rpo, label, owner=None):
        if section not in sections:
            raise EvaluationError('Missing dealer summary destination: ' + section)
        amount = charges.get(owner, 0)
        if owner in allocated:
            raise EvaluationError('A dealer summary charge was included twice')
        if owner is not None:
            allocated.add(owner)
        sections[section]['items'].append(dict(rpo=rpo or '', label=label, price=amount / 100))
        return amount

    interior = build['selected_interior']
    # Retained component rows supply labels only. Actual seat/part ownership and
    # every amount come from the typed selected interior and evaluator charges.
    interior_lines = []
    moved_options = set()
    if interior:
        source_labels = {(r['component_type'], r['rpo']): r['label'] for r in interior['components']}
        seat = interior['seat_option']
        if ('seat', seat['rpo']) in source_labels:
            interior_lines.append((seat['rpo'] if cat.maps['option'][seat['option_id']]['emit_code'] else '',
                                   source_labels['seat', seat['rpo']], ('option', seat['option_id'])))
            moved_options.add(seat['option_id'])
        for part in interior['configured_components']:
            if part['option']:
                item = part['option']; oid = item['option_id']
                interior_lines.append((item['rpo'] if cat.maps['option'][oid]['emit_code'] else '',
                    source_labels.get((part['role'], item['rpo']), item['label']), ('option', oid)))
                moved_options.add(oid)
            else:
                item = part['component']
                interior_lines.append((item['code'], source_labels.get((part['role'], item['code']),
                    part['role'].replace('_', ' ').title() + ' ' + item['code']), ('component', item['id'])))

    total = 0
    causes = {}
    customer_roots = set()
    for cause in session._session.state.causes:
        causes.setdefault(cause.option_id, set()).add(cause.origin)
        if any(not root.startswith('configuration:') for root in cause.roots):
            customer_roots.add(cause.option_id)
    for item in build['summary_items']:
        oid = item['option_id']
        if oid in moved_options:
            continue
        origins = causes.get(oid, set())
        # Standard equipment is a separate rollup in the existing form. Keep
        # actual selections, dependencies and every charge in the dealer recap.
        # A hidden configuration default (for example ZR1 EFR) is not a choice.
        if not charges.get(('option', oid), 0) and (
                origins <= {'standard'} or
                item['step_key'] == 'standard_equipment' and oid not in customer_roots or
                item['display_behavior'] == 'hidden' and origins <= {'standard', 'default'}):
            continue
        code = item['rpo'] if cat.maps['option'][oid]['emit_code'] else ''
        total += add(item['summary_section_id'], code, item['label'], ('option', oid))
    if interior:
        total += add('seats_interior', interior['configured_code'], interior['source']['Interior Name'])
        for code, label, owner in interior_lines:
            total += add('seats_interior', code, label, owner)
    base = charges['configuration', build['configuration_id']]
    if total + base != build['total_minor']:
        raise EvaluationError('Dealer summary does not account for every catalog charge')
    return dict(release_id=session.release_id, revision_id=cat.revision, version=session.version,
        model=cat.model['registry_key'], vehicle=dict(body_style=cfg['body_style'], trim_level=cfg['trim_level'].upper(),
            display_name=cfg['display_name'], base_price=base / 100),
        sections=[s for s in sections.values() if s['items']], msrp=money(build['total_minor']))


def summary_html(order, customer, submitted_at):
    # The legacy field is called plain_text_summary but intentionally contains
    # this small escaped HTML fragment for the existing dealer receiver.
    safe = lambda value: escape(str(value), quote=True)
    lines = ['<p>', f'<strong>Name:</strong> {safe(customer["name"])}<br>',
        f'<strong>Email:</strong> {safe(customer["email"])}<br>',
        f'<strong>Phone:</strong> {safe(customer["phone"])}']
    if customer.get('comments'):
        lines.append(f'<br><strong>Comments:</strong> {safe(customer["comments"])}')
    lines.extend(['</p>', f'<p><strong>Submitted:</strong> {safe(submitted_at)}</p>',
        '<p><strong><u>Variant</u></strong></p>',
        f'<ul><li>{safe(order["vehicle"]["display_name"])}</li></ul>'])
    for section in order['sections']:
        lines.extend([f'<p><strong><u>{safe(section["section"].title())}</u></strong></p>', '<ul>'])
        for item in section['items']:
            label = (item['rpo'] + ' ' + item['label']).strip()
            amount = round(item['price'] * 100)
            lines.append(f'<li>{safe(label)}: {money(amount)}</li>')
        lines.append('</ul>')
    lines.append(f'<p><strong>Total MSRP: {safe(order["msrp"])}</strong></p>')
    return ''.join(lines)


def prepare(session, body, require_turnstile=True):
    if set(body) != {'version', 'customer', 'turnstile_token'}:
        raise ValueError('Provide contact details and the confirmed build version only')
    customer = customer_details(body['customer'])
    token = body['turnstile_token']
    if not isinstance(token, str) or len(token) > 2048 or require_turnstile and not token.strip():
        raise ValueError('Security check is required. Please try again.')
    order = review(session, body['version'])
    submitted_at = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    payload = dict(model=order['model'], customer=customer, vehicle=order['vehicle'], sections=order['sections'],
        msrp=order['msrp'], plain_text_summary=summary_html(order, customer, submitted_at), turnstile_token=token)
    return dict(release_id=session.release_id, revision_id=session.catalog.revision, version=session.version,
                payload=payload, payload_sha256=digest(payload))
