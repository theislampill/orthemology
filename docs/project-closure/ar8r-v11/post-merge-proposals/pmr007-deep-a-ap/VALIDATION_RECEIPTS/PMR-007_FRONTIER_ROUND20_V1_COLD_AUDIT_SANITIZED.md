# PMR-007 Frontier Round 20 V1 — cold audit

```text
audit relation: SAME-MODEL PROCEDURALLY DISTINCT REVIEW
frozen owner: PMR-007_FRONTIER_ROUND20_V1_FROZEN_HASHES.sha256
disposition: REPAIR_REQUIRED
external independence: NO
```

## 1. Frozen-hash custody

All five frozen V1 hashes recomputed without mismatch. The theorem proof and
primary equivalence checks are mathematically coherent at the declared finite,
static, authenticated-root, fixed-path support scope.

## 2. Blocking findings

### R20-F01 — public ancestry note leaks local absolute paths

The hash appendix was generated with `sha256sum` over local files and therefore
records `<LOCAL_ABSOLUTE_PATH>` absolute paths. The bytes are harmless inside private
custody but are ineligible for the sanitized repository proposal. A V2 source
note must bind the same hashes to repository-relative or stable artifact labels.

```text
severity: BLOCKING_SANITIZED_CUSTODY
```

### R20-F02 — incompatibility countermodel is asserted, not independently checked

The primary result hard-codes `joint_execution: false`. It does not compute
whether a compatible action subset covers all paths. Because the theorem
explicitly distinguishes support from execution, the checker must implement the
stronger execution semantics and obtain the mismatch from the model.

```text
severity: BLOCKING_EXECUTABLE_EVIDENCE
```

### R20-F03 — dynamic-rerouting and partial-registry controls are asserted

The primary result hard-codes registered success and operative failure for the
rerouting and omitted-path models. It must actually update the active path set
under the selected action and independently compare registered with operative
path families.

```text
severity: BLOCKING_EXECUTABLE_EVIDENCE
```

### R20-F04 — adaptive quantifier-order failure is asserted

The primary result checks static robustness but assigns
`commit_then_corrupt: false` without enumerating commitments and adversarial
root choices. The repaired checker must evaluate

```text
forall committed action, exists corruption of size <= f disabling it
```

and keep it separate from `forall corruption, exists surviving action`.

```text
severity: BLOCKING_EXECUTABLE_EVIDENCE
```

## 3. Nonblocking findings

### R20-N01 — dependency semantics are one of two natural readings

V1 explicitly adopts the conjunctive-integrity reading: corruption of any
required root disables an action. A redundant-multi-root action that survives
unless every root is corrupted needs a different hypergraph construction. This
is a scope boundary, not a defect.

### R20-N02 — model completeness remains external

The exact equivalence is model-relative. It cannot establish that the path
registry, root aliasing, blocker relation, or action dependencies are correct in
the operative system.

### R20-N03 — theorem-family ceiling is correctly low

The mathematical mechanism is standard transversal-number semantics. No general
mathematical novelty or historical identity is eligible.

### R20-N04 — support robustness is not causal restoration

Even repaired executable countermodels will not transform `kappa` into a T352
world-level restoration theorem. Compatibility, effectiveness, no-new-path,
target adequacy, custody, and reread remain separate.

## 4. Required repair

1. Preserve V1, the primary PASS, frozen hashes, and this audit.
2. Create a V2 source note with no local absolute paths.
3. Create a V2 model/checker that computes compatibility, rerouting,
   partial-registry, and adaptive-commitment controls from explicit structures.
4. Freeze V2 and run a distinct bitmask/temporal rereview.
5. Admit only the V2 scope if all frozen-hash and semantic checks pass.
