# CV-C — soft atomic mass, exact index classes and the finite-state exception

Status: PARTIAL obligation. The source classification is analysed at its declared total primitive-recursive synchronous scope. No counterexample to that scoped ordinary argument was found here. There is no new arithmetical-hierarchy or measure-theoretic Lean proof. The explicit syntax proposal below requires separate review and does not retroactively assign historical program indices.

## 1. Preserve the negative evidence first

A productive observer can have an undecidable zero-defect question; it is invalid to infer a decision algorithm from exact finite cylinder counts. The old Q8 binary halting family is a narrower subfamily, not a proof of CV-C's full Π₃ hardness. Conversely, a finite Mealy machine is not an arbitrary primitive-recursive observer. The finite-state algorithm in §6 does not weaken the general classification.

Strict and non-strict thresholds must not be exchanged. The conjunction `B(k,n)>r for every n` does not by itself imply `inf_n B(k,n)>r`: the rational sequence r+2^(-n) is an elementary counterexample. Forty checked terms in the finite script illustrate, but do not prove, this limit statement.

## 2. Exact semantic class and separately proposed numbering

The source fixes a syntactically total primitive-recursive integer program P_e with

    q_e(x)_n = P_e(n, code(x↾(n+1))) mod 2,

and invalid codes denote the constant-zero program. Thus every observer emits exactly one output bit at each stage, reads no future input bit, is total and 1-Lipschitz in the usual prefix metric. The universal evaluator for the PR class is total computable, not claimed primitive recursive uniformly in e.

**Proposed definition P02-C-SYNTAX-01, not adopted:** use arity-indexed finite syntax trees with constructors zero(k), successor, projection(k,i), composition(k,f,[g_1,...,g_l]), and primitive-recursion(k,g,h). The last has g of arity k, h of arity k+2 and denotes f(x,0)=g(x), f(x,n+1)=h(x,n,f(x,n)). A typed finite-tree parser rejects malformed constructors, arity mismatches and out-of-range projections. Enumerate finite tree strings by length and then lexicographically over a fixed finite alphabet; a decoded non-binary-arity tree or invalid string denotes the two-argument zero program. Encode finite binary words by the sentinel integer 2^length plus their binary value. All these encodings are proposals with fresh identities.

This specifies a usable semantic interface, but the byte-level parser, constructor encoding and uniform compiler are not implemented here. An exact numeric string-to-index codec must be frozen before code-level many-one reductions receive formal credit. The proofs below use a fixed effective numbering with the stated constructors and effective parameter substitution. They do not claim that a newly chosen numbering is byte-identical to an absent historical implementation.

## 3. P02-C01 — soft-mass representation with all limit directions

Let λ be the fair product measure on Cantor space, ν_e=(q_e)_*λ. For an output word σ of length n, let

    p_e(σ)=2^(-n) · #{u∈{0,1}^n : q_e(u)↾n=σ}.

Prefix causality makes this independent of the continuation of u. It is an exactly computable dyadic rational, uniformly in e and σ. Define for k≥0

    B_e(k,n)=Σ_{|σ|=n} max(p_e(σ)−2^(-k),0).

Splitting a cylinder of mass p into child masses p0,p1 decreases this soft mass: max(p0−ε,0)+max(p1−ε,0)≤max(p−ε,0). Hence B decreases in n and increases in k, with values in [0,1]. Write b_e(k)=inf_n B_e(k,n).

For y sampled according to ν_e, the mass m_n(y)=ν_e([y↾n]) decreases to m∞(y)=ν_e({y}) by continuity from above. Define φ_ε(0)=0 and φ_ε(t)=max(1−ε/t,0) for t>0. This function is continuous at zero because it vanishes for t≤ε. We have

    B_e(k,n)=∫ φ_(2^-k)(m_n(y)) dν_e(y).

Dominated convergence therefore gives

    b_e(k)=Σ_{y∈Sν_e} max(ν_e({y})−2^(-k),0).

Only countably many positive singletons occur. Monotone convergence as k→∞ gives the exact identity

    a(ν_e)=sup_k inf_n B_e(k,n),       d(ν_e)=1−a(ν_e).

Neither limit is replaced by a fixed finite search depth. In particular, every finite projection of the fair stream is atomic although the full law is not.

## 4. P02-C02 — exact upper bounds and threshold table

For rational r,

    a(ν_e)>r  iff  ∃k ∃t∈ℚ [t>r and ∀n B_e(k,n)≥t].

The forward implication chooses a genuine positive rational gap below b_e(k); the reverse takes an infimum. This is a Σ₂ formula with an effective matrix. The coding of pairs of existential witnesses is computable. Also a≥r iff ∀j a>r−2^(-j), giving a Π₃ description. Complementation and d=1−a then give, for each fixed rational 0<q<1:

| Property | Exact class claimed by source and justified by the reductions below |
|---|---|
| d<q | Σ₂-complete |
| d≥q | Π₂-complete |
| d≤q | Π₃-complete |
| d>q | Σ₃-complete |
| d=q | Π₃-complete |

For equality, d=q combines d≤q with d≥q; Π₂ is contained in Π₃ and Π₃ is closed under finite conjunction. Endpoint classes are d=0: Π₃-complete; d>0: Σ₃-complete; d=1: Π₂-complete; d<1: Σ₂-complete. Statements d<0 and d>1 are false, while d≥0 and d≤1 are true. Non-strict endpoint formulations reduce accordingly. These are computable many-one classifications of program-index sets in the declared effective numbering, not claims about an arbitrary presentation of real measures.

## 5. P02-C03 — uniform hardness witnesses and rational threshold shifts

**FIN/INF binary witness.** Given a c.e. set W_e with a primitive-recursive bounded stage simulation, copy the current fresh fair input bit at stages when a new element is enumerated; emit zero at every other stage. If W_e is finite, the output depends on finitely many random bits and has finite support, so d=0. If W_e is infinite, an output singleton fixes infinitely many independent input bits, so it has probability zero and d=1. The observer is synchronous and primitive recursive in each bounded prefix. This reduces FIN to d<q and d<1, and INF to d≥q and d=1. Here FIN is Σ₂-complete and INF is Π₂-complete in the conventional c.e.-set numbering.

The FIN completeness premise can itself be derived at the same scope. FIN is Σ₂ because there is a stage after which no new element is enumerated. Given any Σ₂ formula ∃s∀t R(e,s,t) with PR matrix, use the least surviving candidate at each bounded stage, as in the next paragraph, and enumerate a new member whenever it changes. The resulting set is finite exactly when a permanent witness exists. Complementation proves the INF claim. Applying this construction rowwise shows that the set of e for which every W_(e,i) is finite is Π₃-complete. Thus the hardness argument is not merely a borrowed classification label.

**Π₃ witness.** Fix a Π₃-complete predicate in normal form ∀i∃s∀t R(e,i,s,t), with primitive-recursive R. At stage u let r_i(u) be the least s≤u satisfying R(e,i,s,t) for every t≤u, or u+1 if none does. Once a candidate has failed a bounded test, it cannot reappear later; hence r_i is nondecreasing. If some permanent witness s exists, all smaller failing candidates are eventually eliminated and r_i stabilises. If no witness exists, every fixed candidate is eventually eliminated, so r_i is unbounded. Enumerate a new member into W_(e,i) whenever r_i changes. Then W_(e,i) is finite exactly when the existential-universal clause holds.

Use input selector prefixes 1^i0 of weight 2^(-i-1). Emit that prefix unchanged, then run the FIN/INF witness for W_(e,i) on the remaining independent input bits. On the all-ones input emit all ones; this exceptional selector path is productive and null. Components have disjoint output prefixes, and the countable-mixture identity gives

    d_e = Σ_i 2^(-i-1) · 1[W_(e,i) infinite].

Thus d_e=0 iff every clause holds. Bounded minimisation, bounded simulation and finite prefix parsing are PR operations, so the symbolic construction compiles uniformly into the declared class; an actual code-level compiler remains part of the formal handoff. Complementation yields Σ₃ hardness of positive defect.

**Any rational shift, not only dyadic q.** To obtain d'_e=q+(1−q)d_e, first compare a fair binary real with rational q using finite dyadic intervals. Emit the selector bits unchanged until its interval lies wholly below or above q. Below q, continue with a fair diffuse stream; above q, continue with q_e on fresh bits. Distinct stopping prefixes are disjoint output cylinders. The unresolved interval after n bits has mass at most 2^(-n); for non-dyadic q the one indefinitely unresolved path is null. At dyadic q, the comparison terminates after a uniform finite number of bits. Endpoints are immediate.

Consequently the total weight of diffuse components is exactly q and of q_e components is 1−q. Each stage uses rational integer comparisons and bounded prefix operations, so the construction remains synchronous and PR. The countable-mixture law proves the displayed affine defect formula. For q<1, d'_e≤q and d'_e=q are both equivalent to d_e=0, while d'_e>q iff d_e>0. This supplies the Π₃/Σ₃ threshold hardness without changing a strict comparison to a non-strict one.

## 6. P02-C04 — exact finite Mealy algorithm and its ordinary proof

A binary synchronous Mealy machine has a finite nonempty state set S, transitions δ(s,b) and output bits o(s,b), driven by independent fair bits. Define E as the greatest relation on S×S such that, whenever (s,t)∈E, for every b,c∈{0,1},

    o(s,b)=o(t,c) and (δ(s,b),δ(t,c))∈E.

This is cross-input equality, not merely bisimulation under equal inputs. Starting from S×S and deleting violations reaches the greatest relation after at most |S|² strict deletion rounds. Let D={s:(s,s)∈E}. Exactly these states yield one fixed infinite output for every input stream. D is transition-closed. Following, for instance, all-zero inputs from a state in D shows that the fixed output is eventually periodic.

Let τ be the first hitting time of D. All paths hitting D produce an output in a countable set: choose a finite input prefix up to the hit and then one of the finitely many deterministic tails. Every output actually produced in this manner has positive mass, since its finite hitting prefix has positive probability.

For s∉D there are two finite input words with different output words. Finiteness of S gives a uniform length L≥1 such that each non-D state has such witnesses of length at most L; extend them to length L. For any prescribed output block, at least one of those length-L input words fails to match, and has probability 2^(-L). Thus the probability of matching j consecutive prescribed blocks while avoiding D is at most (1−2^(-L))^j, which tends to zero. For any fixed output stream y, its probability on {τ=∞} is therefore zero. The positive-output-singleton set is countable, so its intersection with {τ=∞} is also null. It follows exactly that

    a_s = Pr_s(τ<∞),        d_s = Pr_s(τ=∞).

This proof handles atoms produced by a random finite prefix followed by deterministic tails; it does not equate atomicity with starting in D.

Compute the states R from which D is reachable. Set h=1 on D and h=0 on S\R. On H=R\D solve

    h_s = (h_(δ(s,0))+h_(δ(s,1)))/2.

There is no closed recurrent class wholly inside H, since every H-state has a positive-probability path to D. Equivalently, finiteness gives a uniform block length and a positive chance to leave H in each such block. Its transition submatrix is transient, so I−P_H is invertible. Exact rational elimination yields the unique hitting probabilities; every rational threshold comparison is decidable. This is not an algorithm for unbounded PR observers.

## 7. Executed evidence and limits

The separate Python implementation uses exact `Fraction` arithmetic, greatest-relation iteration and a linear solve. An independent determinism oracle evolves the set of possible current states, checking uniform output at each stage until a reachable-state subset repeats. It does not reuse the pair relation.

All 46,656 labelled three-state binary machines were checked, with 139,968 statewise probability/Bellman checks. Both determinism procedures agreed. Normal and optimised subprocesses produced byte-identical raw rows and result JSON. A four-state fixture checks a nontrivial hitting probability 1/3; delayed-distinguishing and random-prefix fixtures reject two tempting incorrect shortcuts. The row population and six scoped negative illustrations are fully recorded. This is a bounded executable census, not a universal implementation refinement proof, hierarchy proof, Lean audit, or independent external review.

## 8. Literature and remaining formal work

`LITERATURE_COMPARISON.md` distinguishes existing atomic/trivial measure and tally-functional work from this exact PR-synchronous index claim. No exact-priority result or novelty claim follows from the limited search.

Open formal tasks are the concrete codec/compiler, product probability construction, exact cylinder counting, C01's integral/limit identity, arithmetic-set definitions and uniform many-one reductions, rational shift construction, and the finite-state hitting theorem plus implementation correspondence. There is no supplied CV-C Lean module pretending these tasks were discharged by axioms or assumptions. Q1c finite probability work does not automatically close them.
