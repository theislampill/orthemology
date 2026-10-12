# Python-version attribution correction

This source-neutral note corrects one unsupported host-version attribution in
`SOURCE_V3_WRAPPER_REVIEW.md`, SHA-256
`996573dc9603f06cd41041d9433e518150bc6e8298f884537363eb8d7a9c728c`.

The sentence identifying the tested host as “Linux/Python 3.11” was not supported
by a recorded interpreter-version check. The independent replay invoked `python`
but its immutable receipt records no Python version. That specific 3.11
attribution is withdrawn. A subsequent direct check on 2026-10-02 at 22:22 UTC
reported Python 3.12.14 at
`private-locator:915d29ee128338d1c948`.
That later observation is not substituted retroactively as recorded evidence
of the original replay's interpreter version.

The review's tested-platform statement should therefore read: Linux, using the
host Python interpreter and the exact supplied Lean 4.19.0 distribution and
Mathlib/cache bytes. No particular Python minor-version compatibility test is
credited by the independent replay receipt. The main packet README's own
“tested with Python 3.11” statement is likewise not established by this
independent review; retain it as an unsupported historical documentation claim
unless separate author evidence is supplied.

All actual verification results remain unchanged: the exact extracted source-v3
ZIP replay completed with shell exit 0; all 42 positive source stages, 88
scientific and 18 reviewer axiom audits, five intended mutant rejections, and
before/after source/compiler/cache checks passed. The source ZIP remains
`ebdc889de82056029b16edb65de4af5c5503b0d83f7b49977f6340cac27c950b`, with inner
manifest `38822e275751da5bcd9d7f3eab7776e373dba662f64bcc7cb27a654a962e5ad2`.
The independent replay receipt remains
`596e7263fe3ecf3ab6fa1cc1c52e914c4de6949fb2941fbc360d3b6a6a355336`.

This note changes no source, proof, dependency pin, replay outcome, archive byte,
model premise, canonical state or release authority. Preserve the original
immutable evidence and deliver this correction alongside it.
