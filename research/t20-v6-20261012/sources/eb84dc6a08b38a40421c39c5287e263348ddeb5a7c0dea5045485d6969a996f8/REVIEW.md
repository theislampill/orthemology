# Independent bounded review: constrained learning at a fixed finite prior

10 October 2026 UTC. Outcome: **PASS within the stated finite, model-relative mathematical scope. No blocking or nonblocking correction is required.** This is an independent proof, source, and exact-control review, not formal-kernel certification, physical evidence validation, integration approval, or T20/programme closure.

## Exact target and independence

The reviewed author report is `constrained-learning-possibility-20261010/RESULT.md`, 18,333 bytes, SHA-256:

`a625a2c137d291f514c71eee13e6cc7e4399a1bff491d1b59548a5985f6649f9`

The reviewer did not develop the candidate proofs or edit the author packet. The root and original worker's shared development is acknowledged in the author report, and their verification is not treated as independent corroboration. The complete 10-file author packet and all eight hash-bound inherited inputs were copied into this review's `replay/` tree before replaying its unmodified verifier. `REVIEWED_EXACTFILES.json` binds those 18 files. All nine author-manifest entries and all eight inherited-input bindings passed exact byte-count and SHA-256 checks.

The author's verifier writes its results next to itself. It was therefore executed only inside the review snapshot, not against the original packet. Its replay output is byte-identical to the frozen author result. No author or protected source was changed. `MANIFEST.json` binds the completed review artifact; it excludes itself to avoid circular hashing.

## Proof findings

### 1. Finite constrained splitting: valid

For a finite channel, the identity alpha_y q_y(i)=p_i K(y|i), summed over outcomes, establishes Bayes plausibility. Conversely, positive mixture weights and nonnegative posterior coordinates force every proposed posterior to vanish outside supp(p). On supp(p), dividing alpha_y q_y(i) by p_i gives nonnegative column-stochastic entries. Columns outside supp(p) can be filled with any probability law on the output labels because their entire joint-law column is zero.

This argument does not use convexity. Convexity is needed later to replace the other branches by one feasible residual. Duplicate posterior labels, one positive-probability label, and labels of zero probability are handled consistently: a sole positive branch equals p, duplicates are allowed, and null branches have no assigned posterior. The arbitrary off-support columns are a mathematical completion, not observations of previously impossible states.

### 2. Generated minimal face without closure: valid

The displayed set F_C(p) includes p. Reducing any two witness coefficients to a common positive coefficient, then mixing their residuals, proves convexity. For the segment property, if p=lambda q+(1-lambda)r and q=t a+(1-t)b, then

p=(lambda t)a+(1-lambda t)[lambda(1-t)b+(1-lambda)r]/(1-lambda t).

Both coefficients are strict and the residual lies in C. Thus a belongs to F_C(p); the same argument applies to b. Any face containing p must contain every endpoint appearing with positive weight in a witnessing segment, which proves minimality. No limiting sequence, topological closure, compactness, exposed-face theorem, or relative-interior theorem is used.

For reachability, a branch of weight below one supplies a residual by averaging all other posteriors, while a weight-one branch is p itself. The reverse direction is precisely the binary splitting construction. Consequently this is the algebraic minimal face of C, not the closed face of a closure of C and not merely the simplex support face.

### 3. Exact strictly positive reachability: valid

Necessity requires both membership in F_C(p), from completeness of the feasible experiment, and exactly the prior support, from strict positivity of each channel entry. For sufficiency, decreasing a witnessing endpoint weight leaves a residual in C and gives that residual a positive multiple of q on every supported coordinate. The two constructed rows are strictly positive on the current support, and any positive off-support columns complete the kernel. This also covers q=p using two identical posterior labels.

An important interpretation is correct: strict positivity forbids losing prior support, but does not forbid reaching a boundary point of C that still has the prior support. The independent nonclosed-segment control checks precisely this distinction. Mere feasibility and matching support do not suffice if the selected point is outside F_C(p).

### 4. Informative iff nonextreme, with positive binary witness: valid

If some positive-weight posterior differs from p, its complementary feasible mean makes p a nontrivial two-point mixture. Conversely, shrinking both endpoints of any nontrivial decomposition toward p keeps them in convex C, preserves the mixture equation and their distinctness, and gives each exactly supp(p). The splitting construction then yields a binary channel positive at every state. Thus no closedness or full-support hypothesis was omitted.

“Informative” is explicitly about the posterior of the represented, fixed target X. At an extreme prior, the result does not forbid learning about a source, nuisance, authority, unrepresented target, or other aspects of cognition. The report makes that restriction both near its headline and after the corollary. Mathematical existence supplies neither useful information of any fixed minimum size nor a matching physical/permitted source.

### 5. Fixed-target finite adaptive flattening: valid

At each positive-probability history, the conditional barycenter identity allows the same splitting construction. A child's generated face is contained in its parent's generated face, since the parent face contains the child and the child's minimal face is contained in every face containing it.

Multiplying the conditional kernel entries along each terminal transcript gives a stochastic finite transcript channel. Conversely, any prescribed finite terminal posterior mixture with mean p is a one-step splitting. In an already specified finite tree, internal posteriors are finite conditional mixtures of terminal posteriors, so convex C membership at every terminal node implies it at every positive-probability internal node. Variable depths and posterior support loss do not change this conclusion.

The scope guards are necessary and present: a single fixed target, passive observation, correctly conditioned likelihoods, all selection information included in history, arbitrary mathematical channels, and no timing restrictions for the terminal-possibility comparison. Flattening does not assert equivalent physical actions, access, permission, costs, or availability. It does not justify copying marginal likelihoods, unmodelled state-dependent selection, changing targets, or any infinite-horizon stopping claim.

## Inherited example and executed controls

The first-stage fixed-mass example and its failed unchanged repetition are exactly inherited from the prior finite-Bayes report's section 4.2. They are correctly labelled reused. The additional history-conditioned second-stage rows and all four displayed leaves were checked independently by literal transcription into a joint-law calculation, rather than using the author's witness generator. The four leaf weights are each 1/4 and their mean is p.

Executed evidence:

- Unmodified author verifier in `replay/`: PASS, 12 control groups, 19 selected open-segment priors, eight inherited-input hashes. `AUTHOR_CONTROL_REPLAY.log` records execution.
- Separately written `independent_controls.py`: PASS, four fixed discriminating groups, recorded in `INDEPENDENT_CONTROL_RESULTS.json` and `INDEPENDENT_CONTROLS.log`.
  1. C={(t,1-t):0<t<=3/4}, p=(1/2,1/2), and a strictly positive binary channel reaching the included boundary posterior (3/4,1/4) with weight 1/3 and residual (3/8,5/8). Closing C or replacing support equality by relative-interior membership would be erroneous. At its included extreme endpoint, any lower endpoint branch forces a residual above 3/4: r_1=3/4+lambda(3/4-q_1)/(1-lambda).
  2. Two different positive off-support stochastic completions give identical joint laws at a prior with a zero coordinate. A third outcome supported only at that zero-prior state has probability zero and no posterior.
  3. A variable-depth tree first loses support, stops on one branch, and continues uninformatively on the other. Flattening gives exact terminal weights (1/2,1/8,3/8) and preserves the full joint law.
  4. Literal displayed two-stage kernels reproduce the four exact terminal posteriors in the report.
- `SOURCE_REBIND_REVIEW.json`: PASS. The preserved earlier finite-Bayes source and its corrected version match both recorded hashes. Their sole difference adds convex C to the strict-convexity uniqueness condition. No splitting or fixed-mass example used here changed.

These finite controls corroborate the written proofs. They are neither a universal proof by enumeration nor a benchmark, empirical experiment, Lean check, or formal proof certificate. No additional search campaign was conducted.

## Source and ancestry check

The external URLs in the author source register were reopened on 10 October 2026. Only bounded relevant passages were used:

- Kamenica and Gentzkow, *Bayesian Persuasion* (2011): setup, section I.B/Proposition 1, finite-support qualification, Appendix A, and the introduction's prior-work discussion. The full-support setup and posterior-to-signal construction support the stated classical ancestry; the packet's direct support restriction deals with zero prior coordinates. No strategic or optimization conclusion is imported. [Primary paper](https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf).
- Arieli, Babichenko, Sandomirskiy, and Tamuz, *Feasible Joint Posterior Beliefs*, dated 22 December 2020: front matter, introduction's one-agent discussion, and section 2's martingale/splitting statement. Those passages explicitly connect one-agent splitting to Blackwell and Aumann–Maschler. This checks the attribution in that paper, not the original older theorem text or historical priority. [Primary paper](https://tamuz.caltech.edu/papers/feasible.pdf).
- Babichenko, Talgam-Cohen, and Zabarnyi, *Bayesian Persuasion under Ex Ante and Ex Post Constraints*, arXiv v2 dated 11 April 2021: front matter and sections 2.1–2.2, including Definition 2.5. The paper already combines Bayes plausibility with restrictions on each realized posterior. The report appropriately claims no new constraint paradigm or optimization theorem. [Primary paper](https://arxiv.org/pdf/2012.03272v2).
- The MIT Press book record verifies the named *Repeated Games with Incomplete Information* and 1995 edition; no original lemma wording or theorem number is imported. [Publisher record](https://mitpress.mit.edu/9780262526265/repeated-games-with-incomplete-information/).

Local comparison was bounded to the finite-Bayes global/local discussion and section 4.2, warranted-learning sections 6–8, the posterior-inquiry-value report, H-Continuation's instrument definition and Theorem 2, the stochastic-exact-inquiry and quotient-transport contracts, the proof-sensitive cost/completion statement, and the nearby measure-space theorem's scope. All eight files were hash-bound even where only these relevant passages were read. The comparisons substantiate inherited barycenters, branch-weighted values, permission/provenance boundaries, cost-sensitive completion, and stronger exact-stopping objectives. This review does not independently certify every theorem in those inherited packets or establish absence of the present formulation across a whole corpus.

## Disposition and stopping boundary

The packet can be cited as a bounded elementary mathematical application of classical finite splitting and convex geometry at the fixed-prior constraint interface. Preserve the distinction between global preservation, complete local feasibility, and a favorable single branch. Preserve all physical-source, evidence-warrant, target, and permission guards.

No author revision is requested. The review is complete once final hashes and unchanged-source checks pass. It grants no protected change, integration, release readiness, or programme/T20 closure authority.
