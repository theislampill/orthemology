# PMR-007 Deep Round F V1 cold audit

## Frozen input

The V1 theorem, model, checker, and result bytes were frozen before this audit. This is a same-session procedural cold audit, not external human review or independent model-lineage confirmation.

## Disposition

```text
REPAIR_REQUIRED
```

## Blocking finding FPF-F01 — proper function, episode success, and warrant were conflated

V1 defines one conjunctive predicate `NPF_T` containing:

```text
source/design/end/health/operation/environment
+ output accuracy
+ undefeated warrant
```

It then calls this a proper-function success predicate. That loses the exact distinction the program requires among:

```text
proper functional constitution and operation;
episode-level success;
and epistemic warrant or undefeatedness.
```

A properly functioning truth-directed faculty may issue a false output in a difficult case without thereby losing its proper function. Conversely, a lucky accurate output can lack proper operation. Warrant introduces further defeater and environment conditions. The theorem must therefore be split into at least three typed levels.

Required repair:

```text
NFunc_T:
  source-relative truth-directed proper functional operation

NAcc_T:
  NFunc_T plus episode-level accuracy

NWarr_T:
  NAcc_T plus undefeatedness / warrant custody
```

The deletion tests must target the appropriate level rather than treating all eight guards as minimal for one predicate.

## Nonblocking finding FPF-N01 — conditional closure is definitional

The source-relative closure is a contract expansion, not independent mathematical evidence. It may be admitted only as source-formal premise decomposition with zero general novelty and no neutral theorem credit.

## Nonblocking finding FPF-N02 — selected-effect parity is theory-relative

The selected-effect rival supplies a proper-function account only if the selected-effect theory is accepted and its history is established. The packet must not say neutral operational data prove that account either.

## Nonblocking finding FPF-N03 — source authority ceiling

The source materials are a secondary scholarly reconstruction and a contemporary Atharī synthesis. No Arabic-primary wording, source truth, or external specialist confirmation follows.
