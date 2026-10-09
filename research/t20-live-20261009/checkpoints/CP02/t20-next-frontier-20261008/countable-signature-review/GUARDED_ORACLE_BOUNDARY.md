# Three distinct guarded-oracle claims

8 October 2026. These claims use one issued profile at a time. They do not cover a different oracle that returns the aggregate law of a pooled random mixture of profiles, or direct access to hidden route records.

## 1. No total finite-stopping exact census in the general deterministic class

Let a baseline be any finite guarded inventory. It may contain a common productive unguarded route; no empty-world assumption is needed. Suppose a deterministic exact-query procedure stops on that inventory after n queries. Its queried issued subsets may be infinite, and its chosen attenuation rates and subsequent queries may depend on every earlier exact response.

Exclude the finitely many indices used by the baseline. Infinitely many fresh indices remain. Each has one n-bit membership pattern across the queried profiles, so two fresh distinct indices i,j share a pattern. Add a route with positive support {i}, absence guard {j}, and a nonempty visible output. It is disabled at every profile in the transcript. Every endpoint law and every derived answer therefore stays unchanged, at all queried attenuation rates.

Inductively the deterministic procedure follows the same history and stops with the same output on both inventories, which are different. Thus an always-correct procedure cannot stop after finitely many queries on every inventory in the unrestricted finite guarded class. The argument requires a class closed under the hidden-route addition; it is not a theorem for every narrower promised class or known exact route count.

The computational witness can use the first 2^n+1 nonexcluded indices. Freshness is available at proof level even when a particular helper searches from index zero without an exclusion parameter.

## 2. No uniform fixed query budget for randomized single-guard identification

Fix a known positive support {A}, one route and one visible output. Let the sole unknown be a guard index j chosen from M distinct candidates outside {A}. Each exact query has at most two possible answers: the route is disabled, or it is enabled and has the known support-A response. Varying its allowed rate or the next profile adaptively does not add a third response for this model family.

For any fixed internal random seed, a procedure making at most N queries has at most 2^N response leaves. An output at a leaf can correctly name at most one j. Under a uniform prior on the M candidates, its success probability is at most 2^N/M. Averaging over seeds preserves the inequality. Consequently a uniform success guarantee of 2/3 requires 2^N >= 2M/3, and no fixed finite N covers an unbounded guard-index family.

This argument chooses a fixed finite family of models before randomization. It avoids the invalid inference from a seed-dependent pathwise pigeonhole witness to a fixed-model error probability.

## 3. Variable-budget identification may succeed in a promised narrower family

The preceding bounded-budget result does not exclude eventual finite identification when the family is promised to contain exactly one known-positive-support route and exactly one unknown guard index. Tail-threshold queries can first bound that index; membership/binary queries can then locate it. For each fixed finite index, this may take finitely many queries, with no uniform bound over all indices.

The general census obstruction has a different source: without such a completeness promise, a fresh extra guarded route remains compatible with every finite deterministic transcript. Likewise, no conclusion is made against infinite collections of profiles, limiting inquiry, known finite signatures, or additional observations.

These are information-channel distinctions inside the declared model. They do not establish real infinite agents, source-admissible broadcast interventions or the causal reality of the route representation.
