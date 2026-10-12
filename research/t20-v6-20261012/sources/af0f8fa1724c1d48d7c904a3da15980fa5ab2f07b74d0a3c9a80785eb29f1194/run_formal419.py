#!/usr/bin/env python3
"""Fresh native Lean4.19 graph/VCT build and raw audits. Downloads nothing.

A zero exit means build/readback checks passed, pending independent type and
compiler-origin review. It is not automatic canonical Q1f/adoption credit.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,platform,re,subprocess,sys

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def identity(p:Path)->dict:
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lean',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=Path(__file__).resolve().parents[1];out=a.out.expanduser().absolute()
    if out.exists():raise SystemExit('Fresh output directory required; refusing to reuse artifacts')
    out.mkdir(parents=True);lean=a.lean.expanduser().resolve();expected=json.loads((root/'formal/EXPECTED_TARGETS.json').read_text())
    env=os.environ.copy();env['LEAN_PATH']=str(out);env.pop('LEAN_SYSROOT',None)
    receipt={'scope':'NEW_P03_GRAPH_AND_GUARDED_VCT_PROPOSAL','status':'STARTED','started_utc':datetime.now(timezone.utc).isoformat(),
      'python':sys.version,'platform':platform.platform(),'lean':str(lean),'LEAN_PATH':env['LEAN_PATH'],
      'commands':[],'targets':expected['targets'],'observed_theorem_targets':0,'observed_axiom_readbacks':0,
      'artifacts':{},'source_identities':{},'kernel_acceptance_credit':False,'canonical_effect':False,
      'compiler_origin':'Native executable SHA and prefix recorded; independent official-origin verification remains required. Version text alone is not sufficient.'}
    def save():
        (out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    def run(label,argv):
        begin=datetime.now(timezone.utc).isoformat()
        try:p=subprocess.run(argv,cwd=out,env=env,capture_output=True,timeout=120,check=False);code=p.returncode;so=p.stdout;se=p.stderr
        except FileNotFoundError as e:code=127;so=b'';se=(repr(e)+'\n').encode()
        except subprocess.TimeoutExpired as e:code=124;so=e.stdout or b'';se=(e.stderr or b'')+b'\nTIMEOUT\n'
        (out/(label+'.stdout.bin')).write_bytes(so);(out/(label+'.stderr.bin')).write_bytes(se)
        receipt['commands'].append({'label':label,'argv':argv,'cwd':str(out),'started_utc':begin,'exit_code':code,
          'stdout_bytes':len(so),'stdout_sha256':sha(so),'stderr_bytes':len(se),'stderr_sha256':sha(se)})
        save()
        if code:raise RuntimeError(f'{label} nonzero exit {code}')
        if re.search(rb'\bsorryAx\b|declaration uses .?sorry|\berror:',so+se,re.I):raise RuntimeError(f'{label}: forbidden error/proof marker')
        return so,se
    try:
        if not lean.is_file() or not os.access(lean,os.X_OK):
            receipt['status']='HOST_EXECUTION_BLOCKED';receipt['reason']='Exact native compiler file unavailable';save();print(json.dumps(receipt,indent=2));return 2
        receipt['native_executable']=identity(lean)
        with lean.open('rb') as f:header=f.read(4)
        if header!=b'\x7fELF':raise RuntimeError('This Linux packet requires the native ELF compiler, not an output-spoofing shell wrapper')
        so,se=run('version',[str(lean),'--version']);text=(so+se).decode(errors='replace')
        if not re.search(r'\bversion 4\.19\.0\b',text) or '6caaee842e94' not in text:raise RuntimeError('Wrong compiler/version; require Lean4.19.0 commit6caaee842e94')
        so,se=run('prefix',[str(lean),'--print-prefix']);prefix=Path(so.decode().strip());init=prefix/'lib/lean/Init.olean'
        if not init.is_file() or not init.stat().st_size:raise RuntimeError('Native core Init artifact missing at reported prefix')
        receipt['prefix']=str(prefix);receipt['core_init_artifact']=identity(init)
        for name,binding in expected['source_sha256'].items():
            source=root/'formal'/name;b=source.read_bytes()
            if sha(b)!=binding:raise RuntimeError('Frozen source mismatch '+name)
            (out/name).write_bytes(b);receipt['source_identities'][name]={'bytes':len(b),'sha256':sha(b)}
        for module in ['P03GuardedGraph','P03GuardedVCT','P03Audit']:
            run('build-'+module,[str(lean),'-o',module+'.olean',module+'.lean'])
            p=out/(module+'.olean')
            if not p.is_file() or not p.stat().st_size:raise RuntimeError('Missing/empty '+p.name)
            receipt['artifacts'][p.name]=identity(p);save()
        audit=((out/'build-P03Audit.stdout.bin').read_bytes()+(out/'build-P03Audit.stderr.bin').read_bytes()).decode(errors='replace')
        for target in expected['targets']:
            if f"'{target}' does not depend on any axioms" not in audit:raise RuntimeError('Missing or unexpected axiom readback '+target)
            if not re.search(r'(?m)^@?'+re.escape(target)+r'(?:\.\{[^}]*\})?\s*:',audit):raise RuntimeError('Missing type readback '+target)
        receipt['observed_theorem_targets']=len(expected['targets']);receipt['observed_axiom_readbacks']=len(expected['targets'])
        receipt['status']='BUILD_READBACK_PASS_PENDING_INDEPENDENT_TYPE_AND_ORIGIN_REVIEW'
        receipt['note']='Review actual #check/#print types, the restated main-type example and all model definitions. No historical identity, optional TRC or repository adoption follows.'
        save();print(json.dumps(receipt,indent=2));return 0
    except Exception as e:
        receipt['status']='NOT_ACCEPTED';receipt['error']=repr(e);save();print(json.dumps(receipt,indent=2));return 1
if __name__=='__main__':raise SystemExit(main())
