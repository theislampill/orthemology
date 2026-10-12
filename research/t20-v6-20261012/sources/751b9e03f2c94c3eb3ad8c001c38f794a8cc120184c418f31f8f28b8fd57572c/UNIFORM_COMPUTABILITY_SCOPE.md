# Unconditional computability of the actual numeric observer evaluator

## Exact endpoint

The 17 new modules contain 119 public theorem targets, freshly compiled and individually type/axiom audited at Lean 4.19.0 and pinned Mathlib. The baseline passes and three false controls are rejected. Every footprint is contained in propext, Classical.choice and Quot.sound. Receipt: receipts/uniform-computability-20260930T170750Z/UNIFORM_COMPUTABILITY_RESULT.json, SHA-256 a1a4e7be49c31d703543db5e1252a04cac74ca8eddc544146761bb95de67deea.

P02.Codec.UniformComputability.evaluateIndex_computable states, without an effectivity or termination premise, that the sealed P02.Codec.evaluateIndex is Mathlib Computable jointly in its natural index, stage and sentinel-word input. evaluateIndex_nat_computable gives an explicit external Nat-to-Nat theorem: input z is decoded as index z.unpair.1, stage z.unpair.2.unpair.1 and word z.unpair.2.unpair.2. Both domains and the result use the standard natural-number representation.

The proof discharges the earlier operational stage's conditional premise. It does not assert that the unbounded universal evaluator is uniformly primitive recursive. The bounded stack evaluator and complete syntax decoder are primitive recursive; exact unbounded evaluation is obtained by the proved terminating fuel search.

## Actual representation and decoder chain

Explicit constructive bijections encode the unchanged Expr, Stmt, Task and PackedProgram types as natural numbers. Expr uses radix-ten constructor tags and paired child codes. Stmt uses zero for skip and four tagged positive cases with paired natural fields and child codes. Task and PackedProgram use explicit natural pairings. Each encoding has both roundtrip theorems and declared Denumerable/Primcodable instances. Constructor, projection, expression-evaluation and transition proofs use those exact instances.

These internal Mathlib representations do not replace the wire format. The old P02-L1 magic/version, unsigned varints, expression/statement tags, arbitrary variadic sequences, output register, arity check and sentinel base-256 numeric envelope are unchanged. The new effectivity proofs name the existing uvRead, readExpr, readStmt, decodeBytes and decodeIndex definitions directly.

The varint proof uses an arithmetic cursor simulation under the real accumulator invariant, preserving truncation, byte-domain rejection and the final canonicality check. Expression and statement parsers are handled by finite tables containing every suffix of the original stream. Successful parses are proved to return a suffix; table lookups therefore replay exactly the prior-fuel parser. Arbitrary fuel and arbitrary natural-number byte lists are covered, including failures and exact unread suffixes. No generated-code or well-formedness premise is introduced.

The variadic sequence parser uses an independently proved forward iteration with reversed child accumulator, equivalent to the original readMany. None propagates. Both expression children and sequence children use the original shared predecessor fuel, not a substituted global remaining-fuel model.

## Operational connection

The exact finite-register/task stack has the previously sealed soundness, total eventual completion and fuel-monotonicity proofs. The new syntax representations make its actual step and runFuel primitive recursive. The actual sealed decoder is composed with those functions to prove evaluateIndexFuel primitive recursive jointly in all natural inputs. The existing evaluateIndexSearch_exact and Partrec fuel search then prove the unconditional universal Computable result.

Malformed syntax and nonbinary arity keep their specified semantic zero. Exhausted transition fuel remains none and is never assigned zero. The proof does not identify its transition count with Python Meter.steps or certify Python stack, memory, timing or resource exceptions.

## Remaining boundary

This closes the previously explicit formal uniform-evaluator Computable gap. It does not itself certify the variable-depth finite-word enumeration, rational heavy sum and exact AtomicMembership.membershipMatrix as a uniform Computable predicate. That concrete successor is separate from the already sealed measure/normal-form identities. No broad formal arithmetical hierarchy library, novelty, or canonical-adoption claim is added.
