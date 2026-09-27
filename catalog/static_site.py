"""Put static bundles on the WordPress site and check what it serves.

Run: python -m catalog.static_site publish BUNDLE --target USER@sftp.wp.com --root htdocs/order-form
     python -m catalog.static_site check https://SITE/order-form/

Each bundle is uploaded once into its own folder, releases/<id>/, named by the
digest of its bundle.json, so every script and data file has a URL that no
other release shares and caches cannot mix two releases. The form's address
(ROOT/index.html) is the bundle's page with <base href="releases/<id>/">;
switching or rolling back rewrites only that file and current.json.
Publishing a bundle whose folder is already there only switches to it.

Uploads use the system sftp command with the owner's own SSH login (for
WordPress.com: an SSH key added under Hosting > SFTP/SSH). No credentials are
read, stored or passed by this module.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import secrets
import subprocess
import tempfile
import time
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from catalog import static_bundle

AGENT = 'CorvetteCatalog-static-site-check'


def folder_name(bundle):
    return hashlib.sha256((Path(bundle) / 'bundle.json').read_bytes()).hexdigest()[:16]


def pointer_html(page, folder):
    """A bundle page resolving every relative URL inside its release folder."""
    head = re.search(r'<head[^>]*>', page)
    if head is None or '<base' in page:
        raise ValueError('The bundle page needs a <head> and no <base> of its own')
    return page[:head.end()] + f'<base href="releases/{folder}/">' + page[head.end():]


def pointer_page(bundle, folder):
    return pointer_html((Path(bundle) / 'index.html').read_text(), folder)


def _quote(path):
    if '"' in str(path) or '\n' in str(path):
        raise ValueError(f'Unsupported path: {path}')
    return f'"{path}"'


def sftp(target, commands):
    """Run sftp batch commands with the owner's SSH login; return its output."""
    with tempfile.NamedTemporaryFile('w', suffix='.sftp') as batch:
        batch.write('\n'.join(commands) + '\n'); batch.flush()
        result = subprocess.run(['sftp', '-b', batch.name, '-o', 'BatchMode=yes', target],
                                capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'sftp failed ({result.returncode}): {result.stderr.strip() or result.stdout.strip()}')
    return result.stdout


def upload_commands(bundle, root, folder, token):
    """Upload into a hidden staging folder, then rename it into place."""
    bundle, stage = Path(bundle), f'{root}/releases/.{folder}-{token}'
    commands = [f'mkdir {_quote(stage)}']
    for path in sorted(bundle.rglob('*')):
        remote = f'{stage}/{path.relative_to(bundle)}'
        commands.append(f'mkdir {_quote(remote)}' if path.is_dir() else f'put {_quote(path)} {_quote(remote)}')
    commands.append(f'rename {_quote(stage)} {_quote(f"{root}/releases/{folder}")}')
    return commands


def publish(bundle, target, root, run=sftp):
    bundle = Path(bundle)
    description = static_bundle.verify(bundle)
    folder = folder_name(bundle)
    root = root.rstrip('/')
    listing = run(target, [f'-mkdir {_quote(root)}', f'-mkdir {_quote(root + "/releases")}',
                           f'ls -1a {_quote(root + "/releases")}'])
    present = {Path(line.strip()).name for line in listing.splitlines() if not line.startswith('sftp>')}
    if folder not in present:
        run(target, upload_commands(bundle, root, folder, secrets.token_hex(4)))
    current = dict(folder=folder, release_id=description['release_id'],
                   dealer_submissions=description.get('dealer_submissions') is True)
    with tempfile.TemporaryDirectory() as scratch:
        (Path(scratch) / 'current.json').write_text(json.dumps(current, indent=2, sort_keys=True) + '\n')
        (Path(scratch) / 'index.html').write_text(pointer_page(bundle, folder))
        # Each file is uploaded under a temporary name and renamed over the live
        # one. OpenSSH sftp renames with the server's posix-rename extension, which
        # replaces atomically; without it the rename fails and the live page stays.
        # current.json first: it only describes; index.html is the switch.
        token, commands = secrets.token_hex(4), []
        for name in ('current.json', 'index.html'):
            temporary = f'{root}/.{name}.{token}'
            commands += [f'put {_quote(Path(scratch) / name)} {_quote(temporary)}',
                         f'rename {_quote(temporary)} {_quote(f"{root}/{name}")}']
        run(target, commands)
    return dict(current, uploaded=folder not in present)


def _get(url, attempts=3):
    """(status, headers, body); status 0 when the host could not be reached."""
    for attempt in range(attempts):
        try:
            with urlopen(Request(url, headers={'User-Agent': AGENT, 'Cache-Control': 'no-cache'}), timeout=60) as response:
                return response.status, response.headers, response.read()
        except HTTPError as error:
            with error:
                return error.code, error.headers, b''
        except OSError:  # resets and timeouts: retry, then report the file as failed
            time.sleep(attempt + 1)
    return 0, {}, b''


def check(url, workers=8):
    """Fetch the form as a browser would and compare every file with bundle.json."""
    url = url if url.endswith(('/', '.html')) else url + '/'
    status, page_headers, page = _get(url)
    if status != 200:
        raise ValueError(f'{url} answered {status}')
    base = re.search(r'<base href="([^"]+)"', page.decode())
    if base is None:
        raise ValueError(f'{url} is not a published form page (no <base>)')
    folder = base.group(1).removeprefix('releases/').rstrip('/')
    base = urljoin(url, base.group(1))
    _, _, raw = _get(base + 'bundle.json')
    description = json.loads(raw)
    _, _, current = _get(urljoin(url, 'current.json'))
    _, _, release_page = _get(base + 'index.html')
    try:
        current = json.loads(current)
    except ValueError:
        current = None
    # The two pointer files are written separately; both must name this release.
    problems = []
    expected = dict(folder=folder, release_id=description['release_id'],
                    dealer_submissions=description.get('dealer_submissions') is True)
    if current != expected:
        problems.append(f'current.json does not describe the served release: {current}')
    try:
        if pointer_html(release_page.decode(), folder).encode() != page:
            problems.append('The form page is not the release page with its <base>')
    except (ValueError, UnicodeDecodeError):
        problems.append('The release page cannot be checked')
    def fetch(item):
        path, expected = item
        status, headers, body = _get(base + path)
        return path, status, headers, hashlib.sha256(body).hexdigest() == expected
    with ThreadPoolExecutor(workers) as pool:
        results = list(pool.map(fetch, sorted(description['files'].items())))
    kinds = {}
    for path, status, headers, same in results:
        kinds.setdefault(Path(path).suffix or path, dict(status=status, content_type=headers.get('Content-Type'),
            content_encoding=headers.get('Content-Encoding'), cache_control=headers.get('Cache-Control')))
    return dict(page=dict(url=url, cache_control=page_headers.get('Cache-Control')), release_folder=base,
                release_id=description['release_id'], dealer_submissions=description.get('dealer_submissions') is True,
                current=current, problems=problems, files=len(results),
                failed=[path for path, status, _, same in results if status != 200 or not same], kinds=kinds)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    put = commands.add_parser('publish', help='Upload a bundle (if new) and switch the form to it')
    put.add_argument('bundle', type=Path)
    put.add_argument('--target', required=True, help='SFTP login, e.g. USER@sftp.wp.com')
    put.add_argument('--root', required=True, help='Remote folder of the form, e.g. htdocs/order-form')
    look = commands.add_parser('check', help='Fetch the published form and compare every file')
    look.add_argument('url')
    args = parser.parse_args()
    if args.command == 'publish':
        print(json.dumps(publish(args.bundle, args.target, args.root), indent=2))
    else:
        result = check(args.url)
        print(json.dumps(result, indent=2))
        if result['failed'] or result['problems']:
            raise SystemExit(f'{len(result["failed"])} files missing or different; {len(result["problems"])} pointer problems')


if __name__ == '__main__':
    main()
