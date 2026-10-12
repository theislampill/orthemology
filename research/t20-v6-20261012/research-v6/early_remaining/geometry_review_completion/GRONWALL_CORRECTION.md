# Independent bounded review: nonnegative moving-gradient escape

## Bound source and disposition

Source: `f87b2e98e45301fc58c0bdd00193d2f53f2bcc6c20275af97225f116d1b63c8b`, all 97 lines read. Actual original checker: `49e41d3fe5d1eb5a8ce3874697c481139c0b905a4bf1fe01ff01c1230a742512`, all 24 lines read and freshly run unchanged in an isolated directory; 12 exact symbolic controls pass. The ordinary schedule, existence, tightness and coercivity arguments were independently reviewed, rather than inferred from those checks.

**The counterexample and its intended no-uniform-control conclusion are valid. One narrow Gronwall bound needs its constant convention made explicit. The source remains unchanged.**

## Exact correction

At source lines 83–87, the premise allows a finite real constant C, and the text displays

    H(X(t)) ≤ exp(C T) H(2).

Gronwall gives H(X(t)) ≤ exp(C t) H(2). For C < 0, exp(C t) is greater than exp(C T) when t < T, so the displayed uniform estimate does not follow as written. Use

    H(X(t)) ≤ exp(max(C,0) T) H(2),  0 ≤ t < T,

or declare C ≥ 0 in the premise. Every finite C can be replaced by max(C,0) because H ≥ 0. The uniform bound still contradicts coercivity along X(t) → +∞. This is a proof-wording correction, not a withdrawn theorem or a changed counterexample. Root confirmed this narrow disposition on 2026-10-11.

## Independent mathematical check

Set v(s)=1−5s^5 on [0,1/2]. Then 27/32≤v≤1, so the decreasing smooth time map t(s)=∫_s^(1/2)du/v(u) has a smooth inverse through both endpoints and finite T in [1/2,16/27]. Its definition does not use the state trajectory.

With a=s−s^6 and V_t(x)=(x^4−a x^5)^2/2, each frozen potential is a nonnegative coercive polynomial, including V_T=x^8/2. At X=1/s, the inner polynomial equals s and its spatial derivative equals −v/s^3. Therefore −∂xV_t(X)=v/s²=X′ and V_t(X)=s²/2 decreases strictly to zero, while X escapes at finite T.

The weight ∫_0^T V_t(X(t))dt=∫_0^(1/2)u²/[2v(u)]du is finite and at most T/8, so the unnormalized surviving mass has a strictly positive finite limit. Dirac covariance cancels and the supplied full hierarchy holds at every preterminal time. The Dirac probabilities are not tight; their first moment diverges; there is no weak probability or coordinatewise full-moment continuation on the original real carrier.

The failure is absence of a common compact barrier for the moving sublevels. It is compatible with the positive common-energy theorem and with forward completeness of each separately frozen autonomous gradient flow. Smooth coefficient continuation at T does not give state-trajectory continuation there.
