# PMR-007 Deep Round AP V1 — source-world referent identification

```text
identity: PMR-007-SWRI-1
round: PMR-007-DEEP-AP
version: V1
status: POST_MERGE_RESEARCH_CANDIDATE
historical_identity: NONE
repository_mutation: NONE
central_task: state the exact bridge from source-level co-reference to one world referent
```

## 1. Source and world structures

Let `S` be a finite source structure with a unique source object `g` satisfying
a selected role bundle `U_S`. Let `W` be a finite candidate world structure
with translated role bundle `U_W`.

Let `H` be the declared family of admissible source-to-world interpretation
maps. Every `h in H` is required to preserve the selected roles of `g`:

\[
U_S(g)\Rightarrow U_W(h(g)).
\]

Define the world-image fibre

\[
F_H(g)=\{h(g):h\in H\}.
\]

## 2. SWRI-1A — conditional world existence

If `H` is nonempty and every admissible map preserves the selected role bundle,
then some world object satisfies `U_W`.

This is conditional on the existence and adequacy of the interpretation family.
It is not a proof that the actual world realizes the source proposition.

## 3. SWRI-1B — exact world-referent identification

The source package identifies exactly one world referent relative to `H` iff

\[
|F_H(g)|=1.
\]

If the image fibre contains two objects, source-level co-reference does not
select between them.

## 4. SWRI-1C — role-complete interpretation family

Call `H` **role-complete for g** when every world object satisfying `U_W` occurs
as `h(g)` for some admissible `h`.

Under role preservation and role completeness,

\[
F_H(g)=\{w\in W:U_W(w)\}.
\]

Therefore the source role bundle identifies a unique world referent exactly
when the translated role bundle has a unique world realizer.

## 5. Positive anchor construction

An independently warranted anchor relation `A(g,w)` closes the referent bridge
when:

```text
there exists exactly one w with A(g,w);
every admissible map sends g to that w;
the anchor is not defined by the desired conclusion;
and its source, translation, version, referent, and world guards are valid.
```

## 6. Countermodels

```text
AP-CM1 EMPTY INTERPRETATION FAMILY:
  the source role bundle is coherent, but no admissible world interpretation
  is supplied. No world existence follows.

AP-CM2 TWO ROLE-EQUIVALENT WORLD BEARERS:
  two world objects satisfy every translated role and both are admissible
  images of g. Source co-reference holds while world identity is open.

AP-CM3 HIDDEN ANCHOR:
  two role-bearers exist, but H arbitrarily contains only maps to one. The
  singleton image is imported by the map policy, not derived from the roles.

AP-CM4 ROLE PRESERVATION WITHOUT REFLECTION:
  a world image may have extra predicates. The source does not establish a
  complete world profile.

AP-CM5 VERSION OR TRANSLATION DRIFT:
  changed role translation changes H and F_H(g). Old source bytes do not fix
  the new world referent.

AP-CM6 SOURCE-COMPATIBLE IMPERSONAL REALIZER:
  one impersonal world object satisfies the selected functional role bundle
  while personality, de se ownership, and Wisdom fail.
```

## 7. Track-N and architecture effect

The Asfahani translated source presents one creator as necessary, one,
knowing, able, living, volitional, speaking, hearing, and seeing. Accepting that
co-reference filters source models. It does not identify an actual-world
referent unless the source-world interpretation fibre is nonempty and singleton.

Thus source-compatible B1/C1 rivals survive whenever they realize the role
bundle under an admissible interpretation while withholding the neutral
personal or Wisdom discriminator.

## 8. Theorem family and nonclaims

The formal core is a standard image-fibre/interpretation result and a strict
source-world application of the recurring factorization family.

```text
general_mathematical_novelty: 0
historical_identity: NONE
repository_status: PROPOSAL_EVIDENCE_ONLY
external_review: OPEN
owner_adoption: PENDING
```

No result establishes Arabic-primary wording, source authenticity, translation
adequacy, actual-world realization, a Necessary Being, Creatorhood, personality,
Wisdom, Speech, revelation, integrated champion, meniscus, or natural closure.
