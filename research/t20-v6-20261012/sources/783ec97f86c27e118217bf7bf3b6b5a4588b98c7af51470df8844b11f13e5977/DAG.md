# Private DAG — R0F20

Do not confuse **M01–M10** integration cells with historical numbered T20 research checkpoints.

```mermaid
flowchart TD
  M00["M00: Acquire merged repo and pin currentness"]
  M01["M01: Verify source archives, per-file hashes and ZIP safety"]
  M00 --> M01
  M02["M02: Publication rights and private-path gate"]
  M01 --> M02
  M03["M03: Preflight exact additive public projection (dry-run)"]
  M01 --> M03
  M02 --> M03
  M04["M04: Apply precomputed public projection once"]
  M03 --> M04
  M05["M05: Stage files and regenerate release manifest"]
  M04 --> M05
  M06["M06: Focused repo smoke and public content verification"]
  M05 --> M06
  M07["M07: Open one PR for the additive continuation only"]
  M06 --> M07
  M08["M08: Independent changed-surface review"]
  M07 --> M08
  M09["M09: Owner-controlled merge after required CI"]
  M08 --> M09
  M10["M10: Give Dot precise immutable GitHub re-entry anchor"]
  M09 --> M10
```

## Dependency-bound execution (no quota-intensive research re-run)

| Node | Deliverable | Fail-closed stop |
|---|---|---|
| M00 | clean HEAD, baseline ancestor, fixed scientific anchor | live repo or anchored baseline has diverged |
| M01 | 23 archives + 2,821 member checks | any identity mismatch or unsafe ZIP |
| M02 | public/hold disposition; redaction acknowledgement | unresolved confidential/licensing risk |
| M03 | collision-free preimage check | dirty tree, changed owner path or unexpected baseline |
| M04 | new research/t20-live-20261009 tree | existing destination differs |
| M05 | additive staged tree; native release manifest update | unrelated repository paths modified |
| M06 | verified staged exact hashes and narrowly impacted validators | CI/source/status requirements fail |
| M07 | PR URL, HEAD SHA, diff and checks | permission denied, errors or unauthorised scope |
| M08 | review disposition and requirements | missing verification or scientific-scope promotion |
| M09 | actual merged SHA | merge not approved |
| M10 | reference to merged commit and T20 live index | no verified merge SHA |

**Research source lineage**: CP01→CP02→…→CP22 as additive (not cumulative) preservation increments. S01 is an unnumbered later additional mathematical packet. Never represent a later ZIP as containing earlier ZIPs unless its manifest explicitly establishes it.

