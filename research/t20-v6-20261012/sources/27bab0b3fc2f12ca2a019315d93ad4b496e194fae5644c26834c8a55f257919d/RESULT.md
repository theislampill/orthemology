# Checked conditional assembly from the two graph projections

10 October 2026. **The original literal `HasE [] c3 (W originalQ)` remains OPEN without premises.** This package closes the previously unformalized conditional assembly obligation. It supplies neither missing projection bridge.

## Exact result

In the unchanged `scalarContext = [A, End, N]`, using the frozen definitions `stateTransport` and `scalarTransport`, the checked theorem is:

```lean
scalar_fusion_from_bridges :
  ∀ {stateEvidence scalarEvidence : Poly},
  HasE scalarContext stateEvidence stateTransport →
  HasE scalarContext scalarEvidence scalarTransport →
  HasE [] ExactScalarFusion.c3 (ExactScalarFusion.W FullPER.Application.originalQ)
```

Both proof hypotheses are genuinely **HasE**, allowing arbitrary derivations in the current grammar, including extensionality. They are not silently replaced with original Has hypotheses. No inhabitant is declared, assumed globally, or postulated. `originalQ` is the existing `redundantExpr.closed`; `W`, `Leaf`, and `c3` are imported from the unchanged ScalarFusionCore.

Two intermediate results also have actual source typing conclusions:

- `scalar_leaf_from_bridges`: the explicitly assembled polynomial inhabits the literal `Leaf originalQ` in scalarContext.
- `scalar_leaf_i_from_bridges`: the exact I polynomial inhabits that same literal leaf.

## Construction and the necessary normalization step

Let r be the frozen graph run; let x = fst(snd r), s = fst r, t = n Delta z0, and h(v) = snd(v) f a. The frozen invariant gives `Id_A(x,h(s))`.

1. `image_congr_hasE` applies actual `HasE.j` to the state bridge `Id_S(s,t)`, producing `Id_A(h(s),h(t))`.
2. `trans_hasE` composes that with the frozen invariant to obtain `Id_A(x,h(t))`.
3. The frozen `original_scalar_computation`, oriented backwards, supplies the source identity `Id_A(h(t),(originalQ n) f a)` by original identity introduction and inclusion.
4. A second composition yields `Id_A(x,(originalQ n) f a)`.
5. `replace_left_hasE` transports its first endpoint along the scalar bridge `Id_A(x,n f a)`. This gives the literal scalar leaf.

All three new identity helpers explicitly form their two-coordinate theta motives, their base and target instances, and their endpoint typings. The data endpoints and ambient contexts have the original Has/Ctx derivations, which suffice for forming these motives before inclusion. The supplied identity evidence is passed directly to HasE.j; no theorem coercing arbitrary HasE evidence back to Has is used or proved.

There is an important additional step. The initial assembled polynomial raw-converts to the **graph-invariant proof polynomial**, not necessarily to I. The package does not infer a typed I witness merely from a claimed normal form. Instead, `identity_i_hasE` starts with the typed reflexive identity on the scalar left endpoint and applies another actual HasE.j to the already obtained leaf proof. The resulting witness is `jPoly I right leafEvidence`, which the inherited `j_conversion` proves converts to I. `HasE.conv` then retains the exact formed identity type and checks the I scope.

Finally, `scalar_fusion_from_bridges` uses the actual HasE piIntro/allIntro constructors with the original family formation derivations. It abstracts a, then f, introduces the type quantifier, and abstracts n. This produces exactly the imported three-term-binder polynomial c3 and exactly W(originalQ). No eta replacement or changed binder order is used.

## Checks and provenance

`GraphBridgeAssembly.lean` and `AssemblyControls.lean` compile under Lean 4.19.0 with `--trust=0`. The main source hash is:

`0dd6090f8cde9debb2bb58b921bac52c9bd6dd058cece3d2b09fc8f501d1b8e3`

Author controls check:

- the initial assembled witness converts to the graph proof;
- the additional reset witness has the literal leaf type under the same HasE bridge hypotheses and separately converts to I;
- literal definitions of the unchanged originalQ, W and c3;
- the theorem signature accepts two arbitrary HasE bridge derivations;
- seven positive theorem dependency traversals contain no forbidden semantic F/G, soundness, fundamental, graph-parametricity, semantic-standardness, or full-PER target-validation dependency;
- the final theorem actually depends on HasE.j, HasE.conv, HasE.piIntro, HasE.allIntro, the frozen literal graph invariant, and the frozen original scalar computation.

All reported theorem axioms are among ordinary Lean `propext`, `Classical.choice`, and `Quot.sound`; the four new generic identity helpers need only propext and Quot.sound. There are no admitted proofs, added axioms, unsafe implementations, parametricity assumptions, semantic-completeness principles, or omega-rules.

The author replay rehashes the 89 previously verified prerequisite objects and 83 pinned source modules recorded by `hase-full-per-review-20261010/PREREQUISITE_REBUILD.json`, prior full-PER and graph review records, all three predecessor manifests, the graph manifest, the four scalar-frontier source bindings, and the Lean binary. The original 83-module closure is not rebuilt. The source pin remains `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. Existing third-party objects and compiler bootstrap remain the inherited trust base; hashing the executable is not a bootstrap proof.

The frozen graph author and review files, the original compiler and typing grammar, ScalarFusionCore, and all predecessor evidence remain unchanged. Only this new scratch directory was written.

## Replay

From the workspace root:

```text
python hase-graph-bridge-assembly-20261010/verify.py
```

This rehashes reused inputs and compiles only the two new modules. It writes the author logs and JSON receipts under validation. `check.sh` and `lean_path.txt` specify the existing verified object paths for a direct one-file Lean invocation.

## Remaining boundary

This is a sufficient **conditional** route, not a classification of every possible scalar-fusion proof. Neither stateTransport nor scalarTransport has an unconditional source inhabitant here. The frozen direct-conversion obstructions for those two bridge endpoints are unaffected. Neither the original unconditional literal target nor its negation is proved. Independent review is a separate next step; author verification does not claim owner acceptance or programme closure.
