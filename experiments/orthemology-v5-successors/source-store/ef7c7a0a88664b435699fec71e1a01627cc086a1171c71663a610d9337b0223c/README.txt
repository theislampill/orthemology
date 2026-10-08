Modal union source certificate package v2

Status: author-verified; awaiting root's independent replay and acceptance.
The mathematical Lean sources are byte-identical to v1. The changes are the
portable harness's output guards, explicit --trust=0 and their regression tests.

Run with the official Lean 4.19.0 executable and a FRESH output directory OUT:

LEAN_BIN=/absolute/path/to/lean ./replay.sh /absolute/path/to/OUT

OUT must not exist, must have an existing parent, and must be outside this
sealed input tree. Canonical path checks include symlink aliases. If no OUT is
supplied, the default is the sibling path ../modal-union-replay-v2; it too must
be fresh. Reusing a previous output is refused before any writes. No historical
logs are overwritten, and no new output directory may be created in this input
tree. Directory creation is atomic, so a destination appearing after the guard
is also refused.

The script creates a temporary module directory and explicitly invokes all
three green modules and the false-claim checks with --trust=0. It audits all
42 authored theorem dependencies and requires exactly three semantic decide
rejections for the intentionally false claims. Source hashes and results are
written only to the newly created OUT. Its temporary build is removed afterward.

The v1 recipe did not explicitly select --trust=0; this package does not
retroactively attribute that recipe to v1. V1's archive, manifest, source files
and previously retained generated objects remain unchanged in their old folder.

Run the guard and normal-replay regression suite on disposable source copies:

python3 test_harness.py --source /absolute/path/to/this/input \
  --lean /absolute/path/to/lean --record /fresh/outside/path/guard-results.json

The record must be fresh and outside the source tree. Tests compare all source
bytes and paths, plus historical output sentinels, before and after each
refused request. They also verify a normal fresh replay from a separate working
directory. No Mathlib or other external package is required.

STATEMENT_CONTRACT.txt pins the formal premise language. AXIOM_AUDIT.txt states
standard logical dependencies. SOURCE_ONLY_MANIFEST.json lists the exact input
bytes. VERIFICATION_RECORD.json records the v2 recipe and author checks.

These proofs verify conditional graph/equality claims and finite models. They
do not establish actual modal admissibility, source provenance, a theological
premise, physical enactment, or canonical repository adoption.
