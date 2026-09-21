# Actual operational contract: fixed K, revised Gamma

K is the source grammar, interpretation, bound checks, operation compiler,
dispatch semantics and ordinary foundational metatheory. Gamma contains enabled
operation rules and monotonically increasing versions, active observation
signatures, declared probability-law models, per-rule risk obligations and
issued immutable licence records. Revising Gamma never edits K.

## Finite executable interface

The JSON grammar admits bounded natural numbers and Booleans, unit, finite
carriers and products, structural identity/copy/projections, successor/iszero/not,
composition and parallel composition, checked source application, certified
polymorphic selector specialisation, invariant finite edges, checked guarded
samplers and finite-invariant productive observers. Candidates cannot inject
Python code. Arbitrary semantic membership, type equality over all functions,
evidence search or unrestricted normalisation are not decision procedures here.

The typed Lean `Plan` model also has a universe-polymorphic structural schema.
It does not claim every ambient type or function has a JSON representation.
`parametric_reach` is a copy-operation schema; the separate relational theorem
is about the finite pure source. The bounded Python implementation can refuse
resources that the total mathematical schema abstracts away.

`admit_json` checks strict bounded UTF-8 JSON and exact fields; `admit` serialises
through that boundary. It compiles a finite plan, rechecks source/cost certificates
and all relevant permissions and probability requirements, and records immutable
source bytes, compiled interface, version bindings and computed evidence.

## Permission and revision

A process-local Licence names an immutable issued record and its engine identity.
It is not a public-key certificate or a remote-authentication protocol. Caller
Python objects are not proof evidence. The host process and its private state
are trusted; arbitrary code execution in that host defeats this boundary.

Every plan binds all dependencies of its children and the **absence or presence**
of additional probability obligations. Adding an obligation invalidates licences
that previously needed none. Active-vocabulary changes invalidate invariant-edge
licences even when a newly introduced predicate had no old dependency name.
Every model revision changes its stamp even when its numeric law is unchanged.

Dispatch validation, execution and relevant revisions are serialized by one RLock.
Thus there is no relevant revision between the check and use inside a dispatch.
A dispatch linearised before a revision can finish first; after revision returns,
an old relevant licence cannot dispatch. Unrelated changes preserve checked
licences. Revocation followed by re-enabling (ABA) does not restore an old stamp.
`revalidate` can use old immutable source only as a NEW candidate; it cannot reuse
the old authorisation. Even coarsening, which cannot worsen the semantic defect,
requires a new licence.

Registry nonces are checked for uniqueness before insertion. Eight collisions
produce a bounded refusal, never overwrite an old record. Identical nonce bytes
in another engine carry a different issuer identity and do not cross-authorise.
These are local capability properties, not an adversarial host security theorem.

## Revision-sensitive probability certificates

A named probability observation records a finite law description, observation
vocabulary/map and event-repertoire tag. Its source bytes are fingerprinted.
This is an optional observation-environment requirement attached by the trusted
host, not a theorem that deterministic integer operations have diffuse outputs.
Two implemented spaces are finite program outcomes with rational weights, and
finitely tagged uniform intervals with hidden/binned/revealed coordinate views.
In the latter grammar defect is the sum of weights of fully revealed interval
coordinates. Host declarations identify the mathematical law; no algorithm
infers an arbitrary physical law from samples.

A refinement check proves finite factorisation in this grammar and computes

    refined defect = coarse defect + weighted positive-fibre defects.

Admission checks refined defect <= declared epsilon. Old coarse validity does
not authorize after a relevant law/map change. This uses the full-measurable
event contract; an actually finite or countable event family is a different, weaker obligation.
Finite source syntax can still denote an uncountably parameterised semantic
family, so source-string countability alone does not justify that downgrade.
Countable outcome carriers have zero defect. Q8 proves that no complete effective
certificate checker exists for every productive infinite-stream observation in
the general mathematical class; the provided finite invariant checker is sound
but deliberately incomplete. Its implemented 64-state bound is not itself an
undecidability claim.

## Source connection

The `core` operation rechecks a source arrow certificate, constructs its actual
application to a supplied input proof, rechecks the result and retains its raw
term and type. The old semantic All and actual identity/selector self-instantiation
remain intact. `proof_export.py` emits the corresponding Lean Cert constructor
tree and requires a checked result from the Lean finite checker. Eight committed
examples regenerate byte-for-byte. Emission and agreement tests are not kernel
acceptance or universal Python/Lean refinement.

## Resources, effects and incomplete computations

Inputs and outputs have byte, tree, depth, integer and string bounds. Substitution
and type composition charge budgets during construction. Every intermediate
result is checked, so overflow cannot be discarded by later projection. Registry,
revision and vocabulary sizes are bounded; projection is paginated. Serialization
stops before building an oversized whole byte string. These are tested limits,
not a complete operating-system allocator/CPU sandbox.

A checked sampler has two certified same-type leaves and a max-bit cap. `done`
carries a leaf proof; `pending` does not. A residual-probability budget is tested
against 2^-cap. The ideal fair-bit semantics is productive and terminates almost
surely, with expected two bits; the finite API does not promise termination on
all infinite streams. Arithmetic work, bit acquisition, validation and CPU time
are different costs. See PROOFS_V4.md for exact units and assumptions.

## Positive acceptance

Run `python -B demonstrate.py`. It must exhibit nonidentity, distinction,
composition, permission addition, revocation/ABA, source self-application,
observation refinement and new evidence, coarsening, typed sampler residuals,
productive observer invariants and a nonempty executable projection. A reject-all
engine fails the positive probe. These witnesses are mandatory finite evidence,
not a replacement for proving the deployed system.
