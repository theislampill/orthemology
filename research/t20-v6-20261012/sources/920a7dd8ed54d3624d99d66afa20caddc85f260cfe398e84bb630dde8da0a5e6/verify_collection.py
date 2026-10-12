#!/usr/bin/env python3
"""Read-only integrity check for Ninth Research Evidence (Python 3.10+).

No proof execution, downloads, dependency writes, or extraction occurs. The same
checks run under python -O. Use an externally supplied archive digest for custody.
"""
import argparse
import difflib
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
PATH_EXCEPTION_EXPECTED = {'dependencies/CACHE_METADATA_RELOCATION.json': ('d14ffdea106264773d5b708b765a078e1a8a3f529bd909c08dcc806c3d4c446b', 3038), 'dependencies/RESTORATION_RECEIPT.json': ('bdcbe537b888087fca905c541be85f19ced2a3916eaf159e08cc5c50ec67cc71', 4817), 'dependencies/trace_metadata/Hashing.trace': ('a04da4f6a920baa300c6d2d8fcb78ab4ec3ff7ed034bccddf15898f01a51932f', 798), 'dependencies/trace_metadata/IO.trace': ('2ad4ff6300f5e51d5e74692a47f6ae86d9cd2019c805e5a40e3722f191188388', 777), 'dependencies/trace_metadata/Lean.trace': ('7d145437ae028596c26e7b42fa55048c7b8ff275130d96762d85c20db9dbd865', 785), 'dependencies/trace_metadata/Main.trace': ('c08f59e8ef9bfe7110570699cc3b721806172fab2e8905867c004b9f2ceb884d', 786), 'dependencies/trace_metadata/Requests.trace': ('8f17aa4c51e3e1ace9d6cf3829d1e0f4b6d0f8bc312d466719db7af722313970', 802)}
PATH_PREFIX_DIGESTS = {'28e84d0cb5bd1a6a2a8d9ef0d620adc91cff0f7b21cdcad1af230ddf8c4c16d4', '505ef98a7064842aecd7eae0e0f19f06e413516fd047b0198e2bfd89bb7445e3'}
MAX_FILE = 100 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_ENTRIES = 20000
FORBIDDEN_SUFFIXES = {'.olean', '.ilean', '.pyc', '.pyo', '.so', '.dll', '.dylib', '.exe', '.o', '.a'}
FORBIDDEN_PARTS = {'__pycache__', '.git', '.aws', '.codex', '.agents', 'node_modules'}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(name):
    need(isinstance(name, str) and name, 'empty/non-string path')
    need('\\' not in name and ':' not in name, 'non-portable path: ' + name)
    need(not any(ord(c) < 32 or ord(c) == 127 for c in name), 'control character in path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and all(x not in ('', '.', '..') for x in name.split('/')), 'unsafe path: ' + name)
    need(str(p) == name, 'noncanonical path: ' + name)
    need(unicodedata.normalize('NFC', name) == name, 'non-NFC path')
    need(not (set(p.parts) & FORBIDDEN_PARTS), 'forbidden private/cache path: ' + name)
    need(p.suffix.lower() not in FORBIDDEN_SUFFIXES, 'compiled/binary member: ' + name)
    return name


def no_duplicates(pairs):
    d = {}
    for key, value in pairs:
        need(key not in d, 'duplicate JSON key: ' + key)
        d[key] = value
    return d


def parse(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=no_duplicates)


def zip_tree(data, label):
    need(len(data) <= MAX_TOTAL, 'archive too large: ' + label)
    result = {}
    total = 0
    names = set()
    folded = set()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        need(len(z.infolist()) <= MAX_ENTRIES, 'too many members: ' + label)
        for info in z.infolist():
            original_name = info.orig_filename
            safe_path(original_name[:-1] if original_name.endswith('/') else original_name)
            need(original_name == info.filename, 'original ZIP filename differs from logical name')
            name = info.filename[:-1] if info.is_dir() else info.filename
            safe_path(name)
            need(name not in names, 'duplicate ZIP member: ' + label + '::' + name)
            names.add(name)
            need(name.casefold() not in folded, 'case-colliding ZIP member: ' + name)
            folded.add(name.casefold())
            kind = stat.S_IFMT(info.external_attr >> 16)
            need(kind in (0, stat.S_IFREG, stat.S_IFDIR), 'non-regular ZIP member: ' + name)
            need(not info.flag_bits & 1, 'encrypted ZIP member: ' + name)
            need(info.file_size <= MAX_FILE, 'oversized ZIP member: ' + name)
            total += info.file_size
            need(total <= MAX_TOTAL, 'oversized expanded ZIP: ' + label)
            if info.is_dir():
                need(info.file_size == 0, 'nonempty directory member')
                continue
            need(kind != stat.S_IFDIR, 'file marked directory: ' + name)
            body = z.read(info)  # zipfile checks each complete member CRC.
            need(len(body) == info.file_size, 'ZIP size mismatch: ' + name)
            result[name] = body
    for name in result:
        need(not any(str(p) in result for p in PurePosixPath(name).parents if str(p) != '.'), 'file/directory collision: ' + name)
    return result


def local_tree(root):
    need(root.is_dir() and not root.is_symlink(), 'not a regular directory')
    result = {}
    total = 0
    folded = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(directory) / name
            rel = p.relative_to(root).as_posix()
            safe_path(rel)
            need(not p.is_symlink(), 'symlink in packet: ' + rel)
            need(rel.casefold() not in folded, 'case-colliding path: ' + rel)
            folded.add(rel.casefold())
        for name in files:
            p = Path(directory) / name
            need(p.is_file(), 'nonregular file')
            need(p.stat().st_size <= MAX_FILE, 'oversized file')
            b = p.read_bytes()
            total += len(b)
            need(total <= MAX_TOTAL, 'oversized packet')
            result[p.relative_to(root).as_posix()] = b
    need(len(result) <= MAX_ENTRIES, 'too many packet files')
    return result


def rows(manifest, key):
    rs = manifest[key]
    if isinstance(rs, dict):
        rs = [dict(v, path=k) for k, v in rs.items()]
    need(isinstance(rs, list), 'manifest entries are not a list/dict')
    return rs


def check_rows(tree, records, base='', exact=False, exclusions=(), path_key='path'):
    seen = set()
    for row in records:
        name = safe_path(row[path_key])
        need(name not in seen, 'duplicate manifest path: ' + name)
        seen.add(name)
        full = (base + '/' if base else '') + name
        need(full in tree, 'missing manifest member: ' + full)
        body = tree[full]
        length = row.get('bytes', row.get('size'))
        need(isinstance(length, int) and not isinstance(length, bool), 'invalid byte count: ' + full)
        need(len(body) == length, 'manifest size mismatch: ' + full)
        need(re.fullmatch('[0-9a-f]{64}', row['sha256']) is not None, 'invalid SHA256')
        need(sha(body) == row['sha256'], 'manifest digest mismatch: ' + full)
        if 'git_blob_sha1' in row:
            need(hashlib.sha1(b'blob '+str(len(body)).encode('ascii')+b'\0'+body).hexdigest()==row['git_blob_sha1'], 'Git blob identity mismatch: '+full)
    if exact:
        actual = {name[len(base) + 1:] if base else name for name in tree if not base or name.startswith(base + '/')}
        need(actual == seen | set(exclusions), 'manifest file census mismatch: ' + repr(sorted(actual ^ (seen | set(exclusions)))[:20]))
    return len(seen)


def check(tree, staging=False, sealed_candidate=False):
    need(staging != sealed_candidate, 'final integrity mode gate requires exactly one explicit staging or sealed-candidate mode')
    manifest_name = "STAGING_MANIFEST.json" if staging else "MANIFEST.json"
    digest_name = "STAGING_MANIFEST.sha256" if staging else "MANIFEST.sha256"
    expected_status = "STAGING_NOT_FINAL" if staging else "SEALED_CANDIDATE_AWAITING_DETACHED_REVIEW"
    for name in (manifest_name, digest_name, 'COMPONENT_INDEX.json', 'EVIDENCE_LINKS.json'):
        need(name in tree, 'missing top-level file: ' + name)
    manifest_hash = sha(tree[manifest_name])
    need(tree[digest_name].decode('ascii') == manifest_hash + '  ' + manifest_name + '\n', 'manifest SHA file mismatch')
    manifest = parse(tree[manifest_name])
    need(manifest['status'] == expected_status, 'wrong checkpoint status')
    outer_count = check_rows(tree, rows(manifest, 'files'), exact=True, exclusions=(manifest_name, digest_name))
    index = parse(tree['COMPONENT_INDEX.json'])
    need(index['status'] == expected_status and index['canonical_adoption'] is False, 'scope/status mismatch')
    need(index['predecessor']['outer_archive_sha256'] == 'd4110581c437db9a50e238154883a4c857163f1fa257f54335b295ee39b225bb', 'predecessor identity mismatch')
    if not staging:
        need(all(k in index for k in ('g1','report_binding','report_evidence_keys','specialist_preparation','late_additions')), 'required final binding section missing')
        need(index.get('pending_slots') == ['independent_outer_review'] and 'NOT_FINALIZED.txt' not in tree, 'final candidate research/report gates remain pending')
        gates = index.get('finalization_gates', {})
        need(all(gates.get(k) is True for k in ('release_authorized', 'report_verified', 'g1_terminal')), 'final candidate authorization/research gates incomplete')
        need(index.get('outer_acceptance') == {'state':'DETACHED_RECEIPT_REQUIRED','receipt_inside_archive':False}, 'sealed candidate must keep outer acceptance explicitly detached')
        account_state=index.get('reorientation_accounting',{})
        need(account_state.get('report_status')=='FINAL_VERIFIED_REPORT_BOUND' and account_state.get('report_words_not_yet_credited') is False, 'final report binding/accounting remains pending')
    archives = {}
    deep_archives = 0
    deep_members = 0
    def inspect_archive(data, label, depth=0):
        nonlocal deep_archives, deep_members
        need(depth < 8, 'excessive archive nesting')
        t = zip_tree(data, label)
        deep_archives += 1
        deep_members += len(t)
        for name, b in t.items():
            if name.lower().endswith('.zip'):
                inspect_archive(b, label + '::' + name, depth + 1)
        return t
    for row in index['components']:
        path = safe_path(row['path'])
        if path.startswith('unreviewed/'):
            need(row.get('scope_class') == 'paused_unreviewed' and row.get('status') == 'PAUSED_UNREVIEWED_SOURCE_CUSTODY_ONLY', 'unreviewed component promoted to accepted scope')
        else:
            need(row.get('scope_class') != 'paused_unreviewed', 'unreviewed component outside segregated namespace')
        if path.startswith('supplements/'):
            need(row.get('scope_class')=='internal_review_supplement' and row.get('status')=='SCOPED_INTERNAL_PHILOSOPHICAL_REVIEW_CUSTODY', 'supplement component promoted beyond internal review scope')
        if path.startswith('preparations/'):
            need(row.get('scope_class')=='preparation_only' and row.get('status')=='PREPARATION_ONLY_NOT_SENT_OR_EXTERNALLY_REVIEWED', 'specialist preparation promoted to validated scope')
        need(path not in archives and path in tree, 'missing/repeated component')
        need(sha(tree[path]) == row['sha256'] and len(tree[path]) == row['bytes'], 'component identity mismatch: ' + path)
        archives[path] = inspect_archive(tree[path], path)
        need(all(n.startswith(row['root_prefix']) for n in archives[path]), 'component root mismatch: '+path)
    need(set(archives) == {p for p in tree if p.lower().endswith('.zip')}, 'unindexed top-level archive')
    checked_manifests = 0
    checked_entries = 0
    for rule in index['manifest_checks']:
        t = archives[rule['archive']]
        name = safe_path(rule['member'])
        need(name in t and sha(t[name]) == rule['sha256'], 'nested manifest identity mismatch: ' + name)
        d = parse(t[name])
        for key in rule.get('record_keys', ['files']):
            checked_entries += check_rows(t, rows(d, key), rule.get('base', ''), rule.get('exact', False), rule.get('exclusions', []), rule.get('path_key','path'))
        checked_manifests += 1
    def resolve(locator):
        if '::' in locator:
            arc, member = locator.split('::', 1)
            safe_path(member)
            need(arc in archives and member in archives[arc], 'unresolved locator: ' + locator)
            return archives[arc][member]
        safe_path(locator)
        need(locator in tree, 'unresolved locator: ' + locator)
        return tree[locator]
    def pointer(value, expression, context):
        need(isinstance(expression,str) and (expression == '' or expression.startswith('/')), context + ' invalid JSON pointer')
        try:
            for part in expression.split('/')[1:]:
                part=part.replace('~1','/').replace('~0','~')
                value=value[int(part)] if isinstance(value,list) else value[part]
            return value
        except (KeyError,IndexError,TypeError,ValueError):
            raise ValueError(context + ' unresolved JSON pointer: '+expression)
    sidecar_records=0
    for arc,t in archives.items():
        for name,body in t.items():
            if not name.endswith('.sha256'):continue
            seen=set()
            for line in body.decode('ascii').splitlines():
                match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
                need(match is not None,'invalid digest sidecar line')
                relative=safe_path(match.group(2));target=str(PurePosixPath(name).parent/relative)
                need(target not in seen and target in t,'digest sidecar unresolved/repeated target')
                seen.add(target)
                need(sha(t[target])==match.group(1),'digest sidecar mismatch: '+arc+'::'+name)
                sidecar_records+=1
    replay=parse(tree['REPLAY_MAP.json'])
    replay_seen=set()
    replay_targets=0
    for entry in replay['entries']:
        need(entry['id'] not in replay_seen,'repeated replay key');replay_seen.add(entry['id'])
        if entry.get('archive'):
            need(entry['archive'] in archives,'unresolved replay archive locator')
            for field in ('instructions','entry'):
                if entry.get(field):
                    name=(entry.get('root','')+'/' if entry.get('root') else '')+safe_path(entry[field])
                    need(name in archives[entry['archive']],'unresolved replay entry locator')
                    replay_targets+=1
        elif not staging:
            need(entry.get('status') not in ('IMPLEMENTATION_AND_INDEPENDENT_REVIEW_PENDING',),'final replay gate pending')
    for entry in replay['entries']:
        need(set(entry.get('dependencies',[])) <= replay_seen,'unknown replay dependency key')
    binding_records=parse(tree['CODE_SOURCE_BINDINGS.json'])['bindings']
    seen_bindings=set()
    for binding in binding_records:
        key=(binding['record'],binding['json_pointer'])
        need(key not in seen_bindings, 'repeated source binding')
        seen_bindings.add(key)
        value=pointer(parse(resolve(binding['record'])),binding['json_pointer'],'source binding')
        need(value == binding['sha256'] == sha(resolve(binding['target'])), 'source binding digest mismatch')
    expected_bindings=set()
    source_fields={'sha256','source_sha256','snapshot_sha256','source_snapshot_sha256','current_source_sha256','last_checked_source_sha256','source_after_sha256'}
    def source_field_census(data, pointer, record, source_hashes):
        if isinstance(data,dict):
            for k,value in data.items():
                child=pointer+'/'+str(k).replace('~','~0').replace('/','~1')
                if isinstance(value,str) and k in source_fields and value in source_hashes:
                    expected_bindings.add((record,child))
                source_field_census(value,child,record,source_hashes)
        elif isinstance(data,list):
            for i,value in enumerate(data):source_field_census(value,pointer+'/'+str(i),record,source_hashes)
    for arc,t in archives.items():
        source_hashes={sha(b) for n,b in t.items() if n.endswith(('.lean','.py'))}
        for n,b in t.items():
            if n.endswith('.json') and not any(x in n for x in ['MANIFEST','PROJECTION_MAP','ORIGINAL_TO_PUBLIC','original_manifests']):
                source_field_census(parse(b),'',arc+'::'+n,source_hashes)
    native=next((r for r in index['components'] if 'Ninth_Controller_' in r['path']),None)
    native_receipt='receipts/native-controller/Ninth_Controller_Independent_Review_v1_Replay.json'
    if native and native_receipt in tree:
        for i,result in enumerate(parse(tree[native_receipt])['results']):
            if native['root_prefix']+result['source'] in archives[native['path']]:expected_bindings.add((native_receipt,'/results/'+str(i)+'/source_sha256'))
    need(expected_bindings==seen_bindings,'source binding census mismatch')
    links = parse(tree['EVIDENCE_LINKS.json'])
    for link in links['links']:
        body = resolve(link['target'])
        need(sha(body) == link['sha256'], 'evidence link mismatch: ' + link['target'])
        if 'bytes' in link:
            need(len(body) == link['bytes'], 'evidence link byte mismatch')
        if 'source' in link:
            source=resolve(link['source'])
            if 'source_sha256_pointer' in link:
                need(pointer(parse(source),link['source_sha256_pointer'],'evidence source')==link['sha256'],'evidence source digest mismatch')
    g1_bridge_checked=False
    if 'g1' in index:
        g1=index['g1']; acceptance=parse(resolve(g1['acceptance_receipt']))
        need(g1['status']=='INDEPENDENT_SCOPED_PASS' and acceptance['full_endpoint_verified'] is True,'G1 final disposition mismatch')
        need(acceptance['status']=='PASS_BOUNDED_TYPED_AST_EXISTENCE_CHECKER_AND_CHECKED_COMPOSITION','G1 acceptance scope mismatch')
        packet=acceptance['author_packet']; author_bytes=resolve(g1['author_archive'])
        need(packet['version']=='v4' and sha(author_bytes)==packet['zip_sha256'] and len(author_bytes)==packet['zip_bytes'],'G1 exact accepted author archive mismatch')
        bridge_bytes=resolve(g1['reviewer_bridge']);bridge=parse(bridge_bytes)
        need(sha(bridge_bytes)==acceptance['execution']['v4_bridge_sha256'],'G1 reviewer bridge identity mismatch')
        delta=parse(resolve(g1['author_delta']));script=resolve(g1['replay_script'])
        need(sha(script)==delta['v4_replay_sha256']==bridge['v4_replay_py_sha256'],'G1 v4 replay source binding mismatch')
        old=delta['only_replay_text_replacement']['from'].encode('utf-8');new=delta['only_replay_text_replacement']['to'].encode('utf-8')
        need(script.count(new)==1 and old not in script,'G1 replay metadata replacement is not unique')
        previous=script.replace(new,old)
        need(sha(previous)==delta['v2_replay_sha256']==bridge['v2_replay_py_sha256'],'G1 reverse metadata bridge does not reproduce v2')
        actual_diff=''.join(difflib.unified_diff(previous.decode('utf-8').splitlines(keepends=True),script.decode('utf-8').splitlines(keepends=True),fromfile='v2/replay.py',tofile='v4/replay.py')).encode('utf-8')
        need(actual_diff==resolve(g1['replay_diff']) and sha(actual_diff)==delta['diff_sha256'],'G1 exact replay diff mismatch')
        need(delta['source_manifest_sha256']==bridge['shared_source_manifest_sha256']==packet['source_manifest_sha256'],'G1 shared scientific-source manifest mismatch')
        need(delta['v4_public_manifest_sha256']==bridge['v4_public_manifest_sha256']==packet['public_manifest_sha256'],'G1 v4 public manifest binding mismatch')
        need(delta['v4_zip_sha256']==bridge['v4_zip_sha256']==packet['zip_sha256'],'G1 v4 archive bridge mismatch')
        need(acceptance['execution']['portable_full_replay_version']=='v2' and acceptance['execution']['portable_commands']==120,'G1 execution version/count mismatch')
        need(bridge['scientific_and_control_source_bytes_unchanged'] is True and bridge['replay_command_control_order_and_budget_unchanged'] is True,'G1 command-preservation claims not established')
        g1_bridge_checked=True
    specialist_links_checked=0
    if 'specialist_preparation' in index:
        sp=index['specialist_preparation']
        need(sp['status']=='PREPARATION_ONLY_NOT_SENT_OR_EXTERNALLY_REVIEWED' and sp['external_validation_credit'] is False and sp['proposed_occurrence_study_run'] is False,'specialist preparation status or credit mismatch')
        bindings=parse(resolve(sp['bindings']));original_bindings=parse(resolve(sp['original_bindings']));rebase=parse(resolve(sp['link_rebase']));dossier=resolve(sp['dossier']);locators=resolve(sp['source_locators']).decode('utf-8')
        need(bindings['status']==sp['status'] and bindings['human_or_external_validation_credit'] is False and bindings['proposed_occurrence_study_run'] is False,'specialist preparation binding status mismatch')
        need(bindings['primary_source_exposition_delta_words']==bindings['direct_primary_quotation_delta_words']==0,'specialist preparation added source exposition')
        need(sha(dossier)==bindings['dossier_sha256']==rebase['public_dossier_sha256'] and len(dossier)==rebase['public_dossier_bytes'],'specialist dossier public identity mismatch')
        old_links=[r for r in original_bindings['source_links'] if 'href' in r]
        need(len(old_links)==len(bindings['links'])==len(rebase['replacements']),'specialist link census mismatch')
        text=dossier.decode('utf-8');seen=set()
        for original,link,replacement in zip(old_links,bindings['links'],rebase['replacements']):
            need(link['id'] not in seen and re.fullmatch('s[0-9]{2}',link['id']) is not None,'specialist source locator id mismatch');seen.add(link['id'])
            need(link['original_href']==original['href']==replacement['from'] and link['dossier_href']==replacement['to']=='SOURCE_LOCATORS.md#'+link['id'],'specialist href binding mismatch')
            need(link['label']==original['label'] and link['sha256']==original['sha256'] and link['bytes']==original['bytes'],'specialist original-source identity mismatch')
            body=resolve(link['locator']);need(sha(body)==link['sha256'] and len(body)==link['bytes'],'specialist exact source locator mismatch')
            token=']('+replacement['to']+')';need(text.count(token)==1 and replacement['replacement_count']==1,'specialist rebased link not unique')
            text=text.replace(token,']('+replacement['from']+')',1)
            need(locators.count('## '+link['id']+'\n')==1 and link['sha256'] in locators,'specialist human locator missing')
            specialist_links_checked+=1
        original_text=text.encode('utf-8')
        need(sha(original_text)==rebase['original_dossier_sha256']==original_bindings['dossier']['sha256'] and len(original_text)==rebase['original_dossier_bytes']==original_bindings['dossier']['bytes'],'specialist reversible link-only reconstruction mismatch')
        need(rebase['scientific_prose_changed'] is False and rebase['reverse_reconstruction_exact'] is True,'specialist preparation projection claim mismatch')
    late_supplement_links_checked=0
    late_routing_budgets_checked=0
    if 'late_additions' in index:
        late=index['late_additions'];supp=late['supplement'];route=late['routing']
        need(late['base_candidate_sha256']=='00bc7491150c5ea7cbd6b7f78360275a7df286ff2b250f2487889cb602bba4ac','late additions base candidate mismatch')
        receipt_bytes=resolve(supp['acceptance']);receipt=parse(receipt_bytes)
        need(sha(receipt_bytes)=='2196523ee1081c5548747253ab69470ef4c8ca5fe969c6aaf370106804c8d9f3','supplement scoped acceptance identity mismatch')
        need(receipt['schema']=='ninth-supplementary-projection-acceptance-v1' and receipt['decision']=='PASS_SCOPED_PUBLIC_PROJECTION_AND_SOURCE_CUSTODY','supplement acceptance scope mismatch')
        candidate=receipt['candidate'];body=resolve(supp['archive']);manbody=resolve(supp['manifest']);sm=parse(manbody)
        need(candidate['archive_name']==PurePosixPath(supp['archive']).name and candidate['archive_sha256']==sha(body) and candidate['archive_bytes']==len(body) and candidate['manifest_sha256']==sha(manbody),'supplement accepted archive mismatch')
        need(receipt['checks'] and all(v is True for v in receipt['checks'].values()),'supplement acceptance checks incomplete')
        supporting_bytes=resolve(supp['supporting_check']);support=parse(supporting_bytes)
        need(sha(supporting_bytes)==receipt['supporting_check_sha256'] and support['status']==receipt['decision'],'supplement supporting check mismatch')
        need(support['archive_sha256']==sha(body) and support['archive_bytes']==len(body) and support['manifest_sha256']==sha(manbody),'supplement supporting archive binding mismatch')
        need(all(v is True for v in support['checks'].values()) and all(v is True for v in support['manual_content_review'].values()),'supplement supporting checks incomplete')
        claims=sm['claims']
        need(all(claims[k] is False for k in ('external_expert_validation','new_foundational_theorem','new_programme_closure','frozen_report_or_articles_changed','source_budget_reset')),'supplement claim ceiling promoted')
        need(claims['historical_exposition_added_words']==claims['primary_quotation_added_words']==0,'supplement source exposition changed')
        pre=supp['archive']+'::'+supp['root_prefix']
        wb=parse(resolve(pre+'warrant-standard/SOURCE_BINDINGS.json'));cb=parse(resolve(pre+'collective-efficacy/COLLECTIVE_SOURCE_BINDINGS.json'))
        need(wb['collection_reference']['sha256']==late['base_candidate_sha256'],'supplement base source binding mismatch')
        included=[wb['report']['reader']]+[r for key in wb['public_evidence_keys'].values() for r in key['identities']]+cb['public_dossier_keys']
        need(len(included)==24,'supplement included source census mismatch')
        for r in included:
            b=resolve(r['locator']);need(sha(b)==r['sha256'] and len(b)==r['bytes'],'supplement public source locator identity mismatch')
            if 'component_archive' in r:
                a=r['component_archive'];ab=resolve(r['locator'].split('::',1)[0]);need(sha(ab)==a['sha256'] and len(ab)==a['bytes'],'supplement source archive identity mismatch')
            late_supplement_links_checked+=1
        need(len(cb['historical_identity_only_sources'])==13 and all('identity_only' in r['availability'] and 'locator' not in r for r in cb['historical_identity_only_sources']),'supplement historical availability promotion')
        need(all('identity_only' in r['availability'] for r in wb['original_contextual_sources']),'supplement original context availability promotion')
        for source_account in (wb['historical_source_use'],cb['source_accounting']):
            need(source_account['new_historical_exposition_words']==source_account['new_primary_quotation_words']==0,'supplement source allocation changed')
        need(wb['historical_source_use']['new_primary_translation_words']==0 and wb['historical_source_use']['cumulative_allocations_reset'] is False,'supplement translation or budget reset')
        wp=parse(resolve(pre+'warrant-standard/PROJECTION_MAP.json'));wbody=resolve(pre+'warrant-standard/'+safe_path(wp['public']['path']))
        need(sha(wbody)==wp['public']['sha256'],'supplement warrant public identity mismatch')
        need(wp['original']['sha256']==wb['original_assessment']['sha256'] and 'identity_only' in wp['original']['availability'],'supplement original warrant binding mismatch')
        need(wp['historical_exposition_delta_words']==wp['primary_quotation_delta_words']==0,'supplement warrant source delta mismatch')
        lines=wbody.splitlines(keepends=True);exact_ranges=0
        for r in wp['changes']:
            if r['disposition']=='exact_scientific_text':
                lo,hi=map(int,r['public_lines'].split('-'));need(1<=lo<=hi<=len(lines) and r['normalized_range'] is False,'supplement scientific line range invalid')
                need(sha(b''.join(lines[lo-1:hi]))==r['sha256_of_range_including_line_endings'],'supplement scientific range mismatch');exact_ranges+=1
        need(exact_ranges==2,'supplement exact scientific range census mismatch')
        cp=parse(resolve(pre+'collective-efficacy/COLLECTIVE_PROJECTION_MAP.json'))
        need(len(cp['originals'])==len(cp['public_projections'])==2 and all('identity_only' in r['availability'] for r in cp['originals']),'collective original projection census mismatch')
        for r in cp['public_projections']:
            b=resolve(pre+'collective-efficacy/'+safe_path(r['path']));need(sha(b)==r['sha256'] and len(b)==r['bytes'],'collective public projection identity mismatch')
        rb=resolve(route['acceptance']);review=parse(rb)
        need(sha(rb)=='127a4222755f5390f1f40b72fd236b269629ace4cb76e21315d2fbee1bb75b82','routing scoped acceptance identity mismatch')
        need(review['schema']=='specialist-routing-independent-acceptance-v1' and review['disposition']=='ACCEPTED_PREPARATION_ONLY','routing accepted scope mismatch')
        need(all(review[k] is False for k in ('human_specialist_validation','external_validation_credit','candidate_selected','candidate_contacted','availability_or_endorsement_established','lean_audit_expertise_established')),'routing validation/contact scope promoted')
        need(review['checks'] and all(v is True for v in review['checks'].values()) and review['outstanding_corrections']==[],'routing review incomplete')
        rbody=resolve(route['archive']);accepted=review['accepted_archive']
        need(accepted['name']==PurePosixPath(route['archive']).name and accepted['sha256']==sha(rbody) and accepted['bytes']==len(rbody),'routing accepted archive mismatch')
        check_rows(archives[route['archive']],review['accepted_members'],base=route['root_prefix'].rstrip('/'),exact=True,path_key='name')
        account=parse(resolve(route['accounting']));doc=resolve(route['document']);text=doc.decode('utf-8')
        need(sha(doc)==account['document_sha256'],'routing source-accounting document mismatch')
        need(account['no_primary_philosophical_argument_reconstruction_added'] is True,'routing added primary argument reconstruction')
        expected_keys={'OPPY_PROFILE','OPPY2000','HOOVER_PROFILE','HOOVER2004','RASKIN_PROFILE','RASKIN2026','CHATTERJEE_PROFILE','CHATTERJEE2022'}
        need(len(account['entries'])==8 and {r['work_key'] for r in account['entries']}==expected_keys,'routing source budget census mismatch')
        maximum=0
        for r in account['entries']:
            words=0
            for span in r['public_spans']:
                lo,hi=span['start_char'],span['end_char']
                need(span['document']=='REVIEW_ROUTING_ADDENDUM.md' and isinstance(lo,int) and isinstance(hi,int) and not isinstance(lo,bool) and not isinstance(hi,bool) and 0<=lo<=hi<=len(text),'routing span range invalid')
                part=text[lo:hi];need(sha(part.encode('utf-8'))==span['sha256_utf8'] and len(part.split())==span['words'],'routing actual source span mismatch');words+=len(part.split())
            budget_fields=('public_conservative_words','prior_retained_exposition_words','earlier_preparation_allowance_words','preparatory_summary_words')
            need(all(isinstance(r[k],int) and not isinstance(r[k],bool) and r[k]>=0 for k in budget_fields),'routing source budget value invalid')
            ceiling=sum(r[k] for k in budget_fields)
            need(words==r['public_conservative_words'] and ceiling==r['conservative_cumulative_ceiling']<=r['limit']==200 and r['remaining_after_ceiling']==200-ceiling and r['direct_quote_words']==0,'routing cumulative source budget mismatch')
            maximum=max(maximum,ceiling);late_routing_budgets_checked+=1
        preserved={r['work_key']:r for r in account['metadata_only_and_preserved_sources']}
        need(len(preserved)==len(account['metadata_only_and_preserved_sources']) and all(r['new_substantive_exposition_words']==0 for r in preserved.values()),'routing preserved source allocation changed')
        need(preserved['PRUSS_RPSR2004']['prior_cumulative_words']==188 and preserved['CHATTERJEE_ETAL2025']['prior_retained_conservative_words']==preserved['CHATTERJEE_ETAL2025']['conservative_cumulative_words']==98,'routing retained source totals mismatch')
        budget=review['source_budget']
        need(maximum==budget['maximum_conservative_cumulative_ceiling']==194 and budget['per_work_cap']==200 and budget['retained_2025_words']==98 and budget['pruss_cumulative_words']==188,'routing reviewed budget mismatch')
        need(all(budget[k]==0 for k in ('retained_2025_new_substantive_words','pruss_new_substantive_words','review_new_source_synopsis_words','review_primary_quotation_words')),'routing review added source exposition')
    projection_count = 0
    projection_manifest_locators=set()
    if 'PROJECTION_BINDINGS.json' in tree:
        projection_records = parse(tree['PROJECTION_BINDINGS.json'])
        for projection in projection_records['projections']:
            projection_manifest_locators.add(projection['original_manifest'])
            source_map_entries=pointer(parse(resolve(projection['source_map'])),projection['source_entries_pointer'],'source map')
            need(isinstance(source_map_entries,list), 'source map entries are not a list')
            source_map_by_path={e['original_path']:e for e in source_map_entries}
            need(len(source_map_by_path)==len(source_map_entries), 'source map contains repeated entry')
            need(len(source_map_entries)==len(projection['entries']), 'source map entry count mismatch')
            original_bytes = resolve(projection['original_manifest'])
            need(sha(original_bytes) == projection['original_manifest_sha256'], 'original manifest binding mismatch')
            original = parse(original_bytes)
            original_rows = rows(original, projection.get('record_key', 'files'))
            if projection.get('manifest_self_entry'):
                original_rows = original_rows + [{projection.get('path_key','path'): projection['manifest_self_entry'], 'sha256': sha(original_bytes), 'bytes': len(original_bytes)}]
            by_path = {r[projection.get('path_key', 'path')]: r for r in original_rows}
            need(len(by_path) == len(original_rows), 'duplicate original source entry')
            mapped = set()
            for entry in projection['entries']:
                path = entry['original_path']
                need(path in by_path and path not in mapped, 'projection is incomplete or repeated')
                mapped.add(path)
                row = by_path[path]
                need(path in source_map_by_path,'source map omits projected original')
                original_mapping=source_map_by_path[path]
                raw_disposition=original_mapping['disposition']
                normalized_disposition=('exact' if raw_disposition in ('exact','exact_included','preserved','PRESERVED_EXACT') else ('omitted' if raw_disposition in ('omitted','OMITTED') else 'projected'))
                need(entry['disposition']==normalized_disposition,'source map disposition mismatch')
                need(original_mapping['original_sha256']==entry['original_sha256'] and original_mapping['original_bytes']==entry['original_bytes'],'source map original identity mismatch')
                if entry['disposition']!='omitted':
                    relative_target=original_mapping.get('public_path',original_mapping.get('target'))
                    need(entry['target']==projection['public_base']+relative_target,'source map public locator mismatch')
                    need(entry['public_sha256']==original_mapping.get('public_sha256',entry['original_sha256']),'source map public identity mismatch')
                else:
                    need(entry['reason']==original_mapping['reason'],'source map omission reason mismatch')
                need(entry['original_sha256'] == row['sha256'] and entry['original_bytes'] == row.get('bytes', row.get('size')), 'projection origin mismatch')
                need(entry['disposition'] in ('exact', 'projected', 'omitted'), 'invalid projection disposition')
                if entry['disposition'] == 'omitted':
                    need(bool(entry.get('reason')) and not entry.get('target'), 'unexplained omitted entry')
                else:
                    body = resolve(entry['target'])
                    need(sha(body) == entry['public_sha256'], 'projected byte binding mismatch')
                    if entry['disposition'] == 'exact':
                        need(sha(body) == entry['original_sha256'] and len(body) == entry['original_bytes'], 'exact source preservation mismatch')
            need(mapped == set(by_path), 'unmapped original entries')
            projection_count += 1
    manifest_inventory=index['manifest_inventory']
    actual_manifest_locators={arc+'::'+name for arc,t in archives.items() for name in t if name.endswith('.json') and ('MANIFEST' in PurePosixPath(name).name.upper() or '/original_manifests/' in name)}
    inventory_locators={r['locator'] for r in manifest_inventory}
    need(len(inventory_locators)==len(manifest_inventory) and inventory_locators==actual_manifest_locators,'manifest inventory census mismatch')
    directly_checked={r['archive']+'::'+r['member'] for r in index['manifest_checks']}
    for r in manifest_inventory:
        need(sha(resolve(r['locator']))==r['sha256'],'manifest inventory identity mismatch')
        expected='checked_rows' if r['locator'] in directly_checked else ('projection_binding' if r['locator'] in projection_manifest_locators else 'UNCLASSIFIED')
        need(expected!='UNCLASSIFIED' and r['mode']==expected,'manifest inventory contains unchecked manifest')
    exceptions=parse(tree['PUBLIC_PATH_EXCEPTION.json'])
    supplied={r['path']:(r['sha256'],r['bytes']) for r in exceptions['files']}
    need(len(supplied)==len(exceptions['files']) and supplied==PATH_EXCEPTION_EXPECTED,'path exception allowlist mismatch')
    need(set(exceptions['prefix_sha256'])==PATH_PREFIX_DIGESTS,'path exception prefix identity mismatch')
    for n,(digest,length) in PATH_EXCEPTION_EXPECTED.items():
        need(n in tree and sha(tree[n])==digest and len(tree[n])==length,'path exception byte identity mismatch')
    path_pattern=re.compile(rb'(?<![\w/])/(?:workspace|root|home|Users)/[^\s"\'<>]*')
    restoration=parse(tree['dependencies/CACHE_METADATA_RELOCATION.json'])
    authorized_prefixes=[restoration[k].encode() for k in ('current_prefix','historical_prefix')]
    need({sha(p) for p in authorized_prefixes}==PATH_PREFIX_DIGESTS,'path exception actual prefix mismatch')
    for n,b in tree.items():
        if n.lower().endswith('.zip'):continue
        paths=path_pattern.findall(b)
        if paths:
            need(n in PATH_EXCEPTION_EXPECTED,'unlisted host path in '+n)
            need(all(any(path.startswith(prefix) for prefix in authorized_prefixes) for path in paths),'unrelated host path in exception record')
    for arc,t in archives.items():
        for n,b in t.items():need(not path_pattern.search(b),'host path in component '+arc+'::'+n)
    relocation = parse(tree['dependencies/CACHE_METADATA_RELOCATION.json'])
    need(len(relocation['files']) == 5, 'wrong trace relocation count')
    need(sha(tree['dependencies/MATHLIB_CACHE_PIN.json']) == relocation['original_cache_manifest_sha256'], 'cache manifest/relocation binding mismatch')
    expected_trace_names = {'Hashing', 'IO', 'Lean', 'Main', 'Requests'}
    need({PurePosixPath(r['path']).stem for r in relocation['files']} == expected_trace_names, 'unexpected trace relocation member')
    for record in relocation['files']:
        trace = tree['dependencies/trace_metadata/' + PurePosixPath(record['path']).name]
        need(sha(trace) == record['current_sha256'] and len(trace) == record['current_bytes'], 'trace metadata mismatch')
        current = relocation['current_prefix'].encode()
        historical = relocation['historical_prefix'].encode()
        need(trace.count(current) == record['replacement_count'] == 1, 'unexpected relocation replacement count')
        normalized = trace.replace(current, historical)
        need(sha(normalized) == record['original_pin_sha256'] == record['normalized_sha256'], 'trace normalization mismatch')
        need(len(normalized) == record['original_pin_bytes'] == record['normalized_bytes'], 'trace normalization byte mismatch')
    # Each exact source-accounting span is checked without quoting it elsewhere.
    foundation = index['source_accounting']
    account = parse(resolve(foundation['necessity_accounting']))
    for work in account['works']:
        words = 0
        quotes = 0
        for span in work['spans']:
            body = resolve(foundation['necessity_archive'] + '::' + foundation.get('necessity_base', '') + span['document']).decode('utf-8')
            text = body[span['start_char']:span['end_char']]
            need(sha(text.encode('utf-8')) == span['sha256_utf8'] and len(text.split()) == span['words'], 'source-accounting span mismatch')
            words += span['words']
            if span['direct_quotation']:
                quotes += span['words']
        need(words == work['derived_words'] and words <= 200, 'derived-word budget mismatch')
        need(quotes == work['direct_quotation_words'] and quotes <= 25, 'quotation budget mismatch')
    ledger = parse(resolve(foundation['integrity_accounting']))
    integrity_prefix = foundation['integrity_archive'] + '::' + foundation.get('integrity_base', '')
    integrity_main = resolve(integrity_prefix + 'SOURCE_INTEGRITY_WARRANT.md').decode('utf-8')
    paragraphs = integrity_main.split('## Primary-text control\n')[1].split('\n## ')[0].strip().split('\n\n')
    source_map = parse(resolve(integrity_prefix + 'SOURCE_MAP.json'))
    increments = parse(resolve(integrity_prefix + 'INCREMENT_LEDGER.json'))
    actual_integrity_counts = {
        'S1': sum(len(t.split()) for t in [paragraphs[0], source_map['source_to_claim_map'][0]['claim'], source_map['source_to_claim_map'][1]['claim'], increments['increments'][0]['result']]),
        'S2': sum(len(t.split()) for t in [paragraphs[1], source_map['source_to_claim_map'][2]['claim']])}
    for item in ledger['sources']:
        need(sum(x['words'] for x in item['components']) == item['source_derived_word_count'] == actual_integrity_counts[item['source_id']], 'integrity account total mismatch')
        if isinstance(item['budget'], int):
            need(item['source_derived_word_count'] <= item['budget'], 'integrity derived-word budget exceeded')
        need(item['direct_quotation_words'] <= 25, 'integrity quote budget exceeded')
    reorientation=index['reorientation_accounting']
    nexus=parse(resolve(reorientation['nexus_accounting']))
    companion=parse(resolve(reorientation['companion_accounting']))
    nexus_words=0
    nexus_quotes=0
    for span in nexus['spans']:
        document=resolve(reorientation['nexus_base']+span['document'])
        chunk=document.decode('utf-8')[span['start_char']:span['end_char']].encode('utf-8')
        need(chunk==document[span['start_byte']:span['end_byte']] and sha(chunk)==span['sha256_utf8'],'nexus source-accounting span mismatch')
        need(len(chunk.decode('utf-8').split())==span['derived_words'],'nexus source-accounting count mismatch')
        nexus_words+=span['derived_words'];nexus_quotes+=span['direct_quotation_words']
    need(nexus_words==nexus['main_derived_words']==152 and nexus_quotes==0,'nexus aggregate source-accounting mismatch')
    need(nexus['companion']['derived_words']==companion['derived_words_total']==companion['direct_quote_words_total']==0 and companion['entries']==[],'companion source-accounting mismatch')
    need(nexus_words+reorientation.get('report_reserved_words',0)<=nexus['cap'],'aggregate source budget exceeded')
    report_docx_checked=False
    report_claim_blocks_checked=0
    report_derived_words_checked=0
    report_docx_paragraphs_checked=0
    if 'report_binding' in index:
        report=parse(resolve(index['report_binding']))
        need(report['status']=='FINAL_VERIFIED_REPORT_BOUND' and report['markdown_source_redistributed'] is False and report['report_prose_duplicated_in_ledgers'] is False and report['rename_only_docx_bytes_unchanged'] is True,'report custody/scope mismatch')
        review_bytes=resolve(report['acceptance_receipt']);review=parse(review_bytes)
        need(sha(review_bytes)==report['acceptance_receipt_sha256'] and review['status']=='PASS_BOUNDED_SOURCE_TEXT_AND_RENDERED_DOCX','report independent acceptance identity/status mismatch')
        accepted={r['name']:r for r in review['accepted_artifacts']}
        need(len(accepted)==len(review['accepted_artifacts']),'report duplicate accepted artifact')
        source=report['reviewed_markdown_source_identity_only']
        need(source==accepted['REPORT_SOURCE.md'],'report omitted source identity mismatch')
        need(not any(PurePosixPath(n).name=='REPORT_SOURCE.md' for n in tree),'report Markdown drafting source redistributed')
        supplied={r['reviewed_name']:r for r in report['accepted_payloads']}
        need(len(supplied)==len(report['accepted_payloads']) and set(supplied)==set(accepted)-{'REPORT_SOURCE.md'},'report accepted-payload census mismatch')
        for name,r in supplied.items():
            body=resolve(r['path'])
            need(sha(body)==r['sha256']==accepted[name]['sha256'] and len(body)==r['bytes']==accepted[name]['bytes'],'report exact accepted payload mismatch: '+name)
        docx=resolve(report['report_docx']);docx_hash=sha(docx)
        need(report['report_docx_original_name'] in supplied and supplied[report['report_docx_original_name']]['path']==report['report_docx'],'report DOCX rename binding mismatch')
        need({n for n in tree if n.endswith('.docx')}=={report['report_docx']},'report DOCX is missing or duplicated')
        docx_tree=zip_tree(docx,'final report DOCX')
        need('word/document.xml' in docx_tree,'report DOCX document XML missing')
        need(not any('vbaProject' in n or n.startswith('word/embeddings/') or n.startswith('word/comments') for n in docx_tree),'report DOCX has unreviewed active/embedded/comment material')
        for n,b in docx_tree.items():need(not path_pattern.search(b),'host path in report DOCX '+n)
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        xml=ET.fromstring(docx_tree['word/document.xml']);body=xml.find('w:body',ns)
        need(body is not None,'report DOCX body missing')
        paragraphs=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in body.findall('w:p',ns)]
        ledger_bytes=resolve(report['claim_ledger']);ledger=parse(ledger_bytes)
        keymap=parse(resolve(index['report_evidence_keys']))
        need(keymap['status']=='FINAL_REPORT_EVIDENCE_KEY_BINDINGS' and keymap['report_claim_ledger_sha256_at_preparation']==sha(ledger_bytes),'report evidence-key ledger identity mismatch')
        need(set(keymap['keys'])==set(ledger['evidence_keys']),'report evidence-key census mismatch')
        for key,original_key in ledger['evidence_keys'].items():
            public_key=keymap['keys'][key]
            need(public_key['title']==original_key['title'] and public_key['claim_ceiling']==original_key['claim_ceiling'] and public_key['evidence_status']==original_key['evidence_status'],'report evidence-key scope mismatch')
            need(len(public_key['identities'])==len(original_key['identities']),'report evidence identity census mismatch')
            for item,original_item in zip(public_key['identities'],original_key['identities']):
                need(all(item[k]==original_item[k] for k in ('name','sha256','bytes')),'report evidence original identity mismatch')
                if item['availability']=='exact_bytes_included':
                    data=resolve(item['locator']);need(sha(data)==item['sha256'] and len(data)==item['bytes'],'report evidence included-byte mismatch')
                elif item['availability']=='identity_binding_only_source_bytes_not_redistributed':
                    ref=item['binding'];value=pointer(parse(resolve(ref['locator'])),ref['json_pointer'],'report evidence binding')
                    need(value==item['sha256'],'report evidence identity-only binding mismatch')
                else:
                    need(item['availability']=='historical_reference_not_redistributed' and 'locator' not in item,'report evidence availability scope mismatch')
        account_bytes=resolve(report['source_accounting']);account=parse(account_bytes)
        mapping=parse(resolve(report['docx_claim_mapping']));spans=parse(resolve(report['docx_source_accounting']))
        need(mapping['docx']['sha256']==spans['docx']['sha256']==docx_hash,'report DOCX adapter identity mismatch')
        need(mapping['claim_ledger_sha256']==sha(ledger_bytes) and spans['source_accounting_sha256']==sha(account_bytes),'report adapter ledger binding mismatch')
        need(mapping['report_source_sha256']==spans['report_source_sha256']==source['sha256']==ledger['source_document']['sha256']==account['report']['sha256'],'report Markdown identity-only binding mismatch')
        need(len(paragraphs)==mapping['docx_body_paragraph_count']==review['artifact_review']['docx_text_paragraphs'],'report DOCX paragraph census mismatch')
        blocks={b['block']:b for b in ledger['blocks']};seen_blocks=set()
        need(len(blocks)==len(ledger['blocks']),'report claim ledger duplicate block')
        for r in mapping['bound_blocks']:
            ident=r['block'];need(ident in blocks and ident not in seen_blocks,'report claim adapter block census mismatch');seen_blocks.add(ident)
            i=r['docx_body_paragraph_index_zero_based'];need(isinstance(i,int) and not isinstance(i,bool) and 0<=i<len(paragraphs),'report claim paragraph index invalid')
            text=paragraphs[i]
            need(sha(text.encode('utf-8'))==r['visible_text_sha256_utf8'] and len(text)==r['visible_text_characters'] and len(text.split())==r['visible_text_words'],'report actual DOCX claim paragraph mismatch')
            need(r['evidence_keys']==blocks[ident]['evidence_keys'],'report claim evidence-key mapping mismatch')
        need(seen_blocks==set(blocks) and len(seen_blocks)==review['artifact_review']['docx_claim_adapter_blocks']==review['source_review']['all_source_blocks_read'],'report full claim-block census mismatch')
        report_claim_blocks_checked=len(seen_blocks);report_docx_paragraphs_checked=len(paragraphs)
        expected_spans=account['report_spans'];need(len(spans['spans'])==len(expected_spans)==review['artifact_review']['docx_source_accounting_spans'],'report accounting span census mismatch')
        by_work={};quotes=0
        for r,original in zip(spans['spans'],expected_spans):
            i=r['docx_body_paragraph_index_zero_based'];need(isinstance(i,int) and not isinstance(i,bool) and 0<=i<len(paragraphs),'report accounting paragraph index invalid')
            text=paragraphs[i];need(sha(text.encode())==r['paragraph_visible_text_sha256_utf8'],'report accounting paragraph hash mismatch')
            lo,hi=r['start_char'],r['end_char'];need(isinstance(lo,int) and isinstance(hi,int) and 0<=lo<=hi<=len(text),'report accounting span range invalid')
            part=text[lo:hi]
            need(sha(part.encode())==r['sha256_utf8']==original['sha256_utf8'] and len(part.split())==r['derived_words']==original['derived_words'],'report actual DOCX source-accounting span mismatch')
            need(r['work_key']==original['work_key'] and r['direct_quotation_words']==original['direct_quotation_words'] and r['same_span_as_reviewed_source'] is True,'report source-accounting scope mismatch')
            by_work[r['work_key']]=by_work.get(r['work_key'],0)+r['derived_words'];quotes+=r['direct_quotation_words']
        works={r['work_key']:r for r in account['works']};need(len(works)==len(account['works']),'report duplicate source work')
        for key,r in works.items():
            need(r['report_derived_words']==by_work.get(key,0) and r['aggregate_derived_words']==r['accepted_component_derived_words']+r['report_derived_words']<=r['cap'] and r['within_cap'] is True,'report cumulative source budget mismatch')
        need(set(by_work)<=set(works) and quotes==account['report_direct_quotation_words']==review['source_review']['new_direct_quote_words']==0,'report quotation/account census mismatch')
        need(works['PRUSS_RPSR2004']['accepted_component_derived_words']==nexus_words==spans['pruss_component_words'],'report/nexus prior source count mismatch')
        need(by_work.get('PRUSS_RPSR2004',0)==spans['pruss_report_words']==review['source_review']['report_Pruss_words']==36,'report Pruss count mismatch')
        need(nexus_words+by_work['PRUSS_RPSR2004']==spans['pruss_aggregate_words']==review['source_review']['cumulative_Pruss_words']==188,'report aggregate Pruss count mismatch')
        need(review['source_review']['final_G1_review_receipt_sha256']==sha(resolve(index['g1']['acceptance_receipt'])),'report accepted G1 receipt binding mismatch')
        need(review['source_review']['source_accounting_whole_report_review'] is True and review['source_review']['all_report_corrections_resolved'] is True and review['artifact_review']['text_differences']==0 and review['artifact_review']['all_19_pages_independently_rendered_and_visually_checked'] is True,'report whole-source/artifact review incomplete')
        report_docx_checked=True;report_derived_words_checked=sum(by_work.values())
    need(foundation['outer_added_primary_exposition_words'] == 0 and foundation['outer_added_direct_quotation_words'] == 0, 'unexpected outer source exposition')
    return {'status': 'PASS_STAGING_INTEGRITY_NOT_FINAL' if staging else 'PASS_SEALED_CANDIDATE_INTEGRITY_OUTER_ACCEPTANCE_PENDING',
            'outer_acceptance_established': False, 'manifest_sha256': manifest_hash,
            'outer_files_checked': outer_count, 'component_archives': len(archives),
            'all_archive_layers_checked': deep_archives, 'archive_members_checked': deep_members,
            'nested_manifests_checked': checked_manifests, 'nested_manifest_entries_checked': checked_entries,
            'evidence_links_checked': len(links['links']), 'projection_manifests_checked': projection_count,
            'final_report_docx_checked': report_docx_checked, 'report_claim_blocks_checked': report_claim_blocks_checked,
            'report_docx_body_paragraphs_checked': report_docx_paragraphs_checked, 'report_source_derived_words_checked': report_derived_words_checked,
            'specialist_exact_links_and_reversible_href_changes_checked': specialist_links_checked,
            'g1_v4_to_v2_exact_replay_metadata_bridge_checked': g1_bridge_checked,
            'supplementary_public_source_locators_checked': late_supplement_links_checked,
            'routing_cumulative_source_budgets_checked': late_routing_budgets_checked,
            'digest_sidecar_records_checked': sidecar_records, 'replay_locators_checked': replay_targets,
            'code_source_bindings_checked': len(binding_records), 'manifest_inventory_checked': len(manifest_inventory),
            'nexus_source_derived_words_checked': nexus_words,
            'trace_path_exceptions_checked': 5, 'source_accounting': 'PASS',
            'optimized_python': bool(sys.flags.optimize), 'proofs_reexecuted': False,
            'external_toolchain_verified_by_this_command': False}


def bind_detached_acceptance(receipt_bytes, archive_bytes, integrity_result, expected_receipt_sha256=None):
    """Verify a detached review's custody binding; this does not authenticate its author."""
    need(integrity_result.get('status')=='PASS_SEALED_CANDIDATE_INTEGRITY_OUTER_ACCEPTANCE_PENDING', 'detached acceptance requires checked sealed-candidate integrity')
    need(len(receipt_bytes)<=MAX_FILE,'detached receipt too large')
    receipt_hash=sha(receipt_bytes)
    if expected_receipt_sha256 is not None:
        need(receipt_hash==expected_receipt_sha256,'detached receipt external digest mismatch')
    receipt=parse(receipt_bytes)
    need(receipt.get('schema')=='ninth-detached-outer-acceptance-v1','detached receipt schema mismatch')
    need(receipt.get('decision')=='PASS_INDEPENDENT_OUTER_CUSTODY_REVIEW','detached receipt is not an independent outer custody PASS')
    candidate=receipt['candidate']
    need(candidate['archive_sha256']==sha(archive_bytes),'detached receipt archive digest mismatch')
    need(isinstance(candidate['archive_bytes'],int) and not isinstance(candidate['archive_bytes'],bool) and candidate['archive_bytes']==len(archive_bytes),'detached receipt archive size mismatch')
    need(candidate['manifest_sha256']==integrity_result['manifest_sha256'],'detached receipt manifest identity mismatch')
    checks=receipt.get('checks',{})
    need(all(checks.get(k) is True for k in ('normal_integrity','optimized_integrity','public_content_review','report_binding_review','g1_disposition_review')),'detached receipt required checks are incomplete')
    need(isinstance(receipt.get('scope'),str) and bool(receipt['scope'].strip()),'detached receipt scope is missing')
    result=dict(integrity_result)
    result.update(status='PASS_COLLECTION_INTEGRITY_WITH_BOUND_INDEPENDENT_OUTER_RECEIPT',outer_acceptance_established=True,detached_acceptance_sha256=receipt_hash,detached_acceptance_bytes=len(receipt_bytes),reviewer_identity_authenticated_by_this_command=False,receipt_trust_boundary='The detached receipt must be obtained from an independently trusted source. This command verifies its exact artifact binding, not the reviewer identity or scientific truth.')
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--directory', type=Path)
    group.add_argument('--archive', type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--staging', action='store_true', help='Verify staging custody without claiming final completion')
    mode.add_argument('--sealed-candidate', action='store_true', help='Verify immutable candidate contents while independent outer acceptance remains detached')
    parser.add_argument('--detached-acceptance', type=Path, help='Independent detached JSON receipt for this exact candidate ZIP')
    parser.add_argument('--expected-detached-sha256', help='Externally obtained detached receipt digest')
    parser.add_argument('--expected-sha256', help='Externally obtained outer ZIP digest')
    parser.add_argument('--expected-manifest-sha256', help='Externally obtained manifest digest')
    args = parser.parse_args()
    need(not args.detached_acceptance or (args.archive and args.sealed_candidate), 'detached acceptance requires --archive and --sealed-candidate')
    need(not args.expected_detached_sha256 or args.detached_acceptance, '--expected-detached-sha256 requires a detached receipt')
    if args.archive:
        need(args.archive.is_file() and not args.archive.is_symlink(), 'not a regular archive')
        data = args.archive.read_bytes()
        if args.expected_sha256:
            need(sha(data) == args.expected_sha256, 'outer ZIP digest mismatch')
        raw = zip_tree(data, str(args.archive))
        prefix = 'Ninth_Research_Evidence/'
        need(raw and all(n.startswith(prefix) for n in raw), 'outer archive root mismatch')
        tree = {n[len(prefix):]: b for n, b in raw.items()}
    else:
        need(not args.expected_sha256, '--expected-sha256 requires --archive')
        tree = local_tree((args.directory or Path(__file__).resolve().parent).resolve())
    if args.expected_manifest_sha256:
        manifest_key = 'STAGING_MANIFEST.json' if args.staging else 'MANIFEST.json'
        need(manifest_key in tree and sha(tree[manifest_key]) == args.expected_manifest_sha256, 'external manifest digest mismatch')
    result = check(tree, staging=args.staging, sealed_candidate=args.sealed_candidate)
    if args.detached_acceptance:
        need(args.detached_acceptance.is_file() and not args.detached_acceptance.is_symlink(), 'detached receipt is not a regular file')
        result=bind_detached_acceptance(args.detached_acceptance.read_bytes(),data,result,args.expected_detached_sha256)
    if args.archive:
        result['archive_sha256'] = sha(data)
        result['archive_bytes'] = len(data)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, UnicodeError, zipfile.BadZipFile, RuntimeError, ET.ParseError) as exc:
        print('FAIL_COLLECTION_INTEGRITY: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
