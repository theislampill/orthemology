# Executed evidence scope

`intake/input_verification.json` records initial verification. `intake/final_input_recheck.*` contains a fresh raw process result checking the original packet and all extracted preimages. Counts concern the supplied source/evidence subset, not a full Git tree reconstruction or current remote state.

`probes/tests_final16.*` and `probes/tests_optimised16.*` are the current 16-test runs. `probes/census_final.*` is the current bounded census; its stdout embeds the three probe source hashes and exact populations. Later `preseal_*` streams, when present, are fresh repeats on final code. The superseded 15-test runs and earlier census iterations remain evidence of what actually ran, not added test credit. `census_first_source.py` is a retained earlier census source. The first missing I-root implementation produced a genuine failing test in `preimplementation_root.*`; it is not an original canonical defect and receives no historical recovery credit.

`toolchain/lean419_release_headers.*` records the unsuccessful compiler acquisition attempt (DNS failure, exit 6). `toolchain/lean_version.*` records executable-not-found, exit 127. These new environment failures do not replace the accepted historical strict-wrapper FAIL. No compiler build, new kernel theorem or formal artefact is claimed.

All `.stdout`, `.stderr` and `.exit` files retain actual streams and exits. A zero-byte stream is an actual empty stream, not a proof artefact. `.command.json` files retain arguments, local working directories and timestamps as inert provenance; those paths are not instructions. The later qualification driver has not been run against Lean.

Seal-verifier tests and syntax checks, when present, concern packaging/handoff code only. They cannot establish a mathematical theorem or canonical-engine correspondence. The final archive is independently reopened by a fresh process after it is closed; its verification report is delivered outside the archive to avoid circular hashing.
