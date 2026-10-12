# P01 attempt-0003 qualification findings

This is a new, isolated qualification/repair record. It is not the original checkpoint receipt, historical attempt-0002 recovery, canonical adoption, a GitHub change, external peer review, or a claim about P02/P03.

## Input and environment

- Recovered outer archive SHA256: `2e4ea5fa98f0faa71a0dc160560f090e6bf250c32366f64c5e5ce8c9f80ef652`
- Canonical source basis: `03e2604dfcef278b01c60d19b05370fcec4194b6`
- Exact Lean: 4.19.0, commit `6caaee842e94`; Lake 5.0.0-6caaee8
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine locked dependency revisions checked
- Original input hash ledger: `INPUT_IMMUTABILITY.json`
- Shadow source: `shadow-packet/`; exact diff: `SOURCE_REPAIRS.patch`; per-file hashes: `SOURCE_CHANGES.json`

## Qualified result

The fresh strict run completed successfully at 2026-09-30 14:02:42 UTC. `strict-0004/QUALIFICATION.json` reports `KERNEL_VERIFIED_EXACT_PIN_SCOPED_TARGETS` and `kernel_credit: true` for the exact repaired shadow source.

It rebuilt all 30 modules plus the generated audit, verified 31 fresh nonempty `.olean` artifacts, and read back all 382 public declarations. The declarations comprise 224 `theorem`, 127 `def`, 8 `abbrev`, 12 `structure`, and 11 `inductive` declarations; 382 must not be described as 382 new mathematical theorems. All 18 candidate modules, all eleven unchanged load-bearing assertions, and all six generated finite replay examples passed.

The observed transitive axiom union is exactly `{propext, Classical.choice, Quot.sound}`. Of the 382 declarations, 257 have no axioms; all others remain inside this approved ceiling. No `sorryAx` or other nonstandard axiom is present. The compiler audit exited 0 with empty stderr. Its stdout is 110,147 bytes, SHA256 `76a0cf1e51e456dd997a2b6e906a82c46ac1f6865b11054538e0baede079ba7a`.

The qualified formal-source inventory SHA256 is `fc038de1adcd43120beec1f75a4d14aa0d8d33109f96cb024ae355efbe0ec839`. The generated audit, exact target/type readback, source hashes and artifact hashes are included. None of this retrospectively qualifies the unmodified input archive.

The public target set is exactly the original 382 names. No target was dropped or added to the checkpoint inventory. The additional scope tests under `supplemental/` are separately labeled new qualification tests.

## Repairs and statement/interface differences

Nine candidate Lean files required proof/interface repairs, and a tenth received an import-only execution repair. No original mathematical conclusion was weakened or replaced by a new premise, no source reduction or conversion rule was changed, and no proof hole or nonstandard axiom was introduced; the allowed Lean classical/propositional axiom ceiling is audited separately.

1. P01Candidates: after the existing induction rewrites, close two remaining definitional All/intersection equalities with reflexivity
2. P01Polynomials: use the well-founded abstraction equation and explicit simplification where `rfl` could not unfold it; the same K-priority abstraction and literal substitution-naturality/beta statements remain
3. P01PER: make transport across a definitional projection equality explicit; the same represented Sigma definition and saturation theorem remain
4. P01DependentCore: disambiguate ordinary identity from the definition being introduced (`Sub.id`); escape Lean's reserved `variable` identifier without changing its actual declaration name; supply classical decidability for the already noncomputable fibre choice; make dependent index types, fibre transport, environment equality and All introduction endpoints explicit
5. P01ContextualJ: escape the same identifier at uses; replace an ambiguous equality cast with `Eq.mp`; the two-coordinate motive and J conclusions remain
6. P01SystemF: explicitly identify the substituted context with its renamed context; typing rules and subject-reduction premises remain
7. P01Translation: repair parsing of nested tactic proof terms in the positive I/K/S simulation; the exact nonempty target-path conclusion remains
8. P01Examples: instantiate the generic arrow identity-extension lemma at both identical argument PERs, and prove the abstraction code binding using its defining equation
9. P01Certificates: correct an ill-kinded executable return type, `Option (Conv t u)`, to `Option (PLift (Conv t u))`. Lean's Option takes a Type, whereas Conv is a Prop. The successful result now wraps the same actual conversion proof in PLift; `join_sound` correspondingly compares with `some ⟨p⟩` and still concludes exactly `Conv t u`. This is an explicit representation-level interface correction, not an unchanged signature

Explicit binder annotations in fst, snd and sigma_eta_context resolve originally underdetermined elaboration; they express the intended same contextual domain/family. They are recorded in the diff rather than counted as new theorems.

10. P01TypeAlgebra: replace the unnecessary whole-library `import Mathlib` with `import Mathlib.Data.Bool.Basic`. A controlled fresh build of all 30 modules established that this supplies the actual lemmas/tactics used. This changes no mathematical declaration or target type and avoids the intermittent multi-minute full-Mathlib stalls
11. Generated audit: replace nonexistent Lean 4.19 option `pp.width` with the registered `format.width`. The original audit emitted all 382 blocks but correctly failed compiler qualification because of the invalid option; its failed output remains preserved

The original driver failed before compilation because `copytree(..., symlinks=False)` converted Batteries' tracked `docs/README.md` symlink into a regular file. The shadow driver resolves the top-level package directory, preserves interior symlinks, and retains all original pin/cleanliness/artifact/axiom checks. Lean runs with one worker thread to avoid observed import/resource stalls. The inventory scanner now recognizes the escaped source spelling `«variable»` while retaining the original qualified name `P01D.variable`.

## U09 meaning

The direct source reducibility proof covers the exact seven FiniteDerives rules. It establishes source strong normalization without assuming global System-F normalization. The separate Curry-System-F route proves both substitutions, lambda generation, subject reduction, exact typing preservation and positive compatible simulation. Its SN-reflection theorem remains conditional on actual target SN; no global target SN theorem is supplied.

Raw-source confluence, normal-form characterization of conversion, and Ω's lack of any finitely typed representative remain the source-level conclusions. Target beta equality still does not reflect raw source Conv. The canonical code membership and reducibility-candidate interpretations remain distinct.

## U10 replacement meaning and boundaries

The preserved ordinary manuscript constructs a separate endpoint-aware PER/relational interpretation. Arrow equality is typed behavioral equality. All adds an explicit uniformity restriction and assumes/proves body identity extension at the correct recursive boundary. Neither operation relabels the accepted canonical unary Code interpretation or source Conv.

The newly qualified Lean surface is narrower than the full surviving ordinary manuscript: it supplies generic PER, Link, represented Sigma, identity/J, ParamFamily/All interfaces and concrete inhabitants. ParamFamily carries body identity extension explicitly; AllFormation carries contextual body equality/coherence; allIntro requires a genuine uniformity proof. The source does not mechanically implement the whole recursive heterogeneous finite/dependent interpretation, its fundamental theorem, or the probability/coupling theorem. A successful generic interface audit must not erase those boundaries.

New independent exact-rational tests enumerate all 16 relations on two points and all 121 pairs of laws with masses in tenths (1,936 Hall/coupling cases), plus all 30,976 pairs-of-relations/common-intersection cases. They retain the equality/flip counterexample to exchanging `∀ relation ∃ coupling` with `∃ coupling ∀ relation`, refusal for unequal laws under equality-only support, and a zero-weight support control. These are finite semantic/implementation checks, not a general theorem or recovered attempt-0002 executable.

## U11 meaning

The core's terms carry one finite SKI polynomial plus a proof valid at related valuations. Generic ambient sections are not silently admitted as terms. The partial replay theorem consumes actual proof-carrying FiniteEnvelope or DependentEnvelope objects with exact code/type bindings. It does not verify the arbitrary Python/JSON interpreter or prove total export of accepted dependent syntax.

Pi abstraction congruence is at the typed relation of applications, not raw Conv of un-applied bracket compilers. Sigma eta applies only to represented inhabitants. J requires coherence in both endpoint and equality-proof coordinate. Legal All self-instantiation still supplies no same-level full-section Girard retraction. The unchanged canonical TypeCode image still excludes exact Id and Sigma shapes.

## Tests and exclusions

The checkpoint's complete Python suite passes 74/74 in normal mode and 74/74 under `-O`, against shadow sources. Five additional finite coupling meaning tests pass. The additional thirteen-declaration Lean scope check also compiled and passed the same in-Lean transitive axiom gate and unchanged strict readback parser, recorded in `supplemental/SCOPE_QUALIFICATION.json`. It formally confirms that I and S K K can be equal at every appropriate function PER while remaining raw-Conv distinct; Ω can inhabit a new empty-domain arrow PER and even an intrinsic tracked term without source SN; polymorphic identity remains nonempty and legally self-instantiates; and the PLift join interface both rejects distinct normal forms and returns an actual conversion proof on a successful path. These thirteen declarations are new qualification tests, separately counted from the checkpoint's 382 targets.

No GitHub mutation, owner adoption, canonical manifest/status promotion, newly reconstructed attempt-0002 source, general JSON refinement theorem, blanket semantic SN, arbitrary PER equality decision, same-level universe closure, novelty claim, or independent expert review is asserted.

## Record authority

The historical README, receipt, manifest and status files retained in shadow-packet describe the original uncompiled checkpoint. Source repairs invalidate their old source hashes for the shadow copy, so they must not be used as new qualification receipts. The new qualification result, source-difference ledger, and final artifact manifest are authoritative only for this explicitly identified shadow work. The immutable original retains its original seal and all 507 file hashes.

## Failed-run retention

- `baseline-0001`: original driver failed its dependency-cleanliness gate after dereferencing a tracked Batteries symlink. Source files, command evidence, receipt, and the problematic copied README are retained. Only the reproducible generated dependency cache was removed to reclaim disk; `CACHE_RETENTION.json` records this, and the original exact pinned cache remains intact
- `strict-0002`: broad-import run timed out at 300 seconds on P01TypeAlgebra without a compiler diagnostic
- `strict-0003`: broad-import run was interrupted after repeated long stalls, once the invalid audit display option was independently identified; it grants no qualification credit
- `narrow-development/logs/20260930T135743/P01Audit.stdout`: complete readback from the failed invalid-option audit; compiler exit 1 means no success credit despite all type/axiom blocks
- `strict-0004`: the sole authoritative successful complete isolated run for the final shadow packet

All recovered input hashes were rechecked after repairs: exactly 507 files, no changed, missing, or added files. All twelve canonical vendor source modules and the original P01TypeAssertions file are byte-for-byte unchanged.
