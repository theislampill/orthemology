# Independent review: imported compiler transport

## Verdict

**PASS for the stated additive, reduct-level claims.** No blocking mathematical or Lean defect was found in `proofs/ImportedCompilerTransport.lean`, reviewed at SHA-256 `448e9f950a1c51a9267ca04671fe6ade3377a485692621bd8252925ae02fbdbc`.

The exact original compiler endpoints are now formally connected to the independently reviewed open-term full-PER construction. The embedding is injective and preserves **and reflects** inherited raw conversion. The actual endpoints are related at the new Church-to-Church arrow PER while retaining their original raw nonconversion.

This is not a full HasE model or soundness result. The literal judgement `HasE [] c3 (W q)`, its negation, and its witness remain unestablished by this package.

## Independent replay and assumptions

I rebuilt the complete 83-module source closure from the supplied source bytes, both absent Mathlib modules, and the three inherited proof modules into a new `validation/independent-lib/` directory. No author's project `.olean` files were used in that replay. I then compiled the final transport and the reviewer-only checks using Lean `--trust=0` against the fresh reviewer outputs. All 90 compilation invocations exited 0: 83 original modules, 2 Mathlib modules, 4 additive/inherited proof modules, and 1 reviewer-check module.

Environment:

- Lean 4.19.0, executable commit `6caaee842e94`.
- Local Mathlib checkout `c44e0c8ee63ca166450922a373c7409c5d26b00b`; its working tree was clean. The two additionally rebuilt Mathlib source files were also compared directly with `git show HEAD:<path>`.
- Existing third-party dependency artifacts were reused through the package library paths. The Mathlib overlay consists of symlinks to those existing artifacts plus the two fresh Mathlib objects. The reviewer did not change the Mathlib checkout.
- `--trust=0` is Lean's supplied import-checking mode. This review remains relative to the installed Lean executable and dependency installation; it is not a bootstrap verification of the compiler binary.

Evidence:

- `INDEPENDENT_SOURCE_REPLAY.json` and `INDEPENDENT_REPLAY.log`: local binding checks, clean 83-module closure replay, two external rebuilds, three frozen proof rebuilds.
- `INDEPENDENT_TRANSPORT_TRUST_ZERO.json` and `.log`: final transport replay, exact source digest, successful exit, and source stability across the command.
- `INDEPENDENT_CHECKS.json`, `.log`, and `IndependentTransportChecks.lean`: explicit theorem signatures, additional semantic checks, and all 20 exported transport-theorem axiom reports.
- `INDEPENDENT_REVIEW_RECEIPT.json`: final reviewed-source and evidence digests, plus index consistency checks.

The bridge results depend on no new postulate. Their printed dependency union is `propext`, `Classical.choice`, and `Quot.sound`. `source_step_sound`, `source_conv_sound`, `erase_conv`, and `source_plus_sound` have no axioms. The original-source endpoint result and raw-separation result use the stated ordinary Lean axioms. No `sorryAx` appears in any inspected theorem's dependency list. A source scan of all 83 imported modules and four proof modules found no `sorry`, `admit`, `unsafe`, `implemented_by`, `native_decide`, or new axiom declaration outside comments.

## Source and frozen-package binding

For every one of the 83 imported modules I independently recomputed SHA-256 and the Git blob SHA-1, compared both with `ACQUISITION.json`, checked the source-store path's digest and filename, and parsed the actual import declarations after stripping comments. The import graph matches the manifest exactly, is acyclic, reaches all 83 entries from `UArrowAndCompilerControls`, and has no missing local module. The supplied source directory contains exactly those 83 Lean files.

The retained `PINNED_SOURCE_INDEX.json` contains exact path/digest entries for all 83 files. Each has `projection: EXACT` and equal original/public SHA-256 values. Its exact bytes hash to the acquisition receipt's Git blob `964b610cad10e90ec42311721e111cf55e221b4e`; its SHA-256 is `bd91569fda9fb4249680c020eda88bfa7a88dd264f318154083ae84b7677f432`. The acquisition receipt identifies `theislampill/orthemology` at immutable commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c` and the read-only GitHub fetch for the index.

Provenance qualification: the parent supplied the retained successful immutable-pin acquisition evidence. My independent live Git-tree request returned a connector transport-closed error, so this review independently verifies the retained receipt/index/byte binding, not a second successful remote fetch of every path. No local checkout of the source repository is asserted. The five source files also present in the frozen prior package match it byte-for-byte.

`OpenTermStandardness.lean`, `FrozenCompilerMirror.lean`, and `PERInterface.lean` are exact copies of the frozen prior package's reviewed files. Its complete manifest verifies, and a before/after snapshot showed no change anywhere in that package during the clean replay. The reviewer did not edit any original source, author proof, or frozen-package file. All reviewer outputs are additive files under this package's `validation/`.

## Mathematical bridge audit

### 1. Conservative raw embedding

`embed` maps the five inherited constants and application homomorphically into the larger finite open-term carrier. It introduces no new reduction. `erase` maps each added free variable to the existing inert zero constant and otherwise acts homomorphically. `erase_embed` proves an actual left inverse on every inherited raw term; `embed_injective` therefore has no carrier-identification premise.

Every original Step constructor, including left and right compatible contexts, is preserved. Original Conv is preserved by induction over its four constructors. Conversely, every new open-term Conv constructor erases to original Conv, including arbitrary intervening open terms. The retraction consequently proves `Conv (embed t) (embed u) ↔ OrthemologyV3.Conv t u` for all original terms. This does not assert that erase is an inverse on arbitrary open terms or that embed is surjective.

`original_raw_endpoints_still_distinct` applies this reflection theorem to the original imported `endpoints_not_convertible`; it does not merely recheck different pretty-printed endpoints. Reviewer checks additionally derive `¬ Conv I q` in the same new carrier as the typed agreement theorem.

### 2. Exact polynomial and binder transport

`poly` preserves de Bruijn variables and application and applies embed only to atoms. `map_psub`, `map_freeZero`, and `map_drop` establish the corresponding structural equalities for every source polynomial, including polynomials with free variables.

`map_abstract` is equality of the original abstraction algorithm's image with the mirror algorithm, not only agreement after application. Its two application branches preserve the whole-subterm K-priority decision: an absent bound variable produces K applied to the dropped whole subterm; a present variable uses the recursive S branch. There is no eta contraction or replacement by an extensionally equivalent binder.

`map_eval` relates original evaluation to new evaluation under the embedded original environment. Separately, `interp_abstraction_beta` is quantified over an arbitrary `Nat → T` open valuation and arbitrary argument, so it is not restricted to environments in embed's image.

### 3. All actual conversion generators

`source_plus_sound` inducts directly over the imported `P01AC.Intensional.Plus.PolyConvPlus`. All eight constructors are covered: reflexivity, symmetry, transitivity, application, I, K, S, and atom/application bridge. The bridge case is reflexivity because embedding and evaluation compute both representations to literally the same application. The valuation is arbitrary in the open carrier. No HasE derivation, typing premise, normalization hypothesis, or compiler-specific restriction is used.

### 4. Actual compiler output and environments

`original_q_poly_exact` rewrites with the imported `P01AC.ExtensionalRepair.CompilerBodyControl.redundant_closed_exact`, then uses formal abstraction transport and the original named compiler constants. The left side is the actual imported `redundantExpr.closed`, not a replacement definition. The target is the frozen pair-state mirror. `original_p_poly_exact` likewise imports the literal original variable-compiler theorem. The unrelated `UArrowControl.q = K K` is never substituted for the compiler endpoint.

`q_eval_independent` proves independence of the mirror's valuation for every open environment. `original_p_eval_exact` and `original_q_eval_exact` then hold for every original source Env, rather than merely the default environment. Reviewer-only checks also establish exact interpretation and typed endpoint relation across two independently chosen arbitrary open valuations.

### 5. Typed conclusion and its boundary

The endpoint theorem concludes the explicitly constructed `(arrowPER churchPER churchPER).rel`. This is genuine relational arrow equality: the inherited proof handles heterogeneous related inputs. It is neither raw conversion nor the original syntactic identity judgement. Its derivation uses the previously reviewed full quantification over all conversion-saturated PERs on finite open terms, including the fresh-generator orbit needed for uniform finite iteration.

No additional semantic assumption was inserted in the transport theorem. Nevertheless the conclusion is limited by its chosen semantics. It does not show that this full-PER carrier interprets every dependent, impredicative, or identity rule of HasE; it does not establish admissibility of the fresh orbit in another Henkin collection or provide fresh generators in a closed-only carrier. It therefore cannot close all possible PER countermodel routes or infer a HasE witness from semantic relatedness.

## Final disposition

The former formula-mirror/import gap is closed for the compiler endpoints and the stated raw/polynomial operations. Raw nonconversion is explicitly preserved. The full-calculus soundness and literal HasE witness gaps remain open and must remain prominent in any summary. No source correction is requested by this review.
