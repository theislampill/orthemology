"""A finite relational bridge witness, not a metaphysical plural-perfect model.
Names below are metalanguage indices. The qualitative signature has no A/B or
individual-token constants. Model-relative labels do not prove necessity itself.
"""
from dataclasses import dataclass,replace
from itertools import product

@dataclass(frozen=True)
class Structure:
    domain: tuple
    relations: dict


def model():
    d=('A','B','PA','PB','AA','AB','q')
    unary={
      'Bearer':('A','B'),'Power':('PA','PB'),'Act':('AA','AB'),'Created':('q',),
      'DeclaredOriginal':('A','B'),'Powerful':('A','B'),'Knowing':('A','B'),
      'NecessaryLabel':('A','B')}
    r={name:frozenset((x,) for x in xs) for name,xs in unary.items()}
    r.update({
      'Inheres':frozenset({('PA','A'),('PB','B'),('AA','A'),('AB','B')}),
      'ActsOn':frozenset({('AA','q'),('AB','q')}),
      'OwnAttributePrerequisite':frozenset({('A','PA'),('B','PB')}),
      'OtherBearer':frozenset({('A','B'),('B','A')}),
      'SeparableProperPart':frozenset(),
      'ForeignEfficientReceipt':frozenset()})
    return Structure(d,r)

SWAP={'A':'B','B':'A','PA':'PB','PB':'PA','AA':'AB','AB':'AA','q':'q'}

def automorphism(m,p):
    return set(p)==set(m.domain) and set(p.values())==set(m.domain) and all(
        frozenset(tuple(p[x] for x in tup) for tup in ext)==ext for ext in m.relations.values())

# Terms and formula AST. Constants are used ONLY for explicit negative controls.
def V(x):return ('var',x)
def K(x):return ('const',x)
def R(name,*args):return ('rel',name,args)
def EQ(a,b):return ('eq',a,b)
def AND(a,b):return ('and',a,b)
def NOT(a):return ('not',a)
def EX(v,a):return ('exists',v,a)
def ALL(v,a):return ('all',v,a)
def IMPLIES(a,b):return NOT(AND(a,NOT(b)))

def term(t,env):return env[t[1]] if t[0]=='var' else t[1]

def truth(m,f,env):
    kind=f[0]
    if kind=='rel':return tuple(term(t,env) for t in f[2]) in m.relations[f[1]]
    if kind=='eq':return term(f[1],env)==term(f[2],env)
    if kind=='and':return truth(m,f[1],env) and truth(m,f[2],env)
    if kind=='not':return not truth(m,f[1],env)
    vals=(truth(m,f[2],env|{f[1]:x}) for x in m.domain)
    return any(vals) if kind=='exists' else all(vals)

def formulas():
    x,y=V('x'),V('y')
    owns_power=EX('y',AND(R('Power',y),R('Inheres',y,x)))
    acts=EX('y',AND(R('Act',y),R('Inheres',y,x)))
    works=EX('y',EX('z',AND(R('Act',y),AND(R('Inheres',y,x),AND(R('Created',V('z')),R('ActsOn',y,V('z')))))))
    other=EX('y',AND(R('Bearer',y),NOT(EQ(x,y))))
    no_part=NOT(EX('y',R('SeparableProperPart',y,x)))
    return {'owns_own_power':owns_power,'owns_own_act':acts,'acts_on_created_object':works,
            'has_other_numerically_distinct_bearer':other,'has_no_separable_part':no_part,
            'has_own_attribute_prerequisite':EX('y',R('OwnAttributePrerequisite',x,y)),
            'no_foreign_receipt':NOT(EX('y',R('ForeignEfficientReceipt',y,x))),
            'every_own_power_is_intrinsic':ALL('y',IMPLIES(R('OwnAttributePrerequisite',x,y),R('Inheres',y,x)))}

def with_feature(m):
    return replace(m,relations=m.relations|{'DistinguishingFeature':frozenset({('A',)})})

def report():
    m=model();fm=formulas();variant=with_feature(m)
    return {'scope':'Reduced relational witness; necessary/original predicates are declared labels, not independently warranted metaphysics. No perfect predicate or full source countermodel.',
      'domain':m.domain,'relations':{k:sorted(v) for k,v in m.relations.items()},
      'swap':SWAP,'swap_preserves_all_declared_relations':automorphism(m,SWAP),
      'sample_parameter_free_formulas':{k:{g:truth(m,f,{'x':g}) for g in ('A','B')} for k,f in fm.items()},
      'identity_to_A':{g:truth(m,EQ(V('x'),K('A')),{'x':g}) for g in ('A','B')},
      'has_named_power_PA':{g:truth(m,R('Inheres',K('PA'),V('x')),{'x':g}) for g in ('A','B')},
      'qualitative_feature_variant':{'swap_preserved':automorphism(variant,SWAP),'A_feature':True,'B_feature':False,'separable_parts':[],'foreign_receipt':[]},
      'nonzero_own_attribute_prerequisites':len(m.relations['OwnAttributePrerequisite']),
      'foreign_efficient_receipt_count':len(m.relations['ForeignEfficientReceipt']),
      'not_claimed':['all real intrinsic features exhaustively represented','two metaphysically necessary originals are possible','complete perfection or source-faithful efficacy','all attributes are merely mental','any parameterized property fails to distinguish A/B','property difference can never indicate composition','pure mathematical novelty']}

def reactive_reducts():
    """Read-only typed relational reducts of the actual SAME reactive candidate.
    Individual names are meta-indices; the retained signature is qualitative.
    This does not add necessity, perfection, or a missing original-source norm.
    """
    from pathlib import Path
    import sys
    sys.dont_write_bytecode=True
    front=Path(__file__).resolve().parents[3]
    sys.path.insert(0,str(front/'sovereignty-choice-semantics/reactive-context-extension/src'))
    import reactive_context as rc
    c=rc.Catalogue(('e0','e1'));joined=rc.epistemic_model(c)
    records=[]
    for w in joined['worlds']:
        originals=w['originals'];actual=w['actual'];acts={a.bearer:a for a in actual['acts']}
        domains=set(originals)|set(actual['events'])
        powers={g:o.power_token for g,o in originals.items()};knowers={g:o.knowledge_token for g,o in originals.items()}
        act_tokens={g:a.token for g,a in acts.items()}
        goals={f'goal:{i}' for i in range(c.n)};settings={f'setting:{i}' for i in range(c.n)}
        for group in (powers.values(),knowers.values(),act_tokens.values(),goals,settings):domains.update(group)
        r={'Bearer':frozenset((g,) for g in originals),
           'PowerToken':frozenset((x,) for x in powers.values()),
           'KnowledgeToken':frozenset((x,) for x in knowers.values()),
           'ActToken':frozenset((x,) for x in act_tokens.values()),
           'CreatedEvent':frozenset((x,) for x in actual['events']),
           'GoalLabel':frozenset((x,) for x in goals),'SettingLabel':frozenset((x,) for x in settings),
           'Inheres':frozenset(joined['inherence'])|frozenset((a.token,g) for g,a in acts.items()),
           'EfficientEdge':frozenset(w['efficient_edges']),
           'GoalOf':frozenset((a.token,f'goal:{a.goal}') for a in acts.values()),
           'SettingOf':frozenset((a.token,f'setting:{a.setting}') for a in acts.values()),
           'AvailableSetting':frozenset((g,f'setting:{s}') for g,o in originals.items() for s in o.repertoire),
           'SatisfiedIntention':frozenset((g,) for g,v in actual['intentions'].items() if v),
           'SatisfiedOwnEnd':frozenset((g,) for g,v in actual['own_activity_ends'].items() if v),
           'ForecastSetting':frozenset((knowers[g],a.token,f'setting:{a.setting}') for g,forecast in w['forecasts'].items() for a in forecast['acts']),
           'ForecastGoal':frozenset((knowers[g],a.token,f'goal:{a.goal}') for g,forecast in w['forecasts'].items() for a in forecast['acts']),
           'ForecastEvent':frozenset((knowers[g],e) for g,forecast in w['forecasts'].items() for e in forecast['events']),
           'EntireProvider':frozenset((g,e) for e,gs in actual['entire'].items() for g in gs)}
        swap={x:x for x in domains};swap.update({'A':'B','B':'A'})
        for group in (powers,knowers,act_tokens):swap[group['A']]=group['B'];swap[group['B']]=group['A']
        structure=Structure(tuple(sorted(domains)),r)
        records.append({'context':w['context'],'structure':structure,'swap':swap,'is_automorphism':automorphism(structure,swap),
                        'originals':originals,'act_tokens':act_tokens})
    return records
