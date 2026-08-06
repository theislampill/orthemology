# PMR-007 Deep Round AP V2 — source-world referent identification

```text
identity: PMR-007-SWRI-1
round: PMR-007-DEEP-AP
version: V2
status: REPAIRED_POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: state the exact bridge from source-level co-reference to one world referent
```

## 1. Two-sorted source/world setting

Let `S` be a finite **source/discourse structure** and `W` a finite candidate
**world structure**. Let `g in S` be the unique source object satisfying the
selected source role bundle `U_S`.

Let `H` be a declared family of admissible interpretation maps `h:S→W`. The
statement `h(g)=w` records a denotation candidate. It is not numerical identity
between a source object and a world object.

Define the candidate-denotation fibre

\[
F_H(g)=\{h(g):h\in H\}.
\]

The source/world bridge has separately typed guards:

```text
SRC_BYTES; LOCUS; TRANSLATION; ATTRIBUTION;
PROPOSITION_RECONSTRUCTION; TRACK_N_ACCEPTANCE;
MAP_ADMISSIBILITY; ROLE_PRESERVATION;
REFERENT_ELIGIBILITY; WORLD_ADEQUACY; VERSION_CUSTODY.
```

No guard inherits another guard's status.

## 2. SWRI-1A — conditional world-role realization

If:

```text
H is nonempty;
every h in H is world-adequate at the declared scope;
and every h preserves the selected role bundle of g;
```

then every `h(g)` is a candidate world bearer of the translated bundle, and at
least one such bearer exists in the declared candidate world.

The conclusion is conditional on the map family and candidate-world adequacy.
It is not an unconditional existence proof.

## 3. SWRI-1B — exact relative referent determination

Relative to a frozen admissible family `H`, the source package determines one
candidate world referent exactly when

\[
|F_H(g)|=1.
\]

If `|F_H(g)|>1`, the source package does not choose among the surviving
candidate denotations. If `H` is empty, no denotation is established.

A singleton fibre is source-derived only when `H` and its restrictions are
independently warranted rather than chosen to select the desired result.

## 4. SWRI-1C — role-complete interpretation characterization

Call `H` **role-complete for g** when every world object satisfying the
translated role bundle occurs as `h(g)` for some admissible `h`.

Under role preservation, role completeness, and nonempty `H`,

\[
F_H(g)=\{w\in W:U_W(w)\}.
\]

Therefore, at that declared comparison-class scope, unique relative referent
determination is equivalent to unique realization of the translated role
bundle.

Without role completeness, unique role realization remains sufficient but is
not necessary: an independent anchor or additional structural constraint may
narrow the fibre.

## 5. Positive anchor construction

An independently warranted denotation anchor `A(g,w)` closes the relative
referent burden when:

```text
there is exactly one eligible w with A(g,w);
every admissible map respects A;
A is not defined by the desired world conclusion;
source, translation, version, referent, and world guards pass;
and the anchor is stable under every admissible source/world alternative.
```

This yields one candidate denotation at the declared scope. It still does not
by itself establish every predicate attributed to that object or any neutral
personal/Wisdom bridge.

## 6. Countermodels

```text
AP-CM1 EMPTY H:
  source co-reference is accepted but no world interpretation is warranted.

AP-CM2 TWO ROLE-EQUIVALENT WORLD BEARERS:
  both are admissible images of g; the source does not select one.

AP-CM3 HIDDEN ANCHOR:
  H contains only maps to w0 although w1 bears the same roles; uniqueness is
  imported by map policy.

AP-CM4 PRESERVATION WITHOUT REFLECTION:
  h(g) bears all selected roles plus unregistered features; the source does not
  determine the complete world profile.

AP-CM5 VERSION/TRANSLATION DRIFT:
  revised role reconstruction changes H and F_H(g); old denotation custody
  does not automatically transport.

AP-CM6 SOURCE-COMPATIBLE IMPERSONAL REALIZER:
  one world object bears the selected creator/knowledge/ability/life/volition/
  speech roles while de se ownership, philosophical personality, and Wisdom
  remain false in the neutral reduct.

AP-CM7 MULTIPLE WORLDS:
  distinct candidate worlds each contain one role-bearer; within-world
  uniqueness does not select the actual world.
```

## 7. Exact source application

The supplied English translation of Ibn Taymiyyah's commentary on al-Asfahani's
creed presents one creator as necessary, one, knowing, able, living,
volitional, speaking, hearing, and seeing, and the commentary endorses those
predications as true. This is translated-primary access, not Arabic-primary
verification.

Accepting the reconstructed co-reference proposition filters the Track-N source
model class. World realization and referent identity remain behind the bridge
guards above. Source-compatible shared-role-bearer or impersonal-realizer
rivals therefore remain live until the denotation/world and neutral H7/H8
burdens are independently closed.

## 8. Theorem-family and novelty

The formal core is a standard image-fibre/interpretation result and a central
source-world specialization of the recurring factorization family.

```text
general_mathematical_novelty: 0
historical_identity: NONE
repository_status: PROPOSAL_EVIDENCE_ONLY
external_review: OPEN
owner_adoption: PENDING
```

## 9. Nonclaims

No result establishes:

```text
Arabic-primary wording or source-specialist confirmation;
an actual-world interpretation or unique actual world;
complete profile reflection;
a Necessary Being, Creatorhood, personality, or Wisdom in neutral logic;
Speech or revelational identification;
an integrated champion, meniscus, or natural closure.
```
