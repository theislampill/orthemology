# T20 type evidence, v3: a whole-HasE full-PER model now exists

10 October 2026. **The whole-model extension obligation is discharged for one
explicit interpretation. The literal source judgement `HasE [] c3 (W q)` and its
negation remain OPEN.** Semantic validity does not supply source derivability.

Read hase-full-per-extension-20261010/RESULT.md first, then its independent review
at validation/independent-review/REVIEW.md. The earlier root README.md is the
unchanged historical v2 guide; its earlier “no whole-model soundness” boundary is
superseded only by the concrete new result described here.

## What changed substantively

The new FullPER.lean constructs a coherent interpretation of the actual imported
HasE calculus on the previously reviewed finite open-SKI carrier. Fresh mutual
induction on the actual syntax establishes saturated-PER formation, dependent
coherence across related contexts, and soundness for **all twenty actual HasE
rules**. Coverage includes dependent Pi/Sigma, J, proof erasure, conversion,
piExt/allExt, finite builtins, and impredicative All instantiation at every formed
type. Hereditary semantic laws are conclusions, not extra formation premises.

All quantifies over every conversion-saturated PER. This is external type
quantification in the actual grammar, not an assumed term-level enumeration of
all PERs. Identity evidence uses the I-conversion class. Sigma uses a projection
PER without the inherited model's extra represented-pair predicate; this deliberate
choice is disclosed and all actual Sigma rules are proved sound for it.

The new theorem does not borrow soundness of the inherited F/G interpretation.
Independent kernel-environment dependency audits exclude the inherited semantic
definitions and soundness/fundamental constants for six principal conclusions.

## Exact application, and the remaining boundary

Application.lean identifies the new interpretations of actual N and N→N with
the earlier full-PER Church and arrow relations. It establishes:

- The actual imported original compiler and identity endpoints are related at N→N.
- Their represented typed identity is inhabited semantically while their raw
  evaluations remain nonconvertible in the same sound interpretation.
- Every finite successor numeral inhabits N; the empty context is inhabited;
  no closed actual HasE derivation inhabits Bottom.
- The actual pinned ScalarFusionCore.lean definitions W and c3 are imported.
  The actual c3 is semantically in W applied to the actual original compiler;
  the semantic relation also holds at arbitrary related outer environments.

The later LiteralScalarFusion module and its four-way source equivalence were
not rebuilt here. Its retained q alias was inspected and matches the imported
redundant compiler endpoint; no newly imported alias theorem is claimed.

This sound model cannot separate the target. It does not prove completeness,
uniqueness, validity in every PER/Henkin model, the source target, or its negation.
Different justified models or a syntactic argument remain separate obligations.

## How the older evidence fits

1. Open-term standardness: full saturated-PER Church membership iff one uniform
   finite iteration count, with concrete numeral inhabitants.
2. Imported compiler transport: actual pinned source correspondence, injective
   embedding, and preservation/reflection of raw conversion.
3. Raw-motive boundary: the actual theta endpoint cannot be typed Raw while its
   proof coordinate can; no raw reflection follows from an assumed typed identity.
   That earlier package uses inherited F/G soundness. The new independent controls
   establish analogous boundaries from the newly proved fundamental theorem.
4. This package closes the previously conditional whole-model extension premise
   for this concrete interpretation and proves the exact semantic application.

The proposed additional closed-source Church-canonicity result was rejected as
an extra contribution: EffectiveStandardness.semantic_church_standardness plus
inherited ExtensionalRepair.unary_fundamental already supplies observational
standardness for closed HasE terms of type N. The new model offers another route,
not a newly earned conclusion. Unary PER semantics has classical ancestry; no
field-level mathematical novelty or actual-world/philosophical conclusion is claimed.

## Preservation and exact bindings

All 174 files from v2 are retained byte-for-byte. Its old index is preserved as
preservation/V2_ARCHIVE_CONTENTS.json; preservation/V2_PRESERVATION.json gives the
exact path mapping. The v1/v2 ZIPs and their receipts remain unchanged. This adds
only the new package's 24 manifest-listed payloads and its unchanged manifest,
plus this guide, additive replay/verification tools and preservation metadata.

The new manifest SHA-256 is
151def7fb3c5bf543810c1be42601957bccfddce163571468ae72b17c7db479f.
The final independent review SHA-256 is
8228b3f21537dae3e9ac1162425a9797c2e67c254ce3542bece56e4f1604f1bb.
The source pin remains 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c.

No build objects, library overlays, symlinks, or entire dependency trees are bundled.
Historical author/reviewer scripts and receipts retain their original paths and
status wording. Use the additive tools below to avoid writing into reviewed trees.

## Verify and replay this v3 addition

Run `python verify_v3.py` in the extracted root. It checks all four frozen manifests,
187 manifest-listed payloads, every v2 preservation mapping, and the full v3 index.
Then, with Python 3.9+, Git, the retained Lean 4.19.0 toolchain, and already-built
pinned dependencies:

    python replay_full_per.py \
      --lean /path/to/lean-4.19.0-linux/bin/lean \
      --packages /path/to/pinned/.lake/packages \
      --prerequisite-objects /path/to/reviewer/fresh-lib \
      --out /path/to/new-output-directory

The prerequisite receipt binds 89 existing objects: 83 original project modules,
the four prior standardness/transport proofs, and two Mathlib prerequisites.
The wrapper verifies every object hash against that retained receipt, verifies
source bindings, Lean executable hash/version, and package pins, then reuses the
objects read-only. It does **not** rebuild the 83-module closure.

Only FullPER, the actual ScalarFusionCore, Application, the author's dependency
audit, the independent controls, and the independent dependency audit are compiled
anew, once each, all with --trust=0. All outputs go outside the archive. The two
audit sources share a basename and receive separate output subdirectories.
The frozen source/index bytes are rechecked after replay.

Only standard Lean propext, Classical.choice and Quot.sound are admitted by the
checked conclusions. Existing third-party objects are reused; Lean has not been
bootstrap-verified. No installs, protected edits, publication or programme closure
are performed or implied by this preservation replay.
