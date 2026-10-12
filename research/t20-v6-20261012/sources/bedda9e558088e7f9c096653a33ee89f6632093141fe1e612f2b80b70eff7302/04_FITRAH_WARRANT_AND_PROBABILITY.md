# 4. Fiṭrah, proper function, epistemic warrant and the PSR probability argument

**Claim type:** primary-source clarification, independent mathematical diagnostics, and philosophical assessment.  
**Main sources:** A04, A15–A17, M01, M08–M11, M13–M14.  
**Important inheritance:** checkpoint 15 already noticed the worst-case character of the Koons–Pruss Bayesian move and the difference between first-order and higher-order knowledge. The new work supplies explicit formulas, finite controls and a de Finetti scope audit; it does not claim to have first noticed every underlying distinction.

## 4.1 Two Arabic references now replace vague citation chains

The first-principles passage attributed to *Darʾ* 3:309 is directly locatable in the primary text. It concerns the termination of demonstrative reasoning in necessary foundational cognition. The fiṭrah passage routed through *Āthār Ḥujaj al-Tawḥīd* is more directly locatable at *Darʾ* 8:455. Its treatment of natural acknowledgement belongs to a discussion of compatible accounts of the human disposition, not to a generic modern psychological test. [A04, A15]

Neither passage says every confidently held theological belief is immune to error. Nor should they be reduced to a merely passive potentiality which has no direction unless external indoctrination supplies it. A properly source-sensitive reconstruction distinguishes a directed disposition, its maturation, triggering conditions, impediments, actual cognition and volitional response. The earlier Ibn al-Qayyim child-fiṭrah source is useful at exactly the capacity-versus-articulated-recognition boundary. [A16]

This gives a more precise research object than `BelievesInGod = True`. A cognitive episode has a subject, target content, occasion, operating faculty, evidence or signs, an operative basis, and possible obstructing conditions. Which of those is represented determines what the model can establish.

An additional passage in *al-Radd ʿalā al-Manṭiqiyyīn* explicitly allows the same subject matter to be immediate for one person, inferential for another, perceived by one and known through report by another. [A24] This is a distinction between routes and conditions of knowing, not a claim that truth changes with the knower. It supports an episode- and person-indexed interpretation of epistemic basing: requiring every knower to possess the same articulate proof would misrepresent the source’s own account. It does not follow that every claimant has a sound route merely because routes can differ.

## 4.2 Basic warrant is not the same as a proof everyone can repeat

Consider a person who sees a tree. They can know there is a tree without first proving a universal theorem about perception. Likewise, the proposed fiṭrah account treats some recognition as basic or readily elicited rather than dependent on sophisticated philosophical inference.

This analogy is not itself proof that a particular theistic recognition is warranted. It distinguishes two demands:

- the conditions under which the person actually knows;
- the conditions under which a theorist can demonstrate to a sceptic that the person knows.

A formal model of first-order knowledge cannot automatically satisfy the second demand. Conversely, failure to satisfy the second does not, by logic alone, negate the first. The packet includes a reflexive but nontransitive accessibility model in which Kp holds and KKp does not. That is a logical separation, not a model of an actual person's mind and not a claim that every account of knowledge rejects positive introspection.

The same distinction is vital when reading an argument whose stated conclusion concerns knowing that we possess empirical knowledge. It should not be summarised simply as “all knowledge is impossible without this metaphysics.”

## 4.3 A particularly useful correction inside Plantinga's own account

Plantinga's discussion of defeaters distinguishes a bare proper-function account from a purely epistemic one. His revised condition D* explicitly requires the relevant belief-sustaining process to be successfully truth-aimed. Proper functioning directed towards another good, such as protective optimism, does not automatically neutralise an epistemic defeater. [M08]

This is immediately useful for the Orthemological comparison. A faculty working as designed and a faculty warranting a true judgement are not interchangeable simply because the word “proper” occurs in both descriptions. Nor can successful persistence of a belief be treated as proof of its epistemic health.

A proposed fiṭrah model should therefore distinguish:

`Disposition operates`;

`Disposition has the appropriate truth-directed function`;

`This episode's belief is appropriately based`;

`The target proposition is true`;

`Relevant defeat has been addressed`.

The conditions can interact, but none should be silently substituted for another. A model that obtains its truth-directedness from an assumed divine design claim can still be useful as a conditional explanation. It is not an independently neutral proof of that same design claim. This is a scope limitation, not a requirement that ordinary believers perform a full philosophical self-audit before they can know anything.

## 4.4 Koons–Pruss: the exact probabilistic move

The open-access article *Skepticism and the Principle of Sufficient Reason* develops an epistemic route to a restricted explanatory principle. Sections 5–7 include a Bayesian worst-case treatment, an appeal to de Finetti, and an explicit discussion of a neo-Humean escape. The authors themselves recognise that a mathematical construction and a metaphysically warranted probabilistic account are different matters. [M01]

Our first diagnostic isolates the algebra, not the full philosophy. Let:

- U: an observation is uncaused;
- C: it is caused, with C the complement of U;
- K: it has a specified observational character;
- e = P(C ∧ K);
- d = P(U);
- α = P(K | U).

Whenever P(K)>0:

\[
P(U\mid K)=\frac{\alpha d}{e+\alpha d}.
\]

The equation does not determine α. Setting α=1 produces the largest posterior for U at fixed e and d. That is a worst-case choice, not a result of Bayes's theorem. The article makes the choice explicitly; this report does **not** accuse the authors of accidentally dropping α.

The exact test fixes e=1/1000 and d=1/100. With α=1 the posterior is 10/11. With α=1/1000 it is 1/101. Both calculations are correct within their stipulated probability models. Neither α is thereby warranted for real uncaused experiences.

This identifies where the philosophical burden lies. If no objective likelihood exists, one cannot silently promote a chosen numerical bound into an objective chance. If a conservative epistemic policy demands robustness against the whole interval, that policy and its relevance to knowledge must be defended. If the range is narrower, its warrant must also be supplied.

### Imprecise likelihoods can be mathematically informative

For prior p=P(H), likelihood l=P(E|H), and an alternative likelihood a in [u,v], the posterior interval is:

\[
\left[\frac{pl}{pl+(1-p)v},\frac{pl}{pl+(1-p)u}\right].
\]

This follows by monotonicity, with positive denominators. With p=99/100, l=1/2, and a anywhere in [0,1], the interval is [99/101,1]. Thus lack of a precise alternative likelihood does not automatically make mathematical updating vacuous.

This is not a refutation of an argument that no warranted prior or likelihood assignment exists. The example assumes both a prior and an interval; it does not earn them. Its contribution is to stop three claims from collapsing: no precise value, no useful bound, and no warranted probabilistic representation at all.

## 4.5 What de Finetti does—and does not—supply

A probability law can be coherent without being exchangeable. A finite exchangeable law need not be a mixture of identically and independently distributed Bernoulli laws. Infinite exchangeability and the relevant extendibility assumptions are doing real work in the familiar representation theorem. The original finite-exchangeability literature is directly relevant. [M09]

Two exact controls make this plain.

**Coherent but not exchangeable:** assign masses 1/8,1/8,3/8,3/8 to 00,01,10,11. The probabilities are nonnegative and sum to one, but swapping the coordinates exchanges unequal masses 01 and 10.

**Exchangeable but not an iid mixture:** assign mass 1/2 each to 01 and 10. Its covariance is -1/4. In any mixture of iid Bernoulli laws with latent parameter Θ, the covariance is Var(Θ), which is nonnegative. Therefore this finite law cannot have that iid-mixture representation.

The general covariance argument is written out in D6, rather than inferred solely from a numerical scan. The package also checks a projectively consistent uniform-Beta mixture, explicitly separating the probability of one binary word from the probability of a head-count.

Most importantly, a representing parameter or probability measure does not automatically become an efficient cause. A representation theorem states how a law can be expressed; it does not settle whether the represented probabilities are ontic chances, rational credences, or another interpretation. It supplies neither a personal source nor an anti-theistic alternative by itself.

The defensible conclusion for the Koons–Pruss comparison is accordingly narrow: **coherence alone cannot do all the work attributed to the representation theorem**. The probability-theoretic premises and the metaphysical chance-to-causation bridge must be stated separately. This is a substantive local restriction, not a blanket refutation of their restricted PSR or of all epistemic arguments for it.

## 4.6 Sensitivity, safety and the scope of sceptical alternatives

A caused process can be locally reliable while another fact remains unexplained. To convert the latter into a threat to the former, an argument needs a bridge: for example, that the unexplained alternative is relevantly close, uncontrolled intrusions are genuinely available, or no determinate modal/chance structure can distinguish the route.

The reverse mistake is equally easy. Stipulating that all uncaused lookalikes are remote is not evidence that they are remote. A model cannot defeat an epistemic argument by granting itself exactly the causal security that the argument disputes.

This is why the analysis should preserve the target class of facts. A brute universal law may violate an all-facts PSR while falling outside a restricted principle about wholly particular basic natural facts. It is not automatically a counterexample to the actual restricted conclusion. This scope point was already present in checkpoint 15 and is retained, not claimed as new.

A useful research strategy is to distinguish: (a) actual first-order warrant; (b) justified assurance about that warrant; (c) probability assignments over alternative total modal scenarios; and (d) a universal explanatory metaphysics. The connections may be defended, but the connections are not identities.

## 4.7 The remaining Dretske access gap should not be hidden

A separate Dretske paper, *Information and Closure* (2006), has been identified. It is not the unavailable 2005 reply to Hawthorne under another name. Bibliographic and abstract access does not fill the missing body of the original reply. The ledger preserves that limitation. [M10]

The Turner paper on theistic signs provides an additional scholarly comparison for innate recognition and external signs. Its historical reconstruction is not identical to Ibn Taymiyyah's primary words or to Plantinga's complete account. This pass credits the accessible publisher/author record at its limited reading scope rather than pretending to have completed another whole article. [M11]

## 4.8 Research outcome

The new work gives Dot a stronger way to test epistemic claims than a binary `warranted/not warranted` field. It separates truth-directed proper function from mere functional persistence, distinguishes first-order cognition from reflective assurance, and isolates the exact probability assumptions in a live PSR argument.

The broad philosophical question remains: which actual cognitive episodes possess the relevant truth-connected basis, and which explanatory metaphysics is needed for that fact? The mathematics clarifies the question; it does not choose the answer by naming a predicate.
