"""Finite, exact-rational reference controls for the T20 cross-front research.

These functions implement the declared mathematical models. They do not infer
real-world source reliability, semantic truth, or the completeness of a source
support record. All likelihoods in transport contracts refer to historical
states, not automatically to subsequently transported coordinates.
"""
from fractions import Fraction
from collections.abc import Mapping, Hashable, Callable, Iterable
from typing import TypeVar, Any

S=TypeVar('S',bound=Hashable)
T=TypeVar('T',bound=Hashable)


def _mass(measure: Mapping[S, Any]) -> dict[S, Fraction]:
    if not measure:
        raise ValueError('A nonempty finite state domain is required.')
    out={s:Fraction(v) for s,v in measure.items()}
    if any(v<0 for v in out.values()):
        raise ValueError('Negative masses are not probability masses.')
    return out


def normalise(measure: Mapping[S, Any]) -> dict[S, Fraction]:
    """Normalise a finite nonnegative measure; zero evidence is an error."""
    out=_mass(measure); total=sum(out.values(),Fraction(0))
    if total<=0:
        raise ValueError('The evidence normaliser must be strictly positive.')
    return {s:v/total for s,v in out.items()}


def tilt(measure: Mapping[S, Any], likelihood: Mapping[S, Any]) -> dict[S, Fraction]:
    """Bayes/positive-potential reweighting; no re-evaluation at a new state."""
    p=_mass(measure)
    if not set(p).issubset(likelihood):
        raise ValueError('A likelihood is required on every declared state.')
    factors={s:Fraction(likelihood[s]) for s in p}
    if any(v<0 for v in factors.values()):
        raise ValueError('Likelihoods must be nonnegative.')
    return normalise({s:p[s]*factors[s] for s in p})


def pushforward(measure: Mapping[S, Any], mapping: Mapping[S,T]) -> dict[T,Fraction]:
    """Push forward a finite measure without discarding its total mass."""
    p=_mass(measure)
    if not set(p).issubset(mapping):
        raise ValueError('The state map is not total on the measure domain.')
    out:dict[T,Fraction]={}
    for s,v in p.items(): out[mapping[s]]=out.get(mapping[s],Fraction(0))+v
    return out


def tv(p: Mapping[S, Any], q: Mapping[S, Any]) -> Fraction:
    """Total variation distance between normalised finite distributions."""
    a=normalise(p); b=normalise(q)
    return sum((abs(a.get(s,Fraction(0))-b.get(s,Fraction(0)))
                for s in set(a)|set(b)),Fraction(0))/2


def transported_likelihood(mapping: Mapping[S,T], factors: Mapping[S,Any]) -> dict[T,Fraction]:
    """Factor L=ell∘mapping, or reject a nonconstant fibre.

    This tests the unnormalised/evidence-preserving contract. It intentionally
    rejects the degenerate single-image case when factors differ: the
    normalised output alone would hide its lost predictive evidence mass.
    """
    if not mapping or not set(mapping).issubset(factors):
        raise ValueError('Nonempty map and complete historical factors required.')
    ell:dict[T,Fraction]={}
    for s,t in mapping.items():
        value=Fraction(factors[s])
        if value<0: raise ValueError('Negative likelihood.')
        if t in ell and ell[t]!=value:
            raise ValueError('Historical likelihood is not constant on this fibre.')
        ell[t]=value
    return ell


def _kernel(kernel: Mapping[S,Mapping[T,Any]]) -> dict[S,dict[T,Fraction]]:
    if not kernel: raise ValueError('Empty kernel.')
    out={s:_mass(row) for s,row in kernel.items()}
    if any(sum(row.values(),Fraction(0))!=1 for row in out.values()):
        raise ValueError('Each kernel row must have total mass one.')
    return out


def kernel_pushforward(measure: Mapping[S,Any], kernel: Mapping[S,Mapping[T,Any]]) -> dict[T,Fraction]:
    p=_mass(measure); k=_kernel(kernel)
    if not set(p).issubset(k): raise ValueError('Missing kernel row.')
    out:dict[T,Fraction]={}
    for s,m in p.items():
        for y,v in k[s].items(): out[y]=out.get(y,Fraction(0))+m*v
    return out


def kernel_likelihood(kernel: Mapping[S,Mapping[T,Any]], factors: Mapping[S,Any]) -> dict[T,Fraction]:
    """Solve K diag(L)=diag(ell) K on positive support edges."""
    k=_kernel(kernel)
    if not set(k).issubset(factors): raise ValueError('Missing historical factor.')
    ell:dict[T,Fraction]={}
    for s,row in k.items():
        value=Fraction(factors[s])
        if value<0: raise ValueError('Negative likelihood.')
        for y,p in row.items():
            if p==0: continue
            if y in ell and ell[y]!=value:
                raise ValueError('The kernel merges unequal likelihoods on a support component.')
            ell[y]=value
    # A column unreachable from every origin contributes zero measure;
    # its coarse factor can be assigned arbitrarily without changing the identity.
    for row in k.values():
        for y in row: ell.setdefault(y,Fraction(0))
    return ell


def audit_sidecar(base: Mapping[S,T], factors: Mapping[Hashable,Mapping[S,Any]]) -> tuple[dict[S,int],int,int]:
    """Minimal alphabet for the static, evidence-preserving audit profile.

    The base record is retained. Labels may therefore be reused in different
    base fibres. This does not certify future transition sufficiency.
    """
    if not base: raise ValueError('Nonempty finite state domain required.')
    for values in factors.values():
        if not set(base).issubset(values): raise ValueError('Missing source factors.')
    source_order=list(factors)
    fibre_profiles:dict[T,dict[tuple[Fraction,...],int]]={}
    labels:dict[S,int]={}
    for state,record in base.items():
        profile=tuple(Fraction(factors[source][state]) for source in source_order)
        if any(v<=0 for v in profile):
            raise ValueError('Addition/removal audit profiles require strictly positive factors.')
        classes=fibre_profiles.setdefault(record,{})
        if profile not in classes: classes[profile]=len(classes)
        labels[state]=classes[profile]
    alphabet=max(len(c) for c in fibre_profiles.values())
    return labels,alphabet,(alphabet-1).bit_length()


def live_claims(warrants: Mapping[S,Iterable[Iterable[T]]], live_dependencies: Iterable[T]) -> set[S]:
    """Existential survival of a complete, already checked support witness."""
    live=set(live_dependencies)
    return {claim for claim,choices in warrants.items()
            if any(set(support).issubset(live) for support in choices)}


def affected_nodes(dependencies: Mapping[S,Iterable[S]], changed: Iterable[S]) -> set[S]:
    """Reachability from changed source/parameter nodes in a declared DAG."""
    deps={node:set(parents) for node,parents in dependencies.items()}
    changed_closure=set(changed)
    while True:
        newly={node for node,parents in deps.items()
               if set(parents)&changed_closure}-changed_closure
        if not newly: break
        changed_closure.update(newly)
    return changed_closure&set(dependencies)


def replay_dag(dependencies: Mapping[S,Iterable[S]], functions: Mapping[S,Callable[[Mapping[S,Any]],Any]],
               revised_inputs: Mapping[S,Any], cached_values: Mapping[S,Any], changed_inputs: Iterable[S]) -> tuple[dict[S,Any],list[S]]:
    """Replay affected descendants; reuse other nodes under an explicit contract.

    Preconditions: deterministic functions, complete dependency declarations,
    unchanged function definitions, a current cache for the old inputs, and a
    complete changed-input set. The function cannot discover an omitted source
    dependency or an undisclosed input change by magic.
    """
    deps={n:set(ps) for n,ps in dependencies.items()}
    if set(deps)!=set(functions): raise ValueError('Every node needs exactly one function.')
    if set(deps)&set(revised_inputs): raise ValueError('Input and computed-node IDs overlap.')
    unknown=set().union(*deps.values())-set(deps)-set(revised_inputs) if deps else set()
    if unknown: raise ValueError(f'Unknown dependencies: {unknown!r}')
    remaining=set(deps); ordered=[]
    while remaining:
        ready=sorted((n for n in remaining if not (deps[n]&remaining)),key=repr)
        if not ready: raise ValueError('Acyclic dependencies required.')
        ordered.extend(ready); remaining.difference_update(ready)
    dirty=affected_nodes(deps,changed_inputs)
    values=dict(cached_values); values.update(revised_inputs); recomputed=[]
    for node in ordered:
        if node in dirty or node not in values:
            values[node]=functions[node](values); recomputed.append(node)
            # Missing cached parents are also a semantic rebuild cause.
            dirty.update(affected_nodes(deps,{node}))
    return values,recomputed


def euler_correction(initial: Any, target: Any, step: Any, count: int) -> Fraction:
    """Exact rational discretisation of x'=target-x; stable convex steps only."""
    x=Fraction(initial); target=Fraction(target); h=Fraction(step)
    if not 0<=h<=1 or not isinstance(count,int) or count<0:
        raise ValueError('Require 0≤step≤1 and a nonnegative integer step count.')
    for _ in range(count): x=(1-h)*x+h*target
    return x


def replicator(weights: Mapping[S,Any], fitness: Mapping[S,Any]) -> dict[S,Fraction]:
    """A tangent field w_i(c_i-mean_w c) on a finite simplex."""
    w=normalise(weights)
    if not set(w).issubset(fitness): raise ValueError('Missing fitness value.')
    c={i:Fraction(fitness[i]) for i in w}
    mean=sum((w[i]*c[i] for i in w),Fraction(0))
    return {i:w[i]*(c[i]-mean) for i in w}


def audit_tangent(weights: Mapping[S,Any], factors: Mapping[S,Any], tangent: Mapping[S,Any]) -> dict[S,Fraction]:
    """Exact differential of the positive Bayes action on simplex tangents."""
    w=_mass(weights)
    if sum(w.values(),Fraction(0))!=1:raise ValueError('A normalised simplex point is required for its tangent differential.')
    if any(v<=0 for v in w.values()):raise ValueError('Interior weights required.')
    if not set(w).issubset(factors) or not set(w).issubset(tangent):raise ValueError('Incomplete tangent or factor.')
    r={i:Fraction(factors[i]) for i in w}; v={i:Fraction(tangent[i]) for i in w}
    if any(t<=0 for t in r.values()):raise ValueError('Strictly positive audit factors required.')
    if sum(v.values(),Fraction(0))!=0:raise ValueError('Simplex tangent must sum to zero.')
    Z=sum((w[i]*r[i] for i in w),Fraction(0)); dZ=sum((v[i]*r[i] for i in w),Fraction(0))
    return {i:r[i]*v[i]/Z-r[i]*w[i]*dZ/(Z*Z) for i in w}


def rational_weight_step(weights: Mapping[S,Any], potentials: Mapping[S,Any], step: Any) -> dict[S,Fraction]:
    """Positive, audit-equivariant, energy-nonincreasing frozen-potential step.

    Uses factors 1/(1+h*(V_i-min V)). The baseline is only numerical
    centring for this weight step; it does not redefine the position energy.
    Potentials and step selection must be unchanged by the weight audit.
    """
    w=normalise(weights); h=Fraction(step)
    if h<0:raise ValueError('Nonnegative step required.')
    if any(v<=0 for v in w.values()):raise ValueError('Strictly positive labelled weights required.')
    if not set(w).issubset(potentials):raise ValueError('Missing potential.')
    V={i:Fraction(potentials[i]) for i in w}; baseline=min(V.values())
    factors={i:Fraction(1)/(1+h*(V[i]-baseline)) for i in w}
    return tilt(w,factors)
