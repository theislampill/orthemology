#!/usr/bin/env python3
"""Later Codex-only, local proposal qualification. Not a canonical acceptance gate.

Never edits a repository. Never downloads dependencies. Refuses wrong pins,
changed preimages, existing output directories, compiler errors and empty
artifacts. Uses the preserved 4.19 audit implementation for transitive axioms.
All readbacks still require exact statement review before adoption.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path

LEAN_TAG='leanprover/lean4:v4.19.0'
INPUT_SHA='e4e89e99bd35326e342761d080a9506c8d2b90780fb0a50c6736343ff172ed4c'
MATHLIB='c44e0c8ee63ca166450922a373c7409c5d26b00b'
DEPENDENCIES=['InternalPolymorphism','FiniteBridge','BoundaryResults','EffectsAndDependence','RelationalFragment','AuditSupport']
CANDIDATES=['P01SNReflection','P01OpenSubstitution','P01FiniteEffects','P01CoherentJ']
PREFIX='source-main/experiments/orthemology-v5/source/lean/'

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--mathlib',required=True,type=Path,help='existing exact-profile checkout; not imported by these candidates')
    p.add_argument('--lean',default='lean');p.add_argument('--lake',default='lake')
    a=p.parse_args();root=Path(__file__).resolve().parents[1];out=a.output_dir.resolve()
    if out.exists():p.error('output directory must not exist; stale-artifact reuse refused')
    out.mkdir(parents=True);build=out/'build';build.mkdir();log=out/'raw';log.mkdir()
    env=os.environ.copy();env['ELAN_TOOLCHAIN']=LEAN_TAG;env['LEAN_PATH']=str(build)
    records=[];state={'status':'STARTED','canonical_effects':False,'adoption_credit':False,'new_kernel_claim_in_original_P01':False,'mathlib_used_by_candidate_imports':False}
    def run(label:str,cmd:list[str],cwd:Path)->bytes:
        rec={'label':label,'argv':cmd,'cwd':str(cwd),'ELAN_TOOLCHAIN':env['ELAN_TOOLCHAIN'],'LEAN_PATH':env['LEAN_PATH'],
             'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,check=False,timeout=180);so,se,rc=r.stdout,r.stderr,r.returncode
        except OSError as e:so,se,rc=b'',str(e).encode(),127
        except subprocess.TimeoutExpired as e:so,se,rc=e.stdout or b'',(e.stderr or b'')+b'\nTIMEOUT\n',124
        for ext,b in [('stdout',so),('stderr',se),('exit',f'{rc}\n'.encode())]:(log/f'{label}.{ext}').write_bytes(b)
        rec.update(exit=rc,stdout_sha256=sha(so),stderr_sha256=sha(se));records.append(rec)
        (out/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
        if rc!=0:raise RuntimeError(f'{label} returned {rc}')
        return so
    try:
        packet=root/'inputs'/'Orthemology_Pro_P01_Foundational_Formal.zip';data=packet.read_bytes()
        if sha(data)!=INPUT_SHA or len(data)!=850545:raise RuntimeError('input packet identity mismatch')
        state['input_sha256']=sha(data)
        version=run('lean-version',[a.lean,'--version'],build).decode()
        if not re.search(r'\bversion 4\.19\.0,',version) or 'commit 6caaee842e94' not in version:raise RuntimeError('wrong Lean compiler')
        lake=run('lake-version',[a.lake,'--version'],build).decode()
        if 'Lake version 5.0.0-6caaee8' not in lake or 'Lean version 4.19.0' not in lake:raise RuntimeError('wrong Lake profile')
        rev=run('mathlib-revision',['git','-C',str(a.mathlib.resolve()),'rev-parse','HEAD'],build).decode().strip()
        if rev!=MATHLIB:raise RuntimeError('wrong Mathlib profile pin')
        dirty=run('mathlib-status',['git','-C',str(a.mathlib.resolve()),'status','--porcelain','--untracked-files=no'],build)
        if dirty.strip():raise RuntimeError('modified tracked Mathlib files')
        state.update(lean_version=version.strip(),lake_version=lake.strip(),mathlib_head=rev)
        source_inputs=[]
        with zipfile.ZipFile(packet) as z:
            if z.testzip() is not None:raise RuntimeError('input CRC failure')
            inv={r['packet_path']:r for r in json.loads(z.read('SOURCE_INVENTORY.json'))}
            for name in DEPENDENCIES:
                path=PREFIX+name+'.lean';b=z.read(path);r=inv[path]
                if len(b)!=r['bytes'] or sha(b)!=r['sha256']:raise RuntimeError('source identity mismatch: '+path)
                (build/(name+'.lean')).write_bytes(b);source_inputs.append(r)
        ci=json.loads((root/'proposals'/'CANDIDATE_INVENTORY.json').read_text())
        candidate_rows={Path(r['path']).stem:r for r in ci['files']}
        for name in CANDIDATES:
            r=candidate_rows[name];b=(root/r['path']).read_bytes()
            if sha(b)!=r['sha256'] or len(b)!=r['bytes']:raise RuntimeError('candidate identity mismatch: '+name)
            (build/(name+'.lean')).write_bytes(b)
        (out/'input_bindings.json').write_text(json.dumps({'canonical_preimages':source_inputs,'candidate_inputs':ci},indent=2)+'\n')
        artifact_rows=[]
        for name in DEPENDENCIES+CANDIDATES:
            src=build/(name+'.lean');before=sha(src.read_bytes())
            run('compile-'+name,[a.lean,'-o',name+'.olean',name+'.lean'],build)
            ob=build/(name+'.olean')
            if not ob.is_file() or ob.stat().st_size==0:raise RuntimeError('empty/missing artifact: '+name)
            if sha(src.read_bytes())!=before:raise RuntimeError('source changed during compile: '+name)
            artifact_rows.append({'module':name,'source_sha256':before,'olean_bytes':ob.stat().st_size,'olean_sha256':sha(ob.read_bytes())})
        lines=['import AuditSupport']+['import '+n for n in CANDIDATES]+['set_option pp.universes true','set_option pp.fullNames true']
        for name in ci['theorem_targets']:
            lines += [f'#check {name}',f'#print {name}',f'#print axioms {name}',f'#ortho_audit {name}']
        audit=build/'P01Readbacks.lean';audit.write_text('\n'.join(lines)+'\n')
        raw=run('readbacks',[a.lean,'-o','P01Readbacks.olean','P01Readbacks.lean'],build)
        if not raw.strip():raise RuntimeError('empty declaration/type/axiom readback')
        if 'sorryAx' in raw.decode(errors='replace'):raise RuntimeError('sorryAx in readback')
        for name in ci['theorem_targets']:
            if name.encode() not in raw:raise RuntimeError('missing readback name: '+name)
        ob=build/'P01Readbacks.olean'
        if not ob.is_file() or ob.stat().st_size==0:raise RuntimeError('missing readback artifact')
        artifact_rows.append({'module':'P01Readbacks','source_sha256':sha(audit.read_bytes()),'olean_bytes':ob.stat().st_size,'olean_sha256':sha(ob.read_bytes())})
        (out/'artifacts.json').write_text(json.dumps(artifact_rows,indent=2)+'\n')
        state.update(status='CANDIDATE_COMPILE_AND_AXIOM_PREFLIGHT_PASS_PENDING_EXACT_TYPE_REVIEW',targets=len(ci['theorem_targets']),
            all_targets_transitively_audited=True,canonical_status_change=False,required_next_step='Review every actual printed type against the exact P01 claim and source statement. No full U09/U10/U11 closure follows from these helper lemmas.')
    except Exception as e:
        state.update(status='BLOCKED_OR_FAILED_NO_ACCEPTANCE',error=f'{type(e).__name__}: {e}')
    finally:
        state['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        (out/'QUALIFICATION_RECEIPT.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(state,indent=2));return 0 if state['status'].startswith('CANDIDATE_COMPILE') else 1
if __name__=='__main__':raise SystemExit(main())
