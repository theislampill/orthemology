# Final independent packaged-source review: shared controller v3

Verdict: ACCEPT this exact sanitized source ZIP for final delivery. It replaces
v2 as the final source-artifact pointer and resolves the narrow LD_* compiler
subprocess environment finding. The three scientific milestones and their
accepted mathematical scopes are unchanged.

## Exact final source identity

- Archive: `Shared_Root_Controller_Source_v3.zip`
- Bytes: 2,299,830
- SHA-256:
  `bc9ae95ebfa10186afd4853069d6d7eea589592564eb1c3eab267189e65fc443`
- Public manifest SHA-256:
  `f31da25cb722b9b80e58f76acc378c9553dc2c6a92c28f4d7bfc0cb741c99dbf`
- Wrapper SHA-256:
  `d52878878f3e016037b4deddf4eb5847fbcf19d0faaafa1460fc3fbe71b158b2`

The actual ZIP contains 57 source/document/metadata files and 10,111,605
uncompressed bytes. Safe member paths, regular extracted files, no duplicates
or symlinks, and CRC integrity were checked. No compiled object, toolchain,
cache, native binary or original user document is shipped.

All 39 Lean module/audit files and `SCIENCE_INVENTORY.json` are byte-identical
to v2. The 33 scientific source-projection files match their immutable accepted
origins, and all four reviewer modules match their reviewed originals. v3 adds
only the narrow wrapper sanitation function, its bounded test script and
explanatory public metadata/prose. Earlier source and companion candidates are
preserved as historical artifacts, not final delivery pointers.

## Corrected compiler environment boundary

The prior wrapper removed two named loader variables but left `LD_AUDIT` and
other inherited LD_* settings. v3 creates a fresh child environment map and
removes every key beginning with `LD_` at the shared `run_compiler_stage`
boundary. Version, source compilation and axiom-audit calls all use that
runner. Existing Lean override cleanup and the deliberately generated
`LEAN_PATH` remain intact. The incoming map is not changed.

The reviewer inspected the exact narrow diff, independently ran the delivered
bounded test from the actual ZIP, and added a separate child-process probe.
Tests cover LD_PRELOAD, LD_LIBRARY_PATH, LD_AUDIT, LD_DEBUG, LD_PROFILE,
LD_TRACE_LOADED_OBJECTS, LD_PROFILE_OUTPUT, the bare LD_ key and arbitrary
future LD_ names. Trusted child probes receive no LD_* keys for all three
stage categories. Ordinary/nonprefix names and generated imports survive,
while both input and running-parent maps remain unchanged. A red control
shows in memory that the old two-name filter fails the required condition.
No parent Python interpreter was launched with hostile loader settings.

This sanitizes the compiler subprocess map's LD_* prefix. It is not a claim
to validate or protect an already running Python launcher, arbitrary other
host configuration, the operating system or a compromised machine.

Loader evidence:

- `loader-v3-packaged/RECEIPT.json`, SHA-256
  `9f76600f331905816cde91d7e0d04795d31d4a4f93bbdc24dc89537c16cff59d`
- `loader-v3-independent/RECEIPT.json`, SHA-256
  `ce73c024ca9a4c9d73eefc04be198debe09c116513171a3b036c1daae680ae24`

## Independent end-to-end final-ZIP replay

The reviewer extracted the actual final v3 archive into a new location and
invoked its delivered wrapper from an unrelated `/tmp` working directory.
The custom output directory was absent; all custom objects were rebuilt
fresh. Externally supplied pinned Lean 4.19.0 and Mathlib dependencies were
reused read-only. The process exited 0.

All 37 source/reviewer modules and both complete axiom audits passed: exactly
129 new scientific and 20 reviewer theorem closures, with only `propext`,
`Classical.choice` and `Quot.sound`. All 39 build/audit stages were warning-free
and non-timeout; the separately checked compiler version also passed. Full
package, compiler-distribution, Mathlib source and cache identity checks passed
before and after. Exactly the five approved path-only cache trace differences
were recognized; no dependency file was edited. The ZIP identity is unchanged.

Final independent receipt:
`public-v3-positive/replay/REPLAY_RECEIPT.json`, SHA-256
`7adf57551fa7ed31a4647d0c7e2faf5f83f60fb2cb9e3877114fa20eab175ace`.

`public-v3-positive/PORTABILITY_SETUP.json`, `PROCESS_RESULT.json`, `CONSOLE.log`
and `replay/logs/` bind the exact archive, extraction, unrelated caller,
commands, successful process and all stage logs. Earlier author/reviewer v2
replay records are historical; final v3 acceptance is based on this independent
v3 packaged-byte replay. Replay duration is proof/toolchain verification time,
not controller action latency.

## Independent wrapper refusal controls

All 23 earlier packaging controls were rerun against the actual final v3 ZIP.
Their receipt is
`public-v3-wrapper-controls/WRAPPER_CONTROL_RECEIPT.json`, SHA-256
`709a2b0fd5ce9ddd0c5eeb774f58ac6e249a6e72105e1930468f7879805b96f1`.

They check exact source projection and inventories; source tamper refusal
under optimized Python; added/missing files; invalid finite timeout limits;
existing/protected/symlinked output paths; unsafe manifest paths and source
symlinks; missing/duplicate/unexpected/nonstandard axiom audits; explicit
timeout failure status; and the exact five-file metadata exception versus a
sixth changed trace or non-path change to an allowed trace. Negative controls
use isolated copies. The package and actual dependencies stay unchanged.

The five-trace allowance verifies the exact approved current hash/size and
one recorded prefix replacement, then compares the in-memory normalization
to the original pinned hash/size. It never edits dependency files. Full real
dependency checking is exercised by the positive replay; the smaller negative
fixture tests the refusal boundary without duplicating or mutating caches.

## Scientific interpretation retained

The three exact accepted boundaries remain:

- Protected single-action progress: a fixed public program independent of the
  hidden environment and response annotations, under authentic source/
  authority, accurate observation, exact-command freshness, sampled-window
  and completed-slot service premises
- Fixed-controller/order/world attainment: the actual first 20 trials have
  247 reference events, zero installations and zero repairs; the full 21
  reach the installed successor
- Universal finite bad-store weave erasure: legal writes to fixed bad roots
  preserve all good stores/common state and the source-derived endpoint;
  259 serviced events remain, with total length 259 plus inserted writes

Raw accepted traces may stutter forever. No infinite-starvation termination,
general arbitrary-interleaving theorem, moving map/fault set, free adversarial
event count, physical clock or wall-time service guarantee follows. Extra
owner operations, foreign cancellation and competing landings are not licensed
by the finite-corruption increment.

The controller/interpreter remains classical/noncomputable mathematical Lean
reference code. Kernel checking of its theorems and literal use of source
localStep/attempt do not establish extracted or native 21-path execution.
The concrete shared fixture is three-byte ABC with initial ABC+LF draft, one
criterion installation and zero repairs; it is distinct from the 3013-byte
native label-local batch fixture. No observation-equivalence, opacity/search
lower bound, general optimality or new source-authenticity warrant is claimed.

The separate final acceptance companion must bind this v3 identity and these
results. Its static archive acceptance is deliberately external to avoid a
self-referential archive hash.
