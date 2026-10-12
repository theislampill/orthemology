#!/usr/bin/env python3
"""Portable wrapper for the unchanged independent semantic-control review archive.

Proof sources and accepted receipts are preserved. Only environment paths and
successful-core-status compatibility are adapted for a clean rerun.
"""
from pathlib import Path,PurePosixPath
import argparse,difflib,hashlib,importlib.util,json,sys,zipfile,datetime
if sys.flags.optimize:raise RuntimeError('Optimized Python is refused')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ARCHIVE_PIN='a7dac7ac8fe8e867b4581ebcd2757067371985eb728a66fc83720e33389c8f9b'
MANIFEST_PIN='94b983318333e8bd79f08ba2e43f72add2f561629b3b54b05a37faed42d70abf'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def verified_archive(path):
 b=path.read_bytes();assert sha(b)==ARCHIVE_PIN,'Review archive identity mismatch'
 z=zipfile.ZipFile(path);names=z.namelist();assert len(names)==len(set(names))==737
 for i in z.infolist():
  p=PurePosixPath(i.filename);assert not p.is_absolute() and '..' not in p.parts and i.filename==str(p),'Unsafe member'
  assert not i.is_dir() and (i.external_attr>>16)&0o170000 not in [0o120000,0o060000,0o020000],'Nonregular member'
  assert not i.filename.endswith(('.olean','.ilean','.pyc','.o','.a')),'Unexpected compiled object'
 mbytes=z.read('REVIEW_MANIFEST.json');assert sha(mbytes)==MANIFEST_PIN
 m=json.loads(mbytes);assert {r['path'] for r in m['files']}|{'REVIEW_MANIFEST.json','REVIEW_MANIFEST.sha256'}==set(names)
 for r in m['files']:
  b=z.read(r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
 assert z.read('REVIEW_MANIFEST.sha256').decode().split()[0]==MANIFEST_PIN
 return z

def literal_derivation(original):
 old="cr['status']=='PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS'"
 new="cr['status'] in ['PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS','PASS_INDEPENDENT_REVIEW_CHECKS']"
 assert original.count(old)==1
 out=original.replace(old,new)
 old_archive="dependency=d.verify_dependencies(MATH,Path('private-locator:c8706d03ffdb12093ad5'),pins)"
 new_archive='dependency=d.verify_dependencies(MATH,ARCHIVE,pins)'
 assert out.count(old_archive)==1
 out=out.replace(old_archive,new_archive)
 compile(out,'literal-portable-driver.py','exec')
 return out

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--review-zip',type=Path,required=True);p.add_argument('--verify-only',action='store_true');p.add_argument('--lean-bin',type=Path);p.add_argument('--mathlib',type=Path);p.add_argument('--mathlib-archive',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
 if not a.verify_only:
  if any(v is None for v in [a.lean_bin,a.mathlib,a.out]):p.error('--lean-bin, --mathlib and --out are required')
  out=a.out.resolve();assert not out.exists(),'Output must be absent'
  for protected in [HERE,a.mathlib.resolve(),a.lean_bin.resolve().parent]:assert not out.is_relative_to(protected),'Output is inside protected source/dependency root'
 z=verified_archive(a.review_zip.resolve());core=z.read('replay_review.py');lit=z.read('replay_literal_independent.py').decode();derived=literal_derivation(lit)
 compile(core,'replay_review.py','exec')
 preflight={'status':'PASS_EXACT_REVIEW_ARCHIVE_AND_DERIVATION','archive_sha256':ARCHIVE_PIN,'review_manifest_sha256':MANIFEST_PIN,'verified_entries':737,'core_driver_sha256':sha(core),'literal_original_driver_sha256':sha(lit.encode()),'literal_derived_driver_sha256':sha(derived.encode()),'proof_sources_changed':False,'proof_loops_changed':False,'status_compatibility':'Both accepted staged and clean successful core statuses; subsequent source/object/closure checks unchanged','archive_path':'Explicit CLI value; no dependency edits'}
 if a.verify_only:print(json.dumps(preflight,indent=2));return
 out.mkdir(parents=True);snapshot=out/'review-source';snapshot.mkdir()
 for name in z.namelist():
  dest=snapshot/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(name))
 derivedpath=out/'literal_portable_driver.py';derivedpath.write_text(derived)
 (out/'LITERAL_PORTABILITY.diff').write_text(''.join(difflib.unified_diff(lit.splitlines(True),derived.splitlines(True),fromfile='original/replay_literal_independent.py',tofile='portable/literal_portable_driver.py')))
 result={**preflight,'status':'RUNNING','started_utc':utc(),'wrapper_sha256':sha(Path(__file__).read_bytes()),'outcome_boundary':'New execution result; original completed staged review receipts remain unchanged'}
 save=lambda:(out/'WRAPPER_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 save()
 try:
  mod=load('portable_semantic_core_review',snapshot/'replay_review.py')
  mod.ROOT=snapshot;mod.SOURCE=snapshot/'snapshot';mod.LEAN=(a.lean_bin/'lean').resolve();mod.MATH=a.mathlib.resolve();mod.ARCHIVE=a.mathlib_archive.resolve() if a.mathlib_archive else None;mod.OUT=out/'core'
  mod.main();cr=json.loads((mod.OUT/'RESULT.json').read_text());assert cr['status']=='PASS_INDEPENDENT_REVIEW_CHECKS'
  lm=load('portable_semantic_literal_review',derivedpath)
  lm.ROOT=snapshot;lm.SOURCE=snapshot/'literal-snapshot';lm.CORE=snapshot/'snapshot';lm.COREOUT=mod.OUT;lm.OUT=out/'literal';lm.LEAN=mod.LEAN;lm.MATH=mod.MATH;lm.ARCHIVE=mod.ARCHIVE
  lm.main();lr=json.loads((lm.OUT/'RESULT.json').read_text());assert lr['status']=='PASS_INDEPENDENT_LITERAL_ADDENDUM'
  result.update(status='PASS_END_TO_END_PORTABLE_INDEPENDENT_REVIEW',finished_utc=utc(),core_receipt_sha256=sha((mod.OUT/'RESULT.json').read_bytes()),literal_receipt_sha256=sha((lm.OUT/'RESULT.json').read_bytes()));save()
 except Exception as ex:result.update(status='FAILED_CLOSED',finished_utc=utc(),error=str(ex));save();raise
if __name__=='__main__':main()
