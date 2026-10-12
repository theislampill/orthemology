# Mathematical assessment of the scriptural fibre supplement

9 October 2026. A bounded application check of inherited mathematics. The conclusions concern declared finite models, not the actual history or doctrinal truth of any scripture. No prior research result is changed.

## Result

The fibre argument has a valid conditional core. An admissible pair of histories with the same retained observations and different target values defeats uniform exact reconstruction. Under the inherited finite full-simplex moment model, an appropriate separating binary predicate then has defect exactly 1/2.

The additional conclusions need their own mappings: a specified scalar predicate, a moment representation of laws, an explicit continuation contract, and a separate account of epistemic warrant. The first attachment already requests these distinctions. The second can be read consistently with them; parts of the third pass over them or change targets. Neither a positive historical defect nor a zero historical defect is established for a named scripture by the supplied packet.

## Sources actually checked

All three supplied Library texts were read completely. Their identities and the status of local text projections are recorded in INPUT_PROVENANCE.json.

The originally named local inherited file was absent. The following bounded source windows were freshly retrieved from the public repository at commit 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c:

- [H formalisation Theorem 4.2 and Corollary 4.3](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-formalisation/orthing_formalisation_v1.md#L248-L299), source lines 248–299; returned blob c094a9c44fae26484426df67ac5afd9e2190eb4d.
- [H continuation objects and Theorems 1–2](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-continuation/continuation_complete_orthing.md#L108-L292), within the retrieved lines 1–320.
- [H continuation Proposition 9 and conditioning margins](https://github.com/theislampill/orthemology/blob/7efc6217c090b92d65f2c4cb8b011c18eb96bf7c/theory/lineages/h-continuation/continuation_complete_orthing.md#L604-L670), within retrieved lines 565–675; continuation blob 99d0434aad8b8a841f59eb078e2b70c0b961d226.

These blobs match the inherited lineage's recorded source identities. Exact returned excerpts and their line windows are preserved in math-sources/ and MATH_SOURCE_BINDINGS.json. This is a fresh targeted reading, not a full-file reread, repository replay, current-main assertion, or new general theorem.

## 1 What the fibre theorem actually says

For any set D and maps r:D→R and q:D→Q, exact decoding on r(D) exists precisely when q is constant on each r-fibre. No finite-domain or probability assumption is needed for this statement.

For a composite target q=(author, wording), failure means that at least one required component varies on some fibre. It does not mean that every authorship proposition, every wording proposition, or every consequence of the text varies. For a particular binary claim, define its predicate f:D→{0,1} explicitly and show that this predicate separates the proposed histories.

A global counterexample defeats a universal guarantee. To establish ambiguity at the actual observed record r*, the two histories must lie in that record's fibre. Finiteness of the observation panel alone establishes neither kind of ambiguity. Historical admissibility, the observation map, and target equality must be justified rather than built to assume the conclusion.

## 2 The exact bridge to moment defect

The inherited moment theorem requires a finite nonempty state set D, a linear space V⊆R^D containing 1, and every law λ∈Δ(D). Its retained information is

m_V(λ) = (E_λ φ₁, …, E_λ φ_k),

not the observed value r(d). For a scalar f∈R^D, its target is E_λ f. Even arbitrary nonlinear decoders of these moments have optimal worst-case absolute expectation error

d_V(f) = min[g∈V] ||f−g||∞
       = ½ max[m_V(λ)=m_V(λ′)] |E_λ f−E_λ′ f|.

“Finite-support representation” does not establish that the historical state set is finite, that all its laws are admitted, or that a historical panel has been encoded as this moment map.

For the precise connection, put B_r={h∘r:h:r(D)→R}. If every retained numerical feature depends only on r, then V⊆B_r.

- Raw scalar recovery is f∈B_r.
- Universal moment-expectation recovery is f∈V.
- If r(d)=r(d′) but f(d)=1 and f(d′)=0, the Dirac laws δ_d and δ_d′ have equal retained moments and target separation 1. Hence d_V(f)≥1/2. The retained constant approximant g=1/2 gives the reverse bound, so d_V(f)=1/2 exactly.
- If a composite q fails the fibre criterion, some predicate 1{q=z} separates a witnessing pair. This proves the previous conclusion for that predicate, not every binary claim concerning q.
- The converse fails for a smaller feature span: positive moment defect need not mean failure to decode f from the raw panel. It becomes equivalent for scalar f when V=B_r.

Restricted prior families or attainable laws require a separately restricted minimax problem. Their decoding error can be smaller than d_V(f); the full-simplex equality cannot simply be carried over. No investigator's prior or personal error probability is selected by the theorem.

### Finite counterexample A Raw recovery with maximal moment defect

Let D={−1,0,1}, r(x)=x, V=span{1,x}, and f(x)=x²=1{x≠0}. The raw observation identifies the state and f exactly. Nevertheless,

λ=(1/2,0,1/2), λ′=(0,1,0)

both have E x=0, while E_λ f=1 and E_λ′ f=0. The equal-moment witness gives d_V(f)≥1/2; g=1/2 has uniform error 1/2. Thus d_V(f)=1/2 despite perfect deterministic identifiability.

This is a law-versus-observed-point distinction, not a failure of the inherited theorem.

## 3 Continuation completeness and augmentation

The actual source starts with required terminal observables F_A and defines

C₀=span({1}∪F_A),
C_{h+1}=C_h+Σ_{a,o} K_{a,o}C_h.

The finite nonnegative action–observation instruments satisfy Σ_{o,x′}K_{a,o}(x,x′)=1. The theorem preserves the specified branch probabilities and terminal numerators for every law exactly iff C_h⊆V. Conditional answers additionally require positive branch probability. These spans are generated from the required contract and permitted operators, not merely from the current observations.

The correct obstruction is a required function f∈C_h\V. If a separating target predicate is explicitly in F_A, it is already in C₀. Then the valid fibre-to-defect bridge also entails continuation incompleteness at every horizon.

The second attachment's phrase “outside the span generated by the presently available observations” can mean f∉V and is valid with that contract declaration. Its displayed containment test is correct. The third attachment's “outside the continuation span of the panel” is ambiguous: taken literally as f∉C_h, it says the current contract does not cover that target, not that the contract is incompletely represented. The needed correction is to state the contract rather than reverse either theorem.

Proposition 9 gives

a_min = dim(V+C_h)−dim(V).

It counts additional continuous real-valued statistics of the law under ideal access; a complementary basis of moments attains the bound. It does not count manuscripts, independent witnesses, queries, time, or historically obtainable evidence. If all obtainable additions remain functions of the same r, they cannot separate an r-fibre. An abstract one-coordinate augmentation by an unknown f does not make that coordinate obtainable.

### Finite counterexample B Composite failure with a recoverable component

Take two histories d₀,d₁ with r(d₀)=r(d₁)=0 and

q(d₀)=(author α, wording W),
q(d₁)=(author β, wording W).

Let V=span{1}. The combined q is not recoverable. For f=1{author=α}=(1,0), the two Dirac laws and the approximant 1/2 certify d_V(f)=1/2. For the wording predicate g=1{wording=W}=(1,1), d_V(g)=0.

Use one action, one certain observation, and K=I. With a contract requiring only g, every C_h=span{1}; the representation is continuation-complete and a_min=0. Once the authorship predicate f is required, every C_h=span{1,f}; it is incomplete and a_min=1. The missing target must be part of the contract before this conclusion follows.

## 4 Minimax error does not settle actual warrant

In counterexample B, stipulate the separate prior π(d₀)=99/100, π(d₁)=1/100. The constant observation leaves that prior unchanged. The posterior probability of α is 99/100, and choosing α has Bayes classification error 1/100.

At the same time:

- Absolute expectation-estimation minimax error over all laws is 1/2.
- Randomised binary classification minimax error over the two states is 1/2.
- Deterministic binary classification minimax error is 1.

These are different losses and quantifiers. The example does not establish that the stipulated prior is warranted; it shows that the defect alone cannot establish a personal error probability or absence of probabilistic warrant.

A target-varying observed fibre defeats infallible reconstruction from that panel over the admitted alternatives. Calling every high-confidence output improperly functioning additionally assumes a truth-directed design plan that requires this uniform zero-error guarantee. Neither inherited theorem supplies that normative premise or reduces proper-functionalist warrant to worst-case reconstruction.

## 5 What remains open for the proposed comparison

The third text begins with combined exact authorship and original wording, but its zero-defect discussion turns to standardised or received wording. Those are different targets. Recovering a coarser target does not establish recovery of the original composite. A comparison must declare each target without silently importing the conclusion from another.

For any future case, the minimum useful record is: a justified history class, actual retained record, exact target predicate, and either an admissible target-separating pair or an explicit recovery argument. A moment claim additionally needs its finite model, feature space and admitted laws; a continuation claim needs its terminal contract, instruments and horizon. Oral-transmission reports and written witnesses belong in that model according to their actual evidential roles. Their number or asserted independence does not by itself prove zero defect.

The genuinely new work here is the source-bound application crosswalk and two discriminating countermodels. The general factorisation, defect, continuation and augmentation results remain inherited. Historical scripture comparison, sufficient epistemic warrant, and the further theological argument remain separately open.

## Exact check

Run python check_math_transport.py from this folder. MATH_CHECK_RESULTS.json records a successful exact-rational run. It checks matching primal and equal-moment dual certificates, ranks, identity-kernel closures, target separation, and the stated risks for the two finite models. No historical input, floating-point approximation, new dependency, or independent general-theorem certification is claimed.

