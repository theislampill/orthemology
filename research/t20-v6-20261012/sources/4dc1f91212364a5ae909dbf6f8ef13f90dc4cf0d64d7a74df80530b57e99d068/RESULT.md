# Generic Peano rigidity discriminator

## Result

The exact source type `SourceRigidity.Rigidity` is valid in the intended whole-HasE FullPER interpretation and independent of the unchanged source calculus: there is no closed HasE proof of it and no closed HasE proof of its internal negation `arr Rigidity bottom`. Both exclusions also hold for original Has by inclusion. These are metatheorems about all proof polynomials, not source derivations of negation.

`RigidityDiscriminator.lean` adds the consequential discriminator without changing the seven existing modules, the source grammar, a typing rule, the original compiler, or a protected repository.

## Exact statements and interpretation

- `peano_rigidity`: any supported endomorphism of churchPER that preserves zero and successor is PER-related to I in the full cross-input function PER. It uses Church standardness to relate an arbitrary input to a finite numeral, induction on that numeral, and the supported successor operation. It does not specialize the endomorphism to q.
- `rigidity_valid`: FullPER.F of the exact source Rigidity relates the interpretation of the fixed source polynomial c3 to itself, for every type environment and term environment. This checks the entire dependent source type, including both related endomorphisms and related identity-proof arguments.
- `rigidity_fundamental`: the same fixed realizer works at two arbitrary related outer environments, for any context.
- `rigidity_uninhabited`: a hypothetical original HasE inhabitant specializes through the already checked unchanged-source `identity_from_rigidityE`, uses `result_exact`, then contradicts the existing `HomogeneousOriginalIdentity.original_identity_uninhabited`.
- `no_internal_negation`: a hypothetical HasE proof of `Rigidity → bottom`, interpreted by FullPER.fundamental in the admissible empty environment, maps the semantic rigidity realizer to the empty bottom relation. Hence no such source proof exists.
- `source_independence` and `source_independence_Has`: package both all-polynomial exclusions for the two unchanged source judgments.

The already present `SourceRigidity.rigidity_implies_identity` is a genuine closed original Has proof of the implication to the literal identity. Its antecedent has not been adopted or proven. In particular, semantic validity does not promote c3 to a source inhabitant of Rigidity. This research selects a sharply characterized missing generic principle; it supplies no new inference rule and proves no source completeness or conservativity theorem for an extension.

## Ancestry and scope

The semantic branch uses `RecursorUniqueness.church_related_numeral`, hence `OpenTermStandardness.church_standard`, plus the existing typing of successor and its interpretation by the independently defined FullPER soundness theorem. Exact syntactic-zero/successor interpretation lemmas are checked in the new module. The c3 application/evaluation lemmas come from FullPER.Application only for proof-realizer normalization.

The negative branch uses the separately retained homogeneous countermodel: OriginalIdentityNoninhabitation → OriginalWNoninhabitation → HenkinSoundness and its concrete eligible PER universe. Its identity obstruction was already established; this module does not rebuild or alter that countermodel. The branch showing no internal negation instead uses the intended full-PER model. The two arguments do not assume the same semantic quantifier domain, and no such identification is made.

`SourceFoldContract`, `SourceFoldApplication`, and `InternalRecursorPrinciple` remain earlier conditional/source-formation work. No source implication from Rigidity to the more general polymorphic recursor Uniqueness is asserted here; that is a distinct question.

## Verification

Run `python3 replay_discriminator.py` in this directory. It first verifies `DISCRIMINATOR_INPUT_HASHES.json`, replays the eight new modules with Lean 4.19.0 and `--trust=0` into a fresh validation directory, checks printed axiom sets against only propext, Classical.choice, and Quot.sound, and rechecks pinned inputs afterward. It reuses compiled baseline dependencies and third-party libraries; it performs no baseline rebuild. `DISCRIMINATOR_REPLAY.json` records per-module exit codes and hashes of sources, logs, and output objects. This is fresh checking of the new proof modules against retained ancestry, not a claim that all retained ancestry was rebuilt during this run.

Independent frozen replay and transitive Lean constant-ancestry audit passed in `../hase-generic-rigidity-review-20261010/`. In particular, peano_rigidity and rigidity_valid exclude q-specific equality/fusion, SourceFoldContract, and HomogeneousOriginal noninhabitation dependencies; the negative proof intentionally includes the original identity/W obstruction and q’s syntactic laws. The detailed independent ancestry log is `logs/DependencyAudit.log` there.

Author replay: PASS, all eight modules, all pinned inputs unchanged. The initial harness tried NaturalityBoundary before its SourceFoldApplication dependency; that ordering diagnostic is retained under validation, and the corrected topological-order fresh replay passed. No proof source changed to resolve that harness issue.
