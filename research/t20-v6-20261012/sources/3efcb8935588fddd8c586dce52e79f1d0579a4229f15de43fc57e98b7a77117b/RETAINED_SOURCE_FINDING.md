# FABLE corroboration guard: decisive scope update

This section supersedes any reading of the earlier note as saying that retained work lacked proof-support-dependent guards. This is an internal AI source review, not external human review.

## What the retained source actually represents

The parent-located FABLE report explicitly has a proof/provenance calculus, `Γ ⊢_S c : est(a,t)`, and a corroboration guard described as “at least two distinct roots”. It says this creates tension with root-tracking cut/inlining. Thus **source-sensitive guarded proof semantics are already contemplated in retained research**. It would be wrong to claim invention of root guards or first recognition of support-sensitive substitution failure.

The source marks the Core B properties `DERIVED_BUT_UNVERIFIED`: “nothing in this list is checked by any committed artifact” (TYPED-CORE-CANDIDATES.md:89–90). NEGATIVE-RESULTS.md:3–11 marks the research non-adopted and corrects earlier overclaiming. The source provides no exact-support saturation theorem, no support-indexed implementation, no checking-cost recurrence, and no finite-state guarded compiler in these inspected sections. A bounded search for `corroboration guard`, `guard antitonicity`, `support locality`, `at least two ... root`, and `two distinct root` across P15/source-main .md/.py/.lean/.tex/.json/.yaml files located the two prose reports and SPA-R6's firewall, not a guarded compiler implementation. The FABLE checks directory contains only T299 and transversal/packing scripts; its Lean directory contains T299 files. This is bounded evidence, not a whole-history nonexistence theorem.

## Does it provide the demanded concrete licensing rule?

It supplies a real retained *candidate guard* on proof provenance: root count at least two. It does **not** in the inspected text specify the precise eligible content, corroborative roles, source-authentication predicate, or which contribution roots are counted. Therefore it is not yet a fully source-backed two-genuinely-corroborating-sources licence with anti-padding guarantees. A general total-support cardinality guard could accept irrelevant provenance padding; that defect must not be silently attributed to or repaired on behalf of an underspecified source.

The Core B transport side condition is genuinely support-sensitive: every root in the derivation must be in a partial origin map's domain (lines 85–87); an omitted calibration root blocks transport despite retained observation/custody strings (lines 121–132). It is downward closed in support, so it does not itself witness why subset-Pareto pruning is unsafe.

The T20 authority fixture in the earlier note remains a fixed-premise rule already covered by the predecessor. **It does not meet the parent's stronger request for a live licence depending on selected proof support.** It must not be used to claim such applicability.

## Recommended honest scope

A guarded compiler can be motivated by the inherited FABLE corroboration guard, but its content/role scoping must be an expressly declared refinement or constructed instantiation, not presented as extracted from a fully specified inherited two-source rule. Within this bounded search, no fully specified real collective-warrant rule with both exact-proof-support dependence and required anti-padding content/role scope was located.

SPA-R6 supplies the anti-copy and epistemic ceilings: copy/transform/sync inherit root union; authenticated acquisition alone adds a fresh root; distinct declared roots may share a hidden upstream anchor; root accounting proves no common knowledge or warrant. The executable `derive_roots` mirrors that accounting. Its `authenticated` flag is recorded by fixtures; the code does not authenticate actual evidence. No retained code was run or changed by this review.

## Pinned excerpts

### user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/fable-research/AR8R-FABLE-R1-NEGATIVE-RESULTS.md

SHA-256: `01fcca5e53a7f097df378ef6d68e1da5a40a750436ab211e1cd92b393d8d2220`

Lines 1–11:

```text
1: # AR8R-FABLE-R1 — negative results, refutations, and failed candidates
2: 
3: Status: research findings. Non-adopted. Item N1 was **substantially withdrawn and
4: rewritten** after independent review; the withdrawal record is
5: `AR8R-FABLE-R1-CORRECTION-RECEIPT-V1.md`.
6: 
7: None of the items below refutes an adopted premise of the program. They are
8: interpretation firewalls, constraints on proposed future definitions, failed
9: candidates generated inside round 1, and one reaffirmed gate. Round 1's original
10: framing — that four of five were "refutations of premises the program had been
11: treating as available" — was not supported by the repository and is withdrawn.
```

Lines 169–182:

```text
169: ## N5 — cut is not admissible in the certificate calculus without root tracking
170: 
171: Naive cut fails under transport: a two-root countermodel derives a judgment
172: whose inlined form is not derivable. Even root-tracking cut fails in the presence
173: of a corroboration guard ("at least two distinct roots"), because monotone guards
174: break under inlining.
175: 
176: A repaired rule, admissible under support-locality and guard antitonicity, exists:
177: inlining never widens the provenance footprint. But the repair carries a permanent
178: declared tension with corroboration guards.
179: 
180: **Consequence for the program's notion of closure.** "Closure" cannot be assumed
181: to compose. A system that closes over a lemma and then reuses it may lose
182: provenance guarantees the original derivation had.
```

### user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/fable-research/AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md

SHA-256: `19f1ee22e51db677f2b79e3a1db10923db35189a1cb7bc86bb710164dbd15f4a`

Lines 75–112:

```text
75: ## Core B — certificate / provenance calculus (proof-theoretic)
76: 
77: **Signature.** Judgments `Γ ⊢_S c : est(a,t)` — read: certificate `c` is
78: recorded as establishing that item `a` stands in the target-directed relation
79: to target `t` (object-language reading of the judgment, not a claim status) — with every context
80: entry annotated by a provenance root. Rules: assumption, axiom instance,
81: composition along declared target combinations, weakening, transport along a
82: morphism of settings, and repair. Items form an idempotent monoid, so
83: corroboration by copying is not a new item.
84: 
85: The load-bearing rule is transport, whose side condition requires every root in
86: the derivation to lie in the domain of a **partial** root map. Uncarried roots are
87: *dropped*, not relabelled.
88: 
89: **Derived properties** (every item `DERIVED_BUT_UNVERIFIED`; nothing in this
90: list is checked by any committed artifact).
91: 
92: - Survival under damage holds iff some derivation's support avoids the damage; the
93:   survival radius is the minimum transversal of the minimal-support hypergraph.
94: - **The MIN law:** a conjunctive burden is exactly as robust as its weakest
95:   conjunct. Adding guards to a multi-clause landing specification can only *lower*
96:   its radius — directly relevant to T299's six-clause conjunction.
97: - Deletion and corruption are indistinguishable exactly across transport and
98:   identical within a setting: a system that never transports cannot detect
99:   provenance corruption by survival testing alone.
100: - An unconditional sandwich `ν ≤ rad ≤ k·ν`, tight on both sides, with fractional
101:   exactness by LP duality.
102: - Repair buys damage-robustness at the cost of transport-fragility.
103: - Cut is inadmissible naively and under corroboration guards; a root-tracking
104:   repair is admissible under support-locality and guard antitonicity. Revocation
105:   must be modelled as damage, not as evidence.
106: 
107: **Battery outcome.** Level confusion and version: handled. Carrier: handled at the
108: calculus level only — no defence against badly declared axioms. Provenance,
109: partial observation, target mismatch, and closure: **succeeded** (closure twice).
110: Repairs exist for each: three-valuing the judgment (so a negative verdict is
111: *undetermined*, never *refuted*), declaring target-faithfulness explicitly, and
112: the root-tracking cut. Core B is a rival core, not a finished one.
```

Lines 121–140:

```text
121: **Setup.** Three provenance roots (observation, calibration, custody), three
122: context entries, two composition rules mirroring T299's landing conditions, and
123: one version-bump morphism.
124: 
125: **The single datum that separates them.** The root map's domain omits the
126: *calibration* root: a field deployment re-acquires observations and re-runs custody
127: but has no counterpart acquisition for the lab calibration. The instrument still
128: prints its reading. What is missing is the acquisition root of the warrant to
129: *read* that string as a landed burden.
130: 
131: - **Core B:** transport is blocked, the calibration entry is dropped, and forward
132:   saturation never derives the landing judgment. **Not certified.**
133: - **Core A:** both backgrounds have identical six-coordinate matched profiles and
134:   identical labels, so the label is constant on the single attained fibre.
135:   **Certified.**
136: 
137: The reason is structural: a provenance root is not a profile coordinate. The
138: program's own coordinate registry already lists provenance root among the
139: forbidden collapses of the visible profile — this scenario is a concrete witness
140: for that prohibition.
```

### user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/rounds/SPA-R6_PROVENANCE_ROOT_INVARIANT.md

SHA-256: `262de6927a39e3b1a6a6b3640f615613effe5be5564a0d4d27df60b01de5d044`

Lines 1–47:

```text
1: # SPA-R6 — provenance-root nonmultiplicity under copying and synchronization
2: 
3: **Status:** specialist-local formalization of the repository's existing
4: provenance/TAC-SAC noncollapse discipline; no historical reconstruction or
5: novelty.
6: 
7: ## Frozen DAG semantics
8: 
9: Each episode is a node in a finite acyclic lineage graph.
10: 
11: - `copy`, `transform`, and `sync` nodes inherit the union of predecessor roots.
12: - `acquire` nodes inherit predecessor roots and add one fresh authenticated root.
13: - root labels, carriers, episodes, lineages, copies, and evidential independence
14:   remain distinct coordinates.
15: 
16: ## Invariant
17: 
18: Adding a pure copy/transform/synchronization node does not enlarge the global
19: root set. Only a typed authenticated acquisition adds a fresh root in this
20: semantics.
21: 
22: ## Countermodels and firewalls
23: 
24: - One root followed by 100 copies yields 101 episodes and still one root.
25: - Synchronizing two root-bearing episodes unions availability but does not make
26:   carriers or episodes numerically identical.
27: - Two distinct root labels may share a hidden upstream anchor, so root
28: distinctness alone does not prove stochastic or evidential independence.
29: - Equal root sets do not imply equal carriers, episodes, or lineages.
30: 
31: ## Executable evidence
32: 
33: The checker exhausts 23,369 valid operation sequences through five nodes and
34: performs 92,740 node-level invariant checks with zero failures. Seven mutants
35: are killed, including root creation by copy or sync, carrier/root count
36: collapse, distinct-root independence, root-set numerical identity, and
37: capability/authorization/warrant collapse.
38: 
39: ## Conclusion ceiling
40: 
41: ```text
42: AUTHENTICATED_LINEAGE_ROOT_ACCOUNTING_ONLY
43: NO_TAC_SAC_HISTORICAL_IDENTITY
44: NO_NUMERICAL_IDENTITY
45: NO_EVIDENTIAL_INDEPENDENCE
46: NO_COMMON_KNOWLEDGE_OR_WARRANT
47: ```
```

### user-checkpoints/extracted/P15/source-main/docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/specialist-a/source-files/checks/check_r6_provenance_roots.py

SHA-256: `e3ca7be59d8b1c3c4975c435d41084ff818389cf02167fbbb0441cc20f733e8e`

Lines 13–13:

```text
13: PURE_KINDS = {"copy", "transform", "sync"}
```

Lines 35–55:

```text
35: def derive_roots(ops):
36:     roots = [{"r0"}]
37:     global_roots = {"r0"}
38:     trace = [{"node": 0, "kind": "root", "parents": [], "roots": ["r0"], "global_roots": ["r0"]}]
39:     for i, op in enumerate(ops, start=1):
40:         inherited = set().union(*(roots[p] for p in op["parents"])) if op["parents"] else set()
41:         if op["kind"] in PURE_KINDS:
42:             node_roots = inherited
43:         elif op["kind"] == "acquire":
44:             node_roots = inherited | {f"r{i}"}
45:         else:
46:             raise ValueError(op)
47:         before = set(global_roots)
48:         global_roots |= node_roots
49:         roots.append(node_roots)
50:         trace.append({
51:             "node": i, "kind": op["kind"], "parents": list(op["parents"]),
52:             "roots": sorted(node_roots), "global_before": sorted(before), "global_after": sorted(global_roots),
53:             "authenticated": op["authenticated"],
54:         })
55:     return roots, global_roots, trace
```

Lines 114–144:

```text
114: def explicit_models():
115:     # Copy explosion from one root.
116:     ops = tuple({"kind": "copy", "parents": (i - 1,), "authenticated": True} for i in range(1, 101))
117:     roots, global_roots, trace = derive_roots(ops)
118:     copy_explosion = {
119:         "episode_count": len(roots),
120:         "carrier_or_copy_count_after_root": len(roots) - 1,
121:         "authenticated_root_count": len(global_roots),
122:         "last_episode_roots": sorted(roots[-1]),
123:         "lesson": "copy multiplicity does not create independent acquisition roots",
124:     }
125: 
126:     sync_ops = (
127:         {"kind": "acquire", "parents": (), "authenticated": True},
128:         {"kind": "sync", "parents": (0, 1), "authenticated": True},
129:     )
130:     sroots, sglobal, strace = derive_roots(sync_ops)
131:     sync_model = {
132:         "trace": strace,
133:         "final_episode_roots": sorted(sroots[-1]),
134:         "global_root_count": len(sglobal),
135:         "lesson": "synchronization unions availability; it does not make episodes or carriers numerically identical",
136:     }
137: 
138:     hidden_anchor = {
139:         "declared_root_labels": ["rA", "rB"],
140:         "root_labels_distinct": True,
141:         "hidden_upstream_anchor": {"rA": "h0", "rB": "h0"},
142:         "statistical_or_evidential_independence_established": False,
143:         "lesson": "distinct authenticated acquisition roots do not alone establish uncorrelated evidence or distinct ultimate source",
144:     }
```


---

## Earlier inspected T20 interface (qualified above)

# Bounded retained-source review: guarded support compilation

9 October 2026. Read-only inspection of retained inputs. No repository integration, closure, application-soundness, new kernel-validation, or active-research-duration credit.

## Finding

The directly inspected T20 grounded-attestation component already contains **ordinary minimal-root-support saturation for finite positive Horn rules**, anchored-cycle treatment, role-specific testimony/authority premises, and a carrier-to-actual-root quotient. It does **not** give its rules a predicate on the exact supports of the selected premise proofs. Its Python compiler discards strict support supersets immediately. Its Lean `Derivable.step` receives a claim-premise set and proofs available from one ambient root set, but no exact-support argument.

The newer certificate-compilation result expressly excludes hidden proof-dependent admissibility tests. It already notes that fully scoped labels must retain source restrictions and that repeated P premises cannot encode two independent sources; it also supplies an exact-support loop-pruning observation. Consequently, guarded exact-support saturation is **not implemented by these inspected algorithms**, but a finite explicit support-state lifting is compatible with their stated fully scoped grammar interface. A new result should be described as a constructive guarded-interface extension, not a discovery that provenance or copied-source restrictions were absent from the programme. No absence claim is made for uninspected T7–T19 originals.

## A real source-bound licence

Use the retained `historicalDirective` rule:

    issuedAt0 AND standingAt0 -> duty0

The base map ties these roles to `pastOrder` and `pastStanding`. This is an actual authority/provenance combination: provenance of the particular issued directive is insufficient without historical legitimate standing; unrelated current authority, implementation readiness, or source assertions cannot replace the missing role. The same fixture separately requires `ownsDuty0 AND veracious -> duty0`, `liveStanding AND scopeNow -> mayIssueNext`, and `duty0 AND applicableNow0 AND ready -> actNow`. The written source explains historical scope and force.

These rules are **not themselves two-independent-source rules**. In particular, the generic quotient deliberately permits one actual root to support several separately identified facts. Distinct role obligations do not logically entail distinct roots. Do not claim that two-source independence is inherited from `historicalDirective`, or add a distinct-root test and attribute that strengthening to this fixture.

For a test derived from this actual licence, preserve the exact content/time/role judgements. A copied or reviewed `issuedAt0` report does not create `standingAt0`; padding with an unrelated claim cannot do so either. Multiple aliases of one source collapse to one root for any explicitly declared root count. A *newly stipulated* corroboration licence must separately require two eligible reports of the same scoped content (or specific complementary roles), and apply origin separation to those eligible contributions rather than all tokens in the support. The retained source does not supply a universal two-source truth rule.

## Semantic ceiling

Actual-origin identity is supplied, not discovered or authenticated by these formalisms. Declared distinct roots mean provenance separation at the chosen support-duty granularity. They establish neither truth, reliability, nor statistical independence. Conversely, common lineage does not prevent one source from legitimately supplying different facts; it only prevents counting the same origin twice in an explicitly required source count. A faithful review can check a different error without becoming a second original observation.

## Scope of inspection

Targeted searches of the retained P14/P15 orthemology-v5 source did not locate a collective-warrant/source-origin licence; those matches concerned repository source roots. The concrete relevant component was found under retained T20 `grounded-attestation`. Metaphysical cooperation models whose comments merely mention source roots were excluded. The authority fixture, generic derivation type, actual support compiler, quotient interface, and the requested two recent result interfaces were directly inspected. The excerpts below are complete for their declared line ranges, not substitutes for whole-programme inspection.

## Exact snippets and input hashes

### recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/grounded-attestation/lean/OccurrenceControls.lean

SHA-256: `b1423809f4f2b3b5ef6b5490702007637109952df98fdefe04d389d7a9dc792a`

Lines 8–33:

```text
8: inductive Root
9:   | source | truth | pastOrder | pastStanding | grantNow | scopeNow | occasion | implementation
10:   deriving DecidableEq
11: 
12: inductive Claim
13:   | ownsDuty0 | veracious | issuedAt0 | standingAt0 | liveStanding | scopeNow
14:   | applicableNow0 | ready | duty0 | mayIssueNext | actNow
15:   deriving DecidableEq
16: 
17: def baseClaim : Root → Claim
18:   | .source => .ownsDuty0
19:   | .truth => .veracious
20:   | .pastOrder => .issuedAt0
21:   | .pastStanding => .standingAt0
22:   | .grantNow => .liveStanding
23:   | .scopeNow => .scopeNow
24:   | .occasion => .applicableNow0
25:   | .implementation => .ready
26: 
27: def Base (root : Root) (claim : Claim) : Prop := claim = baseClaim root
28: 
29: inductive Rule : Finset Claim → Claim → Prop
30:   | testimony : Rule {.ownsDuty0, .veracious} .duty0
31:   | historicalDirective : Rule {.issuedAt0, .standingAt0} .duty0
32:   | prospective : Rule {.liveStanding, .scopeNow} .mayIssueNext
33:   | implementation : Rule {.duty0, .applicableNow0, .ready} .actNow
```

Lines 117–133:

```text
117:  theorem no_owned_truth_from_authorship_alone :
118:     ¬ Derivable Base Rule {.source} .duty0 := by
119:   let V : Claim → Prop := fun c => c = .ownsDuty0
120:   have roots : ∀ r ∈ ({.source} : Finset Root), ∀ c, Base r c → V c := by
121:     intro r hr c hc
122:     have heq : r = .source := Finset.mem_singleton.mp hr
123:     subst r
124:     simpa [Base, baseClaim, V] using hc
125:   have rules : ∀ P c, Rule P c → (∀ p ∈ P, V p) → V c := by
126:     intro P c hr hp
127:     cases hr with
128:     | testimony => exact False.elim (Claim.noConfusion (hp .veracious (by decide)))
129:     | historicalDirective => exact False.elim (Claim.noConfusion (hp .issuedAt0 (by decide)))
130:     | prospective => exact False.elim (Claim.noConfusion (hp .liveStanding (by decide)))
131:     | implementation => exact False.elim (Claim.noConfusion (hp .ready (by decide)))
132:   intro h
133:   exact Claim.noConfusion (derivable_sound V roots rules h)
```

### recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/grounded-attestation/lean/GroundedSupport.lean

SHA-256: `73a16000e935ec267a3bb837197ab938e90d6d033c63e54847a4d7479d755aed`

Lines 8–22:

```text
8: /-- Finite grounded proofs; the surrounding rule graph may be cyclic. -/
9: inductive Derivable (base : Root → Claim → Prop)
10:     (rule : Finset Claim → Claim → Prop) (available : Finset Root) : Claim → Prop
11:   | root {r c} : r ∈ available → base r c → Derivable base rule available c
12:   | step {premises c} : rule premises c →
13:       (∀ p ∈ premises, Derivable base rule available p) →
14:       Derivable base rule available c
15: 
16:  theorem derivable_mono {base : Root → Claim → Prop}
17:     {rule : Finset Claim → Claim → Prop} {A B : Finset Root}
18:     (hAB : A ⊆ B) {c : Claim} (h : Derivable base rule A c) :
19:     Derivable base rule B c := by
20:   induction h with
21:   | root hm hb => exact .root (hAB hm) hb
22:   | step hr hp ih => exact .step hr (fun p hm => ih p hm)
```

Lines 33–42:

```text
33: /-- Semantic truth is conditional on true roots and truth-preserving rules. -/
34:  theorem derivable_sound {base : Root → Claim → Prop}
35:     {rule : Finset Claim → Claim → Prop} {A : Finset Root}
36:     (meaning : Claim → Prop)
37:     (roots_sound : ∀ r ∈ A, ∀ c, base r c → meaning c)
38:     (rules_sound : ∀ P c, rule P c → (∀ p ∈ P, meaning p) → meaning c)
39:     {c : Claim} (h : Derivable base rule A c) : meaning c := by
40:   induction h with
41:   | root hm hb => exact roots_sound _ hm _ hb
42:   | step hr hp ih => exact rules_sound _ _ hr (fun p hm => ih p hm)
```

### recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/grounded-attestation/grounded_support.py

SHA-256: `9d70989837f3abc364f315a43067554c1b7bd251254e1c33c1d7b358fd948d05`

Lines 4–22:

```text
4: def minimize(family):
5:     family=frozenset(frozenset(s) for s in family)
6:     return frozenset(s for s in family if not any(t < s for t in family))
7: 
8: def minimal_supports(base,rules):
9:     """Least finite grounded closure, annotating claims with minimal root sets."""
10:     result={}
11:     for root,claim in base:
12:         result[claim]=minimize(tuple(result.get(claim,()))+(frozenset({root}),))
13:     rules=[(tuple(body),head) for body,head in rules]
14:     while True:
15:         changed=False
16:         for body,head in rules:
17:             families=[result.get(claim,frozenset()) for claim in body]
18:             if any(not f for f in families):continue
19:             candidates=[frozenset().union(*choices) for choices in product(*families)]
20:             old=result.get(head,frozenset());new=minimize(tuple(old)+tuple(candidates))
21:             if new!=old:result[head]=new;changed=True
22:         if not changed:return result
```

### recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/grounded-attestation/lean/GroundedQuotient.lean

SHA-256: `7a6094de7a0abc93af603605c8f25227711ff4e4aac74b791066cdbe8b210c0b`

Lines 8–19:

```text
8: /-- One actual root may support several separately identified carrier facts. -/
9: def QuotientBase (origin : Label → Root) (U : Finset Label)
10:     (base : Label → Claim → Prop) : Root → Claim → Prop :=
11:   fun r c => ∃ label ∈ U, origin label = r ∧ base label c
12: 
13: /-- Folding fixed carrier aliases is exact for grounded inference when availability
14:     is pulled back to all and only carriers of an available actual root. -/
15:  theorem quotient_derivable_iff (origin : Label → Root) (U : Finset Label)
16:     (base : Label → Claim → Prop) (rule : Finset Claim → Claim → Prop)
17:     (available : Finset Root) (c : Claim) :
18:     Derivable (QuotientBase origin U base) rule available c ↔
19:       Derivable base rule (U.filter (fun label => origin label ∈ available)) c := by
```

### recovery-t20/earlier/consolidated/Orthemology_T16_T20_Consolidated_v1_20261007/t20/sources/grounded-attestation/EXACT_PROBLEM_AND_WRITTEN_PROOF.md

SHA-256: `b7dd5174207871abbff81e4c499bf74eabc7305402c7d88971e8b12bf96b4037`

Lines 15–23:

```text
15: Fix a type B of primitive support roots and a type C of claims. Root identity is the identity of the actual acquisition or supporting duty, not the displayed carrier label. Let base : B -> C assign each root its primitive claim. A positive finitary rule is a pair (P,c), with P a finite set of premise claims and c its conclusion. Let R be the selected rule set.
16: 
17: For a finite available-root set A, define D(A,c) by the least inductive relation:
18: 
19: - Root: if b is in A, infer D(A,base(b)).
20: - Rule: if (P,c) is in R and D(A,p) for every p in P, infer D(A,c).
21: 
22: Only finite derivations generated by these rules count. A cycle is not itself a derivation. Rules may have empty premise sets, but an empty-premise rule is an explicit axiom with its own soundness burden, not a consequence of a cycle.
23: 
```

Lines 31–35:

```text
31: 
32: Proof: induction on the finite derivation. A root remains available by inclusion. Every premise derivation in a rule step transports by induction, so the same rule applies. This does not use acyclicity of the rule graph.
33: 
34: Let V interpret claims as propositions. Suppose each available primitive claim V(base(b)) holds, and every selected rule preserves V from all its premises to its conclusion. Then D(A,c) implies V(c).
35: 
```

Lines 51–65:

```text
51: 
52: A retraction Delta defeats c exactly when it intersects every member of M_U(c). Thus minimal defeating retractions are the minimal hitting sets of the minimal-support family. If the family is empty, c was already underivable. If it contains the empty support, no root-only retraction can defeat c.
53: 
54: A flattened union of all support roots is too conservative: requiring that union to survive treats alternative derivations as jointly necessary. A flattened set of individually occurring roots is also insufficient to reconstruct the alternative bundles. Whole derivational supports matter. This connects directly to the earlier source-relative whole-row discipline, but Theorem 2 gives an exact dynamic test rather than another static row warning.
55: 
56: ## Corollary 4 Source assertion and prospective command can react differently
57: 
58: Use distinct claims ObligationAt(t0), ImperativeAt(t0), AuthorisedIssuerAt(t0), LiveStanding(now), MayIssueNext(now), ApplicableNow(t0) and ExecutableNow. An authenticated source-owned assertion of ObligationAt(t0), together with the applicable veracity and semantic-fidelity roots, supplies a testimonial derivation of ObligationAt(t0). It does not require an additional AuthorisedIssuerAt(t0) premise merely to repeat proof of that same obligation.
59: 
60: A completed bare constitutive directive at t0 derives ObligationAt(t0) through evidence that legitimate standing, correct force and scope held at t0. A later prospective-grant revocation does not delete those historical facts. Instead a distinct current root LiveStanding(now) supports a prospective conclusion MayIssueNext(now); removing that current root may defeat that conclusion. Evidence invalidation of an old attribution or historical-standing record is a different operation, which can remove an old epistemic route. A surviving alternative testimonial route can still support ObligationAt(t0) without a duplicate jurisdiction proof.
61: 
62: Execution now requires the correctly indexed applicability and implementation premises. Removing ApplicableNow(t0) can block ExecutableNow without retracting the historical obligation conclusion. Erasing t0 or interpreting a historical quotation as a new directive changes the rule/claim interpretation and is not licensed by Theorem 2.
63: 
64: The formal result does not assume that all testimony needs exceptional-source certification. Ordinary defeasible entitlement from T17 remains a separate epistemic route. A chosen primitive ordinary-entitlement root can be represented, but the finite model does not reduce all ordinary warrant to a factive universal calculus.
65: 
```

Lines 68–86:

```text
68: Let C={a,b}; there are no available primitive roots and the only rules are a from b and b from a. The set {a,b} is closed under the rules, so a checker accepting any mutually consistent fixed point would accept it. Yet the least grounded derivation contains neither claim. Every alleged finite derivation of a would have a shorter derivation of b, and every derivation of b a shorter derivation of a; there is no leaf. Induction on derivation therefore rules out both.
69: 
70: Adding one genuine root for a grounds both conclusions. The rule graph may contain cycles without making the model useless. The distinction is ungrounded bootstrap versus anchored cyclic reuse, not a blanket ban on feedback or mutual testimony.
71: 
72: ## Counterexample 6 Carrier cut minimisation does not commute with root identification
73: 
74: Take carrier labels a1,a2,a3,b1,b2. Six alternative support bundles are {ai,bj}, for i in {1,2,3} and j in {1,2}. At label level, the unique minimum-cardinality defeating set is {b1,b2}, of size two. The alternative cut {a1,a2,a3} has size three and is discarded by minimum-cardinality-first processing.
75: 
76: Now let a1,a2,a3 be three presentations of one acquisition root a, while b1 and b2 have distinct roots b and c. The six bundles become two minimal actual-root supports {a,b} and {a,c}. Their unique smallest defeating root set is {a}, size one. Mapping only the previously selected minimum label cut returns {b,c}, size two and misses the actual weakest support.
77: 
78: Therefore identify actual roots before optimising a root-fault budget, or retain enough of the full cut/support family to perform the quotient correctly. This is a concrete sharp control, not a new general claim that copying improves independence. It extends the prior copied-root ceiling into a failure of a specific plausible order of computation.
79: 
80: The quotient assumes aliases share the source-root failure duty being modelled. If different carrier channels fail independently, those channel duties need their own primitive roots; identifying the source does not erase real channel evidence.
81: 
82: ## Finite effective computation
83: 
84: For finite B and C, enumerate root subsets S of U. Compute D(S,-) by ordinary least forward closure, which stabilises after at most |C| additions for a fixed S. Keep those S deriving c for which no proper subset derives c. This exact baseline computes M_U(c) and is enough for exhaustive controls.
85: 
86: A support-propagation algorithm can instead carry antichains: root b contributes {b}; a rule takes unions of one support from each premise; at each claim remove strict supersets of another known support. Iterate from no derived supports. A newly admitted support never needs to be reintroduced after a strict subset permanently dominates it, and there are at most |C| times 2^|U| possible supports. Thus the finite process terminates. Its soundness follows by combining finite derivations; completeness follows by induction on a finite derivation, since replacement by a smaller support preserves availability. Cycles without roots contribute no supports.
```

Lines 113–117:

```text
113: 
114: For every pi, the inclusion-minimal cuts of the image support family pi(F) are exactly the inclusion-minimal members of {pi(C) : C in I(F)}.
115: 
116: Proof. The image of a label cut hits every image support: map an element witnessing each original intersection. Conversely, let D be an inclusion-minimal root cut. Its preimage within U is a label cut. By finiteness it contains an inclusion-minimal label cut C. Then pi(C) is a root cut and is contained in D. Minimality of D makes pi(C)=D. Finally an inclusion-minimal image of an archived minimal label cut is a minimal root cut: any smaller root cut contains a minimal root cut, which by the previous argument is another archived image, contradicting image minimality. All empty-family and empty-support cases are covered by the same definitions; existence is invoked only for a set already known to be a cut.
117: 
```

### certificate-compilation-boundary-20261009/RESULT.md

SHA-256: `3d8d11d73055b62913cf36138cc0b3b273d032f8f927a885ee2af11bd8eaf459`

Lines 25–40:

```text
25: Fix finite sets J of fully scoped judgements and E of authenticated evidence-token identities. Let n=|J| and m=|E|. A judgement includes every parameter on which proof substitutability depends: proposition or type, context, claim and rule version, source restrictions, and any relevant resource or independence requirements.
26: 
27: Fix a finite set R of **ground rule instances**. A rule r consists of:
28: 
29: - a head h(r) in J;
30: - a finite ordered list p(r)=(q1,...,qk) of premise judgements in J, possibly with repetitions;
31: - a local evidence requirement B(r) contained in E;
32: - a local checking cost w(r) in the nonnegative natural numbers.
33: 
34: A nullary rule may be an admitted logical axiom, an evidence introduction, or another justified leaf. Its evidence requirement is still explicit. A rule with premises is available exactly when proofs of those precise judgements and its local evidence are supplied. There are no hidden global admissibility tests depending on the proof's shape, history, or the particular proof chosen for a premise. Rule-instance validity is settled at admission, and conditional soundness of the grammar is a separate assumption.
35: 
36: The rules are positive in this operational sense. A judgement whose *content* is a negation can be present, but absence of a proof is not itself an evidence-producing rule. No circular or coinductive proof principle is assumed.
37: 
38: Evidence is persistent, reusable, and combined by set union. Repeated occurrences of a judgement allow reuse of a proof of that same judgement. A demand for two independent sources cannot be encoded merely as two identical P premises: source-labelled judgements or an explicit independently justified relation must retain that demand. If this refinement makes the required judgement universe infinite, this theorem's finiteness assumption has not been met.
39: 
40: All rule premises must be replaceable by any valid proof of the same fully scoped judgement. A context-sensitive typing or assumption-discharge system is covered only after this property is demonstrated for its chosen finite ground interface. Erasing contexts or types to manufacture repeated labels invalidates the pruning proof below.
```

Lines 85–87:

```text
85: An arbitrary tree's *exact* support can shrink. For example a single judgement q has a leaf requiring a and a self-rule additionally requiring b. A two-node derivation has support {a,b}; its one-node dominator has support {a}. The larger support is irrelevant to the Pareto objective, but it is still a genuine possible proof support. The theorem does not claim to enumerate every proof or every exact-support derivation within height n.
86: 
87: If exact support is required for another purpose, repeatedly delete only ancestor–descendant pairs having both the same judgement and the same subtree support. This preserves exact support and weakly reduces cost; node count still decreases when a deleted loop costs zero. Along a branch subtree supports are nested and strictly decrease at most m times; each constant-support block has at most n different judgements after pruning. The finite family bounded by height n(m+1) therefore dominates every proof having that exact support, so it attains the minimum whenever that support occurs. This observation is not needed by the frontier compiler and does not enumerate all support-bearing trees or preserve all derivation structure.
```

### warranted-discrimination-research-20261009/RESULT.md

SHA-256: `71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28`

Lines 41–60:

```text
41: ### 2.2 Evidence is not a truth oracle
42: 
43: Let E be a finite set of distinguishable evidence tokens. Each token identifies its content, source or acquisition route, target/version, applicable scope and authentication conditions. Tokens need not be independent probabilistic samples. Distinct tokens in the examples discharge distinct premise obligations; copying one token does not create another premise or independent source.
44: 
45: K⊆E is the currently accessible authenticated inventory. Authentication establishes the declared identity and integrity conditions, not the truth of every assertion inside the artifact. The source commitments determining what an authenticated token supports remain explicit premises of the analysis. A test may return raw text and deliver no usable token. A separate authentication or interpretation step must then be represented before that text can discharge a premise.
46: 
47: Fix a finite catalogue Γ of admitted valid derivation templates generated from an explicit finite bounded proof grammar, or supplied as individually inspectable finite derivations. Their rule/scope well-formedness is established at catalogue admission. Under the supported-input conditions below, each terminal instantiation/check is guaranteed to succeed; its cost is still paid when executed. An unvalidated or potentially failing candidate is not admitted under this contract: checking it would require an additional outcome-bearing transition. For π∈Γ, record:
48: 
49: - Sπ⊆E: the evidence leaves actually cited in this derivation;
50: - vπ∈V: its exact scoped conclusion;
51: - κπ≥0: its finite real declared terminal assembly/checking cost;
52: - the derivation itself and its rule, interpretation and version references.
53: 
54: The catalogue is not an arbitrary list of true answers. Its supports are extracted from finite derivations. For an acyclic positive rule system they can be compiled recursively: evidence leaves contribute singleton supports; combining premises takes unions; alternative derivations take alternatives. Shared leaves are not counted twice. The catalogue can be incomplete for the logic; all optima below are relative to it and its expressly permitted alternatives.
55: 
56: ### 2.3 Conditional soundness and production
57: 
58: Assume that evidence admitted to K meets the specified source commitments and that each rule preserves the declared judgement when its premises are supported. Induction on a proof object then establishes the ordinary conditional soundness lemma: if Sπ⊆K and π passes the rule/scope checker, producing π warrants vπ **relative to those commitments**. The induction does not authenticate its own leaves or certify the philosophical adequacy of the rule system.
59: 
60: Availability of the leaves makes π eligible for checking. It does not say checking has already occurred. The protocol completes only when it produces and checks a selected π, paying κπ. A previously checked reusable certificate can have its own token and expressly priced reuse rule. An unexecuted terminal instantiation is not silently assigned zero checking cost. Query prices include any authentication charged at acquisition; terminal prices cover the final derivation. Optimising the internal scheduling and reuse of arbitrary proof fragments is outside this restricted model.
```

