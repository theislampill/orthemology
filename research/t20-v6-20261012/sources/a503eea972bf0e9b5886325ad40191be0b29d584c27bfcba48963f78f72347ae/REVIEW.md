# Independent review: matrix-rank Gaussian entrance

11 October 2026 UTC. Source-bound ordinary mathematical review within active T20. No author or predecessor changes, protected integration, formal-kernel certification, exhaustive novelty claim, or programme closure.

## Verdict

**No blocking mathematical defect found in the reviewed theorem, proof, or exact checker.** The result is supported in its stated centred Gaussian, standard observed marginal, positive-definite supplied target, unit Euclidean transport/centred-reaction scope. The review supports the full-density projection, noncommuting matrix formula, arbitrary partial-rank entrance, forward global continuation, smooth determinant remainder, action qualifications, trace, and Gaussian-class uniqueness.

The author checker was replayed separately and passed all 31 controls. A separately written checker passes 51 exact controls, including symbolic matrix identities and rotated partial-rank tests absent from the author checker. Finite controls corroborate the analytic argument; they do not prove its general-dimensional or functional-analytic assertions.

One attribution qualification is worth retaining when summarizing the work: Liero et al. also discuss semidefinite **precision** matrices in Appendix B. Do not paraphrase the author's bounded positive-definite Gaussian-domain statement as saying that the paper never considers any semidefinite matrix. This does not undermine the present constrained, singular-covariance entrance theorem or require changing its mathematics.

## 1. Reviewed bytes and independence

The reviewed author RESULT.md has SHA-256

    489d1a4bbe394b78f3c57e1becc50cca7be75e55b7259ddd660ac5376ce91b03

and verify.py has SHA-256

    034ed66aa79cbcac738633fb34a20decd40d4ba1aa25dd9938b065c7d2c896ad

All files in the author packet, including its four predecessor snapshots, are copied under inputs/author and bound in this review's INPUT_BINDINGS.json. The author freeze hashes and predecessor hashes were checked. The original report and checker were read in full; relevant mathematical contents of all four bound predecessor reports were inspected. Replaying the author checker used an output path in this review folder, so it did not overwrite the author CHECKS.json.

The independent checker does not import, call, or modify the author's calculator. Its conditional-coordinate equations, polynomial differentiation, Gaussian Wick integration, and rotated rank tests were developed separately after reading the stated theorem. These are reviewer controls, not claimed independent certification of new reviewer extensions. The parent's isotropic exact witness was not used to establish this verdict or counted among these 51 controls.

## 2. Full-density projection and noncommuting algebra

Write W=T^{-1}, Delta=B-B*, and n=k+m. Block Gaussian precision gives

    Q=[[I+B*^T W B*, -B*^T W],[-W B*, W]],
    M=-B*^T W Delta,
    N=Delta^T W Delta.

These identities immediately confirm that M need not be symmetric and that the multiplier depends on B and the target, but not S. Holding z fixed in the spatial derivative is essential. Differentiating after holding e=z-By fixed would give the wrong observed score. The independent checker differentiates first and takes the conditional Gaussian expectation second.

For every symmetric P, the coarse potential phi=(y^T P y-tr P)/2 obeys

    K_nu phi / nu = 3(y^T P y-tr P)/2.

On the other hand, the transport part of p_*K_mu q contributes y^T sym(M)y-tr M, while the centred reaction contributes (y^T N y-tr N)/2. Consequently P=(M+M^T+N)/3 is the correct entire-marginal projection. A deliberately incorrect P_wrong=N/3 leaves the observed covariance derivative equal to -(M+M^T), generically nonzero. This failure is verified symbolically with general 2-by-2 matrix entries.

The underlying orthogonal projection is not justified by this covariance test alone. The inspected fixed-marginal predecessor supplies the tangent quotient and potential-field minimum; the correlated-target predecessor supplies the observed flux. Gaussian quadratic potentials satisfy their cutoff conditions by Gaussian tails, and the displayed conditional calculation supplies the required coarse weak multiplier. Thus the full-law projection applies before the covariance representation is chosen.

With C=Q-Sigma^{-1}-Pbar, direct spatial differentiation of v=-Cx and alpha=-(x^T Cx-tr(C Sigma))/2 matches the entire Gaussian log-density derivative for

    Sigma'=-C Sigma-Sigma C-Sigma C Sigma.

Symmetry of C and Sigma does not permit commuting them. The report keeps their order correctly. Its density expression x^T Sigma^{-1} C x uses the automatically symmetrized quadratic form and is valid without commutation. Expanding the inverse terms produces exactly the polynomial F. Since F_yy=0 and the entire tangent is Gaussian, the full observed law is fixed, not merely its covariance in a non-Gaussian approximation.

### An independent coordinate calculation

Let J=[[I,0],[-B,I]], so J Sigma J^T=diag(I,S). Congruence of the covariance tangent, using the conditional potential matrix, gives the following polynomial equations with no inverses of S:

    B'=-B-BP-(I+B B*^T)W Delta+S W(2B*-B),
    S'=2(I+BB^T)+S-(I+B B*^T)W S
                         -S W(I+B* B^T)-S W S.

They agree with the author's extraction from F. No simultaneous diagonalization is involved. The absence of P in the second equation is a result of the conditional covariance subtraction, not deletion of the multiplier. The independent checker verifies these identities symbolically with general 2-by-2 B, B*, S and W, and in different rectangular dimensions with rational positive matrices.

## 3. Partial-rank entrance and the smooth remainder

For v in ker S0, n_v=(-B0^T v,v) lies in ker Sigma0. Sandwiching F between n_v^T and n_v eliminates every term containing Sigma0, leaving 2|n_v|^2. Since F_yy=0, this is exactly v^T S'(0)v. Equivalently, the independent S equation above gives

    V^T S'(0)V=2V^T(I+B0 B0^T)V=A_K>0.

Thus strict inflow holds on the full initial kernel, including non-coordinate and non-invariant kernels. There is no reliance on differentiable choices of eigenvectors.

In the fixed orthonormal range/kernel basis, the upper block is A_R+O(t), the off-diagonal block is O(t), and the lower block is t A_K+O(t^2). For nonempty range, its Schur complement is t A_K+O(t^2), because the cross term is O(t^2). This proves positive definiteness for small positive time and loss of probability meaning at negative time whenever r>0. The empty-range case reduces directly to t A_K+O(t^2).

The determinant argument legitimately proves more than an undifferentiated big-O estimate. Polynomial ODE solutions are locally analytic. The determinant vanishes to precisely order r and has positive leading coefficient det A_R det A_K. Hence

    det S(t)=t^r g(t),    g smooth near 0,    g(0)=d0>0.

The smooth positive factor permits differentiation of log g. Inserting the conditional KL expression therefore gives the stated constant C0 and E=-(r/2)log t+C0+O(t), with a smooth remainder. Differentiation in the report is justified; it is not the invalid inference that every O(t) remainder has bounded derivative.

The independent controls use a rational Householder rotation whose entries are all nonzero. They check rank 0, 1, and 2 conditional covariances in latent dimension 3, with non-coordinate partial kernels, strict inflow, and the exact leading determinant coefficient. The coefficient of det(S0+t S'(0)) suffices as a control of the true leading term because the omitted Taylor terms are O(t^2) and the kernel block has first-order strictly positive leading part.

## 4. Direct independent check of the dissipation pole

The report's differentiable-energy argument is sound. A second calculation helps check its coefficient without differentiating the energy expansion. Put R=Q-Pbar. Expansion of C=R-Sigma^{-1} gives

    D=tr(Sigma^{-1})+H(B,S),
    H=tr(R Sigma R)-2tr R+tr(R Sigma R Sigma)/2
                                -tr(R Sigma)+n/2.

Here H is smooth, indeed polynomial in B,S for the fixed target. Block precision gives

    tr(Sigma^{-1})=k+tr((I+BB^T)S^{-1}).

The same fixed-basis Schur expansion yields

    S(t)^{-1}=t^{-1}V A_K^{-1}V^T+O(1).

Consequently the pole coefficient is

    tr[V^T(I+B0 B0^T)V A_K^{-1}]=r/2.

This confirms the orientation- and target-independent r/(2t) leading term directly. The independent checker verifies the trace decomposition at a noncommuting positive rational state and the inverse Laurent residue at all three rotated rank controls. The identities and their all-dimensional reasoning are a corroborating reviewer calculation, not an additional claim required to rescue the author proof.

## 5. Global continuation and convergence

The conditional KL expression is correct for a fixed standard observed law. Whitening only S by T in the energy expression is an algebraic spectral calculation, not a change of the transport metric. Each finite sublevel bounds B, bounds S above, and keeps its least eigenvalue strictly positive. It is compact inside the positive-state parameter domain.

The dissipation identity E'=-D is supplied by the full orthogonal projection and is also verified independently by direct differentiation of the conditional energy. Since C is symmetric,

    tr(C Sigma C)=||Sigma^{1/2} C||_F^2.

It follows that D=0 forces C=0. The zz and zy blocks then give S=T and B=B*. Conversely the target has P=0 and F=0. No unjustified scalarization or coordinate-mobility inverse is needed.

Starting at any fixed positive time of the entrance, energy descent gives a compact sublevel for the whole remaining trajectory. Standard continuation prevents blow-up and future rank loss. D and its derivative along the flow are bounded on this compact set. Nonnegative integrability plus uniform continuity forces D(t) to zero; the unique zero and compactness force convergence of the entire trajectory to the target. This does not assume a finite initial singular KL or a convergence rate. The Gaussian coupling then supplies the claimed W2 convergence.

## 6. Action, endpoint trace, and uniqueness

The minimum-field assertion is valid among all admissible representations of the same full density tangent: the projected quadratic potential lies in the minimum-potential closure of the inherited quotient. Thus changing field representatives cannot remove the original-time action divergence.

From D=r/(2t)+O(1), the original-time action is infinite while the specified curve has length sqrt(2r epsilon)+O(epsilon^{3/2}). The time changes and their coefficients are correct:

    t=u^2:       new action density 2r+O(u^2),
    t=epsilon u^2, 0<=u<=1:
                 total action 2r epsilon+O(epsilon^2).

These are statements about this curve and its parametrization. They do not establish geodesic optimality, equality with an endpoint distance, or noncompact endpoint attainment.

The common (Y,G) coupling proves W2 convergence to the singular trace by continuity of the positive-semidefinite square root. For r>0, the singular trace and each positive-time full density are mutually singular, so there is no total-variation convergence. The finite integral of sqrt D implies finite spacetime L1 transport and reaction. This allows passage to the endpoint in the compactly supported C1 weak continuity equation, with the initial trace and no extra impulse. The report correctly distinguishes this from finite original-time L2 action; the reparametrized curve does have finite L2 action.

For centred Gaussian entrances, narrow convergence to the specified Gaussian trace forces covariance-parameter convergence by Gaussian characteristic functions. It is not an inference from narrow convergence for arbitrary measures. The polynomial vector field is bounded near that trace, so the positive-time integral equation extends to zero and ordinary ODE uniqueness applies. The report deliberately does not claim noncentred-Gaussian or all-law weak uniqueness. The scalar predecessor has a separate additional mean calculation; it cannot silently enlarge the matrix theorem's stated class.

The finite-horizon approximation claim follows from continuous dependence in a compact tube around the entrance, followed by uniform continuity of matrix square roots on bounded PSD sets. On [h,T], positivity makes the energy and dissipation continuous uniformly. Divergent initial energies and original-time actions are correctly excluded from uniform bounds.

## 7. Bounded predecessor and primary-source comparison

The four copied predecessors support the inheritance claims:

- Singular Gaussian entrance, §§1, 3–7: the scalar mechanism, action/length distinction, endpoint weak equation, reparametrization, trace, and approximation argument are already present.
- Correlated-target correction, §§3–6: the observed spatial-score flux, scalar multiplier, full-density check, and target-dependent energy with compact-sublevel convergence are already present.
- Fixed-marginal correction, §§2–4: the full tangent quotient, orthogonal projection, potential-field minimum, cutoffs, and coarse weak solve are already present. Its general projection formula is not new matrix-entrance material.
- Gaussian primary comparison, §§2–4: normalized Gaussian SHK coefficients and the unconstrained noncommuting covariance equation are already identified with classical literature.

I did not locate the explicit arbitrary-dimensional multiplier, partial conditional-rank statement, or rank-r determinant/action asymptotics as stated in those four reports. This is a bounded document comparison, not a corpus-wide or literature-wide nonduplication claim. The scalar specialization is inherited. Standard Schur complements, Gaussian precision identities, smooth ODE continuation, and determinant arguments carry no originality claim here.

The inspected [Liero–Mielke–Tse–Zhu source](https://arxiv.org/html/2504.20400v1), §3.4, Theorem 3.11 and (3.8a), supplies the unconstrained normalized covariance dynamics. Its displayed Gaussian parameter domain uses positive-definite covariances. Appendix B also discusses a semidefinite extension for the precision equation; this is different from a rank-deficient covariance law with a fixed entire observed marginal. The present report's mathematics is derived directly. The predecessor correctly warns about an apparent expanded-PDE sign inconsistency in this source version; the operator and (3.8a) give the consistent convention used here.

The inspected [Bauer–Charon–Needham–Nishino source](https://arxiv.org/html/2402.15860v3), §3.2 and Remark 4.24, provides weighted-Sobolev orthogonal projection for specified path constraints. This is appropriate classical ancestry. Its finite collection of constraint potentials is not itself a citation for the exact whole-marginal Gaussian entrance theorem; the inspected predecessor quotient and the present Gaussian calculation supply that step.

## 8. Reproduction, controls, and ceiling

Run from this folder:

    python3 inputs/author/verify.py --output AUTHOR_REPLAY.json
    python3 independent_controls.py
    python3 -O independent_controls.py --output INDEPENDENT_CHECKS_OPTIMIZED.json

The author replay has 31 passing controls. The independent checker has 51 passing controls: symbolic matrix/omitted-flux identities; a rectangular positive-state full-density and Wick-action calculation; projection cost and dissipation identities; rotated singular-rank and Laurent-pole controls; target stationarity; and source hashes. The checks use exact SymPy arithmetic. Optimized mode preserves the explicit failure checks.

No required repair is identified. Preserve the stated scope and the source nuance above. This review does not certify exhaustive novelty, unrestricted PDE uniqueness, all-law singular entrance, arbitrary observed covariance under an unchanged metric, geodesic minimality, empirical warrant, protected integration, or T20 closure.
