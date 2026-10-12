#!/usr/bin/env python3
"""Verify the finite archive and actual native patch/review/apply receipt fields.

This reads selected files only. It never invokes Git, applies a patch, compiles,
installs, uploads, or reruns a gate. The archived native receipts own those claims.
"""
import argparse
import importlib.util
import json
from pathlib import Path

_spec=importlib.util.spec_from_file_location('owner_archive',Path(__file__).with_name('owner_archive.py'))
A=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(A)
S=A.S


def json_pointer(value,pointer):
    S.require(isinstance(pointer,str)and(pointer==''or pointer.startswith('/')),'Invalid JSON pointer')
    if pointer=='':return value
    for encoded in pointer[1:].split('/'):
        token=encoded.replace('~1','/').replace('~0','~')
        if isinstance(value,dict):
            S.require(token in value,'Native receipt field absent: '+pointer);value=value[token]
        elif isinstance(value,list):
            S.require(token.isdigit()and str(int(token))==token,'Invalid native array index')
            index=int(token);S.require(index<len(value),'Native array index absent');value=value[index]
        else:raise ValueError('Native receipt pointer crosses scalar: '+pointer)
    return value


def check_bindings(binding,bodies):
    S.require(binding.get('schema')=='owner-native-receipt-bindings-v1','Unknown native binding schema')
    patch=S.safe_relative(binding['patch_path']);S.require(patch in bodies,'Bound patch absent')
    facts=binding['facts']
    S.require(S.digest(bodies[patch])==facts['patch_sha256']and len(bodies[patch])==facts['patch_bytes'],'Actual patch differs from native binding facts')
    ids=[r['id']for r in binding['checks']]
    S.require(len(ids)==len(set(ids)),'Duplicate native check id')
    S.require(set(binding['required_check_ids'])<=set(ids),'Required native check absent')
    records={};verified=[]
    for row in binding['checks']:
        name=S.safe_relative(row['record']);S.require(name in bodies,'Native receipt not selected: '+name)
        if name not in records:records[name]=json.loads(bodies[name])
        actual=json_pointer(records[name],row['pointer'])
        S.require(('fact'in row)!=('expected'in row),'A native check needs exactly one expectation')
        expected=facts[row['fact']]if'fact'in row else row['expected']
        S.require(type(actual)is type(expected)and actual==expected,'Native receipt mismatch: '+row['id'])
        verified.append({'id':row['id'],'record':name,'pointer':row['pointer'],'status':'PASS'})
    return {'status':'PASS_NATIVE_RECEIPT_BINDINGS','checks_passed':len(verified),'checks':verified,
            'patch_sha256':facts['patch_sha256'],'candidate_tree':facts['candidate_tree'],
            'scope':'Actual receipt-field and byte bindings; not a new patch application, scientific run or CI result.'}



def check_layered_review(binding,bodies):
    chain=binding.get('review_chain',{})
    S.require(chain.get('mode')=='INHERITED_FULL_PLUS_FINAL_DELTA','Explicit layered review scope is required')
    full=S.safe_relative(chain['inherited_record']);delta=S.safe_relative(chain['delta_record'])
    S.require(full!=delta and full in bodies and delta in bodies,'Separate inherited and delta review records are required')
    facts=binding['facts']
    S.require(facts['inherited_review_tree']!=facts['candidate_tree'],'Inherited checkpoint must not be relabelled as the final tree')
    S.require(facts['inherited_review_sha256']!=facts['delta_review_sha256'],'One review body cannot supply both inherited and delta scopes')
    S.require(S.digest(bodies[full])==facts['inherited_review_sha256'],'Inherited full-review digest differs')
    S.require(S.digest(bodies[delta])==facts['delta_review_sha256'],'Final delta-review digest differs')
    rules={
      'review.inherited.base':(full,'base_commit'),
      'review.inherited.tree':(full,'inherited_review_tree'),
      'review.delta.base':(delta,'base_commit'),
      'review.delta.predecessor':(delta,'inherited_review_tree'),
      'review.delta.tree':(delta,'candidate_tree')}
    rows={r['id']:r for r in binding['checks']}
    S.require(len(rows)==len(binding['checks']),'Duplicate review binding id')
    records={full:json.loads(bodies[full]),delta:json.loads(bodies[delta])}
    for id,(record,fact) in rules.items():
        S.require(id in rows,'Required layered-review check absent: '+id)
        row=rows[id]
        S.require(row['record']==record and row.get('fact')==fact,'Layered review scope was substituted: '+id)
        actual=json_pointer(records[record],row['pointer']);expected=facts[fact]
        S.require(type(actual)is type(expected)and actual==expected,'Layered-review native field differs: '+id)
    for id,record in [('review.inherited.disposition',full),('review.delta.disposition',delta)]:
        S.require(id in rows,'Review disposition check absent')
        row=rows[id]
        S.require(row['record']==record and isinstance(row.get('expected'),str)and row['expected'].startswith('PASS'),'Review disposition scope differs')
        S.require(json_pointer(records[record],row['pointer'])==row['expected'],'Native review disposition differs')
    return {'status':'PASS_INHERITED_FULL_AND_FINAL_DELTA_BINDINGS','inherited_tree':facts['inherited_review_tree'],
            'final_delta_tree':facts['candidate_tree'],'fresh_whole_diff_review_claimed':False}


def verify_root(root):
    root=S.no_symlink_path(root)
    archive_check=A.verify_tree(root)
    S.require(archive_check['assembly_status']=='READY_TO_SEAL','Final integration fields are not ready')
    manifest=json.loads((root/A.MANIFEST).read_bytes());rows={r['path']:r for r in manifest['files']}
    name='integration/NATIVE_RECEIPT_BINDINGS.json'
    S.require(name in rows,'Finite native receipt binding record absent')
    binding=json.loads(S.checked_bytes(S.source_path(root,name),rows[name]))
    mandatory={'patch.digest','patch.bytes','patch.base','patch.base_tree','patch.tree',
      'clean.digest','clean.base','clean.tree','clean.actual_tree','clean.disposition',
      'review.inherited.disposition','review.inherited.base','review.inherited.tree',
      'review.delta.disposition','review.delta.base','review.delta.predecessor','review.delta.tree',
      'counts.results','counts.sources','counts.suites','counts.receipts','remote.head'}
    S.require(mandatory<=set(binding['required_check_ids']),'Final semantic check coverage incomplete')
    chain=binding.get('review_chain',{})
    needed={binding['patch_path']}|{r['record']for r in binding['checks']}
    needed.update([chain.get('inherited_record',''),chain.get('delta_record','')])
    S.require(needed<=set(rows),'Unselected native binding input')
    bodies={n:S.checked_bytes(S.source_path(root,n),rows[n])for n in needed}
    result=check_bindings(binding,bodies)
    layered_review=check_layered_review(binding,bodies)
    prior_name='integration/PRIOR_CHECKPOINT_IDENTITY.json'
    S.require(prior_name in rows,'Preserved prior-checkpoint identity absent')
    prior=json.loads(S.checked_bytes(S.source_path(root,prior_name),rows[prior_name]))
    S.require(binding['facts']['inherited_review_sha256']==prior['prior_review_sha256'] and binding['facts']['inherited_review_tree']==prior['prior_reviewed_tree'],'Inherited review was rebound away from the preserved checkpoint')
    integration=manifest['integration'];facts=binding['facts']
    for key in ['base_commit','base_tree','candidate_tree','patch_sha256']:
        S.require(integration[key]==facts[key],'Integration metadata differs from native facts: '+key)
    for name,key in [('results','actual_result_count'),('sources','actual_source_count'),('suites','actual_suite_count'),('receipts','actual_receipt_count')]:
        S.require(type(integration[key])is int and integration[key]==facts[name],'Native count differs: '+name)
    S.require(integration['patch_path']==binding['patch_path'],'Patch alias differs')
    link_name='verification/OWNER_LINK_RECEIPT.json'
    S.require(link_name in rows,'Finite owner-link receipt absent')
    link_receipt=json.loads(S.checked_bytes(S.source_path(root,link_name),rows[link_name]))
    link_inputs={r['path']for r in link_receipt['source_files']}|{r['target']for r in link_receipt['links']if r['kind']=='local'}
    S.require(link_inputs<=set(rows),'Link receipt target is outside finite payload')
    link_bodies={n:S.checked_bytes(S.source_path(root,n),rows[n])for n in link_inputs}
    link_spec=importlib.util.spec_from_file_location('verify_owner_links',Path(__file__).with_name('verify_owner_links.py'))
    links=importlib.util.module_from_spec(link_spec);link_spec.loader.exec_module(links)
    link_check=links.check_link_receipt(link_receipt,link_bodies)
    return {'status':'PASS_ARCHIVE_AND_NATIVE_INTEGRATION_BINDINGS','archive_verification':archive_check,'native_verification':result,
            'review_chain_verification':layered_review,'owner_relative_links':link_check,
            'remote_boundary':'The included timestamped readback binds the old PR30 head, never claims CI for the unpushed candidate.',
            'new_execution':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True);args=parser.parse_args()
    print(S.canonical_json(verify_root(args.root)).decode(),end='')

if __name__=='__main__':main()
