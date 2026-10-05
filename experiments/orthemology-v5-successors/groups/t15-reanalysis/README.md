# Reanalysis of the published 15-dyad comparison

The source software reconstructs the Experiment 2 comparison reported by Hertz and colleagues. The same 15 male pairs performed a visual comparison task under private-vote-first discussion (IND) and immediate discussion (INF). Reusing those observations provides numerical checking of a procedure-relative performance contrast; it does not create another participant sample or an experimental replication.

The original aggregate reports mean sensitivities of 3.4375383509947173 (IND) and 4.150174851505185 (INF). The paired difference is 0.7126365005104668, with $t(14)=2.704264596388044$, two-sided $p=0.01711311760610826$, and a 95% interval [0.14743541713250896, 1.2778375838884246]. The separately recorded fresh execution reproduced these values byte for byte; the original reference remains an inherited artifact.

## Source and computation contract

`INPUTS.json` names exactly two official external inputs: the decisions ZIP and the Experiment 2 summary workbook. Each object's SHA-256 is checked before parsing. The selected `Data/Experiment2Data.mat` member has its own hash check. The source checks 15 paired structures, 128-by-19 and 128-by-11 matrix shapes, the specified response/interval/correctness columns, balanced contrast bins, the Experiment 2 worksheet range, and an empty auxiliary sheet. Timing missingness is checked for consistency; it is never used to drop response trials.

`fit_bfgs.py` and `fit_checked.py` retain separately written numerical cores behind the portable interface. One uses BFGS with multiple starts; the other checks derivatives, stationary fits, Hessian positivity and agreement with Fisher scoring. Reanalysis requires cross-implementation agreement below $10^{-6}$, exact agreement with all 120 workbook sensitivity estimates after rounding to four decimals, and preservation of the one negative slope. `validate.py` additionally checks every aggregate reference field within its declared tolerance. These are numerical checks at the supplied finite observations, not a formal proof of the optimisers.

The synthetic test file exercises derivatives; positive and negative slopes; equal-bin versus trial-count weighting; pairing direction and unit; missing timing without loss of choices; invalid selected responses and timing patterns; malformed fit inputs; hash mismatch; local-only CLI help; the aggregate-only output contract; and direct/hardlink overwrite protection. A successful `assertRaises` unit test is a successful test process. It is not misreported as a nonzero subprocess rejection. A separate damaged-input CLI control must complete with exit 2 and the intended `Source SHA-256 mismatch` diagnostic after positive prerequisites succeed.

## Runtime and reproduction

The source README prescribes Python 3.12. The original `BINDING.json` records historical Python 3.12.14. This integration uses a distinct Python 3.12.3 environment and records that actual interpreter's hash rather than silently adopting the historical patch version. The required packages remain numpy 2.3.5, scipy 1.17.0, pandas 2.2.3 and openpyxl 3.1.5. Package acquisition and actual installed dependencies are recorded separately from the source requirement.

The original package is projected into a fresh output directory for a replay. Its original commands are:

```sh
python -B -m unittest discover -s tests -v
python -B reanalyse.py --decisions-zip DECISIONS_ZIP --summary-xlsx SUMMARY_XLSX --output AGGREGATE_JSON
python -B validate.py --decisions-zip DECISIONS_ZIP --summary-xlsx SUMMARY_XLSX
```

Use the verified isolated interpreter and separately obtained hash-matching inputs. The original software has no download function and no record-level output mode. Neither the external input objects nor their participant records belong in this repository. Public evidence consists of aggregate results, exact source and environment identities, terminal stage/control dispositions, and private-log hashes.

Fresh execution status: **FINITE_ONLY**. The original 13 unittest methods passed; all 11 original checksum rows matched; the aggregate and numerical-reference checks passed; and the corrupted-input subprocess completed with exit 2 and the exact intended diagnostic. The fresh aggregate and validation outputs equal their inherited reference bytes. The maximum difference between the two numerical implementations was 3.0215846713588235e-08. Both official inputs, all 12 projected source files, the interpreter, and all 10 installed distribution inventories remained unchanged.

See [fresh aggregate](FRESH_AGGREGATE.json), [numerical validation](FRESH_VALIDATION.json), [execution summary](EXECUTION_SUMMARY.json), and [environment identities](ENVIRONMENT.json). The complete stage/control receipt is embedded in the D18 provenance fragment. Source inclusion, inherited execution, fresh replay, human-specialist review and adoption remain separate status axes.

## What the comparison cannot identify

Private responses were not recorded in the immediate-discussion condition. An announcer's role does not isolate that member's contribution. Consequently the reanalysis does not identify which member supplied the judgement or fit the two mechanisms in the adjacent attribution argument. Graphical panels and original author-program execution remain outside the fresh verification scope. No new participant experiment, external specialist validation, or canonical adoption is claimed.

<!-- SOURCE_NAVIGATION -->
## Inspectable sources

- [Original portable-package instructions](../../source-store/55f26bac8864c6e3279debaf821d1c714abbcff6f22f5364a654823ae6a61b70/README.md) — `T15-EMPIRICAL-README`.
- [Exact official input identities and parsing scope](../../source-store/a919102c102ff3d07b447f52490266aca76afa4f84a972e2f3d78b3470f97a7a/INPUTS.json) — `T15-EMPIRICAL-INPUTS`.
- [Source-required package pins](../../source-store/41b4c6a14166306b9f593728df115892a3f0a64aa4c153741b9579c14b74270d/requirements.txt) — `T15-EMPIRICAL-REQUIREMENTS`.
- [Original aggregate reanalysis driver](../../source-store/20110e73fd822e21651064578946cdf910edc493c973953b2c7d1bb74481dd94/reanalyse.py) — `T15-EMPIRICAL-REANALYSE`.
- [Original BFGS numerical core](../../source-store/cd6f203e2e79f6113de3cef2e4d98926c3f75fe374ca04b3ea73aeee02301a02/fit_bfgs.py) — `T15-EMPIRICAL-FIT-BFGS`.
- [Original checked numerical core](../../source-store/ebefc609d09bf68296e5a1c5392064effaf4c4d462b82cbb451b1e93340ec376/fit_checked.py) — `T15-EMPIRICAL-FIT-CHECKED`.
- [Original synthetic tests](../../source-store/afb1ba14ecbbf193f07ac81f985be30535abf9771387813e9dbd0bbbfc72fb50/test_package.py) — `T15-EMPIRICAL-TESTS`.
- [Original numerical/reference validator](../../source-store/7d9a4c8d071e2591c8d4568c88c277ab61834e52df21500a1367efb2ac7e060a/validate.py) — `T15-EMPIRICAL-VALIDATE`.
- [Inherited aggregate reference](../../source-store/eda676cfd5ac10b0a92040b9164a6d968b7f23ad68e456089579b7cf2d8f6acd/AGGREGATE.json) — `T15-EMPIRICAL-AGGREGATE`.
- [Historical package provenance](../../source-store/60755eff76d1f0b1cc1fcd56aef8a4b8bf91b17fee744ed20b6c6260e0e8f33e/BINDING.json) — `T15-EMPIRICAL-BINDING`.
- [Original package checksums](../../source-store/9ab3df6e096f8158f755ea31408786248d04547d0bd7c38785770d7e9964e41e/SHA256SUMS) — `T15-EMPIRICAL-CHECKSUMS`.
