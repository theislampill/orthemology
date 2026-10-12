# Independent conditional-assembly review

10 October 2026. Verdict: **PASS, within the stated conditional scope.**

The frozen theorem accepts arbitrary actual `HasE scalarContext p stateTransport` and `HasE scalarContext q scalarTransport` derivations and concludes exactly `HasE [] c3 (W originalQ)`. Neither bridge is inhabited here. The unconditional target remains open; this is neither a completeness theorem nor a classification of all possible proofs.

## Source review

- Context is exactly `[A, End, N]`, with indices 0, 1, 2 denoting a, f, n. The endpoint and formation judgements used to construct motives are existing original `Has`/`Ctx` derivations. The identity evidence itself is arbitrary `HasE`; it is never coerced back to `Has`.
- `theta Γ U x` introduces the endpoint at index 1 and its identity proof at index 0. Each new motive shifts the old ambient polynomials by two. Congruence varies the observer's state, composition varies the right endpoint, and left replacement varies the left endpoint. Each has separately proved motive formation, base instance, target instance, and endpoint typing. The proof-coordinate-independent motives are legitimate finite syntax, not semantic families.
- The frozen graph invariant supplies `Id_A(x,h(s))`; state-bridge congruence and composition give `Id_A(x,h(t))`. The existing original scalar computation is correctly reversed to identify h(t) with `(originalQ n) f a`. Composition then left-endpoint replacement along the scalar bridge produces the literal leaf.
- The initially assembled witness is only shown to convert to the graph proof. The separate reset starts from typed reflexivity at scalarL and eliminates the already typed leaf identity using actual `HasE.j`. Its witness `jPoly I scalarR leafEvidence` converts to I by the unchanged combinatory J conversion. `HasE.conv` also supplies identity formation and I scope. This does not infer typing from a raw conversion alone.
- The introduction sequence abstracts a, then f, introduces the type quantifier, then abstracts n. `twkTel [N] = [N]` is definitionally checked. Three term abstractions produce exactly imported c3; the polymorphic step adds no term binder. A new independent control spells out both projection premises and the entire target with the literal `redundantExpr.closed` compiler and triple-abstracted I, and applies the theorem directly.

## Replay and dependencies

Rehashed the pinned prerequisite receipt, all 89 existing verified prerequisite objects, all 83 pinned source modules, predecessor manifests/files, prior full-PER and graph review records, graph manifest/files, scalar-frontier source bindings, and Lean executable. Freshly compiled copied `GraphBridgeAssembly.lean`, copied `AssemblyControls.lean`, and reviewer-written `IndependentControls.lean`, each with Lean 4.19.0 `--trust=0`. The review object directory replaces the author object directory at the head of LEAN_PATH, so controls consume the fresh theorem object.

All three final replays exited zero. Author controls reran seven positive source-dependency traversals and six required-rule/frozen-dependency checks. Those traversals exclude the named semantic soundness, fundamental, standardness, graph-parametricity, F/G and full-PER target-validation dependencies. Full-PER Application is imported for the literal originalQ definition; importing it does not make its semantic theorems dependencies of this source proof. All reported theorem axioms are confined to `propext`, `Classical.choice`, and `Quot.sound`. No new axiom, admitted proof, completeness assumption, or parametricity premise appears in the reviewed sources.

This reuses the inherited compiler/third-party-library trust base and verified prerequisites; it does not repeat the 83-module rebuild or prove Lean bootstrap correctness. Source pin: `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. All author-package files were hashed before and after replay and remained unchanged. Writes are confined to this separate review directory (plus a temporary reference copy).

## Reproduce

Run `python hase-graph-bridge-assembly-review-20261010/replay.py` from the workspace. The script verifies frozen inputs, copies source without modification, writes only review outputs, and rebuilds three review objects. `REVIEW_RECEIPT.json` records final commands' log/source/object bindings. This review provides bounded independent technical evidence, not programme closure or owner acceptance.
