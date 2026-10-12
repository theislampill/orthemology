# Collection launcher: final code delta review

**PASS for the exact final launcher code and the inspected configured replay checks. Final frozen-collection acceptance remains separate.**

The reviewed `verify.py` is SHA256 `3abb48646f0a592276db3ad77f13e1fd06186608eb0bcf09beef3994a4cf1e65`. Compared with the independently reviewed predecessor `61d9ddb167e7cac5f74ae36eaa04c32d08a9e7a0e16487a9ac12a299f89d375c`, exactly four lines add a full staging-path length check before archive members are written. The existing final-destination check remains. The earlier inventory, integrity, terminal-evidence and timeout repairs are unchanged.

The 13 reviewer-owned integrity/status/positive cases pass again in both normal and optimized Python modes. An additional independently constructed boundary case makes the final destination path exactly 240 UTF-16 units, with a short destination basename: the longer temporary staging path is rejected, no final directory is installed, and the staging directory is removed. The author suite was independently rerun from copied final sources: all 44 tests pass.

The configured controls recipe is also independently checked with a valid synthetic receipt and nine single-field negative cases. It distinguishes completed bounded replay, the scoped scalar result, both INCONCLUSIVE baseline outcomes, the full run count and the final resource-inconclusive mutation row. Array-length and last-row lookup are supported by the reviewed code. This is a configuration test, not a new scientific replay.

The actual completed controls and history integration receipts were inspected separately. Each recorded terminal hash matches its actual output file. Controls has nine matching terminal assertions and 166 rows; its final original mutation row has exit 1 and remains resource-inconclusive. History has six matching terminal assertions and the recorded portable source-replay result. These checks retain the component claim ceilings; completion does not convert uncertainty into semantic rejection or new proof credit.

No code-level correction remains in this assessed scope. The code executes trusted reviewed component programs and detects changes to bound inputs; it is not an operating-system sandbox for arbitrary programs. Exact final report bytes, collection inventory, source accounting and any subsequent code change still require their respective acceptance.
