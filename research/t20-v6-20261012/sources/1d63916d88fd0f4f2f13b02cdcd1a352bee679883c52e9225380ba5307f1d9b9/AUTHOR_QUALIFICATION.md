# Author qualification: SCC-based MEC and parity target selector

Status: **AUTHOR_KERNEL_AND_FINITE_TEST_PASS; independent review pending.** The author of these three new modules is not the independent reviewer of this successor. Its eight imported predecessor modules remain byte-identical to the separately accepted target-pruning packet.

## Exact identities

- Main source manifest: 8882aa1df569286d6ddd8fa9ee81608f9820216c7986e79128c4e081e348ef89
- Mutation source manifest: 238adaa6209b3e05dfddfb3cf35b9f2e3c6b954760212ee86ce9ab805899f3df
- SCCPruning.lean: 0fb9bc5ce1b5e4dd1b3201cbbd90240a3893568e49322091f4ed60ec81b4b4f8
- SCCParity.lean: 38b0e0f11834330a0246ce64fc4e0e1b66d91a418cb1d10de4c823ffe4b0ef88
- SCCControls.lean: 14e80896ab46859b8c4ecde2e891123a74315c5f140db1d03b8a9316a8762bc9

The eleven-source cold replay passes with 209 exact type/axiom readbacks and no warnings. Its receipt is d8f934b556e11c3608bf12258ee1ef92d9ebfc0c8ae4a9aa9b87781775ba096d. Only propext, Classical.choice and Quot.sound are permitted foundational dependencies; the executable definitions also report standard axioms, so no axiom-free claim is made. No custom axioms, proof holes, unsafe declarations or native_decide shortcuts are accepted.

The source-hash-verified fresh objects pass 4,096 generic parity comparisons, 512 normalized rational target comparisons and 4,096 exhaustive three-state graph/restriction MEC comparisons. The finite-comparison receipt is c8a64d559ef2c8050018b8394c1e8c978af29aa4cbd9dd3667afe5e0e2dc008c. Twenty new concrete Lean controls are included in the cold build.

Six separately frozen false-proposition mutants are rejected by ordinary kernel decide, with no syntax-error substitute: stopping after one cleanup, freezing the reverse graph, accepting empty successors, replacing all-successor closure by one-successor closure, checking forward rather than reverse paths, and returning singleton pair sets instead of maximal components. Receipt: 3df7338ee039d7ea59caa93761e4640bf06cf2d01ee494a9903ef10351b77bba.

## What has been proved

The new SCC selector equals the exhaustive selector for every finite graph input, with preservation, stabilization, restricted-path connectivity and maximality derived. The replacement is propagated through every parity step/iterate/output and the normalized full-row target interface. The public proof statements and ordinary argument are in the frozen source and ORDINARY_PROOF.md.

The operation-count claim in COST_ACCOUNT.md is ordinary, under explicit finite-table/computable-accessor assumptions. It is separate from semantic kernel correctness. No formal machine/bit-cost semantics, optimized SCC implementation, outer support recursion, stochastic winning iff, policy synthesis or historical novelty is asserted.

## Replay commands

Use the pinned restored environment, with no installation:

    python candidate/tooling/replay_lean.py --root candidate --lean-bin /env/toolchain/lean-4.19.0-linux/bin --mathlib /env/mathlib4 --out /fresh/cold --suites scc_parity_pruning --no-reuse
    python candidate/tooling/replay_oracles.py --root candidate --baseline /fresh/cold --lean-bin /env/toolchain/lean-4.19.0-linux/bin --mathlib /env/mathlib4 --out /fresh/oracles
    PYTHONDONTWRITEBYTECODE=1 python mutations/tooling/replay_mutations.py --packet candidate --baseline /fresh/cold --lean-bin /env/toolchain/lean-4.19.0-linux/bin --mathlib /env/mathlib4 --out /fresh/mutations

The author bundle has the relative directories shown above. Each output must be absent and outside the immutable source packets. All custom objects are rebuilt; the pinned installed official dependency cache is explicitly trusted.
