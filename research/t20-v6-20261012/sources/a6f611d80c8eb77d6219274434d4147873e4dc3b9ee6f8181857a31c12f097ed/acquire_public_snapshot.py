#!/usr/bin/env python3
"""Read-only public-byte acquisition after connector access; no credentials used.

A failed public transport is recorded, never replaced by a fake snapshot.
No repository code is executed. Source bytes are copied only into this packet.
"""
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from hashlib import sha1, sha256
from datetime import datetime, timezone
import json, zipfile, stat

BASE = Path(__file__).resolve().parents[1]
PIN = 'f50dc1aee52356cc6adbef342387576b02afc124'
EXPECTED_TREE = 'afd612bcb4bf2a65727f82283e3a894d497f2865'
DEST = BASE / 'sources' / 'public_snapshot'
DEST.mkdir(parents=True, exist_ok=True)
receipt = {'repository': 'theislampill/orthemology', 'requested_pin': PIN,
           'expected_tree_from_prior_connector_read': EXPECTED_TREE,
           'captured_at_utc': datetime.now(timezone.utc).isoformat(),
           'operations': [], 'current_public_api_head_verified': False,
           'snapshot_tree_verified': False, 'semantic_review_credit': 0}

def get(url):
    with urlopen(Request(url, headers={'User-Agent':'Orthemology-read-only-research/1.0'}), timeout=20) as r:
        return r.read()

try:
    url = 'https://api.github.com/repos/theislampill/orthemology/branches/main'
    data = get(url)
    branch = json.loads(data)
    (DEST / 'branch-main.json').write_bytes(data)
    head = branch['commit']['sha']
    receipt['observed_public_api_head'] = head
    receipt['current_public_api_head_verified'] = True
    receipt['operations'].append({'kind':'public-branch-read','status':'SUCCESS','url':url,
                                  'sha256':sha256(data).hexdigest()})
except Exception as exc:
    receipt['operations'].append({'kind':'public-branch-read','status':'FAILED','error':str(exc)})

archive = Path('private-locator:433359da52c2e48e6467')
try:
    if not archive.exists() or not zipfile.is_zipfile(archive):
        data = get('https://codeload.github.com/theislampill/orthemology/zip/' + PIN)
        archive.write_bytes(data)
    archive_bytes = archive.read_bytes()
    receipt['snapshot_archive_sha256'] = sha256(archive_bytes).hexdigest()
    tree = {}
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        prefixes = {PurePosixPath(i.filename).parts[0] for i in infos if PurePosixPath(i.filename).parts}
        if len(prefixes) != 1:
            raise ValueError('Snapshot has no unique enclosing root.')
        for info in infos:
            p = PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError('Unsafe snapshot member path.')
            if info.is_dir():
                continue
            rel_parts = p.parts[1:]
            if not rel_parts:
                raise ValueError('Unexpected root-level file.')
            data = z.read(info)
            permissions = (info.external_attr >> 16) & 0xffff
            if stat.S_ISLNK(permissions):
                mode = b'120000'
            elif permissions & stat.S_IXUSR:
                mode = b'100755'
            else:
                mode = b'100644'
            obj = sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).digest()
            node = tree
            for parent in rel_parts[:-1]:
                node = node.setdefault(parent, {})
            if rel_parts[-1] in node:
                raise ValueError('Duplicate snapshot member.')
            node[rel_parts[-1]] = (mode, obj)
            # Store symlink payload as ordinary bytes, not an executable filesystem link.
            out = DEST / 'tree' / Path(*rel_parts)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
    def tree_hash(node):
        entries = []
        for name, value in node.items():
            encoded = name.encode('utf-8')
            if isinstance(value, dict):
                entries.append((encoded + b'/', b'40000 ' + encoded + b'\0' + tree_hash(value)))
            else:
                mode, digest = value
                entries.append((encoded, mode + b' ' + encoded + b'\0' + digest))
        payload = b''.join(v for _, v in sorted(entries, key=lambda item: item[0]))
        return sha1(b'tree ' + str(len(payload)).encode() + b'\0' + payload).digest()
    actual_tree = tree_hash(tree).hex()
    receipt['computed_snapshot_tree'] = actual_tree
    receipt['snapshot_tree_verified'] = actual_tree == EXPECTED_TREE
    receipt['operations'].append({'kind':'public-snapshot-acquisition','status':'SUCCESS',
                                  'tree_matches_expected':actual_tree == EXPECTED_TREE})
except Exception as exc:
    receipt['operations'].append({'kind':'public-snapshot-acquisition','status':'FAILED','error':str(exc)})
receipt['full_source_reading_completed'] = False
(BASE / 'ledgers' / 'public_acquisition.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
