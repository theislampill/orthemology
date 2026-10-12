#!/usr/bin/env python3
"""Non-destructive recursive corpus register for the supplied T20 freeze.

Reads ZIP members rather than extracting arbitrary paths. Nested archives are
content-addressed. Text copies keep exact source bytes under safe hash names.
Automatically extracted text is never labelled a fresh scholarly reading.
"""
import collections, hashlib, io, json, os, re, shutil, stat, sys, zipfile
from pathlib import Path, PurePosixPath

ROOT=Path('private-locator:f0a43fb1181206830296')
INPUT=Path('/mnt/data')
TOP_NAMES=['T20bigupdatenext.zip','T20bigupdateprev.zip','T20bigupdate(1).zip',
           'T20bigupdateprev03.zip','T20bigupdateprev02.zip',
           'T20_Scriptural_Recovery_Supplement_20261009.zip',
           'T20_Warranted_Discrimination_Research_and_Lean_20261009.zip']
SOURCES=ROOT/'sources'; SOURCES.mkdir(parents=True,exist_ok=True)
for x in ('inventory','predecessor_work','evidence'): (ROOT/x).mkdir(exist_ok=True)
archives={}; members=[]; texts={}; warnings=[]; failures=[]; total=0
MAX_MEMBER=512*1024*1024; MAX_TOTAL=5*1024*1024*1024

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def family(name):
    s=name.lower()
    if s.startswith('t20bigupdate'): return 'Delivery container'
    if any(x in s for x in ('codex','integration','handoff','launch','consolidated','pr_review','pr-review')): return 'Integration / predecessor / handoff'
    if any(x in s for x in ('hase','sigma','induction','rigidity','type-','type_','substitution','church','fold_transfer','unit_and_fold','complete-development')): return 'Type theory and identity'
    if any(x in s for x in ('repentance','receptivity','self_praise','immanent','determination_source','particular_explanation','wise_reason','wise_means','recipient_right','intrinsic_succession','authority','interpretation_repair','source-successor','source_packet','particular_determination')): return 'Affirmative foundations / source interpretation'
    if any(x in s for x in ('moment','effectivity','tail','stationary','positive_hierarchy','initial_validity','initial_positivity','capped_tensor','fisher_endpoint')): return 'Measure, realisability and computability'
    if any(x in s for x in ('geometry','hessian','nonseparable','tensor','channel','facial','constraint','marginal','feasibility')): return 'Geometry, tensors and learning'
    if any(x in s for x in ('scriptural','recognition','noetic-recognition')): return 'Recognition / communication / DAEE'
    if any(x in s for x in ('proof','discrimination','audit','inquiry','posterior','reset','evidence-revision')): return 'Proof, audit and inquiry'
    if any(x in s for x in ('t20','twentieth','checkpoint')): return 'Earlier or multi-front T20'
    return 'Inherited / other preserved dependency'

def text_candidate(name,size):
    p=PurePosixPath(name); base=p.name.lower(); ext=p.suffix.lower()
    if size>3*1024*1024: return False
    if ext=='.md':
        return any(x in base for x in ('readme','read_me','read_first','read-first','start_here','guide','result','report','review','theorem','synthesis','boundary','foundat','assessment','finding','adjudication','scope','crosswalk','source','status','warrant'))
    if ext=='.tex': return True
    if ext=='.json':
        return base in ('delta_manifest.json','verification.json','check_results.json','source_record.json','source_records.json','sources.json','omissions_and_dependencies.json','component_manifest_checks.json','prior_checkpoint.json','continued_operations.json') or ('review' in base and 'manifest' not in base)
    return False

def read_archive(data,name,location,depth=0):
    global total
    digest=sha(data)
    if digest in archives:
        archives[digest]['occurrences'].append(location)
        if name not in archives[digest]['names']: archives[digest]['names'].append(name)
        return
    rec={'sha256':digest,'bytes':len(data),'names':[name],'occurrences':[location],
         'family':family(name),'member_count':0,'crc_status':'NOT_COMPLETED','warnings':[]}
    archives[digest]=rec
    if depth>18:
        failures.append({'location':location,'reason':'Nested depth bound exceeded'});return
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos=z.infolist(); rec['member_count']=len(infos)
            seen=set()
            for info in infos:
                entry={'archive_sha256':digest,'path':info.filename,'bytes':info.file_size,
                       'compressed_bytes':info.compress_size,'directory':info.is_dir()}
                if info.filename in seen: rec['warnings'].append('duplicate member path: '+info.filename)
                seen.add(info.filename)
                p=PurePosixPath(info.filename)
                safe=not (p.is_absolute() or '..' in p.parts or '\\' in info.filename or '\x00' in info.filename)
                islink=stat.S_ISLNK(info.external_attr>>16)
                entry['safe_relative_path']=safe;entry['symlink']=islink
                if not safe or islink: rec['warnings'].append('Unsafe path/link retained only as inventory: '+info.filename)
                if info.is_dir(): members.append(entry);continue
                if info.file_size>MAX_MEMBER or total+info.file_size>MAX_TOTAL:
                    raise RuntimeError('Read-size safety limit reached at '+info.filename)
                b=z.read(info);total+=len(b);h=sha(b);entry['sha256']=h;members.append(entry)
                if info.filename.lower().endswith('.zip') and zipfile.is_zipfile(io.BytesIO(b)):
                    read_archive(b,p.name,location+' :: '+info.filename,depth+1)
                elif text_candidate(info.filename,len(b)):
                    try: txt=b.decode('utf-8-sig')
                    except UnicodeDecodeError: continue
                    if h not in texts:
                        ext=p.suffix.lower();out=SOURCES/(h+ext);out.write_bytes(b)
                        texts[h]={'sha256':h,'bytes':len(b),'line_count':len(txt.splitlines()),
                                  'path':str(out.relative_to(ROOT)), 'title':next((l.lstrip('# ').strip() for l in txt.splitlines() if l.strip()),p.name)[:220],
                                  'source_kind':'automatically extracted unchanged source',
                                  'fresh_assistant_reading':'NOT_CLAIMED', 'bindings':[]}
                    texts[h]['bindings'].append({'archive_sha256':digest,'member':info.filename,'archive_name':name})
            rec['crc_status']='PASS_ALL_MEMBERS_READ'
    except Exception as e:
        rec['crc_status']='FAILED_OR_INCOMPLETE';rec['error']=str(e)
        failures.append({'location':location,'reason':str(e)})

inputs=[]
for name in TOP_NAMES:
    path=INPUT/name
    if not path.is_file(): failures.append({'location':name,'reason':'Top-level input missing'});continue
    b=path.read_bytes();inputs.append({'name':name,'bytes':len(b),'sha256':sha(b),'path':str(path)})
    read_archive(b,name,name)

# Preserve the previous unfinished attempt's actual program and metadata, without
# assuming its reports prove a new reading or replay in the resumed execution.
for name in ('t20_inventory.py','t20_extract.py','t20_index.py','t20_reading_batches.py'):
    p=INPUT/name
    if p.is_file(): shutil.copy2(p,ROOT/'predecessor_work'/name)
pwork=INPUT/'t20_synthesis_work'; preserved=[]
if pwork.exists():
    for p in sorted(pwork.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(pwork)
        if len(rel.parts)>2 or p.stat().st_size>20*1024*1024 or p.suffix.lower() not in ('.json','.jsonl','.csv','.md','.txt'): continue
        out=ROOT/'predecessor_work'/('workspace__'+'__'.join(rel.parts))
        shutil.copy2(p,out);preserved.append({'original':str(p),'copy':str(out.relative_to(ROOT)),'sha256':sha(p.read_bytes())})
        if len(preserved)>=80: warnings.append('Predecessor metadata copy capped at 80 files');break

# Explicitly compare every mounted standalone ZIP to the content-addressed corpus.
standalone=[]
for p in sorted(INPUT.glob('*.zip')):
    h=sha(p.read_bytes());standalone.append({'name':p.name,'bytes':p.stat().st_size,'sha256':h,'present_in_7_input_recursive_corpus':h in archives})

ordered=sorted(archives.values(),key=lambda r:(r['family'],r['names'][0].lower(),r['sha256']))
for i,r in enumerate(ordered,1): r['archive_id']='A%03d'%i
ids={r['sha256']:r['archive_id'] for r in ordered}
textlist=sorted(texts.values(),key=lambda t:(t['bindings'][0]['archive_name'].lower(),t['bindings'][0]['member']))
for i,r in enumerate(textlist,1): r['source_id']='S%04d'%i

summary={'scope':'Seven explicitly supplied top-level inputs, recursively content-addressed',
         'top_level_inputs':len(inputs),'unique_zip_objects':len(archives),
         'archive_occurrences':sum(len(x['occurrences']) for x in archives.values()),
         'zip_member_occurrences_in_unique_zip_objects':len(members),
         'unique_selected_source_reports':len(textlist),
         'selected_source_lines_automatically_extracted':sum(x['line_count'] for x in textlist),
         'bytes_read_for_crc_and_hashing':total,
         'family_counts':dict(collections.Counter(x['family'] for x in ordered)),
         'failures':failures,'warnings':warnings,
         'global_all_T20_ever_complete':'NOT_CERTIFIED_WITHOUT_AUTHOR_CANONICAL_MANIFEST',
         'all_source_proofs_read_by_assistant':'NOT_CLAIMED',
         'current_visible_tool_readback':'NOT_AVAILABLE_TO_ASSISTANT'}
dump(ROOT/'inventory'/'INPUTS.json',inputs)
dump(ROOT/'inventory'/'ARCHIVES.json',ordered)
dump(ROOT/'inventory'/'SOURCE_REPORTS.json',textlist)
dump(ROOT/'inventory'/'CORPUS_SUMMARY.json',summary)
dump(ROOT/'inventory'/'MOUNTED_ZIP_RECONCILIATION.json',standalone)
dump(ROOT/'inventory'/'PREDECESSOR_WORK.json',preserved)
with (ROOT/'inventory'/'MEMBERS.jsonl').open('w',encoding='utf-8') as f:
    for r in members: f.write(json.dumps(r,ensure_ascii=False)+'\n')

lines=['# Corpus register: the supplied T20 freeze','',
       'This register counts archive objects, not discoveries. Identical bytes at multiple locations have one archive ID. Different bytes with the same or similar names remain distinct.', '',
       f'**Top-level inputs:** {len(inputs)}. **Distinct nested ZIP objects:** {len(archives)}. **Selected unique source reports:** {len(textlist)}.', '',
       '**Completeness boundary:** reconciliation is against the seven supplied inputs and mounted ZIPs, not an independently certified list of every T20 delivery ever made. T20 remains active.', '',
       '**Read status:** source reports are automatically copied unchanged. This does not assert line-by-line scholarly reading or fresh verification of every proof.', '',
       '## Top-level input identities','']
for r in inputs:
    lines += [f"### `{r['name']}`",f"Bytes: {r['bytes']:,}. SHA-256: `{r['sha256']}`.",'']
for fam in sorted({r['family'] for r in ordered}):
    lines += ['## '+fam,'']
    for r in [x for x in ordered if x['family']==fam]:
        reports=[x for x in textlist if any(b['archive_sha256']==r['sha256'] for b in x['bindings'])]
        lines += [f"### {r['archive_id']} — `{r['names'][0]}`",'',
                  f"**Bytes:** {r['bytes']:,}; **members:** {r['member_count']}; **CRC read:** {r['crc_status']}.",
                  f"**SHA-256:** `{r['sha256']}`."]
        if len(r['names'])>1: lines += ['Other exact-byte names: '+', '.join('`'+n+'`' for n in r['names'][1:])+'.']
        lines += ['','Original location(s):']+['- `'+x+'`' for x in r['occurrences']]
        if reports:
            lines += ['','Preserved entry reports (full source index includes all bindings):']
            for x in reports[:10]:
                binding=next(b for b in x['bindings'] if b['archive_sha256']==r['sha256'])
                lines += [f"- [{x['source_id']}: {binding['member']}]({x['path']})"]
            if len(reports)>10: lines += [f'- {len(reports)-10} further reports in `SOURCE_REPORT_INDEX.md`.']
        else: lines += ['','No selected entry-report filename was recognised in this archive. Member inventory remains available; a nested/cumulative container can carry its reports in child archives.']
        lines += ['']
lines+=['## Unresolved inventory failures','',json.dumps(failures,ensure_ascii=False,indent=2) if failures else 'The inventory program recorded no read failures. This is a machine-generated status, not an independently observed scholarly audit.','']
(ROOT/'CORPUS_REGISTER.md').write_text('\n'.join(lines),encoding='utf-8')

sl=['# Source report index','',
    'Each linked file is an unchanged UTF-8 source member. Its source ID is local to this synthesis packet; its content hash and original archive/member binding are the authority. A file being included does not mean it was freshly read, proved, or replayed by this assistant.','']
for r in textlist:
    sl += [f"## {r['source_id']} — {r['title']}",f"[Read unchanged source]({r['path']})",'',
           f"SHA-256 `{r['sha256']}`; {r['bytes']:,} bytes; {r['line_count']:,} text lines."]
    for b in r['bindings']:
        sl += [f"- {ids[b['archive_sha256']]} `{b['archive_name']}` :: `{b['member']}`"]
    sl += ['']
(ROOT/'SOURCE_REPORT_INDEX.md').write_text('\n'.join(sl),encoding='utf-8')

# A portable local semantic index: find exact words without archive extraction.
search='''#!/usr/bin/env python3\nimport argparse,json\nfrom pathlib import Path\np=argparse.ArgumentParser(description="Search unchanged selected source reports")\np.add_argument("term");p.add_argument("--limit",type=int,default=30);a=p.parse_args()\nroot=Path(__file__).resolve().parents[1]\nrows=json.loads((root/"inventory/SOURCE_REPORTS.json").read_text())\nn=0\nfor r in rows:\n    text=(root/r["path"]).read_text(encoding="utf-8-sig")\n    for i,line in enumerate(text.splitlines(),1):\n        if a.term.casefold() in line.casefold():\n            print(f'{r["source_id"]}:{i}: {line[:600]}')\n            print("  "+r["bindings"][0]["archive_name"]+" :: "+r["bindings"][0]["member"])\n            n+=1\n            if n>=a.limit:raise SystemExit(0)\n'''
(ROOT/'verification'/'search_sources.py').write_text(search,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
