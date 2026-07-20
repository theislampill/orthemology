# Worked case: sensory aliasing (identical observation, consequentially distinct states)

**Status:** public case note (Decision 0015). Analytic; no empirical claim. Deterministic fixtures: LS-1…LS-7 in `tests/latent-state-fixtures.json`. Notation follows `docs/notation-registry.yaml`; verdicts follow `docs/verdict-registry.yaml`.

## 1. The pattern

A system must act on a situation whose **current observation does not distinguish it** from other situations that require different action. A corridor inspector stands in one of four visually identical stretches of grey wall; a technician reads a gauge display that is identical in two different valve configurations; a log parser sees a line that is byte-identical whether emitted before or after a checkpoint. The observation is honest and correctly read. It is simply **not injective**: the map from situations to observations collapses cases that the task must keep apart.

Nothing here is a perception failure. The failure mode is a **typing** failure: treating "what I currently see" as if it were "which case this is."

## 2. The typed objects, one by one

Fix a declared analysis `A`, versioned, with its task, level, and tolerance stated.

**Orthemma `m_t`.** *This* encounter, at *this* time, in *this* stretch — a concrete, situated, time-indexed occurrence. Not "grey corridor" (that is a description), not "state 3" (that is a model label). The orthemma is the case itself; two passes through the same stretch are two orthemmata.

**Observation `x_t = Ω_A(m_t)`.** The currently visible ambiguous region: the grey wall panel, exactly as it presents now. `Ω_A` is declared and **non-injective** here — four distinct orthemmata share this observation. That non-injectivity is a fact about the declared observation map, not a defect in the observer.

**Candidate latent states `C^latent_t ⊆ Z_A`.** Under a declared latent layer, several hidden states are consistent with `x_t`: `{z_A, z_B, z_C, z_D}` — the four stretches, model-internally. This set is **plural on purpose**. It is not a profile, not a placement, and not ground truth. It stays plural until sequence or context evidence arrives (which stretch was entered from, how long since the last landmark, what the last cue was). The latent labels are indices in a fitted model, meaningful only inside that model and version.

**Orthemic profile under `A`.** The evaluable fact is `O*(m_t; A)`. The episode's local product is the **inferred partial profile** `p̂_t(m) ∈ Π_A^∂` — partial precisely because the observation underdetermines it. If the task requires the distinction, the episode may not flatten `p̂` to a single placement while candidates remain plural; if the task does **not** require it (Decision 0015 §2 admission test fails), the residual latent ambiguity is orthemically inconsequential and the episode closes without it.

**Metaortheme `μ` (the repeatable governing type).** *Aliased observations must be disambiguated using sequence/context evidence before a distinction-dependent placement is asserted; where disambiguation is unavailable, the candidate set is carried forward plural and the dependent claim is withheld.* This is a repeatable standard: it governs every aliasing case of this kind, in this corridor and in others, this week and next. It is a **type**. It has a version. It is not the corridor, not this run, and not the configuration used tonight.

**Metaorthemma `μ̄` (the case-bound configuration token).** Tonight's binding of that standard — **and only because the M1 material-binding criteria are met**: there is a material case-specific binding, a non-default scope, instrument provenance, and an independent validity condition. It records:

    μ̄ = ⟨ id, lineage;
           MetaInst(μ̄, μ) with (μ, ver(μ));
           (A, ver(A)) with Compatible(μ̄, A);
           model identity + version           (which fitted model, which fit);
           transition/emission mapping        (the P_A(z′|z,a) and Ω_A actually used);
           history window                     (how many prior steps count as context);
           inference threshold                (the posterior mass at which plurality collapses);
           validity interval                  (from when to when this binding holds);
           claim scope                        (which claims in 𝒬 depend on it);
           binder + binding warrant           (who bound it, under what authority)
             — kept DISTINCT from the executor;
           binding time; expiry/supersession ⟩

Had none of these been material — a default window, a stock threshold, no independent validity condition — the **M1 zero-burden rule** would apply: no token, and `GOV_TOKEN_ADEQUATE` (V3c) recorded not-applicable with reason. Binding a token merely because a mapping exists is a typing error (Decision 0015 §5).

**Execution.** The event of actually running the inference: reading the history window, propagating the belief `b_t(z)` under the bound transition model, comparing to the bound threshold. Execution fidelity is **whether the executor did what the bound configuration says** — it is scored independently of whether the binding was any good, and independently of whether the answer came out right.

**Placement.** The resulting profile claim: `p̂_t(m)` asserted at the governed level and tolerance, with its scope and its dependence on `μ̄` recorded. If the belief never crossed the threshold, the correct placement is the partial one, and the distinction-dependent claim is **withheld** — withholding is a placement, not a failure to place.

**Episode `e`.** The complete auditable run: this orthemma, this observation, this candidate set, this bound token, this execution trace, this placement, this closure — with its pathway verdicts, its burden ledger, and its residuals.

## 3. What the typing buys

- **Binder vs executor.** The person who chose tonight's history window and threshold is not the process that ran the inference. A wrong window with a faithful run is `GOV_TOKEN_ADEQUATE` fail / `EXECUTION_FAITHFUL` pass — the corridor was mis-set-up, not mis-walked. Collapsing the two hides which one to fix.
- **Type vs token.** The standard "disambiguate aliased observations by context" survives tonight; the binding does not. Revising the threshold revises a token; revising the standard revises a type; the two changes have different blast radii and different audit trails.
- **Plurality is a result.** A candidate set that stays plural is the correct output of a correct run under an underdetermining observation. An episode that collapses it to satisfy a caller has substituted an executor's convenience for the world.
- **No label transport.** If the model is refit, or `A` re-versioned, `z_B` in the old fit and `z_B` in the new fit are unrelated names (Decision 0015 §3). A claim asserted about the first does not transport to the second without re-establishment (§6).

## 4. Where this is checked

`tests/latent-state-fixtures.json` encodes the case family: LS-1 (consequential aliasing — candidates stay plural), LS-2 (safe merge — a model-state difference that forces no new ortheme), LS-3 (high performance without global orthogonalization), LS-4 (same endpoint, different trajectory), LS-5 (new cue rebound to an existing state), LS-6 (perturbed environment — inferred state is not ground truth), LS-7 (continuous-cell negative control). `scripts/validate_latent_state_fixtures.py` additionally fails closed on any fixture that asserts one of the identities Decision 0015 forbids.

## 5. What this example does *not* need

No neuroscience, no experimental procedure, no claim about any substrate. The pattern is fully specified by a non-injective observation map, a declared optional latent layer, and the framework's existing type/token discipline. (The pattern was *motivated* by reading a neighbouring modeling literature; see `docs/related-work/LATENT-STATE-INFERENCE-AND-ORTHEMOLOGY.md`, which is related work only — nothing in this note depends on it, and nothing in it validates this note.)
