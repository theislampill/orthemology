"""Independent bounded replay against verified copies, not a repo/CI/runtime build."""
from __future__ import annotations
import copy, hashlib, importlib.metadata, json, os, shutil, subprocess, sys
from pathlib import Path
from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parent
AUTHOR = BASE.parent / 'noetic-correction-semantics-20261009'
ROOT = BASE / 'pinned-inputs'
LOGS = BASE / 'logs'
BINDING = json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())
EXPECTED = 'c86b3c6673147b8802fe222373a165a37d4d24a8'
assert BINDING['frozen_commit'] == EXPECTED
KEEP = {
 'tools/check_ir_instance_integrity.py', 'tools/check_diagnostic_ir_catalogue_integrity.py',
 'tools/compiled_runtime_lib.py', 'tools/delta_result_vocabulary.py',
 'tools/build_compiled_runtime.py', '.github/workflows/ci.yml',
 'atomics/skill/references/diagnostics/diagnostic-ir.schema.json',
 'atomics/skill/references/diagnostics/module-catalogue.json',
 'atomics/skill/references/diagnostics/delta-result-vocabulary.json',
 'atomics/skill/references/tactics/M1-self-refutation.md',
 'atomics/skill/references/tactics/M8-reductio.md',
 'tests/ir-fixtures/valid/field-witness-closure-graph.json',
}
verified=[]
for item in BINDING['files']:
    raw=(AUTHOR/'sources'/item['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==item['sha256'],item['path']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['git_blob_sha'],item['path']
    assert len(raw)==item['bytes'],item['path']
    if item['path'] in KEEP:
        out=ROOT/item['path']; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
        verified.append(item)
assert set(x['path'] for x in verified)==KEEP
(BASE/'SOURCE_BINDINGS.json').write_text(json.dumps({'repository':BINDING['repository'],'frozen_commit':EXPECTED,'files':verified},indent=2)+'\n')
LOGS.mkdir(exist_ok=True)
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'tools'))
import check_ir_instance_integrity as ir
import compiled_runtime_lib as cl
schema_path=ROOT/'atomics/skill/references/diagnostics/diagnostic-ir.schema.json'
schema=json.loads(schema_path.read_text())
Draft202012Validator.check_schema(schema)
validator=Draft202012Validator(schema)
catalogue=ir.load_catalogue(ROOT)
# Reproduce only the compiler's module metadata expression, from pinned source
# documents and pinned bundle mapping. No fabricated module identities or paths.
modules={}
for bundle,paths in cl.BUNDLE_SOURCES.items():
    for rel in paths:
        if Path(rel).stem not in ('M1-self-refutation','M8-reductio'): continue
        doc=cl.load_source_doc(ROOT,rel)
        modules[doc.module_id]={'module_id':doc.module_id,'module_class':doc.module_class,
          'canonical_path':doc.canonical_path,'source':doc.source_rel_path,
          'source_sha256':doc.sha256,'bundle_path':bundle}
assert set(modules)=={'M1-self-refutation','M8-reductio'}
map_path=ROOT/'skill/compiled-module-map.json';map_path.parent.mkdir(exist_ok=True)
map_path.write_text(json.dumps({'peer_replay_only':'two-entry compiler-derived projection; not a rebuilt runtime','modules':modules},indent=2)+'\n')
assert modules==json.loads((AUTHOR/'sources/skill/compiled-module-map.json').read_text())['modules']

def schema_errors(value):
    return [{'path':list(e.absolute_path),'schema_path':list(e.absolute_schema_path),'message':e.message} for e in validator.iter_errors(value)]

def sha256(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(tag,args):
    p=subprocess.run(args,text=True,capture_output=True,cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    record={'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    (LOGS/(tag+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    return record

validator_script=BASE/'validate_full_schema.py'
validator_script.write_text('''import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
schema=json.loads(Path(sys.argv[1]).read_text())
value=json.loads(Path(sys.argv[2]).read_text())
Draft202012Validator.check_schema(schema)
errors=[{"path":list(e.absolute_path),"schema_path":list(e.absolute_schema_path),"message":e.message} for e in Draft202012Validator(schema).iter_errors(value)]
print(json.dumps(errors,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
''')
fixtures=ROOT/'peer-fixtures'; fixtures.mkdir(exist_ok=True)
original=copy.deepcopy(ir.POSITIVE_SAMPLE)
control=copy.deepcopy(original);control.update(reason_category=1,alignment_state='alignment-advanced',recognition_strength='strong')
assert schema_errors(original)==[{'path':['routing_gate'],'schema_path':['allOf',8,'then','properties','routing_gate','not'],'message':"'open' should not be valid under {'const': 'open'}"}]
assert not schema_errors(control)
records={}
values={'unchanged-embedded-positive':original,'cleaned-only-reason-category':{**copy.deepcopy(original),'reason_category':1}}
for strength in ('strong','medium','weak','none'):
    value=copy.deepcopy(control);value['recognition_strength']=strength
    values['alignment-advanced-'+strength]=value
    author=json.loads((AUTHOR/'sources/replay-fixtures'/('alignment-advanced-'+strength+'.json')).read_text())
    assert value==author
for name,value in values.items():
    path=fixtures/(name+'.json');path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    api=ir.validate_instance(name,value,schema,catalogue,modules)
    assert api==[],(name,api)
    custom=run(name+'-custom',[sys.executable,'-B',str(ROOT/'tools/check_ir_instance_integrity.py'),'--file',str(path)])
    alias=run(name+'-alias',[sys.executable,'-B',str(ROOT/'tools/check_diagnostic_ir_catalogue_integrity.py'),'--file',str(path)])
    full=run(name+'-full-schema',[sys.executable,'-B',str(validator_script),str(schema_path),str(path)])
    assert custom['exit_code']==alias['exit_code']==0,(name,custom,alias)
    expected_full_exit=1 if name=='unchanged-embedded-positive' or name in ('alignment-advanced-medium','alignment-advanced-weak','alignment-advanced-none') else 0
    assert full['exit_code']==expected_full_exit,(name,full)
    if name in ('alignment-advanced-medium','alignment-advanced-weak','alignment-advanced-none'):
        assert schema_errors(value)==[{'path':['recognition_strength'],'schema_path':['allOf',17,'then','properties','recognition_strength','const'],'message':"'strong' was expected"}]
        assert [k for k in control if control[k]!=value[k]]==['recognition_strength']
    records[name]={'sha256':sha256(path),'custom_api_errors':api,'schema_errors':schema_errors(value),'custom_cli_exit':custom['exit_code'],'compatibility_cli_exit':alias['exit_code'],'full_schema_exit':full['exit_code'],'logs_prefix':'logs/'+name}
official_path=ROOT/'tests/ir-fixtures/valid/field-witness-closure-graph.json'
official=run('unchanged-official-valid-fixture-custom',[sys.executable,'-B',str(ROOT/'tools/check_ir_instance_integrity.py'),'--file',str(official_path)])
assert official['exit_code']==0
samples=run('unchanged-embedded-suite',[sys.executable,'-B',str(ROOT/'tools/check_ir_instance_integrity.py'),'--samples-only'])
assert samples['exit_code']==0
# Establish map sufficiency for this exact API, and preserve positive boundaries.
map_checks=[]
for module in modules:
    subset=copy.deepcopy(modules);subset.pop(module)
    errors=ir.validate_instance('missing-module-control',control,schema,catalogue,subset)
    assert any('does not resolve' in e and module in e for e in errors)
    map_checks.append({'removed':module,'errors':errors})
for title,section,key,replacement in (
    ('closure-is-interlocutor','closure','operator','𝒞(Ψᴵ)'),
    ('transfer-is-guaranteed','transfer_boundary','mode','guaranteed-update'),
    ('transfer-from-interlocutor','transfer_boundary','from','Ψᴵ')):
    value=copy.deepcopy(control);value['field_witness'][section][key]=replacement
    errors=ir.validate_instance(title,value,schema,catalogue,modules)
    assert errors,(title,errors)
    records[title]={'custom_api_errors':errors}
result={'verdict':'confirmed bounded custom-validator/published-schema conformance gap',
 'frozen_commit':EXPECTED,'python':sys.version,'jsonschema':importlib.metadata.version('jsonschema'),
 'source_files_verified_in_author_binding':len(BINDING['files']),'source_files_copied_and_rehashed':len(verified),
 'schema_sha256':sha256(schema_path),'checker_sha256':sha256(ROOT/'tools/check_ir_instance_integrity.py'),
 'module_map_sha256':sha256(map_path),'module_map_scope':'two exact compiler-derived entries; no full runtime rebuild',
 'map_dependency_counterchecks':map_checks,
 'baseline_control_changes':{'reason_category':1,'alignment_state':'alignment-advanced','recognition_strength':'strong'},
 'only_experimental_change':'recognition_strength','records':records,
 'unchanged_official_valid_fixture_cli_exit':official['exit_code'],'embedded_self_checks_exit':samples['exit_code'],
 'scope_limits':['No full repository CI/build','No source edits or patches','No live-model behavior or actual human knowledge, willingness, restoration, or warrant claims']}
(BASE/'PEER_REVIEW_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
