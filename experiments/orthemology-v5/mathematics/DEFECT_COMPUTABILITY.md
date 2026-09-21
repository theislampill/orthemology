# CV-C — Exact computability of the point-concentration defect

Status: ordinary mathematical proof; not Lean-checked or independently refereed.
Continues Q8. Priority is OPEN. The probability property d=0 is the established
property of being a purely point-atomic ("trivial", in algorithmic randomness)
probability measure. It is NOT the zero measure.

## 1. Fix the effective presentation before classifying anything
Let λ be fair-coin measure on Cantor space 2^N. Use a decidable syntax of primitive
recursive integer programs. An index e specifies the bit

    q_e(x)_n = P_e(n, encode(x restricted to n+1)) mod 2.

Invalid syntax denotes the constantly-zero program. Every index denotes a total,
productive, synchronous, 1-Lipschitz observer. Its execution time is not bounded
uniformly by the output length. Universal evaluation of this syntax is total
computable, although not primitive recursive as a function of arbitrary indices.
Put ν_e=(q_e)_*λ and d_e=1−Σ_x ν_e({x}).

For every output word σ of length n, p_e(σ)=ν_e([σ]) is an exactly computable dyadic
rational: enumerate the 2^n input prefixes and evaluate their n output bits.
All complexity statements below are for THIS total effective presentation, not
for arbitrary partial machine indices promised to be productive.

## 2. Original Q8: Π1-completeness on its original indexed subfamily
Let H_e be the observer which emits zero until the fixed-input machine M_e halts,
and then copies fresh input bits forever. A bounded n-step simulation suffices
to compute each output bit, so e↦H_e is a computable map into the syntax above.

If M_e never halts, the law is δ_{0^∞}, so d=0. If it halts at t, an infinite fair
tail remains, every singleton has probability zero, and d=1. Therefore

    {e:d((H_e)_*λ)=0} is Π^0_1-complete,
    {e:d((H_e)_*λ)>0} is Σ^0_1-complete,

under computable many-one reductions. These are exactly non-halting and halting
in a fixed acceptable machine enumeration. They are not classifications for all
productive observers; the next construction increases the quantifier complexity.

## 3. Uniform upper bounds from finite cylinders
For k,n≥0 define the computable rational

    B_e(k,n)=Σ_{|σ|=n} max(p_e(σ)−2^(−k),0).

For fixed k this is nonincreasing in n, because splitting a nonnegative mass p
into p_0+p_1 can only decrease Σ_i max(p_i−ε,0). For fixed n it is nondecreasing
in k. Write b_e(k)=inf_n B_e(k,n).

For an output y sampled from ν_e, let m_n(y)=ν_e([y restricted to n]). Then
m_n(y) decreases to ν_e({y}). Integrating

    φ_ε(m) = max(1−ε/m,0) for m>0, and φ_ε(0)=0

gives E[φ_ε(m_n)]=Σ_{|σ|=n}max(p_e(σ)−ε,0). The functions are bounded by one and
converge pointwise, so bounded convergence proves

    b_e(k)=Σ_{x:ν_e({x})>0}max(ν_e({x})−2^(−k),0).

Monotone convergence in k now yields the exact representation

    a(ν_e)=sup_k inf_n B_e(k,n).                         (C-mass)

No positive atoms need to be computably enumerated for this formula.

For a rational r, a(ν_e)>r iff there exist k and rational t>r such that
∀n B_e(k,n)≥t. The gap t−r is essential: merely requiring B_e(k,n)>r for every n
would admit an infimum equal to r. All rational comparisons here are decidable.
Thus the strict lower cut of a is Σ^0_2. Taking rational approximations to a
nonstrict threshold adds one outer universal number quantifier.

## 4. Exact threshold hierarchy
For any fixed rational q with 0<q<1, the index sets have these complexities:

| Property | Exact complexity |
|---|---|
| d_e<q | Σ^0_2-complete |
| d_e≥q | Π^0_2-complete |
| d_e≤q | Π^0_3-complete |
| d_e>q | Σ^0_3-complete |
| d_e=q | Π^0_3-complete |

Endpoints: d_e=0 is Π^0_3-complete; d_e>0 is Σ^0_3-complete;
d_e=1 is Π^0_2-complete; d_e<1 is Σ^0_2-complete. The other out-of-range or
endpoint inequalities are empty or universal as dictated by 0≤d_e≤1.

### Upper bounds
From C-mass, d_e<q iff a(ν_e)>1−q, which is Σ2; complement gives d_e≥q in Π2.
Also

    a(ν_e)≥r iff ∀m≥1, a(ν_e)>r−2^(−m).

Expanding the strict comparison gives Π3 for d_e≤q. Complement gives Σ3 for d_e>q.
Equality is the conjunction of Π3 and Π2 properties, hence Π3. For q=1, equality
reduces to a=0, a Π2 statement. No statement is weakened to mere undecidability.

### FIN/INF lower bounds
Let W_e be the e-th computably enumerable set with a fixed bounded-stage
approximation. Form J_e by copying input bit n precisely at stages n when W_e
gains a new member; otherwise emit zero. Each output bit uses bounded simulation.

If W_e is finite, the entire output contains only finitely many random bits and
its law has finite support: d=0. If W_e is infinite, infinitely many independent
bits are copied: every singleton probability is bounded by 2^(−j) for arbitrarily
large j, so d=1. Thus FIN reduces to d<q and INF to d≥q for every 0<q≤1. FIN is
Σ2-complete and INF Π2-complete. This proves the first pair of exact bounds.

### A Π3-hard zero-defect family
Consider a uniformly c.e. array (W_{e,i})_{i≥0}. First use the input prefix 1^i0 to
select i, with probability w_i=2^(−i−1), and emit that same prefix. On the remaining
fresh input bits run J_{e,i}. The input 1^∞ has probability zero and maps to itself.
This is a total primitive-recursive synchronous observer: each finite output
prefix needs only its finite input prefix and bounded enumeration simulations.
The emitted selectors make component output sets disjoint. Therefore

    d_e=Σ_{i≥0}2^(−i−1) 1_{W_{e,i} infinite}.           (C-mixture)

In particular d_e=0 iff every W_{e,i} is finite.

For completeness, the latter property is Π3-hard, not just syntactically Π3.
Given any Π3 predicate ∀i∃s∀t R(e,i,s,t) with primitive-recursive R, at stage u let
r_{i,u} be the least s≤u passing R(e,i,s,t) for every t≤u, or u+1 when none does.
The sequence r_{i,u} is nondecreasing. If a permanently passing s exists, it is
eventually bounded by that s and changes only finitely often. If no such s exists,
every finite candidate is eventually eliminated, r_{i,u} is unbounded, and it
changes infinitely often. Enumerate a new element into W_{e,i} at each change.
Then W_{e,i} is finite iff ∃s∀t R(e,i,s,t). This is a uniform computable reduction.
Together with C-mixture it proves Π3-hardness of zero defect and Σ3-hardness of
positive defect. The upper bounds prove completeness.

### Shift to every rational threshold
For a fixed 0≤q<1, form a disjoint tagged mixture with diffuse mass q and remaining
mass 1−q carrying the preceding ν_e. Its defect is

    q+(1−q)d_e.

For dyadic q, a fixed finite prefix of fair bits implements the selector exactly.
For any other rational q, reveal a fair binary real until its dyadic cell lies
entirely below q or entirely above q, emitting that selector prefix. Stopping
prefixes are prefix-free and have total mass one. Conditional on each finite
prefix, the remaining bits are independent and fair. The unique boundary input,
if never decided, is mapped productively by continuing to emit its bits and has
measure zero. After a decision run the chosen observer on the untouched tail.
Endpoint comparisons with rational q are bounded integer computations, so this
is again a total primitive-recursive synchronous observer. Prefix-free tags
prevent collisions between different selected components. Hence the defect
formula holds exactly, without assuming a rational primitive randomness source.

It follows that d≤q and d=q hold exactly when the encoded original d_e is zero;
d>q holds exactly when it is positive. These establish the remaining lower bounds.

## 5. Finite-state observers: exact decidability, not merely an upper bound
Now restrict the description to a finite synchronous Mealy machine: finite state
set S, initial s_0, transition δ:S×{0,1}→S and output o:S×{0,1}→{0,1}. Input bits
are independent fair bits. Define E as the greatest subset of S×S such that for
all b,c,

    (s,t)∈E ⇒ o(s,b)=o(t,c) and (δ(s,b),δ(t,c))∈E.

A decreasing finite relation computation finds E. Let D={s:(s,s)∈E}. A state is
in D exactly when every possible input stream produces the same output stream.
Necessity follows by comparing all finite input pairs; sufficiency by induction
on prefix length. The finite-state relation iteration is complete because every
failed pair has a finite distinguishing prefix. D is transition closed. Its
unique output from each state is eventually periodic (follow, for example,
the all-zero input through finitely many states).

Every run hitting D produces a finite prefix followed by one of finitely many
fixed tails. The set of such outputs is countable, and every output reached by
a finite hitting prefix has positive probability.

Conversely every state outside D has two finite, equally long input words with
different outputs. Finiteness supplies a common L and δ_*=2^(−L)>0. For any fixed
target output block of length L, from any such state its probability is at most
1−δ_*: at least one of the two witnessing words is incompatible. The probability
of matching j successive target blocks while avoiding D is therefore at most
(1−δ_*)^j. Each fixed infinite output has probability zero on runs avoiding D.
Countable union shows these runs give no additional mass to the atomic outputs.
Thus

    a(ν)=Pr(eventually hit D),
    d(ν)=Pr(never hit D).                              (C-finite-state)

This is an exact finite Markov-chain reachability probability. States unable to
reach D have hitting probability zero; D has hitting probability one. On all
other states solve h(s)=(h(δ(s,0))+h(δ(s,1)))/2. The resulting rational linear
system is nonsingular: from each remaining state there is a uniformly bounded
positive-probability path out of that transient subgraph. Gaussian elimination
over rationals computes h(s_0) exactly. Every rational defect threshold is
therefore decidable for this finite-state class.

This classification does not extend to observers with an unbounded computable
control state. They can implement the earlier bounded-simulation constructions.

## 6. Effective presentations and limits of the claims
For any promised uniform presentation with computable cylinder probabilities,
computable rational enclosures give an analogous sup-inf approximation, hence
the same upper arithmetical bounds relative to valid names. Establishing raw
index-set completeness for an arbitrary numbering additionally requires analysing
which names are valid and the complexity of totality. The present theorem avoids
that hidden promise by a syntactically total language. It does not classify all
partial Turing functionals or all higher-type computable descriptions.

The threshold table rules out a sound complete recursively enumerable finite
certificate system for zero defect in this class. Sound incomplete checking is
possible. The v4 finite invariant certificate is one such restricted fragment.
There is no claim that all these infinite laws can be estimated by the Python
engine, or that finite prefix experiments prove the hierarchy theorem.

## 7. Prior-work boundary
The defect is the mass of the standard diffuse component. Porter (2015) studies
computable trivial measures and uses tally functionals to encode logical
behaviour into stream outputs. Thus neither atomicity nor the general encoding
technique is new. Kaminski–Katoen analyse different index sets: probabilistic
termination and expected outcomes. Our theorem's distinguishing object is the
atomic mass of a TOTAL synchronous observer's output law, with the exact table
above and a finite-state exception. An equivalent index theorem may already
exist. No priority conclusion follows from the current bounded literature search.
