# 05 Tensors and Correction Geometry

Source-reader extracts for the 11 October 2026 catch-up. This is a reading aid, not a canonical T20 consolidation or a new research result. Original source wording and historical status are retained below; later documents may supersede earlier ones. Each source is identified by its original archive path and SHA-256.

---

## Source 7a4a668420

Original location: `T20bigupdate(1).zip!/T20_Channel_Tensor_Research_Evidence_20261010.zip!/T20_Channel_Tensor_Research_Evidence_20261010/README.md`

SHA-256: `7a4a668420ee092afa9a641425af71183b7045ac947da3a10c80971c3a83e4f5`

### Original document

# Fixed channels, positive instruments, and tensor-likelihood closure

Portable, additive research evidence, 10 October 2026. Author and independent-review packets are preserved byte for byte. These are ordinary mathematical proofs and finite exact controls, not a formal audit or proof-assistant certificate.

## Results preserved

- Fixed finite passive channel: a nonempty closed convex law family is stable under every defined outcome exactly when its extreme laws are supported within equal-outcome-column blocks. The packet also gives the minimal stable hull and the repeatable-observable crosswalk. This is a global outcome-wise condition; one-prior feasibility and finite posterior reachability are different contracts.
- Proper finite cones: identity-summing positive instruments act by scalar reweighting on canonical indecomposable summands. The cone/instrument transport keeps admissible operations explicit: an intrinsic positive feasible-cone map need not lift to one fixed passive diagonal likelihood about the original target.
- Proper interaction-moment hierarchies: exact passive probability-plus-retained-posterior update on the full law simplex permits only constant likelihoods, for both binary and nondegenerate finite product alphabets. Strictly positive posterior-only updates have the same obstruction; zero-supported likelihoods have the stated support-rank exception. The associated proper-order moment cone is indecomposable; full order recovers the orthant structure.

Independent reviews report no blocking defect under the stated hypotheses. The preserved author controls have 9, 16, and 13 groups; the respective independent controls have 7, 7, and 12 groups. Finite computations corroborate examples and boundaries, not universal theorems by enumeration.

## Provenance and the two cone versions

The current reviewed cone RESULT has SHA-256 `5c74c7086c038dce1be0e9098b42fce9cc4c7aee8670fe0ba682b50d780af5c0`. The unchanged tensor author instead binds `e9f9a5465aa9f6f03f789f852e87a9847f4aa8b5641866b8c293ad2c9a1bb086`. Running its verifier against the current cone therefore correctly fails the input guard.

Both byte sequences are retained. The earlier result is a hash-matching reconstruction by exact reversal of two recorded precision edits, not an independently retained historical snapshot. The delta packet preserves the reconstruction provenance and exact diff. Replay creates separate current-cone and historical-cone workspace trees and never overwrites either preserved evidence version. The frozen tensor author report is not edited. Its review clarifies “first-slot” to “first-order” and that the displayed six-dimensional closure presumes a nonconstant first-slot likelihood, for its multiplication operator or the binary channel {L,1−L}. An otherwise unspecified larger channel need not have that closure. “First-order” includes observables across all slots.

Established ancestry remains explicit: Bayes-plausibility/splitting and compact convex extreme-point arguments; the inherited H-Continuation invariant-observable/intertwining theorem; Loewy–Schneider's cone identity-extremality theorem and the Barnum–Wilce / Heinosaari–Leppäjärvi–Plávala componentwise results; Walsh/Fourier and stabilizing-algebra machinery. These are bounded new-to-packet deductions and applications, with no field-wide novelty claim. The underlying source-read scopes and accessible external source URLs are preserved; no unretained external PDF bytes or exhaustive literature search are implied.

## Files and replay

- `workspace/`: the seven named packets at their original workspace-relative paths, plus every direct local input required by their verifiers and declared source bindings. The historical replay workspace contains only the tensor author and its nine bound inputs, not a conjectural earlier full cone packet. Required reviewer snapshot trees remain intact.
- `SCOPED_INPUTS.json`: input roles, exact sizes/digests, read scopes, and historical substitution provenance.
- `ORIGINALS_BEFORE_AFTER.json`: source-file before/after hash evidence from preservation.
- `METADATA.json`, `MANIFEST.json`: precise scope, runtime, original package identities and every preserved file's size/digest. The outer archive receipt separately binds the ZIP and manifest, avoiding a self-hash claim.
- `replay.py`: integrity checks, three author verifiers, three independent-review control programs, the cone review's author snapshot, the tensor review's portable snapshot replay, and an expected-failure check for current-path cone drift. It compares recorded outputs byte for byte and verifies the preserved bundle is unchanged afterward.

Extract the ZIP into a new directory. From the extracted bundle, run:

    python3 replay.py --verify-only
    python3 replay.py --work-dir /path/to/new-empty-replay-destination

The destination must not yet exist and must be outside the extracted bundle. All writes are confined there. Python 3.10 or later and its standard library are sufficient; tested runtime details are in the outer receipt. No network, Git checkout, compiler, Lean build, or third-party package is required. `REPLAY_RECEIPT.json` and logs are written to the new destination. Fresh-extract replay evidence supplied with this archive records the exact archive hash it tested.

Older source-binding files are retained as bounded ancestry records; this package does not recursively preserve or rerun their historical dependency closures. No protected repository file is changed. The archive adds no empirical/actual warrant, physical realizability, epistemic or normative authority, metaphysical conclusion, integration approval, or T20 closure. Separately ongoing leafwise-geometry and source research are outside this frozen archive.


---

## Source 8fcbc51a17

Original location: `T20bigupdateprev(1).zip!/T20_Nonseparable_Bayes_Repair_Reviewed_20261009.zip!/T20_Nonseparable_Bayes_Repair_Reviewed_20261009/START_HERE.md`

SHA-256: `8fcbc51a17bd5ffe435f0f6ab52e107bb407922399f744e6271c30e60e52ad62`

### Original document

# Reviewed nonseparable Bayes-repair mathematics

9 October 2026 UTC. Intermediate T20 preservation only. This is a separate research unit, with ordinary mathematical proofs and exact executable controls. It does not certify a formal proof, field novelty, repository integration, release readiness, actual noetic warrant, or T20 closure.

Start with `nonseparable-bayes-repair-20261009/RESULT.md`, then `nonseparable-bayes-repair-review-20261009/FINAL_REVIEW.md`. The report classifies first-argument normalization-projecting generators as perspective-plus-mass potentials, proves the Hessian and divergence formulas, and constructs a globally forward radial repair under positive-definite Hessian conditions. Its box proof, coordinate-free transport, and counterexamples preserve the stated scope guards.

## Contents and provenance

- The author report, controls, log, source ledger, and original manifest are copied byte-for-byte.
- The independent review, seal, analysis, separate controls/results, reviewed snapshots, and author rerun log are copied byte-for-byte.
- The targeted primary ancestry note and the cited separable predecessor report are preserved. The predecessor is a source reference, not its full worktree.
- `MANIFEST.json` hashes every other archived file. The manifest intentionally does not hash itself; the external preservation receipt binds the manifest and the complete ZIP.
- `PUBLISHED_SOURCES.json` records the published source URLs and available byte digests. No modern published PDF, executable cache, environment, or unrelated temporary file is included.

## Reproduce

Requirements: Python 3 and SymPy 1.14.0. No network access is needed to run the controls. From this extracted directory:

    python nonseparable-bayes-repair-20261009/verify.py > private-locator:abd1c1bb24f5e0818f40
    cmp private-locator:abd1c1bb24f5e0818f40 nonseparable-bayes-repair-20261009/verification.txt
    python nonseparable-bayes-repair-review-20261009/independent_controls.py > private-locator:ea357e33b533d05cbb2e
    cmp private-locator:ea357e33b533d05cbb2e nonseparable-bayes-repair-review-20261009/INDEPENDENT_CONTROLS.json

Expected: 55 author controls and 28 separate reviewer controls pass. Both rerun outputs should exactly match the preserved logs. Those examples supplement the general written proofs; they do not formally certify them.

To verify archive contents, recompute each file's byte size and SHA-256 against `MANIFEST.json`. The accompanying external preservation receipt records a genuinely fresh extraction, verification before and after both reruns, successful exits, and byte-identical rerun logs. Any alteration to a reviewed report or control source requires a correspondingly updated review.


---

## Source 1221022aa3

Original location: `T20bigupdatenext02(1).zip!/joint-atomic-geometry-preservation-20261010.zip!/joint-atomic-geometry-preservation-20261010/README.md`

SHA-256: `1221022aa3e1f159d63177d7537e07c94556b15025673f869513246a0a4c37d7`

### Original document

# Joint atomic gradient geometry: intermediate preservation

This packet preserves additive intermediate evidence within active T20. It does not authorize integration, protected changes, empirical/philosophical identification, or closure.

## What is preserved

Three separately authored components and their independent acceptance records are preserved byte-for-byte:

- A joint positive-atomic gradient lift, with the metric, full-moment cometric, finite-coordinate realization, continuation hypotheses, and convergence qualifications.
- A concrete two-atom moving-support moment chart, with rational closure and exact algebra controls.
- A primary-source interface comparing the atomic tangent/action calculation to classical spherical transport/reaction geometry, with explicit normalization and domain caveats.

Prerequisite reports and their input digests are included sufficiently to reconstruct the cited assumptions and ancestry. They are reports, not complete reproductions of every preceding project. Any historical kernel results mentioned by those reports are inherited claims; this packet does not rebuild or newly kernel-verify them. Independent reviewer records remain separate from author proofs.

## Scope distinctions

The finite-rank path promise and positivity hypotheses remain substantive. The coercive gradient continuation result inherits the forward-complete/lower-killing-bound theorem. Its finite-time transitions are injective, with inverses on their actual images; global surjectivity onto all finite laws is not inferred. Finite-time rank preservation does not prohibit asymptotic collapse. Nonconvex energy descent does not imply global minimization.

The source interface establishes a fixed-path tangent action and a local metric-speed comparison in its specified domains and conventions. It does not transfer a global ambient geodesic, density existence/convergence theorem, or an unrestricted global metric identification. In particular the optional static Dirac twice-angle calculation must be read with its explicit domain-specific bridge caveat.

## Replay boundaries

Python and SymPy must already be installed. Replay does not install packages or use the network. After extracting the ZIP to a new directory, run:

    python replay.py --output /absolute/path/to/a/new-output-directory

The output must not exist. Replay checks the included-file manifest and explicit accepted/input digest bindings, copies evidence to the output, runs every included configured author and independent executable suite in that copy, compares regenerated reports to preserved bytes, and verifies the extracted packet remained unchanged. It writes a receipt and stdout/stderr logs in the new output.

Executable exact finite controls supplement ordinary mathematical proofs. Their PASS does not prove the whole theorem, all-order identities, limiting arguments, source applicability, or general topology. No theorem-kernel build is included. Modern paper bodies, PDFs, page images, and broad baseline trees are excluded. Source URLs, versions, inspected loci and reading limitations are retained in the authored source interface/ledger. External-source content is not newly validated offline.

The manifest binds every included file except itself. The external ZIP hash binds the manifest and all archive bytes. The external fresh-extract receipt records execution and unchanged originals; no circular self-hash is claimed.

## Exact replay counts

The configured suites are the main portable author suite (699), independent portable suite (151), two-atom supplement (30), and included complete-flow prerequisite suite (158). The preserved original-root main report has 708 checks because it additionally checks nine live predecessor files. Portable replay does not claim to repeat those live-workspace checks; the seal receipt separately records original-file immutability. The source-interface component has no separate executable suite: its direct proof/source review and final byte acceptance are retained. The separate unfinished radial investigation is outside this packet.


---

## Source 216b19c620

Original location: `T20bigupdatenext02(1).zip!/T20_Moving_Objective_Reviewed_Evidence_20261010.zip!/T20_Moving_Objective_Reviewed_Evidence_20261010/README.md`

SHA-256: `216b19c620465eff7c75c705871cf8d5ab25af35cf430808ecaa062dbfa1220e`

### Original document

# Moving-objective moment dynamics: reviewed evidence

Preserved additively on 10 October 2026 UTC. This separate packet preserves the reviewed moving-objective successor and a distinctly scoped switching note. It does not alter earlier archives, perform final integration, or claim T20 closure. The active `moment-evolution-source-comparison` literature investigation is excluded and was not awaited.

## Reviewed successor

- Proof: `evidence/time-varying-square-positivity-20261010/RESULT.md`
- Proof SHA-256: `7ffed76cdfb23ee725bd4030c22dd03bb1f66934d885a6800caf260fdb0741bd`
- Review: `evidence/time-varying-square-positivity-independent-review-20261010/REVIEW.md`
- Review SHA-256: `df593fc0a261960f59510937cd1642417797f654fb1461beed3b11c6416ad998`
- Verdict: `PASS_ORDINARY_INDEPENDENT_REVIEW` under Theorem V's exact hypotheses.

The theorem assumes a fixed finite-dimensional numerical state, its full commutative polynomial moment algebra, coordinatewise C1 boundary regularity, normalization, all polynomial-square tests, and the exact prescribed time-dependent hierarchy. On every compact time window beginning at zero, the objective has bounded polynomial degree and continuous coefficients, together with uniform constants c>0 and C>=0 for which h_t+C-c|x|² is a sum of squares at every time.

It derives an initial probability law with all polynomial moments, the integrated-objective tilt, and positive-time full-moment determinacy. It covers genuinely moving continuous coercive quadratics and appropriately certified higher-degree objectives. Pointwise coercivity alone does not replace the uniform SOS hypothesis. Continuing beyond the supplied domain requires a specified future energy family satisfying the same assumptions.

The proof uses first-derivative radial inequalities, backward integration, classical Nussbaum–Carleman existence, Gaussian bounds, Fourier/compact-test measure evolution, and boundary recovery. It does not differentiate the objective coefficients or reassert the false nonautonomous even-time-derivative positivity premise. The independent review and source note distinguish ordinary universal proof, imported classical mathematical inputs, and finite exact arithmetic controls. No downloaded primary-PDF hash or screenshot verification is added here.

## Fresh replay counts, without inflating arithmetic evidence

- Author: 23 total exact checks = 18 focused algebraic checks +5 input-integrity checks.
- Independent reviewer: 36 total exact checks = 26 focused algebraic checks +10 original/copy integrity checks.

The replay checks these partitions from the actual generated labels as well as requiring the recorded totals, exit zero, and byte-identical result JSON. These finite checks supplement the ordinary universal argument; they do not prove the representation theorem by sampling, certify a proof kernel, or implement a generic detector or general measure reconstruction.

## Separately scoped switching note and correction

`evidence/tensor-objective-switching-20261010/` retains four exact original files:

1. `RESULT.md`: current corrected note, SHA-256 `4192d9c6bd5020a34b5da8f307531effb8fd7d46a2371f836a77e14d962c9528`.
2. `RESULT.before-time-change-correction.md`: superseded pre-correction text, SHA-256 `da47c304f36047f4263af46553ecf685fc264c88ec16580c55d9794990fc863c`. It is historical evidence, not the accepted current wording.
3. `REVIEW_CORRECTION.json`: binds both versions and records the scalar-time-change correction.
4. `CONTROL_RECEIPT.json`: the original exact symbolic control record and four inherited input hashes.

The note is an elementary finite-switch corollary of the retained autonomous theorem plus a proof-route countercontrol. It is not packaged as an additional new classification theorem, an independent universal proof review, or kernel proof. The correction recognizes that scalar time reparametrizations may violate physical-time even-derivative positivity while reducing to a fixed objective in the reparametrized time. The moving-objective result supplies a different proof under its explicit SOS hypotheses; the negative-even-derivative control remains a proof-route obstruction, not a counterexample to realizability.

The fresh preservation replay verifies the note's source hashes, both version hashes, and correction linkage. Its historical arithmetic operation is not re-executed or counted in the 23/36 totals. The successor's own algebraic suites independently include the shifted moving-objective sign controls described in its proof/review.

## Minimal exact prerequisite closure

`SOURCE_BINDINGS.json` records the exact 59-file union:

- Both complete reviewed successor directories, including the original receipts and reviewer snapshot.
- Their five direct prerequisite files and every file named by the two inherited autonomous author receipts.
- The four switching-note files and their four exact source anchors.

Duplicate original frozen copies remain unchanged because the source receipts bind them. This union supports four complete receipt verifications: the successor author and reviewer receipts, plus both inherited autonomous author receipts. It includes no broad baseline, prior archive payload, active literature investigation, or unrelated working output. Inherited checker files required by those receipts are provenance evidence; only the two successor suites are run.

## Portable verification and replay

Requirements: Python 3.12 and SymPy 1.14.0. Reference execution uses Python 3.12.14. No network, Lean toolchain, new research, or dependency installation is required.

1. Extract into a new empty directory.
2. From the package root, run `python3 replay.py --verify-only`.
3. Run `python3 replay.py --output-dir /absolute/path/to/new-empty-replay-directory`.

Without `--output-dir`, a fresh temporary directory is created and reported. Output must be outside the extracted packet. Both original checkers run unmodified in a fresh evidence copy. Logs and `REPLAY_RECEIPT.json` remain in that output directory. The extracted packet is checked before and after replay and never receives generated outputs.

Expected status: `PASS_SOURCE_BOUND_FINITE_CONTROL_REPLAY`.

`INTEGRITY.json` hashes all other package files and excludes its own hash. The companion preservation receipt binds the archive, manifest, fresh replay receipt, tamper-detection controls, and before/after custody records. The fixed preexisting archive set and all copied original sources are verified unchanged. New files produced elsewhere after the custody cut are outside that frozen set.

No source changes, protected-state changes, baseline rebuild, upload, final integration, Lean/formal-kernel certification, field novelty, empirical finding, noetic realization, metaphysical conclusion, or T20 closure is claimed.


---

## Source e936e2d63f

Original location: `T20bigupdatenext03.zip!/reference-geometry-gradient-combined-delivery-20261011.zip!/reference-geometry-gradient-combined-delivery-20261011/GUIDE.md`

SHA-256: `e936e2d63fa4bb49e7cac6eeb04e05f95221dab73917f7a37fe461c84de9ca86`

### Original document

# Reference geometry and gradient descent: combined additive delivery

## Read first

This is a compact, byte-preserving, omission-aware collection. It does not integrate or adopt results, modify protected sources, or close a programme. Original manifests and historical paths are retained unchanged; this guide and the delivery verifier describe the intentional subset.

### Main scope: reference-transported Bregman classification

1. `payload/reference-bregman-classification-20261011/RESULT.md`: the attributed classical Bauschke–Borwein scalar joint-convexity criterion, with Chafaï/Jensen ancestry, transported to the actual positive-law/transported-reference contract. This is **not a novel scalar theorem**. See the written normalized-buffer necessity proof and distinct equality/recovery conditions.
2. `payload/reference-bregman-independent-review-20261011/REVIEW.md`: independent reasoning and 22 exact controls. `REVIEW_FREEZE.json` is PASS with no outstanding findings and binds the frozen author result and review manifest.
3. `payload/reference-geometry-root-controls-20261011/DERIVATION.md`: root derivation and 13 corroborating controls, with final original `MANIFEST.json` and bounded source-reading scope.

Assumptions include a common C³ generator on the positive half-line with strictly positive second derivative, positive input probability laws and reference, and nonnegative column-stochastic channels with zero output rows omitted. No canonical reference, warrant, arbitrary field projectability, or boundary extension follows.

### Related main successor: gradient descent

`payload/reference-gradient-descent-classification-20261011/RESULT.md` (SHA-256 097e12106db027914a1a05795c8d4dde647e9c73e52882562eef5f546f6d7c18) and `payload/reference-gradient-descent-review-20261011/REVIEW.md` form the final PASS-bound successor. Its original author manifest still says review pending: that historical text is retained unchanged; the later review explicitly binds the final report and records its punctuation-only rebind.

The root-state distinction is precise: concave reciprocal curvature r gives universal divergence contraction; affine r(t)=at+b, a,b>=0 and a+b>0, is required for universal same-time deterministic natural-gradient descent through partitions, with all positive references/states/objectives quantified. For r=sqrt(t), the same coarse state (1/2,1/2) has projected velocities (-4/9,4/9) and (-1/2,1/2). Thus even an autonomous coarse-only field fails. This fixture concerns same-time velocity, not every trajectory time change.

A positive remedy remains: the reference-aligned section p_i=mu_i q_j/(Kmu)_j is invariant for pulled-back objectives and gives canonical descent for any admissible r on common positive existence intervals. It is a restricted-state remedy, not universal fine-state autonomy.

For concave r and any nonnegative column-stochastic K with no zero row, the full matrix difference G_V-K G_w K^T is PSD: a weight/Jensen gap plus a channel-variance gap. With at least two outputs, all-objective matrix equality requires deterministic K and V=W. A single objective can survive despite unequal matrices. With one output the tangent fields vanish regardless of strict Jensen gaps; equality does not imply V=W. This is pointwise mobility comparison, not a later-time trajectory/rate theorem.

The old 58,181-byte checkpoint ZIP and its receipt remain unchanged outside this archive; `CHECKPOINT_ANCESTRY.json` records exact hashes/sizes. Its 29 original payload files and omission ledger are retained byte-for-byte. This combines only related additive scopes and is not an all-T20 consolidation.

### Supplemental scope A: law/sample semantics

`payload/law-sample-semantics-20261011/RESULT.md` and `EXACT_CHECK.txt` preserve an **inherited application**: exact-law correction need not be a fixed one-sample Markov channel; law injectivity does not supply a stochastic inverse or statistical sufficiency. The five-identity historical check record is included unchanged but has no executable script here and is not counted as a newly replayed suite. This scope is separate from the classification review's PASS.

### Supplemental scope B: cumulative source transmission

`payload/cumulative-source-transmission-20261011/REPORT.md`, `SOURCE_READS.json`, `INPUT_BINDINGS.json`, and `REVIEW.md` are a bounded shareable primary comparison: **NO NEW WARRANT BRIDGE**. Original manifest/checksum records are also preserved. Reading extents and inherited credit remain as recorded. This is neither a new mathematical theorem nor a general solution to bootstrapping; it does not inherit the classification review's PASS.

## Three evidence classes

- **Written mathematical reasoning and exact symbolic/rational controls:** original classification author 26, independent review 22, root 13; gradient author 28 and independent review 6 discriminator groups (not six individual assertions). Finite controls corroborate the written all-input proof; they cannot certify the global theorem. Root fixtures partly overlap author/reviewer fixtures. Normal and optimized execution are robustness replays, never extra independent evidence or extra novelty credit.
- **Approximate numerical evidence:** none newly generated or claimed in this delivery. Exact radical comparisons are symbolic, not numerical experiments.
- **Integrity/preservation:** SHA-256, sizes, review-freeze bindings, unchanged manifests, archive fresh extraction and output equality. These establish byte identity and replay behavior, not mathematical truth, source authenticity, completeness, or novelty. No formal proof-assistant certification is claimed.

## Portable replay

Requires Python 3 and SymPy (tested versions in the external replay receipt). The unchanged scripts use no network, external source files, original absolute paths, or sibling research directories. Run from the extracted delivery directory; choose a new output directory outside it:

    python -B verify_delivery.py
    python -B replay.py --output ../reference-geometry-replay

The wrapper runs these original classification commands in both modes and checks 26/22/13 counts and frozen stdout:

    python -B payload/reference-bregman-classification-20261011/verify.py
    python -B -O payload/reference-bregman-classification-20261011/verify.py
    python -B payload/reference-bregman-independent-review-20261011/check_independent.py
    python -B -O payload/reference-bregman-independent-review-20261011/check_independent.py
    python -B payload/reference-geometry-root-controls-20261011/check.py
    python -B -O payload/reference-geometry-root-controls-20261011/check.py

For direct commands, redirect stdout/stderr outside the delivery. The wrapper also runs both gradient scripts, normally and with -O:

    python -B payload/reference-gradient-descent-classification-20261011/verify.py
    python -B payload/reference-gradient-descent-review-20261011/independent_controls.py

IMPORTANT: both original gradient scripts use removable Python asserts. Their raw -O runs demonstrate execution/output compatibility only, not checked assertions. The wrapper separately repeats each through `assertion_preserving_runner.py` in both modes. This additive adapter transforms each original assert predicate into an explicit conditional AssertionError without changing original bytes. A deliberately false sentinel must fail in normal and optimized modes. Adapter runs have active checks; their outputs must match the frozen 28-control and six-group records. They add no independent mathematical credit.

    python -B -O assertion_preserving_runner.py payload/reference-gradient-descent-classification-20261011/verify.py
    python -B -O assertion_preserving_runner.py payload/reference-gradient-descent-review-20261011/independent_controls.py

The wrapper enforces an external, previously nonexistent output directory, suppresses bytecode writes, records Python/SymPy versions, and checks integrity before and after replay. Wrapper and integrity failures are explicit and survive optimization.

## Omissions and dependency limits

`OMISSION_LEDGER.json` records all 16 excluded source PDFs, PS, full-text extracts, and page images from the selected research directories, with exact local size/hash and primary-source URL. URLs for conversions/images identify the parent source, not a promise of byte-identical downloadable derivatives. The gradient successor adds no source-file acquisition; no full external source file is embedded. Reports, bounded quotations, source-reading records, and reviews remain.

`PRESERVATION_MAP.json` maps all 37 included originals to exact bytes and hashes. Their original manifests are untouched. The author manifest and review binding still name six omitted source files; the omission-aware verifier validates these entries against the ledger and reports them as acknowledged omissions, **not as rehashed source content**. A blanket original-manifest file-existence checker will fail on this intentional subset.

Inherited reports and the inherited Dar taʿāruḍ reading unit named in `SOURCE_READS.json`/`INPUT_BINDINGS.json` are historical dependencies, not included or newly revalidated. Their original locators/hashes, and the Arabic source URL, remain in the reading records. None is required by the replay scripts. This collection makes no full-paper rereading, exhaustive corpus comparison, or exhaustive novelty claim.

The adjacent external receipt gives the ZIP's exact byte size and SHA-256, fresh-extract replay results, and the full original-directory unchanged check. `DELIVERY_MANIFEST.json` covers every file in this delivery except itself; the external ZIP hash seals that manifest as well.


---

## Source 097e12106d

Original location: `T20bigupdatenext03.zip!/reference-geometry-gradient-combined-delivery-20261011.zip!/reference-geometry-gradient-combined-delivery-20261011/payload/reference-gradient-descent-classification-20261011/RESULT.md`

SHA-256: `097e12106db027914a1a05795c8d4dde647e9c73e52882562eef5f546f6d7c18`

### Original document

# Reference geometry: exact deterministic gradient descent classification

11 October 2026 UTC. Bounded mathematical continuation. Ordinary proof and exact symbolic controls, not formal-kernel certification. No protected edits, repository adoption, empirical/noetic identification, external novelty, or programme closure claimed.

## Result

For the transported-reference separable family below, universal same-time natural-gradient commutation through deterministic partitions holds exactly when reciprocal curvature is affine. Equivalently, only that class has an autonomous projected field for every objective, every reference and every deterministic partition on the unrestricted positive simplex. This is stricter than the inherited divergence-contraction condition, which permits every concave reciprocal curvature. The normalized power family contracts for 1<alpha<2 but fails even autonomous deterministic descent.

## 1. Setting and intrinsic mobility

Let phi be C³ on (0,infinity), with phi''>0, and set r=1/phi''. For a fixed positive reference vector mu, not necessarily normalized, define

    f_mu(p)=sum_i mu_i phi(p_i/mu_i),
    h_p(u,v)=sum_i u_i v_i/[mu_i r(p_i/mu_i)],
    w_i=mu_i r(p_i/mu_i), S=sum_i w_i,
    G_w=diag(w)-ww^T/S.

Here p is a strictly positive probability law, and u,v have zero total mass. This is the inverse tangent metric, not the unconstrained inverse Hessian. Indeed G_w g has zero total mass and

    diag(1/w) G_w g = g-1(w^Tg)/S,

whose pairing with any zero-mass v is g^Tv. Thus gradient descent on a pulled-back objective J(p)=Jbar(Kp) is

    pdot=-G_w K^T g, g=dJbar_(Kp).

Covectors are modulo constants; all displayed cometrics annihilate constants, so linear objectives realize all relevant tests. The reference is fixed throughout the flow, not reset to p.

Let K be a deterministic surjective partition matrix, with one 1 per input column and no empty output. Put q=Kp, nu=Kmu and

    W=Kw, V_j=nu_j r(q_j/nu_j).

Since K diag(w) K^T=diag(Kw) and sum W=sum w,

    K G_w K^T=G_W.                                    (1)

Consequently projected fine descent is -G_W g, whereas canonical coarse descent for f_nu is -G_V g.

## 2. Universal classification

The following are equivalent, with quantification over all finite dimensions, positive references and probability states, surjective deterministic partitions, and C² coarse objectives:

(A) Projected fine and canonical coarse vector fields agree in the same time parameter.
(B) Every pulled-back objective admits a projected vector field depending only on q, not the selected positive lift p in its fibre.
(C) r(t)=a t+b on (0,infinity), where a,b>=0 and a+b>0.

It suffices in (A) or (B) to test the 3-to-2 partition merging the first two coordinates and retaining the third, while allowing mu to vary. Requiring mu itself to be a probability law does not weaken the theorem.

### (C) implies (A)

If r(t)=at+b, then w=ap+bmu and W=aq+bnu=V. Equation (1) gives equality. (A) implies (B) immediately.

### (B) implies (A)

For fixed mu, K and q, the fibre has the positive reference-aligned lift

    p*_i=mu_i q_j/nu_j, i in block j.                  (2)

At that lift, all block density ratios agree and W*=V. If projected velocities are independent of the fine lift for every objective, they equal the canonical velocity witnessed at p*. This also proves the fixed-partition equivalence between all-objective autonomous descent and canonical commutation, without changing any parameters.

### (A) implies (C): binary mobility and a probability buffer

For a two-output partition, G_(x,z)=[xz/(x+z)] L, where L=[[1,-1],[-1,1]]. The unmerged singleton has W_2=V_2=z>0. Equality of cometrics thus forces

    W_1 z/(W_1+z)=V_1 z/(V_1+z), hence W_1=V_1,

because the scalar map x -> xz/(x+z) is strictly increasing on x>0.

Fix arbitrary x,y>0 and 0<lambda<1; put X=lambda x+(1-lambda)y. Choose 0<epsilon<min(1,1/X) and set

    mu=(epsilon lambda,epsilon(1-lambda),1-epsilon),
    p=(epsilon lambda x,epsilon(1-lambda)y,1-epsilon X).

Both vectors are positive probability laws. The singleton weight is unchanged and positive. Equality W_1=V_1 reduces to

    lambda r(x)+(1-lambda)r(y)=r(lambda x+(1-lambda)y).

All x,y,lambda are arbitrary. This all-weight Jensen equality makes r affine (continuity is already provided by phi in C³). Positivity on the whole positive half-line forces a>=0 and b>=0, not both zero: a<0 fails at infinity, and b<0 fails near zero. This proves the theorem.

The vector-field assertion yields equality of flows on their common interval of positive existence by local uniqueness: r is C¹ and Jbar is C². No global interior existence or boundary extension is asserted. Same-time equality matters; a scalar speed comparison is weaker.

## 3. Exact generators and inherited contraction classification

Modulo an arbitrary affine function of t, integrating phi''=1/(at+b) gives

- a=0, b>0: phi(t)=t²/(2b), the weighted quadratic family.
- a>0, b>=0: phi(t)=[(at+b) log(at+b)-(at+b)]/a².

For b=0 this is a positive multiple of t log t modulo affine terms. For a,b>0 it is shifted entropy. All these have affine, hence concave, r and belong to the inherited reference-Bregman contractive class.

For a>0 this shifted-entropy geometry also has a simple affine-blend interpretation. Put M=a+b sum_i mu_i and s_p=(ap+bmu)/M, a probability vector. Direct substitution yields

    h_p=(M/a²) (pullback of the Fisher metric under p -> s_p),
    D_mu^phi(p,q)=(M/a²) KL(s_p || s_q).

When b>0 the image is a restricted subset of the simplex with s_i>b mu_i/M. The reference blend is stipulated geometric data, not acquired evidence. In particular, equality/recovery statements for the blended laws must not be silently promoted to recovery of the original pair p,q without also controlling the reference. The earlier strictly-concave-r pairwise-recovery argument does not apply to affine r.

For normalized power generators with phi_alpha''(t)=t^(alpha-2), r(t)=t^(2-alpha). For 1<alpha<2, r is strictly concave and nonaffine. Their transported Bregman divergences contract under every stochastic K by the inherited theorem, but universal deterministic gradient descent already fails here. The endpoints alpha=1 and alpha=2 satisfy the present theorem. This does not classify arbitrary nonseparable potentials or unadorned simplex geometries.

## 4. Actual same-fibre velocity collisions

Use phi(t)=(4/3)t^(3/2), which has phi''(t)=t^(-1/2) and r(t)=sqrt(t). This differs from the affine-normalized power generator only by an affine term. Let K merge coordinates 1 and 2, retain coordinate 3, and take Jbar(q)=q_1.

### Root-supplied simple reference

    mu=(1,1,2), nu=(2,2),
    p=(1/100,49/100,1/2), p'=(1/4,1/4,1/2),
    Kp=Kp'=(1/2,1/2),
    w(p)=(1/10,7/10,1), w(p')=(1/2,1/2,1).

Thus W(p)=(4/5,1), W(p')=(1,1), and V=(1,1). Their binary mobilities are 4/9 and 1/2. The actual projected velocities at the same coarse state are

    K pdot=(-4/9,4/9), K p'dot=(-1/2,1/2).

There is no autonomous q-only vector field for this single linear objective that covers both fine states. This conclusion is independent of how one might choose a different canonical coarse metric.

### Independent probability-reference control

With exactly the same p,p',K,Jbar, use the normalized reference

    mu=(1/100,1/100,49/50), nu=(1/50,49/50).

Then w(p)=(1/100,7/100,7/10), w(p')=(1/20,1/20,7/10), and V=(1/10,7/10). The projected velocities are

    (-14/195,14/195) and (-7/80,7/80),

respectively. Hence the obstruction does not rely on nonnormalized reference mass. These two-dimensional velocities are collinear, so this fixture establishes failure of same-time autonomy, not failure of every possible trajectory time change. No such stronger assertion is needed.

## 5. A valid restricted-state remedy for every r

For any admissible phi, fix mu and K and restrict to the reference-aligned section (2). At such a state w_i=mu_i r(q_j/nu_j). Writing c=(W^Tg)/(sum W), the fine field satisfies

    pdot_i=-mu_i r(q_j/nu_j)(g_j-c), i in block j,
    qdot_j=-nu_j r(q_j/nu_j)(g_j-c).

Therefore pdot_i=(mu_i/nu_j)qdot_j, proving tangency and invariance of the section for every pulled-back objective. The projected flow is exactly the canonical coarse flow there. This is a conditional restriction with a fixed supplied within-block law, not a repair for arbitrary fine states. An arbitrary fixed section with different block proportions need not be invariant for general r.

Retaining additional state, the actual fine law, or a separately supplied model can also change the question. Pointwise quotient metrics exist at each fine point, but the collision shows they need not define one coarse geometry independent of the lift. None of these mathematical options authenticates an objective, reference, evidence source or actual noetic target.

## 6. Full stochastic comparison inside the contractive class

Here assume additionally that r is concave, exactly the inherited divergence-contractive class. Let K be any nonnegative column-stochastic matrix with no zero row. Define w as before, W=Kw and V_j=(Kmu)_j r((Kp)_j/(Kmu)_j). Rowwise Jensen gives V>=W componentwise. Unlike a deterministic partition, K diag(w) K^T need not be diagonal. The exact decomposition is

    G_V-K G_w K^T = (G_V-G_W)
                         + [diag(Kw)-K diag(w) K^T].   (3)

Both terms are positive semidefinite. For the first, set d=V-W>=0, c_W=(W^Tg)/(sum W), c_V=(V^Tg)/(sum V). Expanding weighted squares gives

    g^T(G_V-G_W)g
       =sum_j d_j(g_j-c_V)^2+(sum W)(c_V-c_W)^2.       (4)

For the second, writing k_i for column i gives

    g^T[diag(Kw)-K diag(w)K^T]g
       =sum_i w_i Var_(k_i)(g).                       (5)

These are pointwise mobility/dissipation identities at a common state, not comparisons of later equal-time trajectories.

For m>=2 outputs, equality of projected and canonical fields for every objective at the specified p,mu,K holds iff K is deterministic and W=V. To prove necessity, equality in the sum of positive semidefinite terms forces both terms zero. If d_j>0, take g=e_j. Since V is strictly positive and m>=2, 0<c_V<1 and the j term in (4) is strictly positive, a contradiction. Thus d=0. Equality of the second matrix forces deterministic columns: its trace is sum_i w_i(1-sum_j K_ji²), a sum of nonnegative terms with strictly positive weights. Sufficiency follows from (3).

If r is strictly concave, W=V for a deterministic K holds exactly when p_i/mu_i is constant on each merged block. Thus for interior powers, the reference-aligned section is exactly the state locus where every objective canonically commutes through a given deterministic partition. If r is affine, V=W for all p and every stochastic K, and (3) reduces to the inherited channel-variance theorem: all-objective commutation holds exactly for deterministic K. For a merely concave r with affine subintervals, retain the precise rowwise Jensen-equality condition rather than incorrectly requiring all densities equal.

For a single objective at the specified state, agreement is equivalent to the sum of the three nonnegative expressions in (4)–(5) being zero, equivalently each being zero. This criterion may hold even when the full matrices differ. For m=1 both tangent fields vanish automatically; one must not conclude V=W from their equality. K then is deterministic, but Jensen may be strict. No classification of a fixed noisy channel for arbitrary nonconcave r is claimed.

## 7. Ancestry, deduplication, attribution and verification

The local depth-two RESULT.md scan for affine reciprocal curvature, shifted entropy and same-fibre velocity found the inherited leafwise report's attribution of the Fisher noisy-channel collision; it found no prior report of this deterministic reciprocal-curvature classification. This is a bounded deduplication check, not a field novelty search.

- reference-bregman-classification-20261011/RESULT.md supplies the transported-reference family, exact concave-r divergence iff, normalized-buffer method, power family and Bauschke–Borwein/Chafai attribution. Its explicit separation of divergence contraction from gradient projectability is preserved.
- noetic-gradient-transport-20261009/RESULT.md §§2–5 and 8 supplies the affine-constrained inverse-Hessian formula, constant-quadratic partition/noise discriminator and pointwise quotient interpretation. Its primary ancestry is Alvarez, Bolte and Brahic, Hessian Riemannian gradient flows in convex programming, §2.2 equations (7)–(10): https://arxiv.org/pdf/1811.10331 . This packet specializes the inherited formula with w_i=mu_i r(p_i/mu_i), rather than claiming new natural-gradient machinery. No additional external source was necessary for this direct derivation; no newly checked primary reading is claimed.
- state-dependent-gradient-obstruction-20261009/RESULT.md §§2–4 supplies the all-objective fibre-constancy criterion and a Fisher collision through a noisy channel, with deterministic Fisher positive control. The present collision is different: a deterministic merge already fails for a contractive nonaffine r.
- leafwise-noetic-geometry-20261010/RESULT.md supplies conditional Fisher exponential-leaf remedies with retained reference-class information. The present section is the explicit reference-aligned partition specialization generalized by direct calculation to all admissible r. The general conditional-model principle is inherited.

The root supplied the affine iff candidate, binary-singleton/Jensen-buffer necessity strategy, the unnormalized-reference fixture, the invariant-section observation and the concave-r stochastic decomposition with its weighted-square identity, and the affine-blend interpretation. This worker independently derived them, strengthened the theorem to universal autonomous descent using the section, and supplied the normalized-reference collision. These are workflow attributions, not priority claims.

verify.py checks the symbolic tangent duality and binary injectivity, the normalized Jensen embedding, affine transport through every one of the 8 three-input binary deterministic partitions (nonempty ones for the two-output test), both radical-to-rational collisions, generator integrations, invariant-section formula, a noisy affine-r variance identity, the general weighted-square gap identity, and the affine-blend Fisher/Bregman identities. Finite controls supplement the all-input proofs. All inherited input bytes and report/control bytes are bound in INPUT_BINDINGS.json and MANIFEST.json. Boundaries remain strict positivity, finite dimensions, fixed supplied references, pulled-back objectives and common interior existence; no rate campaign or protected-source mutation was undertaken.


---

## Source 1d6209f89b

Original location: `T20bigupdatenext03.zip!/grouped-source-audit-gradient-preservation-20261011.tar.gz!/grouped-source-audit-gradient-preservation-20261011/README.md`

SHA-256: `1d6209f89b27336d40bbdc05b24dfc1f1da86d190c167596f21b8a75e2fcbb7a`

### Original document

# Fixed-group audit-gradient result and independent review

Result: PASS within the stated fixed-partition, strictly positive labelled product-domain contract.

Read `grouped-source-audit-gradient-20261011/RESULT.md` first; `grouped-audit-independent-review/independent-review.md` gives the independent proof and review. The exact classification is E=C+sum_g m_g V_g(r_g,x_g). It permits arbitrary smooth within-group nonlinearity while excluding nonseparable cross-group energy dependence under the specified metric. Group masses remain coupled by normalization. A joint interacting counterexample shows why singleton-audit rigidity cannot replace this groupwise contract.

Ownership: the block-coordinate candidate and weight-only control came from the parent; the report gives the proof and stronger joint control; the geometry, universal-singleton argument and positive numerical repair are explicitly inherited. The ancestry check is bounded to the five complete copied and hash-bound records. No broad novelty, closure, integration or formal-kernel claim is made.

Review: the independently derived proof and independently written symbolic control passed. The frozen author checker was independently replayed in normal and optimized Python, both passing 10 control groups / 102 counted controls and fixtures. These checks supplement the written universal proof.

Representation guard: origin labels are model representation choices; a provenance label alone does not establish real-world mutual exclusivity or a correct shared multiplier. Normalized weights are not automatically amounts of epistemic warrant. Shared sourcehood does not itself license a one-group audit.

Verification: `sha256sum -c SHA256SUMS` verifies every packaged file other than the checksum file itself. The author checker also checks the original source hierarchy identified in its INPUT_BINDINGS.json. Run it in the original workspace to reproduce that stronger unchanged-original check. The copied source bytes are all included in author inputs/. Without that original hierarchy, run the self-contained independent symbolic control in grouped-audit-independent-review/check_grouped_covariance.py; this requires Python and SymPy. Merely checking copied bytes does not freshly authenticate the original sources.

The author report and checker were frozen before review and are unmodified here. Review/current-source receipts are retained. No protected artifacts were changed.

