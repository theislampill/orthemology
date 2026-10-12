#!/usr/bin/env python3
"""Compose qualified global89 and SCC3 objects, then freshly check the SCC iff and probes."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, subprocess, sys
sys.dont_write_bytecode = True
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p,x: p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
p = argparse.ArgumentParser(description=__doc__)
for arg in ('out','environment','global-review','scc-qualification','scc-review'):
    p.add_argument('--'+arg,type=Path,required=True)
a = p.parse_args()
base = Path(__file__).resolve().parent
source = base/'source-snapshot'
sys.path.insert(0,str(source/'tooling'))
from portable_core import verify,verify_pins,verify_official,check_source,check_diagnostics,parse_readback
identity = verify(source)
assert identity['manifest_sha256']=='77978694afc11e092edf2587fb049329cac3f8b6ae2ce7511a6e97d3dff99194'
suite = json.loads((source/'replay/SUITES.json').read_text())['suites'][0]
pins = json.loads((source/'replay/DEPENDENCY_PINS.json').read_text())
by = {r['module']:r for r in suite['modules']}
lean,libs,version,checks = verify_pins(a.environment/'toolchain/lean-4.19.0-linux/bin',a.environment/'mathlib4',pins,set(by))
official = verify_official(source,lean.parent,a.environment/'mathlib4',pins,[suite])
qualified = [
    ('global89',a.global_review/'cold-v1/REPLAY_RESULT.json',a.global_review/'candidate-v1',a.global_review/'cold-v1/global_parity_controller/build','384f5a5feddbad0c1588fb9b482d587592b85f134370b86d97d090b8a0da31a9',89),
    ('accepted_scc',a.scc_qualification/'author-cold-v1/REPLAY_RESULT.json',a.scc_qualification/'candidate-v1',a.scc_qualification/'author-cold-v1/scc_region_integration/build','e05f7fcc0ee8badbd6990887309c77f28178f5615bc0607706115f29855759a7',70)]
catalog = {}
receipts = []
for tag,receipt,packet,build,manifest,count in qualified:
    q = json.loads(receipt.read_text())
    assert q['status']=='PASS' and q['fresh_custom_objects']==count
    assert q['input_manifest_sha256']==manifest==sha(packet/'MASTER_MANIFEST.json')
    assert q['lean_sha256']==sha(lean)
    receipts.append({'tag':tag,'receipt_path':str(receipt.resolve()),'receipt_sha256':sha(receipt),'source_manifest_sha256':manifest,'fresh_objects':count})
    for row in q['suites'][0]['modules']:
        catalog.setdefault(row['module'],(tag,row,packet,build))
scc_seal = json.loads((a.scc_review/'DELIVERY_SEAL.json').read_text())
assert scc_seal['sha256']=='883693593b423984fd95a09426a00b03cba9beb740d24b0a7a0c991806ba3882'
scc_result_path = a.scc_review/'portable-targeted-pass/RESULT.json'
scc_result = json.loads(scc_result_path.read_text())
assert scc_result['status']=='PASS_SCOPED_SCC_REGION_SUBSTITUTION'
accepted = {x['module']:x for x in scc_result['source_bindings']}
out = a.out.resolve()
assert not out.exists() and not out.is_relative_to(source)
out.mkdir(parents=True)
for name in ('dependencies','build','source','logs'):(out/name).mkdir()
official_rows = {r['module']:r for r in json.loads((source/'replay/OFFICIAL_IMPORTS.json').read_text())['imports']}
keys,bindings = {},[]
for mod in suite['module_order']:
    row = by[mod]
    deps = [{'module':i,'binding':keys[i] if i in by else official_rows[i]} for i in row['imports']]
    key = hashlib.sha256(json.dumps({'module':mod,'source':row['sha256'],'deps':deps,'pins':pins,'compiler_flags':['-j1','--root=isolated-suite-source']},sort_keys=True).encode()).hexdigest()
    keys[mod]=key
    assert sha(source/row['source'])==row['sha256']
    if mod=='SCCGlobalParityIff':continue
    tag,previous,packet,build = catalog[mod]
    assert previous['status']=='FRESH_COMPILE' and previous['exit']==0
    assert previous['source_sha256']==row['sha256']==sha(packet/previous['source'])
    assert previous['transitive_source_fingerprint']==key
    rel=Path(mod.replace('.','/')+'.olean')
    obj=build/rel
    assert sha(obj)==previous['olean_sha256']
    if tag=='accepted_scc':
        assert accepted[mod]['source_sha256']==row['sha256']
        assert accepted[mod]['qualified_olean_sha256']==sha(obj)
    dest=out/'dependencies'/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(obj.read_bytes())
    bindings.append({'module':mod,'qualification':tag,'source_sha256':row['sha256'],'object_sha256':sha(obj),'transitive_source_fingerprint':key})
assert len(bindings)==92
assert sum(r['qualification']=='global89' for r in bindings)==89
receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Compositional: 89 source/object/fingerprint-bound independent global cold objects and 3 accepted SCC objects; one fresh author corollary and one fresh reviewer probe module. Not a fresh93-module closure.',
    'input_manifest_sha256':identity['manifest_sha256'],'qualified_receipts':receipts,'accepted_scc_review_result_sha256':sha(scc_result_path),
    'lean_sha256':sha(lean),'lean_version':version,'dependency_checks':checks,'official_import_ownership':official,'dependencies':bindings,'fresh_modules':[]}
write(out/'REPLAY_RESULT.json',receipt)
env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[out/'build',out/'dependencies']+libs))
try:
    for name,path in [('SCCGlobalParityIff',source/'src/SCCGlobalParityIff.lean'),('IndependentSCCIffProbe',base/'probes/IndependentSCCIffProbe.lean')]:
        check_source(path.read_text());src=out/'source'/(name+'.lean');src.write_bytes(path.read_bytes())
        run=subprocess.run([str(lean),'-j1','--root='+str(out/'source'),'-o',str(out/'build'/(name+'.olean')),str(src)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=out/'logs'/(name+'.log');log.write_text(run.stdout)
        receipt['fresh_modules'].append({'module':name,'source_sha256':sha(src),'exit':run.returncode,'log_sha256':sha(log),'object_sha256':sha(out/'build'/(name+'.olean')) if run.returncode==0 else None})
        write(out/'REPLAY_RESULT.json',receipt);print(name,run.returncode,flush=True)
        assert run.returncode==0,run.stdout;check_diagnostics(run.stdout)
    runtime=base/'probes/RuntimeSCCControls.lean'
    run=subprocess.run([str(lean),'-j1','--root='+str(runtime.parent),str(runtime)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=out/'logs/RuntimeSCCControls.log';log.write_text(run.stdout)
    assert run.returncode==0,run.stdout
    assert run.stdout.strip().splitlines()==['2','0','0'],run.stdout
    receipt['runtime_controls']={'exit':run.returncode,'source_sha256':sha(runtime),'log_sha256':sha(log),'outputs':[2,0,0],'scope':'Direct public SCC evaluation on three finite controls; no runtime complexity or proof credit'}
    probes=['public_root_is_scc_recursion','public_stage_calls_scc_target','accepted_witness_is_lawful','accepted_witness_has_actual_parity','accepted_witness_unit_seed_irrelevant','arbitrary_seed_policy_enters_public_scc_region','empty_support_public_rejects','coin_public_acceptance_yields_common_witness','identical_rows_public_rejection_rules_out_common_witness']
    targets=suite['targets']+['IndependentSCCIffReview.'+n for n in probes]
    audit=out/'source/IndependentReadback.lean'
    audit.write_text('\n'.join('import '+m for m in suite['module_order'])+'\nimport IndependentSCCIffProbe\nset_option pp.universes true\nset_option pp.explicit true\n'+''.join(f'#check @{t}\n#print axioms {t}\n' for t in targets))
    run=subprocess.run([str(lean),'-j1','--root='+str(out/'source'),str(audit)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=out/'logs/IndependentReadback.log';log.write_text(run.stdout)
    assert run.returncode==0,run.stdout;check_diagnostics(run.stdout)
    receipt['readback']={'target_count':len(targets),'source_sha256':sha(audit),'log_sha256':sha(log),'axioms':parse_readback(run.stdout,targets)}
    assert verify(source)['manifest_sha256']==identity['manifest_sha256']
    receipt['status']='PASS_COMPOSITIONAL'
except BaseException as exc:
    receipt['status']='FAIL_CLOSED';receipt['error']=repr(exc);raise
finally:
    receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write(out/'REPLAY_RESULT.json',receipt)
print(receipt['status'],flush=True)
