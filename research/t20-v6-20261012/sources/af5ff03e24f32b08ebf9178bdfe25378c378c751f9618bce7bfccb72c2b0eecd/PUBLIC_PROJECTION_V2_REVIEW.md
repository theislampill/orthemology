# Independent public-projection check

Date: 2026-10-02 UTC.

## Result

**Verified: the exact public archive is a faithful, self-contained scientific projection of the accepted v2 checkpoint.** This is a packaging sidecar; it does not change the accepted scientific source, broaden the v2 claim, or declare the projection to be the complete original packet.

Public projection manifest SHA-256: `10a05fa51248e267ba1aaac8e141d06f556e504163699cfee57237c19cdcf842`.

Public ZIP SHA-256: `2ae289057d4e414d6ca5e6478369dfa64cfb4f89cdfc10c1d85a6935fb638a08` (275,323 bytes).

Accepted source manifest SHA-256: `a795122fa0d4c3d127371e22599bf23a65a9a546d2abdae8d0d96962682416ae`.

## Mapping, exclusions and complete archive inventory

The reviewer independently compared every public member, not only the declared scientific files:

- 127 retained scientific source/argument/contract/test/evidence files are byte-for-byte identical to their accepted v2 originals, with equal recorded original/public lengths and hashes.
- Six exclusions are exactly the five declared administrative documents and the original top-level package manifest. Retained plus excluded paths exhaust the original 132 bound files plus that manifest, without omissions or double counting.
- 24 independently produced review/evidence files are exact copies of the indicated reviewer originals.
- Five new packaging files are explicitly identified and separately hashed. They are not passed off as original scientific material or counted as new theorems.
- These groups plus the new projection manifest equal all 157 ZIP members. There are no unmanifested, excluded, duplicate, out-of-root or symlink archive payloads.

The public README correctly labels the result as a subset and distinguishes upstream identity manifests from the public archive inventory. It also discloses that historical review scripts retain their original paths; the primary scientific replay is the self-contained entry point. No administrative text excluded by the mapping was found under another archive filename.

## Independent portable execution

The reviewer copied the projection to a separate tree, verified it against the accepted original v2, and ran all four packaging-verifier tests successfully from the package directory.

The reviewer then ran unchanged `replay.py` with official Lean 4.19.0 into a fresh output directory, deliberately omitting `--predecessor-root`. The fresh kernel compile, C generation, native link and run succeed. All 88 native assertions and seven wrapper checks pass, including the original finite race domains. Every built Lean source hash and all five native full-state/byte artifact hashes equal the independently accepted v2 replay.

The standalone receipt correctly records `predecessor_verification: null`: bundled source bindings are checked, but an absent complete upstream tree is not represented as verified by that run. The separate review had already verified all 63 original predecessor records, and rechecked them unchanged after the projection test.

The public source tree and ZIP were rehashed unchanged afterward. The original complete v1 and v2 freezes/ZIPs also remain unchanged.

## Limits

This verifies the named immutable archive and its mapping. The packaging verifier checks declared members and named exclusions; the review’s independent ZIP inventory check establishes that this exact archive contains no additional files. It is not a general privacy scanner for arbitrary later modified workspaces.

The conditional scientific acceptance and all its external source, grant, authentication, atomicity, root-support, time, service and compiler/runtime assumptions remain unchanged. There is no new physical deployment, real permission, general Python refinement, N2/T0 result, R5 defeat, or whole-program closure.

## Evidence

- `verify_public_projection.py`, `PUBLIC_PROJECTION_TERMINAL.log`
- `PUBLIC_PACKAGING_TESTS.log`
- `public-replay-v2/REPLAY_RECEIPT.json` and fresh compile/link/native logs
- `PUBLIC_PROJECTION_V2_RECEIPT.json`
- Complete-source acceptance: `REVIEW_V2.md`, `REVIEW_V2_RECEIPT.json`

This sidecar does not need to be inserted into or change the already verified public archive.
