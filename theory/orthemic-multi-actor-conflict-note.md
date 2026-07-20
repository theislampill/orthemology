# Multi-Actor / Zero-Sum Orthemic Note — stress test, corrections, and formal residue

**Status (revision R4, 2026-07-20; candidate revision pending independent review):** derived multi-actor extension of the formal core; typing follows decisions 0009–0015; nothing here is experimentally validated.

> **Provenance.** Written from three informal zero-sum discussion notes
> supplied to the project (private; not published), treated as a THEORY
> STRESS TEST, not accepted doctrine — original header preserved in
> [`docs/provenance/document-history.md`](../docs/provenance/document-history.md).
> Verdict up front: the source notes surface a real and useful multi-actor
> layer, AND they conflate five distinct categories; the repair below
> preserves the insight without the conflations. The formal residue is a
> **clarification plus derived extensions of the existing actor/analysis
> indices — not a seventh formal addition.**

## 1. What the source notes get right (preserved)

1. **One shared concrete occurrence.** Both players face the SAME orthemma —
   the game state. Multi-actor cases do not multiply occurrences; they
   multiply perspectives on one occurrence lineage.
2. **Actor/analysis-relative evaluation can oppose.** "Correct for A" and
   "correct for B" genuinely diverge under a competitive task; the theory's
   per-actor analysis indexing (`A_α` with `T_α = task(A_α)`, `Π_{A_α}`)
   was built for exactly this and handles it. (Notation update, D1
   reconciliation: `A` is reserved for the declared analysis; the formal
   actor indices are `α, β`, with the prose labels "Player A / Player B"
   naming the actors `α, β` respectively. Multi-actor evaluation is a
   multi-analysis context, so the task-relative shorthand of manuscript
   Definition 3 is forbidden here and ground truth is written in full,
   `O*(m; A_α)`.)
3. **Structural isomorphism across actors.** A's and B's reasoning can be
   the same schema under role substitution while their targets are
   materially incompatible — a real and clarifying observation.
4. **Coupled episodes through a shared successor.** A's move-episode
   produces the successor occurrence B's episode consumes: the typed-edge
   episode graph (core-formalization §5.2) over one occurrence lineage.
5. **Competitive vs cooperative as target-set relations.** Pair programming
   = shared target profile; chess = disjoint target profiles. Correct.

## 2. Category conflations corrected

**C1 — "Player A's ortheme: the state where my utility is maximized."**
That is not an ortheme; it is an OBJECTIVE rendered as a state description.
An ortheme is a repeatable state-type of the occurrence ("White checkmates
Black" IS one). The repair: player A's *target profile set*
`𝒢_{α,A_α} ⊆ Π_{A_α}` is the
set of terminal profiles that satisfy that player's task — the states are orthemes;
"maximize my utility" is the task that SELECTS them. Utility/objective/loss
are external parameters (core-formalization §3), never orthemes and never
metaorthemes.

**C2 — "their orthemes are completely identical in structure."**
Isomorphism is not identity. The goal SCHEMA "win-for-me" is invariant
under the role substitution φ(α→β); the EXTENSIONS differ: φ maps
"White checkmates Black" to "Black checkmates White." Two consequences the
source notes blur: (i) nothing is "the same ortheme" here — the schemas are
isomorphic, the target profiles disjoint; (ii) the interesting fact is
precisely that φ exists and 𝒢_{β,A_β} = φ(𝒢_{α,A_α}) while
𝒢_{α,A_α} ∩ 𝒢_{β,A_β} = ∅.

**C3 — "the metaortheme = the rules of the game + the logic of minimax."**
Three different things, none of them a metaortheme:
- **game transition rules** — the DOMAIN's lawful-transition structure
  (which successor occurrences are reachable at all);
- **utility / rational maximization** — the TASK/objective, an external
  parameter excluded from governed components;
- **minimax** — a POLICY/strategy (a way of choosing actions under the
  task).
A metaorthemic configuration in a game would govern something like: what
counts as EVIDENCE about the opponent's information state; which analysis
depth suffices before a move may be made (an evidence-sufficiency
distinction); whether an engine evaluation is validated or provisional;
when a position assessment is stale (position edited between analyses).
The source notes' "neutral governing logic" intuition is real, but the
neutral shared things are the domain rules and the task-form — the
metaortheme slot was mislabeled.

**C4 — occurrence identity is thinner than it should be, and information
sets are OBSERVATIONS, not identity (corrected after external
review).** "The board" is not enough: chess needs position + move history
(castling/repetition rights) + player-to-move — all WORLDLY facts of the one
occurrence, so they belong in the identity key κ (#4 applied). But a
player's INFORMATION SET is not part of κ: in poker the one concrete deal
(all hole cards) IS the occurrence m; what player α knows of it is α's
OBSERVATION, x_α = Ω_α(m) — the framework's own observation-vs-occurrence
distinction, applied per actor. Imperfect information = one shared m with
divergent Ω_α(m) ≠ Ω_β(m); perfect-information games are the special case
Ω_α = Ω_β = full state. Filing the information set into κ would invert the
occurrence/observation line the theory is built on.

**C5 — strict zero-sum does not mean every state realizes ±X.** U_α + U_β = 0
admits draws (0,0). Terminal profiles partition into 𝒢_α, 𝒢_β, and a
nonempty draw set in general; "the objective manifestation of A's ortheme
mathematically prevents B's" holds only between the two win-sets, not over
the whole terminal space.

**C6 — "reflexively selfish" is task language, not psychology or ethics.**
Under T_α = "win for the player labeled A," correctness is α-indexed by construction; that is
a property of the DECLARED task, not a discovery about agents. And not all
orthemes are actor-relative: "the file hash matches," "the parse is
grammatical" are actor-independent placements; actor-relativity enters
exactly where the task does.

## 3. Formal residue (assessed against the existing core)

Already expressible with existing machinery: episodes carry actor α and
declared analysis A_α (task T_α = task(A_α)); placements are
actor/analysis-indexed; the episode graph couples episodes
over one lineage. **New derived definitions worth adding (clarification,
NOT a new formal addition — the six-addition count is unchanged):**

```text
x_α = Ω_α(m)         actor-α's OBSERVATION of the shared occurrence m
                     (imperfect information: Ω_α(m) ≠ Ω_β(m) over ONE m)
p̂(e, α, T_α)        the current inferred profile of actor α's episode e
                     under its analysis A_α, task T_α = task(A_α)
                     (inferred FROM x_α, never from m directly)
GoalSchema(·)   a PARAMETRIC ortheme schema — the shared
                     goal-form under role substitution ("win for α")
𝒢_{α,A_α} ⊆ Π_{A_α}  actor-α's grounded TARGET PROFILE SET: the profiles
                     T_α declares appropriate as outcomes — the schema's
                     instantiation at α. NORMATIVE TYPING: a SET of
                     profiles; each member is one complete profile
φ(α→β)               a role/perspective isomorphism between Π_{A_α} and
                     Π_{A_β}, when one exists
                     (schema invariance: 𝒢_{β,A_β} = φ(𝒢_{α,A_α}))
Compat_m(𝒢_α, 𝒢_β)    ∃ m′ ∈ Reach(m): O*(m′; A_α) ∈ 𝒢_α ∧ O*(m′; A_β) ∈ 𝒢_β
                     (well-typed: one shared occurrence, each analysis
                     evaluating in its own profile space — never bare
                     intersection of sets from different spaces)
Conflict_m(𝒢_α, 𝒢_β)  no such reachable m′ exists
                     (cooperation: shared analysis + shared target set,
                     or an explicit alignment map φ(α→β))
```

**Three distinct relations the parametric schema untangles:**
(i) SCHEMA identity — players A and B run the same parametric form `GoalSchema(·)`; this is
the true content of the source notes' "locally identical" intuition; (ii)
GROUNDED-ORTHEME identity — `GoalSchema(α)` and `GoalSchema(β)` are DISTINCT grounded
targets, never identical in a strictly competitive task; (iii)
TARGET-PROFILE overlap — `𝒢_α ∩ 𝒢_β` may be empty (zero-sum win-sets),
partial, or total (cooperation). Local similarity is (i); material
exclusivity is emptiness at (iii); no level asserts identity of the
players' orthemes.

**The limited sense in which competitors DO share a metaorthemic
configuration:** both players may consult the SAME governing distinctions —
terminality (decided vs live position), evidence-validity for reading the
opponent's information state, analysis-sufficiency before moving. Sharing
those configurations while holding opposed targets is exactly the
configuration-vs-task separation: metaorthemes govern HOW placements are
made and validated, never WHOSE target wins.

Joint-episode picture: A's and B's orthing episodes alternate on one
occurrence lineage; each actor's action creates the successor the other's
episode consumes (typed handoff edges); under Conflict, each episode's
route choice is also an attempt to steer the lineage away from the other's
target set. Draw states are successors in neither target set.

## 4. Destinations

- **Core formalization:** §5.3 there (multi-actor episodes over one
  lineage; the definitions above; explicitly derived, not a new
  addition). Integrated.
- **Terminology benchmark:** a multi-actor fixture — a scenario where the
  arm must keep apart: shared occurrence / actor-relative target /
  current profile / objective / policy / metaorthemic distinction. The
  source notes become the NEGATIVE calibration example for
  objective-vs-metaortheme-vs-policy conflation (joining the standing
  objective-mislabeled-as-metaortheme example). Integrated into the
  designed (unrun) protocol.
- **Revised manuscript:** §10 worked example (chess) with C1–C6 corrections
  — present in `orthemma-ortheme-systems-revised-draft.md`.
- **Operational product lane:** **no new issue.** After ordinary-language
  translation ("two agents with opposed success criteria acting on one
  artifact") no product invariant emerges that identity, success-surface,
  and handoff governance do not already cover; competitive multi-agent
  execution is out of product scope. Default expectation confirmed:
  theory + benchmark only.

## 5. Status

Analytic note; no empirical claim. The multi-actor fixture is part of the
UNRUN terminology benchmark. Nothing here alters the six formal additions,
the verdict vector, or any product issue.
