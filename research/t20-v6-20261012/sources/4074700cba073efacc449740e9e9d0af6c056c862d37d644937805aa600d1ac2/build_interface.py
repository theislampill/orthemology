"""Build an auditable research handoff, never a canonical theorem admission."""
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=Path('private-locator:36fb2027a2cd56fb6b89')
INPUT=Path('private-locator:e629ba29d6320a9434ae')

def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

nodes=[
 {'id':'L0','claim':'Typed evidence profiles','requires':[],
  'extra_premises':['coordinate schema','units and orientation','extraction identity','descriptive/evaluative partition'],
  'does_not_supply':['comparison rule','truth','authority']},
 {'id':'L1','claim':'Profile order and incomparability','requires':['L0'],
  'extra_premises':['declared partial order or improvement cone'],
  'does_not_supply':['total ranking','compensating scalar weights']},
 {'id':'L2','claim':'Endogenous finite local-view architecture','requires':['L0'],
  'extra_premises':['local states','local observations','explicit channels','shared causes'],
  'does_not_supply':['empirical cognitive anatomy','conditional independence']},
 {'id':'L3','claim':'Finite response architecture','requires':['L2'],
  'extra_premises':['nonempty finite response sets','local implementability','joint feasibility contract'],
  'does_not_supply':['product feasibility','infinite-horizon finite policy space','payoff comparison']},
 {'id':'L4','claim':'Product mixed-simplex geometry','requires':['L3'],
  'extra_premises':['full product of the selected response simplices'],
  'does_not_supply':['physical sampling law','profitable deviation','equilibrium']},
 {'id':'L5','claim':'Finite scalar expected-payoff game','requires':['L4'],
  'extra_premises':['real pure-profile payoff tables','ordinary independent mixed extension'],
  'does_not_supply':['correct utilities','unique equilibrium','convergent dynamics']},
 {'id':'L6','claim':'Finite vector expected-payoff game','requires':['L4','L1'],
  'extra_premises':['vector payoff tables','expected coordinate semantics','explicit nonzero-cone versus interior-cone improvement'],
  'does_not_supply':['unique scalarization','unrestricted vector existence']},
 {'id':'L7','claim':'Team or constrained/pipeline branch','requires':['L3'],
  'extra_premises':['shared objective or hard constraint or ordered transformation semantics'],
  'does_not_supply':['ordinary unconstrained Nash hypotheses','global optimum from unilateral stability']},
 {'id':'E5','claim':'Mixed Nash existence','requires':['L5'],
  'extra_premises':['standard finite Nash/Kakutani theorem'],
  'does_not_supply':['effective sampler','convergence','truth','authority']},
 {'id':'E6','claim':'Nonzero-cone equilibrium existence and weight-witness characterization','requires':['L6'],
  'extra_premises':['orthant order','finite mixed polytope','strictly positive player-specific supporting witnesses','finite Nash and separation'],
  'does_not_supply':['canonical weights','same characterization for arbitrary compact convex games']},
 {'id':'DEPLOY','claim':'Actual joint and temporal deployment model','requires':['L3'],
  'extra_premises':['joint kernel','temporal dependence','observation law','current operational license'],
  'does_not_supply':['normative target correctness','restoration']},
 {'id':'RESTORE','claim':'Sure or almost-sure temporal restoration','requires':['DEPLOY'],
  'extra_premises':['independently supplied safe/target predicates','complete transition model','declared winning mode','proved rank/acceptance or recurrence contract'],
  'does_not_supply':['source truth','historical conclusions','personal identity']},
 {'id':'TRUTH','claim':'Substantive epistemic/world correctness','requires':[],
  'extra_premises':['independent evidence for source, coordinate, target and world adequacy'],
  'does_not_supply':['automatic operational authorization']},
 {'id':'AUTHORITY','claim':'Legitimate application and execution','requires':[],
  'extra_premises':['independently authorized recipient/action/context/version contract'],
  'does_not_supply':['source truth','convergence']}
]
nodeids={n['id'] for n in nodes}
assert all(set(n['requires'])<=nodeids for n in nodes)
remaining=set(nodeids);done=set()
while remaining:
    ready={n['id'] for n in nodes if n['id'] in remaining and set(n['requires'])<=done}
    assert ready,'dependency cycle'
    done|=ready;remaining-=ready
write('assumption_dag.json',{'schema':'p14-assumption-dag-v1','status':'RESEARCH_MODEL_NOT_AUTHORITY',
      'nodes':nodes,'sibling_branches':['L5','L6','L7'],
      'forbidden_automatic_inferences':[['L0','L5'],['L4','E5'],['E5','RESTORE'],['E5','TRUTH'],
                                       ['E6','AUTHORITY'],['L1','DEPLOY'],['L5','L6'],['L6','L7']]})

bindings=[]
for name in ('RECEIPT.json','RESEARCH_BRIEF.md','BRIDGE_GUARDS.md','OBLIGATIONS.json',
             'external-source/Epistemic_Tuples_and_Intra_Agential_Equilibrium.pdf'):
    bindings.append({'kind':'supplied_input','path':name,'sha256':digest(INPUT/name)})
for name in ('experiments/orthemology-v5/mathematics/REFINEMENT_CALCULUS.md',
             'experiments/orthemology-v5/source/observations.py',
             'experiments/orthemology-v5/source/PROOFS_V4.md',
             'experiments/orthemology-v5/source/THEOREM_CATALOGUE.json',
             'experiments/orthemology-v5/source/OPERATIONAL_CONTRACT.md'):
    bindings.append({'kind':'pinned_repository','path':name,'sha256':digest(ROOT/name),
                     'commit':'03e2604dfcef278b01c60d19b05370fcec4194b6'})
write('source_bindings.json',{'sources':bindings,'input_receipt_status':'SEALED_HANDOFF_ONLY',
                             'input_research_executed':False})

units=json.loads((HERE/'obligation_checklist.json').read_text())
for unit in units:
    unit['status']='RESEARCH_COMPLETED_SCOPED_RETURN_NOT_CANONICAL_ADOPTION'
    unit['result_file']='research.md'
write('obligation_checklist.json',units)

theorems=[
 ('ET01-A','PROVED_FINITE','finite poset embeds in a real linear order exactly when it is a chain'),
 ('ET01-B','STANDARD_INSTANTIATION','target sufficiency is fibre constancy; full-codomain guard remains'),
 ('ET01-C','PROVED_FINITE_DIMENSIONAL','strict ranking reversal for unrestricted positive weights exactly at crossing differences'),
 ('ET03-A','PROVED_FINITE','local implementation iff local-view fibre constancy; faithful product-state flattening allowed'),
 ('ET04','STANDARD_CONDITIONAL_THEOREM','finite expected-payoff Nash with explicit nonempty/product/continuity/convexity hypotheses'),
 ('ET05-A','PROVED','strictly positive weighted Nash implies nonzero-cone equilibrium; boundary weights only give interior-cone guarantee'),
 ('ET05-B','PROVED_FINITE_POLYTOPE','nonzero-cone mixed equilibrium iff Nash for some player-specific strictly positive weights'),
 ('ET05-C','PROVED_FINITE_MULTILINEAR','joint concavity on the full mixed product iff additive pure team payoffs'),
 ('ET07-A','PROVED','order isomorphism preserves deterministic-profile comparisons under schema transport'),
 ('ET07-B','PROVED','action bijections and positive affine payoff changes preserve mixed Nash; affine cone transport preserves vector deviations'),
 ('ET-D1','PROVED_IID_ONLY','iid joint-profile deployment eventually stays target almost surely iff target has full joint mass'),
 ('ET-D2','PROVED_CONDITIONAL_DRIFT','nonnegative stopped rank with uniform conditional drift gives finite expected target-entry time')]

interface={
 'schema':'p14-completed-research-interface-v1',
 'status':'COMPLETED_RESEARCH_RETURN_WITH_ACCEPTED_REPAIRED_AND_REJECTED_BRIDGES',
 'basis_commit':'03e2604dfcef278b01c60d19b05370fcec4194b6',
 'input_status':'SEALED_HANDOFF_ONLY','input_research_executed':False,
 'this_return_research_executed':True,'repository_modified':False,
 'canonical_adoption':False,'empirical_validation':False,'kernel_checked_p14':False,'global_novelty_claim':False,
 'theorems':[{'id':i,'status':s,'statement':t} for i,s,t in theorems],
 'repairs':[
  'Every scalar map is lossy is rejected: injectivity and task sufficiency are separate from order reflection.',
  'PDF nonzero-cone formula differs from every-coordinate-strict prose; both improvement modes are named explicitly.',
  'Finite/countable CV-R defect zero does not measure score information loss or ranking adequacy.',
  'Finite response alphabets do not imply a finite unbounded-time policy space.',
  'Nonlinear monotone transforms of pure payoffs can change expected mixed equilibria.',
  'Compact convex continuous payoff sets do not retain the strictly-positive-weight converse without the finite-polyhedral premise.'
 ],
 'rejected_automatic_bridges':[
  'common comparison admission implies common operational license',
  'global analyst access implies local implementability',
  'simplex geometry alone implies equilibrium',
  'equilibrium existence implies convergence or temporal restoration',
  'explicit scalar/vector utility implies substantive normative authority',
  'same mixed marginals imply same joint or temporal law',
  'independent source labels imply independent acquisition roots'
 ],
 'p15_consumption_contract':{
  'allowed':'Use the exact conditional theorems and countermodels in this research return; carry their hypotheses and negative results.',
  'coordinate_warning':'Coordinate extraction/selection/orientation may already contain evaluation; do not place them automatically in a neutral descriptive reduct.',
  'weight_warning':'Supporting weights may depend on the equilibrium and player; existence neither selects a unique bridge nor legitimates it.',
  'positive_controls':'Chains, target-sufficient compression, independently fixed utility and inherited faithful re-encodings can make judgments invariant.',
  'ceiling':'No universal is-ought theorem, anti-naturalism, source truth or global metaphysical conclusion.'},
 'verification':json.loads((HERE/'probe_results.json').read_text()),
 'team_concavity_verification':json.loads((HERE/'team_concavity_results.json').read_text()),
 'artifacts':[]}
for name in ('research.md','assumption_dag.json','source_bindings.json','epistemic.py','test_epistemic.py',
             'probe_epistemic.py','probe_results.json','obligation_checklist.json',
             'team_concavity_check.py','team_concavity_results.json'):
    interface['artifacts'].append({'path':name,'sha256':digest(HERE/name)})
write('p15_interface.json',interface)
