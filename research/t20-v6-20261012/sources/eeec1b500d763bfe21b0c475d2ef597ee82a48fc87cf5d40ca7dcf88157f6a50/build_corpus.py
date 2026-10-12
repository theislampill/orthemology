#!/usr/bin/env python3
"""Inventory actual attached/recovered ZIP bytes and compile a source-linked atlas.

Archive bytes are read with CRC validation; content is deduplicated by SHA-256.
Machine ingestion is deliberately NOT labelled a model's exhaustive reading.
No inherited source program is executed. Original source text is copied unchanged.
"""
from __future__ import annotations
import csv, hashlib, io, json, re, shutil, sys, traceback, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
DATA=Path('/mnt/data')
INPUT_NAMES=[
'T20bigupdatenext02.zip','T20bigupdateprev03.zip','T20bigupdateprev02.zip',
'T20bigupdatenext.zip','T20bigupdateprev.zip','T20bigupdate.zip',
'T20_Scriptural_Recovery_Supplement_20261009(1).zip',
'T20_Warranted_Discrimination_Research_and_Lean_20261009(2).zip',
'Orthemology_T20_Whole_Corpus_Synthesis_20261010.zip']
TRANSCRIPT=DATA/'Pasted markdown(20261010-235350).md'
RECOVERED=DATA/'t20_work/recovered_inputs'
TEXT_EXT={'.md','.txt','.rst','.log','.json','.yaml','.yml','.toml','.ini','.csv','.tsv',
'.lean','.py','.sh','.tex','.bib','.html','.xml','.js','.ts','.tsx','.c','.h','.cpp',
'.hpp','.jl','.r','.agda','.idr','.v','.hs','.ipynb','.cfg','.sql','.sml','.ml'}
REPORT_EXT={'.md','.rst','.tex'}
FONT_EXT={'.ttf','.otf','.woff','.woff2','.eot','.pfb','.pfa'}
BINARY_COPY={'.pdf','.png','.jpg','.jpeg','.webp'}
SOURCES=ROOT/'sources'; CORPUS=ROOT/'corpus'
for d in [SOURCES,CORPUS,ROOT/'evidence']:d.mkdir(parents=True,exist_ok=True)
archives={}; blobs={}; members=[]; inputs=[]; problems=[]; warnings=[]
MAX_MEMBER=512*1024*1024

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def safe_text(b):
    if b'\x00' in b[:20000]: return None
    for enc in ['utf-8-sig','utf-8']:
        try:return b.decode(enc)
        except UnicodeError:pass
    return None

def report_role(name,text):
    p=name.lower(); suf=PurePosixPath(name).suffix.lower()
    if any(x in p for x in ['node_modules/','.lake/packages/','site-packages/','.git/']):return False
    if suf in REPORT_EXT:return len(text.strip())>40
    if suf=='.txt' and any(x in p for x in ['report','research','summary','review','theorem','proof','readme','handoff','source','appraisal','analysis']):return len(text.strip())>100
    return False

def title_of(text, fallback):
    for line in text.splitlines():
        m=re.match(r'^\s*#{1,3}\s+(.+?)\s*#*\s*$',line)
        if m:return re.sub(r'[`*]','',m.group(1)).strip()[:240]
    for line in text.splitlines():
        if len(line.strip())>10 and not line.startswith(('---','```','{','[')):
            return line.strip()[:180]
    return fallback

def add_blob(b,name,parent=None):
    h=sha(b); suf=PurePosixPath(name).suffix.lower()
    if h not in blobs:
        rec={'id':'D-'+h[:20],'sha256':h,'bytes':len(b),'names':[], 'archive_ids':[],
             'suffix':suf,'kind':'binary','copied_path':None,'report':False}
        text=None
        if suf in TEXT_EXT or PurePosixPath(name).name.lower() in {'readme','license','lean-toolchain','makefile'}:
            text=safe_text(b)
        if suf in FONT_EXT:
            rec['kind']='font-not-republished'
        elif text is not None:
            rec['kind']='text'; rec['characters']=len(text);rec['lines']=len(text.splitlines())
            rec['title']=title_of(text,PurePosixPath(name).name)
            rec['report']=report_role(name,text)
            dest=SOURCES/(rec['id']+(suf or '.txt'));dest.write_bytes(b)
            rec['copied_path']=str(dest.relative_to(ROOT))
        elif suf in BINARY_COPY:
            rec['kind']='binary-source'; dest=SOURCES/(rec['id']+suf);dest.write_bytes(b)
            rec['copied_path']=str(dest.relative_to(ROOT))
        blobs[h]=rec
    rec=blobs[h]
    if name not in rec['names']:rec['names'].append(name)
    if parent and parent not in rec['archive_ids']:rec['archive_ids'].append(parent)
    if not rec['report'] and rec['kind']=='text':
        text=(ROOT/rec['copied_path']).read_text(encoding='utf-8-sig')
        rec['report']=report_role(name,text)
    return rec

def ingest_zip(b,logical,parent=None,depth=0):
    h=sha(b);aid='A-'+h[:20]
    if h in archives:
        if logical not in archives[h]['aliases']:archives[h]['aliases'].append(logical)
        return aid
    rec={'id':aid,'sha256':h,'bytes':len(b),'aliases':[logical],'parent_archive':parent,
         'members':0,'direct_source_ids':[],'crc_read_complete':False,'depth':depth}
    archives[h]=rec
    if depth>256:
        problems.append({'archive':logical,'error':'Depth limit exceeded'});return aid
    try:
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            for info in z.infolist():
                if info.is_dir():continue
                rec['members']+=1
                entry={'archive_id':aid,'path':info.filename,'declared_bytes':info.file_size,
                       'compressed_bytes':info.compress_size,'crc32':f'{info.CRC:08x}'}
                members.append(entry)
                pp=PurePosixPath(info.filename)
                if pp.is_absolute() or '..' in pp.parts:
                    warnings.append({'archive':logical,'member':info.filename,'warning':'unsafe original path; content-addressed output only'})
                if info.file_size>MAX_MEMBER:
                    problems.append({'archive':logical,'member':info.filename,'error':'member exceeds configured 512 MiB limit'});continue
                payload=z.read(info)
                entry['sha256']=sha(payload)
                if info.filename.lower().endswith('.zip') and zipfile.is_zipfile(io.BytesIO(payload)):
                    entry['nested_archive_id']=ingest_zip(payload,logical+'!/'+info.filename,aid,depth+1)
                else:
                    blob=add_blob(payload,info.filename,aid)
                    entry['source_id']=blob['id']
                    rec['direct_source_ids'].append(blob['id'])
            rec['crc_read_complete']=True
    except Exception as exc:
        problems.append({'archive':logical,'error':repr(exc)})
    return aid

for name in INPUT_NAMES:
    p=DATA/name
    if not p.is_file():
        problems.append({'input':name,'error':'missing attached path'});continue
    b=p.read_bytes();aid=ingest_zip(b,name)
    inputs.append({'name':name,'origin':'current-conversation upload','sha256':sha(b),'bytes':len(b),'archive_id':aid})
if RECOVERED.exists():
    for p in sorted(RECOVERED.glob('*.zip')):
        b=p.read_bytes();aid=ingest_zip(b,'Library recovery/'+p.name)
        inputs.append({'name':p.name,'origin':'materialised Library recovery','sha256':sha(b),'bytes':len(b),'archive_id':aid})
else:
    warnings.append({'input':str(RECOVERED),'warning':'recovered-input directory not present'})
if TRANSCRIPT.is_file():
    b=TRANSCRIPT.read_bytes();d=add_blob(b,TRANSCRIPT.name)
    inputs.append({'name':TRANSCRIPT.name,'origin':'current-conversation transcript','sha256':sha(b),'bytes':len(b),'source_id':d['id']})
else:problems.append({'input':TRANSCRIPT.name,'error':'transcript missing'})

B={r['id']:r for r in blobs.values()}; A={r['id']:r for r in archives.values()}
reports=sorted((r for r in blobs.values() if r['report']),key=lambda r:(r.get('title','').casefold(),r['id']))
THEMES={
'Foundations, sourcehood, necessity and attributes':{
 'terms':['wisdom','creator','sourcehood','necessary being','necessity','productive efficacy','repentance','receptivity','self_praise','self-praise','immanent','attestation','continuing_title','continuing title','scriptural','mediation'],
 'explain':'This strand concerns what the philosophical or source-based premises actually warrant: sourcehood and efficacy, target-local or common scope, attributes, disclosed reasons, and the force and conditions of an appropriate response. Preserve the dated appraisal and its premises; neither a toy countermodel nor a finite proof certificate silently replaces it.',
 'cross':'Crosswalk: proof-support witnesses localise defeat; source-context provenance identifies changes of interpretation or objective; the new overlap theorem supplies a conditional bridge from local exclusivity to a common source.'},
'Warrant, provenance, withdrawal and investigation':{
 'terms':['warrant','provenance','withdraw','audit','inquiry','investigation','proof cost','shared proof','historical_source','historical source','discrimination','restoration','source_revision','source revision'],
 'explain':'This strand asks which distinctions an investigator must retain to correct a belief, withdraw a source, combine proofs, and choose an informative next action. A current answer, a report probability, a proof support, and the cost of a shared proof are separate objects.',
 'cross':'Crosswalk: historical likelihood transport and conditional origin records connect audits to evolving state representations; dependency-directed replay connects them to source-sensitive objectives and finite certificates.'},
'Tensors, moment recovery, determinacy and effectivity':{
 'terms':['moment','tensor','determinacy','determinate','exponential_tail','exponential tail','capped','separating projection','finite atom','finite-atom','stationary_selection','stationary selection'],
 'explain':'This strand distinguishes recovering a represented law from a finite or infinite moment record, identifying it uniquely, and recovering it effectively with controlled data. A finite-support cap, a separating projection, a tail condition and a computable modulus discharge different obligations.',
 'cross':'Crosswalk: the likelihood-profile example shows why selected expectations need not preserve combinations of evidence; reliable compression requires the moments or features actually used by the allowed continuations.'},
'Realisability, positivity, continuation and damping':{
 'terms':['realisab','realizab','positivity','positive_hierarchy','positive hierarchy','boundary_jet','boundary jet','coercive','killing','damping','polynomial_functional','polynomial functional','heat_affine','heat affine','signed_energy','signed energy','signed_control','signed control','cumulative_law','cumulative law'],
 'explain':'This strand asks whether formal coordinates remain coordinates of an actual probability law during evolution. Componentwise positivity, finitely many square tests, initial determinacy, a full positive functional, and a proved invariant continuation class are not interchangeable.',
 'cross':'Crosswalk: numerical dynamics need a state-validity contract before their outputs can support inquiry or geometry; finite negative-square certificates can defeat an invalid state without reconstructing every detail of the underlying law.'},
'Geometry, posterior dynamics and discretisation':{
 'terms':['gradient','riemann','fisher','geometry','transport','quartic','discret','moving_objective','moving objective','gaussian_observation','gaussian observation','joint-atomic','joint atomic','full-law','full law'],
 'explain':'This strand develops actual geometric correction models, including posterior or leafwise structures, state-and-weight evolution, boundary behaviour, coercive examples and discrete preservation. Each theorem belongs to its specified model class; it is neither merely a drawing nor automatically a universal noetic dynamics.',
 'cross':'Crosswalk: an audit can change the metric or objective as well as the evidence weights. The new sensitivity and replay results identify that additional dependency and give a two-part approximation budget.'},
'Type completion, identity, semantics and effective certificates':{
 'terms':['sigma','induction','recursor','recursion','rigidity','completion','substitution','hase','has_e','fullper','per_','per ','dependent','numeral','canonical_syntax','canonical syntax','telescope','certificate','effective_source','effective source','extraction','serialized','raw_gap','raw gap'],
 'explain':'This strand separates what the original calculus can derive from what an explicitly extended calculus can derive, and separates broad semantic interpretation from finite effective proof checking. Dependent substitution, pairing, induction, recursor computation and uniqueness each require their own stated rules and proofs.',
 'cross':'Crosswalk: certificate checking can preserve the declared source and transformation chain without deciding every semantic truth; faithful extraction is an instance of the same operation-preservation question as audit-safe compression.'},
'Calibration, hidden structure and external representation research':{
 'terms':['calibrat','hidden','unknown structure','recover','weight subspace','universal weight','neural','low-rank','low rank','experimental cost','field guide'],
 'explain':'This strand connects the early recovery and calibration questions to later sufficiency and continuation results. Fitting selected observations or retaining high variance is not automatically preservation of an unseen structure under the next operation.',
 'cross':'Crosswalk: an external representation method should be tested against the declared continuation and decision contract, rather than adopted on the strength of a loose analogy with information or geometry.'},
}

def read_source(d):return (ROOT/d['copied_path']).read_text(encoding='utf-8-sig')
def theme_scores(rec):
    name=' '.join(rec['aliases']).lower(); text=name
    for sid in rec['direct_source_ids']:
        d=B.get(sid)
        if d and d['report']:text+='\n'+d.get('title','').lower()+'\n'+read_source(d)[:15000].lower()
    scores={name:sum(text.count(t) for t in spec['terms']) for name,spec in THEMES.items()}
    return sorted((n for n in scores if scores[n]),key=lambda n:-scores[n])

def canonical_name(rec):
    names=[PurePosixPath(s.split('!/')[-1]).name for s in rec['aliases']]
    return min(names,key=lambda n:(len(n),n))

def select_abstract(text, max_chars=2200):
    # Source-owned contiguous block, not an invented paraphrase.
    lines=text.splitlines(); starts=[]
    for i,line in enumerate(lines):
        if re.match(r'^#{1,4}\s+',line) and re.search(r'overview|summary|main result|principal result|what.*(prove|establish|change)|substantive|theorem|result|finding',line,re.I):starts.append(i)
    start=starts[0] if starts else 0
    window=[]; chars=0
    for line in lines[start:]:
        if chars+len(line)+1>max_chars and window:break
        window.append(line);chars+=len(line)+1
    content='\n'.join(window).strip()
    if start+len(window)<len(lines):content+='\n\n[Excerpt ends here; read the linked complete document for all hypotheses, proofs and qualifications.]'
    return content

def doc_rank(d):
    name=' '.join(d['names']).lower(); title=d.get('title','').lower()
    good=sum(4 for x in ['research','report','theorem','proof','appraisal','analysis'] if x in name or x in title)
    bad=sum(5 for x in ['manifest','checksum','inventory','source_register','verification','coverage','index','readme','handoff','status'] if x in name)
    return good-bad+min(d.get('characters',0)/12000,3)

def quote_block(t):return '\n'.join('> '+line if line else '>' for line in t.splitlines())

def source_link(d):return f"[{d.get('title',d['names'][0])}]({d['copied_path']})"

for rec in archives.values():
    rec['canonical_name']=canonical_name(rec);rec['themes']=theme_scores(rec)
    rec['direct_source_ids']=list(dict.fromkeys(rec['direct_source_ids']))
    rec['direct_report_ids']=[s for s in rec['direct_source_ids'] if B.get(s,{}).get('report')]

# Transcript-mentioned archive recovery accounting; literal spellings and common download suffixes.
mentioned=[]
if TRANSCRIPT.is_file():
    txt=TRANSCRIPT.read_text(encoding='utf-8-sig')
    mentioned=sorted(set(re.findall(r'(?<![\w/])([A-Za-z0-9][A-Za-z0-9_.() -]{4,160}\.zip)',txt)))
all_names={PurePosixPath(s.split('!/')[-1]).name.lower() for r in archives.values() for s in r['aliases']}
def normname(s):return re.sub(r'\(\d+\)(?=\.zip$)','',s.strip().lower())
normal_names={normname(s) for s in all_names}
mention_register=[{'mentioned':m,'exact_or_download_suffix_name_present':normname(m) in normal_names} for m in mentioned]

# Dated correction/supersession cues remain quotations rather than automatic judgements.
cues=[]
for d in reports:
    text=read_source(d);lines=text.splitlines()
    for i,line in enumerate(lines):
        if re.search(r'\bsupersed|\bretract|\bcorrection\b|\bcorrected\b|\bprevious.*(wrong|incorrect|gap)|\bearlier.*(wrong|incorrect|gap)|\bno longer\b',line,re.I):
            cues.append({'source_id':d['id'],'line_start':max(1,i-1),'line_end':min(len(lines),i+3),
                         'text':'\n'.join(lines[max(0,i-2):i+3])})

summary={'generated_utc':datetime.now(timezone.utc).isoformat(),'input_files':len(inputs),
 'top_level_archives':sum('archive_id' in x for x in inputs),'unique_archives':len(archives),
 'archive_member_records':len(members),'unique_non_archive_blobs':len(blobs),
 'unique_text_blobs':sum(r['kind']=='text' for r in blobs.values()),'unique_report_documents':len(reports),
 'copied_source_files':sum(r['copied_path'] is not None for r in blobs.values()),
 'report_characters':sum(r.get('characters',0) for r in reports),
 'archive_crc_read_complete':all(r['crc_read_complete'] for r in archives.values()),
 'problems':problems,'warnings':warnings,
 'coverage_meaning':'Complete machine ingestion and source inclusion where recorded; not a certificate of exhaustive model-visible reading or re-proving.',
 'inherited_programs_executed':False,'inherited_lean_freshly_compiled':False,
 'model_visible_readback_certified':False}
dump(CORPUS/'summary.json',summary);dump(CORPUS/'inputs.json',inputs)
dump(CORPUS/'archives.json',list(archives.values()));dump(CORPUS/'documents.json',list(blobs.values()))
dump(CORPUS/'members.json',members);dump(CORPUS/'transcript_archive_mentions.json',mention_register)
dump(CORPUS/'revision_cues.json',cues)
with (CORPUS/'documents.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['id','sha256','bytes','kind','report','copied_path','names','archive_ids'])
    for d in sorted(blobs.values(),key=lambda r:r['id']):w.writerow([d[k] for k in ['id','sha256','bytes','kind','report','copied_path']]+[' | '.join(d['names']),' | '.join(d['archive_ids'])])

register=['# T20 corpus register','',
'This is a content-addressed documentary register, not a claim that duplicate copies provide independent evidence. Original text files under `sources/` retain their exact bytes. Archive IDs and document IDs are SHA-256 prefixes; full hashes are in the JSON register. Fonts and non-document build artefacts are not republished.','',
'## Coverage totals','',*['- **'+k.replace('_',' ')+':** '+str(summary[k]) for k in ['input_files','top_level_archives','unique_archives','archive_member_records','unique_non_archive_blobs','unique_text_blobs','unique_report_documents','copied_source_files']],
'','These totals describe the actual attached and recovered bytes. “All T20” in this packet means this frozen corpus, not an assertion that Dot has stopped producing later work.','',
'## Input boundaries','', '| Input | Origin | Bytes | SHA-256 |','|---|---|---:|---|']
for x in inputs:register.append(f"| {x['name'].replace('|','/')} | {x['origin']} | {x['bytes']} | `{x['sha256']}` |")
register+=['','## Every unique archive','', '| Archive ID | Name | Direct reports | Primary thematic group |','|---|---|---:|---|']
for a in sorted(archives.values(),key=lambda r:(r['canonical_name'].lower(),r['id'])):
    register.append(f"| `{a['id']}` | {a['canonical_name'].replace('|','/')} | {len(a['direct_report_ids'])} | {(a['themes'][0] if a['themes'] else 'Container / supporting material')} |")
register+=['','## Every unique research report','', '| Document ID | Complete source | Bytes | Archive memberships |','|---|---|---:|---|']
for d in reports:register.append(f"| `{d['id']}` | {source_link(d).replace('|','/')} | {d['bytes']} | {', '.join(d['archive_ids']) or 'Direct transcript upload'} |")
register+=['','## Integrity and scope notes','',json.dumps({'problems':problems,'warnings':warnings},ensure_ascii=False,indent=2),
'','All member paths, aliases and full hashes are in `corpus/members.json`, `corpus/archives.json`, and `corpus/documents.json`. A missing original archive mentioned by a report is not silently fabricated. Literal transcript-mention matches are recorded separately; they are a navigation aid, not proof that every prose reference was correctly parsed.']
(ROOT/'Corpus_Register.md').write_text('\n'.join(register),encoding='utf-8')

atlas=['# Packet-by-packet T20 atlas','',
'Every unique archive discovered in the supplied and recovered inputs has an entry below. The explanations and crosswalks are editorial; indented source excerpts are copied from the named documents and retain their own status and qualifications. An archive date is not a proof of supersession. Where an archive is a cumulative container, its original child packets receive separate entries.','',
'An excerpt is navigation, not a substitute for its complete proof. Every report is included in `All_Research_Reports.md` and as an unchanged source file; the complete document register lists reports not selected as the lead excerpt of a packet.','']
for theme,spec in THEMES.items():
    atlas += [f'## {theme}', '', spec['explain'],'',spec['cross'],'']
    group=[a for a in archives.values() if a['themes'] and a['themes'][0]==theme]
    for a in sorted(group,key=lambda r:(re.findall(r'20\d{6}',r['canonical_name']) or ['00000000'],r['canonical_name'])):
        atlas += [f"### {a['canonical_name']}",'',f"**Archive:** `{a['id']}` · **SHA-256:** `{a['sha256']}`",'']
        ds=sorted((B[s] for s in a['direct_report_ids']),key=doc_rank,reverse=True)
        if not ds:atlas+=['This archive is principally a container or supporting evidence bundle; consult its child-archive entries and member register.','']
        else:
            atlas += ['**Lead document:** '+source_link(ds[0]),'',quote_block(select_abstract(read_source(ds[0]))),'']
            if len(ds)>1:
                atlas+=['**Additional complete documents:** '+ '; '.join(source_link(d) for d in ds[1:9])+('. Additional reports are listed in the corpus register.' if len(ds)>9 else '.'),'']
        if len(a['themes'])>1:atlas += ['**Cross-front connections:** '+ '; '.join(a['themes'][1:4])+'. These thematic matches are navigation suggestions, not inferred proof dependencies.','']
        if 'corrected' in a['canonical_name'].lower():atlas+=['**Revision flag:** this packet labels itself corrected. Read its exact correction and the preserved earlier version; the filename alone does not establish that every earlier claim was withdrawn.','']
other=[a for a in archives.values() if not a['themes']]
if other:
    atlas+=['## Containers and unclassified supporting archives','']
    for a in sorted(other,key=lambda r:r['canonical_name']):
        atlas+=[f"### {a['canonical_name']}",'',f"`{a['id']}`. {a['members']} direct member records. See the full member register and child-archive entries.",'']
(ROOT/'Packet_Atlas.md').write_text('\n'.join(atlas),encoding='utf-8')

with (ROOT/'All_Research_Reports.md').open('w',encoding='utf-8') as f:
    f.write('# Complete text anthology of the research reports\n\nThis anthology preserves every report-classified text file in the ingested corpus. The unchanged individual files are linked at each entry. Inclusion is documentary coverage, not an assertion of fresh independent proof checking. Source code, logs and manifests are indexed separately.\n\n')
    for d in reports:
        text=read_source(d); longest=max([len(m.group()) for m in re.finditer(r'`+',text)]+[2]); fence='`'*(longest+1)
        f.write(f"\n<a id=\"{d['id'].lower()}\"></a>\n\n## {d.get('title',d['id'])}\n\n**ID:** `{d['id']}` · **Complete unchanged source:** [{d['names'][0]}]({d['copied_path']})\n\n")
        f.write(fence+'text\n'+text+'\n'+fence+'\n')

rev=['# Revision and supersession ledger','',
'The following are source-local quotations containing explicit correction, supersession or revision cues. They are deliberately not converted into a machine-decided project-wide verdict. Read the full context before treating a cue as a retraction, recovery or replacement.','']
for cue in cues:
    d=B[cue['source_id']]; rev += [f"## {d.get('title',d['id'])} — lines {cue['line_start']}–{cue['line_end']}",'',source_link(d),'',quote_block(cue['text']),'']
(ROOT/'Revision_Ledger.md').write_text('\n'.join(rev),encoding='utf-8')

# Integrity check of every source copy: exact byte hash, not an unobserved assertion.
copy_checks=[]
for d in blobs.values():
    if d['copied_path']:
        p=ROOT/d['copied_path'];actual=sha(p.read_bytes())
        copy_checks.append({'id':d['id'],'path':d['copied_path'],'matches_original_member_sha256':actual==d['sha256']})
dump(ROOT/'evidence/04_source_copy_integrity.json',{'checks':len(copy_checks),'all_match':all(c['matches_original_member_sha256'] for c in copy_checks),'details':copy_checks})
print(json.dumps({k:v for k,v in summary.items() if k not in ['problems','warnings']},indent=2))
if problems:print('INGESTION PROBLEMS:',json.dumps(problems,indent=2))
