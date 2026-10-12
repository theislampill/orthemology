# Explanatory warrant continuation

Read REPORT.md for the current scientific result. REPORT.first-pass.md is preserved development history and contains the actual-relevance and seed-originality overclaims corrected in the current report, §§4a–4c. It is not a current conclusion.

- ExplanatoryGeneration.lean: candidate-rule generation semantics and initial controls
- ActualUseControls.lean: actual-used positive-path/receipt guards; dormant original route and actual supply into a seed
- IntegratedConsumers.lean: direct application of the repaired interface to both independently owned controls
- provision_join.py and test_provision_join.py: read-only adapter to the provision/identity lane's executed proof records
- JOINT_INTERFACE_RESULTS.json: shared resource/act/contribution/event interpretation
- ../explanatory-review/: independent same-bearer productive/nonproductive controls and stronger beginningless-history tests, owned by the reviewer
- VERIFICATION.json: check scope, hashes, and source bindings

The original-resource predicate of the abstract generation model is a designated seed predicate. Whole-existence originality, actual productive use, receipt completeness, and source-mode perfection require their separately stated semantic/application premises. Neither mathematical solution selection nor a source label supplies them.

Replay with the existing pinned compiler, without downloads:

    PREP=../../hase-positive-research/toolchain-preparation
    LEAN="$PREP/toolchains/lean-4.19.0-linux/bin/lean"
    mkdir -p replay-output
    "$LEAN" --trust=0 -j1 -o replay-output/ExplanatoryGeneration.olean ExplanatoryGeneration.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 -o replay-output/ActualUseControls.olean ActualUseControls.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 Readback.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 ActualUseReadback.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 -o replay-output/ActualProvisionReview.olean ../explanatory-review/ActualProvisionReview.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 -o replay-output/BeginninglessProvision.olean ../explanatory-review/BeginninglessProvision.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 -o replay-output/IntegratedConsumers.olean IntegratedConsumers.lean
    LEAN_PATH="$PWD/replay-output" "$LEAN" --trust=0 -j1 IntegratedReadback.lean
    PYTHONDONTWRITEBYTECODE=1 python -m unittest discover
    PYTHONDONTWRITEBYTECODE=1 python provision_join.py

The adapter requires the adjacent provision-identity/src/provision_semantics.py and reports its hash. It does not modify that source. There is no archive integration, public adoption, new package, or tranche closure here.
