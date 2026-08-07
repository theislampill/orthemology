# PMR-007 Frontier Round 13 cold audit — fault-robust local agreement and restorative certificates

```text
audit relation: same-model procedural audit over frozen V1 hashes
external human review: false
independent model-lineage review: false
overall disposition: PASS_WITH_NONBLOCKING_NOTES
```

## FRLA-1

`PASS.` The correct-view graph is the equality closure of the local protocol
variables. Every scenario clique forces all correct tokens in that scenario to
share one output, and reappearance of a token propagates equality across
scenarios. Hence one output must label each connected component. The exact
feasibility condition is therefore the nonempty intersection of the scenario
output sets assigned to that component.

The sufficiency construction is total on all appearing tokens and can be
extended arbitrarily to unused views. Correct-member nonemptiness prevents an
undefined scenario component. Faulty outputs are not silently constrained; all
fault-generated observations relevant to correct behavior are required to be
inside the scenario-local views.

## Executable check

`PASS.` The frozen checker used three agents, two local views per agent, and two
output objects. It generated 78 membership/view/output scenarios and compared
the component criterion with direct enumeration of every deterministic local
protocol on:

```text
one- and two-scenario families exhaustively;
reproducible three-scenario samples;
3,155 total families.
```

No mismatch occurred. A separate monotonicity test checked 4,632 supersets of
infeasible pairs and found no feasibility resurrection.

The three-scenario sampling is not itself an exhaustiveness claim. The proof is
exact; a fresh rereview should enlarge that finite class rather than promote the
sample count into general validation.

## Fault/membership and public-evidence controls

`PASS.` The two-scenario model is a genuine hidden-central-chooser obstruction:
each scenario separately has a common admissible output, but one correct agent
reuses the same view across two different correct-member sets whose required
outputs are disjoint. The shared token joins the scenario cliques, making the
component intersection empty.

The common public bit repairs only because it is incorporated into every
correct token and differs between the scenarios. The packet correctly requires
truthfulness, common availability, source/currentness binding, and protocol
admissibility. It does not treat a private or forgeable bit as common evidence.

## Warrant and restorative scope

`PASS_WITH_NONBLOCKING_NOTES.` Treating outputs as action-certificate objects
correctly blocks action-only agreement from laundering incompatible warrant.
The Candidate-B application is one-step only. It does not establish dynamic
reach-and-stay, causal landing, bypass resistance, reread closure, or objective
target adequacy.

Nonblocking burdens:

1. the scenario family must be complete for every fault, message, membership,
   source, version, and snapshot pattern claimed;
2. deterministic one-step agreement does not settle randomized,
   asynchronous, fair, or repeated protocols;
3. common output does not itself make the certificate true or independent;
4. the component construction assumes the local view is the complete protocol
   information state for the declared step.

## Ancestry, novelty, and Candidate-C firewall

`PASS.` FRLA-1 is an equality-constraint specialization of Round 4 LIF-1 and
the preserved AR2 local-uniform synthesis family, combined with Candidate A's
complete warranted-output objects. The component elimination is standard. Its
value is the exact fault/membership closed form and cross-lane placement, not a
new general Byzantine-agreement theorem.

Operational agreement on one root label or source certificate does not prove
numerical unity, modal persistence, metaphysical grounding, or source truth.
The packet preserves that Candidate-C firewall.

## Result

```text
blocking findings: 0
nonblocking scenario/protocol/authority notes: 4
repair required: false
fresh rereview required: true
PMR-007 may close: false
```
