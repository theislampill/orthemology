# Source audit revision research packet

The main result is in RESULT.md. It gives exact conditions for dropping an old report while preserving the full-history posterior, positive audit/replacement updates, and counterexamples to two strong deletion implementations.

## Reproduce the exact controls

Run from this directory using Python 3 and its standard library:

    python3 verify.py
    python3 companions/check_triple_interaction.py

The first output should equal CONTROL_RESULTS.json as parsed JSON. The second should equal TRIPLE_CONTROL_RESULTS.json. The inputs subdirectory contains byte-identical copies of the inherited inputs, so replay does not require the prior workspace. If the original inputs remain present beside this packet, verify.py checks those originals as well.

INPUT_BINDINGS.json contains the initial eight input hashes. SOURCE_READS.json records later bounded reading and parent/sibling contributions. MANIFEST.json binds the complete packet except itself. STANDALONE_REPLAY.json records the fresh copied-directory replay.

RESULT.md contains written general proofs. Exact finite controls supplement rather than replace them. All laws are declared finite models; there is no empirical, psychological, formal-kernel, actual-warrant, protected-integration, or T20-closure certification. Any independent review lives in the reviewer's separately bound packet.
