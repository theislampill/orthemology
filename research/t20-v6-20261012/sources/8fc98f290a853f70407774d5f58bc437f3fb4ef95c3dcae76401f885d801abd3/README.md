# Inventory and navigation

`INPUT_IDENTITIES.json` binds all six supplied originals, nine recovered ZIPs and one recovered integration transcript. These originals are not rewritten by the handoff.

`ARCHIVE_MEMBERS.jsonl` inventories recursively retained ZIP members, including repeated and nested occurrences. Its member count is not a count of distinct results. `SOURCE_FILE_INDEX.jsonl` indexes accessible retained text/code/source files, and `HEADINGS.jsonl` gives physical-line entry points. These are mechanically generated navigation aids, not assertions that every listed proof was reviewed.

`REPOSITORY_SOURCE_LOCATORS.json` distinguishes freshly read primary ranges from inherited source paths. `READING_COVERAGE.json` records actual reading scope. The complete packet `MANIFEST.json` is the definitive byte inventory; these navigation indices intentionally do not index themselves.

Useful local searches after extraction:

```sh
python -B tools/verify_packet.py .
grep -in "Hessian\|nudge\|continuation" inventory/HEADINGS.jsonl
grep -in "shared-proof\|warranted-discrimination" inventory/SOURCE_FILE_INDEX.jsonl
```

Do not confuse the filename search results with completed research or a current GitHub status. Use the exact linked sources and their declared evidence boundaries.
