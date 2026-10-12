#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--cold',type=Path,required=True);p.add_argument('--lean-bin',type=Path,required=True);p.add_argument('--mathlib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;out=a.out.resolve();assert not out.exists();out.mkdir(parents=True)
 cold=a.cold.resolve();receipt=json.loads((cold/'REPLAY_RESULT.json').read_text());assert receipt['status']=='PASS' and receipt['input_manifest_sha256']=='3b143fc2c7df13f68893a8de5d65ec7a7e7ea8721af6252e6fed06e433b26fa9'
 build=cold/'fair_component_recurrence/build';lean=a.lean_bin.resolve()/'lean';assert sha(lean)==receipt['lean_sha256']
 for r in receipt['suites'][0]['modules']:assert sha(build/Path(r['module'].replace('.','/')+'.olean'))==r['olean_sha256']
 ml=a.mathlib.resolve();libs=[build,ml/'.lake/build/lib/lean']+list((ml/'.lake/packages').glob('*/.lake/build/lib/lean'))
 env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,libs));env['PATH']=str(lean.parent)+':'+env['PATH'];env.pop('LEAN_SRC_PATH',None)
 source=root/'IndependentIndexControls.lean'
 run=subprocess.run([str(lean),'-j1','--root='+str(root),'-o',str(out/'IndependentIndexControls.olean'),str(source)],cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/'CONTROL.log').write_text(run.stdout);assert run.returncode==0,run.stdout
 assert not re.search(r'\b(warning|error):|sorryAx',run.stdout)
 targets=re.findall(r"'(RecurrenceIndependentReview\.[^']+)'",run.stdout);assert len(targets)==7
 # Removing the initial-coordinate distinction gives the wrong numerical claim.
 negative=out/'NegativeIndex.lean';negative.write_text('import IndependentIndexControls\nopen RecurrenceIndependentReview HiddenParity.Recurrence\nexample : avoid biasedChain 1 1 0 = (1/4 : ℝ) := by norm_num [avoid, biasedChain, Fin.sum_univ_two]\n')
 env['LEAN_PATH']=str(out)+':'+env['LEAN_PATH']
 neg=subprocess.run([str(lean),'-j1','--root='+str(out),str(negative)],cwd=out,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/'NEGATIVE.log').write_text(neg.stdout);assert neg.returncode!=0 and 'error:' in neg.stdout and 'unsolved goals' in neg.stdout
 result={'status':'PASS_INDEPENDENT_LEAN_INDEX_CONTROLS','source_sha256':sha(source),'cold_receipt_sha256':sha(cold/'REPLAY_RESULT.json'),'lean_control_targets':targets,'false_initial_index_rejected':True,'control_log_sha256':sha(out/'CONTROL.log'),'negative_log_sha256':sha(out/'NEGATIVE.log'),'scope':'Actual trajectory indexing and nonuniform finite-chain controls; not replacement for the general infinite recurrence proof'}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
