# Literal rational-cell shift: kernel finite-stage and pointwise refinement

11 October 2026. This is the continuation of the original literal-compiler semantic-fidelity obligation. It is not a replacement unary-tag compiler, a new rational-threshold classification, a reproof of generic hygiene, or an integration/closure claim.

## Result

The seven substantive Lean modules reconstruct the original `compile_shift` control flow in the unchanged P02-L1 `ObserverCore` grammar, including the actual sorted compressed register map from register 12, and prove its finite output and pointwise stream behavior. An eighth module supplies seven positive controls. The Python source-to-typed-AST transcription is separately inspected and documented in `SOURCE_BRIDGE.md`; it is not a kernel formalization of Python or a proof of serialized numeric-code identity.

The main theorem, `P02.LiteralShift.compileShift_correct`, universally quantifies the base body, designated output register, rational numerals, stage `n`, and numerical word `w`. Let `L=n+1`. The proved selector scans precisely the source expressions

`U_k = floor(w / 2^(L-k)) mod 2^k`

and records the first nonempty prefix for which either `b(U_k+1)<=a2^k` (below) or `a2^k<=bU_k` (above). The formal `scanChoice_some_iff` proves earliest-prefix characterization; `scanChoice_none_iff` characterizes failure to resolve over every inspected prefix.

The generated program returns `w mod 2` if unresolved, below, or at the newly completed stopping prefix. After an above stopping prefix of length `k<=n`, it returns the parity of the base body run from a fresh input store on

`stage = n+1-k-1`,

`word = 2^(n+1-k) + w mod 2^(n+1-k)`.

There is no bound on the base AST's finite size, register labels, aliasing or LOOP nesting, and no test enumeration substitutes for these universal statements. The template theorem holds for all natural numeral parameters; correspondence to accepted Python construction is restricted to its actual validation domain `b>0`, `a<=b`, arity two and finite grammar-well-formed source bodies.

## Actual inlining, not a convenient replacement

`literalInline` uses the source's exact support `{0,1,output} union stmtRegs(body)`, sorted increasingly, with map `12+idxOf(register)`. It is not `PRProgram.call`, whose full-range offset allocation is a different AST.

The inherited kernel theorem `LoopRenaming.inlineCode_correct` already proves finite-support renaming, snapshot LOOP behavior, argument freshness and reset correctness. This work reuses it. The new grouping lemma connects the actual variadic Seq-list lowering to that theorem. New support/map/freshness lemmas then establish arbitrary-caller replay correctness, including output/input aliases, high or unwritten output registers, arbitrary previous source-local values, and source LOOP bodies that overwrite their counters or bound registers.

The source's stopping bit, tail index, sentinel, argument evaluation order and final parity are retained. `finish_correct` includes the exact nested found/branch/`stop<=n` guard. The proof does not pretend to establish an explicit Set-event trace: `ObserverCore.exec` records final stores, so that stronger trace remains the previously reviewed ordinary result.

## Pointwise stream theorem

`LiteralShiftWord` proves the exact numerical prefix division and power-plus-modulo suffix equal the sentinel codes of the actual taken/dropped source word. In particular the replay word is not an independently convenient suffix encoding. The inherited `Q8Compiler.sentinel_prefix_last` lemma is reused for the current bit.

`LiteralShiftPrefix` then proves:

- Every bit before and at the first stopping prefix is copied.
- On a below first cut, the whole output stream equals the source stream.
- On an above first cut of length `k`, later output equals the base observer on the fresh dropped tail, at reset stage `n-k`.
- Every indefinitely unresolved stream is copied pointwise.
- Every input has either a first cut or remains unresolved, so the pointwise cases exhaust all streams.

These are pointwise execution theorems, not almost-everywhere shortcuts. Classical first-cut case analysis occurs in the proof, not in the finite running program. Each output computation still performs only its `n+1`-iteration source scan.

The existence/uniqueness of the non-dyadic boundary stream, dyadic eventual resolution, null boundary measure, stopping-cylinder probability weights, and affine defect law are not newly kernel-proved here. Their ordinary proofs remain inherited; the actual compiler's full pointwise refinement is now available as a kernel-checked premise for a future measure bridge.

## Endpoints and unreduced representations

Kernel theorems prove that zero copies one initial bit before running the base on the tail, while one copies every bit. Zero is not claimed to preserve the full base law or equal the base stream map. The source still carries its prefix tag.

`compileShift_scaled` proves equality for every positive scaling factor, and `compileShift_sameRatio` proves equal finite outputs for any positive denominators satisfying exact cross-multiplication equality. Neither denominator is reduced. `prefixValue_lowBits` also establishes the all-natural-word interpretation, including inputs without the conventional high sentinel.

## Evidence and verification boundary

Final author replay is recorded in `FINAL_REPLAY.json`, with its isolated source/object/log directory. It compiles all eight modules under Lean 4.19.0 `--trust=0`, queries all exported theorem types and axiom closures, and checks four deliberately false statements fail for a contradiction. The independent review and its own fresh replay are preserved separately when bound.

The author prerequisites are nine unchanged modules rebuilt under `--trust=0`; `PREREQUISITE_REBUILD.json` binds their sources and fresh objects. `BASELINE_SOURCE_CHECK.json` compares all 77 retained baseline source hashes, but does not mislabel that hash check as a fresh rebuild of all 77 modules. `COVERAGE_SCAN.json` records the retained 129-Lean-file inventory/search and the absence of a literal rational-cell compiler owner. The previous alternative rational compiler expressly excluded Python `compile_shift`.

The official Lean 4.19.0 toolchain and exact Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` were restored separately. All eight dependency pins match the retained manifests, and all 6,641 official cache artifacts were restored successfully. This is dependency setup, not mathematical research evidence. Acquisition records and the environment script identify the installed tools.

The seven positive controls cover stopping-bit preservation, both endpoints, first suffix stage zero, exact suffix sentinel, and an unresolved `1/3` prefix. Four false opposites test early base execution, off-by-one tail stage, missing sentinel and premature unresolved branching. Direct `decide` cannot reduce the sorted inline block in the two tail controls; those controls deliberately use the universally proved refinement to reduce the execution, then check the resulting arithmetic. The negative cases reject `0=1` or `1=0`, rather than counting an elaboration/reduction/import failure as evidence. They are small logical controls, not another compiler census and not the universal proof.

Only the standard Lean axiom closure is permitted (`propext`, `Classical.choice`, `Quot.sound`). No `sorry`, `admit`, `native_decide`, custom axiom or new assumption declaration is permitted in the new proof modules. Build and review records establish the observed result; this document alone does not certify a build.

## Scope retained

The original Python source is unchanged at SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`. Earlier ordinary universal source correspondence, PR code construction, and probability/classification arguments remain credited. This increment is new kernel coverage of the lowered literal selector/replay and pointwise execution, rather than first ordinary correctness.

No host-resource completeness, Python-interpreter kernel verification, original variadic-byte numeric identity, explicit Set-event kernel theorem, new uniform numeric PR code-transformer theorem, kernel measure/defect theorem, repository adoption, owner acceptance, or T20 closure is claimed.
