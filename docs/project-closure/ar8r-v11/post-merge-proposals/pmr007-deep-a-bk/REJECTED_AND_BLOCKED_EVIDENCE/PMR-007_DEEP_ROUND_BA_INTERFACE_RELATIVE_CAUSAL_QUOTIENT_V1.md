# PMR-007 Deep Round BA V1 — interface-relative causal quotients and canonical operational content

```text
identity: PMR-007-IRCQ-1
round: DEEP_BA
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: H7a2 operational constitutive semanticity and representation convergence
```

## 1. Typed finite controlled system

Fix a finite deterministic controlled Moore system

\[
M=(X,A,\delta,\lambda),
\]

where `X` is a nonempty finite state set, `A` is a finite declared action set,
`delta:X×A→X`, and

\[
\lambda:X\to L
\]

is the complete **declared interface label**.  The label may combine only those
observation, target, source, provenance, version, authority, warrant, or status
coordinates independently admitted into the experiment.  Omitted coordinates
are not silently preserved.

For an action word `w=a1...ak`, define the full interface trace

\[
Tr_M(x,w)=
(\lambda(x),\lambda(\delta(x,a_1)),\ldots,
 \lambda(\delta(x,a_1\cdots a_k))).
\]

Define interface equivalence

\[
x\equiv_I y
\quad\Longleftrightarrow\quad
Tr_M(x,w)=Tr_M(y,w)\text{ for every }w\in A^*.
\]

The subscript `I` records that the result is relative to the declared action,
observation, target, source, and version interface.

## 2. Partition-refinement construction

Let `P0` partition `X` by equality of `lambda`.  Given `Pr`, define `P_{r+1}`
by equality of the signatures

\[
Sig_r(x)=
\bigl(\lambda(x),([\delta(x,a)]_{P_r})_{a\in A}\bigr).
\]

The finite refinement sequence stabilizes at `P*`.

## 3. IRCQ-1A — exact trace-equivalence characterization

`P*` is exactly the partition of `X` by `equiv_I`.

### Proof

Inductively, two states lie in the same `Pr` block exactly when their interface
traces agree for every action word of length at most `r`.  The base case is
label equality.  The induction step prefixes one action and compares successor
`Pr` blocks.  At the stable partition, agreement is closed under every action,
so induction on word length gives agreement for all words.  Conversely, states
with all traces equal remain together at every refinement stage. ∎

If two states are inequivalent, some word of length at most `|X|-1`
distinguishes them.  There are at most `|X|-1` strict refinement stages before
stability.

## 4. IRCQ-1B — canonical quotient and exact representation factorization

Let

\[
Q_I=X/{\equiv_I}.
\]

The maps

\[
\bar\lambda([x])=\lambda(x),
\qquad
\bar\delta([x],a)=[\delta(x,a)]
\]

are well defined, and the quotient reproduces every declared interface trace.

Call a deterministic representation `r:X→Y` **interface sufficient** when,
on `r(X)`, there exist `lambda_r` and `delta_r` satisfying

\[
\lambda=\lambda_r\circ r,
\qquad
r(\delta(x,a))=\delta_r(r(x),a).
\]

For every interface-sufficient `r`:

```text
ker(r) is contained in equiv_I;
q_I factors uniquely through r on r(X);
|r(X)| is at least |Q_I|;
and equality holds exactly when the represented system is isomorphic to Q_I.
```

### Proof

Equal `r` values produce equal represented traces, hence equal original traces,
so `ker(r)⊆equiv_I`.  Therefore `[x]` depends only on `r(x)`, defining the
unique factor map.  Surjectivity onto `Q_I` gives the cardinality bound, and
cardinality equality makes the factor map bijective and transition/label
preserving. ∎

Thus `Q_I` is the unique minimal exact deterministic realization up to
interface-preserving isomorphism.

## 5. IRCQ-1C — interface monotonicity

If an interface is strengthened by refining its label map or adding admissible
actions, its equivalence can only become finer and its minimal quotient can
only become at least as large.  Conversely, deleting a target coordinate,
source/provenance field, version distinction, or intervention may merge states
that differ exactly on the deleted coordinate.

This monotonicity is structural.  It does not say that the richer interface is
truer, properly functional, authorized, or worth its cost.

## 6. Operational constitutive-content result

`Q_I` supplies a representation-independent **operational content object** for
the complete declared finite interface:

```text
- it is computed from all permitted counterfactual action traces;
- every exact deterministic representation refines it;
- every minimal exact representation is isomorphic to it;
- its state names and literal content labels remain arbitrary up to isomorphism;
- changing the interface can change the quotient.
```

This closes one limited H7a2 sub-burden:

```text
OPERATIONAL_CAUSAL_CONTENT_CAN_BE_INTRINSIC_TO_A_DECLARED_INTERFACE
UP_TO_ISOMORPHISM.
```

It does not establish metaphysically intrinsic meaning, literal reference,
truth, a mental host, personal ownership, proper function, Wisdom, or Speech.

## 7. Mandatory controls

```text
BA-CM1 TARGET DELETION:
  two states differ only in a declared truth/warrant target; deleting it merges
  them.  Minimality is target-relative.

BA-CM2 ACTION DELETION:
  one action exposes a future difference; removing that action merges states.

BA-CM3 LABEL PERMUTATION:
  quotient structure is unchanged under renaming; literal reference is not
  fixed.

BA-CM4 IMPERSONAL MINIMAL REALIZER:
  an impersonal powers/transition system realizes Q_I exactly; canonical
  operational content does not entail personality.

BA-CM5 PERSONAL/IMPERSONAL TWINS:
  personal and impersonal expansions share the entire quotient and every
  interface trace while differing on first-person ownership and Wisdom.

BA-CM6 INCOMPLETE EXPERIMENT:
  a finite sampled trace set yields a coarser provisional partition than the
  all-word quotient.

BA-CM7 VERSION DRIFT:
  the same bytes under different target/version contracts induce different
  label maps and possibly different quotients.

BA-CM8 STOCHASTIC NONTRANSFER:
  the deterministic theorem does not characterize hidden stochastic systems;
  probabilistic bisimulation or causal-state sufficiency requires a separate
  model.
```

## 8. OSM, PRH, and Bitter-Lesson effect

The OSM paper reports progressive state differentiation and finds that CSCG
most closely reproduced both selected endpoint organization and the reported
learning trajectory among the tested models.  This can motivate a task-relative
causal quotient, but the source does not establish that the measured neural
state is the exact minimal quotient for every intervention or target.

PRH kernel alignment concerns similarity geometry under selected metrics.
Kernel alignment neither implies nor is implied by exact interface-quotient
isomorphism without additional maps.  Convergence can reflect common task and
observation constraints without selecting literal meaning or one metaphysical
realizer.

The Bitter-Lesson comparison should therefore test hand-authored and learned
representations by whether they preserve the declared quotient and held-out
counterfactual traces, not by vocabulary familiarity alone.

## 9. Candidate-G and transcendental effect

The quotient defeats a representation that merely carries redundant
state distinctions while adding no interface consequence.  It supplies a
canonical operational state object and a nondecorative reduction criterion.

It does not defeat the strongest current rival.  An abstract or modal order
plus an impersonal powers realizer can instantiate the same quotient.  A
personal architecture gains a neutral advantage only through an independently
warranted discriminator outside the shared interface reduct.

## 10. Ancestry and authority ceiling

```text
abstract ancestry:
  Myhill–Nerode / Moore-machine minimization;
  deterministic bisimulation and partition refinement;
  causal-state/minimal-sufficient-statistic mechanism at a deterministic scope

relation to Deep U:
  STRICT FORMAL STRENGTHENING OF THE ENDPOINT/TRAJECTORY CONTROL,
  NOT AN EMPIRICAL REANALYSIS

relation to Deep AO:
  DYNAMIC ALL-TRACE SUFFICIENCY COMPLEMENT TO STATIC LIKELIHOOD SUFFICIENCY

relation to Deep AY:
  OPERATIONAL STRUCTURAL CONTENT BELOW H7a2 METAPHYSICAL CONSTITUTIVITY

relation to profile/fibre family:
  GUARDED DYNAMIC CONGRUENCE STRENGTHENING, NOT AN INDEPENDENT GENERAL ORIGIN

general mathematical novelty:
  0
historical identity:
  NONE
external review:
  OPEN
owner adoption:
  PENDING
```

## 11. Nonclaims

No claim is made that the declared interface is complete, true, properly
functional, source-authoritative, metaphysically privileged, or world adequate;
that a learned or biological representation realizes the exact quotient; or
that canonical operational content entails one bearer, mind, person, Creator,
Wisdom, Speech, integrated champion, meniscus, or natural closure.
