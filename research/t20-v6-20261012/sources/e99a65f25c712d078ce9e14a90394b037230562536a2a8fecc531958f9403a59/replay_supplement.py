"""Run only a named bounded control in a disposable declared-source alias layout."""
from pathlib import Path
import json,hashlib,shutil,tempfile,subprocess,sys,argparse
from verify_supplement import main as verify, path
ROOT=Path(__file__).resolve().parents[1]
SUITES={
 'early-operations':{'script':'t20-closure-audit-20261011/early_operations/CONTROL_CHECK.py','modes':[[],['-O']],'scope':'Fresh finite rational interface diagnostics; not inherited optimizer/kernel replay.'},
 'foundations-custody':{'script':'t20-closure-audit-20261011/early_foundations/verify.py','modes':[[]],'scope':'Normal-only author source hashes, row accounting and stored flag checks. Does not reconstruct or independently verify the mathematical application; optimized asserts would supply no evidence.'},
 'later-accounting':{'script':'t20-closure-audit-20261011/review_later/verify_review.py','modes':[[],['-O']],'full_v4_layout':True,'scope':'Reviewer-owned exact 262-row accounting, T12 source identity and immutable v4 checks; not a new theorem or kernel replay.'},
 'independent-foundations-operations':{'script':'t20-closure-audit-20261011/review_foundations_operations/independent_check.py','modes':[[],['-O']],'scope':'Reviewer-owned explicit-exception controls at their declared source/application scope; no universal proof or kernel credit.'}
}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--list',action='store_true');parser.add_argument('--suite',choices=sorted(SUITES));args=parser.parse_args()
 if args.list:print(json.dumps(SUITES,indent=2));return
 if not args.suite:parser.error('--suite required')
 import contextlib,io
 with contextlib.redirect_stdout(io.StringIO()):verify()
 data=json.loads((ROOT/'historical_coverage/SOURCE_PATH_RESOLVER.json').read_text());spec=SUITES[args.suite];routes={}
 for row in data['routes']:
  alias=row['workspace_alias'];path(alias)
  if alias in routes and routes[alias]['sha256']!=row['sha256']:raise RuntimeError('conflicting source alias')
  routes[alias]=row
 if spec['script'] not in routes:raise RuntimeError('Selected suite is not yet available; review still pending')
 results=[]
 with tempfile.TemporaryDirectory(prefix='t20-v5-supplement-') as tmp:
  work=Path(tmp)
  for alias,row in routes.items():
   dest=work/alias;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path(row['included_path']),dest)
  if spec.get('full_v4_layout'):
   dest=work/'t20-consolidation-20261011/projection/package-v4'
   shutil.copytree(ROOT/'package',dest,dirs_exist_ok=True)
  for mode in spec['modes']:
   flags=['-B',*mode,spec['script']];r=subprocess.run([sys.executable,*flags],cwd=work,capture_output=True,text=True,timeout=300)
   output=r.stdout+r.stderr
   # Raw private temporary tracebacks never enter the public successful receipt.
   if r.returncode:raise RuntimeError('Control failed; exit '+str(r.returncode)+'; '+r.stderr.replace(str(work),'<DISPOSABLE_SOURCE_LAYOUT>'))
   results.append({'arguments':flags,'exit_code':r.returncode,'output_sha256':hashlib.sha256(output.encode()).hexdigest(),'output':output})
 print(json.dumps({'status':'PASS','suite':args.suite,'scope':spec['scope'],'python':sys.version.split()[0],'script_sha256':routes[spec['script']]['sha256'],'results':results},indent=2))
if __name__=='__main__':main()
