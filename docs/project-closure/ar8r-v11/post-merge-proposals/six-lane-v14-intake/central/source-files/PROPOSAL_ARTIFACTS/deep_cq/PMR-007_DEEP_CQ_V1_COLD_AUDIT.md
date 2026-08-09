# Deep CQ V1 cold audit

## Disposition

```text
REPAIR_REQUIRED
```

## Blocking findings

### CQ-F01 — switching uncertainty was not sufficiently prominent

The fixed-point theorem is for an adversary allowed to select any live standard
at every step. That is stronger than one unknown but temporally fixed standard.
The title and conclusion must not silently cover both semantics.

### CQ-F02 — the reach-and-stay proof was absent

The V1 statement gave the nested fixed points but did not prove both directions,
the rank construction, or memoryless sufficiency at finite full-state scope.

### CQ-F03 — the fixed-unknown/switching checker witness was defective

The V1 checker’s automatic witness accepted a policy with an undefined action
at an irrelevant state and tested only nonempty singleton winning sets rather
than one common initial state. It is not authority for the claimed semantic
separation. Preserve the V1 result and replace this control with an exact
three-state witness.

### CQ-F04 — supplied targets are not proper-function truth

The finite `T_h` sets are candidate-standard targets. The theorem neither
identifies the correct function-fixing account nor establishes any target as
truth-linked, objectively fitting, teleological, or fiṭrī.

### CQ-F05 — robust simultaneity may be the wrong policy requirement

Requiring one route to satisfy all live rival standards is a conservative
safety contract. Rival standards may instead require adjudication. The theorem
must be framed as robust-to-unresolved-standard uncertainty, not as the unique
meaning of restoration.

### CQ-F06 — source-family restriction is conditional

The monotonic expansion obtained by deleting standards is formal. A
source-relative premise may shrink `H` only after source, translation, referent,
applicability, and world guards are independently warranted.

### CQ-F07 — action eligibility and dynamics are model inputs

The common-action intersection may be empty because of authorization, version,
capability, or semantics. The theorem does not show that the repository or daee
runtime actually enforces those maps.

### CQ-F08 — full observability and finite deterministic scope

The proof does not cover partial observation, hidden standard evidence,
dynamic membership of `H`, stochastic transitions, or infinite state spaces.

### CQ-F09 — relation to existing theorem families

The mathematical core is standard finite robust safety/attractor game
machinery and an application of T351–T354/Round-14-style restoration controls.
It receives zero general novelty.

### CQ-F10 — positive source and human-restoration overread

A nonempty robust kernel is a formal policy certificate. It is not source truth,
causal burden landing in a person, whole-field reread, uptake, or restored
fiṭrah.

## Required repair

- rename the result to switching-standard robust viability;
- provide both fixed-point proofs and the rank argument;
- replace the defective semantic countermodel;
- type target, source, implementation, and human-restoration ceilings;
- retain a fixed-hidden-standard distinction as an open different game;
- record standard ancestry and zero novelty.
