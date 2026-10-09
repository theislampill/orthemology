# Failed shortcuts and retained boundaries

These are exact mathematical countercontrols, not empirical failures of an apparatus.

## 1. The earlier unbalanced hard pair is insufficient against arbitrary rates

Suppose H0 has k singleton routes only on root 1 and H1 adds the full-support route on r>=2 roots. The fixed-p mask instrument distinguishes this pair only through a p^r term. But an arbitrary-rate protocol can set all other root rates to one and choose a_1=1/k for k>=2. Its no-effect means become

q0=(1-1/k)^k,
q1=(1-1/k)^(k+1).

This is exactly the adjacent one-root count experiment, with order k^-1 gap and order k^-2 information rather than a mandatory k^-2r scale. The earlier fixed-p lower proof cannot simply have its scope relabeled to include arbitrary rates.

The balanced baseline puts k singleton routes at every root. Turning any root fully on then saturates the common endpoint under both models. Reducing any root too much suppresses the added full-support route. The separable information proof quantifies this trade-off without assigning a positive constant variance floor.

## 2. No uniform Bernoulli variance floor

Even for the balanced pair, letting all a_i approach zero sends q1 toward one, while letting a root rate approach one sends q1 toward zero. Thus q1(1-q1) has no positive rate-uniform lower bound. Dividing a squared endpoint gap by a claimed constant variance floor is invalid. The proved factor allocation keeps the actual vanishing denominators and compensates them with the baseline powers.

## 3. Per-root count is not the total bound

The hard pair has rk and rk+1 routes, not k and k+1. Plugging k directly into the inherited total-count upper theorem would violate its input contract for r>=2. The valid choice is k=floor((L-1)/r), and the upper must use the supplied total L. The theorem is stated only for L>=r+1 so k>=1. Smaller total bounds do not admit this hard pair; no lower claim for them is inferred from it.

## 4. Rate zero is not an issued-root deletion

The model chooses S first and evaluates guards on S, then assigns attenuation rates. Our pair has no guards, so a disabled positive support can arise either from an omitted root or a zero rate without changing the pair's equality. This does not authorize treating those actions as interchangeable in the larger guarded class. The matching upper retains its issued-profile/mask distinction.

## 5. Addressable routes or internal traces change the experiment

If a controller can assign separate rates to particular route occurrences, it can turn all singleton routes off and the additional full-support route on. The endpoint becomes deterministic and different between the models. The theorem permits root-specific rates shared across occurrences, not such a route-addressable control. Observing which route fired likewise changes the observation law. Neither is a counterexample within the theorem's menu.

## 6. Confidence and sampling limits

As delta tends to 1/2, kl(1-delta,delta) tends to zero whereas log(1/delta) does not. The exact lower bound is therefore kept in binary-KL form for the full range 0<delta<1/2. Uniform logarithmic matching is stated only for delta<=1/4. A fixed-budget conditional KL chain is not an expected-stopping-time proof. Correct one-trial marginals alone do not justify that chain if the actual cross-trial process has extra hidden dependence.

## 7. Common rate is not a perfectly shared random gate

Give each root one Bernoulli gate and reuse that same gate for all route occurrences involving that root. Under H0 the effect occurs when any issued root gate succeeds; duplicating its singleton route k times makes no difference. Under H1 the extra full-support success event is already contained in that same OR event. Thus H0 and H1 are identical under every issued profile and every rate vector in this different gate-sharing model.

For two roots, k=2 and rates (1/2,1/2), the shared-gate no-effect probability is 1/4 in both worlds. The stipulated independent-route model instead gives q0=1/16 and q1=3/64. Equal marginal root rates do not license either substitution. This counterexample is not evidence against the theorem; it rejects an illicit change of its response kernel and prevents the matched upper from being applied under perfectly correlated duplicates.
