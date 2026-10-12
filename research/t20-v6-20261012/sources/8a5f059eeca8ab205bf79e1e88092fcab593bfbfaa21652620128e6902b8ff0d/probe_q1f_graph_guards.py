"""Countermodels only to an untyped graph-guard extrapolation, NOT to typed VCT."""
import json

def acyclic(nodes,edges):
    seen=set();active=set()
    def visit(v):
        if v in active:return False
        if v in seen:return True
        active.add(v)
        for a,b in edges:
            if a==v and not visit(b):return False
        active.remove(v);seen.add(v);return True
    return all(visit(v) for v in nodes)

models=[
 {'id':'P03-Q1f-CE01','source_nodes':['a','b'],'source_edges':[['a','b']],
  'map':{'a':'x','b':'x'},'target_nodes':['x'],'target_edges':[['x','x']],
  'expected_target_dag':False,'meaning':'map collapses endpoints of one source edge'},
 {'id':'P03-Q1f-CE02','source_nodes':['a','b'],'source_edges':[['a','b']],
  'map':{'a':'a','b':'b'},'target_nodes':['a','b'],'target_edges':[['a','b'],['b','a']],
  'expected_target_dag':False,'meaning':'injective map plus additional reverse edge'},
 {'id':'P03-Q1f-POS01','source_nodes':['a','b'],'source_edges':[['a','b']],
  'map':{'a':'c','b':'d'},'target_nodes':['c','d'],'target_edges':[['c','d']],
  'expected_target_dag':True,'meaning':'nontrivial valid edge transport'}]
for m in models:
    f=m['map'];image=set(f.values());es=set(map(tuple,m['target_edges']))
    m['source_is_dag']=acyclic(m['source_nodes'],m['source_edges'])
    m['map_domain_exact']=set(f)==set(m['source_nodes'])
    m['all_source_edges_preserved']=all((f[a],f[b]) in es for a,b in m['source_edges'])
    m['all_output_endpoints_in_image']=all(a in image and b in image for a,b in es)
    m['target_nodes_exact_image']=set(m['target_nodes'])==image
    m['map_injective']=len(image)==len(f)
    m['target_is_dag']=acyclic(m['target_nodes'],m['target_edges'])
    if not all(m[k] for k in ['source_is_dag','map_domain_exact','all_source_edges_preserved',
                             'all_output_endpoints_in_image','target_nodes_exact_image']):
        raise RuntimeError('invalid graph witness '+m['id'])
    if m['target_is_dag']!=m['expected_target_dag']:raise RuntimeError('wrong cycle result')
print(json.dumps({'status':'PASS_SCOPED_COUNTERMODELS','models':models,
 'other_guard_extension':{'version':'exact prior input; declared next output','claim':'same frozen claim',
 'root':'same ROOT','discharged':['d'],'preserved':['d'],'revalidated':[],'required':['d'],
 'semantics':'identity on a singleton interpretation','authority':'chosen valid in the example structure',
 'invalidators':[]},
 'not_a_vct_checker_execution':True,'not_a_counterexample_to_dag_typed_vct':True,
 'conclusion':'The graph guards alone do not imply target acyclicity; injectivity alone does not repair that omission.'},indent=2))
