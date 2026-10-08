# Verification guide

## 1. What each check establishes

The outer candidate assembles evidence. It does not replace any underlying proof or empirical replay and does not mark Sixteenth complete.

1. The independently supplied outer ZIP SHA-256 identifies this candidate's exact bytes.
2. `verify_bundle.py` checks the outer manifest's complete file census, file sizes and hashes. It verifies nested ZIP identities through those file hashes, inspects their safe member structure and checks their declared member/expanded-byte counts. It does not interpret each nested package's internal proof manifest or execute its source.
3. Each source package's own entry point checks its own internal locks. Its full replay, with the exact prerequisites, is a separate operation.
4. Detached author/independent receipts record earlier fresh executions of the exact accepted proof ZIPs. The outer integrity check is not another proof compilation.
5. Empirical source identity, synthetic code tests and full companion-validated analysis are separate checks. Each public receipt states its executed scope.

A hash verifies identity relative to a trusted reference. A manifest shipped with the same bytes is not an independent authenticity authority. Compare the outer digest with the separately delivered candidate receipt before relying on any contained script or manifest.

## 2. Safely inspect and extract

Use Python 3.11 or newer for the outer verifier. Run without `-O`, `-OO` or `PYTHONOPTIMIZE`. First compare the separately supplied verifier file's SHA-256 and ZIP digest against the delivery receipt. Alternatively, after independently verifying the ZIP digest, read its verifier source without executing any other content.

With the detached verifier beside the ZIP:

    python3 -B verify_bundle.py --archive "/path/Orthemology_Sixteenth_Research_Final_Evidence_v1_20261005.zip" --expected-sha256 "DIGEST_FROM_SEPARATE_DELIVERY_RECEIPT" --extract-to "/path/new outer extraction" --extract-packages-to "/path/new package extraction"

Both destination directories must be absent; their parents must exist. They must be disjoint and have no symlink ancestors. Paths with spaces are supported. Existing output is refused, never deleted. The verifier rejects unsafe/duplicate/case-colliding paths, symlinks and other nonregular members, unsupported/encrypted members, file/directory collisions and oversized archives before extracting. It writes ordinary files only and never runs extracted code or accesses the network. Keep failed output for diagnosis and choose a new location for a retry.

An already extracted candidate can be checked without further extraction:

    python3 -B "/path/new outer extraction/Sixteenth_Orthemology_Public_Evidence_Candidate_v1/verify_bundle.py" --directory "/path/new outer extraction/Sixteenth_Orthemology_Public_Evidence_Candidate_v1"

The manifest intentionally excludes its own hash; its bytes are bound by the externally supplied ZIP digest. Every other candidate file, including the verifier, is listed. Successful output says `PASS_INTEGRITY_AND_SAFE_EXTRACTION_ONLY`. The public boundary suite can be rerun from the candidate root with `python3 -B -m unittest discover -s tests -v`; it uses disposable synthetic ZIPs and no study data.

The nested extraction IDs are `core111`, `core-source-build-assurance`, `signed116`, `signed-verification` and `empirical`. Each preserves its inner archive's own root directory. Detached core verification files remain in the extracted outer candidate's `proof-core/verification/` directory.

## 3. Immutable 111-module core

Archive: `proof-core/Sixteenth_Orthemology_Proof_Source_Recovered_v1.zip`

SHA-256: `40c77652d3938e95f832023f32f018e1e394ffbd57adcc7d918d07d578e8a3a2`

The recovered integration contains 88 inherited and 23 additional mathematical modules. All 111 mathematical source files have exact frozen identities. The integration wrapper is newly recovered work. Among 220 main fixture slots, 167 have exact historical hash matches, 52 preserve complete payloads without a retained historical digest, and one was newly regenerated and independently checked. Do not call the entire ZIP a byte-identical restoration of an unavailable historical ZIP.

Author and independent exact-archive replays each built fresh project objects, ran the actual controls and compared complete theorem/declaration inventories. The final detached map takes precedence over earlier receipt fields that still say independent acceptance was pending. It records 111 mathematical roots, 220 main fixtures, four additional integration controls, 22 Python reference tests and 3,485 theorem roots. Read its bounded limitations and the package's `SCOPE.md` and `RECOVERY_SCOPE.md` before interpreting the result.

After safe extraction, use the core package's own `replay.py --source-only` to validate its internal locks. A full replay requires official Lean 4.19.0 and the pinned external dependency sources/objects:

    python3 -B "/path/new package extraction/core111/Sixteenth_Orthemology_Proof_Source_Recovered_v1/replay.py" --source-only

    python3 -B "/path/new package extraction/core111/Sixteenth_Orthemology_Proof_Source_Recovered_v1/replay.py" --lean "/path/lean-4.19.0-linux/bin/lean" --dependencies "/path/preparation/dependencies" --output "/path/new core replay"

The complete success marker is `RECOVERED_SIXTEENTH_SOURCE_PACKAGE_REPLAY_PASS`. An integrity-only pass is not that result. Logical theorem closure and the stricter computational/opaque audits have different scopes; neither physical interpretation nor a verified compiler follows from these checks.

### Additional required-closure source-build assurance

The detached `core-source-build-assurance/Sixteenth_Core111_Dependency_Source_Assurance_v3.zip` records a later, independently accepted qualification. Its SHA-256 is `739941e290a75a43ac1b32b67193f40a1990d943b0da37c4825359e39aaaee45`; begin with its `PUBLIC_README.md`, `METHOD_AND_SCOPE.md` and `PUBLIC_ASSURANCE_v1.json`. Exactly 1,369 required third-party Lean modules were compiled from their pinned sources in an isolated fresh build, without pre-existing third-party proof objects as inputs. The unchanged core111 archive was then freshly replayed against those source-built dependencies. The supplement does not rewrite the accepted source ZIP or its earlier cache-backed receipts.

All five resulting project inventories are byte-identical to the earlier prepared-cache replay. All 226 control-contract metadata rows agree after excluding elapsed-time and log-hash fields. Fourteen dependency object files differ in bytes from the prior prepared objects. No dependency byte-reproducibility claim or general semantic-equivalence proof for those differing objects is made; the pinned-source compilation and complete immutable acceptance replay are the controlling evidence.

This builds the required closure, not all Mathlib, and does not bootstrap the compiler. Official Lean 4.19.0, its Init/Lean/Std/Lake components, runtime and relevant OS/npm tooling remain trusted. Native/FFI verification is not established. The supplement records exact setup, source identities, commands, compiler outputs and replay evidence; it includes neither third-party source checkouts nor built object/resource bytes. The included scripts are historical executed checks with recorded workspace paths, not a new portable setup interface. Repeating the qualification requires equivalent fresh isolated paths and suitable new runtime bounds while preserving the pinned sources, compiler options and trust conditions documented in the supplement. A source-only integrity pass or the cache-preparation helper below is not a substitute for the source-build run.

## 4. Separate signed-controller service

Archive: `signed-service/candidate-v2.zip`

SHA-256: `264aadbd43d3f8cf449b04c7631fa5e53236ea911d2bb6dcc86f696af625c805`

Verification ZIP SHA-256: `5d64afd29cb57f2eccafc694d1e83ab2f2c8a3b71bee46a036b24747569ee1ce`

The unchanged Ninth public packet supplies the 95-module predecessor; the service contributes 21 new production modules. This separate closure has 116 modules. Its `SIGNED_SERVICE_RELEASE_v1.json` binds both immutable archives and their successful author/independent receipts. Each full replay records 172 Lean invocations, including 12 intended native-guard failures. These are invocation roles, not 172 theorem modules. The preserved interrupted v1 record is historical evidence, not a successful replay or a failed theorem.

First check the source identity, then run the complete entry point when prerequisites are available:

    python3 -B "/path/new package extraction/signed116/Orthemic_Signed_Controller_Service_v1/replay.py" --verify-only

    python3 -B "/path/new package extraction/signed116/Orthemic_Signed_Controller_Service_v1/replay.py" --lean-bin "/path/lean-4.19.0-linux/bin" --mathlib "/path/preparation/dependencies/mathlib" --out "/path/new signed replay"

The complete success status is `PASS_FRESH_95_PLUS_21_SOURCE_CONTROLS_AUDITS_CODEGEN_MUTATIONS`. Neither source-only verification nor a partial Ninth stage establishes it. No project build object may be reused.

### Dependency preparation: an important distinction

Both archives pin Mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b` and their transitive sources. The core's `prepare_dependencies.py` prepares exact checkouts and a targeted official cache acquisition. Its targeted set alone is insufficient for the signed package, whose sealed object manifest requires the fuller dependency closure: 6,641 official cached objects and five locally built cache-client objects.

The following is the official-cache preparation route, not the additional source-build qualification. With an already installed official Linux x86_64 Lean 4.19.0 toolchain:

    export PATH="/path/lean-4.19.0-linux/bin:$PATH"
    export LEAN_PATH=""
    export LEAN_SRC_PATH=""
    unset LEAN_SYSROOT
    export LEAN_NUM_THREADS=1
    python3 -B "/path/new package extraction/core111/Sixteenth_Orthemology_Proof_Source_Recovered_v1/prepare_dependencies.py" --directory "/path/new preparation"

Then retain those exact clean checkouts and the same cache locations. From their pinned Mathlib checkout, request the full official cache rather than only the core's selected imports:

    export MATHLIB_CACHE_DIR="/path/new preparation/official-cache"
    export XDG_CACHE_HOME="/path/new preparation/xdg-cache"
    cd "/path/new preparation/dependencies/mathlib"
    lake exe cache get

The pinned source's Lake setup must resolve its exact transitive checkouts, including Batteries; the helper establishes that layout. The recorded environment had transient official-cache download failures before a successful acquisition. A network/cache failure is not permission to change pins, skip missing objects, copy project objects or call preparation successful. If necessary inspect the pinned cache client's documented per-module acquisition and the signed manifest for missing dependency entries, then rerun the signed preflight. The signed entry point checks all required dependency objects and the Lean binary and fails closed on a mismatch. These instructions do not promise that an arbitrary cache environment will reproduce every pinned object automatically.

The signed116 evidence continues to use fresh project builds with identity-checked official dependency objects; no signed-package dependency cold build is claimed. Do not substitute the separately source-built core subset for the signed package’s sealed dependency-object manifest. The later source-build qualification applies only to the required core111 closure. Toolchain, runtime, standard external primitives and official-cache trust remain explicit for the cached route. No dependency source checkouts, toolchains, object bytes or binaries are shipped here.

## 5. Empirical source and complete fresh verification

The exact twelve accepted replay payloads are preserved in `empirical/SHARED_SOURCE_REANALYSIS_REPLAY_v2_RECOVERED_CONTAINER_v1.zip`; the recovery-time ZIP itself has a new container identity. Its SHA-256 is `73a6cdde7cba705f283df52085210592f851cd70f3163f78c42950aa45bfa0ef`.

The public terminal projections record complete-execution status and original evidence digests; they are not the underlying full numerical result bodies. Study-specific observations are stated only in the main report's study account. No raw input or row-level output is redistributed.

Synthetic code tests need no external data. In the extracted `empirical/shared-source-replay/` directory, use the package's Python requirements and run:

    python3 -B -m unittest discover -p 'test_*.py' -v

For a full replay, obtain both hash-identified inputs separately and use the original package's documented command and pinned Python requirements. Do not disable a hash or projection check to make the run proceed. Both required inputs were hash-verified before the complete unchanged pipeline was executed. Read `empirical/PUBLIC_COMPLETE_REPLAY_STATUS_v2.json` and its public independent acceptance for the completed scope and exact comparison. Full numerical result bodies remain local. This candidate performs no downloads automatically.

## 6. Occurrence fixture and public maps

The occurrence directory preserves the approved public fixture and historical member manifest. Run its own `check.py` in a disposable copy when executing it; its recorded output file is sealed evidence. Its checker establishes a finite interpreted fixture, not primary-text authenticity. The fixture's own README states its qualifications.

The mathematical map binds the exact separately delivered companion DOCX and the included public reader text. Verify those digests against the files you receive. `PUBLIC_READER_BLOCK_INDEX.json` gives each paper’s exact byte slice and hash within that one included reader text, so per-paper equation positions can be checked without duplicate paper files. Historical original-input hashes identify evidence that is not bundled and cannot be recomputed from this archive alone. Native equation mappings concern the companion representation; they are not additional kernel proofs.

The claim-source map is a bibliography/locator map for the separately delivered main report. It does not duplicate the report's source exposition. The main report DOCX and companion DOCX are deliberately absent from this evidence archive.
