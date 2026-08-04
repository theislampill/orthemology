
AR8R-T236 — finite positive-Horn coinductive truth residual guard
Setting

Use the setting of AR8R-T235. Let τ⊆A be an independently specified truth
set. Assume:

FACT-TRUTH: F⊆τ.
RULE-SOUND: for every (B,h)∈P, B⊆τ implies h∈τ.

Let M=μT, N=νT, and U*=N\M.

Theorem

M⊆τ.

The following are equivalent:

N⊆τ;
U*⊆τ;
every residually self-supporting U over M is a subset of τ.
Proof

Part 1 follows by induction on the least-fixed-point construction, or on finite
Horn proof trees: facts are true and each rule preserves truth.

Since N=M∪U* and M⊆τ, N⊆τ iff U*⊆τ. By AR8R-T235 every residual
self-supporting set is a subset of the greatest such set U*, while U* itself
is residual whenever nonempty. Hence U*⊆τ iff every residual set lies in
τ.

Interpretation boundary

The theorem identifies the additional truth burden of greatest-fixed-point
semantics relative to the least model. It does not generate the truth of
U*; that truth must be established independently.

A source graph, mutually supporting theory, coherentist model, or powers
network may instantiate the formal pattern only after a target-faithful
interpretation is proved. Membership in the residual set is not itself a
truthmaker, ground, authority, source warrant, or explanation.

Prior-art status

Direct corollary of standard positive-Horn soundness and AR8R-T235. No general
novelty credit.
