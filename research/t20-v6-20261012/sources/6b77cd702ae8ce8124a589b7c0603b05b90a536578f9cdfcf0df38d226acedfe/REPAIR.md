# Positive repair: exact nonlinear coordinates of a belief-state instrument

11 October 2026 UTC. Additive application note; the frozen main report and its prior freezes are unchanged. The parent supplied this repair and its interpretive guard. The construction is inherited conjugacy/predictive-state reasoning, not a new Markov-kernel or filtering theorem.

## Result and domain

The main report excludes, in general, a fixed passive channel on the original finite hidden-state labels whose likelihood rows generate all the powered branch updates. It does **not** exclude a same-outcome Markov kernel whose state is the entire transformed belief representation.

Fix n finite hidden states, positive reference π, exponent a>0, and finitely many strictly positive observation likelihood rows L_o with Σ_o L_o(i)=1 for every i. The experiment is the fixed passive channel, applied successively under its declared conditional observation model. Define the escort homeomorphism F=R_a^π of the probability simplex and its inverse H=R_(1/a)^π. Here q=F(p) is a **coordinate representation** of the original probability law p, with target-probability readout H(q). It is not silently a replacement probability law for the same original target.

For each outcome o put

    g_o(q)=Σ_i L_o(i) H(q)_i,
    T_o(q)=B_(L_o^a)(q)=F(B_(L_o)H(q)).

The Bayes maps are everywhere defined because each L_o is strictly positive. Both g_o and T_o are continuous, including on simplex faces. Each g_o>0 and

    Σ_o g_o(q)=Σ_i H(q)_i Σ_o L_o(i)=1.

Consequently the prescription

    K(q,{o}×A)=g_o(q) 1_A(T_o(q))

for Borel subsets A of the belief simplex defines a Markov kernel from the belief simplex to outcome × belief simplex. A random outcome is chosen with its original predictive probability and the representation then updates deterministically. This kernel has the same named outcomes, without a residual failure label or column renormalization of powered hidden-state likelihoods.

## Exact finite-history transport

For any original starting law p₀ and q₀=F(p₀), recursively put p_t=B_(L_(o_t))p_(t−1), q_t=T_(o_t)(q_(t−1)). Induction gives q_t=F(p_t) at every finite time. At each step,

    g_(o_t)(q_(t−1))=Σ_i L_(o_t)(i) p_(t−1),

so the probability of the complete observation word o₁…o_k under K is exactly the original product of conditional probabilities. Equivalently it is

    Σ_i p₀(i) ∏_(t=1)^k L_(o_t)(i).

The latter product formula assumes repeated conditionally independent uses of the declared passive channel given the fixed hidden state. It does not describe rereading a single stored observation as fresh evidence. Such rereading, changing states, source versions, or dependent observations must instead use the appropriate inherited joint state/instrument before any coordinate transformation.

Every original target readout Cp_t is recovered as C H(q_t). Thus finite histories, their probabilities, and target answers are preserved together. This is stronger than preservation of normalized posterior maps alone. It is not a new claim about permissions, observation access, actual outcome recovery from a sample, or infinite stopping without the inherited additional hypotheses.

## Why this does not contradict the fixed-channel obstruction

The kernel's state is q, a full belief representation. Its outcome probability g_o(q) is generally nonlinear in q. It need not equal Σ_i M_o(i)q_i for any fixed hidden-state likelihood row M_o. The main report asks for exactly that stronger fixed-row representation, with direct q-probability semantics, and gives an obstruction.

For uniform reference, a=1/2, and the report's L_1=(1/4,1/2,3/4), one has

    H(q)_i=q_i²/Σ_j q_j²,
    g_1(q)=[q₁²/4+q₂²/2+3q₃²/4]/Σ_j q_j².

For q=(1/2,1/4,1/4), H(q)=(2/3,1/6,1/6) and g_1(q)=3/8. Directly treating q as the original target probabilities would give L_1·q=7/16, a different prediction. The kernel uses 3/8 and preserves the original experiment. It has not constructed the impossible fixed-likelihood channel of the main report.

A further exact sequence suggested by the parent makes the path contract explicit. After outcome 1 the original posterior is p′=(4/9,2/9,1/3), with next outcome-1 probability 17/36. Thus P(11)=17/96. After two outcome-1 observations, q″=(2/7,2/7,3/7), and its inverse readout is p″=(4/17,4/17,9/17). The transformed state and original posterior differ, while the history probability and decoded target answers agree exactly.

If geometric correction is intended as an **actual change of beliefs** from p to q about the same target, rather than invertible recoding, decoding back to p changes that interpretation. This repair does not establish that the changed beliefs retain their old evidential semantics. Nor does the coordinate kernel supply new evidence, authenticate a reference, justify a target, or establish any cognitive/warrant consequence.

For a credal model family, apply the same construction to each q=F(p) in its exact nonlinear image. Preserve the same model parameter and its source/audit response through the path. No distribution over model identities is implied, and no independent recombination of transformed states with unrelated predictive weights is authorized.

## Inherited ancestry and bounded contribution

- `audit-continuation-transport-20261010/RESULT.md` §§2–3 already owns finite instruments, admissible normalized states, branch probabilities, target readouts and exact predictive continuation. It expressly inherits these mechanisms from H-Continuation. Its explicit coordinates are linear before normalization; the present bijective recoding does not improve its sufficient-state or minimality results.
- `correction-audit-transport-20261011/RESULT.md` §5, especially equation (6), already gives nonlinear conjugation q↦Φ(B_L(Φ⁻¹q)) on the actual image and separately requires recovery of original evidence normalizers. The present finite escort formulas are a direct specialization with those normalizers assembled into one outcome-labelled belief-state kernel.
- `stochastic-inquiry-quotient-transport-20261010/ADDENDUM.md` §§4–5 already distinguishes complete finite predictive laws from posterior-only information and adds the extra lawful-policy/stopping conditions needed for its stronger contracts. No new stopping theorem is claimed here.

Thus the mechanism is already owned. This note makes the exact positive alternative explicit beside the main report's fixed-hidden-channel obstruction, preventing an overreading of its scope. It is not an independent new research campaign or a new mathematical novelty claim.

`verify_repair.py` independently checks exact inverse readout, one-step nonlinear predictive probabilities, the discrepancy from treating q as original target probabilities, and all binary histories through length 8 in rational squared-coordinate representation. The general finite-history proof above is not replaced by that bounded enumeration. Input identities and the unchanged main report are recorded in REPAIR_BINDINGS.json; REPAIR_CHECKS.json records executed controls. No protected file changed.
