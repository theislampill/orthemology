#!/usr/bin/env python3
"""Standard-library verification of an exact finite parsed Markdown-link receipt.

The Markdown parser runs only during assembly. This consumes its hash-bound
receipt and checks actual owner-relative file targets; it does not fetch URLs or
claim to validate fragment anchors, raw HTML links, or other unparsed syntax.
"""
from collections import Counter
import importlib.util
import posixpath
from pathlib import Path
from urllib.parse import unquote,urlsplit

_spec=importlib.util.spec_from_file_location('archive_safety',Path(__file__).with_name('archive_safety.py'))
S=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(S)


def resolve_owner_target(source,href):
    S.safe_relative(source)
    S.require(isinstance(href,str)and '\\'not in href and not any(ord(c)<32 for c in href),'Unsafe Markdown target')
    parsed=urlsplit(href)
    if parsed.scheme or parsed.netloc:
        S.require(parsed.scheme.lower()in('http','https','mailto','tel','doi')or(not parsed.scheme and bool(parsed.netloc)),'Unsupported link scheme')
        return 'external',None
    path=unquote(parsed.path)
    S.require(not path.startswith('/')and '\\'not in path,'Absolute local Markdown target')
    target=source if not path else posixpath.normpath(posixpath.join(posixpath.dirname(source),path))
    S.safe_relative(target)
    return 'local',target


def check_link_receipt(receipt,bodies):
    S.require(receipt.get('schema')=='owner-parsed-link-receipt-v1','Unknown parsed-link receipt')
    sources=receipt['source_files'];names=[r['path']for r in sources]
    S.check_names(names);S.require(len(names)==len(set(names)),'Duplicate parsed source')
    for row in sources:
        S.require(row['path']in bodies,'Parsed source missing')
        data=bodies[row['path']]
        S.require(len(data)==row['bytes']and S.digest(data)==row['sha256'],'Parsed source identity changed')
    counts=Counter();local=external=0
    for row in receipt['links']:
        source=row['source'];S.require(source in names,'Link source is not declared')
        counts[source]+=1
        kind,target=resolve_owner_target(source,row['href'])
        S.require(kind==row['kind'],'Link kind differs from finite receipt')
        if kind=='external':
            S.require(row.get('target')is None,'External link has local target claim');external+=1;continue
        S.require(target==row['target'],'Target is not relative to the actual owner document')
        S.require(target in bodies,'Owner-relative file target does not exist: '+target)
        data=bodies[target]
        S.require(len(data)==row['target_bytes']and S.digest(data)==row['target_sha256'],'Owner-relative target bytes changed')
        local+=1
    for row in sources:S.require(counts[row['path']]==row['parsed_link_count'],'Finite parsed-link coverage count differs')
    return {'status':'PASS_FINITE_OWNER_RELATIVE_LINK_TARGETS','source_files_verified':len(sources),
            'local_targets_verified':local,'external_links_classified_not_fetched':external,
            'scope':receipt['scope'],'markdown_parser_required_at_verification':False}
