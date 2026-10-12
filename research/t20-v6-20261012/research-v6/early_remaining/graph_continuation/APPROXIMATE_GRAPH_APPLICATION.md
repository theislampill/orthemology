# Approximate graph-continuation memory: faithful application

Status: new ordinary specialization of an inherited proved inequality. Independent root review pending. No new Lean theorem and no universal claim established by finite graph enumeration.

## Bound source and model

The inherited manuscript `continuation_complete_orthing.md`, SHA256626504b64c2d7817b882e74992ba989d83c7ef8e67b1467b537101c2b804edb9, Git blob99d0434aad8b8a841f59eb078e2b70c0b961d226 at commit3a0bdeaa1394c656245cae9599adcb143e885059, proves the exact moment-defect identity at lines138–178 and the Walsh approximate-memory bound at lines398–430. Prior reading covered1–330; this branch newly read300–804 and independently reread98–190 to bind the exact normalization used below.

Use the graph packet's declared model and ordinary whole-word correspondence: finite simple undirected G on named slots V, sign states X={−1,+1}^V, both orientations of every edge, deterministic gates x_i←x_i x_j, no informative intermediate observation or feedback, individual terminal unary questions, and at most h sequential elementary updates. Let

    R_h(G)={nonempty S⊆V : 2 tau_G(S)-|S|-1 ≤ h},
    q=|R_h(G)|,
    chi_S(x)=product_(i∈S) x_i,
    b_S(x)=(1-chi_S(x))/2.

Infinite-cost masks are excluded. The source's general visited-set/synthesis theorem and ordinary graph/pullback interpretation identify exactly this required family. A finite graph test is not used to prove that identification.

Let W⊆R^X be a fixed linear observable space containing1, of dimension d+1. A basis1,phi_1,…,phi_d defines the acquired moment vector m_W(lambda)=(E_lambda phi_j)_(j=1)^d. Thus d counts independent nonconstant linear law statistics, not bits, raw samples, tensor order, or arbitrary nonlinear acquisition features.

Assume 0≤epsilon<1/2 and, for every S∈R_h(G), an arbitrary decoder psi_S on the attained moment image satisfies

    sup_(lambda∈Delta(X)) |E_lambda b_S - psi_S(m_W(lambda))| ≤ epsilon.

The error is uniform absolute error in each declared event probability, simultaneously valid across all input probability laws and all required individual questions. No continuity or linearity is required of the decoders. The statement does not assume joint-event or joint-output-law recovery.

Then

    d ≥ q(1-4 epsilon²),

or d≥ceil(q(1-4 epsilon²)) as an integer count. If q=0 the conclusion is d≥0. The endpoint epsilon=1/2 also gives the valid but trivial bound0.

## Proof

Equip R^X with the probability-normalized uniform inner product

    <f,g>_u = 2^(-|V|) sum_(x∈X) f(x)g(x),
    ||f||_(2,u)²=<f,f>_u,
    ||f||_infinity=max_(x∈X)|f(x)|.

The nonempty Walsh characters chi_S form an orthonormal family and are orthogonal to1. Let P be orthogonal projection onto W. Since1∈W, each P chi_S lies in W∩1-perp, which has dimension d. Bessel's inequality, summed over an orthonormal basis of that subspace, gives

    sum_(S∈R_h) ||P chi_S||_(2,u)² ≤ d.                 (1)

The inherited exact defect theorem says that even an arbitrary decoder cannot have universal law error smaller than dist_infinity(b_S,W). Our hypothesis therefore implies dist_infinity(b_S,W)≤epsilon. Because1∈W, the affine transformation f↦(1-f)/2 maps W bijectively to itself, so

    dist_infinity(chi_S,W)=2 dist_infinity(b_S,W)≤2epsilon.

The uniform measure has total mass1, hence ||f||_(2,u)≤||f||_infinity. Orthogonal projection minimizes the L² error; consequently

    ||chi_S-P chi_S||_(2,u)≤2epsilon.

By orthogonality and ||chi_S||_(2,u)=1,

    ||P chi_S||_(2,u)² ≥ 1-4epsilon².

Sum over the q required characters and apply(1). This proves the claimed bound.

## Interpretation and limits

This is the predecessor's exact proof applied to the graph-selected orthonormal family, rather than substituting tensor degree for graph accessibility. For the four-slot path at horizon3, q=12 and epsilon=1/10 imply d≥ceil(288/25)=12; at saturation h=5, q=15 gives d≥ceil(360/25)=15. These numerical substitutions use exact rational arithmetic.

The result is necessary, not an exact optimal approximation frontier at intermediate tolerance. It applies to fixed linear moment acquisition with full-simplex coverage, even when its decoders are nonlinear. It says nothing by itself about arbitrary approximate nonlinear encoders, restricted input-law families, statistical estimation from samples, state-dependent sensing, reacquisition, permission to change the continuation menu, or physical architecture costs. The sharper full exact continuous-encoder dimension result has a different hypothesis and remains separately typed.
