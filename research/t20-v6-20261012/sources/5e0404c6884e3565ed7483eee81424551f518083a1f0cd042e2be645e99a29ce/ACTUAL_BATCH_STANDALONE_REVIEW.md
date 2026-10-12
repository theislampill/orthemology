# Independent final source-ZIP and companion-execution review

Verdict: **PASS for the exact source ZIP and tested companion execution inputs.**
This completes the standalone cold-replay acceptance of the previously accepted
actual-batch science. Assembly of the final acceptance-companion ZIP still needs
a separate archive inventory and byte-equivalence check. This is not whole-tranche
closure or an expanded scientific claim.

## Identities and noncircular scope

- Source archive: `Eighth_Actual_Batch_Controller_Source_v5.zip`, 2,438,940 bytes,
  SHA256 `19f90a7bfd9bd2840c71c972029447533e9f5985281c275c5c0979ff8597f906`.
- Its `PUBLIC_MANIFEST.json`: SHA256
  `6acd4dc584cb37c7c9e168dd71f912f96cd31fedc9f408fdb8742450462dc9fa`.
- Unchanged scientific v4 manifest: SHA256
  `186281d14d0ea41e7ac49aa7a392a6cf05cb92047670f7d639420720785ecf0e`.
- Tested companion execution-input manifest: SHA256
  `f084853b8aafc5497567695e1b5e565af7f68baeaa4c85faefa31798922c193e`.
- Tested `replay_review.py`: SHA256
  `f35cc6d8909ef15ea24156e089f56c6b1db20a83da39c869e6473a76a7cb0aee`.

The companion entrypoint binds and safely extracts the exact separate source ZIP.
It does not certify its own eventual ZIP hash. The tested input manifest is saved
byte-for-byte as `STANDALONE_TESTED_COMPANION_MANIFEST.json`. Adding these resulting
review records creates a distinct final companion manifest and ZIP identity. Their
acceptance must check that the tested code, controls and existing records remain
byte-identical, and that only the declared packaging/acceptance material is added.

## Independent actual run

The reviewer copied the fixed archive and companion inputs into a fresh directory
with spaces in its path, then invoked the companion from an unrelated caller
directory. This caller directory contained three invalid, nonexecuting shadow
`.olean` files named after real imported modules. A trusted Python bootstrap
injected hostile `LEAN_*`, `LD_*` and `DYLD_*` values after interpreter startup,
including absent preload/audit libraries and loader-output sentinel destinations.
The compile subprocesses had to receive the wrapper's sanitized environment.

The run started at 03:29:23 UTC and reached terminal PASS at 03:38:56 UTC on
2026-10-03. It freshly compiled all 61 scientific/dependency modules and all nine
independent reviewer modules, plus two generated named-declaration audit modules.
There was one separate compiler-version invocation. Thus the recorded result has
72 fresh custom objects and 73 clean compiler logs, with 504.524 seconds of summed
compiler-stage time. No old author, previous reviewer, or previous scientific
custom object was permitted on the Lean search path.

The two audits cover every enumerated named explicit declaration: 902 in the
scientific closure and 78 in the reviewer controls. These include the accepted
476 author-theorem subset and 47 independent reviewer theorems. All 980 actual
printed axiom records match the exact declared name sets, with only subsets of
`propext`, `Classical.choice` and `Quot.sound`. Empty closures are checked too.
This is broader than the theorem-only audits credited in the earlier scientific
receipts; those old receipts are not retrospectively relabelled.

The companion replay receipt is
`standalone-companion-v2/independent fresh output/RECEIPT.json`, SHA256
`c8db7a5297aa347474e1acd2691c9259bb058bb812fea9cafc369c062693b932`.
Its nested fresh scientific receipt is
`standalone-companion-v2/independent fresh output/fresh science/RECEIPT.json`, SHA256
`9f75890b82c46f1fb361439c26602c4ef3a266e4ef44c052378c67e7d6fb3d91`.

After the run, a separate read-only reviewer checker verified all source archive
members against the actual extraction, every recorded source/object/log digest,
the complete isolated object inventories, all axiom-log records, and unchanged
input manifests. It found no loader-output sentinel and verified that the three
foreign shadow objects were unchanged. `STANDALONE_POST_REPLAY_BINDINGS.json`
records these checks. No completion is inferred only from an author report.

## Toolchain, cache and wrapper contract

The run uses official Lean 4.19.0, commit `6caaee842e94`, executable SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`,
with `-j1 -s65536`. The wrapper validates all 5,065 pinned Lean distribution
entries, 6,816 Mathlib source records and 34,230 cache entries before and after
the source replay; the companion performs another final dependency check.
The pinned external Mathlib objects are reused read-only, not freshly compiled.

Exactly five Cache-tool `.trace` files use the independently bound restored
compiler-path metadata variant in this actual run. Their raw hashes, normalized
hashes, sizes and one-path substitutions are recorded; no input bytes are
rewritten. The public validator additionally accepts a single exact supplied
canonical compiler-launcher path substitution in those same five files, only if
normalizing it produces the original pinned size and hash. That third-location
case has contract-test evidence; the actual cold run here exercised the known
restored-path case. Neither rule permits a changed `.olean`, argument, dependency
hash, extra replacement, arbitrary prefix normalization or other cache difference.

Static and contract checks accepted the final source wrapper (14 supplied tests
and independent mixed/uppercase diagnostic controls) and the companion (five
tests). The checks include safe extraction, protected fresh output paths, genuine
harmless timeout and missing-launcher cases, failure-status propagation, output
receipt cleanup, environment sanitization and bounded metadata alternatives.
Timeout/resource/launcher failure is inconclusive rather than positive; all
warnings, errors, proof escapes and unexpected axioms fail closed. A resource
diagnostic cannot become success merely because the process exits zero.

The sanitization claim concerns compiler/subprocess environments after a trusted
Python launch. It does not protect an already compromised Python interpreter,
parent loader, operating system or dependency-verification implementation. The
host and ordinary absence of concurrent adversarial input mutation remain trust
assumptions. The source archive itself supplies no toolchain or Mathlib cache.

Earlier wrapper candidates were corrected before this final acceptance: the
initial incomplete loader-variable cleanup, inconsistent version-stage failure
classification, and exit-zero resource-diagnostic acceptance were not credited
as final passing releases. Their diagnostic records remain distinguishable from
this fixed source-v5 replay. Scientific source bytes did not change during these
packaging corrections.

## Scientific scope remains fixed

The accepted actual source still tries all four ordered paths, keeps the actor's
observations unchanged, generates only intra-batch nonce freshness, may mutate
root storage on a false preparation or cancellation reply, and withholds faulty
execution gates. Proposal failure creates synthetic closed records without a
runtime cancellation event. The fixed-action uniqueness theorem remains specific
to that literal withholding controller.

The arbitrary-World availability iff assumes source-record readiness, including
matching root policies equal to the field `w.effectivePolicy`; it does not prove
that field authentic current owner authority. A current-authority conclusion
still needs the separately verified Authority/Aligned/Reachable history theorem.
The exact surviving-envelope predicate is proof-side and supplies no actor oracle.
Numerical cleanup thresholds, exact complete-envelope freshness and genuine
service effects remain separate. Delayed-delivery/retry tombstone controls and
same-nonce/different-command success retain their documented finite scope.

The exact native two-batch projection retains the pinned 3,013-byte source and
the specified pure controller sequence. It is not a proof of the omitted IO
assertions/printing or of a general continuously operating controller. None of
this packaging work establishes physical identity, authentic observation or time,
real service latency, asynchronous/interfering progress, a nonce-allocation
service, shared-alias lifecycle composition or N2/T0/R5 closure. The prior sealed
scientific reviews and the explicit retry-note corrigendum remain authoritative
for their narrower statements.
