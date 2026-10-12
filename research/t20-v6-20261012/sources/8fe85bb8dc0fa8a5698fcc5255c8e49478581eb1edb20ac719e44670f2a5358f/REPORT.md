# Independent uniform computability review

## Verdict

**PASS: unconditional computability of the unchanged actual numeric evaluator.** The existing `evaluateIndex_computable_of_fuel` premise is now discharged. The final external endpoint is exactly:

```lean
Computable (fun code : ℕ =>
  P02.Codec.evaluateIndex code.unpair.1
    code.unpair.2.unpair.1 code.unpair.2.unpair.2)
```

The fully explicit readback shows standard `Denumerable.nat` representations for both domain and codomain, with no decoder, well-formedness, generated-program, or termination hypothesis. The companion triple-input theorem names the same existing evaluator. No semantic substitution or open premise was found.

## Frozen subject and independent execution

The author seal is `UNIFORM_COMPUTABILITY_SEAL.json`, SHA256 `fc5d7ca371c809b6a33063dfd080e0935e3e45405555687162504ed655e8ba17`. Its 119-target receipt is SHA256 `a1a4e7be49c31d703543db5e1252a04cac74ca8eddc544146761bb95de67deea`. The 35-source closure is SHA256 `d086854f1bd8bdfb6520f15a299ce304904fb571f9b4d91e7ec99c3ed5931193`.

The reviewer copied the complete frozen closure and independently rebuilt 39 custom modules: those 35 dependencies, the author audit, the unchanged prior operational controls, and the two new independent control modules. No author or other custom `.olean` was accepted as a build input. The executable was Lean 4.19.0, commit `6caaee842e94`; only the official Mathlib cache pinned at `c44e0c8ee63ca166450922a373c7409c5d26b00b` and its eight exact clean dependency checkouts were reused. Binary and output hashes, exact commands, import closure, and logs are recorded.

Independent receipt: `receipts/20260930T171157Z/RESULT.json`, SHA256 `0bebc6554e09a280a1a9c919158d9d1b3a067591c89ba32d14b5d1db3eda48d2`.

All 262 public Uniform/control declarations had full explicit types and axiom sets read back, including all 119 author theorem targets. Every footprint is contained in `{propext, Classical.choice, Quot.sound}`. The author target identities and axiom sets match exactly. All sealed files, all 35 source bindings, the author audit source, and every shared source from the earlier operational independent review match. No source or seal drift occurred during rebuilding. See `SOURCE_BINDING_RESULT.json` and `FullTypesAxioms.log`.

## Semantic challenges resolved

- Expr, Stmt, Task, and PackedProgram use explicit encode/decode maps with both inverse laws. These are internal mathematical representations; they do not replace the external program bytes or numeric sentinel codec
- Varint effectivity reaches the actual `uvRead`, including byte-range rejection, truncation, canonical re-encoding, and the exact unread suffix. The accumulator invariant is used where required and is proved for the real initial state
- `readExpr_primrec` and `readStmt_primrec` quantify over every natural fuel and every natural-number list. Their results include the exact suffix, failures, and syntax. No generated-code or byte-validity assumption is hidden
- Finite tables contain every suffix of the original input. The success-suffix theorem justifies all recursive lookups, including sequential siblings and arbitrary variadic child counts. The original shared predecessor-fuel semantics is preserved
- `stepByCode_eq_step` identifies the effective coding-based transition with the unchanged finite-register machine. Exact `step`, arbitrary-stack `runFuel`, and the actual decoded `evaluateIndexFuel` are primitive recursive
- The final proof composes the actual `decodeNumeric`, magic/version, arity/output, statement parser, trailing-byte rejection, and finite stack evaluator. Existing soundness, total completion, monotonicity, and terminating fuel search yield `Computable` for the original evaluator

## Independent controls

The independent files contain 43 substantive successful kernel controls plus three proof helpers: 32 malformed/parser/decoder controls and 11 endpoint/representation controls. They cover truncated and overlong varints, nonbytes, malformed literals/counts, unknown tags for arbitrary fuel and tails, exact arbitrary suffixes, insufficient depth, shared child fuel, empty/singleton/three-child variadic sequences, count/payload mismatch, wrong magic, trailing rejection, zero sentinel, wrong arity, and actual numeric decoding/evaluation of valid singleton-Seq syntax outside the serializer's canonical image.

Additional checks independently instantiate the exact old effectivity premise and external Nat-to-Nat theorem. A counterexample proves that unrelated equal-length input lists cannot replace the suffix hypothesis in table lookup. Another control distinguishes internal PackedProgram numbering from the actual external byte index.

All five expected-failure controls failed for the intended reason: treating Computable as Primrec, removing the suffix hypothesis, ignoring parser fuel, accepting an overlong varint, and ignoring trailing bytes. These are qualification/type controls; the first is not a separate proof of a diagonal non-Primrec theorem.

## Scope limits

This award is for the unchanged bit-valued numeric observer evaluator and its exact decoding/execution chain. It does **not** assert that unbounded universal evaluation is uniformly primitive recursive. Uniform primitive recursiveness of expression evaluation and bounded stack execution does not make the unbounded fuel search primitive recursive.

Transition fuel is not Python `Meter.steps`, bit complexity, memory, or wall time. Exhausted fuel remains `none`; invalid syntax or wrong arity keeps the specified semantic zero. Python resource exceptions, a uniform membership-matrix certificate, full hierarchy classification, historical novelty, and canonical adoption are outside this award. Later Membership* work requires a separate frozen review. Earlier prose describing the evaluator gap as open remains historical evidence; this seal specifically closes that gap.
