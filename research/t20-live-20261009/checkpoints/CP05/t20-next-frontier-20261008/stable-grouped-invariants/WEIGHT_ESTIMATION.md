# Separate accuracy-dependent guarantee for matched weights

Use the model and promises of RESULT.md. Let 0<alpha<1 be an additional rational accuracy target. The weights are indexed by the unique matched scalar rank, equivalently by the identified increasing primitive positive counts and the zero component when present. They are not attached to recoverable individual physical routes.

Put

A=(32M)^(C-1),
B=C(16M)^(C-1),
epsilon_alpha=min[1/(32M^2), alpha/(2B)],
Delta_alpha=(w/2)epsilon_alpha^(2C)/4^C,
tau_alpha=min[Delta_alpha/8, alpha/(6A)],
Q_alpha=ceil[4C/tau_alpha].

Run the same finite-grid procedure with Q_alpha, and use enough independent groups that

n >= log(4C/delta)/(2 tau_alpha^2).

The rational power-of-two upper bound for the logarithm can be used exactly as in the main theorem. These formulas give polynomial dependence on M at fixed C,w,alpha, without claiming a sharp exponent or useful runtime.

## Proof

The grid-rounding argument gives moment approximation at most 4C/Q_alpha<=tau_alpha. Its component weights remain at least w/2 because tau_alpha<=Delta_alpha/8<=w/16, so 1/Q_alpha<=tau_alpha/(4C)<=w/(64C).

On the simultaneous empirical good event, selected and true moments differ by at most 3tau_alpha<Delta_alpha. The squared-annihilator lemma therefore gives support Hausdorff distance less than epsilon_alpha. Since epsilon_alpha<=1/(32M^2), the node matching is unique, the zero flag and primitive support agree, and both scalar laws have the same number s of atoms. Write the matched true/selected nodes as a_i,b_i and weights as p_i,p'_i.

The true-node gap is at least gamma=1/(16M). Define its Lagrange polynomial

L_i(z)=product_(j!=i) (z-a_j)/(a_i-a_j).

The absolute sum of its coefficients is at most (2/gamma)^(s-1)<=A. Also, on [0,1], each numerator factor has magnitude at most one; differentiating the product gives

sup |L_i'(z)| <= (s-1)/gamma^(s-1) <= B.

For s=1 the polynomial is the constant one and its derivative is zero, so these bounds remain valid. The coefficient estimate and moment closeness yield

|E_mu L_i-E_nu L_i| <=3A tau_alpha.

Since L_i(a_j) is the Kronecker delta and |b_j-a_j|<epsilon_alpha,

|E_nu L_i-p'_i|
<=sum_j p'_j |L_i(b_j)-L_i(a_j)|
<=B epsilon_alpha.

Together,

|p_i-p'_i| <=3A tau_alpha+B epsilon_alpha <=alpha.

The same empirical event serves every weight, so no additional union bound over components is needed. Thus with probability at least 1-delta the output primitive target is correct and all matched weights have error at most alpha.

This is a separate confidence statement with a potentially larger budget than the main support theorem. It neither estimates an absolute count scale nor identifies an actual calibration independently. Exact real weights are not recovered from a finite sample.
