# Predictive understanding: one faithful corrective-transfer test

11 October 2026 UTC. Bounded additive T20 application. Candidate research only; no protected edits, external contact, T21, programme closure, or independent validation of either authors' claims or the project.

## Result

**The strongest relevant argument already includes the qualitative safeguard.** No new missing-condition objection to Queloz–Beckmann was established. The useful operation is a finite implementation test: take the already-owned source/audit pair and ask whether a proposed demonstration protocol identifies the dependence needed for a subsequent correction. It does not if demonstrations measure only isolated marginals. A conditional probe or retention of the mixed target–audit quantity repairs this particular defect.

This is one source-specific operational application of inherited mathematics, not a new theorem, new counterexample, or general theory of understanding. It identifies exactly where the formal transfer stops: a conditional certificate inside a specified model does not establish that the model captures an actual person's understanding, that the demonstration genuinely reveals it, or that the person is a warranted guide.

## 1. Primary argument, read in context

[Queloz and Beckmann, v1](https://arxiv.org/html/2609.04962v1), §§2.1–2.2, pp.5–9, make trust and learning domain-relative. Their account requires a model preserving relevant relations across variation; the mechanic example includes effective intervention. They explicitly distinguish such organization from a good test record.

Section 3.2, pp.13–17, distinguishes a reusable model from encoded residual data. Its compression does not discard the latter. The future-data objective is approximated using past data, with acknowledged overfitting risk. Section 3.3, pp.18–19, separates constitution from fallible indicators, including explanation, hard cases, and counterfactual handling.

Section 4.1, pp.20–21, asks which structure and task family a compression captures; textual and worldly structure are not automatically interchangeable. Section 4.2 permits tacit understanding. The conclusion, p.23, explicitly denies that predictive success alone settles understanding. These qualifications block a score-only interpretation. They do not supply a finite instrument, an identified causal model, or a proof that actual demonstrations warrant the intended inference.

The source therefore motivates a task-sensitive test but does not itself specify the finite mapping below. Treating its qualitative condition as absent would manufacture a rival the authors reject. Equating its lossless two-part coding with selective moment retention would conflate different operations.

## 2. Exact inherited ownership

All three requested inputs were read at the relevant argument, copied into `inputs/`, and SHA-256 bound in `INPUT_BINDINGS.json`.

1. **H-Continuation**, `tensor-moment-continuation-20261009/H_CONTINUATION_SOURCE.md`, Theorem 2, its finite instrument setup, proof, and adjoining limits, already owns closure under action–observation pullbacks. Theorem 2(b) says that retained moments determine every declared branch probability and target numerator over every reference law exactly when they contain the required continuation space. Part (c) covers bounded adaptive policies; normalization is confined to positive-probability branches. The invariant-space construction, and the full-simplex continuous-coordinate lower bound, are inherited. The source credits predictive-state and invariant-observable ancestry. No generic sufficiency/fibre criterion is rebuilt here.

2. **Audit continuation**, `audit-continuation-transport-20261010/RESULT.md`, §§3–4, already owns the actual commuting audit realization, the equal-marginal pair, the missing target–audit numerator, the four-state moment update, and the distinction between rereading one observation and drawing a fresh verifier. §§5–6 own the weaker posterior-only comparison and its qualifications; those are not extended here. Its own credit to source-audit revision, triple interaction, H-ICS, and prior mathematical methods is retained. The new execution starts with its existing pair, rather than renaming that pair as a new example.

3. **Guide-domain report**, `guide-domain-warrant-test-20261011/REPORT.md`, already owns the specific comparison between success on a token, recognizable expertise through partly shared subject matter, and acquisition of unfamiliar teaching. It retains T19 A30–A31, the whole-*Nubuwwāt* appraisal, the affirmative sourcehood and attestation case, and the distinction between content unfamiliar to a recipient and content beyond warranted source competence. This operation rereads that report; it does not claim a fresh inspection of the Arabic primary pages or inherited whole works.

The prior parent search finding no Beckmann/Lampinen hit was a bounded top-level report search. It is not proof of corpus-wide priority. No additional corpus or philosophical-rival search was performed. No Lampinen paper was read or evaluated in this operation.

## 3. The one concrete operation

### Proposed demonstration-to-correction inference

Specify the tested object before interpreting success. A learner is given a reduced predictive state and expected to answer both present questions and a later corrective question. Does a demonstration protocol adequate for the present questions show that the supplied state can support the correction?

This is a test of a proposed representation and test protocol. It is not a definition of a person's understanding or a model of theological warrant.

Use the inherited four-state space `(Theta,D)` with state order `(0,0),(0,1),(1,0),(1,1)`. `Theta` is the selected binary target and `D` is one fixed future audit result. The inherited laws are

    pi0 = (2/5, 1/10, 1/10, 2/5)
    pi1 = (1/10, 2/5, 2/5, 1/10).

Both give `P(Theta=1)=P(D=1)=1/2`. The proposed compact statistic is `(1, P(Theta=1), P(D=1))`, hence is identical under the two laws.

Now make the demonstration protocol exact: each benchmark query samples a fresh independent episode and reveals only one selected coordinate, either `Theta` or `D`. It never pairs the two coordinates from the same episode. Under either law, every selected coordinate is a fair Bernoulli variable. Sequentially, each fresh selected outcome is fair conditional on the prior history and current query. For a deterministic adaptive policy, each consistent full query–outcome transcript of length `n` therefore has probability `2^(-n)` under both laws; inconsistent transcripts have probability zero. Randomized query-selection factors are common to both models, so their full protocol laws still agree. This is not a claim about outcome probabilities conditional on the entire adaptive choice sequence: later choices can reveal earlier outcomes. This is a protocol-specific identifiability statement, not an allegation about the authors' actual tests.

The calibrated forecast `1/2` achieves the optimal expected Bernoulli log loss, one bit per isolated query, under both laws. That means optimal probabilistic prediction on this protocol, not correct guesses on every realized trial. More data of exactly this type do not reveal the missing dependence. The two joint laws themselves also have equally short descriptions under a declared sign-symmetric parameterization,

    pi_sigma(theta,d) = [1 + sigma (3/5) (-1)^(theta+d)] / 4,
    sigma in {+1,-1}.

This is merely an equal-length encoding of two specified candidates; there is no claim of globally minimal description length. Compactness cannot break their benchmark tie by itself.

### The consequential correction

Observe the fixed audit `D=1` and ask for the updated target probability. The correct answers are

    P_pi0(Theta=1 | D=1) = 4/5
    P_pi1(Theta=1 | D=1) = 1/5.

The same retained input cannot produce both. For these two candidates alone, every common answer has worst-case absolute error at least `3/10`; `1/2` attains that bound. This is the inherited countermodel put through a specifically declared predictive-demonstration protocol.

The missing quantity is exactly `P(Theta=1,D=1)`: it is `2/5` under the first law and `1/10` under the second. The separately predicted event probability `P(D=1)=1/2` is already known. Preserving that denominator alone cannot preserve correction.

### Repair by the existing theorem

Let `M_b` be the diagonal selector for `D=b`, and start with `V=span(1,Theta,D)`. The inherited closure calculation adds `Theta D`, giving rank progression `3 -> 4` in one step. Thus the task's repair is not an unspecified demand for more context: retain the joint numerator, an equivalent mixed moment, or genuine retrievable information from which it follows.

In the existing Walsh basis `(1,tau,delta,tau*delta)`, where `tau=(-1)^Theta` and `delta=(-1)^D`, the two states have moments `(1,0,0,+3/5)` and `(1,0,0,-3/5)`. The already-owned commuting update for audit value `b`, with `s=(-1)^b`, is

    m' = (m+s*d)/2,    t' = (t+s*h)/2,
    d' = s*m',        h' = s*t'.

For `m'>0`, the target-one posterior is `(1-t'/m')/2`. Verification checks the full matrix identity, not only these two inputs. Repeating the same fixed observation is idempotent; a contradictory reread has probability zero and no posterior.

A probe asking for the `D=1` conditional answer separates the two declared candidates. Passing that probe does not identify all possible models, supply the true answer's empirical warrant, or prove unlimited competence. Under a broader finite task family, the inherited closure must be computed for that actual family and its justified channels. At a fixed horizon, do not silently claim invariant closure.

## 4. Where the inference does and does not travel

**Operational contribution.** The executed test turns an otherwise underspecified demonstration into an explicit protocol and finds its missing corrective observable. It supplies an implementable check for a proposed reduced/transmitted predictive state. It also shows a positive repair rather than merely warning that scores can mislead.

**No new missing-condition result.** The paper's structural qualification already excludes the deficient representation as a sufficient basis for the expanded task. The test is consistent with its argument. It does not show that its account equates all compression with understanding, or that the authors overlooked counterfactuals. If only the original isolated-coordinate task is promised, the compact marginal state is adequate. The failure appears when the promised task includes correction.

**No causal-identification result.** This audit conditions on information; it is not a causal intervention. H-Continuation can evaluate declared intervention matrices, but their correctness and their link to the target domain must be supplied. It cannot recover causal mechanisms merely from a predictive score. For a causal use, the necessary transfer is an independently warranted mapping from the relevant intervention to its model operation. No such empirical case has been provided here. Conversely, an account of grammar or logical dependence need not be forced into a causal-mechanical mold.

**No reduction of source-guided warrant.** The guide comparison concerns recognizing relevant excellence in content a learner partly understands, with additional truthfulness, benefit, and broader attestation grounds where applicable. It is not the benchmark protocol above. The learner's warranted reception of new content need not reproduce the teacher's model or independently verify every taught conclusion. Ordinary reliance and acquiring the source's competence are distinct achievements. Nothing in the finite calculation withdraws the report's affirmative warrant or requires a reflective mathematical certificate before ordinary knowledge is possible.

The common research question is whether the demonstrated achievement bears on the further competence being relied on. The two literatures can illuminate that question without identical premises or a shared numerical measure. No subjective-state claim about AI systems follows.

## 5. Verification, coverage, and stopping boundary

Normal and optimized (`python3 -O`) runs of `verify.py` completed successfully using explicit checked raises for the laws, marginals, conditional answers, closure, commuting updates, and impossible branches. Deliberately false checks failed in both modes. Fixed-query likelihood enumeration through length five corroborates that restricted product calculation. A separate two-step adaptive control chooses `D` second exactly when the first bit is one: conditioning on choices `(Theta,D)` makes the first bit certain and gives probability `1/2`, not `1/4`, to outcome pair `(1,1)`. The 16 full-transcript checks confirm the corrected policy law; the all-length statement follows from sequential fairness and common policy factors. The earlier normal-only receipt and pre-correction report/script are preserved unchanged, with exact diffs and a correction receipt. Optional conditional code-length numbers are floating-point illustrations only: retaining the dependence reduces expected conditional log loss from 1 bit to approximately 0.721928 bits. They play no role in a source-warrant judgment.

Primary reading was continuous through the complete main argument, PDF pp.1–23, including §§1–5 and their notes. The 29-page PDF's bibliography was not independently researched. PDF pp.8, 9, 14, 18, 19, 20, and 23 were additionally rendered and visually inspected. The source was obtained from version-specific arXiv PDF and HTML endpoints; metadata and source hashes are retained. No claim of full visual page coverage, verification of cited external works, or independent support for the Proxy Hypothesis is made.

**Exact boundary:** one concrete corrective-transfer application is complete. The selected comparison yields no new general theorem and no newly discovered absent conceptual safeguard. Further progress would require a specified real demonstration, target task and justified operation/model mapping. Without that, extending this example would only duplicate the inherited machinery. T20 remains open; nothing here advances programme status or closure.
