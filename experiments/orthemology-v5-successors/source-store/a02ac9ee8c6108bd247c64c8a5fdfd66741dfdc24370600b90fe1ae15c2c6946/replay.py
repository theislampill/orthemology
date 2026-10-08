#!/usr/bin/env python3
"""Portable exact-source selector replay. All generated files are out of tree."""
from pathlib import Path
import argparse, datetime, importlib.util, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
from verify_artifact import verify, require, digest, json_read, records, check_row, census, unpack_checked_zip

ROOT = Path(__file__).resolve().parent
ALLOWED_AXIOMS = {'propext','Classical.choice','Quot.sound'}
LITERAL_MODULES = ['LiteralSelectorObstruction','LiteralSelectorFamily','LiteralRuntimeCounterexample']
ORDER = ['LiteralSelectorObstruction','LiteralSelectorFamily','FiniteRadixNormalForm',
         'SelectorTableNormalForm','A1AxiomReadback','SelectorCallDomains',
         'SelectorSemanticTransport','A2AxiomReadback','LiteralRuntimeCounterexample',
         'CertifiedSelectorFamily','A3AxiomReadback','ReviewerRawContract',
         'ReviewerPaddingBoundary','ReviewerTransportBoundaries','ReviewerSuppliedConsumer']
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2)+'\n')
def check_core_cache(output, sources, manifest_sha):
    output = Path(output)
    result = json_read(output/'RESULT.json')
    require(result['status']=='COMPLETED_FRESH_REPLAY' and result['source_manifest_sha256']==manifest_sha,
            'Core result does not bind a completed exact replay')
    runs = {}
    readbacks = []
    for row in result['runs']:
        if row.get('suite') != 'runtime':
            continue
        name = row['module']
        if name=='RuntimeReadback':
            readbacks.append(row)
            continue
        require(name not in runs, 'Duplicate core module record')
        runs[name]=row
    require(set(runs)==set(sources) and len(runs)==167, 'Core module census mismatch')
    build = output/'runtime/build'
    all_files = census(build)
    expected = {name.replace('.','/')+'.olean' for name in runs}
    require(all_files==expected, 'Unexpected/missing core object or auxiliary file')
    for name,row in runs.items():
        require(row['exit_code']==0 and row['source_sha256']==sources[name]['sha256'], 'Core source/result mismatch')
        require(digest(build/(name.replace('.','/')+'.olean'))==row['object_sha256'], 'Core object digest mismatch')
    require(len(readbacks)==1 and readbacks[0]['exit_code']==0, 'Core endpoint readback missing')
    require(result.get('runtime',{}).get('axiom_readbacks')==13, 'Core endpoint audit census mismatch')
    return {'receipt_sha256':digest(output/'RESULT.json'),'objects_verified':167,
            'source_object_binding_only':True,'new_kernel_checks_from_this_reuse':0}

def audits(text, expected):
    rows = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text)
    rows += [(n,'') for n in re.findall(r"'([^']+)' does not depend on any axioms",text)]
    require(len(rows)==len(expected) and {n for n,_ in rows}==set(expected), 'Axiom declaration census mismatch')
    for name,block in rows:
        require({x.strip() for x in block.split(',') if x.strip()} <= ALLOWED_AXIOMS, 'Unapproved axiom: '+name)
    return len(rows)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['core-zip','literal-zip','out']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--expected-manifest-sha256',required=True)
    p.add_argument('--core-output',type=Path,help='Optional trusted completed exact core replay; checked, never copied or modified')
    p.add_argument('--lean-bin',type=Path)
    p.add_argument('--mathlib',type=Path)
    p.add_argument('--mathlib-archive',type=Path)
    p.add_argument('--verify-only',action='store_true')
    a = p.parse_args()
    artifact = verify(ROOT,a.expected_manifest_sha256)
    out = a.out.resolve()
    require(not out.exists(), 'Output must be absent')
    protected = [ROOT]
    for x in [a.core_output,a.mathlib,a.lean_bin]:
        if x is not None:
            protected.append(x.resolve())
    for x in protected:
        require(not out.is_relative_to(x) and not x.is_relative_to(out), 'Output overlaps a protected input')
    if not a.verify_only:
        require(a.lean_bin is not None and a.mathlib is not None, 'Proof replay needs --lean-bin and --mathlib')
    packets = {r['id']:r for r in json_read(ROOT/'EXTERNAL_PACKETS.json')['packets']}
    require(set(packets)=={'core','literal'}, 'External packet census mismatch')
    # Hash both archives before creating output. No downloads, opaque selector
    # evaluation, historical mutant probe, or native code generation occurs.
    for key,path in [('core',a.core_zip),('literal',a.literal_zip)]:
        require(digest(path)==packets[key]['sha256'] and path.stat().st_size==packets[key]['bytes'], 'External packet identity mismatch: '+key)
    out.mkdir(parents=True)
    result = {'status':'RUNNING','started_utc':utc(),'artifact':artifact,
              'driver_sha256':digest(__file__),'external_packets':packets,
              'historical_probes_retried':False,'native_codegen_claimed':False,
              'heartbeat_flags_added':False,'parallel_lean_processes':1,
              'wall_clock_per_module_seconds':180,'runs':[]}
    save = lambda:write(out/'RESULT.json',result)
    save()
    try:
        roots = {}
        for key,path in [('core',a.core_zip),('literal',a.literal_zip)]:
            r = packets[key]
            roots[key]=unpack_checked_zip(path,out/'dependencies'/key,r['sha256'],r['bytes'],r['members'])
            require(digest(roots[key]/'SOURCE_MANIFEST.json')==r['source_manifest_sha256'], 'External source manifest mismatch')
        core = roots['core']; literal=roots['literal']
        cm = json_read(core/'SOURCE_MANIFEST.json')
        for row in cm['sources']:
            check_row(core,row['path'],row)
        core_sources={r['path'][12:-5].replace('/','.'):r for r in cm['sources'] if r['path'].startswith('runtime/src/')}
        require(len(core_sources)==167, 'Core scientific source census mismatch')
        lm = records(json_read(literal/'SOURCE_MANIFEST.json')['files'])
        for row in lm.values():
            check_row(literal,row['path'],row)
        result['required_scientific_dependency_sources_verified']=170
        if a.verify_only:
            result.update(status='PASS_ARTIFACT_AND_EXTERNAL_SOURCE_BINDING_ONLY',new_kernel_check=False,finished_utc=utc())
            save(); print(json.dumps({'status':result['status'],'new_kernel_check':False})); return
        lean = (a.lean_bin/'lean').resolve(); math=a.mathlib.resolve()
        pins = json_read(core/'DEPENDENCY_PINS.json')
        require(digest(lean)==pins['lean_binary_sha256'], 'Pinned Lean binary mismatch')
        require(subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version'], 'Lean version mismatch')
        spec=importlib.util.spec_from_file_location('selector_external_dependency_identity',core/'verify_dependency_identity.py')
        identity=importlib.util.module_from_spec(spec);spec.loader.exec_module(identity)
        result['dependency_identity']=identity.verify_dependencies(math,a.mathlib_archive,pins)
        # Strip optimization only for exact historical scripts that intentionally
        # reject it or use assertions. The public guards themselves remain active
        # when this wrapper is invoked with python -O.
        env=dict(os.environ)
        for key in ['LEAN_SRC_PATH','LEAN_PATH','PYTHONOPTIMIZE']:
            env.pop(key,None)
        co=a.core_output.resolve() if a.core_output else out/'fresh-core'
        if a.core_output is None:
            command=[sys.executable,'-B',str(core/'replay.py'),'--mode','runtime','--lean-bin',str(lean.parent),
                     '--mathlib',str(math),'--out',str(co)]
            if a.mathlib_archive:
                command += ['--mathlib-archive',str(a.mathlib_archive.resolve())]
            with (out/'core-replay.log').open('w') as f:
                q=subprocess.run(command,env=env,stdout=f,stderr=subprocess.STDOUT)
            require(q.returncode==0, 'Fresh core driver failed; inspect its separate receipt')
        result['core_cache_binding']=check_core_cache(co,core_sources,packets['core']['source_manifest_sha256'])
        result['core_rebuilt_by_this_invocation']=a.core_output is None
        result['official_external_cache_trusted']=True
        build=out/'build';build.mkdir()
        logs=out/'logs';logs.mkdir()
        libs=[math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
        require((libs[0]/'Mathlib.olean').is_file(), 'Official Mathlib cache missing')
        env['LEAN_PATH']=os.pathsep.join(map(str,[build,co/'runtime/build']+libs))
        bindings=json_read(ROOT/'PROOF_SOURCE_BINDINGS.json')['files']
        sources={r['module']:(ROOT/r['path'],r['sha256']) for r in bindings}
        for name in LITERAL_MODULES:
            row=lm['src/'+name+'.lean'];sources[name]=(literal/row['path'],row['sha256'])
        require(set(sources)==set(ORDER), 'Replay module census mismatch')
        axiom_count=0
        for name in ORDER:
            src,expected=sources[name]
            require(digest(src)==expected, 'Source changed before compilation')
            obj=build/(name+'.olean')
            command=[str(lean),'-j1','--root='+str(src.parent),'-o',str(obj),str(src)]
            start=time.monotonic()
            try:
                q=subprocess.run(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
                code=q.returncode;text=q.stdout
            except subprocess.TimeoutExpired as ex:
                text=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT_180_SECONDS\n';code=None
            log=logs/(name+'.log');log.write_text(text)
            row={'module':name,'source_sha256':expected,'exit_code':code,'elapsed_seconds':round(time.monotonic()-start,3),
                 'log':'logs/'+name+'.log','log_sha256':digest(log)}
            if obj.exists():row['object_sha256']=digest(obj)
            result['runs'].append(row);save();print(name,code,flush=True)
            require(code==0 and 'error:' not in text and "declaration uses 'sorry'" not in text, 'Proof stage failed: '+name)
            if name in ['A1AxiomReadback','A2AxiomReadback','A3AxiomReadback']:
                stage=name[:2]
                manifest=json_read(ROOT/f'originals/{stage}/SOURCE_MANIFEST.json')
                axiom_count += audits(text,[d['name'] for d in manifest['declarations']])
            elif name.startswith('Reviewer'):
                prior=json_read(ROOT/f'evidence/{name}_RECEIPT_PROJECTION.json')
                axiom_count += audits(text,prior['axioms'])
        require(axiom_count==183, 'Expected 138 scientific and 45 reviewer axiom checks')
        # Run unchanged finite controls in a disposable out-of-tree layout.
        finite=out/'finite-controls';finite.mkdir();(finite/'evidence').mkdir()
        shutil.copyfile(ROOT/'controls/finite_controls.py',finite/'finite_controls.py')
        with (finite/'stdout.log').open('w') as f:
            q=subprocess.run([sys.executable,'-B',str(finite/'finite_controls.py')],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=60)
        require(q.returncode==0 and json_read(finite/'evidence/FINITE_CONTROLS.json')==json_read(ROOT/'evidence/FINITE_CONTROLS.json'), 'Finite controls mismatch')
        guards=out/'original-census-controls';guards.mkdir();(guards/'snapshot').mkdir();(guards/'evidence').mkdir()
        shutil.copyfile(ROOT/'controls/check_original_replay_guards.py',guards/'check_replay_guards.py')
        shutil.copyfile(ROOT/'historical/A2_replay.py',guards/'snapshot/replay.py')
        with (guards/'stdout.log').open('w') as f:
            q=subprocess.run([sys.executable,'-B',str(guards/'check_replay_guards.py')],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=30)
        gr=json_read(guards/'evidence/REPLAY_GUARDS.json')
        require(q.returncode==0 and gr['status']=='PASS_FROZEN_CENSUS_HELPER_CONTROLS' and len(gr['cases'])==6, 'Original guard controls failed')
        verify(ROOT,a.expected_manifest_sha256)
        check_core_cache(co,core_sources,packets['core']['source_manifest_sha256'])
        result.update(status='PASS_FRESH_PUBLIC_SELECTOR_AND_REVIEWER_REPLAY',finished_utc=utc(),
                      fresh_modules=15,scientific_axiom_checks=138,reviewer_axiom_checks=45,
                      finite_controls_passed=True,original_census_controls_passed=6)
        save()
    except Exception as ex:
        result.update(status='FAILED_OR_RESOURCE_INCONCLUSIVE',finished_utc=utc(),error=str(ex))
        save();raise
if __name__=='__main__':
    main()
