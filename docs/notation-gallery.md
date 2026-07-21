# Orthemology notation gallery

**Status:** DRAFT — not peer reviewed. Rendered by the R7B mathematical-
typesetting pipeline (Decision 0023). Every normative symbol in
`docs/notation-registry.yaml` appears below as real mathematics: GitHub
renders the `$...$` / ` ```math ` source through MathJax, and
`scripts/build_pdfs.py` renders `artifacts/notation-gallery.pdf` through the
pinned Typst compiler via `scripts/latex_to_typst_math.py`. This is a
**typography layer, not a notation redesign**: each row's meaning is the
registry role, unchanged (Decision 0005). `scripts/validate_math_source.py`
asserts a bijection between non-retired symbols and this gallery and that
`scripts/validate_pdf_math.py` finds no missing-glyph (notdef/tofu) in the
rendered PDF — the defect reproduced in
`docs/project-closure/r7b/R7B-PDF-MATH-BASELINE.md` (the core `mu`-vector and
`C`-vector rendering as notdef under the old `#raw` path). Below they compose
correctly as $\vec\mu$ and $\vec C$.

## 1. Normative symbols rendered as mathematics

| Registry key | Rendered | Role |
|---|---|---|
| `A` | $A$ | declared analysis (identifier + version) |
| `alpha, beta, ...` | $\alpha, \beta$ | actor indices |
| `T = task(A)` | $T = \operatorname{task}(A)$ | task component of the analysis |
| `M_univ, O_univ` | $\mathcal{M}, \mathcal{O}$ | universal occurrence and ortheme universes |
| `M_A, O_A` | $\mathcal{M}_A \subseteq \mathcal{M}, \ \mathcal{O}_A \subseteq \mathcal{O}$ | analysis-active domain and repertoire |
| `Inst_A` | $\operatorname{Inst}_A \subseteq \mathcal{M}_A \times \mathcal{O}_A$ | analysis-relative instantiation (the primitive) |
| `O*(m; A)` | $O^*(m; A)$ | true (actual) profile of m under A |
| `Pi_A` | $\Pi_A$ | complete-profile space under A |
| `Pi_A_partial` | $\Pi_A^\partial$ | partial-profile space under A |
| `C_hat` | $\hat C_{A,\alpha,t}(m)$ | candidate set of complete profiles |
| `p_hat` | $\hat p_{A,\alpha,t}(m) \in \Pi_A^\partial$ | inferred (partial) profile — belief, never ground truth |
| `Omega` | $\Omega_{A,\alpha,t}$ | observation map |
| `mu` | $\mu = \langle g, S_\mu, \operatorname{select}_\mu, \operatorname{prov}, \operatorname{ver} \rangle$ | metaortheme type |
| `pi_mu` | $\pi_\mu$ | paired meta-policy |
| `mu_bar` | $\bar\mu_{e,j}$ | the j-th metaorthemma in episode e |
| `MetaInst` | $\operatorname{MetaInst}(\bar\mu_{e,j}, \mu)$ | token typing of a metaorthemma under a metaortheme |
| `Gamma_E` | $\Gamma_E = (E, \rightsquigarrow)$ | episode DAG |
| `e_Gamma` | $e_\Gamma = \operatorname{comp}(\Gamma_E)$ | composed boundary-level episode |
| `GoalSchema` | $\operatorname{GoalSchema}(\alpha)$ | parametric goal schema |
| `G_target` | $\mathcal{G}_{\alpha, A_\alpha}$ | actor-alpha's grounded target profile set |
| `Rep_A` | $\operatorname{Rep}_A$ | representation family under A |
| `chi` | $\chi \in \operatorname{Rep}_A$ | one representation |
| `L_A_star` | $L_A^*(\chi)$ | best attainable loss/risk under representation chi |
| `select_mu` | $\operatorname{select}_\mu$ | metaortheme state-selecting evidence procedure |
| `estatus_e` | $\operatorname{estatus}_e$ | per-claim evidence-status map of episode e |
| `eps_A` | $\epsilon_A$ | accepted tolerance of the analysis |
| `theta_stop` | $\theta_{\text{stop}}$ | ANDON stop/escalation risk threshold |
| `K_A` | $\mathcal{K}_A$ | cause repertoire |
| `R_A` | $\mathcal{R}_A$ | route repertoire |
| `W_A` | $\mathcal{W}_A$ | warrant-state repertoire |
| `Q_e` | $\mathcal{Q}_e$ | claim ledger of episode e |
| `delta_e` | $\delta_e$ | residual-disposition map of episode e |
| `ReqPath` | $\operatorname{ReqPath}(e)$ | governance-derived required pathway verdicts |

## 2. Structural constructs (typesetting showcase)

The pipeline handles the full range of publication constructs the corpus
uses. These are the constructs named in the Decision 0023 design spike.

### 2.1 Episode signature (display)

The formal-core episode signature — the exact site of the reproduced
notdef defect — rendered as real mathematics (`\vec\mu`, `\vec C` compose):

```math
e = \langle \operatorname{id};\ m, \kappa, v;\ x, H;\ \alpha, w, A, T, t;\ \vec\mu, \operatorname{MetaTok}, \pi;\ \vec C, \hat p;\ r;\ \operatorname{estatus};\ \mathcal{Q};\ \delta;\ \operatorname{hand\_in}, \operatorname{hand\_out};\ a, \operatorname{Succ} \rangle
```

### 2.2 Multi-line aligned equations

```math
\begin{aligned}
\operatorname{TokenAdequate}(\bar\mu, e) &\Leftrightarrow \operatorname{MetaInst}(\bar\mu, \mu) \wedge \operatorname{Compatible}(\bar\mu, A(e)) \\
\operatorname{V3c}(e) &\Leftrightarrow \forall \bar\mu \in \operatorname{MetaTok}(e): \operatorname{TokenAdequate}(\bar\mu, e)
\end{aligned}
```

### 2.3 Set comprehension and predicate

Grounded target: $\mathcal{G}_{\alpha,A_\alpha} = \{\, x \in \mathcal{M}_A \mid O^*(x; A_\alpha) \in \Pi_A \,\}$, and
strict soundness $\operatorname{StrictlySoundReasoning}_\chi(e) := \operatorname{ReasoningPathAdequate}_\chi(e) \wedge \operatorname{TokenTruthLinked}_\chi(e)$.

### 2.4 Underbrace

$\underbrace{O^*(m; A)}_{\text{ground truth, never asserted from discourse}} \neq \underbrace{\hat p_{A,\alpha,t}(m)}_{\text{inferred belief}}$

### 2.5 Labeled arrows (world transition vs learner update)

$m_t \xrightarrow{a_t} m_{t+1}$ (occurrence lineage) is not $\theta_t \xrightarrow{U_A(e_t)} \theta_{t+1}$ (learner update).

### 2.6 Table containing inline math

| Object | Symbol | Non-claim |
|---|---|---|
| observation map | $\Omega_{A,\alpha,t}$ | not the occurrence |
| inferred profile | $\hat p_{A,\alpha,t}(m)$ | not $O^*(m; A)$ |
| metaorthemma | $\bar\mu_{e,j}$ | not the metaortheme type $\mu$ |

All notation meanings are those of `docs/notation-registry.yaml`; nothing here
introduces a new symbol or claim.
