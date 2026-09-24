"""Compressed, rotating backups of the local authoring draft.

Run: python -m catalog.draft_backup list BACKUP_DIR
     python -m catalog.draft_backup restore BACKUP_FILE --database NEW_DRAFT
Restore returns the draft exactly as it was, including saved edits that are
not yet accepted, and never overwrites an existing database.
"""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import gzip
import hashlib
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile

from catalog import authoring

PREFIX, SUFFIX = 'draft-', '.sqlite.gz'
KEEP_RECENT, KEEP_DAYS = 20, 30


def backups(directory):
    """Draft backups, newest first. Names sort by UTC time."""
    directory = Path(directory)
    if not directory.is_dir():
        return []
    return sorted((p for p in directory.iterdir() if p.name.startswith(PREFIX) and p.name.endswith(SUFFIX)), reverse=True)


def snapshot(database, directory, now=None):
    """Write one consistent compressed copy unless the newest backup is identical.

    Returns the backup path, or None when nothing changed since the last one.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    now = now or datetime.now(timezone.utc)
    stage = Path(tempfile.mkdtemp(prefix='.draft-', dir=directory))
    try:
        copy = stage / 'draft.sqlite'
        with closing(authoring.open_workspace(database)) as db, closing(sqlite3.connect(copy)) as target:
            db.backup(target)
        content = hashlib.sha256(copy.read_bytes()).hexdigest()[:16]
        latest = backups(directory)
        if latest and latest[0].name.endswith(f'-{content}{SUFFIX}'):
            return None
        packed = stage / 'draft.sqlite.gz'
        with copy.open('rb') as raw, gzip.open(packed, 'wb', compresslevel=1) as out:
            shutil.copyfileobj(raw, out)
        destination = directory / f'{PREFIX}{now.strftime("%Y%m%dT%H%M%S%fZ")}-{content}{SUFFIX}'
        os.replace(packed, destination)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    prune(directory, now)
    return destination


def prune(directory, now=None):
    """Keep the newest KEEP_RECENT backups and the newest one of each of the last KEEP_DAYS days."""
    now = now or datetime.now(timezone.utc)
    keep, days = set(), set()
    for index, path in enumerate(backups(directory)):
        stamp = datetime.strptime(path.name[len(PREFIX):len(PREFIX) + 22], '%Y%m%dT%H%M%S%fZ').replace(tzinfo=timezone.utc)
        day = stamp.date()
        if index < KEEP_RECENT or ((now - stamp).days < KEEP_DAYS and day not in days):
            keep.add(path)
        days.add(day)
    for path in backups(directory):
        if path not in keep:
            path.unlink()


def restore(backup, database):
    """Decompress and check a backup, then place it at a new path."""
    backup, database = Path(backup), Path(database)
    if database.exists():
        raise ValueError('Restore destination already exists')
    database.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.restore-', dir=database.resolve().parent) as stage:
        copy = Path(stage) / 'draft.sqlite'
        with gzip.open(backup, 'rb') as packed, copy.open('wb') as raw:
            shutil.copyfileobj(packed, raw)
        with closing(sqlite3.connect(copy.resolve().as_uri() + '?mode=ro', uri=True)) as db:
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('Backup database failed its integrity check')
        with closing(authoring.open_workspace(copy)):
            pass
        # A hard link fails instead of replacing a file created meanwhile.
        os.link(copy, database)
    return database


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    listing = commands.add_parser('list', help='Show draft backups, newest first')
    listing.add_argument('directory', type=Path)
    recover = commands.add_parser('restore', help='Create a new draft workspace from a backup')
    recover.add_argument('backup', type=Path)
    recover.add_argument('--database', type=Path, required=True, help='New draft path; must not exist')
    args = parser.parse_args()
    if args.command == 'list':
        for path in backups(args.directory):
            print(path.name, f'{path.stat().st_size / 2**20:.1f} MB')
    else:
        restore(args.backup, args.database)
        print('Restored draft workspace:', args.database)


if __name__ == '__main__':
    main()
