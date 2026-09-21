# Pinned standalone formal project — NOT yet compiled

Lean `leanprover/lean4:v4.19.0`.
Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` (actual v4.19.0 tag).
The complete transitive revision graph is in lake-manifest.json, assembled from
the retrieved upstream manifest, not falsely reported as produced by Lake here.

The twelve inherited modules are byte-identical to v4. None is newly labelled
elaboration-correct. `CrossCheck.lean` additionally applies the actual pinned
`Counterexamples.Girard` API; it adds no foundational assumption. `Verification`
is a default build root and imports all required modules. Its commands check
all 145 inherited declarations plus that one independent upstream cross-check.

After installing the pinned official Lean toolchain in an environment with
network/dependency access:

    # Run from the v5 packet root; evidence stays outside the frozen packet.
    python3 -B formal_project/build.py --output ../formal-build-evidence

The driver copies the exact project bytes to a fresh external build tree.
Lake caches and generated metadata therefore never mutate the frozen packet.
A reused build directory is refused. Equivalent underlying commands, run in
that staged tree, are:

    lean --version
    lake build
    lake env lean -o ../formal-build-evidence/Verification.olean Verification.lean

The Python driver is the acceptance entrypoint: it checks exact compiler and
Mathlib and transitive dependency identities, complete build artifacts, the mandatory declaration list,
actual declaration types and their transitive axiom output. Every audited target
executes the in-Lean `#ortho_audit` command. Missing tools return 2; any build,
version, coverage, timeout or axiom error returns 1; only actual full acceptance
returns 0. A cached `lake build` alone does not replace the fresh audit invocation.

The approved ceiling is propext, Classical.choice, Quot.sound. The actual
footprint is UNKNOWN until a real successful audit. No `sorryAx`, custom
foundational axiom, or native-evaluation proof dependency is approved.

## Public-role map (original names retained)
- checkerSound: OrthemologyV3.checked_sound and OrthemologyV4.checker_sound
- exec_implies_checked: OrthemologyV4.execution_implies_checked
- revision stability: OrthemologyV4.revision_stability
- parametric reach: OrthemologyV4.parametric_reach
- SCUU/Girard negative: OrthemologyV4.not_SCUUAt
- positive OWOU: OrthemologyV4.positive_OWOU
- combined witness: OrthemologyV4.mainWitnessAt

Read their actual types in the generated audit; role labels do not strengthen
the statements. The positive witness concerns the declared Plan/API fragment,
not the full bounded mutable Python runtime. The probability chain and hierarchy
proofs in ../mathematics are ordinary mathematics, not part of this audit.

This project is deterministic source preparation. Its Lake configuration is also
uncompiled in the current environment; any actual compatibility error remains
for a real build to diagnose. No fake compiler or forged transcript is included.
