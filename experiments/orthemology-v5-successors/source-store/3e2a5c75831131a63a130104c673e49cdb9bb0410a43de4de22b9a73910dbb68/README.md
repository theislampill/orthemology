# Independent Orthemic certificate-calculus review

This companion records independent scientific-source review, cold replay, and additional executable controls for the exact author packet named in ACCEPTANCE_RECEIPT.json. The review concerns finite certificate checking and common lawful almost-sure policy existence on exact rational inputs. It does not approve deployment or broader foundational claims.

Read INDEPENDENT_REVIEW.md for the result, proof ownership, admission boundary, and trust limits. Evidence includes the fresh public replay summary, the reviewer's stronger compiler/cache identity check, and five separately derived checker mutations. No author or historical custom compiled object was credited in the original independent cold review.

## Replay

The companion does not duplicate the author's scientific source archive. Extract the exact author packet identified by both manifest digests in the receipt.

For source-only checks:

    python replay_review.py --author-packet /path/to/author-packet --verify-only

For a fresh one-lane replay of the complete author packet followed by the independent tests:

    python replay_review.py --author-packet /path/to/author-packet --lean-bin /path/to/lean/bin --mathlib /path/to/mathlib --mathlib-archive /path/to/exact-mathlib.tar.gz --out /previously/absent/output

The archive option can be omitted for the author's supported clean pinned Git source route. No downloads occur. The output must be outside protected inputs. Each Lean command uses -j1 and a 180-second wall cap. No heartbeat override is added: the eight new modules use defaults, while two unchanged inherited sources retain their existing 800000 settings. Four deliberate mutation guards in the author replay and five independently derived checker mutations are expected to fail; unrelated failures do not count.

An already successful consumer-local cold author replay can be supplied with --core-replay. This mode rechecks the exact source identity and all 95 production object hashes before compiling the independent controls. It is explicit receipt-qualified reuse, not a claim that those 95 modules are rebuilt in that invocation. The original independent review did rebuild them from source.

The portable source verifier trusts official external Lean/Mathlib objects. It does not source-bootstrap the compiler/library, prove binary refinement, or validate a raw-byte parser. The stronger environment-specific distribution/cache comparison recorded in this review is separate from that portable trust boundary.

## Submission boundary

The checker accepts finite typed AST data. Independence from synthesis does not authorize running arbitrary Lean or Python supplied by a certificate producer. A recipient needs a trusted constructor or decoder that enforces finite indices and AST conditions. These replay scripts execute the exact reviewed scientific source package; they are not a verified wire-format parser, upload service, or untrusted-producer code runner.

The original full portable replay ran on author v2. Final author v4 has byte-identical scientific/control sources; the wrapper changed only a resource-reporting metadata literal, with identical commands, controls, order and budgets. Documentary/custody changes and that exact wrapper bridge are recorded in the receipt. The optional qualified-core mode accepts the qualified v2 result or a fresh v4 result; neither is misreported as a full execution of different wrapper bytes.
