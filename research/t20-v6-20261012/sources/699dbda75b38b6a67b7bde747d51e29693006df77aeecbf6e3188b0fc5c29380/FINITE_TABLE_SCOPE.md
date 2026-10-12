# Actual finite rational output-cylinder table

The three new modules FiniteOutputTable, FixedIndexPrimrec and FiniteTableWitnesses are qualified at the exact Lean/Mathlib pins. All 12 named theorem targets compile and have only approved standard axiom footprints. The baseline passes; two false controls normalize to False and are rejected. Receipt: receipts/finite-table-20260930T163652Z/FINITE_TABLE_RESULT.json, SHA-256 6ffbca92ec1ef3fdf4fdca376e057be87a450c5d84480f1a07918682ecbdcf97.

The main source-level computation is P02A2.FiniteOutputTable.indexTable e N w : nonnegative rational. It enumerates every N-bit source word, executes the actual numeric evaluator at each stage using that stage's own available prefix, and counts output words equal to w. Its value is count divided by 2^N. No measure, infimum, supremum, atomic-support set or oracle is evaluated by the table.

indexTable_exact proves the ENNReal cast of that exact rational equals the actual fair-Cantor pushforward mass of AtomicMembership.cylinder N w under ObserverCore.output (P02.Codec.evaluateIndex e). The proof uses actual prefix causality, measurable output coordinates, disjoint input cylinders, and their exact 2^-N probabilities.

FixedIndexPrimrec.evaluateIndex_fixed_primrec, in namespace P02.Codec, proves each fixed numeric code has a primitive-recursive binary prefix evaluator, including malformed/nonbinary codes' specified zero fallback. This is pointwise in the code, not a uniform PR evaluator.

The positive controls give all four two-bit identity probabilities as 1/4, the constant-zero atom as 1, a forbidden true output as zero, and the first-input-then-zero output true,false as 1/2. The negative controls assert a wrong dyadic weight or incorrectly use the complete word too early; both reduce to false rational equalities. Initial decide-based control runs are retained but not counted as successful controls because kernel reduction stalled in rational representation. The final controls use exact rational normalization.

The dependency closure binds the frozen HeavyCylinders source SHA-256 894e4f5b5d9e32ac9b40a0058dd420b6089156a83b4d79ada2c47c3771637d4f, plus the already sealed concrete codec and measure sources. The root's rational heavy-sum normal-form instantiation is a separate result.

TOTAL_COMPUTABILITY_ARGUMENT.md gives the ordinary source-driven total-algorithm argument. It is explicitly distinct from a formal Mathlib Computable theorem for the full uniform decoder/evaluator/table, which this seal does not claim. The complete formal hierarchy classification and full Python host-runtime refinement are not implied. Original sources and previous seals remain unchanged.
