# Restricted checker runtime comparison

This deterministic bounded comparison exercises the separately implemented Lean and Python checkers. It is not a formal refinement, parser correspondence, or proof of agreement on all inputs. The accepted generic Lean theorem and written fragment proof have their own scope.

The recorded run used Python 3.12.14 and Lean 4.19.0 on Linux. It tested 720 generated pairs at arities zero through five, including manufactured algebraic identities and independent random pairs. For each pair it compared the Python verdict with the Lean identity decision and generated-certificate verification, and checked a reflexive certificate. All 174 negative Python verdicts had an independently evaluated finite-grid witness. Direct evaluation also checked normal forms at small tuples. The receipt records counts and source hashes.

The observed run imported the already-built v4 research project. Its restricted Lean modules and Python source are byte-identical to their copies in proof v5. This is runtime evidence on those exact sources; it is not a cold dependency rebuild or a separate proof-v5 runtime replay.

From the outer evidence root, after building the proof package, run:

    python3 -B restricted-runtime/check_runtime_agreement.py python-reference/certificate_checker.py .runtime-check
    ROOT=$(pwd)
    (cd lean && lake env lean "$ROOT/.runtime-check/RuntimeAgreement.lean") > .runtime-check/lean-output.txt 2>&1
    python3 -B restricted-runtime/check_runtime_agreement.py python-reference/certificate_checker.py .runtime-check --verify-lean

Require the Lean command to exit successfully before accepting the final verifier result. Generated cases, Lean expressions and runtime output are local replay products. The supplied generator and recorded receipt contain no external source dataset.
