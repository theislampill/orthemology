# Stability of law-dependent atomic classifications

## Subject and boundary

This extension uses the actual positive-singleton support from the recovered P02 attempt-0002 formalisation. The input law changes, so the atomic-membership event itself changes with the law. Ordinary data processing cannot be applied by pretending that this is a fixed observation function.

For each measurable observation f_i, let A_i^μ be the source event that f_i has positive singleton mass under μ's pushforward. Take a countable observation family. The common event C_i = A_i^μ ∪ A_i^ν differs from A_i^μ only on a μ-null set, and from A_i^ν only on a ν-null set. This follows because each other-law positive support is countable, and its points outside the current law's positive support are singleton-null under the current pushforward.

For a countable observation family, all coordinate replacements hold simultaneously almost everywhere, yielding a common measurable representative under each law. A further checked generalisation removes the countability restriction for the distributional statement: coordinatewise almost-everywhere equality gives equal finite-cylinder probabilities, and finite-measure uniqueness extends equality to the full product sigma-algebra. This does not assert simultaneous almost-everywhere equality of uncountably indexed functions, or measurability of arbitrary uncountable conjunctions.

## Checked statement

Using event-supremum total variation (not the doubled signed-variation convention), the total variation between the complete μ-specific and ν-specific atomic-pattern laws is at most TV(μ,ν). Every fixed measurable decoder of those patterns inherits the same bound.

This is a joint distribution bound. It is stronger than listing separate coordinatewise bounds, because any measurable event or decoder in the entire countable pattern space is covered by the same constant.

Specialisations include a fixed family consisting of all finite observations and the full history observation. The resulting pattern records initial diffuse status, first finite loss, persistence and full-history atomic status. Consequently a measurable classification into initial loss, finite loss stage, residual infinity and retained full-history atom has the same full-law TV bound. The generic decoder theorem, explicit first-loss decoder, its measurability, the full-history classifier, and its atom/residual/finite-stage interpretations are all checked.

## Existing checked special cases

- TotalVariation.lean: measurable pushforward contraction and actual positive-singleton defect stability
- ResidualStability.lean: actual infinite residual event J stability, with its law-dependent events replaced by one common representative
- AtomicPattern.lean: countable joint atomic pattern and every measurable decoder
- ArbitraryPattern.lean: arbitrary-index product-sigma-law generalisation using finite-cylinder uniqueness
- LossDecoder.lean: measurable first finite loss and atom/loss/residual decoder
- HistoryClass.lean: actual P02 full-history classification and joint law bound

No coherence assumption is needed for the generic atomic-pattern theorem. Coherent refinement is needed to interpret finite losses as irreversible stages and match the CV-R decomposition.

## Limitations

The theorem controls changes of the underlying law in full-law total variation. Finite-marginal proximity, weak convergence or Wasserstein proximity alone does not imply the premise. An atomic grid can converge weakly to a diffuse law while its defect stays zero and the limiting defect is one. The theorem does not make these weaker metrics adequate.

The observation functions are shared between the two laws. Simultaneously changing source laws and observation functions needs an additional coupling or observational-discrepancy bound. The result supplies no truth, authority or normative warrant by itself.

Historical novelty has not been established. These are new mechanised extensions in this research tranche, not a claim that the underlying measure-theoretic argument is unknown in the literature.
