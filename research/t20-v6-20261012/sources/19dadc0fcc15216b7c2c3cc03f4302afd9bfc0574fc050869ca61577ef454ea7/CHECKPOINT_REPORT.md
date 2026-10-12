# Mixed substitution, auxiliary checkers and telescope codes

## Accepted increment

This additive packet preserves three independently accepted layers on the unchanged source syntax and natural encoding:

1. Primitive-recursive realizers for finite mixed term/type substitution, type renaming and instantiation, actual TypeCode substitution/compilation, and finite support.
2. Primitive-recursive realizers for all five actual auxiliary certificate checkers, with exactness on genuine encoded inputs.
3. Primitive-recursive canonical telescope validity and canonical decode₂/re-encoding, together with exact transport through the standard List Nat encoding.

The proofs use genuine root-qualified Mathlib primitive recursion and actual source operations, not an inference from executable Lean or Encodable alone. Selected Lean 4.19.0 trust-zero compilation, independent source/code controls and standard-axiom audits support the bounded claims. Preservation replay supplies additional reproducibility evidence, not another independent mathematical review.

No whole Joint/E serialized-checker computability or source-derivability RE theorem is claimed. The full certificate-domain validator, descriptors, Rule maps/templates and final certificate-tree recursion are excluded. T20 remains active.

## 1. Finite mixed source operations

Read `hase-coded-mixed-transformations-20261010/RESULT.md` and `hase-coded-mixed-independent-review-20261010/REVIEW.md`.

Finite environments distinguish the two binder sorts. Under pi/sigma, the term images are lifted and stored type images receive term weakening. Under all, term images stay fixed while type images receive the source type-variable lift. The literal source trename leaves embedded polynomials unchanged. TypeCode substitution uses its real upSub/singleSub equations, not an invented type representation.

Bottom-default type images and shifted-parameter fallback modes remain distinct under nested binders. Actual finite compilation uses arr, hence pi with a weakened codomain; finSupport takes maximum at arrow and saturating decrement at all. A separate open-arr control makes omitted weakening observable even though genuine finite translations have no free term variables.

The natural-code functions are total arithmetic extensions. Their exactness statements concern genuine source encodings and finite encoded environments. No arbitrary-function-environment computability, decoder agreement on malformed inputs or replacement source Primcodable instance is assumed.

Independent evidence includes 21 selected predecessor/candidate builds, 18 kernel source equations importing only retained AllSyntax, 16 direct code/environment equations, and all 67 named helper theorem axiom checks. Four author and ten independent false equations reject. The initial review punctuation failure is preserved as a failed fixture attempt, not accepted proof evidence.

## 2. Five actual auxiliary checker realizers

Read `hase-auxiliary-checker-computability-20261010/RESULT.md` and `hase-auxiliary-checker-independent-review-20261010/REVIEW.md`.

All 24 constructors across Step, Red, Poly, Finite and Lookup are covered. Exactness is against the original AuxiliaryCertificates.check… definitions on genuine encoded inputs.

- Step contextual cases require the child to certify the declared endpoints.
- Red connects the Step target and recursive Red source at the same intermediate term.
- Poly symmetry retains the child's original orientation, transitivity shares the same middle polynomial, application separates both branches, and the bridge distinguishes an atom containing a Term application from a Poly application of atoms.
- Finite allE uses the actual TypeCode instantiation with the correct image/body order and capture-avoiding shifts. Reduction checks both typing and the actual Red evidence.
- Lookup checks the entire telescope, declared index/type and actual weakening. Nested successor controls require three weakenings and reject a permuted context or missing weakening.

The review freshly compiled the actual AuxiliaryCertificates source, three grammar modules and all 13 candidate modules. It consumed the separately accepted mixed-review objects under exact pins. It added 38 source controls, 55 direct code controls, ten interface guards and an 83-helper axiom audit. Six author, ten independent source and five independent code-layout mutations reject for semantic reasons.

Canonical-input exactness does not make these totalized functions standalone syntax-domain validators. Malformed natural inputs may have behavior unrelated to an operational source decoder. A complete submitted-code checker must separately provide canonical domain gates and the remaining certificate/checker operations.

The ten interface guards check the real Mathlib Primrec constant, right-nested natural tuple order and exact correspondence to each original checker. Negative tests are discriminating examples, not exhaustive mutation coverage.

## 3. Telescope validity and standard-list transport

Read `hase-telescope-code-validity-20261010/RESULT.md`, `SUPPLEMENT.md`, and especially `REPLAY.md`, followed by `hase-certificate-domain-independent-review-20261010/TELESCOPE_REVIEW.md`.

The current workspace entrypoint is:

```
python3 hase-telescope-code-validity-20261010/verify_release.py
```

`CURRENT.md` preserves an earlier runner instruction and theorem inventory. Its verify_final.py command is superseded by REPLAY.md. The old final runner misclassified a generic proof module as an axiom-audit module and raised a Python KeyError after the Lean proof compiled. The release runner limits parsing to the three actual audits. Earlier negative tests also needed well-founded-evaluator reduction and a corrected namespace in a false list-code claim. All those sources/logs remain historical; no theorem was changed to repair the harness.

`validTel` is primitive recursive and recognizes exactly the unchanged Encodable image of Tel = List Ty, on every natural input. Nil is zero; a cons uses the retained successor-pair encoding, a canonically valid Ty head and a recursively valid tail. The tail decreases even for malformed positive codes.

The normalizer correspondence is to canonical Encodable.decode₂ followed by re-encoding. Ordinary source-decoder equivalence on all inputs is not asserted.

`encode_map_encode` is a generic algebraic identity for every Encodable source type, under the existing standard list codec. `listNatDecode` is the standard primitive-recursive List Nat decoder with empty default; on genuine encoded source lists it returns exactly the list of element codes. These results neither flatten the source codec nor infer Primcodable/computability of an arbitrary Encodable source type or function.

Independent telescope evidence has 16 selected builds, 15 theorem axiom audits, six genuine/four malformed runtime outputs, and three expected semantic rejections. It verified all 2,944 release pin entries and the 35-entry author release freeze. The telescope-only review freeze excludes the review directory's separate descriptor/global activity.

## Exact freezes and dependency provenance

- Mixed independent receipt: `1c3d8625b6a5668200b7dcea927bc2589f8de6a8421f521507ce05b259f6701a`
- Mixed review manifest: `8a2dcc4949cedba77791cefb4a901b030ee8a9fecbba568869ded106eaf718c6`
- Auxiliary independent receipt: `15f0912a54bb0a09731863ac35ba0f02ce9725c306eedd64a97bd6b5329a82d3`
- Auxiliary review manifest: `cab8f8e306ac2f2af18fa3bf7ee5ccf1180b59e4f25dba4c759dcbe3c6a7acd6`
- Telescope author release freeze: `249fd826de921673f25e9db8c9f4cc3051d9ed03d319a91f57c57423292277cc`
- Telescope independent receipt: `3a67a57764b9204a15847e856b14daf64186ef0d67403e30353a32bbbdb63c6b`
- Telescope-only review freeze: `402c5ac5b69faa3d6cf764daee3a681ab35e23018c00be7f85153b56f438e51a`

Author-consumed caches, independent rebuilt outputs and prior historical attempts retain their own paths/hashes. They are not silently treated as one interchangeable provenance record. The mixed review's retained AllSyntax/SubstitutionSyntax/FiniteBridge source/object bindings are preserved. Auxiliary EXACT_IMPORT_GUARDS records its exact first-resolved imported objects. The telescope accepted subset uses its released pins and freshly rebuilt selected modules; no provisional telescope dependency is accepted.

Our auxiliary replay intentionally consumes the exact pinned accepted mixed-review output, matching its original review. A separate mixed replay freshly rebuilds that lane's selected sources. This does not replace historically consumed helper pins with whichever newly rebuilt object is convenient. Each fresh lane has its own output library, preventing generic audit/control module-name collisions.

All three review scopes use retained imported objects. No complete baseline source rebuild, bootstrap validation, new compiler verification or new independent audit is implied. The preservation wrapper pins the original search-root order, whole object inventories in those roots, toolchain bytes, retained dependency files, first-resolved direct imports, frozen evidence and prior archives.

## Portable narrow replay

This is a compact source/evidence package with an exact dependency-reuse contract. It can be extracted elsewhere while the pinned original workspace remains available. It does not bundle the toolchain or cached objects and is not advertised as a standalone upstream source distribution.

Use the manifest SHA from the separate preservation receipt and a new output directory outside the extracted packet:

```
python3 /extracted/Mixed_Substitution_Auxiliary_Checkers_And_Telescope_Evidence_20261010/verify_replay.py \
  --expected-manifest-sha256 MANIFEST_SHA_FROM_RECEIPT \
  --workspace /path/to/pinned/workspace \
  --output /new/disposable/replay-output --replay
```

The established wrapper compiles 61 selected modules: mixed 24, auxiliary 21 and telescope 16. It checks all 38 expected semantic rejections: 14, 21 and three respectively. Exact compiler/runtime diagnostics are compared after only absolute source-path adjustment. The Lean `--root` option preserves original relative module identities. Original verification scripts are not run in place, and no frozen receipt is overwritten.

All retained pins and all 183 prior ZIP archives are checked before and after. Six negative custody guards reject tampering, omissions, extra files, symlinks, a wrong external manifest pin and existing output reuse. Custody-only mode omits `--workspace` and `--replay`.

`REUSE_CONTRACT.json` identifies accepted source/log records, original-copy bindings and historical-only files. Partial progress receipts, superseded runners and unsuccessful controls remain history, not additional successful verification. New descriptor/global validators, Rule maps/templates, final treechecker/RE work, publisher texts, protected changes, prior-archive rewriting and uploads are excluded.
