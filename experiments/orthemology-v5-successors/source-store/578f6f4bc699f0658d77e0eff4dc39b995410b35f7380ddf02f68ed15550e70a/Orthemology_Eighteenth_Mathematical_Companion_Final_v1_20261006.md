> **DERIVED public reading projection.** Original DOCX `Orthemology_Eighteenth_Mathematical_Companion_Final_v1_20261006.docx`; original SHA-256 `e1cacf4081f897cdd8eacea9fd8cc75274e4f6f3d90845a01082112b00242960`. This projection was prepared on 7 October 2026. Original authored text order, link destinations, native mathematics, AI attribution, dates, and scope limitations are retained. Research, reading, review, and verification claims below remain the source’s dated claims, not fresh acceptance or replication. Internal page references name the original DOCX pagination; Markdown has no matching page numbers. Where present, native equations are rendered as TeX with an exact source-to-projection map and declared spacing and prime-glyph normalization. Word typography, pagination, and dynamic page-number fields are not reproduced.

# Orthemology Eighteenth Mathematical Companion

One hidden irreversible change and effective parity control

Prepared by dot, an AI assistant powered by OpenAI

6 October 2026

# 1 How to read the result

A controller can observe what happens without observing which rules now govern it. This companion studies a precise version of that problem. There are two finite stochastic models. The environment begins in model 0, may change once to model 1 after seeing a selected action, and may also never change. The controller receives physical observations, but no announcement of the change. Its objective concerns the priorities that recur forever.

The principal result is a complete finite criterion for the existence of an almost-sure winning policy. A finite certificate exists exactly when any lawful measurable policy can win. From a positive certificate one can construct a deterministic program that acts on finite observed histories. A negative answer can be accompanied by finite evidence excluding every admitted policy. For explicitly encoded rational probabilities, the existence decision is P-complete under deterministic logarithmic-space many-one reductions.

The certificate is finite, but the winning program can need unbounded counters. A separate example proves that no finite-memory time-homogeneous randomised controller can replace it in general. Statistical recovery has no promised deadline. The theorem concerns probability-one eventual success under each permitted adversary, rather than success on every possible infinite support path.

Three information distinctions are essential. First, an observation impossible in model 0 proves that the change has happened; an observation impossible in model 1 does not prevent a later change. Second, exact numerical row equality can matter when each hidden mode owns a different priority map. Third, when the priority map is common to both modes, a stronger synthesis theorem is available: trusted support information alone produces one policy that works for every numerical realisation of those supports.

Sections 2–4 specify the model and finite certificate. Sections 5–8 give the probability arguments and both directions of the main theorem. Sections 9–10 turn the criterion into a signed decision and a polynomial construction. Sections 11–12 separate real-number representation from uniform support-only control. Section 13 provides small examples that distinguish the claims. Section 14 records the precise mathematical and formal scope.

The arguments are ordinary mathematical proofs. Machine-checked coverage and implementation qualification are described separately; this companion does not equate the ordinary theorem with an unrestricted kernel-checked endpoint. The result extends the programme’s earlier fixed-hidden-model work while retaining ownership of its stationary learning, finite-certificate and memory-separation ingredients.

# 2 The operational model

## Finite data and lawful actions

Let $S$ and $A$ be nonempty finite sets with fixed effective enumerations, and let $s_{0}\text{∈}S\text{.}$ At state $s\text{,}$ the controller must select an action from a supplied nonempty menu $M\text{(}s\text{)}\text{⊆}A\text{.}$ These menus are independently declared lawful in both modes. They are not inferred from transition probabilities or from an estimated hidden mode.

For each mode $i\text{∈}\text{\{}0\text{,}1\text{\}}\text{,}$ the input contains a stochastic row family and a natural-number priority map:

$$P_{i}\text{:}S\text{×}A\text{×}S\text{→}\text{[}0\text{,}1\text{]}\text{,}\quad\quad \sum_{y\text{∈}S}^{}P_{i}\text{(}s\text{,}a\text{,}y\text{)}\text{=}1\text{,}\quad\quad d_{i}\text{:}S\text{×}A\text{→}\text{ℕ}\text{.}$$

The principal algorithmic theorem takes every row entry to be an exactly encoded rational number. Section 11 extends the mathematical existence theorem to arbitrary real rows. Priorities have finite range because the pair carrier $B\text{=}S\text{×}A$ is finite. We write $e\text{=}\text{(}s\text{,}a\text{)}$ and $P_{i}\text{(}e\text{,}y\text{)}\text{=}P_{i}\text{(}s\text{,}a\text{,}y\text{)}\text{.}$

The controller sees physical states and its own past actions. Before round $t\text{,}$ its public history is

$$h_{t}\text{=}\text{(}x_{0}\text{,}a_{0}\text{,}x_{1}\text{,}\text{…}\text{,}a_{t\text{−}1}\text{,}x_{t}\text{)}\text{,}\quad\quad x_{0}\text{=}s_{0}\text{.}$$

Initially the mode is $m_{0}\text{=}0\text{.}$ The order of a round is fixed:

1.  The controller chooses $a_{t}\text{∈}M\text{(}x_{t}\text{)}$ from its observed history and private seed.
2.  After seeing that action, the adversary chooses $m_{t\text{+}1}\text{∈}\text{\{}m_{t}\text{,}1\text{\}}\text{.}$
3.  The next receipt is sampled from $P_{m_{t\text{+}1}}\text{(}x_{t}\text{,}a_{t}\text{,}\text{⋅}\text{)}\text{.}$
4.  The priority of the round is $c_{t}\text{=}d_{m_{t\text{+}1}}\text{(}x_{t}\text{,}a_{t}\text{)}\text{.}$

The governing receipt mode therefore also owns the departure-pair priority. Neither that mode nor that priority is supplied as an additional observation. Once the mode is 1 it remains 1. A change at index $n$ first changes the row and priority of round $n\text{,}$ and retaining mode 0 forever is legal.

## Policies and success

A private-seed policy has a probability space $\text{(}R\text{,}\text{ℛ}\text{,}\nu\text{)}$ and a measurable action map $\pi\text{:}R\text{×}H_{\text{fin}}\text{→}A\text{.}$ The seed is independent of the environment’s fresh transition randomness and the adversary’s private randomness. This representation permits arbitrary private memory and a whole sequence of private random choices; it does not assume a finite-state controller or a standard Borel seed space. The complete action and receipt history remains available to the policy.

A legal adversary is measurable and nonanticipating. It may use the public history, the currently selected action, its own earlier choices and its own random seed. It may not inspect the controller’s hidden seed or future transition randomness. The environment samples the prescribed fresh row conditional on the actual past and governing mode.

Write $\text{𝖯𝖺𝗋}$ for minimum-infinitely-often parity: the least priority appearing infinitely often is even. The existence question is

$$\text{∃}\pi\: \text{∀}\alpha\quad\quad \underset{s_{0}}{\overset{\pi\text{,}\alpha}{\text{Pr}}}\text{(}\text{𝖯𝖺𝗋}\text{)}\text{=}1\text{.}$$

One policy must work for all legal adversaries. No bounded detection time, expected recovery duration or final declaration of the hidden mode is required. A finite prefix cannot determine failure of this tail objective. For a total policy, histories inconsistent with its intended invariant receive a fixed lawful fallback action, such as the first action in the current menu.

## The two public layers

A finite history is mode-0 compatible when every recorded transition has positive $P_{0}$ probability. While compatibility persists, the controller remains in the uncertain layer. A past receipt with zero $P_{1}$ probability cannot permanently eliminate mode 1: the adversary may change after the next chosen action.

In contrast, an actual receipt satisfying $P_{0}\text{(}x_{t}\text{,}a_{t}\text{,}x_{t\text{+}1}\text{)}\text{=}0$ proves that mode 1 governed that round and will govern every subsequent round. The controller then enters the known-mode-1 layer permanently. This is a sound consequence of the exact support data. There is no assumption that such a receipt ever occurs, even after an actual change.

# 3 Reduction to deterministic change indices

Let $Q_{n}^{\pi}$ be the actual run law for policy $\pi$ when rounds before $n$ use mode 0 and rounds from $n$ onwards use mode 1. Let $Q_{\text{∞}}^{\pi}$ be its no-change law. Include the priorities determined by the governing modes in these laws.

**Lemma 1. Fixed-index equivalence.** A fixed lawful measurable private-seed policy wins against every legal one-change adversary if and only if it wins under $Q_{\text{∞}}^{\pi}$ and under $Q_{n}^{\pi}$ for every $n\text{∈}\text{ℕ}\text{.}$

**Proof.** The forward implication uses deterministic legal adversaries. For the reverse implication, put the policy seed, the adversary’s private random seed and an independent sequence of uniform random variables on one product probability space. Fix an inverse cumulative distribution sampler for each finite row. Construct the actual adaptive run and, on the same space, a run for every deterministic change index, all using the same policy seed and uniform sequence.

Let $\tau$ be the actual first change index. On $\text{\{}\tau\text{=}n\text{\}}\text{,}$ the actual run and the fixed-$n$ run agree at every time. Before $n$ they have the same mode-0 histories, so the same seed gives the same actions; at $n$ both first use mode 1; thereafter both remain there. Induction identifies their receipts and priorities as well. The same argument identifies the actual run with the no-change run on $\text{\{}\tau\text{=}\text{∞}\text{\}}\text{.}$ Consequently,

$$\text{\{}\text{actual parity failure}\text{\}}\text{⊆}\underset{n\text{∈}\text{ℕ}\text{∪}\text{\{}\text{∞}\text{\}}}{\text{⋃}}\text{\{}\text{fixed-index }n\text{ parity failure}\text{\}}\text{.}$$

Every event on the right is null, including after adjoining the unused adversary randomness. A countable union of null events is null. Nonanticipation ensures that the constructed adaptive process has the required conditional row law. We have not conditioned on a random change time and asserted that its selected tail is independent. The policy and seed measure have remained unchanged.

There is also an exact positive-mixture representation. Use a hidden permanent-mode-0 status with initial probability one half. Otherwise start in a waiting status that independently changes to an absorbing mode-1 status with probability one half after each action. The resulting law is

$$Q_{\text{mix}}^{\pi}\text{=}\frac{1}{2}Q_{\text{∞}}^{\pi}\text{+}\sum_{n\text{≥}0}^{}2^{\text{−}n\text{−}2}Q_{n}^{\pi}\text{.}$$

Every coefficient is positive, so this mixture wins almost surely exactly when every component law does. The permanent branch is essential: geometric waiting alone gives no positive no-change atom. This construction describes an equivalent auxiliary probability law; it does not replace the adversary by an assumed hazard model or supply a generic partially observed parity theorem.

# 4 The finite certificate and main theorem

## Components and their priorities

For a nonempty pair set $E\text{⊆}B\text{,}$ define its used source states by $U\text{(}E\text{)}\text{=}\text{\{}s\text{:}\text{∃}a\: \text{(}s\text{,}a\text{)}\text{∈}E\text{\}}\text{.}$ It is a $P_{\theta}$ end component when every positive successor of every pair in $E$ belongs to $U\text{(}E\text{)}\text{,}$ and the graph of those positive transitions is strongly connected on $U\text{(}E\text{)}\text{.}$ Every used source has at least one action in $E\text{,}$ by definition. An end component need not be maximal.

A known-mode-1 good component $F$ is a $P_{1}$ end component for which $\text{min}_{e\text{∈}F}d_{1}\text{(}e\text{)}$ is even. An uncertain candidate-$\theta$ component $E$ satisfies three conditions:

1.  It is a $P_{\theta}$ end component.
2.  It cannot reveal mode 1 under its candidate kernel: $P_{\theta}\text{(}e\text{,}y\text{)}\text{>}0$ implies $P_{0}\text{(}e\text{,}y\text{)}\text{>}0\text{,}$ for every $e\text{∈}E\text{.}$
3.  Every mode whose full rows agree with the candidate throughout $E$ has even priority minimum there:

$$\text{[}\text{∀}e\text{∈}E\: \text{∀}y\text{∈}S\quad P_{\sigma}\text{(}e\text{,}y\text{)}\text{=}P_{\theta}\text{(}e\text{,}y\text{)}\text{]}\: \text{⇒}\: \underset{e\text{∈}E}{\text{min}}d_{\sigma}\text{(}e\text{)}\text{ is even}\text{,}\quad\quad \sigma\text{∈}\text{\{}0\text{,}1\text{\}}\text{.}$$

The candidate always agrees with itself. An unequal-row rival may have odd minimum. In that case the controller must either detect a recurrent discrepancy or leave the component; it cannot simply assume that the rival is absent. Equality means equality of complete numerical distributions, not equality of positive supports or selected coordinates.

## Safety and progress data

A positive certificate supplies state sets $K\text{,}W\text{⊆}S\text{,}$ known-layer pairs $D_{1}\text{,}$ uncertain-layer pairs $D\text{,}$ and finitely many qualifying components and finite paths. It requires $s_{0}\text{∈}W\text{.}$ The regions may overlap, and $K$ may be empty.

Every $\text{(}s\text{,}a\text{)}\text{∈}D_{1}$ has $s\text{∈}K\text{,}$ $a\text{∈}M\text{(}s\text{)}\text{,}$ and every $P_{1}$-positive successor in $K\text{.}$ From every state in $K\text{,}$ a positive $P_{1}$ path using $D_{1}$ reaches a used state of a supplied known-layer good component contained in $D_{1}\text{.}$

Every $\text{(}s\text{,}a\text{)}\text{∈}D$ has $s\text{∈}W\text{,}$ $a\text{∈}M\text{(}s\text{)}\text{,}$ and satisfies

$$P_{0}\text{(}s\text{,}a\text{,}y\text{)}\text{>}0\text{⇒}y\text{∈}W\text{,}\quad\quad \text{(}P_{1}\text{(}s\text{,}a\text{,}y\text{)}\text{>}0\: \text{and}\: P_{0}\text{(}s\text{,}a\text{,}y\text{)}\text{=}0\text{)}\text{⇒}y\text{∈}K\text{.}$$

Thus every possible receipt is accounted for: a mode-0-compatible receipt stays in $W\text{,}$ while a mode-1-only receipt enters $K\text{.}$

Every supplied known-layer component $F$ must satisfy $F\text{⊆}D_{1}\text{,}$ and every supplied uncertain component $E$ must satisfy $E\text{⊆}D\text{.}$ For every $s\text{∈}W$ and candidate $\theta\text{,}$ the certificate supplies either a path to such a qualifying uncertain $\theta$ component, or a path to a revealing exit into $K\text{.}$ Internal path steps use pairs in $D$ and receipts positive under both $P_{\theta}$ and $P_{0}\text{.}$ A revealing final step also uses a pair in $D\text{,}$ has positive $P_{\theta}$ probability and has zero $P_{0}$ probability. The exit alternative is possible only for candidate 1.

These paths prove positive reachability. They do not grant control over stochastic receipts. Safety requires all-positive-successor closure independently of the chosen paths. Simple paths of length at most $\text{|}S\text{|}\text{−}1$ suffice before an endpoint; the revealing edge, when present, is recorded separately. Finite subset encodings and bounded simple paths make the certificate relation finite and decidable. A policy-success proof or semantic winning predicate is not a certificate field.

**Theorem 2. Complete finite characterisation.** For the rational input and operational contract of Section 2, the following statements are equivalent:

1.  A lawful measurable private-seed policy wins almost surely against every legal one-change adversary.
2.  A positive finite certificate satisfying this section exists.
3.  The deterministic effective history policy compiled from some such certificate wins against every legal one-change adversary.
4.  The initial state belongs to the greatest uncertain region computed in Section 9.

There is a terminating signed decision procedure: on a positive input it returns a certificate and winning program; on a negative input it returns finite descending-region evidence excluding every admitted policy. Section 10 gives a polynomial decision construction for explicitly encoded rational input.

The rest of the proof has two distinct tasks. Necessity must recover finite evidence from an arbitrary measurable winner, including the cross-mode priority obligation. Sufficiency must show that a literal history program can navigate and learn despite a finite contaminated prefix and arbitrarily long gaps between samples of a row.

# 5 Adaptive sampling and the stale data bound

## A row tape construction of the actual law

Fix a deterministic change index $n\text{.}$ Draw the controller seed, $n$ independent uniforms for the prechange receipts, and an independent infinite receipt tape for every pair $e\text{.}$ Each postchange tape cell has distribution $P_{1}\text{(}e\text{,}\text{⋅}\text{)}\text{.}$ At and after round $n\text{,}$ selecting pair $e$ consumes exactly its next unused tape cell. The tape family and prefix uniforms are independent of the private seed.

This construction has the required adaptive law. For a fixed finite public history $h$ of length $T\text{,}$ let $C_{h}$ be the measurable set of seeds selecting its recorded actions. The history fixes every selected tape index. Its receipt constraints use distinct tape coordinates and distinct prefix uniforms. For every measurable seed set $D\text{,}$ therefore,

$$\text{Pr}\text{(}r\text{∈}D\text{,}H_{T}\text{=}h\text{)}\text{=}\nu\text{(}D\text{∩}C_{h}\text{)}\prod_{t\text{<}\text{min}\text{(}n\text{,}T\text{)}}^{}P_{0}\text{(}e_{t}\text{,}x_{t\text{+}1}\text{)}\prod_{n\text{≤}t\text{<}T}^{}P_{1}\text{(}e_{t}\text{,}x_{t\text{+}1}\text{)}\text{.}$$

These finite-cylinder probabilities identify the entire joint seed and run law. In particular, no independence between a random acquired sample count and its tape has been assumed. The count may depend on the values already read. No change is handled by tapes distributed according to $P_{0}$ and an empty contaminated prefix.

## Simultaneous regularity

For one tape and receipt, put $X_{k}\text{=}\text{𝟏}\text{\{}Y_{e\text{,}k}\text{=}y\text{\}}\text{,}$ $p\text{=}P\text{(}e\text{,}y\text{)}\text{,}$ and $S_{m}\text{=}\sum_{k\text{<}m}^{}{\text{(}X_{k}\text{−}p\text{)}}\text{,}$ where $P$ is the final row family. Independence gives $\text{𝔼}S_{m}^{2}\text{≤}m\text{/}4\text{.}$ For $j\text{≥}1\text{,}$

$$\text{Pr}\text{(}\text{|}S_{j^{2}}\text{|}\text{≥}\varepsilon j^{2}\text{)}\text{≤}\frac{1}{4\varepsilon^{2}j^{2}}\text{.}$$

The sum is finite, so the probability of infinitely many such deviations is zero: bound that event by every tail union and let its summable tail bound tend to zero. Applying this to positive reciprocal-integer tolerances proves $S_{j^{2}}\text{/}j^{2}\text{→}0\text{.}$ Between consecutive squares, bounded increments give

$$\frac{\text{|}S_{m}\text{|}}{m}\text{≤}\frac{\text{|}S_{j^{2}}\text{|}}{j^{2}}\text{+}\frac{2j\text{+}1}{j^{2}}\text{,}\quad\quad j^{2}\text{≤}m\text{<}{\text{(}j\text{+}1\text{)}}^{2}\text{.}$$

Thus the complete tape averages converge. Intersecting finitely many pair and receipt events yields simultaneous convergence for every row coordinate. Every tape cell also lies in its row’s positive support almost surely, by a countable union of zero-probability exceptions. On this single regularity event, every positive-probability symbol occurs infinitely often on its tape.

Let $N_{e}\text{(}t\text{)}$ count all uses of $e$ before round $t\text{,}$ and let $N_{e\text{,}y}\text{(}t\text{)}$ count those followed by $y\text{.}$ Define the prefix counts $b_{e}\text{=}N_{e}\text{(}n\text{)}\text{,}$ $b_{e\text{,}y}\text{=}N_{e\text{,}y}\text{(}n\text{)}\text{,}$ and the postchange count $J_{e}\text{(}t\text{)}\text{.}$ For $t\text{≥}n\text{,}$ sequential consumption gives the pathwise identities

$$N_{e}\text{(}t\text{)}\text{=}b_{e}\text{+}J_{e}\text{(}t\text{)}\text{,}\quad\quad N_{e\text{,}y}\text{(}t\text{)}\text{=}b_{e\text{,}y}\text{+}\sum_{k\text{<}J_{e}\text{(}t\text{)}}^{}\text{𝟏}\text{\{}Y_{e\text{,}k}\text{=}y\text{\}}\text{.}$$

Here $0\text{≤}b_{e\text{,}y}\text{≤}b_{e}\text{≤}n\text{.}$ If a pair is used infinitely often, its postchange count tends to infinity and its empirical row converges to the final actual row. This is a pathwise implication on the regularity event; we do not condition the law on which pairs will recur.

**Lemma 3. Uniform strict-gate bound.** Fix $\delta\text{>}0\text{.}$ On the regularity event there is a finite integer $k_{\text{*}}$ such that, at every testing time $t\text{,}$ for every phase index $r\text{≥}k_{\text{*}}\text{,}$ every pair satisfying $N_{e}\text{(}t\text{)}\text{>}r\text{,}$ and every receipt $y\text{,}$

$$\text{|}\frac{N_{e\text{,}y}\text{(}t\text{)}}{N_{e}\text{(}t\text{)}}\text{−}P\text{(}e\text{,}y\text{)}\text{|}\text{<}\delta\text{.}$$

**Proof.** Simultaneous complete-tape convergence supplies an integer $L\text{≥}1$ after which every tape average is within $\delta\text{/}2$ of its row. Choose $k_{\text{*}}\text{≥}n\text{+}L$ with $k_{\text{*}}\text{>}2n\text{/}\delta\text{.}$ A gated count $c\text{=}N_{e}\text{(}t\text{)}\text{>}r\text{≥}k_{\text{*}}$ cannot occur before the change. Its postchange count is $j\text{=}c\text{−}b_{e}\text{>}k_{\text{*}}\text{−}n\text{≥}L\text{.}$ The exact contamination identity yields

$$\text{|}\frac{N_{e\text{,}y}\text{(}t\text{)}}{c}\text{−}p\text{|}\text{≤}\frac{\text{|}b_{e\text{,}y}\text{−}b_{e}p\text{|}}{c}\text{+}\frac{j}{c}\text{|}\frac{1}{j}\sum_{k\text{<}j}^{}\text{𝟏}\text{\{}Y_{e\text{,}k}\text{=}y\text{\}}\text{−}p\text{|}\text{<}\frac{n}{c}\text{+}\frac{\delta}{2}\text{<}\delta\text{.}$$

The bound is uniform over testing times and over all sequential tape-consuming policies on the given tapes. A starved row cannot be an exception: if its old count still clears the sufficiently large gate, the same arithmetic forces enough postchange samples; otherwise it is excluded from the test. The controller need not know $L$ or $k_{\text{*}}\text{.}$

If a candidate row $Q\text{(}e\text{,}\text{⋅}\text{)}$ differs from the final row at a coordinate by more than $\delta\text{,}$ an infinitely used pair eventually rejects that candidate at every fixed phase: its empirical row converges, and its count eventually clears the fixed gate. Positive-successor recurrence also follows directly: an infinitely used pair consumes its entire tape, so every positive successor follows it infinitely often.

## The recurrent component of an arbitrary run

On the regularity event, let $E$ be the pairs appearing infinitely often. Finiteness makes $E$ nonempty and ensures that after a finite time no pair outside $E$ is used. Positive-successor recurrence makes $E$ closed under every positive successor of the final kernel: such a successor state recurs, and one of its finitely many departing actions must recur.

For two used states, choose a sufficiently late occurrence of the first and a later occurrence of the second. The intervening segment uses only $E$ and positive final-kernel transitions. It gives a directed path between them. Thus $E$ is strongly connected and is an end component. On a never-revealing run it has no positive final-kernel successor with zero $P_{0}$ probability, since recurrence would force such a receipt to occur.

The priorities recurring infinitely often are exactly the final-mode priorities of pairs in $E\text{.}$ One inclusion is immediate; for the other, an infinitely recurring priority must come from an infinitely recurring pair because the pair carrier is finite. The realised parity minimum is therefore $\text{min}_{e\text{∈}E}d_{\sigma}\text{(}e\text{)}\text{,}$ where $\sigma$ is the final mode.

# 6 Positive prefixes and equality of confined tails

## The residual private seed

The necessity proof must preserve the private information carried by an arbitrary policy. Fix a finite history $h\text{=}\text{(}x_{0}\text{,}a_{0}\text{,}\text{…}\text{,}a_{n\text{−}1}\text{,}x_{n}\text{)}\text{,}$ and define

$$C_{h}\text{=}\text{\{}r\text{:}\pi\text{(}r\text{,}h_{t}\text{)}\text{=}a_{t}\text{ for every }t\text{<}n\text{\}}\text{,}\quad\quad L_{P}\text{(}h\text{)}\text{=}\prod_{t\text{<}n}^{}P_{t}\text{(}e_{t}\text{,}x_{t\text{+}1}\text{)}\text{.}$$

For any deterministic prefix schedule $\text{(}P_{t}\text{)}\text{,}$ finite-cylinder factorisation gives

$$\text{Pr}\text{(}r\text{∈}D\text{,}H_{n}\text{=}h\text{)}\text{=}\nu\text{(}D\text{∩}C_{h}\text{)}L_{P}\text{(}h\text{)}\text{.}$$

If the prefix probability is positive, then $\nu\text{(}C_{h}\text{)}\text{>}0$ and $L_{P}\text{(}h\text{)}\text{>}0\text{.}$ Its conditional seed measure is the ordinary positive-event restriction

$$\eta_{h}\text{(}D\text{)}\text{=}\frac{\nu\text{(}D\text{∩}C_{h}\text{)}}{\nu\text{(}C_{h}\text{)}}\text{.}$$

The likelihood cancels. Thus the same positive public history has the same residual seed measure under every schedule assigning it positive likelihood. No disintegration theorem for arbitrary seed spaces is required. The unused uniform coordinates remain independent with their original product law, as one verifies first on finite future cylinders and then extends by uniqueness of measures.

Let $\pi_{h}\text{(}r\text{,}g\text{)}\text{=}\pi\text{(}r\text{,}h\text{⊙}g\text{)}\text{,}$ where concatenation identifies the shared boundary state. This retains the old history and private memory. The residual measure is used only in an existence proof; it need not be effectively samplable by the eventual certificate compiler.

## Killing before an unsupported action

Fix a nonempty pair set $E\text{,}$ a starting state, a policy $\psi$ and a seed measure $\eta\text{.}$ Record pairs and receipts until the policy first selects a pair outside $E\text{.}$ Kill immediately before that action and emit a cemetery symbol thereafter. The killed record takes values in the countable product of the finite alphabet $\text{(}E\text{×}S\text{)}\text{⊔}\text{\{}\text{†}\text{\}}\text{.}$

**Lemma 4. Equality of killed laws.** If two row families $P\text{,}Q$ agree on every complete row of $E\text{,}$ their killed-record laws for the same start, policy and seed measure agree on the whole product sigma-algebra.

**Proof.** Couple the constructions using the same seed and uniforms, and choose inverse cumulative distribution samplers that agree pointwise for equal rows. At a shared live history the same policy chooses the same action. If its pair is outside $E\text{,}$ both records die immediately. Otherwise the matching row produces the same receipt, so the histories remain equal. Induction identifies the entire killed record pointwise. Equal measurable maps have equal pushforward measures. This proves equality for infinite events, not merely equality of individual finite-transition probabilities.

The event that no cemetery symbol occurs and every pair in $E$ appears infinitely often is measurable. It is a countable intersection of countable unions of coordinate events. Its inverse image is exactly the event that the whole tail stays in $E$ and has $E$ as its exact recurring pair set.

For a complete ordinary run, write $T_{E}\text{(}n\text{)}$ for that event beginning at index $n\text{.}$ Since there are finitely many pairs,

$$\text{\{}\text{InfPairs}\text{=}E\text{\}}\text{=}\underset{n\text{≥}0}{\text{⋃}}T_{E}\text{(}n\text{)}\text{.}$$

A positive-probability recurring-set event therefore has a deterministic confinement index $n$ with positive probability. At that index, one of the finitely many public prefixes $h$ also has positive joint probability. The random last use of a pair outside $E$ need not be a stopping time; no restart at that random time is used.

## Finite prefix substitution

Consider two schedules with arbitrary deterministic prefixes of length $n\text{,}$ followed by stationary tails $P$ and $Q\text{.}$ Assume $h$ is positive under both prefixes and the tail rows agree throughout $E\text{.}$ Lemma 4 identifies a common killed tail law $k_{h}$ for the residual policy and seed measure. For every measurable killed-tail event $G\text{,}$

$$\underset{P}{\text{Pr}}\text{(}H_{n}\text{=}h\text{,}\: K_{E}\text{∈}G\text{)}\text{=}\nu\text{(}C_{h}\text{)}L_{P}\text{(}h\text{)}k_{h}\text{(}G\text{)}\text{,}$$

$$\underset{Q}{\text{Pr}}\text{(}H_{n}\text{=}h\text{,}\: K_{E}\text{∈}G\text{)}\text{=}\nu\text{(}C_{h}\text{)}L_{Q}\text{(}h\text{)}k_{h}\text{(}G\text{)}\text{.}$$

Hence the probabilities differ by the strictly positive finite factor $L_{Q}\text{(}h\text{)}\text{/}L_{P}\text{(}h\text{)}\text{.}$ This transfers positivity of the exact recurring-$E$ event. It does not assert absolute continuity of unrestricted infinite laws or a stationary law conditional on future confinement.

**Lemma 5. Cross-mode parity transport.** Suppose a policy wins under every finite fixed-index law and under no change. A positive-probability never-revealing recurrent component selected under candidate $\theta$ has even priority minimum for every rival whose full rows agree on that component.

**Proof for candidate 0.** Select a deterministic index $n$ and prefix $h$ with positive no-change probability jointly with $T_{E}\text{(}n\text{)}\text{.}$ Compare no change with a change at $n\text{.}$ Both use $P_{0}$ on the entire prefix, and their tail rows agree on $E\text{.}$ The selected event has exactly the same positive probability under the changed law. Its recurring priorities are now $d_{1}\text{(}E\text{)}\text{;}$ an odd minimum would contradict winning. The prefix need not have positive probability under fixed mode 1. That is precisely why the late-change comparison is needed.

**Proof for candidate 1.** Start with immediate change and select a positive prefix and confinement event inside the never-revealing event. Every prefix transition is then $P_{0}$-positive as well as $P_{1}$-positive. After selecting it, drop the never-revealing restriction, preserving positivity. Substitute the mode-0 prefix and tail. The exact confined-tail event retains positive probability by the likelihood ratio formula. An odd mode-0 minimum would contradict no-change winning. Here never revelation is used to justify a positive finite prefix, not to postulate a stationary law conditioned on an infinite future event. The candidate’s own even minimum follows directly from winning.

# 7 Necessity of the finite certificate

Suppose a lawful measurable private-seed winner exists from $s_{0}\text{.}$ Let $K$ be the physical states from which some mode-1 policy wins almost surely under the common menus. Let $W$ be the states from which some one-change policy wins almost surely beginning in mode 0. These semantic sets are tools of this proof, not queries made by the finite checker.

At a positive mode-0-compatible public history of a winning policy, its residual policy is one-change winning from the current state. Otherwise choose a legal continuation adversary with positive conditional failure and splice it after that exact history, retaining mode 0 beforehand. The positive probability of reaching the history would give positive total failure. Positive-event seed restriction from Section 6 makes this argument valid with arbitrary private seeds.

Apply the same reasoning after a positively selected action. Every $P_{0}$-positive successor must belong to $W\text{.}$ If a $P_{1}$-positive successor has zero $P_{0}$ probability, change after that action; its positive-probability residual must be mode-1 winning, so the successor belongs to $K\text{.}$ The action-before-change convention is important here. Moreover, an immediate-mode-1 history that remains mode-0 compatible is also a positive no-change history with the same residual seed measure. Thus the same safety conclusions hold along it until revelation.

Take $D$ to contain all lawful pairs satisfying these uncertain safety clauses, and $D_{1}$ all lawful mode-1-safe pairs with source in $K\text{.}$ There are only countably many finite histories, so their zero-probability exceptions can be removed together. Adding safe actions does not invalidate a certificate; sufficiency will show why fair navigation through the resulting larger action set still succeeds.

Fix $s\text{∈}W\text{,}$ choose one winning policy there, and examine candidate $\theta\text{=}0$ under no change or candidate $\theta\text{=}1$ under immediate change. Before revelation its positively used pairs lie in $D\text{.}$ If revelation has positive probability, it occurs at some finite time along a positive finite history. The internal part of that history uses candidate-positive, mode-0-positive transitions; its final revealing edge enters $K\text{.}$ Deleting cycles supplies the required finite route.

If revelation has probability zero, intersect the never-revealing event with the probability-one regularity and winning events. Its exact recurrent pair set is a nonempty end component by Section 5. There are finitely many possible pair subsets, so some such $E$ occurs with positive probability. It is contained in $D\text{,}$ is candidate-closed and strongly connected, and has no candidate-positive revealing edge. A positive finite prefix reaches one of its used states; deleting cycles gives an internal path. Its candidate priority minimum is even, and Lemma 5 proves the rival clause whenever its antecedent holds. Thus it is a qualifying uncertain component.

The same fixed-mode recurrent-set argument gives the known-layer clauses. From each state in $K\text{,}$ take a mode-1 winner. Every positively used action is safe for $K\text{,}$ by the residual argument. Some good recurrent mode-1 component is reached along a positive finite safe path. Select one finite component and path witness for each required state. Finiteness of the state set makes all the selected evidence finite.

We have constructed all fields of a positive certificate and have $s_{0}\text{∈}W\text{.}$ The proof neither assumes a finite-memory original winner nor asks the checker to decide a semantic winning predicate. It is the necessity implication of Theorem 2.

# 8 The deterministic controller and sufficiency

## The literal controller

Fix a positive certificate and fixed orders on its actions and components. In known mode 1, cycle through the $D_{1}$ actions available at the current state until reaching a supplied good component. Retain the first applicable component and thereafter cycle through its actions at each source. Use persistent state-departure counts modulo each current menu’s size. With a fixed menu, any infinite sequence of departures cycles fairly regardless of its initial counter offset.

In the uncertain layer keep a phase index $r\text{,}$ initially zero, with candidate $\theta\text{=}r\: \text{mod}\: 2\text{,}$ and either no component or one retained candidate component. Keep global state-departure, pair-use and pair-receipt counts from the whole observed history. Do not reset them at a phase boundary.

Before an action, if no component is retained, select the first supplied candidate component containing the current state, when one exists. Cycle through its actions if retained; otherwise cycle through $D$ at the current state. Define $\delta$ as half the least positive coordinate difference between the two row families, or set $\delta\text{=}1$ when every row agrees. After the new receipt and count update, reject the candidate precisely when

$$\text{∃}e\text{,}y\quad\quad N_{e}\text{>}r\quad \text{and}\quad \text{|}\frac{N_{e\text{,}y}}{N_{e}}\text{−}P_{\theta}\text{(}e\text{,}y\text{)}\text{|}\text{≥}\delta\text{.}$$

First give revelation precedence: a $P_{0}$-zero receipt enters known mode 1 immediately. Otherwise, if the candidate is rejected or the receipt leaves the retained component’s used states, increment $r$ by exactly one and clear the component. If both occur, increment only once. If neither occurs, retain the phase and component. Select any new component before the next action.

Every step consists of finite scans, integer counter operations and exact rational comparisons. The strict count gate prevents division by zero. A fixed lawful fallback completes the program on inconsistent histories. The program never receives the actual mode, an adversarial change time, a posterior distribution or a convergence oracle.

## Safety and the known layer

All selected actions are lawful. In the uncertain layer, every mode-0-compatible possible receipt remains in $W\text{.}$ A revealing possible receipt belongs to $K\text{,}$ and actual mode 1 is then permanent. Known-layer support closure preserves $K\text{,}$ and a retained good component is closed under the actual mode-1 kernel.

Known-layer navigation reaches a supplied component almost surely. Otherwise, on the regularity event, let $C$ be its nonempty recurrent state set. Fair cycling uses every $D_{1}$ action at each source of $C$ infinitely often. Positive-successor recurrence makes $C$ closed under every corresponding positive edge. A checked finite path from any state in $C$ to a target remains in $C\text{;}$ its target recurs and would trigger retention, a contradiction. Once a good component is retained, the same recurrent closure and strong-connectivity argument forces every used state and every component pair to recur. Its even minimum is therefore the actual parity minimum.

## Phases stabilise despite contamination

Fix one deterministic change law or no change, and let $\sigma$ be its final mode. Work on the regularity event of Section 5. Lemma 3 supplies a phase cutoff beyond which every gated empirical coordinate is strictly within $\delta$ of its final true row, uniformly over testing times. Thus a sufficiently large true-candidate phase can never be rejected.

Suppose the uncertain layer persists and phase indices increase without bound. Since each increase is by one and candidates alternate, a true-candidate phase above the cutoff begins after the actual finite change. It begins with no retained old component. No statistical rejection is possible there. Every subsequently selected true-candidate component is closed under the actual row and has no revealing candidate edge; its operation cannot cause a component exit. Navigation without a retained component causes no exit increment. Revelation would end the uncertain layer. Hence the selected true phase cannot increase again, contradicting unbounded growth.

Therefore the controller either enters known mode 1 or eventually has a stable uncertain phase. The proof gives a finite random cutoff, not a known learning time. It covers transient pairs with frozen prechange data as well as recurrent pairs.

## A stable candidate need not name the actual mode

Let a final stable phase have candidate $\theta\text{.}$ Every infinitely used pair has full row equality between $P_{\theta}$ and the actual final kernel $P_{\sigma}\text{.}$ Otherwise some coordinate differs by at least $2\delta\text{;}$ empirical convergence and the fixed phase gate would eventually reject it.

If navigation continued forever, fair cycling would use every $D$ action at every recurrent source infinitely often. On those pairs numerical row equality transfers actual positive-successor recurrence into closure under candidate-positive edges. A checked candidate path from that recurrent set must reach a component entry or a revealing exit. The first endpoint is visited and triggers retention. At the second, the recurring action has an actual-positive revealing receipt, which must occur. Either contradicts permanent uncertain navigation. Hence a component $E$ is eventually retained.

Within that component, let $C\text{⊆}U\text{(}E\text{)}$ be the nonempty recurrent state set. Fair operation uses every $E$ action at each source in $C$ infinitely often. Its rows agree with the candidate, so $C$ is closed under candidate-positive edges. Strong connectivity forces $C\text{=}U\text{(}E\text{)}\text{:}$ a path from $C$ to a point outside it would have a first edge violating closure. Every pair of $E$ consequently recurs, and full row equality holds on all of $E\text{.}$ The certificate’s rival clause now gives an even $d_{\sigma}$ minimum.

This proves parity under each deterministic change law and under no change, for the same compiled policy. Lemma 1 gives success against every permitted adaptive randomised adversary. It proves sufficiency and the effective-policy implication in Theorem 2. Notice that the controller need not identify the hidden mode: a stable wrong candidate is allowed when its complete recurrent behaviour has the required actual parity.

# 9 Greatest regions and complete negative evidence

For a tentative known-layer region $X\text{⊆}S\text{,}$ let $D_{1}\text{(}X\text{)}$ consist of the lawful pairs with source in $X$ and every positive $P_{1}$ successor in $X\text{.}$ Let $F_{1}\text{(}X\text{)}$ contain those states in $X$ with a positive $D_{1}\text{(}X\text{)}$ path to a good mode-1 component contained in $D_{1}\text{(}X\text{)}\text{.}$ The component search can initially enumerate every pair subset.

The operator is monotone and contractive. Enlarging a region preserves old safe actions, qualifying components and paths, while $F_{1}\text{(}X\text{)}\text{⊆}X$ by definition. Starting with $K_{0}\text{=}S\text{,}$ iterate

$$K_{j\text{+}1}\text{=}F_{1}\text{(}K_{j}\text{)}\text{.}$$

There are at most $\text{|}S\text{|}$ strict decreases. At the terminal equality, write the fixed region as $K^{\text{*}}\text{.}$ The necessity and sufficiency arguments for the known layer identify it with the semantic known-mode-1 winning region.

Now fix $K^{\text{*}}\text{.}$ For $X\text{⊆}S\text{,}$ let $D\text{(}X\text{,}K^{\text{*}}\text{)}$ be all lawful pairs with source in $X\text{,}$ all positive $P_{0}$ successors in $X\text{,}$ and all $P_{1}$-positive, $P_{0}$-zero successors in $K^{\text{*}}\text{.}$ Let $F\text{(}X\text{)}$ consist of the states in $X$ satisfying both candidate progress obligations using this pair set and all its qualifying uncertain components. Again $F$ is monotone and contractive. Iterate

$$W_{0}\text{=}S\text{,}\quad\quad W_{j\text{+}1}\text{=}F\text{(}W_{j}\text{)}\text{,}$$

and let $W^{\text{*}}$ be the terminal fixed region. It carries its own finite paths and component witnesses.

To establish greatestness, take any submitted positive certificate $\text{(}K_{c}\text{,}W_{c}\text{)}\text{.}$ Its known-layer witnesses imply $K_{c}\text{⊆}F_{1}\text{(}K_{c}\text{)}\text{.}$ Monotonicity places $K_{c}$ in every descending iterate, hence in $K^{\text{*}}\text{.}$ Enlarging its recovery region to $K^{\text{*}}$ preserves every uncertain witness. Thus $W_{c}\text{⊆}F\text{(}W_{c}\text{)}\text{,}$ and induction places $W_{c}$ in every uncertain iterate and in $W^{\text{*}}\text{.}$ Conversely, the terminal regions supply a certificate whenever $s_{0}\text{∈}W^{\text{*}}\text{.}$ This proves the final equivalence of Theorem 2.

A negative certificate records the two entire descending traces, beginning at $S\text{,}$ with each update recomputed and the final equality and exclusion $s_{0}\text{∉}W^{\text{*}}$ checked. It excludes all positive certificates and hence all measurable winners. Merely presenting a fixed point that excludes the initial state is insufficient: a smaller fixed point need not be greatest. The full trace is what proves exclusion from the greatest region.

# 10 Polynomial decision and exact complexity

## Separating the two component cases

Define the full-row-equality mask

$$R_{\text{eq}}\text{=}\text{\{}e\text{∈}B\text{:}\text{∀}y\text{∈}S\quad P_{0}\text{(}e\text{,}y\text{)}\text{=}P_{1}\text{(}e\text{,}y\text{)}\text{\}}\text{.}$$

For candidate $\theta\text{,}$ first remove from $D$ every pair with a candidate-positive, mode-0-zero successor, obtaining $D_{\theta}\text{.}$ An end component inside $D_{\theta}$ qualifies exactly in one of two cases: it contains a pair outside $R_{\text{eq}}$ and has even candidate minimum; or it is contained in $R_{\text{eq}}$ and has even minima for both priority maps. This exact two-mode case split preserves numerical equality rather than replacing it with support equality.

## Maximal end components by graph decomposition

Given an allowed pair set $B\text{′}$ and a candidate kernel, process a state set $U$ by retaining all pairs of $B\text{′}$ with source in $U$ whose every positive successor lies in $U\text{.}$ Form the graph of all their positive edges and compute its strongly connected components. If the whole graph is strongly connected and each state has a retained action, return all the retained pairs as one end component. Discard a singleton with no retained action. Otherwise recursively process each graph component, using the original allowed pair set and the smaller source set.

Every nonterminal call splits its state set into at least two proper nonempty subsets. A strongly connected graph with more than one state has an outgoing edge at each state, so the no-action exception cannot produce a hidden unary recursion. With $n\text{=}\text{|}S\text{|}\text{,}$ the recursion tree has at most $n$ leaves and $2n\text{−}1$ nodes.

Every original end component survives filtering and lies wholly in one graph component, because its own positive-edge graph is strongly connected. Follow that child recursively. It cannot be discarded at a no-action singleton, since it supplies an action there, so it is contained in a returned component. Returned source sets are disjoint. This coverage and disjointness prove maximality. Filtering always retains or deletes whole actions; it never deletes adverse outcomes from a retained action.

## Thresholds preserve the exact target union

For every even priority value $v$ present in the candidate array, restrict $D_{\theta}$ to pairs with $d_{\theta}\text{≥}v\text{,}$ compute its maximal end components, and retain a component if it contains a pair of priority exactly $v$ and a pair outside $R_{\text{eq}}\text{.}$ Each retained component qualifies. Conversely, a qualifying distinguishing component has an even minimum $v\text{,}$ lies in this restriction and is contained in one of its maximal components. Its minimum witness and distinguishing pair survive, so that maximal component is retained.

For the all-equal case, enumerate pairs of attained even values $\text{(}v_{0}\text{,}v_{1}\text{)}\text{,}$ restrict to

$$\text{\{}e\text{∈}D_{\theta}\text{∩}R_{\text{eq}}\text{:}d_{0}\text{(}e\text{)}\text{≥}v_{0}\text{ and }d_{1}\text{(}e\text{)}\text{≥}v_{1}\text{\}}\text{,}$$

and retain maximal components attaining both thresholds. Any qualifying all-equal component lies in the restriction for its two minima. A maximal component containing it cannot lower either minimum, and the old minimum witnesses remain. It therefore qualifies and is retained. The two witnesses may be different actions.

These constructions produce exactly the union of source states of all qualifying components. Their component lists need not be identical to an exhaustive list; equality of the target source union is the needed fact. It preserves every positive progress predicate and every region iterate. Known-layer targets use the simpler single-priority threshold construction.

**Theorem 6. Polynomial rational-input decision.** The existence question in Theorem 2 is decidable in deterministic polynomial time in the explicit rational input length.

**Proof.** Let $m\text{=}\text{|}S\text{×}A\text{|}\text{.}$ Each candidate needs at most $m$ single thresholds and $m^{2}$ double thresholds, collected from values actually present rather than all integers up to the largest priority. One maximal-component call has at most $2n\text{−}1$ recursive nodes and polynomial graph work at each. The two region iterations have at most $n$ strict decreases and a terminal check. Reachability and witness extraction are finite graph searches. A loose bound of order $n^{3}m^{3}$ for dominant incidence work suffices under an ordinary explicit graph representation.

Exact rational sign and equality tests have polynomial bit complexity; binary priority comparison and parity testing do too. No simulation, inverse minimum positive probability or inverse statistical separation enters the decision stage. These facts prove a polynomial bound in the full explicit input bit length.

The same reasoning shows that existence depends only on the two positive-support graphs, the full-row-equality mask, menus and priorities. It does not follow that one controller can be calibrated from those data alone for general hidden mode-owned priorities; Section 12 gives the counterexample. Polynomial offline decision also gives no polynomial online learning time or finite-memory bound.

## A self contained lower bound

For a conventional decision language, reject malformed encodings and inputs failing the finite stochastic-input conditions. Validating finite carriers, nonempty menus, rational nonnegativity and normalised rows is polynomial in the explicit encoding length. The reduction below always produces valid inputs.

**Theorem 7. Exact rational-input complexity.** The existence language of Theorem 2 is P-complete under deterministic logarithmic-space many-one reductions. Hardness already holds with identical kernels, a common state-based priority map taking values 0 and 1, two actions lawful everywhere, and row entries in $\text{\{}0\text{,}1\text{/}2\text{,}1\text{\}}\text{.}$

**Proof.** Theorem 6 gives membership in P. For hardness, fix any language $L$ decided by a deterministic polynomial-time Turing machine. We construct, in logarithmic workspace, an acyclic monotone circuit evaluating its computation, then a stochastic instance whose almost-sure value is one exactly when that circuit is true. The details below make the simulation and all-policy bound explicit.

Take a deterministic one-tape machine with a two-way tape, finite tape alphabet $\Gamma$ and finite control states $Q\text{.}$ One may use this machine model to define P; a fixed multitape machine also has a polynomial one-tape simulation by representing its fixed number of tapes on marked tracks and sweeping their polynomially bounded used interval to read and update the marked positions. The overhead changes the time polynomial only. Choose a fixed integer bound $T\text{=}c{\text{(}n\text{+}1\text{)}}^{k}$ at least $n\text{+}1\text{,}$ where $n$ is the input length, that bounds the running time. Make every halting state persistent by a stationary move leaving its symbol and control state unchanged.

Let $\Lambda$ be the finite alphabet of unheaded tape symbols $\gamma$ and headed symbols $\text{(}\gamma\text{,}q\text{)}\text{.}$ In a valid one-head configuration, the next label of a cell is determined by its current label and its two neighbours. A headed centre writes the prescribed new symbol and keeps the head only for a stationary move. An unheaded centre receives the new head if a neighbour moves into it, keeping its own old symbol. Otherwise it stays unheaded with its old symbol. These cases define a local function $f\text{:}\Lambda^{3}\text{→}\Lambda$ on valid triples; give contradictory multiple-head triples arbitrary values to make it total.

Place the input in cells 0 through $n\text{−}1$ and the initial head at 0, using a blank there for the empty input. Represent the window

$$J\text{=}\text{\{}\text{−}T\text{−}2\text{,}\text{…}\text{,}n\text{+}T\text{+}2\text{\}}\text{.}$$

Through time $T\text{,}$ the head remains between $\text{−}T$ and $T\text{.}$ Cells outside the initial input and visited head positions stay blank and unheaded. A boundary formula asking for a neighbour just outside $J$ therefore uses the constant one-hot representation of that blank unheaded label. These explicit ghost cells close every local formula and reproduce the infinite-tape run on $J\text{.}$

For every represented time, cell and label, introduce an indicator $X_{t\text{,}j\text{,}b}\text{.}$ The initial indicators are constants fixed by the input. Define the later indicators by the monotone formula

$$X_{t\text{+}1\text{,}j\text{,}b}\text{=}\underset{f\text{(}a\text{,}c\text{,}d\text{)}\text{=}b}{\text{⋁}}\text{(}X_{t\text{,}j\text{−}1\text{,}a}\text{∧}X_{t\text{,}j\text{,}c}\text{∧}X_{t\text{,}j\text{+}1\text{,}d}\text{)}\text{.}$$

Exactly one triple conjunction is true when the previous neighbouring labels are one-hot. It produces exactly the label specified by $f\text{.}$ Induction proves both the one-hot invariant and fidelity to the machine’s actual run. The finite alphabet and update function are fixed for the machine, so each formula expands to a constant-size binary AND/OR gadget; an empty disjunction is false. At time $T\text{,}$ a binary OR chain over all accepting headed labels is true precisely when the machine accepts. There are order $T\text{(}n\text{+}T\text{)}$ gates, up to machine-dependent constants.

For explicit logarithmic-space generation, number two shared constant gates first, then all time-zero indicators, then the local gadgets in lexicographic time and cell order. Use a fixed template with a constant number of slots per cell block and fixed output-label offsets. Two binary AND gates realise each triple conjunction; a binary OR chain combines its terms. Padding, or a final OR with false, makes every output slot explicit. Internal wires point to earlier slots; input wires point to the previous layer or to ghost-cell constants. The numbering is topological.

Constantly many counters for time, shifted cell position, label and template slot need only $O\text{(}\text{log}\text{(}n\text{+}2\text{)}\text{)}$ work bits. All addresses use sums and products of polynomially bounded integers. Initial symbols are found by rescanning the read-only input with an index counter. Thus a transducer can recompute each gate’s type and child indices without storing any configuration, layer or circuit. The fixed machine and local template are part of that transducer, not part of the varying input.

Now make one observed stochastic state per gate, plus absorbing states $\text{𝖳}$ and $\text{𝖥}\text{;}$ start at the output gate. Both actions 0 and 1 are lawful everywhere. At an OR gate with children $u\text{,}v\text{,}$ action 0 leads deterministically to $u$ and action 1 to $v\text{.}$ At an AND gate, either action chooses the two children with probability one half each; if they coincide, combine the masses into probability one. A constant gate leads deterministically to its corresponding terminal. Both terminals self-loop. Use this same kernel for both modes. Give every pair priority 0 except pairs with source $\text{𝖥}\text{,}$ which have priority 1 in both modes.

Every nonterminal transition moves backwards in topological order, so every supported run reaches a terminal in finitely many steps. Parity is exactly the event of reaching $\text{𝖳}\text{.}$ Identical kernels and priorities make the change adversary irrelevant under the original action-before-change timing.

Define terminal values $V\text{(}\text{𝖳}\text{)}\text{=}1\text{,}$ $V\text{(}\text{𝖥}\text{)}\text{=}0\text{,}$ and, recursively,

$$V\text{(}\text{OR}\text{(}u\text{,}v\text{)}\text{)}\text{=}\text{max}\text{\{}V\text{(}u\text{)}\text{,}V\text{(}v\text{)}\text{\}}\text{,}\quad\quad V\text{(}\text{AND}\text{(}u\text{,}v\text{)}\text{)}\text{=}\frac{V\text{(}u\text{)}\text{+}V\text{(}v\text{)}}{2}\text{.}$$

These values bound every admitted policy. Fix any private seed and any history ending at a gate. Induct on remaining circuit depth. At an OR gate the resulting deterministic continuation chooses one child and is bounded by its value. At an AND gate the fresh transition averages the two induction bounds. Constants and terminals are immediate. The bound holds pointwise in the seed; integrating over an arbitrary measurable seed law preserves it without a conditional-distribution assumption. A deterministic memoryless policy selecting a maximum-value child at each OR gate attains the values. Shared subcircuits and duplicate children cause no difficulty.

The recursion implies that $V\text{(}g\text{)}\text{=}1$ exactly when gate $g$ has Boolean value true. A maximum equals one exactly when some child value is one; an average of numbers in $\text{[}0\text{,}1\text{]}$ equals one exactly when both are one. A false output therefore has an all-policy bound strictly below one, including for unbounded-memory randomised policies.

Finally, emit the explicit dense stochastic input directly by enumerating kernel, source, action and destination indices and recomputing the gate type and children. A polynomial gate count $G$ gives $G\text{+}2$ states and order ${\text{(}G\text{+}2\text{)}}^{2}$ constant-size entries. The same logarithmic counters suffice. Duplicate AND children are emitted as one unit entry, so every row is normalised. Menus, priority entries and the initial state are likewise logarithmic-space computable. We have constructed a valid instance $I_{x}$ with

$$x\text{∈}L\quad \text{⇔}\quad I_{x}\text{ admits an almost-sure one-change winner}\text{.}$$

This proves the claimed hardness for every $L\text{∈}\text{P}\text{,}$ and hence P-completeness.

The lower-bound construction uses acyclic gate behaviour before absorption. It does not treat stochastic choice as a sure adversarial AND operation on arbitrary cyclic graphs: for example, repeated coin flips between a self-loop and a target reach the target almost surely despite an infinite target-avoiding support path. P-completeness here is an ordinary exact complexity classification. It is not an optimal polynomial-degree claim, a numerical runtime lower bound or an unconditional parallel lower bound.

# 11 Real kernels and the boundary of representation

## Effective winners exist nonuniformly

The ordinary probability and component arguments use actual positivity, full-row equality, finite minima and empirical convergence. They do not require rational denominators. Thus the finite characterisation extends mathematically to any two real stochastic kernels on the same finite carriers.

**Theorem 8. Nonuniform real-kernel effectivity.** For each individual real-kernel instance, existence of a lawful measurable private-seed winner is equivalent to existence of a deterministic effective finite-history winner. This is not a uniform procedure that recovers a winner or an exact signed answer from arbitrary real-number names.

**Proof.** From a positive finite certificate, hard-code its finite data together with the exact support masks and equality mask. In particular, revelation uses the exact mode-0 support mask, never a zero test on numerical approximations. Suppose some coordinates differ, and let $\Delta\text{>}0$ be the smallest positive coordinate difference. Choose a positive rational $\tau$ and rational centres $q_{\theta}\text{(}e\text{,}y\text{)}$ satisfying

$$4\tau\text{<}\Delta\text{,}\quad\quad \text{|}q_{\theta}\text{(}e\text{,}y\text{)}\text{−}P_{\theta}\text{(}e\text{,}y\text{)}\text{|}\text{<}\tau\text{/}4\text{.}$$

Such finitely many rational values exist even if the original coefficients are noncomputable. They are nonuniform finite advice. The centres need not form stochastic rows; they are used only in comparisons, not to generate receipts or determine support.

Replace the empirical test’s centre by $q_{\theta}$ and its rejection threshold by $\tau\text{.}$ On sufficiently large gated samples, the true empirical row is within $\tau\text{/}2$ of the actual row, so its distance to the true centre is less than $3\tau\text{/}4\text{.}$ Hence large true phases cannot be rejected. For a recurrent wrong row, a distinguishing coordinate has distance from the wrong centre greater than $\Delta\text{−}\tau\text{/}4\text{>}15\tau\text{/}4\text{;}$ convergence forces eventual rejection at any fixed phase. The remainder of the proof uses the original exact support data and certificate and is unchanged.

If every row agrees across modes, no learner is needed. Fix candidate 0, fairly navigate to a qualifying component and cycle there. Both priority minima are even and both physical kernels agree. This special case has a finite-state policy. In the general case the program remains finite but may use unbounded counters. All its runtime operations are ordinary finite computations on integer, rational or finite discrete data. The converse is immediate because a deterministic effective policy is an admitted measurable policy.

## Exact decisions from Cauchy names are impossible

The representation qualification cannot be dropped. Consider two observed states and two actions, with Bernoulli receipts independent of source and action. Use priorities 2 for choosing the governing mode’s action and 1 for the other action. Winning then requires eventual exclusive use of the final mode’s action.

Fix $p_{0}\text{=}1\text{/}3\text{.}$ For a Turing machine $M\text{,}$ let $\varepsilon_{M}\text{=}0$ if it never halts, and let $\varepsilon_{M}\text{=}2^{\text{−}\text{(}T\text{+}3\text{)}}$ if its first halt is at step $T\text{.}$ Set $p_{1}\text{=}1\text{/}3\text{+}\varepsilon_{M}\text{.}$ This gives full support uniformly. A fast-Cauchy name for $\varepsilon_{M}$ is computable uniformly: at requested precision $2^{\text{−}k}\text{,}$ simulate $k$ steps; output the dyadic value if the halt has occurred, otherwise output zero. A later halt contributes at most $2^{\text{−}\text{(}k\text{+}4\text{)}}\text{.}$ Adding one third to this name gives a uniform name for $p_{1}\text{,}$ and taking complements supplies names for the remaining stochastic-row coordinates.

If the machine never halts, the two receipt laws agree, so the same observation and action law would have to choose action 0 eventually under no change and action 1 eventually under immediate change. That is impossible. If it halts, the positive gap permits a rational threshold strictly between the two Bernoulli parameters. Empirical means eventually choose the right final action for each deterministic change index, and Lemma 1 handles every legal adaptive adversary.

Therefore exact existence decision from arbitrary computable-real names would decide halting. No such total uniform algorithm exists. Every individual value in this reduction is rational; the obstruction remains under a promise of rational-valued rows when they are supplied only through Cauchy names. It is the absence of exact equality information in the representation, not irrationality itself. This does not conflict with polynomial decision from explicit rational fractions, with decision given trusted exact support and equality masks, or with per-instance nonuniform effective winners.

# 12 Common priorities permit uniform support only synthesis

## The stronger quantified theorem

Assume $d_{0}\text{=}d_{1}\text{=}d\text{.}$ Let the input provide exact nonempty support sets $H_{i}\text{(}e\text{)}\text{=}\text{\{}y\text{:}P_{i}\text{(}e\text{,}y\text{)}\text{>}0\text{\}}\text{,}$ menus, priorities and an initial state, but no numerical probabilities or equality mask. A compatible realisation is any pair of real stochastic kernels with exactly those supports.

**Theorem 9. Uniform support-only synthesis for common priorities.** There is a terminating effective procedure returning either finite negative evidence excluding a winner for every compatible realisation, or one positive certificate and one deterministic effective policy $\pi$ such that

$$\text{∀}\text{(}P_{0}\text{,}P_{1}\text{)}\text{ compatible}\quad \text{∀}\alpha\text{ legal}\quad\quad \underset{P_{0}\text{,}P_{1}}{\overset{\pi\text{,}\alpha}{\text{Pr}}}\text{(}\text{𝖯𝖺𝗋}\text{)}\text{=}1\text{.}$$

The same program is fixed before the numerical realisation and adversary are chosen. Positivity for one realisation is equivalent to positivity for every realisation and to existence of the common finite certificate. The probability-one assertion is separate under each law; it does not assert a single probability-one event simultaneously across uncountably many laws.

With common priorities, component qualification simply requires a candidate end component with no candidate-positive revealing edge and even common minimum. The candidate’s own parity clause already implies every other parity clause. Every finite condition therefore uses only supports, menus and priorities. For an explicit decision route, use the uniform rational distribution on each supplied support and run the finite criterion. Any equalities introduced by those representative rows are irrelevant to the common-priority clause. Necessity for each real realisation follows from the same recurrent-component argument.

## A one sided empirical test

Use the same certificate navigation, retained components, counters, phase alternation, revelation precedence and component-exit rule. Replace the numerical row test by rejection when

$$N_{e}\text{>}r\text{,}\quad\quad y\text{∈}H_{\theta}\text{(}e\text{)}\text{,}\quad\quad \frac{N_{e\text{,}y}}{N_{e}}\text{<}\frac{1}{r\text{+}1}$$

for some pair and candidate-positive receipt. It is an exact integer comparison $\text{(}r\text{+}1\text{)}N_{e\text{,}y}\text{<}N_{e}\text{.}$ Inspect every candidate-positive coordinate of every gated pair; leave candidate-zero coordinates untested. The program uses no numerical coefficient or supplied lower probability bound.

Fix an actual compatible realisation and final mode $\sigma\text{.}$ Its finitely many positive row entries have a positive minimum $p_{\text{*}}\text{,}$ used only in this proof. Lemma 3 with tolerance $p_{\text{*}}\text{/}2$ gives a phase cutoff beyond which every gated candidate-$\sigma$ positive coordinate has empirical frequency greater than $p_{\text{*}}\text{/}2\text{.}$ Increase the cutoff until $1\text{/}\text{(}r\text{+}1\text{)}\text{≤}p_{\text{*}}\text{/}2\text{.}$ Thus the true candidate cannot be rejected at any testing time above it. The previous phase argument again gives known-mode-1 entry or a stable uncertain phase. No value of $p_{\text{*}}$ is computed or passed to the policy.

In a stable phase of index $r_{\text{last}}\text{,}$ an infinitely sampled pair cannot have a candidate-positive, actual-zero receipt. Its empirical frequency would converge to zero, eventually fall below the positive threshold $1\text{/}\text{(}r_{\text{last}}\text{+}1\text{)}\text{,}$ and cause rejection. Hence on every recurrent pair,

$$H_{\theta}\text{(}e\text{)}\text{⊆}H_{\sigma}\text{(}e\text{)}\text{.}$$

This is only inclusion. Actual-positive, candidate-zero coordinates are intentionally untested, and neither equality of supports nor equality of rows has been proved.

Inclusion is enough. During permanent navigation, all actions at recurrent sources recur. Candidate-positive successors are actual-positive and hence recurrent, so the recurrent state set is candidate-closed. A supplied candidate path forces a component entry or revealing exit, a contradiction. Within a retained component, the same closure and candidate strong connectivity force every used state and pair to recur. Extra actual successors do not invalidate the argument: an exit would change the phase, and extra internal edges cannot destroy candidate reachability. The exact recurrent pair set is the retained component, whose common priority minimum is even.

Thus the one support-based program wins for each fixed-index law of each chosen realisation, then for every legal adversary by Lemma 1. Since the program was selected before the arbitrary realisation, this proves the theorem’s quantifier order. Trusted exact supports are an input assumption; no finite sample is claimed to recover them.

## General mode owned priorities need calibration

**Proposition 10. The general skeleton does not determine a common winning policy.** There are two positive rational instances with identical supports, full-row-equality mask, menus, priorities and initial state, for which no single measurable private-seed policy wins in both.

**Proof.** Take states and actions $\text{\{}0\text{,}1\text{\}}\text{,}$ both actions lawful, and initial state 0. Let receipts be Bernoulli with mode parameter $p_{i}\text{,}$ independent of source and action. Give action $i$ priority 2 in mode $i\text{,}$ and the other action priority 1. In instance A take $\text{(}p_{0}\text{,}p_{1}\text{)}\text{=}\text{(}1\text{/}3\text{,}2\text{/}3\text{)}\text{;}$ in instance B take $\text{(}p_{0}\text{,}p_{1}\text{)}\text{=}\text{(}2\text{/}3\text{,}1\text{/}3\text{)}\text{.}$ Both support masks are full and their within-instance equality masks are empty.

Each instance is positive: threshold the empirical mean of genuine receipts at one half, using the appropriate orientation of the action labels. The finite prechange prefix vanishes. But compare instance A with no change and instance B with immediate change. Both give the same Bernoulli-one-third observation law for any common policy and fixed seed distribution. The first requires eventual exclusive action 0; the second requires eventual exclusive action 1. These events are disjoint and cannot both have probability one under the identical law. Randomisation, including random selection of a program, is already included in the private seed and does not help.

Thus supports plus the equality mask determine existence, while numerical calibration may still be needed to choose a winning policy for general mode-owned priorities. The distinction is between a winner for each realisation and one winner shared by all realisations. The example even has a common positive lower bound of one third, so lack of such a bound is not the cause of failure.

# 13 Discriminating examples

## The minimal static and change separator

Take states $q\text{,}r\text{,}$ initial state $q\text{,}$ and one lawful action $a\text{.}$ Mode 0 alternates the states and mode 1 keeps the current state fixed:

$$P_{0}\text{(}q\text{,}a\text{,}r\text{)}\text{=}P_{0}\text{(}r\text{,}a\text{,}q\text{)}\text{=}1\text{,}\quad\quad P_{1}\text{(}q\text{,}a\text{,}q\text{)}\text{=}P_{1}\text{(}r\text{,}a\text{,}r\text{)}\text{=}1\text{.}$$

Use the common priority map $d\text{(}q\text{,}a\text{)}\text{=}0\text{,}$ $d\text{(}r\text{,}a\text{)}\text{=}1\text{.}$ The unique policy wins both fixed models from $q\text{:}$ alternating visits have recurring minimum 0, and immediate mode 1 stays at $q\text{.}$ A change at index 1 instead first moves to $r\text{,}$ then remains there forever with priority 1. No policy can repair this because there is only one action.

The certificate detects the failure. The known-mode-1 winning region is $\text{\{}q\text{\}}\text{.}$ An uncertain region containing $q$ must include its mode-0 successor $r\text{,}$ but at $r$ the only action has a mode-1-positive, mode-0-zero successor $r$ outside the known region. That action is unsafe, so uncertain progress fails.

Two observed states and one action are minimal for this existence gap. On one physical state, every stochastic row is the same deterministic self-loop, so a common policy generates the same seed-dependent action sequence under every schedule. If it wins both fixed modes, intersect their two probability-one seed events. On that intersection it satisfies both priority objectives, and a finite change only alters a finite prefix of the eventual mode-1 sequence. Lemma 1 then gives one-change winning. One state therefore cannot separate the existence predicates.

## A winner that requires unbounded memory

Take the unequal Bernoulli instance A of Proposition 10. The empirical-mean policy eventually chooses action 0 under no change and action 1 after each finite change. It is a deterministic effective winner.

Now restrict to a finite-memory time-homogeneous controller, allowing fixed randomised action and memory-update kernels. Count all persistent information in its finite memory; do not supply an unbounded clock or a stored arbitrary parameter for free. Under either fixed mode, the product of controller memory, observed state and selected action is a finite Markov chain. The two plant kernels have the same strictly positive supports. The product chains therefore have the same positive initial support, reachable vertices and reachable bottom strongly connected components.

Every reachable bottom component is entered with positive probability and, conditional on entry, every vertex in it recurs almost surely. No-change co-Büchi success requires every such vertex to select action 0. Immediate-change success requires those same nonempty components to select action 1. This is impossible. No finite-memory homogeneous randomised controller of any finite size wins the example.

This is the programme’s earlier hidden-standard Bernoulli memory separation embedded in the exact one-change contract. It does not establish a memory lower bound for the common-priority subclass. Its size is minimal for this particular memory separation: with one action memory cannot change the action sequence; with one physical state any winner has some recurring action set whose minima are even in both modes, and a finite periodic controller cycling that set wins.

## Numerical equality changes existence

In the unequal Bernoulli input, take $W\text{=}K\text{=}S$ and all lawful pairs as uncertain safe pairs. For candidate $i\text{,}$ use $E_{i}\text{=}\text{\{}\text{(}0\text{,}i\text{)}\text{,}\text{(}1\text{,}i\text{)}\text{\}}\text{.}$ It is candidate-closed and strongly connected, has own minimum 2 and no mode-0-zero receipt. Its rival rows differ, so the rival odd minimum does not disqualify it. Both states are already component entries. The known-layer component is $E_{1}\text{.}$

Replacing numerical row equality by support equality would wrongly reject this positive input. Every support is full, but no nonempty pair set has even minimum under both opposing co-Büchi maps. An action-0 pair makes the mode-1 minimum 1, and an action-1 pair makes the mode-0 minimum 1.

For a stronger representation control, replace the mode-1 Bernoulli parameter by one third as well. Supports, menus and priorities stay unchanged. The no-change and immediate-change observation and action laws are now identical, yet demand disjoint eventual actions. The input is negative. Thus supports alone cannot classify existence in the general mode-owned-priority class. The equality mask changes, which is consistent with Section 10.

## Why the strict count gate is necessary for this learner

Add a transient initial state $z$ to active states $u\text{,}v\text{,}$ with only action 0 lawful at $z$ and both actions lawful at active states. At $\text{(}z\text{,}0\text{)}\text{,}$ mode 0 sends to $u$ surely, while mode 1 sends to $u$ with probability two thirds and $v$ with probability one third. At active pairs, mode 0 has probabilities $\text{(}2\text{/}3\text{,}1\text{/}3\text{)}$ on $\text{(}u\text{,}v\text{)}\text{,}$ and mode 1 has $\text{(}1\text{/}3\text{,}2\text{/}3\text{)}\text{.}$ Complete the unused row for $\text{(}z\text{,}1\text{)}$ by copying the row for $\text{(}z\text{,}0\text{)}$ within each mode. Every unspecified transition probability is zero, so no transition returns to $z\text{.}$ Give both actions at $z$ priority 2 in both modes, and use the opposing co-Büchi action priorities at active states. Every positive coordinate difference is one third, so $\delta\text{=}1\text{/}6\text{.}$

This is a positive input: each candidate’s active action component works as in the Bernoulli example, and an empirical learner wins after leaving $z\text{.}$ Now change at index 1. The first receipt is $u$ surely. The transient pair has count 1 and an empirical row exactly equal to its old true mode-0 row, frozen forever.

Modify only the controller’s gate from $N_{e}\text{>}r$ to $N_{e}\text{>}0\text{.}$ Every true mode-1 phase is then rejected by the frozen transient coordinate, whose discrepancy is $\text{|}1\text{−}2\text{/}3\text{|}\text{=}1\text{/}3\text{>}1\text{/}6\text{.}$ The active receipts never reveal mode 1. Both candidate components contain both active states and select only their own action. Every odd phase therefore lasts at most one action, while either some even phase persists forever or infinitely many even phases occur. In either case action 0 occurs infinitely often under actual mode 1, so the weakened learner fails with probability one.

The original gate removes the obstruction exactly: every mode-1 phase has odd $r\text{≥}1\text{,}$ so the frozen count 1 fails $N_{e}\text{>}r\text{.}$ This example does not prove that every ungated algorithm fails or that forgetting schemes cannot work. It shows why the precise global-count and phase-gate construction proved here cannot be weakened in that natural way.

## Why thresholding must precede maximality

At one state, let two self-loop actions have priorities 2 and 1. The unrestricted maximal component contains both and has odd minimum, but the priority-2 action alone is good. The even threshold 2 finds it. For the equal-row two-priority case, use three self-loop actions with priority pairs $\text{(}2\text{,}3\text{)}\text{,}$ $\text{(}3\text{,}2\text{)}$ and $\text{(}1\text{,}1\text{)}\text{.}$ The first two together have even minima $\text{(}2\text{,}2\text{)}\text{,}$ while neither alone does. The double threshold $\text{(}2\text{,}2\text{)}$ excludes the spoiling third action and retains both necessary minimum witnesses.

# 14 Scope and programme ownership

The theorem concerns two finite stochastic models, one irreversible hidden change, lawful common nonempty menus, full physical-state observations, hidden governing-mode departure-pair priorities and minimum-infinitely-often parity. It does not automatically extend to repeatedly changing modes, a variable number of hidden modes, succinct exponentially large state descriptions, empty-menu deadlocks or an altered priority observation convention. Those changes require new statements and proofs.

The finite decision uses trusted exact input data. It does not discover real-world permissions, certify the correctness of an empirical support estimate or infer normative authority from a stochastic model. Exact-rational decision, per-instance effective control with real kernels, uniform support-only common-priority control and impossible uniform exact decision from Cauchy names are separate claims with different input and quantifier conditions.

Neither the finite certificate nor the polynomial decision bound supplies a bounded learning time, finite expected recovery cost or general finite-memory sufficiency. Almost-sure winning is not sure winning on every infinite support path. The controller may retain a candidate whose name is wrong but whose recurrent rows and objective behaviour suffice.

The earlier Ninth and Sixteenth programme results retain their fixed-hidden-model certificate and controller endpoints. Stationary row-tape convergence, private-seed cancellation, killed-law equality, empirical phase control and finite witness reification retain their earlier ownership. The hidden-standard result retains the Bernoulli finite-memory separation. The Eighteenth extension is the exact one-change law family, the persistent future-mode-1 safety obligation, the late deterministic change transport, the complete two-layer criterion and its specialised decision and synthesis consequences. It is not a relabelling of the earlier fixed-model theorem or of a reset theorem with a supplied public fault flag.

This companion supplies ordinary proofs. Formal coverage must be stated theorem by theorem, including any remaining assumptions and the exact operational law to which an endpoint is bound. The separately documented kernel and executable work should be read with that distinction intact. No claim of human specialist review or global priority over the literature is made here.
