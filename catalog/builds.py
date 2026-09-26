"""Customer builds as replayable, signed history: shared by the server and the browser.

A build token carries the release, model, configuration and confirmed actions;
the build is rebuilt by replaying those actions. A preview returns a short-lived
signed pending token bound to that build and warning; confirmation re-derives
the preview and requires the same warning. Dealer payloads use the rebuilt state.
"""
import base64
import hashlib
import hmac
import json
import time

from catalog import dealer
from catalog.consumers import ConsumerSession, encode
from catalog.evaluator import EvaluationError

MAX_HISTORY = 200          # confirmed actions carried in one build token
PENDING_SECONDS = 15 * 60  # how long a reviewed change can wait for confirmation
UNAVAILABLE = 'This saved build can no longer be opened; start a new build'


def _b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()


def _unb64(text):
    return base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))


class Tokens:
    """HMAC-signed JSON. The kind field keeps build and pending tokens apart."""
    def __init__(self, key):
        self.key = key

    def _mac(self, body):
        return hmac.new(self.key, body.encode(), hashlib.sha256).digest()

    def sign(self, kind, payload):
        body = _b64(encode(dict(payload, k=kind, v=1)).encode())
        return body + '.' + _b64(self._mac(body))

    def verify(self, token, kind):
        try:
            body, mac = str(token).split('.')
            valid = hmac.compare_digest(_unb64(mac), self._mac(body))
            payload = json.loads(_unb64(body)) if valid else None
        except (ValueError, TypeError):
            payload = None
        if not isinstance(payload, dict) or payload.get('k') != kind or payload.get('v') != 1:
            raise ValueError('Missing, altered or foreign build' if kind == 'build'
                             else 'Missing, stale, foreign or altered confirmation')
        return payload


def description(release_id, default_model, catalogs, dealer_submissions=False):
    """What the form loads first: release identity, dealer mode and every model's contract."""
    return dict(release_id=release_id, default_model=default_model,
                dealer=dict(enabled=dealer_submissions, endpoint=dealer.ENDPOINT if dealer_submissions else None,
                            site_key=dealer.SITE_KEY if dealer_submissions else None),
                models={key: catalog.contract() for key, catalog in catalogs.items()})


class Builds:
    """The form's operations on one release. catalogs maps model keys to ConsumerCatalogs."""
    def __init__(self, identifier, catalogs, tokens, dealer_submissions=False):
        self.identifier, self.catalogs, self.tokens = identifier, catalogs, tokens
        self.dealer_submissions = dealer_submissions
        # The last build handed out, so the next request on it need not replay
        # every action. Only an exact token match with an unchanged version reuses it.
        self.last = None

    def response(self, build, session, cards_for, notice=None):
        build = dict(r=self.identifier, m=build['m'], c=build['c'], h=build['h'])
        token = self.tokens.sign('build', build)
        self.last = (token, build, session)
        catalog = session.catalog
        result = dict(build_token=token, model=build['m'], configuration_id=build['c'], **session.current(),
                      card_steps=catalog.card_steps(build['c']),
                      cards=catalog.cards(session._session.state, cards_for))
        return dict(result, notice=notice) if notice else result

    def rebuild(self, token):
        """Verify a build token and replay its confirmed actions on this release."""
        if self.last and self.last[0] == token and self.last[2].version == len(self.last[1]['h']):
            _, build, session = self.last
            session.cancel(session.version)  # drop any held preview, as a fresh replay would
            return build, session
        build = self.tokens.verify(token, 'build')
        catalog = self.catalogs.get(build.get('m'))
        history = build.get('h')
        if catalog is None or build.get('c') not in catalog.ev.configs or not isinstance(history, list) or len(history) > MAX_HISTORY:
            raise ValueError(UNAVAILABLE)
        session = ConsumerSession(catalog, build['c'], self.identifier)
        try:
            for action, target in history:
                step = session.preview(action, target, session.version)
                session.confirm(step['token'], step['warning_sha256'], session.version)
        except (EvaluationError, TypeError, ValueError):
            raise ValueError(UNAVAILABLE) from None
        return build, session

    def dispatch(self, path, body):
        # Which steps to price; None prices every card.
        cards_for = body.get('cards_for')
        if cards_for is not None and not (isinstance(cards_for, list) and all(isinstance(k, str) for k in cards_for)):
            raise ValueError('cards_for must be a list of step keys')
        if path == '/api/session':
            catalog = self.catalogs.get(body['model'])
            if catalog is None or body['configuration_id'] not in catalog.ev.configs:
                raise ValueError('Choose an available model and configuration')
            session = ConsumerSession(catalog, body['configuration_id'], self.identifier)
            return self.response(dict(m=body['model'], c=body['configuration_id'], h=[]), session, cards_for)
        build, session = self.rebuild(body.get('build_token'))
        if path == '/api/restore':
            notice = None if build['r'] == self.identifier else \
                'The catalog was updated since this build was saved. Prices and availability reflect the current catalog.'
            return self.response(build, session, cards_for, notice)
        if path == '/api/cards':
            return self.response(build, session, cards_for)
        if path == '/api/preview':
            if len(build['h']) >= MAX_HISTORY:
                raise ValueError('This build has reached its change limit; download it or start a new build')
            result = session.preview(body['action'], body.get('target'), body['version'])
            pending = self.tokens.sign('pending', dict(b=hashlib.sha256(body['build_token'].encode()).hexdigest(),
                a=body['action'], t=body.get('target'), w=result['warning_sha256'], x=int(time.time()) + PENDING_SECONDS))
            return dict(result, token=pending)
        if path == '/api/confirm':
            pending = self.tokens.verify(body.get('token'), 'pending')
            if (pending['b'] != hashlib.sha256(body['build_token'].encode()).hexdigest()
                    or pending['w'] != body.get('warning_sha256') or pending['x'] < time.time()):
                raise ValueError('Missing, stale, foreign or altered confirmation')
            session._version(body['version'])
            # Re-derive the change; it is applied only if the warning is identical.
            fresh = session.preview(pending['a'], pending['t'], session.version)
            if fresh['warning_sha256'] != pending['w']:
                raise ValueError('This change no longer matches what you reviewed; review it again')
            session.confirm(fresh['token'], fresh['warning_sha256'], session.version)
            return self.response(dict(build, h=build['h'] + [[pending['a'], pending['t']]]), session, cards_for)
        if path == '/api/cancel':
            session._version(body['version'])
            return self.response(build, session, cards_for)
        if path == '/api/order':
            return session.order()
        if path == '/api/dealer/review':
            return dealer.review(session, body['version'])
        if path == '/api/dealer/prepare':
            # The dealer contract accepts only contact details, version and security token.
            fields = {k: v for k, v in body.items() if k not in ('build_token', 'cards_for')}
            return dealer.prepare(session, fields, require_turnstile=self.dealer_submissions)
        raise ValueError('Unknown operation')
