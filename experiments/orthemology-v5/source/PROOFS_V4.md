# SAME v4 continuation: ordinary proofs and their exact scope

**Status.** The arguments in this document are ordinary mathematical proofs,
subject to further review. The Lean sources are uncompiled candidates. No theorem
here receives kernel credit from Python tests, static source inspection, an audit
fixture, or an exported Lean file. Original T01–T24 and their limitations remain
under `history/Orthemology_v3_Critical_Handoff/inputs/v3/`.

The positive internal requirement is unchanged: in the preserved realisability
model, `All(B)` belongs to the same semantic code universe C over which it ranges.
Instantiation at that very code is legal. The finite source grammar is a subset
of the semantic code universe, not a syntax for every predicate on programs.

## V4-Q1 — exact quantitative observation-refinement identity

Let nu' be a probability measure on Y', h:Y'→Y measurable, and nu=h_*nu'. Assume
singletons in both spaces are measurable. For any such probability lambda write
S_lambda={y:lambda({y})>0}, a(lambda)=lambda(S_lambda), d(lambda)=1-a(lambda).
These are **positive point masses**, not arbitrary indivisible measurable sets.

S_lambda is countable: for each integer n≥1, at most n points have mass≥1/n,
and their union contains every positive point. Thus it is measurable.

For y∈S_nu let w_y=nu({y}) and define the probability law on Y'

    rho_y(B) = nu'(B ∩ h⁻¹({y}))/w_y.

Only positive fibres are used; this is restriction and division, not an assumed
general disintegration theorem. Every positive point z of nu' maps to a positive
point h(z) of nu. Moreover rho_y({z})=nu'({z})/w_y in that fibre and is zero
outside it. Partitioning the countable set S_nu' by h gives

    a(nu') = Σ_(y∈S_nu) w_y a(rho_y).

Since Σ_y w_y=a(nu), subtraction from one yields exactly

    d(nu') = d(nu) + Σ_(y∈S_nu) w_y d(rho_y).              (Q1)

Every sum is countable and nonnegative. In particular d(nu')≥d(nu). Equality
holds iff d(rho_y)=0 for **each positive coarse fibre**: all w_y are positive,
and a sum of nonnegative summands vanishes iff each summand vanishes. Nothing is
required of null fibres, and arbitrary regular conditional laws on them play no
role. This proves the accepted monotonicity and equality statements.

## V4-Q2 — sharp worst unrestricted almost-sure intersection failure

For all families A of measurable lambda-conull sets whose intersection is
measurable, the minimum intersection mass is a(lambda), and is attained.
Every conull set contains every positive point; otherwise its complement has
positive mass. Hence every eligible intersection contains S_lambda. Conversely
use the family {Y\{y}: y∉S_lambda}; its members are measurable and conull, and
its intersection is exactly the measurable S_lambda. Consequently d(lambda) is
the largest possible failure mass of the universal conjunction, despite each
individual requirement having probability one.

The event repertoire is load-bearing. This equality concerns the **full
measurable repertoire**, or another repertoire rich enough to supply the stated
separating family. For a restricted repertoire it gives an upper bound on
possible failure, not necessarily an attained bound.

If Y is countable then lambda(S_lambda)=1 by countable additivity. Thus the
defect is zero on any unchanged countable program-output carrier, even with
irrational point probabilities. Finitely described programs, their finite
outputs, complete random streams, and measures over them are different objects.

## V4-Q3 — transport of a probabilistic certificate

Under the hypotheses of Q1 and Q2, a coarse certificate d(nu)≤epsilon does not
establish the refined certificate. The exact additional obligation is

    d(nu) + Σ_y w_y d(rho_y) ≤ epsilon.                    (Q3)

Conversely this inequality does establish the refined bound, by Q1. A sound
upper bound for each conditional defect is sufficient, though not necessarily
necessary, when exact values are unavailable. Neither statement computes a law
from arbitrary empirical samples or from a field named `defect`.

Under coarsening the old finer bound remains semantically sufficient, because
d(coarse)≤d(fine). That does not automatically preserve operational authority:
the context may have changed its rule, law identity, interpretation or permission.
The implementation therefore checks the new context and issues a new licence.

For a composable finite chain of observation refinements, the nonnegative
increments telescope: d(nu_n)=d(nu_0)+Σ_(i<n)(d(nu_(i+1))-d(nu_i)). This is a
useful budget ledger, not a novel fixed-point or convergence theorem.

## V4-Q4 — limits do not preserve the needed condition automatically

Uniform grid laws on [0,1] have defect zero and converge weakly to the uniform
law, whose defect is one. For every continuous test function the integrals are
Riemann sums. Thus d is not lower semicontinuous.

Uniform laws on [0,1/n] have defect one and converge weakly to delta_0, of defect
zero: their integrals converge to f(0) for every bounded continuous f by
continuity at zero. Thus d is not upper semicontinuous either.

The first n fair bits form a finite observation space, always of defect zero.
The complete fair stream has no positive singleton and has defect one. The
limiting observation object and measurable event repertoire have changed. This
is not a counterexample on an unchanged countable output carrier.

## V4-Q5 — finite invariant-extension criterion

Let every f in a family F be invariant on the edges of a relation R on X.
Define x≡_F y iff every f has equal value on x and y. For proposed new edges S,

    F remains invariant on EqClosure(R∪S) iff S⊆≡_F.

Necessity follows from inclusion of each S-edge in the closure. For sufficiency,
equalities are preserved along R, S, reflexivity, symmetry and transitivity;
induction on the equivalence-closure construction proves the assertion. For
finite explicit F and S the edge/predicate comparison is a complete finite
checker. It is not a decision procedure over all semantic predicates.

`Engine` binds edge licences to the global active-vocabulary version as well as
the individual observations. This handles the case of **adding a new predicate**,
which an old list of positive dependencies alone would miss.

## V4-Q6 — the exact law grammar actually checked by observations.py

Two carriers are implemented. On a finite program carrier, a view is an explicit
partition and refinement requires a coarsening factorisation; every defect is
zero. On a disjoint tagged union of unit intervals, weights are nonnegative
normalised rational numbers. View 0 hides the coordinate, view m>0 returns its
m equal-width bin, and view -1 reveals its real coordinate. The tag is retained.

Hidden or binned components contribute their full weight to positive point mass;
fully revealed uniform components contribute zero. Hence the defect is the sum
of weights with view -1. A hidden or m-binned positive component newly revealed
has m coarse atoms each of mass w/m (one if hidden), each with conditional defect
one. A still finitely binned component has conditional defect zero. An already
revealed component has no positive coarse points to add. These cases prove the
exact calculation in `refinement`; finite bin divisibility checks prove its
claimed factorisation. Zero-weight fibres are correctly omitted.

The model checker does not accept a caller-supplied defect or a generic
`arbitrary-measure` tag. Law identity, weights, event repertoire and observation
map are independently represented, validated and fingerprinted. Relating this
declared model to an actual instrument remains an explicit trusted-host burden.

## V4-Q7 — countable property families are a different case

If (A_n) is a countable family of measurable probability-one events, then
lambda(∩_n A_n)=1, on **any** probability space: the complement is a countable
union of null events. In particular neither finite active vocabularies nor a
countable family of finite source predicates alone gives the full-repertoire
counterexample of Q2. A certificate for the full measurable repertoire is a
stronger optional requirement. The operational examples explicitly request it;
it is not inferred from the finite pure source type grammar.

Countability of the set of finite source strings does **not** by itself make
all semantic instances countable: one finite expression B can still range over
the entire semantic code universe. Q7 applies to an actually countable family
of events, not to an uncountably parameterised family merely described by finite
syntax. The protected semantic All retains its full declared range.

## V4-Q8 — an effective boundary for arbitrary productive observations

**Ordinary result; not kernel-checked and not a priority claim.** Let Cantor space
2^N carry fair product measure and its Borel sets. There is a uniformly computable
family of total 1-Lipschitz maps q_e:2^N→2^N for which deciding d((q_e)_*mu)=0 is
undecidable. Indeed that safe class is not recursively enumerable.

Let M_e be an arbitrary program on its fixed input. Number output positions from n=1. Define the nth output bit
of q_e(x) to be x_n if M_e has halted within n simulated steps, and zero otherwise.
A finite output prefix requires only a bounded simulation; so q_e is uniformly
computable and productive regardless of M_e's termination. Equal length-n input
prefixes give equal length-n outputs, proving 1-Lipschitz continuity in the usual
prefix metric.

If M_e never halts, q_e is the constant zero stream, and its law has defect zero.
If M_e halts at time T, q_e emits a fixed finite zero prefix followed by a fair
infinite tail. Every singleton has probability zero, and the law has defect one.
Thus

    d((q_e)_*mu) = 0 iff M_e does not halt,
    d((q_e)_*mu) = 1 iff M_e halts.

A total decision algorithm would decide halting. A recursively enumerable safe
class would enumerate nonhalting; interleaving this enumeration with the usual
halting simulation would again decide halting. The latter is impossible by the
standard diagonal argument: a decider H would allow a program to loop exactly
when H predicts its self-application halts, and halt otherwise.

It follows that there is no sound **and complete** recursively checkable finite
certificate system proving zero defect for all these productive observation
sources. Enumerating finite candidate certificates would enumerate the safe
class. This does NOT prohibit sound incomplete checkers or complete checkers for
a suitably restricted decidable grammar.

Every finite-prefix observation q_e^n still has defect zero, since its outcome
space is finite. For every fixed finite n a machine that halts later is
indistinguishable from a nonhalting machine through that observation. This makes
the finite/infinite and event-expressiveness boundaries particularly explicit.

`productive_observer.py` implements bounded prefixes of a concrete finite binary
tape-machine grammar and a sound sufficient certificate: an explicit set of
nonhalting control states containing the initial state and closed under both
read-symbol transitions. Induction on simulated steps proves the machine never
leaves that set and never halts; the ideal observed stream is therefore constant,
with defect zero. The actual checker enumerates all those obligations. An
unreachable halting state outside the invariant is permitted. Failure to find
such an invariant is not a proof of non-atomicity. A finite observed halt is a
positive witness of the non-atomic full-stream law under the fair-input model.

The mathematical undecidability result ranges over arbitrarily large finite
program descriptions. The reference API's fixed 64-state/128-prefix cap is NOT
an undecidable finite input space, and finite tests do not prove undecidability.
The new engine operation `observer` admits a supplied invariant only after that
finite check, transforms actual bit prefixes, and participates in permission
addition/revocation and dependency binding. No generic law-estimation oracle was
introduced. General probabilistic-program undecidability is established prior
art; this reduction specialises it to the present defect and observation target.

## V4-O1 — actual fixed-K operational construction

During an engine run, K is the fixed candidate grammar, parser, type rules,
primitive interpretations, certificate checkers and dispatch implementation.
Gamma consists of policy versions/permissions, active invariant vocabulary,
probability models and their versions, operation-specific obligations (including
their absence), the issued-record registry, a unique native issuer identity and
revision counter. Engineering changes between source versions require fresh
qualification; they are not themselves Gamma-only revisions under fixed code.

Compilation is structural on a bounded finite AST. Interfaces are nat (bounded
256-bit naturals), bool, unit, products and finite carriers, plus explicitly
controlled core-proof, bit-prefix and sampler-result interfaces. Operations
include identity, copying, projections, successor, zero test, negation,
composition, parallel composition, checked internal-source application, certified
selectors, invariant-preserving edges, typed threshold sampling and certified
productive-observer prefixes. No caller Python function is executed.

Admissibility first checks the actual code/certificates, not a `pass` field.
Every rule in the dependency closure must be enabled. Probability requirements
are looked up from Gamma and checked by Q6; caller-supplied evidence cannot
replace them. Every ordinary dependency also records `need:key` even when the
probability obligation is ABSENT. This negative dependency ensures that adding
a new obligation invalidates licences issued before it existed.

The compiled plan, canonical source bytes and exact dependency stamps are stored
in an immutable issued record. A native licence also carries the issuing Engine's
identity. Tokens are never reused within that registry; repeated entropy is
retried a bounded number of times and then refused. Thus an entropy collision
cannot overwrite a revoked record. Equal token text in different engines cannot
cross-authorise because issuer identity is checked independently. This is a
process-local capability discipline, not remote authentication or protection
against hostile Python code mutating private engine fields.

## V4-O2 — success preservation and executable reach

For every successfully compiled primitive, its implementation returns a value of
the declared result interface, or an explicit resource rejection. Identity,
copying and projections have their usual product interpretations; successor may
reject at the 256-bit limit rather than overflow; the Boolean primitives are
literal-type checked. Composition checks intermediate interface equality and
checks every intermediate value, so an overflowing intermediate cannot be
hidden by a later Boolean result. Parallel composition uses separate typed
inputs. These cases give source/target preservation by induction on the plan.

For `core`, a checked finite source derivation f:A→B and an input source derivation
x:A produce the actual derivation app(f,x):B. The reference checker recomputes
that rule and validates its output. The preserved finite-source soundness proof
then gives semantic membership. This is an explicit source-to-operation
interpretation, not a field saying `realizedBy`. Self-instantiated identity and
Boolean proofs are supplied among the actual exported examples.

For `selector`, the checked marker-free polymorphic proof and its symbolic
reduction certificate prove uniform first/second projection; its ordinary
substitution proof is preserved from v3. The engine returns that projection on
its declared interface. For edges, Q5 proves every active observation is
preserved. For sampling, only a rechecked proof at the common leaf type is
returned; a pending state has no proof field. For a productive observer, the
closed-control invariant proves the finite-prefix output is all zeros. These
complete the operation-specific preservation cases.

The source grammar admits genuinely many interfaces and arbitrarily extensible
schemas, but the concrete Python API enforces finite resource ceilings. No claim
is made that every Lean type has a serialisation or that every total typed Plan
executes within those ceilings. The success-preservation/refinement assertion is
conditional on actual compiler and execution success. This is weaker than an
end-to-end kernel proof of the Python parser/checker, which remains OPEN.

The positive executable witnesses include nonidentity successor, distinct zero
predicates, heterogeneous nat→bool composition, copying/product adapters,
internal source self-application, permission addition, permission removal,
re-enabling with a new ticket, and nonidentity productive-observer prefix
transformation. The declared positive probe fails on a reject-all engine.

## V4-O3 — stale evidence and races

At dispatch, issuer identity, issuance and every stored dependency stamp are
checked under the same RLock held through execution. Context-changing methods
hold that lock too. Issued records are never overwritten. A relevant policy,
model, vocabulary or requirement change increments its version. Therefore a
previous record cannot pass the equality check after that change. Restoring the
old permission does not restore the old version (ABA). Unrelated changes preserve
all recorded bindings and permit reuse. Revalidation treats an old handle only
as a way to nominate its immutable source for a NEW full check; it does not reuse
its authority.

Dispatch and revision are consequently serialisable at this lock boundary. A
revision waiting for a dispatch is not deemed to have taken effect before it
acquires the lock. Once the revision completes, subsequent dispatch cannot use
the old relevant evidence. This proof assumes the trusted host does not mutate
private fields, the fixed source code is the executed code, and ordinary Python
locking semantics hold. It is not a distributed lease or an OS sandbox theorem.

The executable projection lists current issued operations, their canonical source
hashes and dependencies with bounded pagination. It is a view of current handles,
not a theorem that an old displayed row stays executable after a revision.

## V4-O4 — independently specified positive and negative formal targets

`OperationalKernel.lean` proposes an independent universe-polymorphic typed Plan
schema, an evaluation function, finite stamped licences, a Boolean checker and
permission revision. OWOU requires an actual embedding of EVERY plan in that
stated schema, successful checking/evaluation at an open context, execution
implies checking, and concrete permission-adding and permission-revoking cases.
The constructor supplies these witnesses and their proof terms; OWOU is not True.
The source constructor takes an actual checked finite derivation, and evaluates
its realised application. The theorem `parametric_reach` is the **copy schema at
arbitrary Lean universes**, not Reynolds parametricity for ambient Lean functions.

`OperationalBoundary.lean` starts with actual operation handles for packing full
Hurkens sections into a same-level small type and unpacking them, at a specified
state, with total successful calls and a returned-value beta law. From these
operational calls choose pack/unpack witnesses. Functionality of the API's Option
result identifies the unpacked value with the original section; pointwise
application gives beta. The preserved `no_self_product` theorem then contradicts
this package. The O argument is used in the extraction, not an unused label.

Thus the ordinary argument proves the two independent claims for the declared
mathematical API schema:

    every API lacks that SCUU capability;
    the constructed typed-plan API satisfies its nonvacuous OWOU specification.

Their conjunction is `mainWitnessAt`. The source is UNCOMPILED. The typed schema
and Python engine are related by the ordinary partial implementation argument in
O2; they are not silently identified. Full deployed refinement, actual types and
transitive theorem footprints remain formal-acceptance obligations. Internal
realisability All never supplies the full ambient section package.

## V4-R1 — binary logical relations for the finite pure source

A relation code is a binary relation on raw terms invariant under reduction in
each coordinate. Interpret bottom as the empty relation, arrows by mapping
related inputs to related outputs, and forall by intersection over relation
codes. Closure follows by transporting each output coordinate through its
reduction step. Define relational environments and lift them at binders.

Structural induction on finite type syntax proves relational renaming and
substitution equations; the binder case uses lifted substitution and the
renaming equation. In particular relational interpretation of type
instantiation agrees with environment extension by the interpretation of its
actual type argument.

**Fundamental theorem:** if the declared finite pure calculus derives t:A, then
for every binary relation environment rho, (t,t) belongs to the interpretation
of A at rho. For I and K this follows by reducing each coordinate to the selected
related input. For S, apply the two function-relatedness hypotheses to the same
related pair, then transport both sides through the S step. Application is the
arrow definition. Universal introduction uses the induction hypothesis at every
extended relation environment; elimination uses the substitution equation.
Reduction transports the induction hypothesis in each coordinate. This exhausts
the finite derivation constructors.

`RelationalFragment.lean` contains this induction and derives `checked_parametric`
from an actual Checked derivation. It does not prove that EVERY inhabitant of the
unary semantic intersection is relationally parametric, and has no effectful
fundamental theorem. This is a conventional finite-source logical-relations
result, not a new solution to general Reynolds parametricity.

## V4-R2 — actual source-to-Lean certificate export

`proof_export.py` parses raw JSON through the strict parser and real checker.
It emits the corresponding finite Lean Cert constructors: I/K/S, application,
universal introduction/elimination, and one `Cert.step` per accepted head step.
Structural induction over the checked source shows this constructor mapping
preserves erasure and type, using the v3 de Bruijn substitution equation at type
elimination. A accepted finite reduction trace is already required to have the
same head successor at each adjacent pair; repeated step constructors preserve
its result. No evaluator or theorem assertion supplied by the caller is emitted.

Eight concrete JSON proofs generate `GeneratedExamples.lean` reproducibly. Each
example asks Lean to run its checker and prove BOTH the expected program and
the expected type, then derives semantic soundness from `checked_sound`. All of
these declarations are mandatory build/audit targets. Exporting text is not
compiling it. Agreement of these examples is not the full Python implementation
refinement theorem, and a native code backend has not been verified.

## V4-S1 — productive threshold source, mass and cost

The ideal source compares a fair stream's real U∈[0,1] to p=sqrt(2)-1. At a state
(n,k), its dyadic cell is [k/2^n,(k+1)/2^n). Read one bit to choose a child. The
polynomial H(x)=x²+2x-1 is strictly increasing on [0,1] and has that unique,
irrational root. A settled cell returns its certified left/right pure program;
otherwise another bit is requested. Every transition does finite integer work
and reads one bit, proving productivity. There is exactly one unsettled cell at
every finite depth; dyadic boundary representations form a null exception and
do not change the law.

Consequently P(N>n)=2^-n, P(N=n)=2^-n for n≥1, total terminating mass is one,
E[N]=2 and E[N²]=6. The branch probabilities are p and 1-p. Every terminating
branch returns a proof at the same internally polymorphic source type. The
single never-settling boundary stream has measure zero; not every possible
infinite stream terminates.

At a finite cap m the residual mass is exactly 2^-m, not zero. With k_m the
unsettled cell, the left/right/residual masses are k_m/2^m,
(2^m-k_m-1)/2^m and 1/2^m. They sum to one. The expected number of consumed bits
before stopping or the cap is Σ_(n<m)2^-n=2-2^(1-m). `certificate` computes these
fractions exactly; `sampler_budgeted` checks the residual against its requested
budget. IID fair bits and the declared threshold are explicit premises, not
inferred from a caller's list of zeros and ones.

The implemented transition arithmetic has 3 multiplications, 5 shifts, 6
additions, 1 subtraction and at most 2 sign comparisons per consumed bit. The
counter omits validation, type checking, parsing, allocation and acquisition of
random bits. The previous counter of 5 additions was reproduced and corrected.
Big-integer operations are not unit-cost instructions. Under an independently
chosen bit-cost model with per-depth work at most a n²+b (n begins at one), the
expected arithmetic work is at most

    Σ_(n≥1) 2^-(n-1) (a n²+b) = 12a+2b.

This uses ordinary convergent power-series sums and is not a CPU benchmark.
The bounded API is capped at 128 bits. The unbounded source semantics and its
probability theorem have not been implemented in Lean measure theory.

## V4-S2 — a discharged fixed-point example and its limits

On K=[0,1], let F(p)={(1-p²)/2}. Its values are nonempty closed convex singletons,
it maps K to K, and its graph is closed by continuity. K is nonempty, compact and
convex. These discharge Kakutani's elementary finite-dimensional hypotheses;
indeed the fixed point is directly solvable: p=sqrt(2)-1 is the unique root in K.
After one iterate, values lie in [0,1/2], where
|F(x)-F(y)|=(x+y)|x-y|/2≤|x-y|/2. Thus iteration converges geometrically, by a
separate contraction argument.

Use the fixed law on the two already-certified polymorphic Boolean programs.
The S1 fair-bit source exactly realises its irrational bias, so this particular
semantic fixed point has an effective realisation with proved ordinary mass and
bit cost. Finite trees of rational mixtures alone could not realise it, since
finite sums/products of rationals remain rational. No effective selector for
all real points of the closed probability simplex is inferred. A constant map
at a noncomputable real already supplies semantic existence without an effective
sampler under a finite-description/no-extra-oracle contract.

Finite outcome support ensures point concentration even when probability
parameters vary over a real continuum. Taking a convex weak closure of every
point mass on a continuous outcome carrier is a different operation, and the
preserved continuum obstruction still applies. These distinctions keep the
Kakutani, sampling, typing, and computability claims separate.

## Preserved unresolved metatheory

The original source-to-System-F normalisation bridge and conversion-completeness
counterexamples remain ordinary proofs/candidates, not compiled developments.
The semantic K t Omega obstruction is unchanged. Coherent dependent Pi/Sigma
and conversion transport remain preserved; full contextual dependent substitution,
identity elimination J, universe formation and a decidable dependent checker have
not been constructed. The new R1 finite pure fundamental theorem does not close
those gaps. No end-to-end Python/JSON or native backend verification is claimed.

**Contribution classification:** concrete integration and sharper application
boundaries, with additional ordinary arguments. The closure construction,
logical-relations induction, halting reduction method and elementary probability
identities use established mathematics. Global theorem novelty, foundational
breakthrough and peer review remain unestablished independently of correctness.
