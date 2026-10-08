# Orthemology Seventeenth Mathematical Companion

## 1 Finite inference under assignment uncertainty

This companion develops a finite probability contract for a weighted binary-assignment statistic. It answers three questions: which assignment information makes an observed extreme value meaningful, how to bound its probability when assignments may depend on earlier assignments, and how to keep numerical approximations conservative. It contains ordinary written proofs and synthetic counterexamples. It does not establish any real experiment's assignment mechanism, and it makes no claim of new historical ownership for classical randomisation, dynamic programming or concentration arguments.

The central distinction is simple. Knowing that each coin is individually fair does not say how all the coins move together. If they can move as one coordinated pattern or its opposite, an absolute weighted total can be constant. Bounds on the next coin's probability after every preceding pattern provide stronger information. They allow an exact finite recursion and scalable conservative bounds, while still allowing dependence.

The second distinction concerns the response. A no-effect hypothesis can make the response schedule fixed while assignments are varied. It cannot turn a merely marginal assignment distribution into random assignment relative to that schedule. The assignment relation and the sharp no-effect hypothesis are separate premises.

The mathematics below retains these premises throughout. The quantitative outputs are upper probability bounds under specified model families. A large bound is not evidence that the no-effect hypothesis is true; a small bound challenges it only together with the maintained assignment and measurement assumptions.

## 2 The finite experiment and conditioning contract

There are \(N\) binary placement coordinates in a specified total order. Write \(Z_i=1\) for the positive assignment and \(Z_i=0\) for the negative assignment, and \(A_i=2Z_i-1\). The full assignment is \(z\) in a specified set \(\Omega\subseteq\{0,1\}^N\). Unless additional restrictions are stated, \(\Omega\) is the full cube. The order is part of the model: a probability conditional on previous rounds for one participant is not automatically a probability conditional on every earlier coordinate in a participant-by-round ordering.

Let \(X\) denote inputs legitimately fixed by the experiment/conditioning contract. Possible components include task items, complete cue content and polarity schedules, source identities, treatment assignments, group membership, and exogenous baseline data. Their inclusion is a requirement to be justified, not an automatic consequence of their being present in a dataset. In particular, a cue presented before its own response need not have been fixed before earlier placements. A future adaptive cue, feedback value, or knowledge report cannot be silently treated as a baseline covariate.

Let \(u\) describe a fixed experimental world: the units, exogenous states and potential response process relevant to this finite experiment. The randomisation draws generating placement are excluded from \(u\); they remain random under the assignment law. For each admissible full array \(z\), let \(W_u(z)\) be the complete recorded response trajectory, including availability \(R_i(z)\), every recorded response \(F_i(z)\), and any additional outcome-derived variables used by the statistic or its analysis rule. Potential responses may depend on earlier assignments, other participants' assignments, feedback, common cues and treatment. No no-carryover or no-interference assumption is imposed.

The sharp full-trajectory null is

\[
H_0:\quad W_u(z)=w_u\quad\text{for every }z\in\Omega.\qquad\text{(2.1)}
\]

This is a statement about the whole trajectory, not merely \(\mathbb E[F_i(1)-F_i(0)]=0\), a zero regression coefficient, or absence of a same-round direct effect. It must cover availability whenever unavailable responses are encoded or observations are selected by availability. It must cover every outcome-dependent ingredient held fixed during reference assignment calculations. It does not require feedback itself to be invariant if feedback is not fixed or used in an unjustified conditioning step; rather, it says the resulting recorded response trajectory is invariant even allowing the intervention's downstream feedback consequences.

An assignment contract supplies a law \(Q_{X,u}\) for \(Z\), or a set of possible such laws, conditional on the legitimate fixed inputs and fixed experimental world. Usual randomised-design reasoning provides a law not depending on \(u\) beyond allowed design inputs. A weaker sufficient condition for the robust results is that, for every relevant \(u\) under \(H_0\), \(Q_{X,u}\) belongs to the declared family. A claim only about the marginal law \(Q(Z\mid X)\), averaged over a possibly assignment-associated \(u\), is not sufficient for freezing \(w_u\).

For a sequential physical experiment, the same point can be expressed using exogenous randomisation and a specified history: the required probability bounds must hold conditional on the fixed potential-response schedule and every assignment prefix relevant to the model. Bounds conditional on a larger legitimate history imply bounds conditional on a smaller one by averaging when the endpoints are deterministic functions of the retained information. Conditioning additionally on a future observed variable does not follow from this averaging argument.

### 2.1 Why both parts of the contract are indispensable

Here is a finite counterexample with no placement effect. Let \(U_i\) be independent fair signs. Set the response under every intervention to \(W_i(z)=U_i\), so the sharp null is true. Now let the observational assignment be \(A_i=U_i\). Marginally, the assignment array is a product of fair signs. Nevertheless, with fixed observed weights \(a_i=W_i\), the observed sum is always \(N\). A reference calculation that freezes those weights and substitutes independent fair \(A_i\) gives two-sided probability \(2^{1-N}\), for \(N\) at least one. For \(N=6\) it rejects at level \(.05\) on every experimental world. The error is not the sharp null; it is treating the marginal assignment law as a randomised law conditional on the potential responses.

A related conditioning error begins with genuine independent randomisation \(A_i\) independent of \(U_i\), and the same invariant response \(W_i(z)=U_i\). Define a post-assignment variable \(C_i=\mathbf1\{A_i=U_i\}\). Conditional on \(C_i=1\), \(A_i\) and the response agree deterministically. Keeping the fair unconditional reference law after selecting or conditioning on \(C_i\) produces the wrong test. A correct conditional design calculation would have to account for the selection event and the experimental world; the unconditional coin law is no longer the claimed conditional law.

These are synthetic examples. They distinguish a marginal distribution from the conditional assignment relation required by a fixed-response reference calculation; they are not evidence about any actual experiment.

## 3 A fully specified candidate weighted statistic

The following defines a generic finite-response statistic. A scientific application must select its population, response validation and weighting before inspecting the assignment-response relation. No actual observations are used here.

Let \(E_i\) be a binary eligibility indicator supplied by legitimate fixed inputs. Let \(B_i\) be a signed recorded response in \([-1,1]\) when a response is available. Let \(R_i\) indicate availability under a predeclared validation rule. Define \(Y_i=R_iB_i\) by cases: \(Y_i=B_i\) when \(R_i=1\) and \(Y_i=0\) otherwise. No unobserved \(B_i\) is imputed. The zero contribution of an unavailable response means no recorded directional contribution; it does not mean that a neutral response was observed.

Eligibility must be invariant under the assignment intervention, or covered by an adequate conditional model. A rule measured before its own response is not automatically fixed with respect to earlier assignments. These conditions are requirements of the mathematical application, not conclusions from the notation.

For each group \(g\), let \(n_g=\sum_{i:g(i)=g}E_i\) over its prespecified member-round coordinates. Let \(G_+\) be the number of groups with \(n_g>0\). If \(G_+=0\), the selected statistic has no eligible population and no test is defined. Otherwise put

\[
\begin{aligned}
c_i&=\dfrac{E_i}{G_+ n_{g(i)}}\quad\text{if }n_{g(i)}>0,\\c_i&=0\quad\text{if }n_{g(i)}=0,\\
a_i&=c_iY_i,\\
S(z;w,X)&=\sum_{i=1}^{N}a_i(2z_i-1),\\
T(z;w,X)&=|S(z;w,X)|.
\end{aligned}\qquad\text{(3.1)}
\]

Groups are equally weighted; eligible member-rounds within a group are equally weighted. The denominator never depends on whether a response is available. Thus \(\sum_i c_i=1\) and \(|S|\leq\sum_i|a_i|\leq1\). Other participant/group weightings are possible, but their denominators and target population must be stated rather than changed after looking at results.

The product \(A_iB_i\) is a signed assignment-response alignment. Its sign does not identify a hidden generating mechanism. Negative \(a_i\) are allowed; the probability results below do not require response weights to be positive.

Under \(H_0\) and the assignment contract, \(a_i=a_i(w_u,X)\) are fixed numbers when assignments are varied. The weights need not have arisen from independent outcomes. Observed response-derived weights could, mathematically, be chosen by an assignment-invariant rule under \(H_0\); prospective declaration is still required here to avoid an undisclosed search over questions, transformations or subgroups. A rule that depends directly on the observed placements must instead be rerun for every reference array and incorporated into the statistic. Holding its chosen output fixed would not implement the same test.

Availability deserves its own predeclared diagnostic, for example \(S_R(z)=\sum_i c_iR_i(2z_i-1)\). A zero-aligned-evidence statistic can miss placement effects consisting only of availability changes or cancellations. If both statistics can trigger an inferential rejection, predeclare a joint randomisation statistic or an error allocation such as a Bonferroni split. Calling a second test a diagnostic does not remove multiplicity. Purely descriptive reporting can be identified as such.

Treatment is held fixed only under a valid conditional placement law given treatment. Subgroups, selected time windows, transformations and interactions require their own predeclared inferential treatment. A rejection concerning placement does not identify an effect of another intervention.

### 3.1 Fixed opportunity weighting

An alternative target retains every scheduled opportunity in its denominator. Suppose there are \(K\) groups, group \(g\) has a fixed roster of \(m_g\) members, and every member has \(J\) scheduled questions. With the same eligibility indicator \(E_i\) and recorded evidence \(Y_i\) as above, define

\[
c_i=\frac{E_i}{K m_{g(i)}J},\qquad a_i=c_iY_i.\qquad\text{(3.2)}
\]

The scheduled question count \(J\) is distinct from the availability indicator \(R_i\). All groups remain in the population, including groups with no eligible opportunities or no recorded directional evidence. The total opportunity weight per group is \(1/K\), while its total eligible weight can be smaller. Thus, with \(H_E=\sum_i c_i\),

\[
|S(z)|\leq\sum_{i=1}^{N}|a_i|\leq H_E\leq1.\qquad\text{(3.3)}
\]

This target differs from the equally weighted mean of group-specific means among eligible opportunities. It must not inherit that target's normalisation silently. Both constructions yield fixed real coefficients under the specified sharp null and assignment contract, so every probability result below applies to either. Fixed exported or observed membership is not automatically intervention-invariant: that fact, or an adequate conditional law for it, remains an application premise.

## 4 Declared assignment models and their different warrants

The following are different hypotheses about the design, not interchangeable approximations.

- Known joint law. \(Q(z\mid X,u)\) is specified on \(\Omega\) and applicable to the retained experimental units. Direct summation, exact state computation or a valid Monte Carlo rank procedure can produce a reference test.
- Fair marginal law. Each \(Q(Z_i=1\mid X,u)=1/2\), with arbitrary dependence. This does not specify conditional probabilities after previous assignments and gives the two-sided impossibility in Section 6 when the support allows complements.
- Rectangular sequential interval law. For every positive-probability prefix \(h\) in a specified order, \(\ell_i(h)\leq Q(Z_i=1\mid Z_{<i}=h,X,u)\leq u_i(h)\), with known \(0\leq\ell_i(h)\leq u_i(h)\leq1\). All kernels satisfying these restrictions are allowed. This is the sharp recursion model in Section 7.
- Independently assigned coordinates with unknown biases. \(Q\) is a product law, with \(p_i\) in specified intervals. This is a smaller family than the sequential interval family. A general event probability is multiaffine in the separate \(p_i\), so a maximum over a rectangular box occurs at some vertex, but there may be \(2^N\) vertices. A common unknown \(p\) across coordinates is another restriction and does not follow this separate-coordinate endpoint argument.
- Known blocking, balancing, permutation or shared-coin law. Such a design can be analysed on its actual support and joint law, sometimes very efficiently. It must be documented. It does not follow from observed totals, repeated vectors or a general statement that placement was random.
- Unspecified randomised placement. No numerical bounds, probabilities or support symmetries are known. This description alone does not specify a numerical reference distribution.

A stipulated model can support a conditional sensitivity statement, explicitly beginning “if the assignment mechanism satisfies ...”. It is not retrospectively upgraded into a recovered design fact. A single observed complete array cannot warrant arbitrary-prefix probability bounds merely through its frequencies. Statistical estimation under a separately justified repeated-draw model is a different task; assuming that model to estimate its own independence premise would be circular.

## 5 Finite reference probabilities and validity

Fix \(X\),\(u\) satisfying \(H_0\), suppress these arguments, and let \(T\) be the fixed statistic on \(\Omega\). For a known law \(Q\) define the inclusive tail function and \(p\)-value

\[
\begin{aligned}r_Q(t)&=Q\{T(Z)\geq t\},\\p_Q(z)&=r_Q(T(z)).\end{aligned}\qquad\text{(5.1)}
\]

Inclusive ties are essential to this simple nonrandomised validity statement. A strict tail or a mid-\(p\) adjustment is not automatically a level-valid \(p\)-value. For any \(\alpha\in[0,1]\),

\[
Q\{p_Q(Z)\leq\alpha\}\leq\alpha.\qquad\text{(5.2)}
\]

Proof. There are finitely many distinct statistic values. If none has upper-tail mass at most \(\alpha\), the rejection event is empty. Otherwise let \(t_*\) be the smallest such value. Since the upper-tail function is nonincreasing, the rejection event is exactly \(\{T\geq t_*\}\), whose \(Q\) probability is at most \(\alpha\). This also covers zero-probability statistic values by restricting to the support. End proof.

For a declared nonempty family \(\mathcal Q\) containing the actual conditional law, define

\[
\begin{aligned}r_*(t)&=\sup_{Q\in\mathcal Q}Q\{T(Z)\geq t\},\\p_*(z)&=r_*(T(z)).\end{aligned}\qquad\text{(5.3)}
\]

Then \(p_*(z)\geq p_{Q_0}(z)\) for the actual \(Q_0\). Consequently

\[
Q_0\{p_*(Z)\leq\alpha\}\leq Q_0\{p_{Q_0}(Z)\leq\alpha\}\leq\alpha.\qquad\text{(5.4)}
\]

This is finite-sample validity, uniform over the declared family, conditional on the fixed experimental world. Averaging over such worlds preserves the inequality when the contract holds in every world under the null. Taking the supremum separately at each observed threshold does not invalidate the test; pointwise domination is the reason. The maximising law need not be the actual law and may differ between thresholds.

Any certified upper bound \(U(t)\geq r_*(t)\) gives an equally valid, possibly more conservative \(p\)-value \(\min\{1,U(T(z))\}\). An algorithm that merely finds one admissible law supplies a lower bound on \(r_*\), which has the wrong direction for this purpose. A large approximate search is not a certificate of a global upper bound.

Attribution of a rejection to placement noninvariance is conditional on the maintained assignment, linkage and measurement contract. Formally the test controls rejection of the sharp null under that contract. If the contract is only a speculative model, the result challenges the conjunction, not the null in isolation. Nonrejection proves neither invariance nor absence of source use.

## 6 Fair marginals alone make this two sided test vacuous

Proposition. Suppose \(\Omega\) contains \(z\) and its bitwise complement \(z^{\mathrm c}\) for every possible observation \(z\), and \(\mathcal Q\) includes every fair-marginal law on \(\Omega\). Let \(S(z)=\sum_i a_i(2z_i-1)\) with fixed real weights, and \(T(z)=|S(z)|\). Then \(p_*(z)=1\) for every \(z\).

Proof. For the particular observed \(z\), define \(Q_z\) to assign mass \(1/2\) to \(z\) and mass \(1/2\) to \(z^{\mathrm c}\). Each coordinate is one in exactly one of these arrays, so \(Q_z\) has fair marginals. Also \(S(z^{\mathrm c})=-S(z)\), hence \(T(z^{\mathrm c})=T(z)\). Both support points satisfy the inclusive tail event at the observed threshold. Therefore \(r_{Q_z}(T(z))=1\), and no probability can exceed one. End proof.

The same construction works for any complement-invariant extremeness statistic. It does not require equal weights, positive weights, independent participants, or a particular observed array. A conventional doubled smaller one-sided \(p\)-value is also one for this pair law, with the usual cap at one.

\(Q_z\) is chosen after fixing \(z\) only as a member witnessing the pointwise supremum over the previously declared family. It is not an assertion about the actual generator, a fitted estimate of its law, or a claim that every admissible law is equally plausible. Section 5 explains why this pointwise worst-case calculation still gives a valid robust \(p\)-value.

Qualitative strict positivity without numerical bounds does not rescue the test on the full cube. Let \(U\) be the uniform law on the cube and take \(Q_\varepsilon=(1-\varepsilon)Q_z+\varepsilon U\) for \(0<\varepsilon<1\). It has fair marginals, full support, and strictly interior conditional branch probabilities at every prefix. Its tail probability is at least \(1-\varepsilon\) and tends to one. Thus the supremum is still one even if the exact two-point law is excluded. If the tail event is proper, full support prevents attainment of one; the conclusion is then a supremum, not a maximising law. This extension uses the full-cube support and must not be transferred to an arbitrary restricted support without a corresponding construction.

This is not a theorem that every possible test under every fair-marginal model is useless. A prespecified one-sided event is not complement-invariant, and additional support or independence restrictions can rule out the construction. The one-sided distinction does not offer a conventional-level rescue under the present family: for an inclusive signed upper tail at the observed \(S(z)\), the pair law gives probability \(1/2\) when \(S(z)>0\) and probability one when \(S(z)\leq0\). Its robust one-sided \(p\)-value therefore cannot reject at a level below \(1/2\). The exact probability-one proposition above concerns the ordinary two-sided linear-alignment statistic under the stated family. If a documented support is not closed under complements, the proposition must not be applied without checking it.

With no marginal restrictions at all, the point mass at the observed array gives the same upper-tail conclusion even more directly. Saying only that some randomness was used, without quantitative constraints, does not repair the numerical inference gate.

## 7 Sharp recursion for sequential interval bounds

### 7.1 The family and the finite recursion

At each prefix \(h\) of length \(i-1\), let \([\ell_i(h),u_i(h)]\) be a specified nonempty closed interval. A kernel policy \(q\) chooses \(q_i(h)\) in that interval. It induces the full-array law

\[
\begin{aligned}b_i(z)&=q_i(z_{<i})\quad\text{if }z_i=1,\\b_i(z)&=1-q_i(z_{<i})\quad\text{if }z_i=0,\\Q_q(z)&=\prod_{i=1}^{N}b_i(z).
\end{aligned}\qquad\text{(7.1)}
\]

The piecewise factor selects the realised branch probability and avoids an ambiguous \(0^0\) convention. Conditional restrictions are substantive only at reached histories; assigning an arbitrary admissible kernel at an unreachable history has no effect on the law. Let \(\mathcal Q_{\mathrm{rect}}\) be the laws generated by all such policies. Choices at distinct histories are otherwise unconstrained. This last “rectangularity” condition is important to sharpness.

For a threshold \(t\), set

\[
V_N(z)=\mathbf1\{|\sum_{i=1}^{N}a_i(2z_i-1)|\geq t\}.\qquad\text{(7.2)}
\]

Working backwards, at a prefix \(h\) of length \(i-1\) put

\[
\begin{aligned}v_0&=V_i(h,0),\qquad v_1=V_i(h,1),\\
V_{i-1}(h)&=\max_{q\in[\ell_i(h),u_i(h)]}\{(1-q)v_0+qv_1\}\\
&=v_0+\max\{\ell_i(h)(v_1-v_0),u_i(h)(v_1-v_0)\}.
\end{aligned}\qquad\text{(7.3)}
\]

Then

\[
V_0(\varnothing)=\max_{Q\in\mathcal Q_{\mathrm{rect}}}Q\{|S|\geq t\}.\qquad\text{(7.4)}
\]

Proof by backward induction. At a final prefix the terminal value is the exact event indicator. At an earlier prefix, any admissible continuation first chooses a feasible branch probability \(q\); conditional success on each branch is at most that branch's induction value. This proves the displayed maximum is an upper bound. The objective is linear in \(q\), so choose \(u_i(h)\) when \(v_1>v_0\), \(\ell_i(h)\) when \(v_1<v_0\), and either endpoint when equal. By induction there are optimal continuation policies in both subtrees. Rectangularity allows their simultaneous use under the chosen \(q\). Combining them attains the bound. Repeating to the root proves equality and existence of an optimising endpoint policy. End proof.

Thus the exact maximiser is allowed to favour different sides after different histories. Such conditional kernels are also a chain-rule representation of a precomputed correlated array. Their mathematical dependence on history does not establish that the historical generator ran online, consulted feedback, or adaptively reacted to participants. This is ordinary finite-horizon dynamic programming; the proof does not invoke iid assignments or outcomes.

### 7.2 Equivalent finite linear program

Assign a nonnegative mass \(x(h)\) to every prefix, with \(x(\varnothing)=1\) and \(x(h)=x(h,0)+x(h,1)\). Impose

\[
\ell_i(h)x(h)\leq x(h,1)\leq u_i(h)x(h).\qquad\text{(7.5)}
\]

Maximise sum of \(x(z)\) over terminal arrays in the tail event. These constraints are linear, including when \(x(h)=0\). Positive prefix masses recover \(q_i(h)=x(h,1)/x(h)\); zero-mass prefixes can be completed arbitrarily. The feasible leaf masses are exactly \(\mathcal Q_{\mathrm{rect}}\), so the linear program has the same optimum as the recursion.

Additional restrictions linking different histories, such as fair marginals, common bias parameters, exchangeability, or an exact global balance requirement, can change the feasible family. Some can be added as linear constraints on leaf masses; independence or a common product parameter is not automatically a linear constraint. The unaugmented Bellman recursion remains an upper bound for any smaller family but need not be sharp for it. Rectangularising a family is a conservative enlargement, not proof that all resulting policies are actual possible designs.

The bounds must cover every relevant prefix, or a specified conservative envelope of all of them. Knowing the numerical propensity only on the single observed path does not supply a full reference distribution. Filling unobserved branches with \([0,1]\) is a valid enlargement only if that is explicitly the intended family; its result may be uninformative.

### 7.3 State compression and its limits

If the bounds depend only on the coordinate \(i\), and the statistic is a fixed weighted sum, the partial sum \(s\) is a sufficient state for optimisation. With \(J_{N+1}(s)=\mathbf1\{|s|\geq t\}\),

\[
J_i(s)=\max_{q\in[\ell_i,u_i]}\{(1-q)J_{i+1}(s-a_i)+qJ_{i+1}(s+a_i)\}.\qquad\text{(7.6)}
\]

Evaluate \(J_1(0)\). The maximising \(q\) still depends on \(s\). If bounds or future allowed actions depend on additional state, that state must be retained. If they depend on the whole prefix, merging histories merely because they have the same partial sum can give the wrong answer. A finite sufficient state may include remaining balance counts, block state or other documented generator state.

Dropping zero-weight or ineligible coordinates is harmless for this deterministic-coordinate-bound model after averaging over omitted history: the retained conditional probabilities remain within the same deterministic bounds. It is not automatically harmless for history-dependent bounds, support constraints, or a known coupled design. In those cases the omitted coordinates can carry relevant assignment state even though they contribute zero to \(S\).

## 8 A smallest counterexample to a fixed product worst case

Take \(N=2\), \(a_1=a_2=1\) and \(t=2\). At every history, require the probability of a plus sign to lie in \([1/4,3/4]\). The event \(|A_1+A_2|\geq2\) is exactly the event that the signs match.

Use \(\Pr(A_1=+1)=1/2\), then

\[
\begin{aligned}\Pr(A_2=+1\mid A_1=+1)&=\tfrac34,\\\Pr(A_2=+1\mid A_1=-1)&=\tfrac14.\end{aligned}\qquad\text{(8.1)}
\]

The four probabilities for \((++,+-,-+,--)\) are \((3/8,1/8,1/8,3/8)\). Both signs have fair marginals, and the tail probability is \(3/4\). Bellman optimality is immediate: after either first sign, the matching probability is at most \(3/4\), and the chosen kernel reaches it.

For an independent product law with \(p_1,p_2\) in \([1/4,3/4]\), the matching probability is

\[
p_1p_2+(1-p_1)(1-p_2).\qquad\text{(8.2)}
\]

It is affine in each coordinate separately, so its maximum is at a box corner. The four corner values are \(5/8,3/8,3/8,5/8\). Hence even the best independent coordinate-specific product law has probability only \(5/8\). The adaptive optimum is strictly larger, \(3/4\).

The same example shows why centring at the unconditional expectation cannot replace a martingale or conditional-drift argument. Here \(\mathbb E[S]=0\) and each increment has magnitude one. Nevertheless

\[
\Pr(|S-\mathbb E[S]|\geq2)=\tfrac34>2\exp(-1),\qquad\text{(8.3)}
\]

so the familiar unadjusted independent-sign two-sided exponential bound is false for this dependent array. The corrected bound in Section 10 includes the allowed conditional drift.

Even within a common-bias independent model, one cannot mechanically maximise a nonmonotone event at the common parameter's interval endpoints. For \(a_1=1\), \(a_2=-1\) and \(t=2\), the event is disagreement of the underlying plus signs. Under iid \(\operatorname{Bernoulli}(p)\), its probability is \(2p(1-p)\), maximised at \(p=1/2\), not at either endpoint of \([1/4,3/4]\). This is a different counterexample concerning a shared parameter; it does not contradict multiaffinity in separately free coordinate parameters.

## 9 Directed tails have exact endpoint product optimisers

Assume now deterministic coordinatewise bounds \([\ell_i,u_i]\), without cross-history restrictions. Write \(w_i=|a_i|\). For \(a_i\) nonnegative put \(X_i=A_i\), \(\alpha_i=\ell_i\) and \(\beta_i=u_i\). For \(a_i\) negative put \(X_i=-A_i\), \(\alpha_i=1-u_i\) and \(\beta_i=1-\ell_i\). Then \(S=\sum_i w_iX_i\) and

\[
\alpha_i\leq\Pr(X_i=+1\mid Z_{<i})\leq\beta_i.\qquad\text{(9.1)}
\]

For zero weights the sign convention is immaterial. Here \(Y_i\) denotes an auxiliary comparison sign, distinct from the recorded evidence in Section 3. Let these \(Y_i\) be independent signs with \(\Pr(Y_i=+1)=\beta_i\). Then for every \(t\),

\[
\max_{Q\in\mathcal Q_{\mathrm{rect}}}Q(S\geq t)=\Pr\!\left(\sum_{i=1}^{N}w_iY_i\geq t\right).\qquad\text{(9.2)}
\]

Proof. Any binary sequential law can be generated using independent uniforms \(U_i\) and its conditional probabilities \(q_i(X_{<i})\), with \(X_i=+1\) when \(U_i\leq q_i\). On the same uniforms put \(Y_i=+1\) when \(U_i\leq\beta_i\). Since \(q_i\leq\beta_i\), \(X_i\leq Y_i\) coordinatewise on every realised path. Nonnegative \(w_i\) imply \(S\leq\sum_i w_iY_i\). This proves the tail inequality. The independent endpoint law \(q_i=\beta_i\) is in \(\mathcal Q_{\mathrm{rect}}\) and attains equality. End proof.

Similarly the exact minimum-direction optimiser has independent signs with plus probabilities \(\alpha_i\):

\[
\max_{Q\in\mathcal Q_{\mathrm{rect}}}Q(S\leq-t)=\Pr\!\left(\sum_{i=1}^{N}w_iY_i^{\mathrm{low}}\leq-t\right).\qquad\text{(9.3)}
\]

For \(t>0\) the upper and lower events are disjoint under any one law, but their maximisers can be different laws. Therefore

\[
r_*(t)\leq\min\{1,\Pr_{\beta}(S\geq t)+\Pr_{\alpha}(S\leq-t)\}.\qquad\text{(9.4)}
\]

This is an upper bound, not generally an equality. In the two-coordinate example its uncapped sum is \(9/16+9/16=9/8\), while the sharp two-sided value is \(3/4\). At \(t=0\) the absolute-tail probability is one and should be handled directly.

If original bounds depend on history, deterministic envelopes \(\alpha_i\) and \(\beta_i\) containing all admissible favourable-sign probabilities still give the same conservative domination. They do not in general give a sharp endpoint law for the original smaller family. No stochastic-order claim here applies to an arbitrary nonmonotone event.

## 10 Scalable conservative exponential bounds

Continue with the deterministic favourable-sign bounds \(\alpha_i,\beta_i\) from Section 9, or valid deterministic envelopes. These formulas can be evaluated without enumerating arrays. They are upper bounds rather than exact two-sided probabilities.

For \(\lambda\geq0\), define

\[
\begin{aligned}C_+(\lambda)&=\prod_{i=1}^{N}\{(1-\beta_i)e^{-\lambda w_i}+\beta_i e^{\lambda w_i}\},\\C_-(\lambda)&=\prod_{i=1}^{N}\{(1-\alpha_i)e^{\lambda w_i}+\alpha_i e^{-\lambda w_i}\}.\end{aligned}\qquad\text{(10.1)}
\]

The conditional exponential factor for \(w_iX_i\) is at most the corresponding factor in \(C_+\), because \(\exp(\lambda w_i)\geq\exp(-\lambda w_i)\). Iterated conditional expectation therefore gives \(\mathbb E_Q\exp(\lambda S)\leq C_+(\lambda)\) under every admissible dependent law. Applying the same reasoning to \(-S\) gives \(C_-\). The elementary pointwise inequality \(\mathbf1\{S\geq t\}\leq\exp(\lambda(S-t))\) gives, for \(t>0\),

\[
\begin{aligned}B_+(t)&=\inf_{\lambda\geq0}e^{-\lambda t}C_+(\lambda),\\B_-(t)&=\inf_{\lambda\geq0}e^{-\lambda t}C_-(\lambda),\\r_*(t)&\leq\min\{1,B_+(t)+B_-(t)\}.\end{aligned}\qquad\text{(10.2)}
\]

Any fixed nonnegative choices of \(\lambda\) give valid upper bounds; numerical optimisation only improves tightness. A numerical minimum must not be rounded down and called a certificate. Logarithms avoid overflow, and certified outward arithmetic can preserve the required upper-bound direction. These are the usual exponential-moment arguments, with the assignment restrictions made explicit.

There is a simpler closed-form bound. Put

\[
V=\sum_{i=1}^{N}w_i^2,\qquad M_+=\sum_{i=1}^{N}w_i(2\beta_i-1),\qquad M_-=\sum_{i=1}^{N}w_i(1-2\alpha_i).\qquad\text{(10.3)}
\]

For \(V>0\),

\[
r_*(t)\leq\min\!\left(1,\exp\!\left(-\frac{[(t-M_+)_+]^2}{2V}\right)+\exp\!\left(-\frac{[(t-M_-)_+]^2}{2V}\right)\right),\qquad\text{(10.4)}
\]

where \(x_+=\max(x,0)\). To prove this without importing an independence premise, consider a sign taking values \(\pm w\) with plus probability \(p\). Let \(K(\lambda)\) be its log moment generating function. \(K(0)=0\), \(K^{\prime}(0)=w(2p-1)\), and \(K^{\prime\prime}(\lambda)\) is the variance under exponential tilting. The tilted variable still lies at \(\pm w\), so \(K^{\prime\prime}(\lambda)\leq w^2\). Integrating twice for \(\lambda\geq0\) gives \(K(\lambda)\leq\lambda w(2p-1)+\lambda^2w^2/2\). Apply this to each deterministic endpoint factor in \(C_+\) and \(C_-\), then minimise the resulting quadratic exponent over \(\lambda\geq0\). This establishes the displayed bound.

The step “variance at most \(w^2\)” follows directly: a variable at \(\pm w\) with tilted mean \(m\) has variance \(w^2-m^2\leq w^2\). Thus the proof is complete in this finite setting. This is the familiar bounded-increment exponential argument, not a new inequality.

For symmetric bounds \(\ell_i=1/2-\varepsilon_i\) and \(u_i=1/2+\varepsilon_i\), with \(0\leq\varepsilon_i\leq1/2\), define \(D=\sum_i2\varepsilon_i|a_i|\). Then \(M_+=M_-=D\) and

\[
r_*(t)\leq\min\!\left(1,2\exp\!\left(-\frac{[(t-D)_+]^2}{2V}\right)\right).\qquad\text{(10.5)}
\]

This keeps the permitted predictable drift explicit. If \(t\leq D\), this particular bound is trivial; that does not prove the exact recursion is trivial. If every conditional probability is exactly \(1/2\) in the specified order, the chain rule gives a product of fair assignment signs conditional on the fixed experimental world. The familiar \(D=0\) expression is then valid, while response dependence and feedback remain allowed under the sharp null. Fair unconditional marginals do not imply that case.

More generally \(S\) minus its actual predictable conditional-mean sum is a martingale, but the compensator requires the actual conditional law. Subtracting only the unconditional \(\mathbb E[S]\), or estimating a propensity and ignoring estimation/model uncertainty, does not supply that martingale. The bounds above avoid this step by using an externally justified deterministic drift envelope.

If \(V=0\), \(S\) is identically zero. Its observed absolute threshold is zero and its \(p\)-value is one. There is no division by zero case to regularise.

## 11 Exact cases and computational certification

### 11.1 Exact finite state calculations

For deterministic coordinate bounds and weights \(a_i=m_i\Delta\) with integer \(m_i\), the partial sum lies on a finite lattice. Let \(L=\sum_i|m_i|\). A dynamic program over at most \(2L+1\) sum states per layer uses \(O(NL)\) arithmetic operations and \(O(L)\) memory for the value alone. Backtracking an optimal policy or saving all layers takes more memory. Sparse reachable sums, parity and symmetry can reduce this count. This is pseudopolynomial in the integer weight magnitudes, not polynomial in their binary encoding length.

For equal-magnitude weights, count states give a particularly small exact recursion. For known independent but nonidentical probabilities, standard convolution of the weighted two-point distributions gives the known-law distribution. For a documented fixed-count uniform assignment, the state includes the remaining count; the next plus probability is the remaining number of plus placements divided by the remaining coordinates. At some states it is zero or one. Known independent blocks with known within-block laws can instead convolve block contribution distributions. None of these shortcuts may be borrowed solely because it is convenient for a particular dataset.

Conditioning on an assignment total can be legitimate when the model establishes the corresponding conditional law. For example, under independent common-probability Bernoulli assignments, conditional on the total number of ones every array with that total has equal probability, regardless of the unknown common probability. This follows because each such array has the same product probability \(p^k(1-p)^{N-k}\). Fair marginals alone do not imply this conditional uniformity. Observing a total does not certify a permutation design.

### 11.2 Why finite does not mean feasible at large sample sizes

The full binary assignment tree has exponentially many leaves. A general history-dependent contract may require exponentially many histories even to specify its input. With arbitrary unequal rational weights, distinct partial sums can also grow exponentially. Clearing denominators can create enormous integer weights, so the \(O(NL)\) statement is not a promise of practicality.

Arithmetic-operation counts omit bit complexity. Exact rational probabilities can acquire large numerators and denominators through multiplication and addition. Real weights must have a specified exact finite representation or a certified numerical enclosure. Ordinary floating-point equality at the inclusive tail threshold can otherwise change the event. A mathematically exact recurrence is not, by itself, a verified numerical implementation or a scalable product interface.

### 11.3 Safe weight coarsening

Choose computational weights \(\widetilde a_i\) and certify

\[
\eta=\sum_{i=1}^{N}|a_i-\widetilde a_i|.\qquad\text{(11.1)}
\]

For every full array, \(|S(z)-\widetilde S(z)|\leq\eta\) by the triangle inequality. Hence

\[
\{|S(z)|\geq t\}\subseteq\{|\widetilde S(z)|\geq\max(0,t-\eta)\}.\qquad\text{(11.2)}
\]

For an unchanged assignment family, an exact or upper-bounded coarse-lattice tail at the lowered threshold is a conservative bound for the original tail. A data-dependent computational choice of coarse weights also remains conservative if the certificate holds pointwise for the same fixed original statistic and assignment family; it must not redefine the inferential target. Use the original observed threshold \(t=|S(z_{\mathrm{obs}})|\); merely rounding the weights and testing at their newly observed threshold has no such automatic guarantee. If \(t\leq\eta\) the displayed outer event is the full space.

This compression is directly usable with deterministic-coordinate bounds. If bounds depend on the unrounded partial sum or other original state, the computational state must retain enough information or use a conservative envelope over all original histories represented by a coarse state. The coarsening error bound does not by itself justify merging assignment states.

### 11.4 Branch pruning and finite resource limits

At partial sum \(s\), let \(R_{\mathrm{rem}}\) be the sum of the absolute remaining weights. All terminal sums lie between \(s-R_{\mathrm{rem}}\) and \(s+R_{\mathrm{rem}}\). If \(|s|+R_{\mathrm{rem}}<t\), the continuation tail value is exactly zero. If \(|s|-R_{\mathrm{rem}}\geq t\), it is exactly one. These are safe sufficient pruning rules; gaps in the attainable weighted sums may allow additional pruning.

An unfinished subtree can be bounded by \([0,1]\). Propagating lower and upper continuation bounds through the monotone Bellman update gives a certified bracket at the root. A resource-limited run may report its upper endpoint as a conservative \(p\)-value or report that the bracket is too wide for the requested decision. It must not return the best policy found as though it were an upper bound. This permits a declared finite computation budget without silently dropping possible assignments.

### 11.5 Monte Carlo statements and their limits

For a known exact assignment law \(Q\), generate \(B\) independent reference arrays from \(Q\) and include the observed assignment in the rank comparison. Conditional on the fixed null trajectory, the \(B+1\) statistics are exchangeable. Therefore

\[
p_{\mathrm{MC}}=\frac{1+\sum_{b=1}^{B}\mathbf1\{T(Z^{(b)})\geq T(z_{\mathrm{obs}})\}}{B+1}\qquad\text{(11.3)}
\]

is a valid conservative Monte Carlo \(p\)-value. To see this, among any fixed \(B+1\) statistic values, at most \(\lfloor\alpha(B+1)\rfloor\) indices can have their inclusive upper rank divided by \(B+1\) at most \(\alpha\); ties can only reduce this number. Exchangeability assigns the observed index no privileged position, so its rejection probability is at most \(\alpha\). The leading one and tie rule are part of the procedure, not cosmetic small-sample corrections. A simulator for a guessed law has only that guessed-law interpretation.

Simulating a selected candidate adversarial policy does not upper-bound the robust optimum. Nor does taking the maximum over a finite, unverified collection of policies prove a maximum over every admissible policy. When a valid deterministic domination reduces the problem to one or two known product tails, simulation can approximate those tails, but an approximate number should not be passed off as a certified upper probability.

A general way to retain conservative validity is to produce, conditional on each observed dataset, a randomised nonnegative upper bound \(U\) for \(p_*(z_{\mathrm{obs}})\) that fails with probability at most \(\delta\), using independent computational randomness and a justified confidence procedure. Replace \(U\) by \(\max(0,U)\) first if necessary. Then \(\min(1,U+\delta)\) is valid. For \(\delta\leq\alpha<1\), the rejection event equals \(\{U+\delta\leq\alpha\}\); it lies inside \(\{p_*\leq\alpha-\delta\}\) except on the failure event, so its probability is at most \((\alpha-\delta)+\delta\). For \(\alpha<\delta\) the event is empty because \(U\geq0\). For \(\alpha=1\) validity is the trivial probability bound by one. This is only useful when the computational procedure genuinely bounds the full robust quantity, not a lower-bound candidate. Simultaneous error across two simulated tails or several bounds must be included in \(\delta\).

## 12 Conditional inference from block complement symmetry

A test can sometimes be calibrated without identifying the entire assignment law. A sufficiently supported symmetry can determine the reference distribution within the observed assignment orbit, while leaving the probabilities of different orbits unknown. This section gives one finite example. It specifies an additional model; it does not assert that any particular experiment satisfies it.

### 12.1 The conditional symmetry contract

Fix legitimate inputs \(X\) and a potential-response world \(u\), excluding the assignment randomisation draws. Partition the finite coordinate set into \(M\) prespecified nonempty blocks \(I_1,\ldots,I_M\). The group

\[
\mathcal G=\{-1,+1\}^{M}\qquad\text{(12.1)}
\]

acts on a sign array \(x\) by multiplying every coordinate in block \(I_b\) by \(e_b\), for \(e\in\mathcal G\). Write this transformed array as \(ex\). Require the legitimate assignment set \(\Omega\) to be closed under these transformations.

Let \(Q\) be the conditional assignment law given \((X,u)\). For each block, let \(f_b\) flip that block alone. The required symmetry is invariance of the full joint law under every such generator:

\[
Q\{A=x\}=Q\{A=f_bx\}
\quad\text{for every }x\in\Omega\quad\text{and every }b.\qquad\text{(12.2)}
\]

Composition then gives the same equality for every \(e\in\mathcal G\). Symmetry of each block's marginal distribution is a different, insufficient premise.

Assume the sharp recorded-trajectory null on the relevant assignments, including availability and every ingredient held fixed by the statistic. Thus the real coefficients \(a_i=a_i(X,u)\) remain fixed under all these transformations. The block partition and conditioning scheme must also be fixed appropriately. Response independence, no interference and no carryover are not required.

### 12.2 Theorem and proof

Define the block contributions and the inclusive orbit probability by

\[
C_b(A)=\sum_{i\in I_b}a_iA_i,\qquad\text{(12.3)}
\]

\[
p_{\mathrm{block}}(A)=2^{-M}\sum_{e\in\mathcal G}
\mathbf1\!\left\{
\left|\sum_{b=1}^{M}e_bC_b(A)\right|
\geq
\left|\sum_{b=1}^{M}C_b(A)\right|
\right\}.\qquad\text{(12.4)}
\]

For every \(\alpha\in[0,1]\) and every positive-probability orbit \(O\),

\[
Q\{p_{\mathrm{block}}(A)\leq\alpha\mid O(A)=O\}\leq\alpha,\qquad\text{(12.5)}
\]

where \(O(A)=\{eA:e\in\mathcal G\}\). Consequently the unconditional rejection probability under \(Q\) is also at most \(\alpha\).

Proof. Because every block is nonempty and every coordinate is a sign, a nonidentity block flip changes at least one coordinate. The action is therefore free, so each orbit has exactly \(2^M\) distinct arrays. Joint-law invariance gives every array in a particular orbit the same mass. Conditional on a positive-probability orbit, the assignment is uniform, regardless of that orbit's total probability.

Put \(T(x)=|\sum_i a_ix_i|\). Fixed coefficients give \(T(eA)=|\sum_b e_bC_b(A)|\), so the displayed probability is the inclusive upper rank of \(T(A)\) divided by the orbit size. Among \(m\) fixed statistic values, at most \(\lfloor\alpha m\rfloor\) positions have inclusive upper rank at most \(\alpha m\); ties cannot increase this number. Uniformity within the orbit proves the conditional inequality. Averaging over the orbits proves the unconditional inequality. Averaging over fixed worlds preserves it if the contract holds in every world under the sharp null. End proof.

Here exactness means finite-sample level control, allowing conservativeness from ties and discrete attainable levels. Orientations producing identical statistic values retain their multiplicities. Uniform weighting of distinct statistic values would be a different procedure.

### 12.3 Independent orientations and dependent block patterns

Let \(V\) be any jointly distributed collection of block sign patterns, conditional on \((X,u)\). Its blocks may be dependent. Given \((V,X,u)\), let \(E\) be uniform on \(\mathcal G\), equivalently a collection of mutually independent fair block signs, and set \(A=EV\). For any fixed \(g\in\mathcal G\), the sign vector \(gE\) is again uniform and independent of \(V\) under the same conditioning. Hence \(gA\) and \(A\) have the same conditional law. This proves the required joint invariance without independent coordinate assignments or independent block patterns.

The representation does not require literal block-orientation coins in a physical implementation. Under an invariant law, orient each block canonically so that its first coordinate is positive. Conditional on the entire canonical pattern collection, the original anchor signs are uniform on \(\mathcal G\). The assignment symmetry, rather than a particular implementation of it, is the premise needing support.

This family can admit deterministic dependence within a block. For example, give each of several two-coordinate blocks the fixed pattern \((+1,+1)\), then orient the blocks independently and fairly. Within a block its second sign is determined by its first. A reached full-prefix conditional probability is therefore zero or one. It violates every finite interval

\[
\left[\frac{1}{1+\Gamma},\frac{\Gamma}{1+\Gamma}\right],
\qquad 1\leq\Gamma<\infty,\qquad\text{(12.6)}
\]

although the block test remains valid. Conversely, for \(\Gamma>1\), a product law with nonfair coordinate biases inside this interval need not be block-complement invariant. The block-symmetry and finite conditional-bound families are therefore not nested in general.

### 12.4 Synthetic separation from marginal block symmetry

Consider six nonzero block contributions that are equal and aligned. Only the two unanimous orientations attain the largest absolute sum, so the inclusive orbit probability is

\[
\frac{2}{2^6}=\frac{1}{32}.\qquad\text{(12.7)}
\]

Now orient all six fixed block patterns using one common fair sign \(H\). Each block separately has a symmetric marginal distribution, and the whole array has global-complement symmetry. Yet its joint law contains only two of the independently flipped orientations. The unsupported six-block reference probability is \(1/32\) at both possible observations, so it rejects at level \(0.05\) with probability one. The valid two-element global-complement reference gives probability one. This is a synthetic failure of an omitted premise, not a reconstruction of an actual assignment process.

With \(k>0\) nonzero block contributions, the smallest possible inclusive two-sided orbit probability is \(2/2^k\), attained when those contributions are aligned in sign. Zero-contribution flips duplicate values equally. If every contribution is zero, the probability is one. A single global-complement block is always uninformative for the absolute statistic. Choosing more, finer blocks requires stronger joint invariance; the improved resolution is not available merely by changing the partition.

### 12.5 Classical attribution and the weaker statistic condition

This is a specialisation of classical finite-group testing. Hemerik and Goeman's section 2 gives group-based level control under a transformed-statistic-vector invariance condition weaker than full-data invariance. That weaker condition can justify a rank test without making the actual assignment orbit uniform. The proof here deliberately retains the stronger joint assignment-law premise.

Jesse Hemerik and Jelle Goeman, *Exact testing with random permutations*, TEST 27, 811–825 (2018), section 2, Definition 1 and Theorem 1. DOI: [10.1007/s11749-017-0571-1](https://doi.org/10.1007/s11749-017-0571-1). [Open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6405018/).

## 13 Proof status and use

The arguments in this companion are ordinary finite mathematical proofs, independently challenged with exact synthetic controls. They are not a newly kernel-checked Lean package. Finite checks supplement rather than replace the proofs. Existing programme results on constructed row laws, observed-policy laws, asymptotic tests and subprobability budgets retain their previous ownership; none is assumed to authenticate an actual assignment mechanism.

A scientific application must bind the intended assignment coordinate, legitimate conditioning inputs, population and schedule, full response and availability null, law family, statistic and numerical procedure. The model can be useful even when its empirical premises remain provisional, provided that conditional status accompanies the result.
