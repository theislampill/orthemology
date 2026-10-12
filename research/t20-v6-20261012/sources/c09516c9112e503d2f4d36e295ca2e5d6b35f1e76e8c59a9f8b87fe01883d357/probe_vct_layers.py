#!/usr/bin/env python3
"""Finite declared-contract models for Q1f layer independence.

Not execution of the historical VCT checker and not evidence of real authority.
Evidence validation is exact context-indexed token equality in this toy model;
semantic preservation is checked at BOTH finite worlds, not assumed as a flag.
"""
from copy import deepcopy
from pathlib import Path
import argparse,json

def frame(name,version,root,req):
    expected={o:f'{o}/contract-{version}' for o in req}
    return {'id':name,'version':version,'root':root,'claim':'claim-'+str(version),
            'nodes':[name+'0',name+'1'],'edges':[[name+'0',name+'1']],
            'rank':{name+'0':0,name+'1':1},'required':req,'discharged':req,
            'expected_evidence':expected,'evidence':dict(expected),'meaning':[False,True]}

def hop(a,b):
    preserved=[o for o in a['discharged'] if o in ['source-auth','reason-valid']]
    new=[o for o in b['discharged'] if o not in preserved]
    return {'input_frame':deepcopy(a),'map':dict(zip(a['nodes'],b['nodes'])),
       'preserved':preserved,'revalidated':new,
       'carry':{o:{a['evidence'][o]:b['evidence'][o]} for o in preserved},
       'fresh':{o:b['evidence'][o] for o in new},'world_map':[0,1],
       'new_root_evidence':None if a['root']==b['root'] else 'independent-root-B'}

def fixture():
    a=frame('A',1,'ROOT-A',['source-auth','reason-valid'])
    b=frame('B',2,'ROOT-A',['source-auth','reason-valid','version-valid'])
    c=frame('C',3,'ROOT-B',['source-auth','reason-valid','version-valid','permission'])
    p={'epoch':7,'compatible_versions':{'7':[1,2,3],'8':[4]},
       'authority':[['A','B'],['B','C']],'redelegable':['B'],'invalidators':{},
       'independent_root_tokens':{'ROOT-B':'independent-root-B'}}
    return {'frames':[a,b,c],'hops':[hop(a,b),hop(b,c)],'policy':p}

def sound(s):return all(s['evidence'].get(o)==s['expected_evidence'].get(o) and o in s['expected_evidence'] for o in s['discharged'])
def ranked(s):
    n=set(s['nodes']);return len(n)==len(s['nodes']) and set(s['rank'])==n and all(type(x) is int and x>=0 for x in s['rank'].values()) and all(u in n and v in n and s['rank'][u]<s['rank'][v] for u,v in s['edges'])

def check(data):
    ss,hh,p=data['frames'],data['hops'],data['policy'];rows=[]
    if len(ss)!=len(hh)+1 or not hh:return {'accepted':False,'reason':'path shape'}
    rows.append({'initial_evidence_sound':sound(ss[0]),'initial_DAG':ranked(ss[0])})
    for i,(a,b,h) in enumerate(zip(ss,ss[1:],hh)):
        f=h['map'];P=set(h['preserved']);R=set(h['revalidated'])
        graph_domain=set(f)==set(a['nodes'])
        target_image=set(f.values())==set(b['nodes'])
        edges=all([f.get(u),f.get(v)] in b['edges'] for u,v in a['edges'])
        carry=all(o in a['discharged'] and a['evidence'].get(o)==a['expected_evidence'].get(o)
            and o in a['expected_evidence']
            and h['carry'].get(o,{}).get(a['evidence'].get(o))==b['expected_evidence'].get(o)
            and b['evidence'].get(o)==b['expected_evidence'].get(o)
            and o in b['expected_evidence'] for o in P)
        fresh=all(o in b['expected_evidence'] and h['fresh'].get(o)==b['expected_evidence'][o]
            and b['evidence'].get(o)==b['expected_evidence'][o] for o in R)
        rootok=(a['root']==b['root'] or h['new_root_evidence'] is not None and h['new_root_evidence']==p['independent_root_tokens'].get(b['root']))
        wm=h['world_map'];semantic=len(wm)==len(a['meaning']) and all(type(v) is int and 0<=v<len(b['meaning']) and b['meaning'][v]==a['meaning'][u] for u,v in enumerate(wm))
        rows.append({'exact_boundary':h['input_frame']==a,
          'graph_DAG_and_domain':ranked(b) and graph_domain and target_image and edges,
          'reason_evidence':carry and fresh and set(b['discharged'])==P|R,
          'target_coverage':set(b['required'])<=P|R,
          'authority':[a['id'],b['id']] in p['authority'],
          'redelegation':i==0 or a['id'] in p['redelegable'],
          'version_currentness':b['version'] in p['compatible_versions'].get(str(p['epoch']),[]),
          'invalidators':not p['invalidators'].get(b['id'],[]),
          'semantic_square':semantic,'root_custody':rootok})
    return {'accepted':all(all(row.values()) for row in rows),'guard_rows':rows,
            'failed_coordinates':[[i,k] for i,r in enumerate(rows) for k,v in r.items() if not v]}

def run(out):
    out.mkdir(parents=True,exist_ok=True);positive=fixture();result=check(positive)
    if not result['accepted']:raise AssertionError(result)
    models=[{'id':'VCT-A2-POSITIVE','model':positive,'result':result}]
    variants={
      'EVIDENCE-CONTRACT-DRIFT':lambda d:d['frames'][2]['evidence'].__setitem__('reason-valid','reason-valid/contract-2'),
      'TARGET-CONTRACT-OMISSION':lambda d:d['frames'][2]['required'].append('new-target-obligation'),
      'AUTHORITY-ABSENT':lambda d:d['policy']['authority'].remove(['B','C']),
      'REDELEGATION-ABSENT':lambda d:d['policy']['redelegable'].clear(),
      'VERSION-EPOCH-CHANGE':lambda d:d['policy'].__setitem__('epoch',8),
      'INVALIDATOR-OPEN':lambda d:d['policy']['invalidators'].__setitem__('C',['source-retracted']),
      'SEMANTIC-NONCOMMUTATION':lambda d:d['hops'][1].__setitem__('world_map',[1,0]),
      'NEW-ROOT-WITHOUT-WITNESS':lambda d:d['hops'][1].__setitem__('new_root_evidence',None)}
    for name,mutate in variants.items():
        d=deepcopy(positive);mutate(d);r=check(d)
        if r['accepted']:raise AssertionError(name)
        models.append({'id':'VCT-A2-'+name,'model':d,'result':r,
            'scope':'finite declared-contract guard-deletion/alteration model; no new historical theorem credit'})
    # Valid path does not imply direct authority or identical endpoints' roots.
    direct=['A','C'] in positive['policy']['authority']
    roots_equal=positive['frames'][0]['root']==positive['frames'][-1]['root']
    if direct or roots_equal:raise AssertionError('shortcut countermodel misconfigured')
    shortcuts={'path_accepted':True,'direct_A_C_authority':False,'initial_final_root_equal':False,
        'reason':'Per-hop authority plus intermediate redelegation yields an authorised PATH. A separately witnessed independent root can legitimately change the final root. Neither direct authority transitivity nor root equality is an unconditional conclusion.'}
    (out/'LAYER_MODELS.json').write_text(json.dumps({'models':models,'shortcut_countermodel':shortcuts},indent=2)+'\n')
    summary={'positive_paths':1,'separating_models':len(variants),'shortcut_countermodels':2,'all_expected_outcomes':True,
             'historical_checker_reexecuted':False,'kernel_credit':False}
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();run(args.out)
