# PMR-007 Deep Round AW V1 — provenance-root robust diagnosis

## Candidate status

```text
identity: PMR-007-PRAD-1-CANDIDATE-V1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: NOT CLAIMED
```

## 1. Root-level diagnosis code

Let `H` be a finite hypothesis set and `G` a finite set of independently
authenticated provenance/acquisition roots.  Root `g` returns one complete
root-level certificate symbol `c_g(h)` under hypothesis `h`.  All copies,
paraphrases, repeated tests, and messages deriving from `g` are grouped into
that one corruption unit.

For selected roots `R subset G`, define the codeword

```text
c_R(h) = (c_g(h))_{g in R}
```

and minimum root distance

```text
d_R = min_{h != h'} |{g in R : c_g(h) != c_g(h')}|.
```

## 2. V1 candidate thresholds

V1 proposes that exact diagnosis surviving any `f` corrupted roots exists iff

```text
d_R > f
```

for both:

```text
identified erasures:
  the decoder knows which roots failed;

adversarial substitutions:
  corrupted roots may return arbitrary unmarked symbols.
```

Copies within one root do not increase `d_R`.  Distinct displayed labels count
only after actual-root authentication.

## 3. Intended application

The model connects robust collective diagnosis, false-tawatur, experiment
design, theorem-origin multiplicity, source-route independence, and
restorative evidence.  It does not establish root authenticity, truth,
tawatur warrant, authorization, common knowledge, or real-world independence.
