# Seven-rule constructor-square design

Approved parent scope: an independent source-AST checker for the actual seven Python proof rules, including explicit reduction traces and ordinary refusal branches, and a proof that successful outputs agree in both term and type with the inherited Cert checker after the actual exporter erasure.

Representation: TypeCode and Term encode the exact validated tagged Python tuples; SourceProof encodes validated dictionary shape with i/k/s/app/all_i/all_e/reduce. Reduction stores the explicit source List Term, not merely its length. The source checker never calls the inherited Cert checker or examines an encoded Cert to decide acceptance. Export erasure separately translates rules and expands reduce to trace.length-1 Cert.step wrappers exactly as proof_export._cert does.

Proof stages:
1. Prove the independent Python-pattern head-step function agrees with certifiedHeadStep on successful steps (and refusals).
2. Prove the explicit trace validator agrees with repeated Cert.step checking, conditional on the separately checked initial source proof.
3. Prove seven-rule checker correspondence by source-AST induction. Check successful result and exact output term/type, derive inherited checked_sound.
4. Keep typed AST validity, raw JSON parsing, CPython behavior and exact runtime resource policies visible as separate boundaries; add resource refusal refinement explicitly rather than removing guards or claiming universal Python correctness.
5. Preserve concrete cross-language runs as independent finite evidence. Add negative source-AST cases (wrong scope, application mismatch, empty/wrong-start/invalid trace, nonpolymorphic all_e). Add nonvacuous positive self-instantiation and reduction controls. Never introduce sorry, axioms or native_decide.
