# Erratum to the independently reviewed hard-name computation formula

8 October 2026 UTC. This separate correction leaves the original REVIEW.md,
REVIEW_RECEIPT.json, REVIEW_MANIFEST.json and every sealed payload unchanged.

## Location and correction

In REVIEW.md section 3, the paragraph headed “Computability of the hard names”
contains the transcription

    Q_N=u(1-b)+bu^(1/N).

The second term is missing a factor u. The correct formula is

    Q_N=u(1-b)+bu^(1+1/N)
       =u(1-b+b u^(1/N)).

Here u=1-a. If rational bisection encloses u^(1/N) in [lo,hi], the correct
enclosure for Q_N is

    [u(1-b+b lo), u(1-b+b hi)].

Since 0<=u,b<=1, its width is ub(hi-lo)<=hi-lo. Thus the stated rational-root
bisection computation and certified-approximation conclusion remain valid.

## Effect on the review

The author RESULT.md, the model derivation in REVIEW.md section 2, and both
the author and independent executable controls already use the correct
formula. The error is confined to this one explanatory transcription. It
does not change the mathematical verdict, hard family, uniform distance,
fixed-name argument, randomized argument, or controls and their reported
results. The original scoped PASS remains applicable together with this
erratum. No physical validation, integration, release or T20 closure follows.

ERRATUM_RECEIPT.json binds this correction to the frozen review, its original
receipt and manifest, and the already-correct author result and control scripts.
