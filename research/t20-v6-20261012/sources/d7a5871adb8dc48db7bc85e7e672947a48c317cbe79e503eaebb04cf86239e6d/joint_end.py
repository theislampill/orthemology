"""Interpreted richer ends over the UNCHANGED recovered reactive law.

Full intention content is not source-level complete volition. Original root
nonreceipt is not individual entire original provision. Product-only observation
perturbations are test controls, never proposed wise metaphysical worlds.
"""
from pathlib import Path
from dataclasses import dataclass,replace
import importlib.util,sys,hashlib
ROOT=Path(__file__).resolve().parents[3]
MODEL_PATH=ROOT/'recovery-t20/addendum/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py'
assert hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()=='f73cee9c0271dd2a80843a3994534e1119fca33386e59a483f3175d69880a6cc'
spec=importlib.util.spec_from_file_location('valued_recovered_model',MODEL_PATH)
Model=importlib.util.module_from_spec(spec);sys.modules[spec.name]=Model;spec.loader.exec_module(Model)
@dataclass(frozen=True)
class End:
    product_q:int
    kind:str
    subject:str
    peer_identity:str|None
@dataclass(frozen=True)
class Choice:
    end:End
    exercise:object
    def with_end(self,end):return Choice(end,self.exercise)
    def with_product_intention(self,q):
        return Choice(replace(self.end,product_q=q),Model.Exercise(self.exercise.bearer,q,self.exercise.setting))
def make_context(q,kind):
    return {'q':q,'catalogue':Model.Catalogue(('e0','e1')),'originals':{g:Model.Original(g) for g in ('A','B')},
            'ends':{g:End(q,kind,g,'B_original' if g=='A' else 'A_original') for g in ('A','B')}}
def ordinary_choices(ctx):return tuple(Choice(ctx['ends'][g],Model.own_policy(ctx['originals'][g],ctx['q'])) for g in ('A','B'))
def execute(ctx,choices,product_transform=None):
    choices=tuple(choices)
    by={c.exercise.bearer:c.exercise for c in choices}
    if len(by)!=len(choices):raise ValueError('Duplicate actor exercise.')
    base=Model.execute(ctx['catalogue'],by.get('A'),by.get('B'))
    edges=tuple((token,e) for e,proof in base['proofs'].items() for token in proof['intrinsic_inputs'])
    joint=(set(by)=={'A','B'} and bool(base['events'])
           and all(roots==frozenset(('A','B')) for roots in base['supports'].values())
           and len({int(a.goal) for a in by.values()})==1
           and all(c.end.subject==c.exercise.bearer and c.end.product_q==c.exercise.goal for c in choices))
    observed=base['events'] if product_transform is None else product_transform(ctx['catalogue'],base['events'])
    result={'choices':choices,'base':base,'evaluated_product':observed,
            'target_catalogue':ctx['catalogue'].targets,
            'actual_agent_identities':{'A':'A_original','B':'B_original'},
            'policy_conforms':choices==ordinary_choices(ctx),'joint_relation':joint,
            'source_roots':frozenset(g+'_original' for g in by),
            'efficient_edges':edges,
            'structural_nonreceipt':all(not Model.has_foreign_donor(t,g,edges)
                 for g,o in ctx['originals'].items() for t in (o.power_token,o.knowledge_token)),
            'intentional_aboutness':tuple((c.exercise.bearer,c.end.peer_identity) for c in choices if c.end.kind!='own'),
            'synthetic_product_observation_control':product_transform is not None}
    result['full_end_satisfied']={c.exercise.bearer:satisfies(c.end,result) for c in choices}
    return result


def satisfies(end,run):
    """Truth conditions for stated end content, never a CompleteWill test."""
    if end.kind not in {'own','joint','original_joint'}:raise ValueError('Unknown end kind.')
    base=run['base']; by={a.bearer:a for a in base['acts']}
    product=(run['evaluated_product']==run['target_catalogue'][end.product_q])
    own=(end.subject in by and by[end.subject].goal==end.product_q and bool(base['events'])
         and all(end.subject in roots for roots in base['supports'].values()))
    if not(product and own):return False
    if end.kind=='own':return True
    peer='B' if end.subject=='A' else 'A'
    joint=(run['joint_relation'] and peer in by and by[peer].goal==end.product_q)
    if end.peer_identity is not None:
        joint=joint and run['actual_agent_identities'][peer]==end.peer_identity
    if end.kind=='original_joint':
        joint=joint and peer+'_original' in run['source_roots']
    return bool(joint)


def forecast(ctx):
    # Generated from the full end records and known policies before any actual
    # intervention/run is supplied. It includes richer satisfaction and support.
    return execute(ctx,ordinary_choices(ctx))


def active_solutions(ctx):
    # The existing simultaneous solution function is reused, not enlarged.
    q=ctx['q']; out=[]
    for a,b in Model.response_pairs(ctx['catalogue'],q,q):
        out.append(tuple(Choice(ctx['ends'][g],ctx['originals'][g].issue(q,s))
                         for g,s in (('A',a),('B',b))))
    return tuple(out)


def shifted_product(c,events):
    # Alter only the evaluated product observation to challenge a hidden
    # success filter. This record is flagged synthetic, not a factual world.
    if not events:return events
    return c.targets[(c.targets.index(events)+1)%len(c.targets)]


def source_comparison(q):
    """Separate source-origin control, not a change to the two-original rival.

    Compare a generic real other-agent project, retaining created peer
    requisites. Do not claim same complete created inventory or same de re B.
    """
    c=Model.Catalogue(('e0','e1')); local=c.targets[q]
    graphs={
      'plural':{'A_original':(),'B_original':(),
                'A_act':('A_original',),'B_act':('B_original',)},
      'derived':{'A_original':(),'A_act':('A_original',),
                 'C_created':('A_original',),'C_power':('A_original',),
                 'C_will':('A_original',),
                 'C_act':('C_created','C_power','C_will')},
    }
    def roots(node,graph):
        parents=graph.get(node,())
        return frozenset((node,)) if not parents else frozenset().union(*(roots(p,graph) for p in parents))
    result={}
    for mode,graph in graphs.items():
        peer_act='B_act' if mode=='plural' else 'C_act'
        peer_identity='B_original' if mode=='plural' else 'C_created'
        for e in local:graph[e]=('A_act',peer_act)
        all_roots=frozenset().union(*(roots(e,graph) for e in local))
        actual_actors={'A':{'act':'A_act','intended_product':q},
                       peer_identity:{'act':peer_act,'intended_product':q}}
        real_joint=(len(actual_actors)==2 and all(set(graph[e])=={'A_act',peer_act} for e in local)
                    and all(a['intended_product']==q for a in actual_actors.values()))
        inventory=local if mode=='plural' else local|frozenset(('C_created','C_power','C_will','C_act'))
        result[mode]={'local_product':local,'created_inventory':inventory,'original_roots':all_roots,
                      'graph':graph,'actual_actor_records':actual_actors,
                      'generic_joint_end':real_joint,
                      'original_peer_end':real_joint and roots(peer_act,graph)==frozenset(('B_original',)),
                      'designated_B_end':real_joint and peer_identity=='B_original',
                      'scope':'Typed origin comparison; no claim of same complete created history or preserved de re peer intention.'}
    return result
