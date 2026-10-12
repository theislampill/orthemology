# Independent digest-bound review: grouped count/calibration invariants

## Verdict and scope

**PASS** for the mathematical claims, declared observation model, rational-node constructive decoder and membership check, and population-level scale corollary in the exact author bytes recorded in `REVIEW_RECEIPT.json`.

This is an independent scoped mathematical review. It does not grant owner acceptance, release, protected integration, empirical/source certification, or T20 closure. The binding is to the named result, corollary, control script and output, rather than any future contents of the author directory. Later changes require a new binding.

The reviewer read both result files in full, independently rederived their claims, inspected the author control script, replayed that script from a review-only copy, and implemented a separate exact-rational control suite. Only files inside this review directory were written. The supplied frozen global-calibration manifest hash and the required predecessor result/process hashes were checked before and after the independent controls.

## Mathematical assessment

1. **Interior grouped equivalence.** The full grouped endpoint law is the mixture of Bernoulli product laws. Its exchangeable count law is binomial-mixture data and determines all moments through that group length. With both competitors bounded by C atoms, a signed difference has at most 2C nodes, and the Lagrange/Vandermonde argument through degree 2C-1 is valid. The author correctly limits this statement to the bounded competitor class and separately describes the degree-2s positive support certificate.

2. **Rational scale and primitive integer signature.** At an interior survival value, count-to-node mapping is strictly decreasing, so sorting fixes the positive-count rank and associated weight. Atom one identifies zero mass. Matched nodes imply common positive rational count ratio by logarithms. Dividing the first support by its gcd and applying Bezout makes the second scale an integer. Thus two supports are integer dilations of one unique primitive vector, while their direct ratio need only be rational. The zero-only case is separate, and no gcd-one premise is inferred from the data.

3. **Prior effects and pointwise feasibility.** The exact upper-bound candidate set is 1 through floor(M/max(v)); a supported maximum exactly equal to M is a different premise. At a single interior command, a scale satisfies the error band exactly when its forced actual rate is within eta of the command. The piecewise-linear extension proves sufficiency without violating monotonicity, endpoints or the uniform band. The clipped, root-free rational test is equivalent.

4. **All-command and adaptive invariance.** Pointwise power reparameterization preserves static monotone endpoint calibrations, continuity and strict monotonicity when present, but does not automatically preserve a stipulated error band. Equality holds componentwise, so matching latent ranks and fresh endpoint randomness gives equality of all adaptive and stopped grouped transcripts under the stated complete conditional kernels. Merely equal one-trial marginal means would be weaker. Common calibration across components and held-count conditional independence are correctly declared as premises.

5. **Boundary and failure cases.** The zero-only law has no positive primitive vector. At survival one all count laws collapse to the no-hit atom; at survival zero only zero mass survives. The author's nondecreasing step-map example shows that endpoint preservation alone does not supply any interior command. The inherited shifted two-component collision, the fresh-resampling counterfeit with calibration deviation 1/8, and the label-dependent-calibration example each break a different necessary premise and are mathematically correct.

6. **Constructive rational decoder and exact membership.** The rational-node contract excludes the zero-count atom one and requires ordered distinct nodes in (0,1). A denominator prime has the same nonzero signed valuation at every node under the common-power promise. Primitive normalization follows from the gcd of those valuations. Bezout reconstructs the rational base; checking that base and every integer power certifies membership rather than merely guessing ratios. Domain, order and sign checks reject malformed inputs. The source program's power and sorted-node checks also enforce increasing reconstructed exponents. Arbitrary real calibration and rational weights do not by themselves establish this input contract.

7. **Computability and sampling boundaries.** The new two-component gcd-one Cauchy countermodel correctly localizes its queries to the fixed command and does not import the predecessor's unrelated one-component histogram obstruction. Its limiting scalar nodes support the finite-transcript impossibility argument for arbitrary-valid approximation replies. The rare-component caveat and the absence of a uniform sampling guarantee are correctly separated from exact population identifiability. The result does not claim a bit-complexity or approximate rational-recognition algorithm.

8. **Faithful population scale reduction.** With primitive vector and weights fixed, F is continuous and strictly increasing despite possible vanishing derivative at zero. The mean curve determines b=F^(-1)(m), and b then determines all mixed-command held-group component kernels. For a full known curve, the only candidate calibration at scale d is 1-b^(1/d); the uniform band must be tested over the entire command domain. This is an observational reduction, not a physical calibration readout.

9. **Sharp general-pair radius.** The midpoint parameterization gives continuous strictly increasing endpoint-preserving rate maps with opposite errors (u^d-u^e)/2. Differentiation yields `theta(d,e)=[(e-d)/(2e)](d/e)^[d/(e-d)]`. At that radius the scalar bases match identically. Below it, the maximizing midpoint command gives disjoint A^d and B^e intervals, and F preserves separation. Necessity does not silently assume continuity of every admissible nuisance map.

10. **Scale catalogue.** For D>=2, the final adjacent pair D-1,D supplies the all-command ambiguity threshold eta*_(D-1). Below it, the frozen common midpoint command separates all pure-scale intervals, and F preserves their order. The author correctly transfers the population threshold while declining to import pure-count sample gaps unchanged. The transformed gaps depend on F and on the fixed primitive weights; estimating an unknown signature is another problem. D=1 is correctly treated as no remaining scale ambiguity.

Details of the independent proofs, including full-curve feasibility and the oracle obstruction, are in `INDEPENDENT_DERIVATIONS.md`.

## Corrections and clarifications before binding

No substantive counterexample to the final theorem or corollary was found. The review requested and the final text adopted two precision changes: distinguishing the ordered Bernoulli-product mixture from its binomial count law, and explicitly excluding atom one from the positive-count rational decoder. The review also requested explicit endpoint-collapse formulas. The final binding includes the resulting boundary statement.

Other important boundaries were added or made explicit during author/reviewer discussion: a discontinuous monotone calibration need not have any interior survival command; calibration must be common across latent components; rational weights do not imply rational moments at arbitrary real calibration; and the approximation-oracle obstruction concerns two-component primitive signatures at a fixed command. These delimit the theorem rather than weaken its proved interior conclusion.

## Controls actually run

- **Author replay:** all 14 control families passed from a byte-identical script copied into this review directory. The reproduced JSON output is byte-identical to the author output. The families include 385 rational primitive decodings, 252 finite-horizon equivalent world pairs, malformed-input rejection, calibration feasibility, general-pair power bounds, the catalogue reduction, and algebraically certified Cauchy-countermodel intervals.
- **Independent implementation:** 33,266 exact assertions passed. These check primitive gcds, noninteger direct rescaling, full binary word/moment equivalence, Lagrange interpolation identities, rational-node membership, the shifted moment collision, fresh and held resampling behavior, label-dependent counterfeit laws, endpoint collapse, pointwise-band extensions, general-pair power maps and derivative signs, and transformed scale separation.
- **Adaptive controls:** a separate outcome-dependent protocol with a randomized policy seed and early stopping was exactly enumerated at four scale pairs and three horizons. Both worlds' complete stopped transcript laws agreed and normalized exactly.
- **Digest guard:** the required frozen inputs were unchanged before and after controls. `verify_receipt.py` checks every bound artifact, replays only review-local scripts, then verifies all digests again.

The independent feasibility control initially used an incorrect expected set for its own test constants, 1/2 command, (3/4)^12 base and eta=1/4. Exact evaluation corrected that expected set to {3,4}; no author theorem or author data changed. The final suite and receipt use the corrected expectation. This was a reviewer test-fixture correction, not a theorem failure.

Finite controls are diagnostics. Universal validity rests on the arguments reviewed above, not on the number of enumerated assertions.

## Exclusions

No review here establishes actual latent persistence, common calibration, route independence, physical route identity, productive ownership, source perfections, empirical intervention eligibility, numerical stability, uniform finite-sample mixture reconstruction, new field-wide priority, protected repository integration, or project closure. No predecessor was amended. No additional semantics follow from matching the scalar observation model.
