"""Publishing static bundles by sftp batch and checking what a host serves."""
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shlex
import shutil
import tempfile
import threading
import unittest

from catalog import static_bundle, static_site


def bundle(folder, release, page='<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body></body></html>'):
    folder = Path(folder); (folder / 'catalog').mkdir(parents=True)
    (folder / 'index.html').write_text(page)
    (folder / 'style.css').write_text(f'/* {release} */')
    (folder / 'catalog/model.sqlite.gz').write_bytes(b'\x1f\x8b' + release.encode())
    files = {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob('*')) if p.is_file()}
    (folder / 'bundle.json').write_text(json.dumps(dict(format=static_bundle.FORMAT, release_id=release, files=files)))
    return folder


def local_sftp(server_root, log):
    """Interpret sftp batch commands against a local folder, like the remote server."""
    def run(target, commands):
        log.append(commands); out = []
        for command in commands:
            op, *args = shlex.split(command)
            optional, op = op.startswith('-'), op.lstrip('-')
            try:
                if op == 'mkdir':
                    (server_root / args[0]).mkdir()
                elif op == 'put':
                    shutil.copyfile(args[0], server_root / args[1])
                elif op == 'rename':
                    # posix-rename: a file is replaced atomically, a folder never is.
                    if (server_root / args[1]).is_dir():
                        raise OSError('exists')
                    (server_root / args[0]).replace(server_root / args[1])
                elif op == 'ls':
                    out += [p.name for p in (server_root / args[-1]).iterdir()]
                else:
                    raise AssertionError(op)
            except OSError:
                if not optional:
                    raise
        return '\n'.join(out)
    return run


class StaticSiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.server = self.root / 'server'; (self.server / 'htdocs').mkdir(parents=True)
        httpd = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(self.server / 'htdocs')))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        self.addCleanup(httpd.server_close); self.addCleanup(httpd.shutdown)
        self.url = f'http://127.0.0.1:{httpd.server_port}/order-form/'
        self.log = []
        self.run_sftp = local_sftp(self.server, self.log)

    def publish(self, folder):
        return static_site.publish(folder, 'user@host', 'htdocs/order-form/', run=self.run_sftp)

    def test_publish_switch_rollback_and_check(self):
        first, second = bundle(self.root / 'a', 'release-a'), bundle(self.root / 'b', 'release-b')
        result = self.publish(first)
        self.assertEqual((result['release_id'], result['uploaded']), ('release-a', True))
        checked = static_site.check(self.url)
        self.assertEqual((checked['release_id'], checked['failed'], checked['problems'], checked['files']), ('release-a', [], [], 3))
        self.assertEqual(checked['current']['folder'], static_site.folder_name(first))
        self.assertTrue(checked['release_folder'].endswith(f'/order-form/releases/{result["folder"]}/'))
        # The pointer page is the bundle page, resolving inside its release folder.
        page = (self.server / 'htdocs/order-form/index.html').read_text()
        self.assertIn(f'<head><base href="releases/{result["folder"]}/"><meta charset', page)
        self.assertEqual(self.publish(second)['release_id'], 'release-b')
        self.assertEqual(static_site.check(self.url)['release_id'], 'release-b')
        # Rolling back re-points without uploading again; both folders stay.
        uploads = len(self.log)
        self.assertFalse(self.publish(first)['uploaded'])
        self.assertEqual(len(self.log), uploads + 2)  # listing and pointer only
        self.assertTrue(all(c.startswith('put') and '/.' in c or c.startswith('rename') for c in self.log[-1]))
        self.assertEqual([p.name for p in (self.server / 'htdocs/order-form').iterdir() if p.name.startswith('.')], [])
        self.assertEqual(static_site.check(self.url)['release_id'], 'release-a')
        self.assertEqual(sorted(p.name for p in (self.server / 'htdocs/order-form/releases').iterdir() if not p.name.startswith('.')),
                         sorted([static_site.folder_name(first), static_site.folder_name(second)]))

    def test_check_reports_altered_or_missing_files(self):
        folder = self.publish(bundle(self.root / 'a', 'release-a'))['folder']
        served = self.server / 'htdocs/order-form/releases' / folder
        (served / 'style.css').write_text('/* stale */')
        (served / 'catalog/model.sqlite.gz').unlink()
        self.assertEqual(static_site.check(self.url)['failed'], ['catalog/model.sqlite.gz', 'style.css'])

    def test_check_reports_pointer_files_that_disagree(self):
        first, second = bundle(self.root / 'a', 'release-a'), bundle(self.root / 'b', 'release-b')
        self.publish(first); stale = (self.server / 'htdocs/order-form/current.json').read_text()
        self.publish(second)
        live = self.server / 'htdocs/order-form'
        (live / 'current.json').write_text(stale)  # an interrupted switch
        self.assertIn('current.json', static_site.check(self.url)['problems'][0])
        (live / 'current.json').unlink()
        self.assertEqual(len(static_site.check(self.url)['problems']), 1)
        self.publish(second)
        page = (live / 'index.html').read_text()
        (live / 'index.html').write_text(page.replace('</body>', '<script>x</script></body>'))
        self.assertEqual(static_site.check(self.url)['problems'], ['The form page is not the release page with its <base>'])

    def test_a_bundle_that_does_not_verify_is_not_uploaded(self):
        folder = bundle(self.root / 'a', 'release-a')
        (folder / 'style.css').write_text('changed')
        with self.assertRaises(ValueError):
            self.publish(folder)
        self.assertEqual(self.log, [])

    def test_pointer_refuses_pages_it_cannot_redirect(self):
        for page in ('<html><body></body></html>', '<html><head><base href="/"></head></html>'):
            with self.subTest(page=page), tempfile.TemporaryDirectory() as folder:
                with self.assertRaises(ValueError):
                    static_site.pointer_page(bundle(folder, 'r', page), 'f')


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


if __name__ == '__main__':
    unittest.main()
