from pathlib import Path
import hashlib,json,re
W=Path(__file__).resolve().parents[2];R=W/'hase-finite-raw-obstruction-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rp=W/'hase-full-per-review-20261010/PREREQUISITE_REBUILD.json';receipt=json.loads(rp.read_text())
cs={x['module']:x for x in receipt['source_checks']};br={x['module']:x for x in receipt['build_records']};mods=set();external=set()
def add(m):
 if m in mods:return
 if m not in cs:external.add(m);return
 mods.add(m)
 for n in cs[m]['imports']:add(n)
add('ExtensionalRepairSyntax');rows=[]
for m in sorted(mods):
 p=W/'hase-imported-compiler-transport-20261010/sources'/f'{m}.lean';o=W/'hase-full-per-review-20261010/fresh-lib'/f'{m}.olean'
 assert sha(p)==cs[m]['sha256'],m
 assert sha(o)==br[m]['object_sha256'],m
 rows.append({'module':m,'source_path':str(p.relative_to(W)),'source_sha256':sha(p),'object_path':str(o.relative_to(W)),'object_sha256':sha(o),'verified_against':'PREREQUISITE_REBUILD.json/source_checks and build_records'})
packages=W/'separating-projection-lean-20261009/.lake/packages';dirs=sorted(x for x in packages.iterdir() if x.is_dir());external.add('Mathlib.Data.Fintype.Card');extrows={}
def strip_comments(s):
 out=[];i=0;depth=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;i+=2
  elif depth and s[i:i+2]=='-/':depth-=1;i+=2
  elif depth:
   if s[i]=='\n':out.append('\n')
   i+=1
  elif s[i:i+2]=='--':
   i=s.find('\n',i)
   if i<0:break
  else:out.append(s[i]);i+=1
 return ''.join(out)
def addext(m):
 if m in extrows or m in ['Init','Lean','Std'] or m.startswith(('Lean.','Init.','Std.')):return
 rel=Path(*m.split('.'));opts=[(d/rel.with_suffix('.lean'),d/'.lake/build/lib/lean'/rel.with_suffix('.olean')) for d in dirs];opts=[(s,o) for s,o in opts if s.exists() and o.exists()]
 assert len(opts)==1,(m,opts)
 s,o=opts[0];extrows[m]={'module':m,'source_path':str(s.relative_to(W)),'source_sha256':sha(s),'object_path':str(o.relative_to(W)),'object_sha256':sha(o),'scope':'Existing pinned external source/object pair; not rebuilt in this pass.'}
 source=strip_comments(s.read_text())
 for line in source.splitlines():
  if re.match(r'^import\s',line):
   for n in re.sub(r'--.*','',line).split()[1:]:addext(n)
for m in sorted(external):addext(m)
controls=['hase-type-indexed-henkin-obstruction-20261010/RESULT.md','hase-type-family-review-20261010/REVIEW.md']
bind={'scope':'Reused source/object closure verified against prior trust-zero receipt. External source/object import closure hash-bound, not rebuilt. Official Lean/Init/Std libraries come from the retained Lean 4.19.0 toolchain.','source_pin':receipt['pin'],'mathlib_revision':receipt['mathlib_revision'],'lean_binary_sha256':sha(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'receipt':{'path':str(rp.relative_to(W)),'sha256':sha(rp)},'source_objects':rows,'external_source_objects':[extrows[m] for m in sorted(extrows)],'read_only_prior_controls':[{'path':p,'sha256':sha(W/p)} for p in controls]}
(R/'INPUTS.json').write_text(json.dumps(bind,indent=2)+'\n');print('Bound source/object pairs:',len(rows),'External source/object pairs:',len(extrows))
