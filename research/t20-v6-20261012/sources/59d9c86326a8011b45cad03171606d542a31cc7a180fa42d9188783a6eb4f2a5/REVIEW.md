# Independent review: singular Gaussian entrance

11 October 2026 UTC. Ordinary mathematical review only. No protected edits, integration, formal-kernel certification, field priority, general-law PDE uniqueness, metric-completion theorem or T20 closure.

Status: ACCEPT for the stated ordinary-mathematics scope. The frozen author RESULT.md hash is 4bfdbfda33420acc2efc53f7ad3f353b9d7cd763d00b21b8b2860f4805aee47b. No blocking finding. All 15 author manifest entries match the frozen snapshot; normal and optimized author replays each pass 34 controls, including unchanged live predecessor bindings. The independent checker passes 16 controls in normal and optimized Python.

## Independent derivation

For fixed target parameters β∈R and τ>0, the inherited coordinate vector field

    b′ = [b(s−τ)−(b−β)(1+2s+b²/3)]/τ,
    s′ = [2bs(b−β)−(s+2+2b²)(s−τ)]/τ

is polynomial in b,s. Its ordinary locally unique smooth solution from (b0,0) has s′(0)=a=2(1+b0²)>0 and therefore s(t)=at+O(t²)>0 immediately. It is important that existence here comes from the polynomial coordinate field, not a finite value of initial KL. Starting at any sufficiently small positive time, the inherited positive-time theorem applies. Its finite KL sublevel is compact inside s>0 and prevents a later boundary contact or finite-time blowup; it supplies global Gaussian continuation and convergence to the stipulated target.

For t>0 the exact full-density tangent is verified using C=Γ⁻¹−Σ⁻¹−[(b−β)(b−3β)/(3τ)]E11, v=−Cx, α=−(xᵀCx−tr(CΣ))/2. The identity

    Σ′ = −CΣ−ΣC−ΣCΣ

agrees with the coordinate ODE, and substitution in the logarithmic Gaussian density derivative agrees with −div(ρv)/ρ+α as a polynomial identity in the full spatial variable. This establishes an actual full-law solution for positive times; a covariance closure assertion alone would not establish it.

The limiting law is the pushforward of Y∼N(0,1) under Y↦(Y,b0Y). With independent Z∼N(0,1), the coupling (Y,b(t)Y+√s(t)Z) gives expected squared displacement (b(t)−b0)²+s(t)→0. Thus weak endpoint convergence, even W2 convergence, is direct. The endpoint law charges a line of target measure zero, so KL at the endpoint is infinite.

The energy has expansion

    E(t)=−½log t+C0+O(t),
    C0=½[(b0−β)²/τ−1+log(τ/a)].

One should not differentiate an unqualified O(t) remainder to infer dissipation. The reviewer instead independently subtracts the pole from the exact expression D=(∇E)ᵀMc∇E. The remainder D−(1+b²)/s is polynomial in b,s with denominator depending only on τ, so

    D(t)=1/(2t)+O(1).

This proves divergent original-time quadratic action on every [0,ε] and

    ∫₀^ε √D(t)dt=√(2ε)+O(ε^(3/2)).

The Cauchy–Schwarz estimate ∫(|v|+|α|)dμ≤√(2D) makes the spacetime flux and source finite measures near zero. Integrating the established positive-time weak equation from δ>0 and letting δ↓0 therefore gives the endpoint weak equation for compactly supported C1 tests, using both L1 integrability and endpoint convergence. Assigning any values at time zero to the fields is harmless because that time slice is null for dt μt. This statement neither produces L2 fields in original time nor defines the KL differential at the singular endpoint.

Under t=u², the fields transform to 2u v(u²),2u α(u²). Their action density is 4u²D(u²)=2+O(u²), hence action on [0,U] is 2U+O(U³). The transformed curve has a genuine finite-action singular endpoint and retains the entire y marginal. It is a reparametrized trajectory, generally not a solution of the original unrescaled gradient equation in u.

Any other Gaussian positive-time solution of the same ODE, continuous in b,s to (b0,0), satisfies its integral equation from zero because the polynomial right side stays bounded near that state. Standard ODE uniqueness then identifies it with this entrance. This does not prove uniqueness among arbitrary measure-valued weak PDE solutions.

## Scope comparison

- correlated-target-marginal-correction-20261011/RESULT.md supplies the actual positive-time full-density projected flow, minimum tangent fields, compact sublevels and convergence. The singular entrance transports that result using the polynomial extension; it does not rederive a general PDE well-posedness theory.
- fixed-marginal-endpoint-action-20261011/RESULT.md supplies universal singular endpoint feasibility and attained minimum action on compact product tori. Here the state space is Euclidean and the path is a specific Gaussian KL trajectory after time change. The new construction neither needs nor extends that compact attainment theorem; it is not a shortest-path proof.
- full-law-gradient-action-tail-20261010/RESULT.md includes an infinite initial-length example for a different polynomial-energy flow and heavy-tailed law. That example explicitly concerns its own path. Infinite initial energy alone does not force infinite length, so this infinite-KL finite-length entrance does not contradict it.
- fisher-endpoint-geometry-20261010/RESULT.md concerns a different one-sided lognormal statistical family and finite Fisher boundary. It does not establish the present constrained transport–reaction entrance.

## Independent exact controls

check_independent.py verifies covariance and full-density identities, boundary positivity, exact minimum-field dissipation, absence of a second singular pole, the universal asymptotic coefficients, and singular covariance factorization. It also verifies the independently constructed exact witness β=b0=0,τ=1:

    b(t)=0,
    s(t)=2(exp(3t)−1)/(2exp(3t)+1).

This satisfies s′=(s+2)(1−s), s(0)=0 and lim tD(t)=1/2. These symbolic controls supplement the ordinary local ODE, compact-sublevel continuation and weak endpoint arguments. They are not formal-kernel proofs or numerical inference.

## Final frozen-candidate inspection

The added noncentered Gaussian argument is correct. Independently averaging the noncentered score gives the linear coarse source c(b−2β)y/τ, hence multiplier c(b−2β)y/(2τ). The projected gradient at the mean is c(−b/2,1)/τ; the mean dynamics is −(I+Σ) times this vector, giving zero y derivative and c′=−c(1+s+b²/2)/τ. Covariance dynamics is unchanged. The review checker independently verifies the full noncentered density identity, not only its means. Narrow Gaussian trace convergence implies convergence of the Gaussian parameters, even for the degenerate limit, so the stated enlarged Gaussian-class uniqueness is valid.

The finite-horizon positive-state approximation is a valid ordinary continuous-dependence argument in a compact tube for the polynomial extension. The positive-state solutions are globally available from the predecessor. Uniform parameter convergence gives uniform W2 convergence by the displayed coupling; away from zero, energies and dissipations converge uniformly. At zero their initial energies diverge, and the finite-horizon dissipation integral diverges by the positive-state energy identity, as the candidate states.

The author correctly credits gaussian-correction-geometry-20261011/RESULT.md §8 for the earlier finite intrinsic Gaussian distance to zero variance. Also, singular feasibility via the older pure-reaction mixture does not itself depend on compactness; only the cited attainment theorem does. The candidate explicitly keeps these distinctions and does not claim first finite-distance connection.

The stronger impossibility assertion about alternative original-time fields is justified by the inherited full-tangent minimum: any L2 spacetime representation would have L2 slices almost everywhere and action density at least D, contradicting its divergent integral. A weak endpoint L1 identity alone does not evade that obstruction.

No author file was edited. The author snapshot, original-aware replay logs, independent checker/results, and source bindings are contained in this review packet. These are reproducible supplementary controls around an ordinary analytic proof, not a formal proof or an instruction to integrate or close T20.
