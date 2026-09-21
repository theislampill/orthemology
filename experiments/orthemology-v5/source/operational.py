"""O_F: finite checked operations, current dependency licences, pure execution.
The trusted host may revise the context. Candidates cannot supply Python code.
Tickets are process-local bearer handles, NOT a remote authentication scheme.
All dispatch/check-use and revision actions are serialised by the same lock.
"""
from __future__ import annotations
from dataclasses import dataclass
from threading import RLock
import secrets,hashlib
from boundaries import Rejection,bound_tree,load_json,dump_json
import reference as r
import extensions as e
import productive as p
import guarded_sampler as gs
import observations as ob
import productive_observer as po
BOOL=('all',('arr',('v',0),('arr',('v',0),('v',0))))
MAX_RECORDS=4096
MAX_REVISIONS=10000
@dataclass(frozen=True)
class Licence:
    ticket:str
    issuer:object=None
@dataclass(frozen=True)
class Compiled:
    tag:str
    dom:tuple
    cod:tuple
    data:tuple
    deps:frozenset
    nodes:int=1
@dataclass(frozen=True)
class Issued:
    source:bytes
    compiled:Compiled
    bindings:tuple
    probability_evidence:tuple=()

def interface(x):
    bound_tree(x)
    if x in ('nat','bool','unit'):return (x,)
    if type(x) in (list,tuple) and len(x)==3 and x[0]=='pair':return ('pair',interface(x[1]),interface(x[2]))
    if type(x) in (list,tuple) and len(x)==2 and x[0]=='finite' and type(x[1]) is int and 1<=x[1]<=4096:return ('finite',x[1])
    raise Rejection('interface: outside declared grammar')

def accepts(a,x):
    bound_tree(x)
    if a[0]=='nat':return type(x) is int and 0<=x and x.bit_length()<=256
    if a[0]=='bool':return type(x) is bool
    if a[0]=='unit':return x is None
    if a[0]=='pair':return type(x) in (tuple,list) and len(x)==2 and accepts(a[1],x[0]) and accepts(a[2],x[1])
    if a[0]=='finite':return type(x) is int and 0<=x<a[1]
    if a[0]=='bits':return type(x) in (list,tuple) and len(x)<=p.MAX_BITS and all(type(b) is int and b in (0,1) for b in x)
    if a[0]=='core':return type(x) is dict and set(x)=={'proof'} and r.check(x['proof'])[1]==a[1]
    if a[0]=='sample':
        if type(x) is not dict:return False
        if set(x)=={'status','bits','cell'}:
            return x['status']=='pending' and type(x['bits']) is int and 0<=x['bits']<=p.MAX_BITS and type(x['cell']) is int and 0<=x['cell']<(1<<x['bits'])
        return set(x)=={'status','bits','branch','proof'} and x['status']=='done' and x['branch'] in ('left','right') and type(x['bits']) is int and 1<=x['bits']<=p.MAX_BITS and r.check(x['proof'])[1]==a[1]
    raise Rejection('interface: invalid compiled tag')

class Engine:
    def __init__(self):
        self._lock=RLock();self._issuer=object();self._rules={'schema':(0,True),'vocabulary':(0,True)};self._observations={};self._issued={};self._epoch=0;self._prob_observations={};self._prob_requirements={}
    @classmethod
    def standard(cls):
        o=cls()
        for key in ['structural','primitive:succ','primitive:iszero','primitive:not','core','selector','edge','sampler','observer']:o.revise_rule(key,True)
        return o
    def _revision_budget(self):
        if self._epoch>=MAX_REVISIONS:raise Rejection('resource: revision history bound')
    def revise_rule(self,key,allowed):
        if type(key) is not str or not key or len(key)>200 or type(allowed) is not bool:raise Rejection('revision: malformed policy')
        if key in ('schema','vocabulary') or key.startswith(('obs:','probobs:','need:')):raise Rejection('revision: reserved key')
        with self._lock:
            self._revision_budget();old=self._rules.get(key,(-1,False));self._rules[key]=(old[0]+1,allowed);self._epoch+=1
    def set_observation(self,name,values):
        bound_tree(values)
        if type(name) is not str or not name or len(name)>200 or type(values) not in (list,tuple) or not 1<=len(values)<=4096 or any(type(x) is not int or x<0 for x in values):raise Rejection('observation: finite natural signature required')
        with self._lock:
            self._revision_budget()
            if name not in self._observations and len(self._observations)>=128:raise Rejection('resource: observation count')
            self._observations[name]=tuple(values)
            for key in ['vocabulary','obs:'+name]:self._rules[key]=(self._rules.get(key,(-1,False))[0]+1,True)
            self._epoch+=1
    def remove_observation(self,name):
        if type(name) is not str:raise Rejection('observation: text key required')
        with self._lock:
            self._revision_budget()
            if name not in self._observations:raise Rejection('observation: unknown name')
            del self._observations[name]
            for key in ['vocabulary','obs:'+name]:self._rules[key]=(self._rules[key][0]+1,key=='vocabulary')
            self._epoch+=1
    def set_probability_observation(self,name,spec):
        if type(name) is not str or not 1<=len(name)<=128:raise Rejection('observation: model name')
        raw=dump_json(spec);ob.check(load_json(raw))
        with self._lock:
            self._revision_budget()
            if name not in self._prob_observations and len(self._prob_observations)>=128:raise Rejection('resource: probability vocabulary count')
            self._prob_observations[name]=raw
            key='probobs:'+name;self._rules[key]=(self._rules.get(key,(-1,False))[0]+1,True);self._epoch+=1
    def refine_probability_observation(self,name,spec):
        if type(name) is not str or not 1<=len(name)<=128:raise Rejection('observation: model name')
        spec=load_json(dump_json(spec))
        with self._lock:
            if name not in self._prob_observations:raise Rejection('observation: missing coarse model')
            report=ob.refinement(load_json(self._prob_observations[name]),spec)
            self.set_probability_observation(name,spec)
            return report
    def coarsen_probability_observation(self,name,spec):
        if type(name) is not str or not 1<=len(name)<=128:raise Rejection('observation: model name')
        spec=load_json(dump_json(spec))
        with self._lock:
            if name not in self._prob_observations:raise Rejection('observation: missing fine model')
            report=ob.refinement(spec,load_json(self._prob_observations[name]))
            self.set_probability_observation(name,spec)
            report['revision_direction']='coarsening'
            return report
    def require_probability(self,rule,observation,epsilon):
        if type(rule) is not str or rule in ('schema','vocabulary') or rule.startswith(('need:','obs:','probobs:')):raise Rejection('probability: operation policy key required')
        if type(observation) is not str or not 1<=len(observation)<=128:raise Rejection('observation: model name')
        eps=ob.pair(ob.rational(epsilon))
        with self._lock:
            self._revision_budget()
            if rule not in self._rules or observation not in self._prob_observations:raise Rejection('probability: unknown rule or model')
            self._prob_requirements[rule]=(observation,tuple(eps))
            key='need:'+rule;self._rules[key]=(self._rules.get(key,(0,True))[0]+1,True);self._epoch+=1
    def remove_probability_requirement(self,rule):
        if type(rule) is not str:raise Rejection('probability: policy name')
        with self._lock:
            self._revision_budget()
            if rule not in self._prob_requirements:raise Rejection('probability: unknown obligation')
            del self._prob_requirements[rule]
            key='need:'+rule;self._rules[key]=(self._rules[key][0]+1,True);self._epoch+=1
    def _stamp(self,key):
        return self._rules.get(key,(0,True) if key.startswith('need:') else None)
    def _item(self,licence):
        # Caller-native dataclasses are not proof-carrying authority. Validate
        # before hash-table lookup to reject unhashable/oversized forged fields.
        if type(licence) is not Licence or type(licence.ticket) is not str or len(licence.ticket)!=48 or any(x not in '0123456789abcdef' for x in licence.ticket):raise Rejection('authority: malformed licence')
        if licence.issuer is not self._issuer:raise Rejection('authority: wrong issuer context')
        if licence.ticket not in self._issued:raise Rejection('authority: unissued licence')
        return self._issued[licence.ticket]
    def revalidate(self,licence):
        with self._lock:
            old=self._item(licence)
            # A stale handle can nominate immutable source for a NEW check; it
            # cannot confer any authority on the returned admission decision.
            return self.admit_json(old.source)
    def describe(self,licence):
        with self._lock:
            v=self._item(licence)
            return {'current':self._current(v),'source_sha256':hashlib.sha256(v.source).hexdigest(),
                    'bindings':[[k,list(b)] for k,b in v.bindings],
                    'probability_evidence':[load_json(x) for x in v.probability_evidence]}
    def _compile(self,c):
        budget=[1000];type_work=[200000]
        def fields(d,*ks):
            if set(d)!={'op',*ks}:raise Rejection('candidate: incorrect fields')
        def node(tag,a,b,data,keys,children=()):
            bound_tree(a,work=type_work);bound_tree(b,work=type_work)
            deps=frozenset({'schema',*keys}).union(*(x.deps for x in children))
            return Compiled(tag,a,b,data,deps,1+sum(x.nodes for x in children))
        def go(d,h=0):
            budget[0]-=1
            if h>60 or budget[0]<0:raise Rejection('resource: operation budget')
            if type(d) is not dict or type(d.get('op')) is not str:raise Rejection('candidate: named operation required')
            op=d['op']
            if op=='primitive':
                fields(d,'name');n=d['name'];tys={'succ':(('nat',),('nat',)),'iszero':(('nat',),('bool',)),'not':(('bool',),('bool',))}
                if type(n) is not str or n not in tys:raise Rejection('candidate: unknown primitive')
                return node(op,*tys[n],(n,),{'primitive:'+n})
            if op in ('id','copy'):
                fields(d,'type');a=interface(d['type']);return node(op,a,a if op=='id' else ('pair',a,a),(),{'structural'})
            if op in ('first','second'):
                fields(d,'left','right');a,b=interface(d['left']),interface(d['right']);return node(op,('pair',a,b),a if op=='first' else b,(),{'structural'})
            if op=='compose':
                fields(d,'first','second');a,b=go(d['first'],h+1),go(d['second'],h+1)
                if a.cod!=b.dom:raise Rejection('typing: composition mismatch')
                return node(op,a.dom,b.cod,(a,b),{'structural'},(a,b))
            if op=='parallel':
                fields(d,'left','right');a,b=go(d['left'],h+1),go(d['right'],h+1)
                return node(op,('pair',a.dom,b.dom),('pair',a.cod,b.cod),(a,b),{'structural'},(a,b))
            if op=='core':
                fields(d,'proof');t,a=r.check(d['proof'])
                if a[0]!='arr':raise Rejection('typing: source arrow required')
                return node(op,('core',a[1]),('core',a[2]),(dump_json(d['proof']),),{'core'})
            if op=='selector':
                fields(d,'type','proof','trace');a=interface(d['type']);t,ty=r.check(d['proof'])
                if ty!=BOOL:raise Rejection('typing: polymorphic selector required')
                cert=e.certify_selector(t,d['trace']);return node(op,('pair',a,a),a,(cert.selector,cert.overhead),{'selector'})
            if op=='observer':
                fields(d,'source','invariant')
                po.certify_constant(d['source'],d['invariant'])
                return node(op,('bits',),('bits',),(dump_json(d['source']),),{'observer'})
            if op=='sampler_budgeted':
                fields(d,'source','max_pending');q=gs.check(d['source']);cert=gs.certificate(q)
                if ob.rational(cert['pending_mass'])>ob.rational(d['max_pending']):raise Rejection('sampler: residual budget not met')
                return node(op,('bits',),('sample',q.leaves.ty),(q,),{'sampler','core'})
            if op=='sampler':
                fields(d,'left','right');q=p.check(d['left'],d['right']);return node(op,('bits',),('sample',q.ty),(q,),{'sampler','core'})
            if op=='edge':
                fields(d,'size','source','target');n,s,t=d['size'],d['source'],d['target']
                if type(n) is not int or not 1<=n<=4096 or any(type(x) is not int or not 0<=x<n for x in [s,t]):raise Rejection('edge: invalid carrier/endpoints')
                for v in self._observations.values():
                    if len(v)!=n or v[s]!=v[t]:raise Rejection('preservation: edge changes active observation')
                return node(op,('finite',n),('finite',n),(s,t),{'edge','vocabulary',*('obs:'+k for k in self._observations)})
            raise Rejection('candidate: unknown operation')
        return go(c)
    def admit(self,c):return self.admit_json(dump_json(c))
    def admit_json(self,raw):
        x=load_json(raw);frozen=dump_json(x)
        with self._lock:
            if len(self._issued)>=MAX_RECORDS:raise Rejection('resource: licence count')
            c=self._compile(x);bindings=[];probability=[];deps=set(c.deps)
            for key in sorted(c.deps):
                if key not in ('schema','vocabulary') and not key.startswith('obs:'):
                    # Even ABSENCE of an obligation is version-bound; adding one
                    # must invalidate evidence issued before the obligation existed.
                    deps.add('need:'+key)
                    if key in self._prob_requirements:
                        name,eps=self._prob_requirements[key]
                        evidence=ob.certify(load_json(self._prob_observations[name]),eps)
                        evidence.update(operation_policy=key,observation=name)
                        probability.append(dump_json(evidence));deps.add('probobs:'+name)
            for key in sorted(deps):
                rule=self._stamp(key)
                if rule is None or not rule[1]:raise Rejection('authority: disabled dependency '+key)
                bindings.append((key,rule))
            # Registry identity is an invariant, not a probabilistic assumption.
            # Repeated entropy must never overwrite an older (possibly revoked)
            # ticket. Bounded retries fail closed and preserve all old records.
            for _ in range(8):
                token=secrets.token_hex(24)
                if token not in self._issued:
                    self._issued[token]=Issued(frozen,c,tuple(bindings),tuple(probability))
                    return Licence(token,self._issuer)
            raise Rejection('authority: ticket uniqueness could not be established')
    def _current(self,c):return all(rule[1] and self._stamp(k)==rule for k,rule in c.bindings)
    def _execute(self,c,x):
        work=[200000]
        def go(c,x):
            bound_tree(x,work=work)
            if not accepts(c.dom,x):raise Rejection('typing: intermediate input')
            if c.tag=='id':y=x
            elif c.tag=='copy':y=[x,x]
            elif c.tag=='first':y=x[0]
            elif c.tag=='second':y=x[1]
            elif c.tag=='primitive':
                y=x+1 if c.data[0]=='succ' else x==0 if c.data[0]=='iszero' else not x
            elif c.tag=='compose':y=go(c.data[1],go(c.data[0],x))
            elif c.tag=='parallel':y=[go(c.data[0],x[0]),go(c.data[1],x[1])]
            elif c.tag=='core':y={'proof':{'rule':'app','function':load_json(c.data[0]),'argument':x['proof']}}
            elif c.tag=='selector':y=x[c.data[0]]
            elif c.tag=='observer':y=po.prefix(load_json(c.data[0]),x)['output']
            elif c.tag=='sampler':y=p.run_prefix(c.data[0],x)
            elif c.tag=='sampler_budgeted':y=gs.run(c.data[0],x)['output']
            elif c.tag=='edge':y=c.data[1] if x==c.data[0] else x
            else:raise Rejection('internal: unknown executable node')
            # No later operation may erase an out-of-contract intermediate.
            bound_tree(y,work=work)
            if not accepts(c.cod,y):raise Rejection('typing: intermediate output')
            return y
        return go(c,x)
    def dispatch(self,licence,value):
        x=load_json(dump_json(value))
        with self._lock:
            item=self._item(licence)
            if not self._current(item):raise Rejection('authority: stale evidence')
            c=item.compiled
            if not accepts(c.dom,x):raise Rejection('typing: wrong input')
            y=self._execute(c,x)
            if not accepts(c.cod,y):raise Rejection('typing: wrong output')
            return load_json(dump_json(y))
    def project(self,*,limit=128,offset=0):
        if type(limit) is not int or not 1<=limit<=128 or type(offset) is not int or not 0<=offset<=MAX_RECORDS:raise Rejection('resource: projection pagination')
        with self._lock:
            current=[(key,v) for key,v in self._issued.items() if self._current(v)]
            out=[{'ticket':key,'source_sha256':hashlib.sha256(v.source).hexdigest(),'nodes':v.compiled.nodes,
                  'dependencies':[k for k,_ in v.bindings]} for key,v in current[offset:offset+limit]]
            return load_json(dump_json(out))

def positive_probe(o):
    try:
        return o.dispatch(o.admit({'op':'primitive','name':'succ'}),2)==3 and o.dispatch(o.admit({'op':'primitive','name':'iszero'}),0) is True and o.dispatch(o.admit({'op':'primitive','name':'not'}),True) is False
    except Rejection:return False
