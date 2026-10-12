# Dependent-pair eta remains independent relative to explicit Rigidity

## Checked result

Let SigmaRaw = Σ (_ : Raw), Raw, and let
Eta = Π (z : SigmaRaw), Id SigmaRaw z (pair (fst z) (snd z)).

`SigmaTagBoundary.relative_independence` proves, for the unchanged actual HasE grammar:

- There is no source polynomial p with HasE [] p (Rigidity → Eta).
- There is no source polynomial p with HasE [] p (Rigidity → (Eta → Bottom)).

`no_eta_under_rigidity` additionally states the first exclusion directly in the open source context [SigmaRaw, Rigidity] for the literal identity body. `no_eta` excludes closed Eta without Rigidity.

All checked by Lean 4.19.0 with --trust=0. Printed dependencies are limited to propext, Classical.choice, Quot.sound; no sorry or added axioms. `full_eta_valid` is axiom-free. Run `bash check.sh` from anywhere in this retained workspace.

## Actual all-rule model

TaggedPER is a separate interpretation, with the original finite open SKI carrier and faithful Raw = Conv. It quantifies over all conversion-saturated PERs at All. It differs from FullPER only by adding `(tag z ↔ tag w)` to the componentwise Sigma relation, where tag z means raw SKI conversion from z to its projection reconstruction.

`tag_congr` proves conversion invariance, and `tag_pair` proves that introduced pairs have the tag. The dependent Sigma PER, saturation, and context transport proofs have been updated. The complete mutual source induction `form_sound` / `has_sound` is checked over the actual HasE recursors, including impredicative All elimination, mixed substitution, J, proof erasure, source conversion, piExt, allExt, and the actual finite typing grammar. No inherited semantic Sigma eta law is imported as a source rule.

## Concrete discriminator

I inhabits SigmaRaw semantically because its two projections are Raw terms and its tag equals itself. But its tag is false. Assuming I convertible to its reconstruction, application to inert zero yields conversion of normal zero with the distinct normal term zero K (K I). The existing independently reviewed OpenDevelopments.normal_unique proves the contradiction. No new confluence development is used.

The reconstruction is a literal pair and has true tag. Thus the projections of these two objects are convertible (`matching_observations`), while their Sigma relation fails (`matching_observations_not_identity`). This is an information/identity boundary: equality of the listed first and second observations alone does not entail the corresponding source Sigma identity, even with explicit Rigidity. This is not a claim about physical continuation or any additional empirical reconstruction process.

## Why explicit Rigidity does not close this gap

The literal Rigidity type uses All/Pi/identity over Church N and no Sigma. `rigidity_exact` proves its interpretation agrees definitionally with FullPER; the previously checked generic Rigidity inhabitant remains valid. On the other side, the original componentwise FullPER validates Eta with K I and jointly validates Rigidity. These two actual source-sound interpretations establish both halves of the stated relative independence.

No extension has been adopted, no source rule has been changed, and no protected baseline file was edited. This bounded result does not assert that arbitrary dependent eliminators fail or that any particular additional completion principle is required. Source well-formation and further positive controls are undergoing independent review in a separate reviewer directory.

## Inputs and limits

`TaggedPER.lean` derives from retained `hase-full-per-extension-20261010/FullPER.lean` with namespace isolation and a narrow Sigma change. `Boundary.lean` reuses retained reviewed OpenDevelopments and RigidityDiscriminator modules. `INPUTS.json` hashes candidate files and the existing compiled search-path inventory; `validation/build.log` records successful elaboration. The script intentionally reuses already-built dependencies rather than rebuilding the campaign baseline. Independent replay is separate evidence.
