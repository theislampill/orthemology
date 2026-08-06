# PMR-007 Deep Round AS — proper-function intervention basis and norm-source diagnosability V1

```text
campaign: AR8R_POST_MERGE_MENISCUS_PROGRAM_V1
wave: PMR-007
round: Deep AS
canonical post-merge identity: PMR-007-PFIT-1
status: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
```

## 1. Central burden

Deep A, F, K, P, X, and Y separate frequency, causal role, selected effect, design, learned target, truth linkage, teleology, fiṭrah, and Wisdom. Deep AQ shows that a central architecture discriminator requires source exclusion, a predictive/interventional surplus, or a defended prior. The remaining practical question is:

```text
which interventions are sufficient or necessary to distinguish
competing proper-function and norm-source accounts?
```

This round freezes a finite deterministic experiment model. It characterizes identification, not truth.

## 2. Typed setting

Let:

- `H` be a finite declared set of proper-function or norm-source accounts;
- `I` be a finite set of independently admissible interventions;
- `O` be a finite set of **complete response/certificate objects**;
- `r:H×I→O` be a deterministic response map;
- the hidden account remain fixed throughout the testing episode;
- interventions not alter the account, admissibility contract, or response semantics.

For two accounts `h,h'`, define their disagreement set

\[
D(h,h')=\{i\in I:r(h,i)\ne r(h',i)\}.
\]

## 3. PFIT-1A — nonadaptive intervention-basis characterization

A nonadaptive intervention set `J⊆I` identifies every account exactly iff

\[
\forall h\ne h',\quad J\cap D(h,h')\ne\varnothing.
\]

Equivalently, the restriction map

\[
h\mapsto (r(h,i))_{i\in J}
\]

is injective.

Therefore the minimum nonadaptive intervention number is the transversal number of the pairwise-disagreement hypergraph:

\[
\delta_{NA}(H,I,r)
=
\min\{|J|:J\text{ hits every }D(h,h')\}.
\]

If some `D(h,h')` is empty, the two accounts are observationally identical on every admissible intervention and no declared test identifies the full family.

### Proof

If `J` misses `D(h,h')`, the two accounts have the same response signature on `J`; exact identification fails. Conversely, if `J` hits every pairwise disagreement set, every pair differs on at least one selected intervention, so all signatures are distinct.

## 4. PFIT-1B — exact adaptive recurrence

For a current candidate set `S⊆H`, define

\[
V(S)=0\quad(|S|\le1),
\]

and otherwise

\[
V(S)=1+\min_{i\in I}\max_{o\in O}V(\{h\in S:r(h,i)=o\}),
\]

where interventions that do not split `S` are ineligible and `V(S)=∞` when no intervention splits a non-singleton `S`.

Then `V(H)` is exactly the minimum worst-case depth of an adaptive deterministic zero-error decision tree.

### Proof

At the root, every deterministic strategy chooses an intervention `i`; the observed response restricts the possible accounts to one response fibre. The worst branch has the displayed depth. Induction on `|S|` proves the lower bound and constructs an optimal tree from a minimizing intervention and optimal subtrees.

## 5. PFIT-1C — adaptive and nonadaptive tests are distinct

Always

\[
V(H)\le \delta_{NA}(H,I,r),
\]

because a nonadaptive basis can be queried sequentially. Strict inequality can occur.

For response rows

```text
h0 = 000
h1 = 001
h2 = 010
h3 = 101
```

all three interventions are required nonadaptively, while an adaptive tree has depth two:

1. query the first intervention;
2. if response `1`, identify `h3`; if response `0`, query the second or third according to the remaining branch.

Thus `delta_NA=3` and `delta_AD=2`.

## 6. Proper-function application

### Target-relative versus truth-linked function

If every admissible intervention keeps installed-target success aligned with independently correct truth/fittingness, the target-relative and truth-linked accounts can have identical response rows. They are not experimentally distinguished by that regime.

A separating experiment requires a **target/truth divergence intervention** whose truth coordinate is independently available. Harmful corrigibility supplies the canonical control: exact success relative to a destructive or false target while the truth-linked account rejects it.

### Design versus truth-linked function

A separating experiment requires design intention and truth to diverge. A malicious or incompetent design plan can preserve designed function while defeating epistemic truth linkage.

### Selected effect versus truth-linked function

A separating experiment requires actual selection history and truth to diverge. A trait selected because successful deception aided survival preserves selected-effect function while defeating truth direction.

### Plantinga-style versus generic design

The test must vary proper operation or environmental suitability while preserving generic design status. Merely observing successful output cannot identify the stronger account.

### Fiṭrah/source-relative function

A source-relative account requires authenticated source, correct reconstruction, version, applicability, impairment/health classification, and the declared restoration relation. A neutral response profile cannot supply these coordinates by itself.

## 7. Strongest controls

### AS-CM-ALIGNED-REGIME

All feasible interventions keep target, truth, design, selected history, and source verdict aligned. Several accounts share one response row; no finite declared test identifies them.

### AS-CM-HARMFUL-CORRIGIBILITY

A controller is perfectly corrected toward a harmful target. `PF_TARGET` succeeds while `PF_EPI` fails.

### AS-CM-MALICIOUS-DESIGN

A flawless designed classifier executes a deceptive plan. Design function survives; truth-linked function fails.

### AS-CM-SELECTED-DECEPTION

A deceptive trait was selected because deception succeeded. Selected effect survives; objective truth direction fails.

### AS-CM-SOURCE-VERSION

The same operational profile receives different Track-N applicability verdicts under different authenticated source/version contracts.

### AS-CM-TARGET-LEAKAGE

The intervention label or response object contains the correct account identity. The resulting “identification” is target leakage, not evidence.

### AS-CM-STATE-CHANGE

An intervention changes the governing account or its target. The static response-map theorem no longer applies; a game or controlled-transition model is required.

## 8. Deep AQ and experimental effects

Deep AQ `GATE E` is not discharged by naming an intervention. It requires an admissible experiment whose candidate response distributions differ. PFIT-1 supplies the finite deterministic design criterion and exact minimum test quantities for a declared proper-function account family.

The result also sharpens future T299/T300 and OSM-style work:

```text
endpoint success alone:
may leave norm-source accounts in one response fibre;

learning trajectory or causal intervention:
may split that fibre only if the competing accounts actually predict
different complete response objects;

representation choice:
cannot manufacture a split absent from the frozen experiment;

provenance-root conservation:
repeated copies of one experiment do not create additional independent tests.
```

## 9. Theorem-family and complexity status

The nonadaptive result is a direct finite **test-cover / hitting-set** characterization. The adaptive recurrence is standard deterministic decision-tree diagnosis. Candidate 1 and AR-T4 supply adjacent query/diagnosability interfaces but not the same proposition.

```text
Candidate 1:
tight query complexity for hidden matching cardinality threshold;
not this account-identification problem.

AR-T4 / active diagnosis:
shared finite discrimination mechanism and ancestry control.

Deep AQ/AO:
evidential and representation sufficiency guards.

general mathematical novelty:
0.
```

The value is a central experiment-design invariant and exact impossibility boundary for the proper-function program.

## 10. Nonclaims

- Identifying an account from its frozen response signature does not establish the account true.
- The declared account catalogue need not be complete.
- The theorem assumes deterministic complete response objects.
- It does not solve stochastic, bounded-error, interactive, history-dependent, state-changing, adversarial-message, or dynamic-membership diagnosis.
- Feasibility and authorization of interventions are external guards.
- It does not authenticate source or truth coordinates.
- It does not establish a personal designer, Wisdom, Necessary Being, or integrated champion.
