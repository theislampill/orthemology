"""Exact portable family admission hooks; generic execution remains prohibited."""
from pathlib import Path
import hashlib,json

RECIPE='t08-semantic-portable-family-v1'
BINDINGS_SHA='6eb339e70f570056a9bc7b110ae5d8652956646e749cce6062ccfd5b0fff8468'
DRIVER={'driver_sha256':'3f2bcdbac6726d5924aa193b250a43c91474bca3f1cd1a22568f760f224169a3','driver_bytes':5897,
        'archive_sha256':'54e5e68673fd1ab35921144c6c5df958217da3a96de7a060b0bbb34f0ba6637e','archive_bytes':242937,'root':'','driver_path':'replay_review_portable.py'}
INNER={'driver_sha256':'210480b01a6a14f8458541ccb34d782f7bf87536aaf11df4751aff62addb5da4','driver_bytes':7591,
       'archive_sha256':'a7dac7ac8fe8e867b4581ebcd2757067371985eb728a66fc83720e33389c8f9b','archive_bytes':1520801,'root':'','driver_path':'replay_review.py'}
MEANINGS={'--review-zip':'INPUT_FILE','--lean-bin':'LEAN_BIN_DIRECTORY','--mathlib':'MATHLIB_ROOT','--out':'FRESH_OUTPUT_DIRECTORY'}
PARENT='original-portable'
MISMATCH=['error: application type mismatch','η ≤ ε : Prop','η ≤ ε / 2 : Prop']

def bindings():
    raw=Path(__file__).with_name('portable_bindings_v2.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=BINDINGS_SHA:raise ValueError('Portable code-owned bindings changed')
    return json.loads(raw)

APPROVED={name:row['suite_fingerprint'] for name,row in bindings().items()}

def validate_driver(api,row,source):
    api.check_custody_driver(source,DRIVER)
    api.require(row['id']=='portable' and row['sha256']==DRIVER['driver_sha256'] and row['external_input_id']=='portable-archive'
                and row['argument_meanings']==MEANINGS,'Portable original driver contract changed')

def diagnostic(api,row,sources):
    if row['literal'] not in MISMATCH:return False
    api.check_custody_driver(sources[row['source_id']],INNER)
    return True

def validate_package(api,suite,plan):
    owned=bindings();api.require(suite['id'] in owned,'Unreviewed portable namespace view');view=owned[suite['id']]
    api.require(len(plan['drivers'])==1 and len(plan['inputs'])==2 and not plan['fixtures'],'Portable family requires exactly two original archives')
    for iid,contract in [('portable-archive',DRIVER),('core-review-archive',INNER)]:
        row=plan['inputs'][iid]
        api.require(row['kind']=='FILE' and row['expected_sha256']==contract['archive_sha256'] and row['expected_bytes']==contract['archive_bytes'],'Portable exact archive identity differs')
    roots=['original/core/cost/build'] if view['namespaces']==['cost'] else ['original/literal/build','original/core/runtime/build']
    api.require(plan['build_roots']==roots,'Portable namespace-specific build roots changed')
    stages=list(plan['stages'].values());api.require(stages[0]['id']==PARENT and len(stages)==len(view['children'])+1,'Portable observation census differs')
    api.require([row['argv'][2] for row in stages[1:]]==[row['id'] for row in view['children']],'Portable child observation order differs')
    for row in view['children']:
        api.require(row['source_id'] in plan['contents'] and api.sha(plan['contents'][row['source_id']])==row['source_sha256'],'Portable child/source projection binding differs')
        api.require(row['source_binding']=={'kind':'ORIGINAL_SOURCE','source_id':row['source_id'],'source_sha256':row['source_sha256']},'Portable child source kind changed')
    for row in view['module_objects']:
        module=plan['modules'][row['module']]
        api.require(module['source_id']==row['source_id'] and 'original/'+row['relative_object'] in [x['object_path'] for x in view['children'] if x['id']==row['child_id']], 'Portable module/object namespace binding differs')
    plan['portable_view']=view

def validate_argv(api,stage,driver,plan):
    if stage['argv'][:1]==['{builtin:observe-child}']:
        api.require('portable_view' in plan,'Missing portable source-bound view')
        children={row['id']:row for row in plan['portable_view']['children']}
        api.require(len(stage['argv'])==3 and stage['argv'][1]==PARENT and stage['argv'][2] in children,'Foreign portable child observation')
        child=children[stage['argv'][2]];expected=child['expected_exit']
        kind='NEGATIVE_CONTROL' if expected else 'REFERENCE_TESTS' if child['id']=='literal/native' else 'LEAN_AUDIT' if child['axiom_count'] else 'POSITIVE_CONTROL'
        api.require(stage['kind']==kind and stage['expected_exit_codes']==[expected] and not stage['output_paths'],'Portable original observation role/output changed')
        api.require([x['literal'] for x in stage['expected_diagnostics']]==child['diagnostic_literals'],'Portable diagnostic contract differs')
    else:
        expected=['{tool:python}','-B','{driver:portable}','--review-zip','{input:core-review-archive}','--lean-bin','{tool:lean-bin}','--mathlib','{dependency:mathlib}','--out','{out}/original']
        api.require(stage['id']==PARENT and stage['kind']=='DRIVER' and stage['argv']==expected and stage['expected_exit_codes']==[0]
                    and stage['output_paths']==['original'] and not stage['expected_diagnostics'],'Unreviewed portable original invocation')

def is_portable(suite):
    return any(row['recipe']==RECIPE for row in suite['replay']['drivers'])
