#!/usr/bin/env python3
"""Offline, narrow, idempotent, fail-closed publication-projection copier.
Does NOT push, open PRs, update canonical successor research state, or execute upstream scripts.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
PACKAGE=Path(__file__).resolve().parents[1]
BASE='3a0bdeaa1394c656245cae9599adcb143e885059'
BASE_FILE='experiments/orthemology-v5-successors/groups/t20-successor/ASSEMBLY_STATE.json'
BASE_BLOB_SHA='40d80962256983c219eb9079461ad5b1482c8bbb'
PUB='research/t20-live-20261009/'
def h(f):
 q=hashlib.sha256()
 with open(f,'rb') as s:
  for b in iter(lambda:s.read(1024*1024),b''):q.update(b)
 return q.hexdigest()
def git(repo,*args):
 p=subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True)
 if p.returncode:raise RuntimeError('git '+ ' '.join(args)+' failed: '+p.stderr[:1200])
 return p.stdout.strip()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--dry-run',action='store_true');ap.add_argument('--allow-dirty',action='store_true',help='NOT recommended; only for applying identical existing projection');a=ap.parse_args()
 repo=Path(a.repo).resolve();root=Path(git(repo,'rev-parse','--show-toplevel'))
 if root!=repo:raise RuntimeError('Pass the exact repository root')
 if not a.allow_dirty and git(repo,'status','--porcelain'):
  raise RuntimeError('Working tree is not clean; do not overwrite any work')
 git(repo,'cat-file','-e',BASE+'^{commit}')
 if subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',BASE,'HEAD']).returncode:
  raise RuntimeError('Expected merged 2026-10-08 baseline not an ancestor of HEAD')
 bf=repo/BASE_FILE
 if not bf.is_file() or git(repo,'hash-object',str(bf))!=BASE_BLOB_SHA:
  raise RuntimeError('Frozen T20 source anchor differs; reacquire and review current repo first')
 m=json.loads((PACKAGE/'inventory/PUBLIC_PROJECTION.json').read_text())
 copied=skipped=0
 todo=[]
 # Complete preflight BEFORE any publication writes: a late collision cannot
 # produce a partially staged repository tree.
 for entry in m['published']:
  rel=entry['repo_path'];src=PACKAGE/'PUBLIC_OVERLAY'/rel;dst=repo/rel
  if not rel.startswith(PUB) or src.is_symlink() or not src.is_file() or h(src)!=entry['public_sha256']:
   raise RuntimeError('Invalid preimage/allowed path: '+rel)
  if dst.is_symlink() or any(parent.is_symlink() for parent in dst.parents if parent!=repo and repo in parent.parents):
   raise RuntimeError('Destination or ancestor is a symlink: '+rel)
  if dst.exists():
   if not dst.is_file() or h(dst)!=entry['public_sha256']:raise RuntimeError('Existing path differs: '+rel)
   skipped+=1;continue
  todo.append((src,dst))
 copied=len(todo)
 if not a.dry_run:
  for src,dst in todo:
   dst.parent.mkdir(parents=True,exist_ok=True)
   dst.write_bytes(src.read_bytes())
 print(json.dumps({'verified_existing':skipped,'to_copy' if a.dry_run else 'copied':copied,'dry_run':a.dry_run,'baseline':BASE,'root':str(repo)},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e: print('REFUSED:',e,file=sys.stderr);sys.exit(2)
