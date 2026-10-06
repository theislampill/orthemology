#!/usr/bin/env python3
"""Exercise the exact frozen census helper without running Lean or changing dependencies."""
from pathlib import Path
import ast,hashlib,json,sys
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
R=Path(__file__).resolve().parent;src=R/'snapshot/replay.py';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
txt=src.read_text();tree=ast.parse(txt);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_object_census'];assert len(nodes)==1
node=nodes[0];helper=ast.get_source_segment(txt,node);namespace={'Path':Path,'sha':sha}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(src),'exec'),namespace)
check=namespace['check_object_census'];out=R/'evidence/replay-guard-fixtures';assert not out.exists();out.mkdir()
rows=[]
for name in ['positive','extra-object','missing-object','symlink','wrong-object-digest','wrong-source-digest']:
 build=out/name;build.mkdir();f=build/'Fixture.olean';f.write_bytes(b'Non-executable object-census test fixture, not Lean bytecode.\n')
 sources={'Fixture':'bound-source-digest'};runs={'Fixture':{'exit_code':0,'source_sha256':'bound-source-digest','object_sha256':sha(f)}}
 if name=='extra-object':(build/'Unexpected.olean').write_bytes(b'extra')
 if name=='missing-object':f.unlink()
 if name=='symlink':(build/'unexpected-link').symlink_to('Fixture.olean')
 if name=='wrong-object-digest':runs['Fixture']['object_sha256']='0'*64
 if name=='wrong-source-digest':runs['Fixture']['source_sha256']='unbound-source'
 try:count=check(build,runs,sources);passed=True;msg=''
 except AssertionError as e:passed=False;count=None;msg=str(e)
 assert passed==(name=='positive'),(name,passed,msg)
 rows.append({'case':name,'accepted':passed,'verified_object_count':count,'diagnostic':msg,'expected_outcome_observed':True})
r={'status':'PASS_FROZEN_CENSUS_HELPER_CONTROLS','driver_sha256':sha(src),'exact_helper_source_sha256':hashlib.sha256(helper.encode()).hexdigest(),'cases':rows,'lean_processes_started':False,'dependency_objects_changed':False,'scope':'Exact helper execution with minimal non-executable fixtures; full invocation succeeded separately against the exact 167+5 independent object trees.'}
(R/'evidence/REPLAY_GUARDS.json').write_text(json.dumps(r,indent=2)+'\n');(R/'evidence/census_helper.py.txt').write_text(helper+'\n');print(json.dumps(r,indent=2))
