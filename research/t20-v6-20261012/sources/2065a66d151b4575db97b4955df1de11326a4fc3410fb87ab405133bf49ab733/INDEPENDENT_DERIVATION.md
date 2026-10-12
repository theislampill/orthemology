# Independent derivation and adversarial representation checks

10 October 2026. The core argument below was derived from the assignment before reading the author's report. The subsequent checks compare that argument against the frozen author report. The parent supplied the candidate compactification and inequalities in the assignment; this is independent validation, not independent discovery. The parent's constructive notes were not used as evidence.

## 1. Input and negative information

The input is one oracle for (r,k) approximating m_r to 2^-k, with the promises m_0=1 and existence of exactly one half-line probability with these finite moments. Promises supply neither decidability nor a numerical convergence modulus.

Let P=P([0,1]) with ordinary W1 and rational finite atomic ideal points. Classical compactness follows from compactness of the interval. Effective total boundedness is explicit: round locations to mesh 1/n, then round down n of the n+1 weights to denominator Q and assign the remaining mass to the last location. The two W1 costs are <=1/n and <n/Q. The finite list of all denominator-Q grid probabilities is therefore a certified finite net. Distances of ideal points are exact finite rational CDF sums.

These nets semidecide covers by finitely many ideal open balls. Refine the net until each center has distance plus the net radius strictly below a covering-ball radius. Soundness is the triangle inequality; termination is the positive minimum of the maximum ball margin on the compact space. Dovetail finite subfamilies for enumerated open sets. No feasibility test for exact real equalities is involved.

Write c_N(y)=min(y/(1-y),N), extending with c_N(1)=N. Its Lipschitz constant is <=(N+1)^2. For r>=1, I_rN(lambda)=integral c_N^r has Lipschitz constant L=r N^(r-1)(N+1)^2 on P. Define F by all constraints m_r-m_(r+1)/N <= I_rN <= m_r for integers r,N>=1.

The complement is effectively open, not merely classically open. For example at an ideal center q the strict lower violation m_r-m_(r+1)/N-I_rN(q)>a>0 can be certified by finite oracle approximations. Any rational ball of radius rho with L rho<a then lies in that violation set. Enumerate all such certified balls, and analogously for upper violations. Every violating measure is eventually covered by one, using its positive violation margin and ideal-point density. This explicitly supplies the negative information consumed by the cover test.

## 2. Exact identification of the fibre

A representing law satisfies the upper inequalities and the lower ones since, for x>N,

0 <= x^r-min(x,N)^r <= x^r <= x^(r+1)/N.

Conversely, if lambda satisfies the constraints, N lambda({1})<=I_1N<=m_1 for every N; thus lambda({1})=0. After inverse compactification, monotone convergence gives each moment <=m_r. The lower bound tends to m_r because the NEXT moment input is finite; hence equality. Mass normalization was built into P. There is no need to infer computability of lambda({1}) or decide whether an input moment vanishes.

Both halves matter. Upper constraints alone generally leave many measures, including delta_0, and do not identify a moment sequence. The lower constraints encode recoverable tail information from supplied numerical next-moment names. Replacing those names by assertions of finiteness would break this representation argument.

## 3. Uniform singleton extraction

On the promised domain F is a singleton {lambda}. For any precision epsilon enumerate all ideal q and semidecide P subset (P\\F) union B(q,epsilon). Run these searches in parallel. At least one succeeds because a dense ideal center lies within epsilon of lambda; every success certifies the requested error. The finite subcover consumes finitely many grades and precision queries. There is no need to recognize uniqueness, choose a point of a general closed set, or compute a uniform condition number over the entire moment domain. This is the standard effective compact singleton principle, rather than a new general selection theorem.

## 4. Removing the artificial endpoint and output metric

For the half-line use d_b(x,z)=min(1,|x-z|), and the corresponding Wasserstein metric, which gives the standard weak-measure representation. A compact approximation q is sent to (c_R)_*q. The true-law clipping cost in that metric is <=m_1/R; transporting q incurs at most (R+1)^2 W1(q,lambda). The pushforward of an ideal point is again rational finite atomic, even if q has mass at y=1. Thus choose R from a rational bound on m_1, then request a sufficiently precise compact approximation. This proves a genuine output name without assuming inverse compactification is continuous at 1.

The author's optional ordinary-W1 strengthening is also valid: the true clipping cost is <=m_2/R, so the same construction works in the finite-first-moment Wasserstein representation. This does not compute an indexed l1 allocation: evaluation of atom masses remains discontinuous at accumulating supports.

## 5. Joint damping without a zero test

At a named t>=0 choose rational U>t by approximation. Integrate g(y)=c_R(y)^r exp(-t c_R(y)) against lambda. Its Lipschitz constant for r>=1 is bounded by (r R^(r-1)+U R^r)(R+1)^2. Its value can be computed uniformly on [0,1] and t in [0,U]; t-name errors cost <=R^(r+1) times their magnitude. On x>R both the original and clipped integrands are bounded by x^r, so the total integral error is <=2m_(r+1)/R. At r=0 the better error is m_1/R. These bounds hold uniformly for every t>=0, including zero, and supply a finite precision budget jointly in grade and named t.

Z(t)>=exp(-U H)>0 for H>m_1 by Jensen. A certified positive rational lower bound yields effective normalized division. Bounded Lipschitz test integration yields the normalized tilted weak law. All finite derivative orders follow from A_r^(k)=(-1)^k A_(r+k), with one-sided derivatives at zero; finite next moments justify dominated difference quotients. This is smooth one-sided data, not a convergent Taylor expansion.

## 6. Strict enlargement and geometric scope

For f(x)=exp(-sqrt(x))/2, z=sqrt(x) gives density z exp(-z), total mass one, and m_r=(2r+1)!. Every positive exponential in x has divergent integral. The symmetric square-root lift of ANY competing law has even moments (2r+1)! and zero odd moments. For 0<b<1 monotone convergence gives E cosh(bY)=(1+b^2)/(1-b^2)^2, hence E exp(b|Y|)<infinity. Identical convergent moment expansions force identical characteristic functions first locally and then throughout the common strip. Squaring identifies the original law. Taylor coefficients of Z at zero have divergent term ratio for every nonzero parameter, so the strict extension is real.

For the Fisher corollary, the affine t coordinate, its scale and basepoint, and the supplied mean q(0) are necessary input. V^(n-2)(0)=(-1)^n kappa_n, and the finite Bell recurrence computes moments uniformly. Neither an arbitrary coordinate-dependent abstract metric jet nor an uncalibrated Fisher tensor is interchangeable with these data. Point masses are admitted, so no nonsingular mean-coordinate chart follows without additional assumptions.

## 7. Sources and inherited scope

Directly read the author's full report; the exponential-tail predecessor's input and continuation statements; and the capped-recovery predecessor including its compact singleton proof, representation contract, l1 boundary, and bounded-simplex continuation. These ancestors already own effective compact inversion, bounded moment continuation, and signed strict-interior continuation under a supplied exponential bound. The present theorem adds the unbounded moment fibre built from its own next-moment names and its determinate-input nonnegative continuation. It does not supersede the ancestors' stronger/different conclusions, repair their endpoint counterexamples, or establish field priority.

Primary sources independently opened: Galatolo–Hoyrup–Rojas, https://members.loria.fr/MHoyrup/computinvmeas.pdf, Proposition 1 / Remark 4 and Theorem 2.9; Hoyrup–Rojas, https://members.loria.fr/MHoyrup/random_metric.pdf, Section 4.3. They support standard compact-singleton and computable-integration ancestry. The concrete bounds above are checked directly, rather than attributed as a new result of those sources.

## 8. Later frozen addition: constant readouts

The revised report adds a parent-proposed corollary after the initial derivation. On the nonempty effective compact fibre, a supplied computable continuous G has effectively compact image. If its image is promised singleton, enumerate intervals of length below the requested error and semidecide fibre containment in their inverse images. Some succeeds; every success encloses the same value. Relative computability is sufficient because the restriction domain is the represented compact fibre. For the entire q(t), equality across two representing laws implies (log Z_mu-log Z_nu)'=0 on (0,infinity). Each Z tends to 1 at zero by bounded convergence, fixing that constant to zero. Standard Laplace uniqueness then identifies the laws. This extension is correct and makes no new arbitrary-law selection claim.
