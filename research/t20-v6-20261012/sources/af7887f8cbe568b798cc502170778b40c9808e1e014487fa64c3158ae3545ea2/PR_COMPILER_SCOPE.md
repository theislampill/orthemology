# Structural primitive-recursive compiler

## Checked result

Eight new modules contain 44 individually checked declarations, freshly built with Lean 4.19.0 and the previously pinned Mathlib. All declared axiom footprints are contained in propext, Classical.choice and Quot.sound. Positive controls compile; false claims obtained by omitting recursion-order adapters or substituting the wrong parameter literal fail by kernel reduction.

The main theorem P02A2.PRDerivation.compile_correct states that for every arity-indexed finite derivation tree d and every argument vector, the generated concrete LOOP program denotes exactly meaning d. The explicit syntax has zero, successor, projection, finite composition, and primitive recursion constructors. The compiler recursively emits the retained ObserverCore Expr/Stmt grammar. There is no evaluator/oracle constructor, arbitrary semantic-function constructor, fuel assumption on LOOP execution, or admitted simulation axiom.

PRProgram proves reset fresh-block calls. PRComposition preserves source inputs and distinct component-result buffers before applying the outer function. PRRecursion verifies the source-style last-argument recursor using actual snapshot-bound loops, preserving parameters and maintaining the accumulator. PRHeadRecursion supplies two verified input-order adapters to match Mathlib's first-argument Nat.Primrec' convention. PRDerivation composes these into the structural compiler.

PRCoverage proves that every fixed Mathlib Primrec finite-arity function has an extensionally equal derivation and hence an actual LOOP program. This is an existence theorem, not an extractor from erased Prop proofs. The separately defined compile function is executable on explicit derivations. PRSpecialize embeds a natural parameter as a concrete literal in a fixed program's argument list and proves the resulting finite syntax computes its exact section.

## Source relationship

The unchanged expression/statement semantics are the recovered P02-L1 grammar. The new macros have the same ordinary composition and recursion principles as recovered prcodec.py, but use fresh consecutive range blocks based on the checked program bound. They are not claimed to use the Python Builder's exact sorted-register allocator or identical bytes. This allocator change does not alter the previously sealed CandidateSource/compile_sigma2 AST comparison, whose files remain unchanged.

Recovered prcodec.py SHA-256: dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c.

## Boundary

This closes the explicit fixed-arity PR-derivation-to-LOOP semantic coverage gap. It does not alone prove serialization/parser correctness, a formal numeric-index many-one reduction, a uniformly primitive-recursive universal interpreter, the complete hierarchy membership theorem, or any novelty/adoption claim. Byte/numeric codec work is a separate post-seal extension.
