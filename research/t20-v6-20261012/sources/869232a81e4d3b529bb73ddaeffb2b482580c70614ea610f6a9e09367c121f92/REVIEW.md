# Independent review: literal rational-cell compiler kernel refinement

11 October 2026 UTC. **PASS for the bound seven-module implementation refinement.** All seven new modules were independently compiled into fresh reviewer-owned objects with Lean 4.19.0 `--trust=0`. Their 66 exported theorem closures contain only `propext`, `Classical.choice`, and `Quot.sound`, or subsets thereof. Seven positive controls also passed; four deliberately false assertions were rejected for their intended propositions. There is no `sorryAx`, new custom axiom, or native-reduction axiom in the inspected closures.

Acceptance is for the reconstructed, source-faithful typed AST in the unchanged `ObserverCore` semantics. Its association with the original Python implementation is independently reviewed ordinary structural correspondence, not a kernel theorem about Python execution or original serialized bytes. Exact pins are in `SOURCE_PINS.json` and `BINDINGS.json`.

## Results independently checked

`compileShift_correct` in `LiteralShiftCorrect.lean` identifies the actual lowered compiler's final output with its finite stopping/replay specification for every finite typed observer body, arbitrary output register, and every natural `a,b,n,w`. The accompanying theorems distinguish unresolved, below, stopping-observation, and strictly-after-above cases. No genuine-sentinel assumption restricts the numerical-word theorem.

The Python entry point's accepted domain remains arity two, a grammar-well-formed finite body, and natural parameters `b>0`, `a<=b`. The typed template is defined outside that domain, but no claim is made that Python accepts those extra cases. `Program.__post_init__` alone does not establish body well-formedness.

The source transcription preserves the following details of the original `prcodec.py`, SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`:

- Registers 3–11 have their original roles; the register support includes inputs, output, all reads/writes and loop counters. Ascending finite support is mapped by `12 + idxOf`, retaining Python's sorted compressed allocation. The different offset/full-register-range `PRProgram.call` construction is not substituted.
- Variadic `Seq` nodes use the inherited decoder's `sequenceList` lowering. `literalInline_exec_eq` proves the executional grouping needed to reuse the existing finite-support `inlineCode_correct`; that inherited general renaming theorem is not claimed as new.
- Every mapped source register is reset, then the two arguments are installed in order. Freshness is proved for actual argument registers 9 and 10. `literalInline_correct` handles arbitrary caller-local contents and arbitrary source output aliases, with no assumption that a loop body preserves its counter.
- The source scan's assignment order, truncated arithmetic, below-first inclusive comparisons and one-based stop length are preserved. `selectedStore_agrees`, `scanChoice_none_iff` and `scanChoice_some_iff` establish the selector result and first-resolution characterizations universally.
- The stopping bit is copied before replay. The guard `stop<=n` requires a nonempty post-stop suffix. Replay reconstructs `2^(n+1-stop) + w % 2^(n+1-stop)` and resets the base index to `n+1-stop-1` before applying output parity.

`LiteralShiftEndpoints` proves the low-observed-bit interpretation, zero's copied initial bit/fresh-tail behavior, one's identity-bit behavior, disjoint cell tests at positive denominator, positive scaling and arbitrary equal-ratio output equivalence. Those are unbounded semantic equalities, not equal resource-failure behavior.

`LiteralShiftWord` connects the source's actual division/power/modulo expressions to list prefixes and re-sentineled dropped tails, including out-of-range drops and the empty suffix. `LiteralShiftPrefix` then proves the full pointwise copied-prefix/fresh-tail splice for each first cut, a first-cut-or-unresolved dichotomy for every stream, and pointwise copying for every indefinitely unresolved stream. Thus its all-stream statement does not assume selector termination or discard an exceptional input before defining its output.

## What the kernel increment does not establish

- The source bridge does not parse the Python source or prove a Python-language simulation. It is explicit structural inspection against the pinned original source. Reserializing the lowered binary Seq tree can change sequence tags, so original byte/numeric-code identity is not claimed.
- These modules do not identify the unique non-dyadic boundary stream, prove dyadic resolution or boundary nullity, or establish a measure/pushforward/affine-defect theorem for this selector. Those mathematical connections remain inherited ordinary results. The existing alternate unary-tag formal shift is not silently transferred here.
- `ObserverCore.exec` records stores, not explicit Set traces. The earlier exact-Set-trace argument remains ordinary mathematical assurance.
- No new uniform numeric primitive-recursive compiler theorem, Python host-resource completeness, repository adoption, or T20 closure follows. Earlier ordinary universal correspondence and PR construction were already present in the original codec-correspondence document; this result adds kernel coverage of the literal rational-cell execution and pointwise splice, rather than first ordinary-proof credit.

Default Python meter/storage caps and recursive construction/parsing still permit resource failure. The theorem concerns mathematical unbounded natural-number semantics, and normal host returns agree under the reviewed correspondence; exceptions are not semantic zero.

## Independent replay and controls

The reviewer copied all seven frozen sources and built fresh objects in dependency order, with the reviewer build first in `LEAN_PATH`. Only nine unchanged prerequisite objects were reused: each was independently checked against the author's fresh rebuild receipt, each prerequisite source against the original baseline manifest, and each object copied into an isolated reviewer-owned prerequisite directory. No author's new theorem object was used as fallback. `--trust=0` type-checks imported modules. All 77 retained baseline source hashes were separately rechecked; this is not a claim to have freshly rebuilt all 77.

`InspectTypes.lean` reads back all 66 compiled theorem signatures. `InspectAxioms.lean` queries every one of their axiom closures; `InspectControlAxioms.lean` queries the seven control theorems. The complete outputs are retained. All frozen substantive source hashes were rechecked after compilation. The author's bound `RESULT.md` and `SOURCE_BRIDGE.md` were read in full and accurately state the demonstrated scope and remaining exclusions.

The independently replayed controls cover both stopping bits, zero/one endpoints, fresh-tail stage zero, tail sentinel, and an unresolved `1/3` prefix. The four negative files assert wrong early-base, index, sentinel and unresolved outputs. Each failed with an explicit `decide` false-proposition diagnostic, not a missing import, blocked reduction or failed typeclass search. Tail controls use the universal execution theorem to normalize the actual AST; they are corroborating false-assertion controls, not independent source mutations or another universal proof. They use no `native_decide`.

Evidence: `REPLAY.json`, `CONTROLS.json`, `BASELINE_SOURCE_CHECK.json`, retained source snapshots, axiom/compilation/control logs, and replay scripts. No original compiler or inherited proof source was edited by the reviewer. Acceptance applies only to the bound bytes and stated scope.
