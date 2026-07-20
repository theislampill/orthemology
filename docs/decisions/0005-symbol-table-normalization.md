# Decision 0005 — Symbol-table normalization (D4)

**Date:** 2026-07-20 · **Decider:** Claude Fable 5 under the owner's standing autonomy mandate (R2 closure) · **Status:** implemented, registry-driven, machine-validated.

**Question.** A corpus-wide collision audit found several symbols carrying two unrelated roles: `G` (episode graph vs target profile set), `q`/`Q` (representation vs claim ledger), `W` (goal schema vs warrant repertoire), `ε` (metaortheme selector vs evidence-status map vs tolerance), `R*` (best risk vs route repertoire), `τ` (ANDON threshold vs generic time), and `App(e)` competing with `ReqPath(e)` as a pathway requirement function. What is the normative symbol table?

**Decision.** Adopt the registry in [`docs/notation-registry.yaml`](../notation-registry.yaml), enforced by `scripts/validate_notation.py`. Highlights (semantic roles control over glyph preference):

- `A` — declared analysis only; **actors are `α, β, …`, never A/B**;
- `𝓜, 𝓞` universal universes; `M_A ⊆ 𝓜`, `O_A ⊆ 𝓞` analysis-active domain/repertoire, with unsubscripted `M`, `O` licensed as scoped shorthand once one analysis is fixed (this keeps single-analysis prose readable while making the analysis-dependence of the domain explicit at the definition site);
- `Inst_A ⊆ M_A × O_A`; `O*(m; A)`; `Π_A` complete-profile space; `Π_A^∂` partial-profile space; `Ĉ_{A,α,t}(m)`/`C^profile` candidate complete profiles; `p̂_{A,α,t}(m) ∈ Π_A^∂`; `Ω_{A,α,t}` where indices matter;
- `μ`, `π_μ`, `μ̄_{e,j}`, `MetaInst(μ̄_{e,j}, μ)`;
- **episode DAG `Γ_E = (E, ⇝)`** (replacing the bare `G`), composed episode `e_Γ = comp(Γ_E)`;
- **`GoalSchema(α)`** (replacing the overloaded `W(·)`), target sets **`𝒢_{α,A_α}`** (replacing `G(α, T_α)`);
- `Rep_A`, one representation **`χ`** (replacing `q`), best attainable loss **`L_A*(χ)`** (replacing `R*(q)`);
- **`select_μ`** (replacing the selector role of `ε_μ`), **`estatus_e`** (replacing the bare `ε` evidence-status map), **`ε_A`** accepted tolerance, **`θ_stop`** ANDON threshold;
- `𝒦_A`, `ℛ_A`, `𝒲_A` cause/route/warrant repertoires (task-subscripted forms remain licensed scoped shorthand);
- `𝒬_e` claim ledger, `δ_e` residual-disposition map;
- **`App(e)` retired from normative use.** `ReqPath(e)` is the sole pathway requirement function; applicability is expressed through `ReqPath(e)` membership plus recorded per-verdict `not-applicable` reasons. (`App(e)` had been a discretionary-looking recorded set that could compete with the governance-derived requirement; nothing it expressed is lost.)

**Scoped-shorthand rule** (from Decision 0001, restated normatively): task-subscripted forms and unsubscripted `M`, `O` are licensed only after one analysis is explicitly fixed, and are forbidden in multi-analysis contexts.

**Consequences applied:** formal core, manuscript, multi-actor note, overview, glossary, schemas, fixtures, and validators. Historical documents under `archive/` retain old symbols and are never rewritten; the notation validator whitelists archive/history contexts.

**Non-decision.** No definition changed meaning; every rename is 1:1 role-preserving, recorded in the registry's `retired_symbols` list.
