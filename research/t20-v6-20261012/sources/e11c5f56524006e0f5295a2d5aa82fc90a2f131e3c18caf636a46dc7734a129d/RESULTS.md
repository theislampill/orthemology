# P01 recursive, Curry and finite-effect successor

This is new research built on the repaired P01 shadow. The original 507-file checkpoint and the qualified repaired source remain unchanged.

## Main advance

The predecessor stopped at generic ParamFamily and AllFormation interfaces. This successor constructs the actual recursive interpretation of the frozen finite TypeCode syntax and proves its identity extension, renaming/substitution and fundamental theorem for all seven FiniteDerives rules.

It also proves parametricity of the original Curry-System-F Has judgment under related open valuations. The finite SKI compiler's abstraction rule is validated in typed PER equality, with both endpoint obligations proved. The proof does not reflect target beta equality into raw Conv.

## Finite probabilistic advance

A finite product seed chooses each mixture branch through a Fin den coordinate and gives application children independent coordinates. The same seed is shared between compared runs. Quantitative proofs establish exact support, total mass, mixture weights, product sampling, both coupling marginals and finite support.

The common-coupling theorem constructs its matrix before quantifying over relation environments. The original closed EffectDerives/MExpr language has a literal embedding and a common-coupling theorem with no input-valuation premise. Relation-respecting observations give exactly equal observed distributions.

A concrete fair-mixture example shows the left run returning I with probability 1, while the right returns I and S K K with probability 1/2 each. The coupling puts mass 1/2 on (I,S K K) and is valid for every relational environment at the polymorphic identity type. The raw laws differ, while every permitted respectful observation agrees.

## Key sources

- sources/P01RecursiveModel.lean: recursive model, IE, substitution, all-seven-rule fundamental theorem
- sources/P01RecursiveAssertions.lean: explicit load-bearing theorem contracts
- sources/P01CurryParametricity.lean: open valuations, lambda compilation and genuine Has parametricity
- sources/P01ModelWitnesses.lean: nonvacuity, legal self-instantiation, forbidden fixed-context allI, marker exclusion and I/S K K boundary
- sources/P01EffectSeeds.lean: finite seeds, literal original-language embedding, exact Outcome support and shared-seed relational theorem
- sources/P01FiniteCoupling.lean: rational pushforwards, finite support, normalization, marginals, common witness and observed-law equality
- sources/P01EffectMass.lean: exact pure, mixture and independent application mass laws
- sources/P01CouplingWitness.lean: concrete non-diagonal coupling and unequal raw distributions

## Evidence and limits

The authoritative receipt is qualification-v4/QUALIFICATION.json. It reports KERNEL_VERIFIED_SCOPED_P01_SUCCESSOR with kernel_credit=true for all 151 declarations across eight modules, plus a fresh audit artifact. The declaration kinds are {'abbrev': 1, 'structure': 2, 'theorem': 107, 'def': 37, 'inductive': 2, 'instance': 2}. These are 151 declarations, not 151 new mathematical theorems. The exact observed axiom union is propext, Classical.choice and Quot.sound.

The final declaration/type/axiom readback SHA256 is e33d31c10fd4cc5dd55630ca0b570f8241103b1f708761af9e951912d9639d26. The receipt also binds the exact qualification-driver and compiler binary hashes, parent artifact hashes, source bytes and output artifacts.

Use this final qualification receipt, exact readback and source manifest included in the package. Earlier qualification-v1 and qualification-v2 receipts cover their explicitly smaller source sets only.

All work uses Lean 4.19.0 (commit 6caaee842e94) and Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. Imports from the repaired checkpoint are bound to its successful strict-0004 receipt and all 31 artifact hashes. The approved axiom ceiling remains propext, Classical.choice and Quot.sound.

This is not the full dependent recursive relational model, a general Hall/max-flow theorem, a total frontend refinement, canonical adoption, or a claim of novel mathematics. Read REMAINING_OBLIGATIONS.md for the exact boundary and proposed next decision.
