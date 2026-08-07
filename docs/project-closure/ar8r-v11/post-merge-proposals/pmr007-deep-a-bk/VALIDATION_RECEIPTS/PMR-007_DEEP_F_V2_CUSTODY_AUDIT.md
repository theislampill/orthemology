# PMR-007 Deep Round F V2 source-custody audit

## Disposition

```text
REPAIR_REQUIRED
```

## Blocking finding FPF-F02 — one registered locator phrase did not match the supplied bytes

The source hash matched, and three El-Tobgui locator phrases plus every al-ʿUjayrī phrase matched. One El-Tobgui phrase was normalized as:

```text
healthy fiṭra has not been tampered
```

but the supplied Markdown bytes join the transliterated token and the following verb:

```text
healthy fiṭrahas not been tampered with
```

The failed source-custody result must remain preserved. The locator check must be repaired against the actual bytes rather than reported as PASS by intention.

This defect does not change the mathematical content of V2, but it blocks the source-custody admission chain.
