# PMR-007 Frontier Round 20 V2 — static pathwise provenance-root robustness

```text
round: PMR-007-FRONTIER-ROUND20
canonical identity: PMR-007-PRRC-1
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
current disposition: REPAIRED_FROZEN_PENDING_DISTINCT_FRESH_REREVIEW
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Problem and relation to the preserved program

T351 shows that stable pathway restoration cannot be certified while a
registered error-effective path remains untouched.  T352 gives a guarded
sufficiency result when the path family is complete, each intercepted path is
actually neutralized, the repair is locally sound, no new error path appears,
the target is independently adequate, and custody plus reread are complete.

Those results treat blockers as available.  They do not measure how many
**actual provenance roots** must be corrupted before all blockers of one path
fail together.  Round 19 supplies a canonical-root query interface; current
daee false-tawatur and memetic-ecology records separately warn that copied
multiplicity is not independent origin or warrant.

Round 20 therefore introduces one scoped robustness margin for fixed declared
path systems.

## 2. Exact typed setting

Let

\[
\mathfrak R=(U,P,I,B,R_{\mathrm{req}})
\]

be a finite static restorative-root system where:

```text
U:
  a finite set of actual authenticated provenance-root identities,
  or an independently validated canonical quotient of such identities;

P:
  a nonempty finite path family that is complete for the declared fixed model;

I:
  a finite portfolio chosen before corruption;

B(a) subseteq P:
  the fixed set of paths blocked by action a;

R_req(a) subseteq U:
  the individually load-bearing required provenance roots of action a.
```

### Conjunctive dependency semantics

Each member of `R_req(a)` is necessary for the action in the declared model.
For a static corruption set `F subseteq U`, action `a` is available exactly
when

\[
F\cap R_{\mathrm{req}}(a)=\varnothing.
\]

Thus corruption of **any** required root disables the action.  An empty
required-root set denotes a root-independent action and remains available
under every root corruption.

This is not the semantics of redundant alternative supports.  If an action can
survive through several alternative root bundles, the object needed is its
family of minimal disabling sets, not one `R_req(a)` edge.

### Static pathwise survival

For an integer `f>=0`, the portfolio is **statically pathwise `f`-root-robust**
when

\[
\forall F\subseteq U\ (|F|\le f\Rightarrow
  \forall p\in P\ \exists a\in I:
  p\in B(a)\land F\cap R_{\mathrm{req}}(a)=\varnothing).
\]

The portfolio is visible before the adversary chooses one static corruption
set.  The statement is pathwise availability/certification, not yet a theorem
about sequential choice, retries, scheduling, resource conflicts, or action
interaction.

## 3. Root-transversal invariant

For each path `p`, define

\[
\mathcal H_p(I)=
\{R_{\mathrm{req}}(a):a\in I,\ p\in B(a)\}.
\]

For a finite family `H` of subsets of `U`, define the transversal number

\[
\tau(H)=\min\{|F|:F\subseteq U,\ \forall E\in H,\ F\cap E\neq\varnothing\}.
\]

Use the exact boundary conventions:

```text
tau(empty family) = 0;

tau(H) = infinity when H contains the empty edge.
```

The first says an unblocked path is already failed at zero corruption.  The
second says no root corruption can disable a root-independent blocker.

Define

\[
\kappa_{\mathrm{root}}(I)=
\min_{p\in P}\tau(\mathcal H_p(I)).
\]

## 4. PRRC-1 — exact static pathwise characterization

### Theorem

For every finite static restorative-root system and every integer `f>=0`,

\[
I\text{ is statically pathwise }f\text{-root-robust}
\quad\Longleftrightarrow\quad
\kappa_{\mathrm{root}}(I)>f.
\]

### Proof

For a fixed path `p`, a corruption set `F` disables every blocker of `p` iff

\[
\forall a\in I\ (p\in B(a)\Rightarrow
F\cap R_{\mathrm{req}}(a)\neq\varnothing),
\]

which is exactly the statement that `F` is a transversal of
`H_p(I)`.  Therefore `tau(H_p(I))` is the minimum static corruption size that
leaves path `p` without an available blocker.

If `kappa_root(I)<=f`, choose `p` and a transversal `F` of size at most `f`.
Every blocker of `p` is disabled, so static pathwise robustness fails.

If `kappa_root(I)>f`, let `F` be any corruption set of size at most `f` and
let `p` be any path.  Since `F` is smaller than `tau(H_p(I))`, it is not a
transversal of `H_p(I)`.  Hence some blocker root set is disjoint from `F`, so
some blocker of `p` remains available.  This holds for every path and every
admissible static corruption set. ∎

## 5. Guarded executable-portfolio corollary

Assume additionally:

```text
COMPATIBILITY:
  every set of simultaneously available actions in I is jointly executable;

NO INTERACTION:
  executing one surviving blocker neither disables another nor creates a new
  error-effective path in the declared horizon;

SIMULTANEOUS AVAILABILITY:
  root status does not change between certification and execution;

LOCAL EFFECTIVENESS AND SOUNDNESS:
  each selected blocker really neutralizes its declared paths and creates no
  target error;

T352 G1/G4/G5/G6-STYLE GUARDS:
  path completeness, no new path, target adequacy, custody, and reread.
```

Then `kappa_root(I)>f` is sufficient for the declared jointly executable fixed-
model restoration certificate against every static corruption of at most `f`
roots.  Necessity for the root-resilience coordinate remains exact, but the
full restoration conclusion also depends on the listed non-root guards.

Without compatibility and no-interaction, PRRC-1 remains only pathwise.

## 6. Monotonicity and false-multiplicity consequences

At the admitted semantics:

### Copied-action duplication invariance

Duplicating an action without changing its actual required-root set does not
change `H_p` as a set family and does not change `kappa_root`.  Copying cannot
manufacture resilience.

### Portfolio enlargement

Adding a genuine blocker adds a hyperedge to one or more `H_p` families.  A
transversal must hit at least as many edges, so `kappa_root` weakly increases.
The increase can be zero when the new action shares an old bottleneck.

### Action deletion

Deleting blockers weakly decreases `kappa_root`.

### Root contraction

If two actual roots are identified by a quotient map, the image of any old
transversal is a transversal of the contracted family with no larger size.
Therefore root contraction can only weakly decrease the certified margin.

### Displayed-root refinement is not actual resilience

Splitting one actual root into several labels may raise a displayed-label
transversal number while leaving the actual-root invariant unchanged.  Only an
independently validated root-identity map licenses the higher value.

## 7. Positive construction

Let `P={p1,p2}`, `f=1`, and let:

```text
a1: blocks p1, R_req={r1}
a2: blocks p1, R_req={r2}
a3: blocks p2, R_req={r2}
a4: blocks p2, R_req={r3}
```

For both paths the transversal number is `2`; hence `kappa_root=2`.  Every
single-root corruption leaves one blocker on each path, while corruption of
`{r1,r2}` leaves `p1` unblocked and corruption of `{r2,r3}` leaves `p2`
unblocked.  The threshold is sharp.

## 8. Preserved countermodels and scope failures

### R20-CM-COPIED-ROOT

Many apparent actions with the same actual root have `kappa_root=1`.

### R20-CM-COMMON-BOTTLENECK

Root sets `{r,x1}`, `{r,x2}`, ... still have transversal number `1`.

### R20-CM-INCOMPATIBLE-REPAIRS

Distinct-root blockers for different paths may be mutually incompatible.
PRRC-1 pathwise availability does not imply a joint execution schedule.

### R20-CM-DYNAMIC-REROUTING

Blocking every fixed registered path can activate an omitted path.  Fixed-path
robustness is not dynamic restoration.

### R20-CM-ADAPTIVE-ONE-SHOT

A sequential adversary that targets the chosen action after observing it can
defeat a one-shot policy even when the static corruption threshold is larger.

### R20-CM-UNAUTHENTICATED-ROOTS

Two displayed roots that alias one actual root produce a false margin.

### R20-CM-PARTIAL-PATH-REGISTRY

A complete certificate over an incomplete registry remains incomplete.

### R20-CM-REDUNDANT-SUPPORT-SEMANTICS

If an action needs only one of several alternative supports, `R_req` is the
wrong representation and the transversal theorem can understate resilience.

### R20-CM-ADAPTIVE-PATH-AND-ROOT COUPLING

A repair can reveal which path the system will take and thereby let an
adaptive adversary corrupt the unique root supporting the next blocker.  This
requires a game value over histories, not the static `kappa_root` invariant.

## 9. Ancestry, source, and implementation relation

```text
AR8R-T351:
  path-interception necessity;

AR8R-T352:
  guarded fixed-path sufficiency and completeness/no-new-path firewall;

AR8R-T353:
  self-sealing/output-local correction control;

PMR-007 Round 15:
  current daee event-local closure does not determine temporal stability;

PMR-007 Round 19:
  canonical-root multiplicity/query interface;

AR2/AR3 and agentic communication:
  provenance-root preservation, target-local applicability, authorization,
  and reason transport;

current daee memetic ecology and false-tawatur fixtures:
  copied/common-source multiplicity is not source independence or warrant;

TAWATUR-WARRANT:
  a separate school-labeled qualitative assessment, not a machine conclusion;

standard hypergraph transversal theory:
  exact mathematical mechanism.
```

PRRC-1 is a **compositional corollary and useful implementation certificate**
for provenance-indexed restorative portfolios.  It is not an independent new
general hitting-set theorem, not a historical T351/T352 identity, and not a
creed-internal tawatur result.

## 10. Candidate and flywheel effects

### Candidate A

The result converts visible blocker multiplicity into an exact actual-root
robustness margin.  It strengthens the provenance branch beyond root counting,
while leaving authentication, independent acquisition, distributed knowledge,
and recipient warrant open.

### Candidate B

The result adds one nondecorative resilience coordinate to restorative-cutset
certification.  It does not replace temporal stability, burden landing,
recursive reread, causal efficacy, or target adequacy.

### Candidate C

Plural source routes and argument copies cannot gain metaphysical or epistemic
weight merely by presentation count.  The theorem supplies no world bridge and
no source truth.

### Reverse pressure

```text
copied-root failure:
  REOPENS false-multiplicity and source-authentication burdens;

dynamic-rerouting failure:
  REOPENS T352 path-completeness and Round-14 temporal burdens;

incompatible-repair failure:
  REOPENS route-order and joint-execution architecture;

high kappa with unverified roots:
  BLOCKS implementation and causal claims;

low kappa:
  NARROWS any claim of resilient restoration.
```

## 11. Authority ceiling

```text
proof status:
  human finite proof plus primary executable evidence; distinct rereview pending;

historical identity:
  none;

general mathematical novelty:
  zero / not claimed;

orthemological contribution:
  scoped provenance-resilience certificate and false-multiplicity boundary;

external review:
  open;

owner adoption:
  pending;

repository integration:
  not authorized.
```

The theorem does not establish actual restoration, fitri restoration, source
truth, evidential independence, causal landing, common knowledge, or a
world-directed metaphysical conclusion.
