# P03 later Codex implementation handoff

## 1. Authority and input gate

This is a research/proposal checkpoint, not an instruction to alter authoritative source. U03, U04 and Q1f remain PARTIAL here and retain their original canonical open statuses. The three proposed Python changes have executable finite evidence; no proposed Lean source was compiled. No integration replay, publication, owner adoption, external review or historical recovery credit is granted.

The preserved main is `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`, PR #28 merged. A later executor must confirm custody and obtain whatever authority is required before touching a canonical checkout. The optional commands below operate on a new isolated directory, not on that checkout. A checkout at a different tree needs explicit rebase/review rather than silent application.

First read `README.md`, all three obligation reports under `research/`, `inputs/OBLIGATION_CONFIRMATIONS.json`, `proposal/DEFINITION_AND_STATUS_CHANGE_PROPOSALS.json`, and `proposal/PATCH_MAP.json`. The exact original input is nested in `inputs/`; the public R15/R16 statement supplements are independently hash-bound at the frozen commit. The older pending headers in those supplements do not undo the later scoped ordinary-argument acceptance recorded in the supplied canonical formalisation map.

Verify the whole ZIP and its detached digest **before** trusting the extracted tools. With `CHECKPOINT_ZIP` set to the actual downloaded ZIP path:

```bash
set -euo pipefail
CHECKPOINT_ZIP="$(realpath -- "$CHECKPOINT_ZIP")"
cd -- "$(dirname -- "$CHECKPOINT_ZIP")"
sha256sum -c "$(basename -- "$CHECKPOINT_ZIP").sha256"
```

After extraction, set `PACKET` to its actual root. The following independently reopens the ZIP and checks every member, the control hash chain, and the nested original input bindings. `AUDIT_OUT` must name a new file outside the extracted sealed packet.

```bash
python -B "$PACKET/tools/verify_checkpoint.py" \
  --zip "$CHECKPOINT_ZIP" \
  --sha256 "$CHECKPOINT_ZIP.sha256" \
  --out "$AUDIT_OUT"
```

## 2. Reconstruct without modifying any existing repository

The supplied source subset is not a complete repository clone. This is a bounded executable reconstruction for the existing source test interface. It does not claim the whole repository or historical `verify.py` manifest gate has been rerun. The original source manifests remain exact preimages and are intentionally not regenerated to bless the candidate.

```bash
set -euo pipefail
PACKET="$(realpath -- "$PACKET")"
WORK="$(mktemp -d -t orthemology-p03-proposal.XXXXXXXX)"
export WORK PACKET
python -B "$PACKET/tools/prepare_proposal.py" --mode baseline \
  --out "$WORK/baseline" > "$WORK/baseline-reconstruction.json"
python -B "$PACKET/tools/prepare_proposal.py" --mode proposal \
  --out "$WORK/candidate" > "$WORK/proposal-reconstruction.json"
export P03_SOURCE="$WORK/candidate"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
```

`prepare_proposal.py` verifies the original input SHA-256, its CRC and source population; checks the three exact preimages and postimages; and refuses an existing destination. The result has exactly 70 files and exactly these three source differences:

| Path relative to source root | Proposal purpose | Explicit scope caveat |
|---|---|---|
| `boundaries.py` | Refuse an emitted JSON container depth the decoder would reject | More conservative encoder success domain; generic node-depth gate unchanged |
| `operational.py` | Capture a bounded flat observation tuple before validation and lock waiting | Not a general concurrent deep-copy guarantee or an invocation-time snapshot |
| `proof_export.py` | Check row type/arity before unpacking and raise `Rejection` | New exact list/tuple row grammar; formerly tolerated arbitrary two-item iterables need deliberate review |

For any later authorised repository application, compare **all** preimage hashes in `PATCH_MAP.json` before applying any diff. Do not apply one file and discover a different preimage for another. Copying postimages or applying the supplied unified diffs must produce the recorded postimage hashes. Other repository files, manifests, public indexes and acceptance/status owners are a separate later implementation/review action.

## 3. Exact executable replay commands and expected evidence

The finite test claims are tied to Python 3.13.5 in the captured environment. A run on another Python version is useful new evidence but must be labelled with that actual version. Save all output, exits, environment and source identities outside the sealed checkpoint. This shell function fails the script on a nonzero replay result while preserving its actual exit.

```bash
mkdir -- "$WORK/logs"
python --version > "$WORK/logs/python-version.txt" 2>&1
python - <<'PY' > "$WORK/logs/environment.json"
import json, os, platform, sys
print(json.dumps({'python':sys.version,'executable':sys.executable,
  'platform':platform.platform(),'environment':{k:os.environ.get(k)
  for k in ('PYTHONHASHSEED','PYTHONDONTWRITEBYTECODE','P03_SOURCE','PATH')}},indent=2))
PY
run_checked() {
  label="$1"; shift
  printf '%q ' "$@" > "$WORK/logs/$label.command"; printf '\n' >> "$WORK/logs/$label.command"
  date -u +%FT%TZ > "$WORK/logs/$label.started"
  set +e
  "$@" > "$WORK/logs/$label.stdout" 2> "$WORK/logs/$label.stderr"
  code=$?
  set -e
  printf '%s\n' "$code" > "$WORK/logs/$label.exit"
  date -u +%FT%TZ > "$WORK/logs/$label.ended"
  test "$code" -eq 0
}
cd -- "$WORK/candidate"
run_checked suite-normal python -B -m unittest discover -s tests -v
run_checked new-regressions-normal python -B "$PACKET/tools/test_new_regressions.py" -v
run_checked contracts-normal python -B "$PACKET/tools/test_refinement_contracts.py" -v
run_checked exporter-normal python -B "$PACKET/tools/test_export_row_refusal.py" -v
run_checked suite-optimised python -B -O -m unittest discover -s tests -v
run_checked new-regressions-optimised python -B -O "$PACKET/tools/test_new_regressions.py" -v
run_checked contracts-optimised python -B -O "$PACKET/tools/test_refinement_contracts.py" -v
run_checked exporter-optimised python -B -O "$PACKET/tools/test_export_row_refusal.py" -v
run_checked finite-correspondence python -B "$PACKET/tools/probe_finite_correspondence.py"
run_checked graph-guards python -B "$PACKET/tools/probe_q1f_graph_guards.py"
find "$WORK/candidate" -type f -print0 | sort -z | xargs -0 sha256sum \
  > "$WORK/logs/candidate-source.sha256"
```

Expected final proposal counts: 183 existing methods, 2 new regression methods, 12 contract methods and 2 exporter methods per Python mode: **199 methods per mode**, across four commands, not a new universal proof. One exporter method contains four malformed-row subcases. The independent finite probe checks 4,928 shifts, 94,864 substitutions and 3,405 head-step terms. The graph probe supplies two countermodels to an untyped extrapolation plus one positive control. The corpus already exists and the probe checks its identity rather than replacing it.

For negative replay, set `P03_SOURCE="$WORK/baseline"` and execute `test_new_regressions.py` and `test_export_row_refusal.py` under a recorder that expects nonzero. They fail for the recorded three concrete defects. Do not repair the tests to make unchanged source green; do not treat those failures as kernel counterexamples. Raw red and green evidence is already retained in this checkpoint.

## 4. Exact later Lean 4.19.0 graph-candidate commands

This environment could not launch Lean: the retained `lean --version` probe has exit 127. The new two-file graph candidate is **UNVERIFIED**. Syntax inspection, ordinary induction and Python counts do not replace kernel evidence.

Obtain a real, independently authenticated distribution for **Lean 4.19.0, commit `6caaee842e94`**. Confirm binary provenance against the pinned distribution; a printed version string alone does not establish compiler identity. Set `LEAN419` to the actual native executable. The helper downloads nothing, accepts no replacement pin and creates a new output directory:

```bash
python -B "$PACKET/tools/compile_lean419_candidate.py" \
  --lean "$LEAN419" --out "$WORK/lean419-graph"
```

The helper captures executable hash, version, prefix, source hashes, commands, exits, stdout/stderr and freshly generated nonempty `.olean` files. Its build commands are exactly:

```bash
"$LEAN419" --version
"$LEAN419" --print-prefix
# In a fresh directory containing only the two hash-bound .lean candidates:
export LEAN_PATH="$WORK/lean419-graph"
"$LEAN419" -o P03GuardedGraph.olean P03GuardedGraph.lean
"$LEAN419" -o P03GuardedGraphAudit.olean P03GuardedGraphAudit.lean
```

`P03GuardedGraphAudit.lean` contains explicit `#check`, `#print` and `#print axioms` for exactly five declarations listed in `EXPECTED_TARGETS.json`. The predicted axiom sets are empty, **not observed empty**. Reject a missing declaration, elaboration/compiler error, nonzero exit, missing/empty artifact, stale reused artifact, wrong version, `sorryAx`, proof-output spoofing or unexplained dependency. Independently inspect the actual types and binary origin even if the helper reports a build/readback pass. The helper deliberately grants no automatic kernel acceptance.

The standalone candidate imports only `Init`. For any later integration with accepted native source, retain the existing Lean 4.19.0 / Lake `5.0.0-6caaee8` / Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` pin and the unchanged documented project interface. Separate 4.32.2 results remain separate. Do not convert the preserved original strict-wrapper FAIL into either a missing-tool result or a successful candidate build.

Even a genuine successful graph build would establish only rank-respecting DAG transport: it is **not** `VersionCustodyTransport.guarded_reason_dag_composition`, full VCT, TRC or a recovered historical declaration.

## 5. Remaining acceptance work, not silently discharged

**U03:** Review the proposed owned-input/outcome and row-domain contracts. Complete universal byte decoding/duplicate-key/integer/Unicode validation, structural-validation and all seven checker-rule correspondence, export constructor fidelity, budgets and typed refusal paths. The report supplies ordinary substitution/shift reasoning and source mappings, not whole-Python formalisation. Resource refusal must not become accepted success merely to make a theorem total.

**U04:** Formalise the complete Gamma/issued-record/lock/call-local relation in the report, including persistent issuer identity and issued records, complete read sets with absences, monotone stamps, the validation-snapshot invariant, rejection no-effect and success linearisation. Explicitly distinguish API `Rejection` atomicity from host crash/OOM atomicity. U03 is an interface dependency, not presumed complete. Any probability-extension proof requires the declared accepted premises or an explicitly conditional P02 interface, never assumed new P02 success.

**Q1f:** First validate the graph candidate at the actual pin, retaining the target DAG premise. Then supply the independent target-indexed obligation/evidence semantics, version/root/semantic commutation and authority/re-delegation/invalidator layers required by the full VCT statement. Do not encode the desired conclusion as a Boolean field and claim its projection as a proof. Optional TRC needs the P12/PMR-007-COB-1 pure results, exact VCT custody and DAEE validator/record correspondence. No real-world successor completeness, source truth, human restoration or owner policy follows from a finite model certificate.

New definitions, narrower native domains, implementation changes, manifests, public indexes, publication-source changes and any canonical adoption each require their later authorised review. This handoff grants none of those effects.
