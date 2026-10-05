# Occurrence-correspondence evidence

This component makes the Fourteenth report's bounded occurrence result reproducible. It contains original verification code and source-identification metadata, not a copy of Fusha or its evidence data. It requires Python 3 and uses only its standard library; the replay was tested with Python 3.12.14.

## Exact result and limits

For occurrence `quran:61:5:4`, the pinned pilot records one projection reused by four appearance records. Its projection SHA-256 is `f4f1da458b5eeb1561b42f92aad53762d04c59957fe237386d55a8bcdcdb80aa`.

The replay checks 70 source-file byte bindings and the same 12 occurrence assertions as the accepted research result, for **82 assertions** in total:

- The projection content hashes correctly and all four appearance hashes agree.
- Entry certification remains separate from a candidate sense edge. No certified sense edge is substituted.
- The governor relation remains unresolved and absent from the rendered governor field. Both unresolved dependency keys remain present.
- The discovery lattice retains two segmentation candidates and four function candidates. Promoting the sense status would change the projection hash.
- Five relevant facts have certified status in the recorded event fold: four occurrence-specific facts and one entry-level rootlessness fact. These are not five independent evidence sources.
- Three historical function/governor/case claims remain review-required while their version-2 successors are certified.
- The separate illustrative canary remains candidate, keeps clitic-component, candidate-entry and root-family relations distinct, and has different projection and surface bytes from the pilot. Its hash is `12d227eb2429f14e1a6d7173bb8372e954189f101016c9041249779b2eca112e`.

Here “certified” describes status recorded in the pinned application data. It is not independent certification of Arabic accuracy. The result establishes bounded occurrence reuse with retained distinctions; it does not settle sense identity, certify a host lexeme from a root-family link, or prove general meaning-preserving transport across representations or versions.

**Full repository regression, linguistic correctness, current/live deployment and the broader correspondence problem remain unverified.** No builder, migration or certification transition is part of this replay. The canary's format validation is not proof that it is the pilot's generated projection.

## Source identity

- Repository: [theislampill/fusha](https://github.com/theislampill/fusha)
- [Pinned commit](https://github.com/theislampill/fusha/commit/c8b5db593d88311e5a020607dba70ff838ab61c5): `c8b5db593d88311e5a020607dba70ff838ab61c5`
- Git tree: `a5bd2b045bc36c78047b5d3f7e9c2807fbf4153c`
- [Pilot projection records](https://github.com/theislampill/fusha/blob/c8b5db593d88311e5a020607dba70ff838ab61c5/qamus/examples/p007-li-pilot/projections.jsonl)
- [Separate canary](https://github.com/theislampill/fusha/blob/c8b5db593d88311e5a020607dba70ff838ab61c5/qamus/examples/website-payloads/multi_entry_liqawmihi_61_5_4.payload.json)

`source-lock.json` lists exactly 70 repository-relative paths, each with its pinned URL, Git blob SHA-1, SHA-256 and byte length: 1,902,456 bytes altogether. This is a selected source closure, not the whole repository. All 70 are byte-checked; only the selected records receive the 12 occurrence-data checks. Source paths naming votes/evidence are metadata only; their contents are not bundled.

## Obtain the source separately

From a directory containing the extracted archive's `language/` folder, the following ordinary Git commands obtain a separate checkout. They contact GitHub only when you choose to run them; neither this package nor its verifier downloads anything or runs repository builders.

```sh
git -c core.autocrlf=false clone --no-checkout https://github.com/theislampill/fusha.git fusha-source
git -C fusha-source -c core.autocrlf=false checkout --detach c8b5db593d88311e5a020607dba70ff838ab61c5
git -C fusha-source rev-parse HEAD
git -C fusha-source rev-parse 'HEAD^{tree}'
```

The last two outputs must equal the commit and tree above. These commands make no upstream changes. Review the repository's source boundaries and code before executing its scripts. Keep downloaded source/data outside any redistribution of this component.

## Run the original verifier

```sh
python3 -I -B language/verify_occurrence.py fusha-source > occurrence-check.json
```

If this folder has another name, substitute that name for `language`; the verifier finds `source-lock.json` beside itself. A separately supplied directory containing only the exact 70 locked files also works. Files outside that list are ignored, so success does not attest an entire checkout or its Git history.

Exit code 0 means all 82 assertions passed. The JSON output lists their names and the bounded query result. Its expected SHA-256 is `be8e02f6087646a5ea97024ce0470a582cf99412a044a0ce80ace3562c2702c3` (UTF-8, LF line endings). A missing directory/file or changed source bytes fails before occurrence analysis. The verifier parses the same in-memory bytes it checked, imports no application code, invokes no subprocesses and writes only to stdout. Shell redirection creates the receipt outside the source directory. It does not authenticate a substituted copy of this package; retain the accompanying archive integrity information.

## Optional retained targeted checks

After inspecting the pinned source, these are the actual script names and supported arguments for the previously retained checks. Run them from `fusha-source/`; this step executes application code and is separate from the read-only data verifier. The self-tests create temporary fixtures, and the pilot validator invokes local validation/count subprocesses. Suppress Python bytecode writes in child processes too:

```sh
cd fusha-source
export PYTHONDONTWRITEBYTECODE=1
python3 -B tools/validate_p007_pilot.py
python3 -B tools/validate_p007_pilot.py --self-test
python3 -B tools/validate_meta_transclusion_projection.py --self-test
python3 -B tools/validate_website_payload.py qamus/examples/website-payloads/multi_entry_liqawmihi_61_5_4.payload.json
```

Only these targeted commands are claimed: pilot validation reports 12 occurrences / 78 appearances / 49 facts and NOT-DEPLOYED; the pilot self-test rejects 14 named mutations then accepts the fixture; the meta self-test checks synthetic completion/closure cases; the website command validates only the illustrative canary. The 14 mutations are separate from the 82 data assertions.

For this package, all four commands were replayed from a fresh layout containing only the locked 70 files. They exited 0, reproduced the retained outputs exactly and left that source inventory byte-identical. The portable verifier likewise reproduced the accepted JSON exactly from a relocated directory containing spaces. Packaging-only checks rejected a missing/non-directory input, a missing locked file and a changed source byte sequence. These input checks add no linguistic or application coverage. No whole-repository or additional website self-test is claimed.

## Supplementary sense-scope source identity

The report also credits an explicit candidate sense mapping while leaving authoritative inclusion in that sense unestablished. That accepted assessment consulted nine additional files from the same pinned commit. `sense-source-lock.json` separately identifies these files by repository-relative path, pinned URL, byte length, Git blob SHA-1 and SHA-256. They total 4,962,017 bytes and do not overlap the original 70-file lock. Their source contents, including dictionary text, are not bundled.

Using the same separately obtained checkout, run this optional command from the directory containing `language/` and `fusha-source/`:

```sh
python3 -I -B language/verify_sense_sources.py fusha-source > sense-source-check.json
```

A directory containing only the exact nine supplemental files also works. This separate standard-library verifier checks source identity only and prints relative paths and pass/fail results, never source content. It does not parse those files, execute application code, or independently repeat the interpretive sense-scope assessment. Exit 0 means all nine byte bindings matched; missing or changed files fail.

The original `source-lock.json` and `verify_occurrence.py` remain unchanged: their scope is still 70 byte bindings plus 12 occurrence-data assertions. The supplement supplies nine additional source-identity checks, with **zero new occurrence-data or linguistic tests**. A fresh relocated nine-file layout passed; changed-byte and missing-file cases were rejected, and the unmodified source inventory was unchanged by verification. The full-regression, linguistic-certification and deployment limits above still apply.
