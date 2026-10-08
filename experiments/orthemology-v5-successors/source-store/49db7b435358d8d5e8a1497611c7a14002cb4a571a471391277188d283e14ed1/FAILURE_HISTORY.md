# Preserved failure history

1. The author's initial neutral implementation failed the anchored-cycle test as expected. AUTHOR_INITIAL_RED.txt preserves that assertion failure, with only the executor prefix normalised. The independent review preserved the log without independently certifying its chronology.
2. The independent review's evidence checker initially confused a sibling output directory with the source directory because it used textual startswith rather than resolved path containment. The initial output, two-case diagnosis and passing recovery output are retained. This was a review-harness failure, not a proof failure.
3. The first portable packaging runner invoked Lean from a separate output directory without setting Lean's source root. Lean rejected the input location before checking GroundedSupport. PORTABLE_WRAPPER_INITIAL_FAILURE.txt preserves that failure with neutral path placeholders. The corrected wrapper supplies --root for the sealed source package; its later verified result is separately recorded.

No failed attempt receives successful rejection credit for a mathematical conjecture. The six reviewed scientific modules were not changed for any packaging repair. Raw historical originals remain bound by the projection map and review evidence hashes; private executor paths and compiled objects are excluded.
