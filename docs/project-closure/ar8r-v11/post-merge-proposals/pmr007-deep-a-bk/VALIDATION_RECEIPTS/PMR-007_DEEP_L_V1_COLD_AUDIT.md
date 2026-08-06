# PMR-007 Deep Round L V1 cold audit

```text
audited candidate: PMR-007-SDL-1-CANDIDATE-V1
frozen receipt: PMR-007_DEEP_L_V1_FROZEN_HASHES.sha256
disposition: REPAIR_REQUIRED
```

## Blocking findings

### DL-F01 — OWN collapses authorship, utterance, attribution, and attribute subsistence

The V1 `OWN(g,c)` coordinate does too much. A speaker may utter a quotation without authoring its content; a source may author content without the current relay being that source; the Asfahani passage concerns Divine speech as an attribute not created in another, which is not the same relation as ordinary content authorship. Split:

```text
UTTER(g,c,e): episode-level speech act;
AUTHOR(g,c): content origination/authorship;
ATTR_N(g,s): Track-N source predicate that speech attribute s belongs to/subsists in g;
RELAY(e,t): token relay relation.
```

### DL-F02 — AUTH hides several independently failing custody coordinates

`AUTH(g,e,t,k)` bundles source identity, episode identity, provenance, version, authorization, and current applicability. Existing AR2/AR3 and PMR results require these to remain separate. Split them and preserve their guard-deletion models.

### DL-F03 — source-conditioned disclosure is partly stipulated

Adding `UNCR_N` to the conjunction does not prove uncreated status; it classifies a disclosure under an accepted source premise. The repaired packet must explicitly distinguish:

```text
neutral expression/relay fact;
source-authenticated attribution;
Track-N uncreated-speech predicate;
revelational identification.
```

### DL-F04 — created-token status is not typed

The packet calls `t` a created token but includes no `CREATED_TOK(t)` coordinate. Add it as an explicit model/source premise. Expression alone does not determine the token's ontological status.

### DL-F05 — empty bearer model is framework-sensitive

`L-CM1` uses an empty bearer set. Replace it with a nonmental dummy/abstract domain or explicitly use a semantics allowing empty sorts. The nonentailment needs no empty sort.

### DL-F06 — source custody and exact locators are not frozen

Freeze the supplied Asfahani English bytes and exact phrases concerning informative/compositional speech, uncreated speech, origination from Allah rather than creation in another, and nonseparation from the bearer. Preserve translated-primary authority and the absence of Arabic-primary verification.

## Nonblocking notes

1. The articulability→mentality→capacity→occurrence ladder is correctly nonentailing.
2. Target-relative fidelity is correctly distinguished from full content identity.
3. The round is central source-formal-world adjudication, not general mathematics.

## Required repair

```text
split utterance, authorship, source attribute, and relay;
decompose custody/authentication guards;
add created-token predicate;
replace empty-sort witness;
classify the positive source contract conditionally;
freeze source custody;
run distinct relation/custody rereview.
```
