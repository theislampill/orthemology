"""Independent repair check: fresh local copy, exact patch, unchanged original review."""
from __future__ import annotations
import copy, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parent
FINDING=BASE.parent/'noetic-guard-peer-review-20261009'
AUTHOR=BASE.parent/'noetic-correction-semantics-20261009'
PATCH_SHA='ba1c28f70bc74b70451ae4a63910f49308a23d5b068d1a3e61c8cb0bf9c97a58'
PREIMAGE_SHA='ea6630a53ce8c77d6cc3102ae6ffd5aba0dc84539f1ffe5350fbc1aa4d9c4d1a'
PREIMAGE_BLOB='469a1d4e60520671171caf4989353460eada7a8b'
COMMIT='c86b3c6673147b8802fe222373a165a37d4d24a8'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def file_sha(p):return sha(p.read_bytes())
def git_blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
# Original evidence files stay byte-for-byte unchanged, including its manifest.
original={}
for line in (FINDING/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    p=FINDING/name
    assert file_sha(p)==expected,name
    original[str(p)]=expected
original[str(FINDING/'SHA256SUMS')]=file_sha(FINDING/'SHA256SUMS')
patch=AUTHOR/'UNAPPLIED_RECOGNITION_GUARD.patch'
assert file_sha(patch)==PATCH_SHA
raw=(AUTHOR/'sources/tools/check_ir_instance_integrity.py').read_bytes()
assert sha(raw)==PREIMAGE_SHA and git_blob(raw)==PREIMAGE_BLOB
ROOT=Path(tempfile.mkdtemp(prefix='fresh-replay-',dir=BASE))
LOGS=ROOT/'logs';LOGS.mkdir()
binding=json.loads((FINDING/'SOURCE_BINDINGS.json').read_text());assert binding['frozen_commit']==COMMIT
for record in binding['files']:
    raw=(FINDING/'pinned-inputs'/record['path']).read_bytes()
    assert sha(raw)==record['sha256'] and git_blob(raw)==record['git_blob_sha'] and len(raw)==record['bytes']
    dest=ROOT/record['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
map_source=FINDING/'pinned-inputs/skill/compiled-module-map.json'
map_dest=ROOT/'skill/compiled-module-map.json';map_dest.parent.mkdir()
map_dest.write_bytes(map_source.read_bytes())
local_patch=ROOT/'UNAPPLIED_RECOGNITION_GUARD.patch';local_patch.write_bytes(patch.read_bytes())
checker=ROOT/'tools/check_ir_instance_integrity.py'
assert file_sha(checker)==PREIMAGE_SHA
full_validator=FINDING/'validate_full_schema.py'
schema=ROOT/'atomics/skill/references/diagnostics/diagnostic-ir.schema.json'
strong=json.loads((FINDING/'pinned-inputs/peer-fixtures/alignment-advanced-strong.json').read_text())
values={}
for strength in ('strong','medium','weak','none'):
    v=copy.deepcopy(strong);v['recognition_strength']=strength;values['advanced-'+strength]=v
v=copy.deepcopy(strong);del v['recognition_strength'];values['advanced-recognition-missing']=v
v=copy.deepcopy(strong);v.update(alignment_state='blocked',recognition_strength='none');values['nonadvanced-none']=v
fixture_dir=ROOT/'repair-fixtures';fixture_dir.mkdir()
for name,v in values.items():
    (fixture_dir/(name+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def run(name,command):
    p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    result={'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    (LOGS/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

api_script=ROOT/'api_probe.py'
api_script.write_text('''import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'tools'))
import check_ir_instance_integrity as ir
root=Path(__file__).resolve().parent
value=json.loads(Path(sys.argv[1]).read_text())
schema=ir.load_json(root/'atomics/skill/references/diagnostics/diagnostic-ir.schema.json')
errors=ir.validate_instance('repair probe',value,schema,ir.load_catalogue(root),ir.load_compiled_modules(root))
print(json.dumps(errors,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
''')
results={}
for stage in ('before','after'):
    if stage=='after':
        check=run('patch-dry-run',['patch','--dry-run','--fuzz=0','-p1','-i',str(local_patch)])
        assert check['exit_code']==0,check
        applied=run('patch-apply',['patch','--fuzz=0','-p1','-i',str(local_patch)])
        assert applied['exit_code']==0,applied
        after_raw=checker.read_bytes()
        addition=b'\n    if (\n        instance.get("alignment_state") == "alignment-advanced"\n        and "recognition_strength" in instance\n        and instance["recognition_strength"] != "strong"\n    ):\n        errors.append("schema: alignment-advanced requires recognition_strength strong when supplied")\n'
        before_raw=(FINDING/'pinned-inputs/tools/check_ir_instance_integrity.py').read_bytes()
        assert after_raw.count(addition)==1
        assert after_raw.replace(addition,b'',1)==before_raw
    results[stage]={}
    for name,v in values.items():
        fixture=fixture_dir/(name+'.json')
        cli=run(stage+'-'+name+'-main',[sys.executable,'-B',str(checker),'--file',str(fixture)])
        alias=run(stage+'-'+name+'-alias',[sys.executable,'-B',str(ROOT/'tools/check_diagnostic_ir_catalogue_integrity.py'),'--file',str(fixture)])
        api=run(stage+'-'+name+'-api',[sys.executable,'-B',str(api_script),str(fixture)])
        full=run(stage+'-'+name+'-full-schema',[sys.executable,'-B',str(full_validator),str(schema),str(fixture)])
        expected=1 if name=='advanced-recognition-missing' or (stage=='after' and name in ('advanced-medium','advanced-weak','advanced-none')) else 0
        assert cli['exit_code']==alias['exit_code']==api['exit_code']==expected,(stage,name,cli,alias,api)
        expected_schema=0 if name in ('advanced-strong','nonadvanced-none') else 1
        assert full['exit_code']==expected_schema,(stage,name,full)
        errors=json.loads(api['stdout'])
        if name=='advanced-recognition-missing':
            assert len(errors)==1 and 'missing required field: recognition_strength' in errors[0],errors
        elif stage=='after' and name in ('advanced-medium','advanced-weak','advanced-none'):
            assert errors==['repair probe: schema: alignment-advanced requires recognition_strength strong when supplied'],errors
        elif expected==0:assert not errors
        results[stage][name]={'fixture_sha256':file_sha(fixture),'api_exit':api['exit_code'],'api_errors':errors,'main_cli_exit':cli['exit_code'],'alias_cli_exit':alias['exit_code'],'full_schema_exit':full['exit_code'],'full_schema_errors':json.loads(full['stdout'])}
    selfcheck=run(stage+'-embedded-samples',[sys.executable,'-B',str(checker),'--samples-only'])
    assert selfcheck['exit_code']==0,selfcheck
    assert 'Embedded bad samples checked: 54' in selfcheck['stdout']
    results[stage]['embedded_self_checks_exit']=0
# Show the original unrelated category3/open issue remains present and unchanged.
original_fixture=FINDING/'pinned-inputs/peer-fixtures/unchanged-embedded-positive.json'
unrelated=run('after-unchanged-positive-full-schema',[sys.executable,'-B',str(full_validator),str(schema),str(original_fixture)])
assert unrelated['exit_code']==1 and [x['path'] for x in json.loads(unrelated['stdout'])]==[['routing_gate']]
for p,expected in original.items():assert file_sha(Path(p))==expected,p
assert file_sha(patch)==PATCH_SHA
assert file_sha(AUTHOR/'sources/tools/check_ir_instance_integrity.py')==PREIMAGE_SHA
result={'verdict':'bounded candidate repair passes independent before/after replay',
 'frozen_commit':COMMIT,'candidate_patch_sha256':PATCH_SHA,'preimage_sha256':PREIMAGE_SHA,'preimage_git_blob_sha':PREIMAGE_BLOB,
 'postimage_sha256':file_sha(checker),'original_review_sha256':file_sha(FINDING/'REVIEW.md'),'original_review_manifest_sha256':file_sha(FINDING/'SHA256SUMS'),
 'original_evidence_files_unchanged':len(original),'map_projection_sha256':file_sha(map_dest),'replay_root':str(ROOT),
 'patch_exactly_seven_added_lines':True,'results':results,
 'unrelated_category3_open_gate_still_schema_invalid':True,
 'scope':'Unapplied to protected/pinned source. Applied only to fresh local copy. Two-entry compiler-derived map projection reused; no full runtime build, CI, complete schema-coverage, or human-state claim.'}
(BASE/'REPAIR_PEER_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
