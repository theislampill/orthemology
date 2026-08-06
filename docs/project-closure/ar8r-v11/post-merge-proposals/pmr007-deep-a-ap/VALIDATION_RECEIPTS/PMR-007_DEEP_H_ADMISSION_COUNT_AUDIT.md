# PMR-007 Deep Round H admission-count audit

## Disposition

```text
REPAIR_REQUIRED_AT_ADMISSION_METADATA_ONLY
```

The distinct rereview result contains `normalized_posterior_cases: 12288`. The first admission overlay incorrectly recorded `36864`, multiplying the executed case count by the three outcomes a second time.

The mathematical result and rereview PASS are unchanged. The incorrect overlay and hash receipt are preserved as rejected metadata evidence. A corrected V2 admission overlay must use the exact executable count and receive a new admission hash receipt.
