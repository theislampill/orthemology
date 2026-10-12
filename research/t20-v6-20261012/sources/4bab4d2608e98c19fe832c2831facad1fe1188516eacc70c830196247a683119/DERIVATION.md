# Rational cut boundary controls

11 October 2026 UTC. Root review preparation, ordinary mathematics, not a new general classification or kernel result.

Write H(k,n) for heavy-cylinder mass, M=sup_k inf_n H(k,n), and use the inherited finite probability semantics. Exact cut normal forms must preserve rational slack:

- M ≥ a iff for every rational q<a there exists k such that every n has H(k,n)≥q (nonnegative q suffice when a≥0).
- M > a iff there exists rational q>a and k such that every n has H(k,n)≥q.
- Negating these supplies the complementary cuts. When defect=1−M, its strict and non-strict cuts reverse the mass cut. Normal-form upper bounds do not themselves prove arithmetical hardness.

A concrete law exposes why the rational slack in the strict cut is necessary. On Cantor space let μ=(1/2)δ_(000…)+(1/2)λ, where λ is fair Bernoulli product measure. Its atomic mass is exactly1/2. At heavy threshold1/2 (k=1), for n≥1 the all-zero cylinder is the only heavy cylinder, with mass1/2+2^(-n-1); the other cylinders each have mass2^(-n-1)<1/2. At n=0 total mass is1. Therefore every finite H(1,n)>1/2 although their infimum is1/2. Replacing M>a by ∃k∀n H(k,n)>a incorrectly accepts this exact law at a=1/2.

This is an equality/limit guard for the original cylinder semantics. No new philosophical consequence or independent classification credit is claimed.
