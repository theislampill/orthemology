# Changing objectives: exact use and limit of the coercive hierarchy theorem

10 October 2026 UTC. Additive application note. This is an elementary consequence of retained results plus a proof-route countercontrol, not a new classification theorem, independent mathematical review, or T20 closure. Inherited inputs are hash-bound in CONTROL_RECEIPT.json.

## Finite changes preserve the same underlying law

Fix finitely many switch times 0=τ₀<τ₁<… and a coercive real polynomial h_j on each positive-length interval. A normalized square-positive polynomial functional path is coordinatewise continuous at the switches and satisfies the corresponding normalized hierarchy, with coordinatewise C¹ regularity within each segment and the requisite right regularity at its start. The full polynomial algebra in one fixed finite-dimensional real space is used throughout.

The accepted coercive theorem applied to the first segment supplies its unique underlying law μ. At its positive-time endpoint, its global extension has a determinate full moment record. Continuity identifies this record with the next segment's initial record. Applying the same theorem to the next segment therefore cannot select another law with those moments: its initial representing law is the previous endpoint law. Induction glues the finite schedule.

Thus, throughout the path,

L_t(p) = ∫ p exp(−U_t) dμ / ∫ exp(−U_t) dμ,

U_t = Σ_{k<j}(τ_{k+1}−τ_k)h_k + (t−τ_j)h_j.

All h_j are lower bounded; the finite tilt is integrable with every polynomial moment. A positive multiple of the first coercive energy plus the other lower-bounded energies remains coercive. The inherited positive-time determinacy applies. Once μ and the schedule are fixed, the continuation is unique. Once a whole such path is given, its μ is unique. An indeterminate initial moment record alone may still parameterize multiple paths through its representing-law fibre.

No common quantitative coercivity bound is asserted. No unrestricted signed objective covectors from the finite-channel theorem are imported into this unbounded setting. The important interface consequence is that full moment continuity at a positive-time switch prevents an invisible reset to a different law. Finite moment continuity alone would not supply that conclusion.

## Smoothly moving objectives: the proof does not automatically transfer

For time-dependent polynomial h_t, unnormalization gives A'_t(p)=−A_t(h_t p), but

A''_t(q²)=A_t(q²[h_t²−∂_t h_t]).

The second term destroys the inference that every even derivative is nonnegative. This is an actual obstruction to the fixed-energy central-Taylor argument, even for genuinely realizable paths and coercive quadratics at every time.

Take h_t(x)=(x−t)² and μ=(δ₋₁+δ₀)/2. The integrated energy is t x²−x t²+t³/3. The unnormalized atom weights are exp[−t−t²−t³/3]/2 and exp[−t³/3]/2. Their ratio exp[−t−t²] varies, so the normalized path is nonconstant.

At t=1/10, h_t²−∂_t h_t equals −7359/10000 at −1 and −1999/10000 at 0. Both weights are positive, hence A''_t(1)<0 strictly. The derivative identity, both rational values and the weight ratio were checked exactly using SymPy and Fraction; no exponential rounding or Lean verification is claimed. CONTROL_RECEIPT.json records the executed operation and input hashes.

This is not a counterexample to nonautonomous realizability or uniqueness. It refutes one attempted transport of the existing proof. Obtaining vector representing measures for an abstract square-positive genuinely time-dependent hierarchy remains outside this argument. Scalar time changes h_t=c(t)h+d(t), with suitable positive c and regularity, reduce to the retained fixed-energy theory and are not examples of this new obstruction.

## Source scope

- tensor-moment-continuation-20261009/RESULT.md: finite-channel controlled tilt and objective-changing interface.
- measure-moment-continuation-boundary-20261009/RESULT.md: unbounded moment and control distinctions.
- tensor-realizability-extension-20261010/RESULT.md: positive-time determinacy, law recovery and continuation.
- coercive-square-positivity-20261010/RESULT.md: the reviewed full square-positivity existence theorem.

The inherited universal results do the work in the finite-switch corollary. This note does not independently reprove them, implement a noetic process, or establish that an actual epistemic correction is a probability-law tilt.
