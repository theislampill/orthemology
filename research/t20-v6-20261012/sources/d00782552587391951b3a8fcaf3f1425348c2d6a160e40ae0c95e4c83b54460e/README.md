# Eleventh research evidence

This selection preserves accepted research components and their bounded review and source records. The scientific claims and limitations belong to those records and the separate native report. Packaging and integrity checks add no scientific result.

## Locations and custody

- `ORIGIN_BINDINGS.json` records original identities and selected public locations.
- `CLAIM_COMPONENT_CROSSWALK.json` links report claim IDs and section locators to selected evidence, with historical identity-only references explicitly distinguished from distributed bodies. It does not repeat the report's argument.
- `MANIFEST.json` binds every selected file, every nested archive member, selected source/review receipt links and the external native report.
- The four component ZIPs in `components/` are preserved byte-identically from their current public acceptances. Their own directory prefixes and historical records remain intact. Current public-projection manifests control membership; older manifests and receipts retain only their stated historical role.
- The dependent-All v2 package includes the exact v1-to-v2 design-record projection and the earlier private-to-v1 chain. The superseded original design bodies are not included.
- `Orthemology_Eleventh_Research_Report_v1_20261003.docx` is the external report companion. No second copy of its prose, authoring text or rendering artifacts is included here.

## Verify without rerunning science

Place the extracted evidence directory alongside the separately downloaded report and evidence ZIP. From the extracted directory, run:

```sh
python3 check_integrity.py --report "../Orthemology_Eleventh_Research_Report_v1_20261003.docx" --archive "../Orthemology_Eleventh_Research_Evidence_v1_20261003.zip"
```

The report's exact basename, byte count and SHA-256 are all required. If a browser added a duplicate-download suffix such as `(1)`, make a copy with the exact report basename before using `--report`. Renaming alone cannot make different bytes pass. Quote paths containing spaces, as in the example.

`--archive` additionally compares every outer ZIP member with the extraction. `--expected-manifest-sha256` accepts a separately obtained trusted manifest hash. The checker works under normal Python and `python3 -O`. A staging manifest is refused unless `--allow-staging` is explicitly supplied. Final-review mode requires the exact external report, selected report identity receipts and complete claim crosswalk.

A successful check establishes consistency with recorded byte identities, exact membership, ZIP CRCs and selected custody links. It does not rerun proofs, reproduce arguments, certify source interpretations, confer acceptance or authenticate the package. A coordinated replacement of the whole package and its manifest must be detected by comparison with the separately supplied acceptance or outer archive hash. The checker executes no scientific helper and requires no compiler or network.

Scientific reproduction is a separate optional operation described inside each component. It requires the specified external trusted Lean/Mathlib environment. Historical helper behavior is preserved, including an assert-based input checker; it is not used as the outer integrity gate. Original failed diagnostics remain failures, and any approved path-normalized transcript is separately bound to its original identity. No primary source captures, exploratory drafts, compiled caches or report-rendering images are selected.
