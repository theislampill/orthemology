# Worked case: the stale steer (recovered directive without current force)

**Status:** public case note (Decision 0006). Analytic; no empirical claim. Deterministic fixture: F6 in `tests/verdict-fixtures.json`. Notation follows `docs/notation-registry.yaml`; verdicts follow `docs/verdict-registry.yaml`.

## 1. The pattern

A long-running system loses part of its working context (a summarization/compaction step, a crash, a handover) and then *recovers* an earlier governing instruction — from a transcript, a log, a cached record. The recovered instruction is genuine: it really was issued, by the right authority, and the recovery is textually faithful. The system follows it. Everything about the execution is diligent — and the outcome is wrong, because the instruction had been superseded after it was issued and before it was recovered.

The pattern generalizes far beyond software agents: a nurse follows a medication order that was countermanded on a later ward round; a contractor builds from a superseded drawing revision; a deployment gate enforces a rollback directive the incident channel already lifted. In each case the failure is not forgery, not misreading, and not disobedience. It is a **currency** failure on the governing side.

## 2. The directive record

Model the directive itself as a first-class record:

    d = ⟨ id;                 which directive this is
          version;            which edition of it
          issuer/authority;   who issued it, in what role
          warrant;            under what authority it was issued
          scope;              what cases, components, and time it governs
          issued-at;          when it was issued
          effective-from;     when it begins to bind
          effective-until;    when it lapses (if declared)
          supersedes;         earlier directives it replaces
          superseded-by;      later directives that replace it (filled in later)
          recovery-provenance ⟩  how THIS copy of it reached the present episode

## 3. Five predicates that must not be collapsed

For a directive `d`, an episode `e`, and a time `t`:

| Predicate | Question | Typical evidence |
|---|---|---|
| `Exists(d)` | Was such a directive ever issued at all? | the issuance record |
| `Authentic(d)` | Is this record a faithful copy of what was issued? | integrity/provenance of the copy |
| `Recovered(d)` | Did this episode obtain the record through a declared recovery channel? | the recovery-provenance field |
| `Authorized(d)` | Did the issuer have the warrant, in scope, to issue it? | the warrant and role records |
| `InForce(d, e, t)` | Does `d` currently bind episode `e` at time `t` — within scope, past `effective-from`, before `effective-until`, and **not superseded**? | the supersession chain and the current governance state |

Each predicate can hold without the ones below it. The stale-steer case is exactly:

    Exists(d) ∧ Authentic(d) ∧ Recovered(d) ∧ Authorized(d) ∧ ¬InForce(d, e, t)

Existence, provenance, authorization, scope, and current force are **different claims**, and evidence for one is not evidence for another: a perfect hash of the transcript establishes `Authentic(d)` and nothing else. In particular, **context compaction or transcript recovery does not by itself restore current governing force** — recovery affects `Recovered(d)`, which is orthogonal to `InForce(d, e, t)`.

Supersession is itself governed: a later explicit correction by the issuing authority supersedes the earlier instruction (`superseded-by` is filled), and from that moment `InForce` fails for the old edition even though every other predicate still holds — an authentic directive may be **authentic evidence of an earlier instruction** and simultaneously **stale as governance**.

## 4. How the verdict layer sees it

When the episode binds `d` as a governing token — a metaorthemma `μ̄` whose binding map points at the directive edition actually applied — the existing machinery covers the case with no new primitive:

- **`EVIDENCE_CURRENT` (V2c) fails** for the load-bearing claim "this directive is the current governing instruction": the evidence (the recovered copy) is valid *about the past issuance* and stale *about present force* — evidence about a different occurrence-version, exactly the framework's currency discipline applied to governance;
- **`GOV_TOKEN_ADEQUATE` (V3c) fails**: the bound token is not `Current(μ̄, t(e))` — correct general standard, defective case-specific binding to a superseded edition;
- **`EXECUTION_FAITHFUL` (V3d) passes**: the executor did exactly what the bound instruction said — *a system following a stale but authentic directive executes faithfully under a defective governing token*, the framework's clean separation of executor fidelity from binding adequacy;
- **`EX_ANTE_JUSTIFIED` (V3e)** turns on whether, at decision time, a supersession check was available and required — a recovered directive with a declared recovery channel and no currency check may still fail V3e where governance requires re-validation after recovery;
- **warrant-state classification (the `W` governed component)** is implicated: "was authorized (then)" must not be laundered into "is authorized (now)";
- **route selection (V4a)** is implicated when the stale directive selects the route;
- **`CLOSURE_TRUTHFUL` (V5) fails** if the episode closes with the claim that it acted under current instructions.

Fixture **F6** encodes the core of this: `EXECUTION_FAITHFUL` pass, `GOV_TOKEN_ADEQUATE` fail, `EVIDENCE_CURRENT` fail, `CLOSURE_TRUTHFUL` fail ⇒ `PathwayDefective`, with `RESULT_CORRECT` fail on the "directive-in-force" claim. The lucky variant (the superseded directive happens to coincide with the current one) lands in the correct-result/defective-pathway cell already witnessed by F4.

## 5. What the example does *not* need

No private transcript, session identifier, or project-internal detail is required to state any of this; the pattern is fully specified by the directive record and the five predicates. (The pattern was *motivated* by an internal engineering record; that record is private, and nothing in this note depends on it.)
