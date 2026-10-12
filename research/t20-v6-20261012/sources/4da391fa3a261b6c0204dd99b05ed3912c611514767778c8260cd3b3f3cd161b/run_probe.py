"""New portable comparison; never rebinds or executes the historical whole verifier."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
OLD='3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06'
NEW='852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0'
DEP='received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py'
def require(ok,message):
 if not ok:raise RuntimeError(message)
outputs=[];runs=[]
for flavor,expected in [('old',OLD),('repaired',NEW)]:
 actual=hashlib.sha256((ROOT/flavor/DEP).read_bytes()).hexdigest()
 require(actual==expected,'unexpected dependency bytes')
 historical_preflight=(actual==OLD)
 require(historical_preflight==(flavor=='old'),'historical pin boundary lost')
 for flags in [[],['-O']]:
  p=subprocess.run([sys.executable,*flags,'-B','test_transport.py'],cwd=ROOT/flavor/'hase-rational-kernel-transport-20261011',capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0'))
  require(p.returncode==0,p.stderr)
  result=json.loads(p.stdout);require(result['count']==162 and result['exhaustive_rows']==125 and result['status']=='PASS','caller scope changed')
  digest=hashlib.sha256(p.stdout.encode()).hexdigest();outputs.append(digest)
  runs.append({'dependency':flavor,'optimized':bool(flags),'checks':162,'finite_rows':125,'stdout_sha256':digest,'historical_dependency_pin_accepts':historical_preflight})
require(len(set(outputs))==1,'caller outputs differ')
print(json.dumps({'status':'PASS','runs':runs,'scope':'Exact exercised rational Python caller, disclosed substitution only; original pin refuses repaired bytes; not full Python-observable equivalence or historical 3097-pin/Lean verifier.'},indent=2))
