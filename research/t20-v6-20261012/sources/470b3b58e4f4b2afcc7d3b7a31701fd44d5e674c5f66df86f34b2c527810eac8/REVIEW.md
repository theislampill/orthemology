# Independent review: partial quadratic rank classification

10 October 2026 UTC. Independent ordinary mathematical review, with a separately authored exact-control script. This review does not claim a formal-kernel result, field priority, protected integration, or closure authority. The parent proposed the rank classification and strengthened mixture; the investigator authored the result. This reviewer inspected their proof rather than serving as a second author. Review feedback included confirmation of the mixture witness and its variance-based nonstationarity test.

## Verdict and frozen target

**PASS: no blocking mathematical finding in the reviewed classification.** Final target bindings, replay output, and source-currentness checks are recorded in REVIEW_RECEIPT.json and AUTHOR_SNAPSHOT_BINDINGS.json. The review applies to those exact bytes, not to future changes.

The warranted sharp split is:

- Nullity d−r≤1: every normalized, full-square-positive, coordinatewise C¹ hierarchy on a positive-length interval has at least one fixed initial probability law lifting the entire path. Its coordinates have a unique global admissible continuation.
- Nullity d−r=0: every such specified path has exactly one lift, and every positive-time full moment record is determinate.
- Nullity d−r≥1: unique-law identification can fail even for genuine full-support laws with strictly square-positive records.
- Nullity d−r≥2: existence can fail at every time of one global, strictly square-positive hierarchy. The displayed example is nonstationary when r≥1; zero damping forces stationarity.

The first item requires one common law for all times and does not require uniqueness of that law.

## 1. Existence bridge and exact classical hypothesis

The unnormalization a(t)=exp(−∫₀ᵗL_v(h)dv), A_t=a(t)L_t gives A_t′(p)=−A_t(hp). Coordinate regularity suffices because multiplication by the fixed polynomial h uses only finitely many coordinates in each equation. Induction yields all higher derivatives without assuming a sequence-space norm.

For h=Σ_{i≤r}x_i², every q²hⁿ is an actual finite SOS. Backward Taylor therefore has nonnegative terms and remainder. Its n-th term yields A_t(q²hⁿ)≤n!A₀(q²)/tⁿ. In precisely the controlled coordinates, hⁿ−x_i^(2n) is an SOS with nonnegative multinomial coefficients. Hence L_t(x_i^(2n))≤n!/[a(t)tⁿ]. Since 0<a(t)≤1, the lower bound sqrt(a(t)t/n) on reciprocal even-moment roots is valid; vanishing moments have the usual infinite reciprocal-root convention.

The key imported result was independently rechecked in the primary Putinar–Schmüdgen Theorem 25, printed p. 24 of arXiv:0810.0840v1: d−1 controlled marginals give existence from full PSD; the final marginal condition adds determinacy. There is no hidden assumption of prior vector representability. The proof in that source treats d≥2. The author's separate use of Hamburger for d=1,r=0 is correct, and r=1 adds scalar Carleman.

I also rechecked the inherited exhaustion proof, rather than relying only on its headline theorem. It explicitly needs just one positive-time representative plus all joint q²hⁿ inequalities. At that time, the nonnegative exponential series yields every polynomial-weighted exponential bound needed for de-tilting. Analytic agreement extends to the whole open interval. Monotone convergence then recovers every boundary square moment and total mass one. Polarization supplies signed and mixed moments. No measurable family of representatives or hidden-coordinate exponential tail is assumed. This validates the use of the classical existence theorem in the nullity-one case.

## 2. Three uniqueness questions are correctly separated

A common normalized path fixes its normalizer through the scalar ODE and fixes its polynomial-weighted transforms on a positive interval. Analytic identity and signed Laplace uniqueness extend those transforms globally. Thus all lifts of a finite path supply the same future coordinates, even if the lifts are different.

For nullity≤1, every admissible extension itself has a lift, so uniqueness is genuinely in the full admissible class. For other ranks the author correctly restricts the inherited continuation conclusion to lifted paths. No all-nonmoment-path global extension theorem is being smuggled in.

The de-tilting map gives a bijection between representatives of any positive-time full record and whole-path lifts. Consequently particular-path law uniqueness is equivalent to positive-time moment determinacy. The universal version holds exactly at full rank, while special lower-rank paths such as δ₀ can still have unique laws.

Finally, uniqueness of continuation of a specified finite path is distinct from uniqueness from initial moments alone. At full rank, different initial laws with the same boundary moments can generate different paths. At rank zero, every coordinate path is constant even when its underlying law is indeterminate. The stated quotient F_c/∼_h respects all these distinctions.

## 3. Law ambiguity is a genuine full-support probability control

The logarithmic Gaussian calculation gives zero sine-perturbation contribution to every integer moment. Adding the same Gaussian half-mixture keeps the two hidden laws distinct, matches all their moments, and makes their densities everywhere positive on the full real line. Product with Gaussian laws in all other coordinates produces true full-support probabilities with all absolute moments.

The killing factor depends only on the controlled Gaussian block. Its normalizer is (1+2t)^(−r/2); its tilted coordinate variance is (1+2t)^(−1). Therefore the hidden difference survives at every time while every full mixed moment agrees. This proves failure of universal law identification for every nullity≥1. Full support implies strict square positivity for every nonzero polynomial. The path is nonstationary for r≥1 and stationary for r=0, exactly as claimed.

This example is not a nonmoment functional and does not establish the nullity≥2 existence obstruction. The author keeps those mechanisms separate.

## 4. Full-PSD nonmoment obstruction and uniform mixture

The source reinspection confirms the requisite classical input: a normalized square-positive functional on the entire R[u,v], not a truncated pseudo-moment list, with value −1 on F=1+u⁴v²+u²v⁴−u²v²≥0. Its full infinite positivity remains an imported theorem. The exact controls neither construct it nor certify all its moment matrices.

Evaluation of the controlled coordinates and all but two hidden coordinates at zero is a unital algebra homomorphism E. Thus B=Λ∘E is square-positive and B(hp)=0. Any representing law would project to a representative of Λ, which is impossible. This proves the stationary necessity direction already.

The strengthened functional A_t=(13/14)B+(1/14)G_t uses the actual standard-Gaussian killed functional G_t. Its derivative is −A_t(h·), and its mass (13+Z_r(t))/14 is bounded below by 13/14. Quotient differentiation therefore gives the normalized hierarchy globally, with the required boundary regularity.

For any nonzero q, the weighted Gaussian is positive on an open set where q²>0; hence A_t(q²)>0 for every finite time. The Gaussian expectation of F is exactly 6. Since 0<Z_r(t)≤1,

    A_t(F)=−13/14+(3/7)Z_r(t)≤−1/2.

This is a uniform nonrepresentation witness for one fixed global path, including t=0. It is stronger than an arbitrarily-long-finite-horizon family.

For r≥1, h−L_t(h) is a nonzero polynomial, so strict square positivity gives L_t(h)′=−L_t((h−L_t(h))²)<0. For r=0, h=0 and the mixture is stationary. The general witness-based ε=δ/[2(δ+M)] variant is also valid because F≥0 and e^(−th)≤1 imply G_t(F)≤M.

## 5. Affine quadratic transport and boundaries

For a symmetric PSD Q, the affine quadratic xᵀQx+bᵀx+c is lower bounded exactly when b∈Ran Q. Completing the square, diagonalizing Q, and positively rescaling the active eigenvectors give an invertible affine normal form with exactly rank(Q) controlled coordinates. The constant term cancels from normalized dynamics. Pullback and its inverse preserve the full polynomial algebra, square positivity, all absolute moments, representability, determinacy, and law-lift multiplicity. The nullity classification therefore transports exactly.

The author correctly excludes a nonzero linear term in a null direction. The supplied-polynomial-automorphism corollary is likewise valid because both maps preserve polynomials; it is not a classification of arbitrary noncoercive polynomials. Finite-dimensional, all-degree, real commutative hypotheses remain essential.

## 6. Executed evidence and limitations

- The independently authored check_independent.py checks controlled SOS differences, factorial growth, rank edge cases, exact Gaussian monomial recursions including rank zero and odd moments, the source witness's finite evaluation and Gaussian expectation, normalization, strict-decrease identities, the logarithmic cancellation, and a non-diagonal affine quadratic normal form.
- Negative controls distinguish two hidden directions from the d−1 hypothesis, reject an incorrect Gaussian killing scale, and show why an excessively large mixing weight loses the displayed negative witness.
- The author controls are replayed in a separate copy with copied predecessor inputs. No author or predecessor file is edited by the review.
- The fresh isolated author replay passed all 1,232 controls. The separate reviewer checker passed 1,605 exact checks, including 1,309 Gaussian monomial recursion cases and 14 frozen-file integrity checks. Integrity bindings and executed counts appear in the receipt and JSON outputs. They supplement the ordinary proof; they do not formalize the imported measure theorems or infinite functional.
- Source claims are reinspections of inherited material. The primary Theorem 25 page was also checked visually. The textbook was checked through parsed primary text, with no successful page-image verification claimed.

The historical truncated-functional exclusion was separately read and hash-bound: Controls.lean proves Λ((x³−x)²)=−96 for that particular zero continuation, and its retained independent review confirms the degree-scoped boundary. This is an exclusion guard, not a premise of the rank theorem or a claim that every extension of those truncated moments fails. No unrelated Lean build was repeated.

No mathematical repair is required by this review. Broader literature novelty, arbitrary-polynomial classification, all-rank nonmoment continuation existence, constructive realization of Λ, finite-degree certification, and formal-kernel validation remain outside the reviewed claim.
