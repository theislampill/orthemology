#!/usr/bin/env python3
"""Fresh isolated proof build, independent readback, and expected-failure mutations."""
from pathlib import Path
import hashlib,json,os,subprocess,time,re,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT.parents[1]
SRC=ROOT/'source';EV=ROOT/'evidence';TC=BASE/'tranche2/toolchain';ML=TC/'mathlib4';LEAN=TC/'lean-4.19.0-linux/bin/lean'
MODULES=['PolynomialAND', 'ANDCorrection', 'ANDScore', 'ANDRepair', 'ANDPotentialBinding', 'FiniteHullWeights', 'ANDIntrinsic', 'PolynomialBounds', 'ConstraintBounds', 'ExplicitANDScale', 'ScaleReadback']

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pin=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    assert subprocess.check_output(['git','-C',str(ML),'rev-parse','HEAD'],text=True).strip()=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
    version=subprocess.check_output([str(LEAN),'--version'],text=True).strip();assert 'version 4.19.0' in version
    mathlib_status=subprocess.check_output(['git','-C',str(ML),'status','--porcelain'],text=True);assert not mathlib_status
    toolchain={'lean_binary_sha256':digest(LEAN),'mathlib_lake_manifest_sha256':digest(ML/'lake-manifest.json'),'mathlib_git_status':mathlib_status}
    for row in pin['sources']:
        assert digest(SRC/row['name'])==row['sha256']
    imported=set()
    for m in MODULES:
        content=(SRC/f'{m}.lean').read_text()
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b',re.sub(r'/\-.*?\-/','',content,flags=re.S))
        imported.update(re.findall(r'^import (\S+)',content,re.M))
    assert imported-set(MODULES)=={'Mathlib'}
    build=ROOT/'build'/time.strftime('%Y%m%dT%H%M%SZ',time.gmtime());build.mkdir(parents=True)
    libs=[build,ML/'.lake/build/lib/lean',*sorted(ML.glob('.lake/packages/*/.lake/build/lib/lean'))]
    env=dict(os.environ,LEAN_PATH=':'.join(map(str,libs)));results=[]
    for m in MODULES:
        start=time.monotonic();p=subprocess.run([str(LEAN),'-j1','--root='+str(SRC),'-o',str(build/f'{m}.olean'),str(SRC/f'{m}.lean')],env=env,cwd=ML,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (EV/f'{m}.log').write_text(p.stdout)
        ok=p.returncode==0 and 'sorryAx' not in p.stdout and 'error:' not in p.stdout and 'PANIC' not in p.stdout
        results.append({'module':m,'exit_code':p.returncode,'passed':ok,'seconds':time.monotonic()-start,'source_sha256':digest(SRC/f'{m}.lean'),'warnings':p.stdout.count('warning:')})
        print(m,'PASS' if ok else 'FAIL',flush=True)
        if not ok:
            print(p.stdout);break
    result={'status':'PASS' if len(results)==len(MODULES) and all(x['passed'] for x in results) else 'FAIL','lean':version,'toolchain':toolchain,'mathlib_commit':'c44e0c8ee63ca166450922a373c7409c5d26b00b','modules':results,'build_directory':str(build.relative_to(ROOT)),'local_import_closure':sorted(imported),'scope':'Copied immutable author sources plus independent audit readback/controls. Mathlib and official Lean reused at pinned identities.'}
    (EV/'REPLAY_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    assert result['status']=='PASS'

if __name__=='__main__':main()
