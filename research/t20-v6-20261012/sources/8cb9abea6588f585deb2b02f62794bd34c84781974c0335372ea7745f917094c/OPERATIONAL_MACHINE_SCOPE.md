# Faithful finite-register stack and eventual numeric evaluation

This stage freshly qualifies UniformComputabilityNumeric, UniformComputabilityMachine and UniformComputabilityControls: 35 named theorem targets, approved standard axiom footprints, a passing baseline and two rejected false controls. Receipt: receipts/operational-machine-20260930T164514Z/OPERATIONAL_MACHINE_RESULT.json, SHA-256 fa4de6b41560db7ae8306018a1a5d8739ff147f0a052f435c0e5b1d4566c5f30.

The actual minimal-byte and sentinel numeric decoders now have Mathlib Primrec certificates. This is a complete decoder-envelope result, not yet a complete program-parser certificate.

The operational interpreter stores natural register values in a finite association list and runs an explicit stack of statement/repeat tasks. Expression evaluation and finite-register execution are proved equal to the retained functional-store semantics. The loop count is captured once at entry; the current iteration index is written before each body. Overwriting the bound or index inside the body therefore has the specified behavior.

runFuel_sound states that every successful run agrees with the original semantics. runFuel_complete gives sufficient transition fuel for every finite statement and input. Successful results persist at all greater fuel budgets. The numeric evaluateIndexFuel uses the actual sealed decodeIndex; its corresponding soundness, completeness, monotonicity and eventual-value theorems hold for every natural index and input.

Invalid syntax or nonbinary arity returns some 0. Fuel exhaustion returns none. The exhausted_one theorem exhibits a semantic-one program whose zero-fuel result is none, preventing resource exhaustion from being silently assigned a semantic zero.

The unbounded search evaluateIndexSearch is exactly Part.some of the sealed evaluateIndex for every index/input. The theorem evaluateIndex_computable_of_fuel is deliberately conditional: a Mathlib Computable certificate for the numeric bounded machine would imply Computable for the actual universal evaluator. Its premise is not discharged by this stage. Uniform coding of syntax, parser computation and transition computation remain the specific next formal bridge.

Eight kernel semantic controls and 24 actual-numeric compiled execution vectors check captured count, overwritten index, natural arithmetic including zero divisors, both branches, zero loops, invalid codes and arity rejection. A fresh comparison reproduced all 24 vectors with recovered prcodec.py (SHA-256 dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c); zero resource budget raises its ResourceLimit as expected. The supplemental comparison receipt is receipts/OPERATIONAL_SOURCE_COMPARISON.json. Finite testing is not asserted as universal Python refinement.

Fuel counts statement/repeat transitions only. Expression arithmetic, decoding, memory and host resources are not metered by this fuel, so there is no equality claim with Python Meter.steps, bit bounds or host exceptions. No uniformly PR universal evaluator, full Python host implementation refinement, or complete formal hierarchy certificate is claimed. All prior seals remain unchanged.
