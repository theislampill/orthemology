# Independent review dispositions

The independent reviewer checked the arbitrary finite analysis and froze the
four core files: RESULT.md, THEOREMS.md, src/robust_masks.py and
src/test_robust_masks.py. All eleven author control groups pass.

The review independently verified forty guarded multi-effect models over 1,600
probability coordinates using endpoint-law convolution and combined calibration
and sampling perturbations. Three independent rational-interval groups also
pass. Its separate fixed-mask lower-bound controls cover 234 parameter pairs.
These are assurance counts, not empirical trials or additional discoveries.

The float-acceptance concern was substantive for the word certified. It was
reproduced in EXACT_INPUT_RED.log, corrected by exact-rational input guards, and
verified in EXACT_INPUT_GREEN.log. Integer coordinate counts are also enforced.

The chosen series-width target is the conservative
p^(2r)/(64·2^r), with quotient endpoint error at most 5/64. The code derives a finite
required term count; it does not treat an arbitrary resource cap as a success
proof. The manuscript explicitly separates the numerical certificate from the
statistical good event and both from causal/source applicability.

The reviewer supplied the matching restricted-mask lower bound. Its general
proof was read here and the K>=2 and all-roots-active qualifications checked.
The independent receipt and frozen snapshots stay in the sibling review package.
No core edits followed that final review; subsequent exports and evidence
bookkeeping have separate hashes.
