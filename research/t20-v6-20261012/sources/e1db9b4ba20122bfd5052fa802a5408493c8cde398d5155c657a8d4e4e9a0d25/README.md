# Independent hidden-parity target-pruning review

The source-bound report is `REPORT.md`. The immutable author candidate is copied unchanged under `candidate-v1`; the reviewer's two additional Lean control/assembly modules are under `src`. The prior fourth-tranche stochastic criterion is copied only for scope comparison.

The accepted result is exact finite target construction, including a verified executable exhaustive reference and a normalized rational-kernel adapter. Hard-menu/support recursion, the stochastic policy-existence iff and polynomial SCC/MEC implementation remain separate.

## Replay

Provide the already installed, exactly pinned official environment. From this extracted packet:

    python checks/verify_packet.py
    PYTHONDONTWRITEBYTECODE=1 python checks/replay_review.py --env /path/to/restored/environment --out /fresh/absent/output

The environment layout is `toolchain/lean-4.19.0-linux/bin` plus `mathlib4`. The output must be outside this immutable packet. This cold-compiles all eight author modules and both reviewer modules, checks types/axioms, reruns the 4,096 generic and 512 normalized comparisons, and replays independent and author mutation controls. It does not install software. Allow several minutes for the exhaustive reference evaluations.

Native finite executions are tests; the exact refinements and ordinary `decide` propositions are kernel proofs. The official installed object cache is trusted. No old missing proof or audit is reconstructed, and no canonical source is changed.
