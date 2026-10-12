# Independent review: literal rational-shift probability bridge

11 October 2026 UTC. **PASS for the five bound new modules.** Independent fresh compilation with Lean 4.19.0 `--trust=0` succeeded. All 64 exported theorem signatures and axiom closures were read back from reviewer-built objects. Their closures contain only `propext`, `Classical.choice`, and `Quot.sound`, or subsets thereof. Both intended-false controls were rejected for their stated contradictions. No `sorryAx`, custom assumption, or native-reduction axiom occurs in the inspected closures.

## Exact accepted target

`P02.LiteralShift.compileShift_defect` proves, for every finite typed observer body, arbitrary designated output register, and natural `a,b` with `0<b` and `a<=b`,

`defect (fairCantor.map (compiledOutput body output a b))`

`= (a:Real)/b + (1-(a:Real)/b) * defect (fairCantor.map (output (programValue body output)))`.

The map on the left is the unchanged source-lowered literal selector/replay AST from the preceding independently checked checkpoint. The defect is the existing `P02A2.defect`, namely one minus the real-valued atomic mass. It is not total-variation distance. No hypothesis assumes the desired law, a stopping weight, boundary nullity, base diffuseness, or base atomicity. Only the displayed valid rational-parameter hypotheses remain.

The stronger `compileShift_probability_law` identifies the actual pushforward with a countable sum indexed by its actual stopping leaves. Every component retains that leaf's entire copied word. The atomic-mass theorem and exact total/below/above leaf-weight theorems are also accepted.

## Semantic checks

- **First stopping words.** A leaf contains a length, finite binary word and side, together with `FirstCut` on its fixed completion. The predicate includes positive length and absence of earlier resolution, excluding empty and invalid rows. `FirstCut_congr` proves independence from the completion's unobserved tail. First-cut uniqueness and equality of the observed word establish disjoint source cylinders, including uniqueness of the side.
- **Literal probabilities.** The finite payload map is proved bijective onto the integers below `2^N`; the actual fair-cylinder law gives its uniform distribution. The below test is equivalent to payload `< floor(a*2^N/b)`. Eventual-side unions use depths `k+1`, preserving the source's exclusion of an empty-word stop even at zero and one. Persistence joins finite classifications to the first-cut events.
- **Null boundary.** Any two unresolved prefixes at a given depth have the same payload. Consequently all indefinitely unresolved inputs lie in a single payload fibre at each positive depth, of mass `2^(-N)`. The geometric limit proves nullity without assuming selector termination or introducing another random-input model. Measurability of the events is proved. Explicit existence/uniqueness of a rational binary expansion is unnecessary and is not claimed.
- **Exact weights.** Finite floor probabilities converge to `a/b`. The measurable below/above events are disjoint and exhaust the complement of the proved null set, giving above weight `1-a/b`. The final leaf sums have total weight one and side weights `a/b` and `1-a/b`. Inclusive boundary comparisons, zero/one and unreduced representations remain covered; no coprimality condition enters.
- **Actual law.** `compiledOutput_on_leaf` uses the earlier kernel-checked copied-prefix and fresh-tail execution theorems. The inherited arbitrary-prefix `restricted_tail_law` gives unnormalised cylinder disintegration. Measurability comes from the inherited numerical-prefix observer theorem. Thus neither conditional normalisation nor an assumed alternative tagged-observer law is substituted.
- **Atomic mass.** Prefix embedding has the measurable left inverse `dropBits`, so the inherited mass-monotonicity argument proves mass preservation. A countable-index adaptation of the inherited countable-mixture proof handles the leaf index type. Its finite component measures and positive-singleton sets are the actual measures in question. Below components have zero atomic mass; above components have the base atomic mass. Therefore compiled atomic mass is exactly `(1-a/b)` times base atomic mass. The final ENNReal-to-Real calculation uses the proved unit-interval bound before subtraction.
- **Discharged premises.** General intermediate mixture lemmas accept an unresolved-null premise, but `compileShift_probability_law`, `compileShift_atomic_mass` and `compileShift_defect` discharge it with `fair_unresolved`; coefficient identities are similarly discharged with the proved stopping-weight results. The final target does not retain hidden probabilistic assumptions.

The fair-first-bit theorem and the constantly-zero base example correctly rule out dropping the prefix: at zero shift the output law differs from the base law, although their defects agree. The unit endpoint has defect one. These are consistent with the actual source compiler and with the final theorem.

## Independent evidence

`replay.py` freezes the five source copies, builds fresh objects in an isolated reviewer directory, and reads back all 64 theorem types and axiom closures. `LEAN_PATH` contains no author's new proof objects. The preceding seven literal modules are reused from this reviewer's previously verified objects, with both their source and object hashes checked. Thirty-four unchanged baseline prerequisite sources and objects are checked against the original source manifest and the author's final fresh prerequisite receipt, then copied into an isolated dependency directory. `--trust=0` checks imported modules. This review does not claim another rebuild of the earlier seven-module checkpoint or all 77 baseline modules.

The two negative files falsely assert that zero shift loses its stopping prefix, and that unit-shift defect is zero. Both reduce, using the already checked true theorems, to `False`; Lean's `decide` diagnostic explicitly rejects that proposition. Missing imports, blocked reduction and name-resolution errors were excluded. The positive first-bit and endpoint results are among the 64 queried theorems, rather than a repeated finite compiler census.

All new source pins were rechecked after replay. The author's `RESULT.md` and `SOURCE_BRIDGE.md` were read in full and accurately describe the accepted target and exclusions. Evidence is retained in `REPLAY.json`, `SOURCE_PINS.json`, source snapshots, complete logs and `BINDINGS.json`.

## Ownership and remaining boundary

The original P02 ordinary proofs already own the rational-cell partition, fresh-tail law, affine atomic-defect identity and ordinary code-construction arguments. Existing kernel work owns the operational semantics, hygiene, literal finite/pointwise refinement, fair measure and generic mass principles. This increment supplies the previously missing kernel probability/atomic-defect bridge for the literal lowered AST; it is not a new ordinary classification or probability model.

Original Python source remains pinned to `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`. Its correspondence with the typed AST is separately reviewed ordinary structural transcription. No theorem here parses Python source, certifies all host executions, establishes original variadic byte/numeric-code identity, formalizes explicit Set-event traces, or adds a uniform numeric PR compiler theorem. Grammar validity and the accepted arity/rational domain remain necessary for the Python association. No protected source edit, integration, owner acceptance or T20 closure is implied.

Acceptance applies only to the bound bytes and this scope.
