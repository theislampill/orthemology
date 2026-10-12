## 13. Classification of all universally audit-covariant labelled flows

The separable positive result admits a useful converse. This makes the connection a classification, rather than only one convenient example. It should be compared with T20's existing posterior-gradient classification before assigning any novelty credit.

### Theorem J: vector-field classification

Let the state space be the product of the positive simplex \(\Delta_{n-1}^{\circ}\) and an open smooth position/state domain \(X\). A positive audit acts by

\[
T_r(w,x)=(B_rw,x),\qquad r_i>0.
\]

Let a continuously differentiable vector field have unique local flows. Its flows commute with **every** such audit, wherever both sides are defined, if and only if the vector field has the form

\[
\boxed{\dot x=v(x),\qquad
\dot w_i=w_i\left(c_i(x)-\sum_jw_jc_j(x)\right).}
\]

Here \(v\) and the fitness functions \(c_i\) are independent of the weights. Adding a common function of \(x\) to all \(c_i\) changes nothing.

### Proof

Flow commutation implies vector-field equivariance by differentiation at time zero:

\[
F(T_rz)=D T_r(z)F(z).
\]

Conversely, equivariance makes \(T_r\) of any solution another solution with the transformed initial value; local uniqueness then gives flow commutation.

Use log-odds coordinates \(u_i=\log(w_i/w_n)\), for \(i<n\). They identify the positive simplex with \(\mathbb R^{n-1}\). The audit acts by the translation

\[
u_i\longmapsto u_i+\log(r_i/r_n).
\]

Every translation is obtainable from a positive audit. Equivariance therefore says that the transformed vector field is invariant under every translation in \(u\). Its \(u\)-components and \(x\)-components depend only on \(x\): write them as \(c_i(x)\) and \(v(x)\), with \(c_n=0\).

Since \(\dot u_i=\dot w_i/w_i-\dot w_n/w_n\) and \(\sum_i\dot w_i=0\), solving for the weight derivatives gives precisely the centred replicator form above. The same calculation proves its equivariance and hence the converse. The one-weight case is the trivial special case. ∎

### Corollary: the standard joint metric forces a separable energy

Assume \(X=X_1\times\cdots\times X_n\), with connected open Euclidean factors. Use the joint metric

\[
g_{(w,x)}((\dot w,\dot x),(\dot w,\dot x))
=\frac1\alpha\sum_i\frac{\dot w_i^2}{w_i}
+\sum_iw_i\|\dot x_i\|^2,
\qquad \alpha>0.
\]

For a twice continuously differentiable energy \(E\), its negative gradient flow commutes with every positive weight audit, with the objective and metric held fixed, if and only if

\[
\boxed{E(w,x)=\sum_iw_iV_i(x_i)+C}
\]

for functions \(V_i\) and a constant \(C\).

To prove necessity, Theorem J makes the log-odds velocity independent of \(w\). The Fisher-gradient formula then makes the tangent derivatives of \(E\), at fixed \(x\), independent of \(w\). Consequently \(E\) is affine in the weights and can be written \(\sum_iw_iV_i(x)\), absorbing a common \(x\)-dependent term into the coefficients.

Its position component is

\[
\dot x_j=-\frac1{w_j}\sum_iw_i\nabla_{x_j}V_i(x).
\]

Theorem J requires this component to be independent of all weights. The corresponding affine identity on the simplex forces \(\nabla_{x_j}V_i=0\) whenever \(i\ne j\). Connectedness of the product factors then gives \(V_i=V_i(x_i)\). Sufficiency follows by direct substitution: positions evolve independently of weights, and the weight component is the centred replicator field with \(c_i=-\alpha V_i(x_i)\). ∎

This is a classification for the **specified metric, labelled positive state space, fixed objective, and universal audit family**. It does not prohibit interaction energies. It shows why they generally need a different retrospective replay contract. An audit that also transforms the objective, a prior, or another context field is an action on a larger state space and must be analysed there; it is not ruled out by the fixed-objective theorem.

For a restricted declared family of audits, test equivariance under that actual family or its justified closure. Do not replace an integer-generated audit group by its entire real span without proof: a nonconstant periodic vector field can commute with integer translations while failing to commute with all real translations.

## 14. A discretisation can preserve positivity and descent but fail the audit contract

Continuous audit covariance does not automatically pass to an arbitrary discrete integrator. This supplies a new acceptance test for the discretisation frontier.

### An exact Euler counterexample

Take \(w=(1/2,1/2)\), fitness \(c=(0,1)\), audit \(r=(1,2)\), and step \(h=1/2\). The centred replicator Euler step is

\[
U_h(w)_i=w_i+h\,w_i(c_i-\overline c).
\]

It gives \(U_h(w)=(3/8,5/8)\). Auditing afterwards yields

\[
B_rU_h(w)=(3/13,10/13).
\]

Auditing first gives \(B_rw=(1/3,2/3)\), and the Euler step then gives

\[
U_hB_r(w)=(2/9,7/9).
\]

Both paths have positive normalised weights; the Euler step decreases the energy \(E(w)=w_1\) when the first coordinate is indexed as the lower-fitness coordinate. Yet the endpoints differ by total variation \(1/117\).

Thus **positivity, normalisation and energy descent do not by themselves certify source-audit fidelity of the discrete step**.

### Theorem K: an exact rational audit-covariant weight step

For fixed potentials \(V_i\), choose \(h\ge0\), let \(b=\min_iV_i\), and define

\[
A_i=\frac1{1+h(V_i-b)},\qquad
w'_i=\frac{w_iA_i}{\sum_jw_jA_j}.
\]

For strictly positive weights, this step:

1. preserves strict positivity and total mass for every finite \(h\ge0\);
2. commutes with every positive audit whose revision leaves these potentials and the step selection unchanged;
3. does not increase \(\sum_iw_iV_i\);
4. is unchanged by adding a common constant to all potentials;
5. has derivative at \(h=0\) equal to the negative Fisher-gradient weight field \(-w_i(V_i-\overline V)\).

**Proof.** Every denominator is at least one, giving the first claim. The second follows because two positive reweightings commute. For the third,

\[
\sum_iw'_iV_i-\sum_iw_iV_i
=\frac{\operatorname{Cov}_w(V,A)}{\mathbb E_w A}\le0.
\]

The sign follows from

\[
\operatorname{Cov}_w(V,A)
=\tfrac12\sum_{i,j}w_iw_j(V_i-V_j)(A_i-A_j),
\]

because \(A_i\) is decreasing in \(V_i\). The minimum baseline shifts by the same common constant as the potentials, proving claim 4. Finally \(A_i=1-h(V_i-b)+O(h^2)\); normalising cancels the common baseline and gives claim 5. ∎

The minimum is a numerical baseline for the **weight update only**. It does not redefine the position energy or authorise differentiating a different, minimum-subtracted positional objective.

### Positive joint construction

For a separable energy \(\sum_iw_iV_i(x_i)\), first apply position maps \(x_i'=P_i(x_i)\) which are independent of the audited weights, preserve the declared position domain, and satisfy \(V_i(x_i')\le V_i(x_i)\) individually. Then apply the rational weight step using the new values \(V_i(x_i')\).

The resulting joint step preserves positive realised atomic states, commutes with the declared weight audits, and does not increase the joint energy. Position descent gives the first energy inequality; the covariance argument gives the second. The positions and subsequent factors are unchanged by a weight audit, so the two reweightings commute exactly.

This is a constructive reference scheme, not a statement that every existing T20 scheme is faulty or that this method is always more accurate. A global line search whose step choice depends on the audited weights may break the commutation premise. Convergence order, stiffness, boundary constraints, moving objectives and interaction terms need their own analysis. The code verifies the stated finite controls without claiming those additional properties.

