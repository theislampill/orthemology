# Branchwise escort conjugacy need not define an observation instrument

Root derivation, 11 October 2026 UTC. Finite, strictly positive likelihoods; no empirical or philosophical calibration claim.

Fix a positive reference probability vector pi and exponent a>0. Let R_a(p)_i be proportional to pi_i^(1-a) p_i^a. For a strictly positive likelihood L, direct cancellation proves R_a(B_L(p))=B_(L^a)(R_a(p)). This is an identity between normalized maps, not by itself a joint observation model.

Suppose outcomes o have strictly positive original likelihoods L_o(i) with sum_o L_o(i)=1 at every latent state. A same-outcome stochastic channel H_o(i) realises ALL conjugated posterior maps on the full interior simplex exactly iff there are constants c_o>0 with

H_o(i)=c_o L_o(i)^a and sum_o c_o L_o(i)^a=1 for every i.

Proof: equality of B_H and B_G at even one full-support distribution forces H_i/G_i to be a single scalar through cancellation of that distribution and the normalizers. Apply separately to each outcome with G=L_o^a. Stochastic normalization yields the condition. Conversely those constants define the desired channel and Bayes maps. R_a is a bijection of the interior simplex, so testing every transformed interior law is legitimate. The proof requires the stated full-state contract; a restricted reachable family needs a separately checked condition.

Example: three states, two outcomes, L_1=(1/4,1/2,3/4), L_0=(3/4,1/2,1/4), a=1/2. Subtracting the first and third normalization equations forces c_1=c_0=c. The middle equation forces c=1/sqrt(2). The first then gives (1+sqrt(3))/(2sqrt(2)), which is not 1: its square is (2+sqrt(3))/4<1. Thus NO same-outcome stochastic instrument realises these two posterior maps simultaneously.

Dividing powered likelihoods by their statewise sum makes a stochastic channel but inserts a nonconstant common likelihood factor into each branch, changing its posterior. Adding a reject/failure outcome after a common scaling can complete a subinstrument, but changes the outcome and continuation contract. Neither is an exact repair under the original two-outcome contract.

This criterion preserves posterior maps only. Even when constants exist, preservation of original event probabilities is an additional requirement, not supplied by this argument. It does not dispute classical escort/Bayes conjugacy or the inherited normalized correction calculations; it blocks an unwarranted promotion from branchwise algebra to a full observational interface.

The same symmetric channel defeats every a>0 other than a=1. Endpoint equations force equal constants, while the middle and endpoint equations then require (1/4)^a+(3/4)^a=2(1/2)^a. Strict concavity for 0<a<1, or strict convexity for a>1, contradicts that equality. At a=1 the original channel is a solution. Consequently universal same-outcome posterior-instrument compatibility over all finite positive channels holds for this escort family exactly at the identity exponent. This is a universal-class statement; particular channels can admit nonidentity scales.

## Exact positive coordinate repair

The obstruction is to a fixed hidden-state likelihood channel acting linearly on q as a distribution over the original target. It does not prohibit a Markov kernel whose states are complete transformed beliefs. Put p=R_(1/a)(q), g_o(q)=sum_i p_i L_o(i), and T_o(q)=B_(L_o^a)(q). Then sum_o g_o(q)=1 and q maps, with outcome o, to T_o(q) with probability g_o(q). Branchwise conjugacy proves by induction that this kernel reproduces every original finite observation history and original posterior through the inverse readout. The g_o are generally nonlinear in q; this is consistent with the fixed-channel impossibility. Its underlying coordinate-change mechanism is inherited.

For the example channel, a=1/2 and uniform reference, start q=(1/2,1/4,1/4). Its underlying p=(2/3,1/6,1/6). The first outcome-1 probability is 3/8; after it p'=(4/9,2/9,1/3), with next outcome-1 probability 17/36. Hence the probability of 11 is 17/96. After 11 the transformed state is (2/7,2/7,3/7), while inverse readout gives original posterior (4/17,4/17,9/17). Calling those transformed coordinates themselves the original posterior would change the proposition represented.

This repair treats correction as an invertible change of representation. It does not show that actually replacing one's belief distribution by R_a(p) constitutes epistemic improvement. For an uncertain family, keep each model's g_o and T_o paired through that same model, as required by the preceding credal result.
