# PMR-007 Deep Round AX V1 — source testimony likelihood and the world-selection gate

```text
identity: PMR-007-STWG-1
round: DEEP_AX
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_burden: independently warranted source-world anchor and actual-world selection
```

## 1. Candidate setting

Let the candidate architectures be `A` (unified personal ground) and `R`
(source-compatible impersonal/powers rival).  Let `G` be a finite set of
provenance roots.  Root `g` emits one complete source observation `Y_g` in a
finite alphabet, with architecture-conditioned probabilities

\[
P_g^A(y),\qquad P_g^R(y).
\]

All translations, copies, summaries, and repeated presentations descending
from one actual root remain attached to that root.

For observed source vector `y=(y_g)`, define

\[
L(y)=\prod_{g\in G}\frac{P_g^A(y_g)}{P_g^R(y_g)}.
\]

The candidate source gate says that posterior odds are prior odds multiplied by
`L(y)`, and that source evidence breaks A/R parity exactly when `L(y) != 1`.

## 2. Proposed positive use

If an independently authenticated source root is more likely to produce the
observed source-role statement under `A` than under `R`, it supplies source
likelihood evidence for `A`.  Several independent roots multiply their
likelihood ratios.  Deterministic copies from one root do not add a new factor.

## 3. Source and world guards

The formal source observation becomes architecture evidence only after:

```text
source bytes and provenance;
translation and proposition reconstruction;
source-referent identity;
source-to-world interpretation;
version and applicability;
architecture-conditioned source reliability;
and the candidate-world likelihood model.
```

Source-role compatibility alone is not a likelihood model.

## 4. Candidate countermodels

```text
AX-CM1 COPIED TRANSLATIONS:
  several translations descend from one source root;
  naive multiplication overcounts one root.

AX-CM2 SHARED COMMON CAUSE:
  two apparent roots are correlated given the architecture;
  the product of marginal likelihoods differs from the joint likelihood.

AX-CM3 SOURCE COMPATIBILITY PARITY:
  both architectures predict the same source-role statement distribution;
  source compatibility leaves posterior odds unchanged.

AX-CM4 HIDDEN REFERENT ANCHOR:
  the interpretation family is restricted to map the source bearer only to
  the preferred world bearer; the apparent source discriminator imports the
  target.

AX-CM5 VERSION DRIFT:
  one wording has different applicability under two version contracts.

AX-CM6 TRANSLATION CHANNEL:
  a common lossy translation can erase source discrimination; it cannot be
  treated as a second independent source.
```

## 5. Intended central effect

The candidate aims to turn Deep AQ's source gate into an exact evidential
contract.  It does not claim that any supplied source currently satisfies the
contract, that source testimony is false or true, that the actual world has
been selected, or that Track-N source predication is a neutral theorem.
