# Independent review summary

The reviewed V2 semantic snapshot has SHA256 9afcbf0c91b695c1f27f36424e00d74b2bfc06b16231122c06e08d47b5289ff7. Review passed the narrowly stated retained-standard checker experiment, the evidence-class transport results, and conditional draft repair.

Two wording problems were corrected before V2 was accepted: the actual source-file recovery is distinct from the constructed C0-to-C1 experiment, and the implemented command fields are distinct from the external root/commitment interface.

The review also identified and preserved an operational scope gap: the draft-repair transition never changes an installed criterion. An explicit criterion-installing successor is required before that stronger result is claimed.

Source, grant and actor records are trusted inputs in the model; the checkers do not authenticate themselves. The mathematical and code results do not consume the programme's necessary-source or essential-truthfulness hypotheses.

The independent execution results were: 25 unit tests passed; 393,216 bounded state/command pairs with 480 applications and 392,736 rejections; 393,216 shared Python/Lean output projections with zero differences; nine central Lean theorem axiom lists empty. Additional independent probes checked a complete successful state, 26 isolated guard perturbations, and 256 small evidence/relation configurations.

A minor source-interpretation precision is retained: Abadi et al. leave timestamp/lifetime freshness checks outside their formal logic; that logic does not establish the live freshness assumptions used by a deployment.
