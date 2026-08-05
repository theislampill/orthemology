# PR #21 — final rereview record V2

Review chain for the Codex-blocked PR #21 repair cycle. Reviewer independence:
the implementer ran on Claude Fable 5; both distinct reviews ran as fresh-context
Opus 5 agents given the requirements and evidence surfaces only — no
implementation commentary and no desired verdict.

```text
codex owner audit:        head defe548  -> BLOCK_PENDING_REPAIR (4 findings)
fable independent audit:  head defe548  -> agree 4/4, plus additional findings
                          (orthemma p7 table + raw records; core pp1/8/11 raw
                          blocks; gallery p2 cosmetic) — all repaired or
                          recorded
same-agent adversarial:   repaired tree -> no new blocking findings (labeled
                          same-agent; gates: own-text validator pass, no
                          withdrawn-language reintroduction, scope containment,
                          typography-only manuscript diffs, guard presence in
                          all six generated mains)
distinct review round 1:  head a25a2bf  -> BLOCK (C1 gate coverage; I1
                          residual "provably"; I2 Column-N placeholder
                          regression; I3 exemption breadth; I4 ungated
                          claim-supported cells; M1-M5)
repairs:                  commits 3379a4e..265723d
distinct review round 2:  head 265723d  -> PASS. All findings verified
                          repaired with an out-of-repo mutation harness
                          (5/5 required mutations kill the gate; 5/5 prior
                          evasion probes now fail); no blocking regressions
                          in the full a25a2bf..HEAD diff.
```

Honest residuals recorded by the round-2 reviewer, accepted as non-blocking:

1. The claim-language gate is a lexical tripwire; part of its green status
   comes from vocabulary choice rather than semantic change, exactly as the
   validator's scope note discloses. Human review remains the outer gate.
2. Anchor fragility: renaming the prior-art table's header row would disable
   that table's scan (a visible structural edit). Future hardening candidate.
3. Pre-existing (carried forward, not created here): the r7e-sol arxiv
   compatibility report's header prose cites an older "authoritative source
   commit" while its machine-rewritten hash table tracks the current build.

This record is documentation added on top of the PASSed head; the commit that
adds it changes no gated artifact other than the regenerated hash/state
surfaces, and the exact-head CI run on the final push gates the result.
