# Repository-native v5 replay

This directory is a compact active-source projection with a **new integration adapter**. It is not the original V4/V5 packet and does not claim original-packet recovery. Original source records and research ceilings are preserved.

From the repository root, with POSIX CPython 3.11+; this executor uses Ubuntu CPython 3.12.3. Pinned formal build requires Lean4 4.19.0 and exact Lake manifest dependencies. No compiler substitute.

```sh
python3 -B experiments/orthemology-v5/verify_repository.py --check
python3 -B -m unittest discover -s experiments/orthemology-v5/tests -v
python3 -B experiments/orthemology-v5/verify_repository.py --output ../orthemology-replay-new
```

0 strict runtime+kernel PASS; 1 failure; 2 runtime PASS/kernel OPEN; --check is static only. Exit 2 is not a full success. No mocked compiler can grant kernel credit.

The strict adapter executes 183 tests in each mode, both 335,744-case censuses, 6 legacy and 10 V4 intended mutations, 12 scenarios, and 9 mathematical plus 3 staging probes in each mode. It stages a complete formal project from the one active Lean source owner before invoking the preserved strict formal checks. Evidence goes to a fresh directory outside the checkout.

The frozen [formal dependency lock](formal_project/lake-manifest.json) requires real toolchain/dependency availability; no automatic installation is performed by this adapter. The twelve shared modules live in source/lean, with the Apache notice and source/LICENSES/Apache-2.0.txt retained.

Relative links inside exact inherited ledgers are original-packet locators. SOURCE_MAP records their custody disposition; unavailable off-Git evidence is not a working public download.

See [provenance and status](../../docs/provenance/v5-consolidation/README.md), [parity contract](../../docs/provenance/v5-consolidation/VERIFIER_PARITY.json), and [integration guide](../../docs/architecture/V5-INTEGRATION-GUIDE.md). A3F and A3G remain PARTIAL. No A7/A8/A9 credit is created by running this command.
