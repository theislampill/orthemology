# Independent review: bounded literal compile_shift trace audit

Status: PASS for the bounded scope below. The final frozen script was independently rerun in normal and optimised Python; all author bindings match.

## Target and protected-source identity

The target is the existing Python `compile_shift` in `user-checkpoints/extracted/P02/code/prcodec.py`, SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`. The audit imports that file by explicit path, without substituting a compiler. Its pin agrees with `rational-shift-realisation-20261011/ORIGINAL_SOURCE_BINDINGS.json`. This review writes only in its separate review directory. No compiler bug or repair is claimed.

## Independent inspection

- Compiler registers are j=3, found=4, branch=5, stop=6, value=7, den=8, tail_len=9, tail_word=10, answer=11. Source registers are sorted and allocated from 12. The expected trace uses this actual allocation correctly.
- The oracle computes exact rational dyadic cells using Fraction and an incremental prefix, rather than evaluating the compiler's multiplication/comparison expressions. It selects the first disjoint below/at-above cell and excludes the stopping bit from the suffix. This is a meaningfully independent semantic oracle for stopping and suffix selection.
- Trace expectations are deliberately implementation-specific for Set order and register allocation. Base execution, register enumeration, sentinel encoding, decoding, and interpreter execution use original runtime helpers. Thus this is differential evidence relative to those helpers, not an independent interpreter verification.
- `run(trace=True)` records Set statements only. Implicit LOOP counter updates are not recorded. “Full trace” must mean full Set-event trace, not every register write or instruction.
- Unresolved, below, and at-above stopping observations copy the current bit. Base evaluation occurs only for the at-above branch after a nonempty post-stop suffix exists; base index is suffix length minus one and the suffix gets its own high sentinel.
- Exact trace comparison checks every explicit source-local zero reset, argument assignment, renamed base Set event, answer capture and final parity assignment. A shift evaluation invokes the base once at most; it is not itself a repeated-inline persistence test.

## Novelty relative to the directly relevant prior tests

The existing `P02/tests/test_new_research.py` (SHA-256 `acfcc82dfcb45595c509e90c0a2341abd27e137321fa67671fe0991651befcbd`) already has a rational-cell reference oracle and compares complete six-bit output prefixes for five base observers at 0, 1/3, 1/2, 2/3, 1. It already checks stage parity, first suffix bit, whole-word sentinel correctness, and has a separate repeated-inline reset test for compile_pi3. Its historical surviving shift mutation was already repaired by strengthening a sentinel fixture; that is not a new finding here.

The present audit's increment is bounded internal Set-event observability (including output-invisible timing/sentinel/boundary/reset errors), broader base alias/scratch/high-register cases, exhaustive words of lengths 1–7 for every raw a/b with 1≤b≤8 and 0≤a≤b, unreduced-ratio trace comparisons, and selected much deeper boundary cases. It does not introduce the rational-cell reference method or first discover tail sentinel/reset requirements.

## Scope boundaries

Deep non-dyadic controls cover five particular cuts through depth 128 and two flipped-bit suffix neighbours per depth. Dyadic controls cover selected numerators at depths 1–32 and four suffixes. These are finite selected boundaries, not all cuts at those depths. Scaled ratios include a large 2^80+1 factor, but finite equality tests do not establish arbitrary-ratio equivalence. No probability law, infinite-stream theorem, primitive-recursive syntax coverage, Lean verification of the literal compiler, or repository adoption follows from these tests.

## Review feedback

The initial audit used Python assert for decisive checks, which disappear under optimisation. The author was asked to use explicit failures before final freeze. This is audit-harness hardening, not a compiler repair. The author was also asked to state Set-event and single-invocation limits accurately and demonstrate reset-omission sensitivity on a copied AST.

## Final verification

The frozen author script SHA-256 is `8e11ed8bcb0218c959f27299de97e83894e0c52e33bbbeb7dafd7b82fa210813`; author BINDINGS.json SHA-256 is `7e48d54fee0de5f6bc53e3de6205e086218768e817800e41937322b5f0b761b2`. Every bound author and inherited file was independently rehashed and matched.

An identical script copy in this review directory was run using `python -B check_literal.py` and `python -B -O check_literal.py` (paths rooted at this directory). Both exited 0, reproduced the author's exact JSON bytes, and checked 97,456 positive/equivalence cases: 89,408 exhaustive, 5,376 unreduced, 640 non-dyadic, 1,280 neighbours, 752 dyadic. All five copied-AST mutation controls had witnesses. Only the wrong-tail-index first witness changes output; reset omission, early invocation, sentinel omission and equality-boundary first witnesses are trace-only.

The final source has zero Assert nodes and explicit require calls at each of the five decisive check sites. `--false-check` exited 1 with the intended RuntimeError in both normal and optimised mode. This verifies that the explicit failure mechanism survives optimisation; source inspection confirms the oracle, unreduced, boundary, negative-witness and source-preservation checks use it.

The compiler source remains byte-identical to its inherited pin after all replays. The author preserved the earlier assert-based script as historical normal-only evidence and corrected Set-event/single-invocation wording. No remaining review blocker was found within the assigned bounded scope. The shared interpreter/helper dependence and unproved universal literal-compiler/infinite-law connection remain explicit limits, not failed tests or repaired defects.

Machine-readable replay details: REPLAY_RECEIPT.json. Guard inspection: GUARD_INSPECTION.json. Full independent normal/optimised and deliberate-failure logs and exits are preserved alongside their result JSON files.
