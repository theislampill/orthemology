# Execution and acceptance notes

Replay uses the pinned official Linux Lean distribution on a trusted Linux-compatible host. Python, the host and the operating system are not attested by this artifact. Process-group cleanup in the acceptance driver is POSIX-specific.

The exact source ZIP was independently replayed from its packaged bytes in a fresh extraction and build. The companion's tested entrypoint, reviewer controls and historical inputs are byte-identical here; acceptance records were appended afterwards. The final companion ZIP is checked by extraction/inventory equivalence, without circularly claiming that it certifies its own hash.
