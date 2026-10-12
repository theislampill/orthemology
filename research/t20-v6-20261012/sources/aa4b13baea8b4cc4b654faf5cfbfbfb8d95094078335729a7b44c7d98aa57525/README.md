# Independent fibrewise split review

Disposition: PASS within the stated scope. Read REVIEW.md first. Author payload and reviewer evidence remain separate; no protected integration or programme closure is authorized.

## Replays

Requires Python 3, SymPy, NumPy, SciPy; author verification additionally uses mpmath. From this review directory, with the frozen author directory as its sibling:

    python3 check.py --output private-locator:e5bdeb04ed4ee617a198
    python3 -O check.py --output private-locator:ec503e28ddb2a0c2c095
    python3 implementation_controls.py --author-dir ../fibrewise-split-correction-20261011 --output private-locator:bb5c0d9aadb106bb9eff
    python3 -O implementation_controls.py --author-dir ../fibrewise-split-correction-20261011 --output private-locator:ed6cf44856d05d5d6ef6
    python3 verify_bindings.py --author-dir ../fibrewise-split-correction-20261011 --output private-locator:9937b3c7aae0470188cd

The independent mathematical script imports no author/root checker. The implementation script imports the frozen implementation itself and compares it with separately generated examples. Bindings check all 31 author-manifest files, the manifest digest, copied predecessors, and key identities. Add --original-root /path/to/original/workspace only when those original reports are available.

Author replay uses fresh, nonexistent output directories:

    python3 ../fibrewise-split-correction-20261011/verify.py --output-dir private-locator:cf0378afda97359a450b
    python3 -O ../fibrewise-split-correction-20261011/verify.py --output-dir private-locator:9fbfe6a13a7c8fde1108
    python3 -m unittest discover -s ../fibrewise-split-correction-20261011 -p test_gaussian_step.py -v
    python3 -O -m unittest discover -s ../fibrewise-split-correction-20261011 -p test_gaussian_step.py -v

Recorded author replay includes five optional original-workspace checks; portable replay without them has 60 rather than 65 checks.

IMPLEMENTATION_FINDING.json retains the independently reproduced complex-array rejection defect, pre-fix hash, resolution, and frozen fixed hash. It must not be omitted from preservation.

SOURCE_READING.json records bounded independent primary-source access and supplementary inspection of the preserved v3 source. Exact splitting, normalized power reaction, and Gaussian updates are credited to prior literature. No PDE-limit/existence theorem, universal finite computation, field-priority, formal proof, or empirical-target warrant is claimed.
