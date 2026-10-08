#!/usr/bin/env python3
"""Out-of-tree P1 replay. No downloads, installation, cache mutation or bootstrap."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode=True
PACKET=Path(__file__).resolve().parent
SOURCE_PIN='d0177de1ebeb8de4ff71898dbccc729ca420c70a50c307f1bacccd6d2c38d43d'
REVIEW_PIN='c55e4f5ae6dba9ce0f517c2b6ab242fdfbad7e4f8951e856cb7487e7fd1c15a0'
PINS={'LEAN_DISTRIBUTION_PIN.json':'6f364a506b2b7bc8934b13ef50b296fd2047d9b7894a2b7f637ad44e4f8e52fb','MATHLIB_SOURCE_PIN.json':'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431','MATHLIB_CACHE_PIN.json':'7dc08ad35391b67f1fb930b1315432ec17321dc6ecfad13b4689f32ade95d2f9'}
MODULES=[('imports','P02A2.ObserverCore'),('src','PythonExprCore'),('src','PythonExprMachine'),('src','PythonExprBounds'),('src','PythonExprSafety'),('controls','P1Required'),('controls','P1Controls'),('controls','P1Axioms'),('reviewer','ReviewerContract')]
MUTANTS=['OperandOrderMutant','ReadyTickMutant','RegisterWidthMutant','PowerFaultMutant']
class Refuse(Exception):pass
def demand(condition,message):
    if not condition:raise Refuse(message)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')
def safe_rel(name):
    q=Path(name)
    demand(not q.is_absolute() and all(x not in ('','.','..') for x in q.parts),'Unsafe manifest member')
    return q
def verify_packet():
    manifest=PACKET/'PUBLIC_MANIFEST.json'; data=json.loads(manifest.read_text());expected=set()
    demand(sha(PACKET/'bindings/ACCEPTED_SOURCE_MANIFEST.json')==SOURCE_PIN,'Accepted source manifest identity mismatch')
    demand(sha(PACKET/'acceptance/ORIGINAL_REVIEW_RECEIPT.json')==REVIEW_PIN,'Accepted review receipt identity mismatch')
    for row in data['files']:
        rel=str(safe_rel(row['path']));demand(rel not in expected,'Duplicate public manifest entry');expected.add(rel)
        p=PACKET/rel
        demand(p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Public payload identity mismatch: '+rel)
    actual={str(p.relative_to(PACKET)) for p in PACKET.rglob('*') if p.is_file()}
    demand(not any(p.is_symlink() for p in PACKET.rglob('*')),'Packet symlink refused')
    demand(actual==expected|{'PUBLIC_MANIFEST.json','PUBLIC_MANIFEST.sha256'},'Unexpected or missing public payload')
    demand((PACKET/'PUBLIC_MANIFEST.sha256').read_text().split()[0]==sha(manifest),'Public manifest sidecar mismatch')
    source=json.loads((PACKET/'bindings/ACCEPTED_SOURCE_MANIFEST.json').read_text())
    review=json.loads((PACKET/'bindings/ACCEPTED_REVIEW_MANIFEST.json').read_text())
    custody=json.loads((PACKET/'CUSTODY_MAP.json').read_text())
    for key,original in [('accepted_source',source),('accepted_review',review)]:
        rows=custody[key];lookup={x['original_path']:x for x in rows}
        demand(len(rows)==len(lookup)==len(original['files']),'Incomplete/duplicate custody inventory')
        for old in original['files']:
            row=lookup.get(old['path']);demand(row is not None and row['original_sha256']==old['sha256'] and row['original_bytes']==old['bytes'],'Original custody identity mismatch')
            if row['disposition']=='preserved':
                q=PACKET/safe_rel(row['public_path']);demand(q.is_file() and sha(q)==old['sha256'],'Preserved custody byte mismatch')
            elif row['disposition']=='derived':
                q=PACKET/safe_rel(row['public_path']);demand(q.is_file() and sha(q)==row['public_sha256'] and bool(row['reason']),'Derived custody mismatch')
            else:demand(row['disposition']=='omitted' and bool(row['reason']),'Unknown custody disposition')
    # Every scientific source and original control remains byte-identical.
    for row in source['files']:
        rel=row['path']
        if rel.startswith(('src/','imports/','controls/')) or rel in ('source/prcodec.py','source_contract.py'):
            demand(sha(PACKET/rel)==row['sha256'],'Scientific/control source drift: '+rel)
    return {'public_manifest_sha256':sha(manifest),'accepted_source_manifest_sha256':SOURCE_PIN,'accepted_review_receipt_sha256':REVIEW_PIN,'public_files':len(expected),'original_source_payloads':len(source['files']),'original_review_payloads':len(review['files'])}
def inventory(base,pin,allow_trace=None):
    expected={r['path'] for r in pin['entries']};seen=set();changed=[]
    demand(len(expected)==len(pin['entries']),'Duplicate dependency entry')
    for root in pin['roots']:
        q=base/root;demand(q.is_dir(),'Missing dependency inventory root')
        for p in ([q] if root else [])+list(q.rglob('*')):seen.add(str(p.relative_to(base)))
    demand(seen==expected,'Dependency inventory missing/extra entries')
    for row in pin['entries']:
        rel=str(safe_rel(row['path']));p=base/rel;kind=row['kind']
        if kind=='directory':ok=p.is_dir() and not p.is_symlink()
        elif kind=='symlink':ok=p.is_symlink() and os.readlink(p)==row['target'] and p.exists() and p.resolve().is_relative_to(base)
        else:
            ok=p.is_file() and not p.is_symlink() and p.stat().st_size==row.get('bytes',row.get('size')) and sha(p)==row['sha256']
            if not ok and allow_trace is not None and rel in allow_trace['allowed_paths']:
                demand(p.is_file() and not p.is_symlink(),'Invalid trace file')
                raw=p.read_bytes();prefix=allow_trace['prefix'];historic=allow_trace['reference_prefix']
                demand(prefix and raw.count(prefix)==1,'Trace relocation must replace exactly one supplied prefix')
                normalized=raw.replace(prefix,historic)
                ok=len(normalized)==row.get('bytes',row.get('size')) and hashlib.sha256(normalized).hexdigest()==row['sha256']
                if ok:changed.append(rel)
        demand(ok,'Dependency identity mismatch: '+rel)
    return {'entries':len(expected),'exact_except_trace_paths':sorted(changed)}
def verify_dependencies(lean,mathlib,prefix,reference_prefix):
    for name,pin in PINS.items():demand(sha(PACKET/'dependencies'/name)==pin,'Dependency pin manifest changed')
    l=json.loads((PACKET/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text())
    c=json.loads((PACKET/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
    s=json.loads((PACKET/'dependencies/MATHLIB_SOURCE_PIN.json').read_text())
    delta=json.loads((PACKET/'dependencies/TRACE_PATH_DELTAS.json').read_text())
    demand(set(delta['allowed_paths'])=={f'.lake/build/lib/lean/Cache/{x}.trace' for x in ['Hashing','IO','Lean','Main','Requests']},'Trace delta scope expanded')
    delta['prefix']=prefix.encode() if prefix else b''
    delta['reference_prefix']=reference_prefix.encode() if reference_prefix else b''
    demand(bool(prefix)==bool(reference_prefix),'Both trace prefixes are required together')
    lr=inventory(lean,l);cr=inventory(mathlib,c,delta)
    for row in s['files']:
        p=mathlib/safe_rel(row['path']);demand(p.is_file() and not p.is_symlink() and p.stat().st_size==row['size'] and sha(p)==row['sha256'],'Dependency source identity mismatch: '+row['path'])
    return {'lean_distribution':lr,'mathlib_cache':cr,'source_records':len(s['files']),'pin_manifests':PINS,'official_precompiled_cache_trusted':True,'proof_dependencies_rebuilt':False}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean-root',type=Path,required=True)
    parser.add_argument('--mathlib-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True,help='A new, nonexistent directory outside all input trees')
    parser.add_argument('--trace-prefix',default='',help='Exact existing prefix in the five relocated cache traces, including trailing slash; comparison only')
    parser.add_argument('--pinned-trace-prefix',default='',help='Reference cache prefix supplied externally; replacement must reproduce exact pinned hash and size')
    parser.add_argument('--verify-only',action='store_true')
    a=parser.parse_args();demand(not sys.flags.optimize,'Optimized verification refused')
    lean=a.lean_root.resolve(strict=True);mathlib=a.mathlib_root.resolve(strict=True)
    # Resolve an absent output through its parent; reject preexisting paths/symlinks.
    demand(not a.output.exists() and not a.output.is_symlink(),'Output must not exist')
    out=a.output.resolve()
    for root in [PACKET,lean,mathlib]:demand(not out.is_relative_to(root) and not root.is_relative_to(out),'Output overlaps an input tree')
    packet=verify_packet();deps=verify_dependencies(lean,mathlib,a.trace_prefix,a.pinned_trace_prefix)
    out.mkdir(parents=True,exist_ok=False)
    write(out/'INPUT_RECEIPT.json',{'status':'PASS_PACKET_AND_DEPENDENCIES',**packet,'dependencies':deps})
    if a.verify_only:print('PASS: exact packet/dependency verification; no compilation requested.');return 0
    replacements=[(str(PACKET),'$PACKET'),(str(out),'$OUTPUT'),(str(lean),'$LEAN_ROOT'),(str(mathlib),'$MATHLIB_ROOT'),(sys.executable,'$PYTHON')]
    def neutral(text):
        for old,new in sorted(replacements,key=lambda x:len(x[0]),reverse=True):text=text.replace(old,new)
        return text
    env={k:v for k,v in os.environ.items() if not k.startswith(('LEAN','LD_'))}
    cache=json.loads((PACKET/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
    build=out/'build';build.mkdir()
    env['LEAN_PATH']=':'.join([str(build)]+[str(mathlib/root) for root in cache['roots']])
    env['PYTHONDONTWRITEBYTECODE']='1';env['PATH']=str(lean/'bin')+os.pathsep+env.get('PATH','')
    results=[]
    def command(name,cmd,expected=0,source=None):
        start=time.monotonic()
        try:
            p=subprocess.run(cmd,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
        except subprocess.TimeoutExpired as error:
            raw=error.stdout or b'';raw=raw.decode(errors='replace') if isinstance(raw,bytes) else raw
            (out/'logs').mkdir(exist_ok=True);(out/'logs'/(name+'.log')).write_text(neutral(raw)+'\nTIMEOUT: NO REJECTION OR SUCCESS CREDIT\n')
            raise Refuse('Bounded command timed out: '+name)
        clean=neutral(p.stdout);log=out/'logs'/(name+'.log');log.parent.mkdir(exist_ok=True);log.write_text(clean)
        rec={'name':name,'expectation':'REJECT' if expected else 'ACCEPT','exit_code':p.returncode,'elapsed_seconds':time.monotonic()-start,'command':[neutral(str(x)) for x in cmd],'source_sha256':sha(source) if source else None,'raw_diagnostic_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'path_neutral_log_sha256':sha(log),'diagnostic_path_substitution_only':True,'wall_limit_seconds':180}
        results.append(rec);write(out/'COMMANDS.json',results)
        demand(p.returncode==expected,'Unexpected command result: '+name)
        if expected:demand("error: tactic 'rfl' failed" in p.stdout and 'unknown module' not in p.stdout and 'file not found' not in p.stdout,'Mutation did not fail at its intended proof')
        else:demand('error:' not in p.stdout and 'sorryAx' not in p.stdout and "declaration uses 'sorry'" not in p.stdout,'Proof admission/error refused: '+name)
        return clean
    for kind,name in MODULES:
        src=PACKET/kind/(name.replace('.','/')+'.lean');obj=build/(name.replace('.','/')+'.olean');obj.parent.mkdir(parents=True,exist_ok=True)
        demand(not obj.exists(),'Cold object collision')
        text=command(name,[str(lean/'bin/lean'),'-j1','--root='+str(PACKET/kind),'-o',str(obj),str(src)],source=src)
        demand(obj.is_file(),'Successful compile omitted object')
        if name in ['P1Axioms','ReviewerContract']:
            lines=[x for x in text.splitlines() if 'depends on axioms:' in x or 'does not depend on any axioms' in x]
            demand(len(lines)==(37 if name=='P1Axioms' else 4),'Axiom audit census mismatch')
            for line in lines:
                if 'depends on axioms:' in line:demand(set(line.split('[',1)[1].rstrip(']').split(', '))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom refused')
    for name in MUTANTS:
        src=PACKET/'controls'/(name+'.lean');obj=build/(name+'.olean')
        command(name,[str(lean/'bin/lean'),'-j1','--root='+str(PACKET/'controls'),'-o',str(obj),str(src)],expected=1,source=src)
        demand(not obj.exists(),'Rejected mutant emitted an object')
    for name,rel in [('SourceShape','source_contract.py'),('SourceContract','controls/test_source_contract.py'),('PythonEdges','controls/check_python_edges.py')]:
        command(name,[sys.executable,'-B',str(PACKET/rel)],source=PACKET/rel)
    # Reproduce the exact original independent control bytes in an output-only
    # compatibility layout. Both literal copies derive from the bound source;
    # historical independent-custody evidence is the retained original receipt.
    mirror=out/'control-layout';control=mirror/'tranche9/reviews/python-runtime-refinement/controls/independent_source_controls.py'
    control.parent.mkdir(parents=True);shutil.copyfile(PACKET/'reviewer/independent_source_controls.py',control)
    for rel in ['tranche9/baseline/components/Eighth_Literal_Runtime_Counterexamples_20261002/prcodec.py','tranche9/baseline/components/Semantic_Control_Independent_Review_20261002/literal-snapshot/prcodec.py']:
        dest=mirror/rel;dest.parent.mkdir(parents=True);shutil.copyfile(PACKET/'source/prcodec.py',dest)
    (control.parents[1]/'evidence').mkdir()
    command('IndependentPythonControls',[sys.executable,'-B',str(control)],source=PACKET/'reviewer/independent_source_controls.py')
    evidence=control.parents[1]/'evidence/INDEPENDENT_SOURCE_CONTROLS.json';obs=json.loads(evidence.read_text())
    demand(obs['differential_cases']==266760 and obs['seeded_boundary_cases']==1593 and len(obs['mutation_controls'])==18 and all(x['detected'] for x in obs['mutation_controls']),'Independent control census mismatch')
    expected={name.replace('.','/')+'.olean' for _,name in MODULES}
    demand({str(x.relative_to(build)) for x in build.rglob('*.olean')}==expected,'Unexpected custom object census')
    demand(not any(x.is_symlink() for x in build.rglob('*')),'Custom object symlink refused')
    # Final packet identity check detects any accidental source/control mutation.
    demand(verify_packet()==packet,'Packet changed during replay')
    report={'status':'PASS_PORTABLE_P1_REPLAY','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**packet,'dependencies':deps,'compiled_scientific_modules':4,'fresh_observer_dependency':True,'public_axiom_checks':37,'reviewer_universal_consumers':4,'author_lean_controls':21,'reviewer_lean_controls':28,'rejected_machine_mutations':4,'python_differential_cases':266760,'python_seeded_boundary_cases':1593,'python_behavior_mutants':18,'new_resource_inconclusive_runs':False,'author_custom_objects_reused':False,'no_input_tree_mutation':True,'control_layout_literal_copies':'Two byte-identical output-only copies of the bound input; no new independent provenance claim','scope':'Expression algorithm-model correspondence only; frontend/CPython/host, parser/statement/full runner remain residual. No P2/P3 work.','commands_sha256':sha(out/'COMMANDS.json'),'objects':[{'path':str(x.relative_to(build)),'sha256':sha(x)} for x in sorted(build.rglob('*.olean'))]}
    write(out/'REPLAY_RECEIPT.json',report)
    print(json.dumps({k:report[k] for k in ['status','public_manifest_sha256','compiled_scientific_modules','public_axiom_checks','rejected_machine_mutations']},indent=2))
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (Refuse,OSError,ValueError,KeyError) as error:
        # Do not leak machine-specific paths into the portable terminal summary.
        if isinstance(error,Refuse):print('REFUSED: '+str(error),file=sys.stderr)
        else:print('REFUSED: input or verification failure ('+type(error).__name__+')',file=sys.stderr)
        raise SystemExit(2)
