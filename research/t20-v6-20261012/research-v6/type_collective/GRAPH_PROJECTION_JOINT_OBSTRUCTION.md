# Internal graph: construction, projection boundaries, and later joint obstruction

The fully read InternalGraph (SHA 74ef636570ba73c227daf40d913bdba5a9c40bb83b87579f1b902f1f6a2db25e, 366 lines) constructs an old-Has graph type with independent state and scalar coordinates related by identity. Its nested-Sigma pack, lifted step, seed and Church-instantiated run are genuinely typed, with an included HasE iterated invariant. Based J supplies congruence and transitivity at the formed two-coordinate motives. This is positive source evidence, not a merely semantic graph.

ProjectionBoundary (99209853e5882ee3ce54d86c32cd0f33efcc43e66ef7dca934788ca5ecfd8469, 174 lines) forms two exact HasE bridge targets in scalarContext = [A, End, N]:
- stateTransport equates fst(graphRun n f a) with stateRun n at the state carrier S;
- scalarTransport equates fst(snd(graphRun n f a)) with n f a at A.

It proves both seed and single-step projection equations by raw conversion and supplies the exact retained compiler computation. The lifted iteration projection equations nevertheless fail PolyConvPlus. The two countervaluations use badN = K(K I) and badScalarN = K(K K) and are explicitly untyped. Their consequences are raw-conversion obstructions only. They do not establish either bridge's individual HasE noninhabitation.

GraphBridgeAssembly (0dd6090f8cde9debb2bb58b921bac52c9bd6dd058cece3d2b09fc8f501d1b8e3, 200 lines) accepts arbitrary HasE witnesses for both exact bridges, uses J to move the invariant through the state and scalar observations, and returns the unchanged literal HasE [] c3 (W originalQ). Its intermediate canonical-I witness still depends on the supplied identities; conversion is applied after typed J, not inverted from a raw normal form.

The later fully read OriginalWNoninhabitation sound Henkin theorem excludes that exact output. Consequently the two bridge judgements cannot both be inhabited. GraphBridgeNegative.lean proves:

    ¬ ∃ s x,
      HasE scalarContext s stateTransport ∧
      HasE scalarContext x scalarTransport

This is a new external join of exact existing results. It does not select which bridge fails, assert internal negation evidence, or settle a HasJ counterpart.

Fresh kernel evidence: all 103 original dependencies were built from exact source bytes in fresh_lean/naturality_union with pinned Lean 4.19 and --trust=0, no historical research oleans. GraphBridgeNegative.lean then compiled with exit 0. Source hashes, command, compiler hash and log are in GRAPH_BRIDGE_COMPILATION.json; full dependency receipt is FRESH_COMPILATION.json in that directory.
