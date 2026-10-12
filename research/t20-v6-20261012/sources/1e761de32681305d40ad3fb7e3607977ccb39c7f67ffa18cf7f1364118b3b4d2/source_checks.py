#!/usr/bin/env python3
"""Bounded mechanical and exact-rational replay, not new source interpretation."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess,re
sys.dont_write_bytecode=True
root,w,out=map(lambda x:Path(x).resolve(),sys.argv[1:]);out.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,s):
 if not c:raise ValueError(s)
# Run unchanged author script in a disposable sibling-source overlay.
A='prior-evidence-correction-20261010';stage=out/'stage';stage.mkdir();author=stage/A;shutil.copytree(root/A,author)
bindings=json.loads((author/'INPUT_BINDINGS.json').read_text())
for r in bindings:
 src=author/r['packet_path'];need(sha(src)==r['sha256'] and sha(w/r['source_path'])==r['sha256'],'Original prior-source custody')
 dst=stage/r['source_path'];need(dst.resolve().is_relative_to(stage),'Unsafe overlay path');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
q=subprocess.run([sys.executable,str(author/'verify.py')],cwd=stage,capture_output=True,text=True);(out/'AUTHOR_REPLAY.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'Author controls failed');need((author/'CHECK_RESULTS.json').read_bytes()==(root/A/'CHECK_RESULTS.json').read_bytes(),'Author control result differs')
review=out/'independent';(review/'controls').mkdir(parents=True);script=root/'m2-prior-independent-review-20261010/controls/independent_bayes.py';shutil.copyfile(script,review/'controls/independent_bayes.py')
q=subprocess.run([sys.executable,str(review/'controls/independent_bayes.py')],capture_output=True,text=True);(out/'INDEPENDENT_REPLAY.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'Independent rational controls failed');need((review/'INDEPENDENT_CONTROLS.json').read_bytes()==(root/'m2-prior-independent-review-20261010/INDEPENDENT_CONTROLS.json').read_bytes(),'Independent result differs')
# Root's recorded default-branch read is currentness evidence, not another live lookup.
j=json.loads((root/'prior-evidence-root-check-20261010/DEFAULT_BRANCH_READ.json').read_text());b=j['content'].encode();need(b==(root/A/'sources/M2-prior-probability.md').read_bytes(),'Root retrieved content mismatch');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==j['sha'],'Root Git blob mismatch')
# Exact extract identity against the retained received page-map, without new reading credit.
O='owed-response-specification-20261010';record=json.loads((root/O/'SOURCE_READS.json').read_text())
for r in record['files']:need(sha(w/r['path'])==r['sha256'] and (w/r['path']).stat().st_size==r['bytes'],'Owed witness custody')
s=(w/O/'sources/ubudiyya-majmu10-direction-clean.txt').read_text();matches=list(re.finditer(r'ج/\s*10\s*ص\s*-(\d+)-',s));pages={int(m[1]):s[m.start():matches[i+1].start() if i+1<len(matches) else len(s)] for i,m in enumerate(matches)};need(len(matches)==len(pages),'Duplicate source page marker');n=0
for p in (w/O/'sources').glob('ubudiyya-[0-9]*-[0-9]*.txt'):
 a,b=map(int,re.fullmatch(r'ubudiyya-(\d+)-(\d+)\.txt',p.name).groups());need(p.read_text()=='\n\n'.join(pages[k] for k in range(a,b+1)),'Derived extract mismatch');n+=1
v=json.loads((root/'review-owed-response-specification-20261010/VERIFICATION.json').read_text())
for name,h in v['author_files'].items():need(sha(root/O/name)==h,'Owed reviewer/author binding')
receipt={'status':'PASS_BOUNDED_TEXT_AND_RATIONAL_CHECKS','author_rational_groups':15,'independent_binary_models':1080,'independent_threshold_checks':9720,'owed_exact_extracts':n,'owed_witness_hashes':len(record['files']),'root_default_branch_record_bound':True,'new_live_lookup':False,'new_independent_reading':False,'proof_assistant_credit_for_text_or_rational_tests':False};(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
