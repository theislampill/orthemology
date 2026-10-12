# Actual candidate and Sigma2 AST compiler refinement

## Sealed scope

The 52 declarations in CandidateCompiler, CandidateSource, CandidateWitnesses and Sigma2Compiled were freshly compiled and individually type/axiom audited at the exact Lean/Mathlib pins. Receipt: receipts/candidate-20260930T150947Z/CANDIDATE_RESULT.json, SHA-256 2beddd3cab8712b85bfb908afc48b73ebaa4af2b5405d7cadc5a08f7e55086d7.

The proof is now about generated statements in the retained ObserverCore grammar. It is distinct from the previously sealed mathematical prefix-family result. It still does not verify Python execution, byte parsing, numeric indexing, or arbitrary primitive-recursive derivation coverage.

## Exact recovered comparison

Original file: private-locator:d8dc20b3e088111e6617
SHA-256: dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c
Outer checkpoint ZIP SHA-256: f90e399269ccd33c1df42b13c085f09d4e85ea6e2ecfd6f6ee9501de6671d0e2
Relevant functions: registers, Builder.inline, _candidate, compile_sigma2.

Both constructions collect source registers from arity-three inputs, designated output, every expression read and every statement write/loop index. CandidateSource sorts that finite set and allocates the fresh matrix-local registers as 11 plus their list index, exactly the first Builder.inline allocation in compile_sigma2. It resets every matrix-local register on every invocation, loads parameter/candidate/test in source registers 0/1/2, runs the renamed matrix body and copies its output to register 10. A universal theorem discharges the control block's matrix-value and caller-frame contract for this actual inlining construction.

The first candidate block has output register 3, saved stage 5, candidate index 6, test index 7, found flag 8, good flag 9, matrix result 10, and matrix locals starting at 11. It snapshots the stage, starts with default stage+1, scans candidate and test indices inclusively through stage, resets good for each candidate, and freezes the first success. The kernel proof derives its exact output as the least surviving candidate, with fallback stage+1, for every caller store and arbitrary stage expression.

The previous-stage block uses the next fresh base 11+registerList.length. Sigma2Compiled.secondMap preserves input registers, sends output 3 to 4, and shifts all first-block locals 5 and above to that fresh base. Its injection and execution correspondence are proved. Swapping the otherwise unused prototype register 4 back to 3 makes the map globally injective; register 4 is not used by the candidate prototype with the supplied stage expressions. Consequently the renamed block matches the source's second fresh allocation and stage expression n−1.

The complete construction resets previous to zero, runs that previous-stage block only when n is nonzero, resets output to zero, then copies word modulo two precisely when the candidate changed. Binary sequence/skip is the semantic normalization of the source's finite sequence lists; identical serialized bytes are not claimed.

## Strongest checked conclusions

For every fixed arity-three matrix body, designated matrix output, natural parameter and caller store, actual execution of the generated Sigma2 statement equals the explicit least-candidate innovation prefix function. The n=0 predecessor is exactly zero.

The actual fair-Cantor pushforward of that generated syntax therefore has positive-singleton defect zero iff there exists a candidate s whose matrix output is nonzero for every t. If no such s exists, every output singleton is null and the defect is one. The generated fixed binary prefix function is formally Primrec. This is a source-bound AST compiler theorem, rather than an inference from finite tests or a presumed simulation axiom.

## Negative controls

The baseline compiles. A version that tests only t<stage misses the inclusive upper test, returning 1 instead of 2 in a concrete matrix. A version that omits the found guard overwrites the first success, returning 2 instead of 0 for a constant-true matrix. The two asserted equivalences are rejected by kernel reduction as false propositions. Sort-normalization witness lemmas make the concrete source allocator reducible without native_decide or external evaluation axioms.

## Remaining hierarchy boundary

The recovered Python file contains the ordinary converse construction through zero, successor, projection, composition and primitive recursion. At this seal, Lean has checked fresh inlining and grammar-to-Primrec soundness, but not a constructive translator from a full primitive-recursive derivation presentation into the grammar. The byte/numeric codec also remains unverified. Thus this seal is not yet a certified numeric-index many-one reduction or full hierarchy-completeness theorem. The tagged countable-row law and its later compiler binding are separate from the Sigma2 row.
