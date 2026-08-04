# PMR-M3-01 — Necessary existence, originator, and Creator: guarded separation

## Provenance and status

```text
campaign: AR8R_POST_MERGE_MENISCUS_PROGRAM_V1
wave: PMR-001
candidate_id: PMR-M3-01
historical identity: NONE
provenance: HONEST_POST_MERGE_RESEARCH
initial status: FROZEN_CANDIDATE_PENDING_COLD_AUDIT
source-relative scope: translated-primary Asfahani commentary locus
world-directed status: NOT ESTABLISHED
novelty claim: NONE — standard first-order entailment/nonentailment applied to a source boundary
```

This packet does not recover or replace any historical theorem. In particular, it does not claim the exact payloads of T367–T370. Those identities remain historical references unless their exact packets are independently located.

## Source proposition isolated

The controlling translated-primary locus distinguishes four claims:

1. a modal/existential argument may yield **some necessary existence**;
2. that conclusion alone does not yield a **Creator/Maker**;
3. observed originated entities provide a more direct route to an **originator**;
4. the further attribution of Creatorhood and attributes requires additional work.

The relevant local source is `A-Commentary-on-the-Creed-of-Asfahani-v2.3(1).md`, lines 331–350 in the attached Markdown snapshot. Translation authority is translated-primary-text access, not independent Arabic-edition verification.

## Typed signature

Let the first-order language contain:

```text
N(x)   x is necessarily existent in the declared sense
E(x)   x is externally real rather than merely mental/abstract
O(y)   y is originated
R(x,y) x originates y
W(x)   x possesses the volitional guard relevant to this ascent
P(x)   x possesses the power guard relevant to this ascent
K(x)   x possesses the knowledge guard relevant to this ascent
C(x)   x satisfies the scoped Creator predicate
```

`C` is a scoped formal target. It is not a definition of the divine name, a revelational identification, or a proof of personality, unity, Wisdom, Life, Speech, mercy, or love.

## Premise packages

```text
NE:
  ∃x N(x)

ORIG:
  ∃y O(y)

B_orig:
  ∀y (O(y) → ∃x R(x,y))

B_NE:
  ∀x∀y (R(x,y) → (N(x) ∧ E(x)))

B_creator:
  ∀x ((N(x) ∧ E(x) ∧ ∃y R(x,y) ∧ W(x) ∧ P(x) ∧ K(x)) → C(x))

G_WPK:
  ∀x∀y (R(x,y) → (W(x) ∧ P(x) ∧ K(x)))
```

These are deliberately separated. `B_orig` is the immediate originator bridge. `B_NE` is the additional bridge from originator status to necessary external actuality. `B_creator` is a guarded classification bridge. `G_WPK` is the strong attribute/agency package whose source and world-directed adequacy remain separate burdens.

## Result M3-01A — necessary existence does not entail Creator

```text
NE ⊭ ∃x C(x)
```

### Proof by countermodel

Take a one-object structure `{u}` with `N(u)` true and every other predicate and relation false. Then `NE` is true and `∃x C(x)` is false. Therefore necessary existence alone does not entail Creator.

### Stronger nonimplication

Even the package

```text
∃x (N(x) ∧ E(x))
```

does not entail `∃x C(x)`: use the same model with `E(u)` also true.

This is the formal counterpart of the source warning that a necessary-existence conclusion is compatible with Maker-denying positions.

## Result M3-01B — originated existence plus the originator bridge yields an originator

```text
ORIG ∪ B_orig ⊨ ∃x∃y R(x,y)
```

### Proof

Choose `y` from `ORIG`. Instantiate `B_orig` at `y`. Its witness `x` satisfies `R(x,y)`. Existential generalization gives the conclusion. ∎

No necessity, external actuality, agency, or Creatorhood follows from this result alone.

## Result M3-01C — necessity and external actuality require their own bridge

```text
ORIG ∪ B_orig ∪ B_NE ⊨ ∃x (N(x) ∧ E(x) ∧ ∃y R(x,y))
```

### Proof

Choose `y` from `ORIG`. `B_orig` gives `x` with `R(x,y)`. `B_NE` gives `N(x) ∧ E(x)`. Existential generalization gives the conclusion. ∎

This makes explicit that the source's immediate originated-to-originator move and the later necessary/external classification are distinct arrows.

## Result M3-01D — an externally real necessary originator does not entail Creator without the guarded bridge package

```text
ORIG ∪ B_orig ∪ B_NE ⊭ ∃x C(x)
```

### Countermodel PMR-CM-M3-IMPERSONAL-ORIGINATOR

Take domain `{u,e}` with `u ≠ e` and interpret:

```text
O(e) = true
R(u,e) = true
N(u) = true
E(u) = true
W(u) = false
P(u) = false
K(u) = false
C(u) = false
all other atoms = false
```

`ORIG`, `B_orig`, and `B_NE` hold. There is an externally real necessary originator. No Creator exists in the scoped language. This is an **impersonal-originator control**, not a claim that such a model is metaphysically or source-theologically adequate.

## Result M3-01E — the full guarded package entails the scoped Creator conclusion

```text
ORIG ∪ B_orig ∪ B_NE ∪ G_WPK ∪ B_creator ⊨ ∃x C(x)
```

### Proof

Choose `y` from `ORIG`. `B_orig` gives an `x` with `R(x,y)`. `B_NE` gives `N(x)` and `E(x)`. `G_WPK` gives `W(x)`, `P(x)`, and `K(x)`. These satisfy the antecedent of `B_creator`, so `C(x)`. Existential generalization gives `∃x C(x)`. ∎

## Deletion tests

Relative to the conjunctive `B_creator` bridge, each of `W`, `P`, and `K` is load-bearing. For each guard `g`, use the impersonal-originator model with the other two guards true and `g` false. `ORIG`, `B_orig`, `B_NE`, and the remaining guards hold, while the antecedent of `B_creator` does not fire and `C` remains false.

This establishes premise minimality **only for the declared bridge schema**. It does not establish that these are the only possible source or metaphysical routes to Creatorhood.

## R5 rival effect

The model `PMR-CM-M3-IMPERSONAL-ORIGINATOR` gives the following exact comparison after `B_orig` and `B_NE` are kept separate:

```text
necessary existence: satisfied
external actuality: satisfied
originator/actualizer role: satisfied
Will guard: withheld
Power guard: withheld
Knowledge guard: withheld
scoped Creator conclusion: withheld
```

Therefore the impersonal-originator rival is not excluded by necessary existence, external actuality, or originator status alone. It is transformed or excluded only by an independently justified bridge that supplies the missing agency/attribute guards.

## Source–formal–world firewall

What this packet establishes:

- a precise source-aligned nonentailment;
- a guarded implication;
- a source-preserving-with-respect-to-the-weak-locus countermodel;
- the exact bridge coordinates doing the formal work.

What it does not establish:

- independent Arabic wording or edition verification;
- that `B_orig`, `B_NE`, `G_WPK`, or `B_creator` are world-true;
- cross-world necessity;
- uniqueness, unity, personality, Wisdom, Life, Speech, mercy, or love;
- revelational identification;
- a complete Necessary-Being proof;
- any new general mathematical theorem.

## Family and ancestry disposition

```text
families:
  FAMILY-GROUND
  FAMILY-RIVAL
  FAMILY-SOURCE

relation to Asfahani source locus:
  FORMALIZATION_OF_TRANSLATED_PRIMARY_BOUNDARY

relation to owner-reported T367:
  SHARED_MECHANISM_ONLY_PENDING_EXACT_T367_PACKET

relation to owner-reported T368:
  COMPATIBLE_RIVAL_CONTROL_PENDING_EXACT_T368_PACKET

relation to T334 joint-contribution program:
  APPLICATION_ONLY; source and bridge packages are kept distinct

general mathematical novelty:
  ZERO
```
