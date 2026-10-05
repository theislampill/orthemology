# Independent review: finite-limit warrants and strict certificates

3 October 2026 UTC. Ordinary mathematical/design review only. No new checker, compiler, formalisation, canonical edit, external contact or publication. Author inputs are preserved. `REVIEWED_INPUTS.sha256` identifies the inspected local inputs; the author's 17-entry dependency manifest was also checked successfully.

## Verdict first

**Admit a small standalone mathematical boundary addendum. Do not implement another checker on the present evidence.**

There is no blocking mathematical defect in the stated compact-neighbourhood theorem, the effective-search result under its represented-input promises, the half-affine composition, the two strict-certificate completeness equivalences, or the uniform exact-zero obstruction. The latter genuinely fits the admitted P02-L1 grammar; an explicit finite-syntax construction and its invariant are supplied in `MATHEMATICAL_CONTROLS.md` rather than leaving that admission to an unrestricted-program assumption.

The useful increment is the conjunction of three facts in Tenth's corrected inverse-system setting:

1. Compact completion makes an answer that is stable on an ambient open neighbourhood finitely witnessable.
2. Effective compact information makes that witness searchable without a supplied numerical convergence rate.
3. Neither conclusion makes exact boundary equality uniformly certifiable, even when the whole state is uniquely determined and uniformly computable with a known geometric rate.

This delimits a legitimate use of Ninth's finite-warrant interface. It does not extend Ninth's completed finite-rational existence calculus, strengthen P02's hierarchy theorem, or supply a collective acquisition protocol. The recommended concise replacement/addendum is `MINIMAL_ADDENDUM.md`.

## Findings that change admission or use

### R1. Additional inherited ownership: the arithmetic mechanism already exists

`PRIOR_OWNERSHIP.md` properly credits P02 syntax and halting simulation, but its P02 entry does not name the particularly close owner: **C2-06, Rational shift compiler**, and the corresponding `compile_shift` in `P02/code/prcodec.py:293–310`. They already use a dyadic prefix interval, exact rational endpoint comparisons by integer cross-multiplication, and finite-prefix stopping. C2-12 supplies the surrounding rational-selector argument. The original V5 `DEFECT_COMPUTABILITY.md`, §4, “Shift to every rational threshold,” also owns this mechanism in the historical source.

That earlier use has a different measure/selector purpose and may use non-strict endpoint tests. It does not already prove the new strict certificate claim for an independently specified inverse-limit scalar. Conversely, changing the purpose and using strict inequalities does not make dyadic endpoint arithmetic, finite-prefix evidence, or proof checking new methodology.

**Disposition:** add these exact ownership locators before assigning contribution credit. This is a credit/allocation correction, not a refutation of the new theorem.

### R2. Concrete implementation hazard: P02's observer wrapper erases unary generators

The proposal correctly invokes unary mathematical evaluation. In the inspected actual source, however, `evaluate_index(index,n,word)` returns zero whenever the decoded program is not arity two (`prcodec.py:185–188`). Every admitted unary generator therefore takes that wrapper's zero fallback. This is P02's deliberate *observer* convention, not a bug in P02.

Any later implementation must use the general `run(P,(i,))` semantics or prove an appropriate adapter. A valid unary constant-one program is the decisive control: its scalar is 1, whereas the wrong wrapper would fabricate an all-zero prefix and accept a false below-1/4 claim at depth 3. Invalid input must not be quietly repaired into the zero generator either.

**Disposition:** mandatory adapter control if implementation is ever selected. The written design itself is correct and claims no implemented adapter.

### R3. The proposed mutation sentence is too indiscriminate as a test specification

`CERTIFICATE_DESIGN.md:112` groups stale inputs, false arithmetic and changed checker semantics together as changes that “must prevent” acceptance. These need different tests.

- An unchanged certificate bound to an altered expected record must fail literal binding. A freshly rebound certificate may be valid and should be assessed afresh.
- A changed claimed numerator or replayed bit must fail its corresponding equality check.
- Reversed composition need not change palindromic or constant prefixes. Use a non-palindromic witness.
- Replacing a strict comparator by a weak comparator preserves many existing true acceptances. The requirement is that a selected equality-boundary control expose a **new false acceptance**, not that all original positive cases be rejected.

For the last point, the two legal binary expansions of 1/4 matter: `01000...` saturates a lower endpoint, while `00111...` saturates an upper endpoint. A test using only the first can miss the weakened below comparator. The controls file gives both and an order-sensitive `01` example.

**Disposition:** sharpen the future test contract. No defect in the strict formulas as written.

### R4. No distinct implementation benefit has yet been established

The recipient already receives the generator AST independently and recomputes every submitted bit. The prefix and claimed numerator are consequently redundant for soundness; a depth alone could identify the same check. The design explicitly admits this, and makes no efficiency claim. Nothing here demonstrates reduced checking work, acquisition-root independence, new communication capacity, or a new permitted action in an existing deployed protocol.

The diagnostic example does distinguish release of a strict claim from an unsupported equality inference under an independently admitted rule. That earns an **application-boundary addendum**. It does not meet the stronger portfolio test for a new collective mechanism. In particular a hardcoded constant-zero example is also solvable by a global syntax theorem; the bounded-halting example with a verified zero prefix is a cleaner witness of the boundary.

**Disposition:** no new checker/runtime lane. If a future concrete recipient protocol needs this query, reuse the existing syntax/evaluator and binding machinery; require that consumer and its extra benefit before implementation admission.

## Mathematical audit

### A. Composition and realization: correct

The intended finite composite is `f_0 ∘ ... ∘ f_(n−1)`, so extending its depth composes the new map on the right. With `V_0=0` and `V_(n+1)=2V_n+b(n)`, induction gives

`F_(0,n)(x)=(V_n+x)/2^n` and `K_(0,n)=[V_n/2^n,(V_n+1)/2^n]`.

The general affine recurrence printed in the design, `A'=Aa_n`, `B'=B+Ab_n`, has the same orientation. The direct series construction in the controls proves existence and uniqueness at **every** coordinate without borrowing an effective predecessor-selection algorithm from the compactness proof. The error bound is uniform in the program, depth and starting coordinate.

Finite range enclosure does not require uniqueness. Every compatible realization belongs to the finite image. Existence is separately secured for the admitted half-affine system; this avoids obtaining a vacuous all-realizations result from an inconsistent model.

### B. Strict soundness and completeness: correct, including edge thresholds

Let `L_n=V_n/2^n` and `U_n=L_n+2^-n`. The verified inequalities are exactly `U_n<τ` and `L_n>τ`, because `d>0` and `2^n>0`. Soundness follows from `L_n≤x_P≤U_n`.

If `x_P<τ`, pick n with `2^-n<τ−x_P`; then `U_n≤x_P+2^-n<τ`. If `x_P>τ`, pick n with `2^-n<x_P−τ`; then `L_n≥x_P−2^-n>τ`. The actual finite evaluation supplies the certificate. These proofs hold for all rational τ, including negative thresholds, 0, 1 and thresholds above 1, and at depth zero when its inequality happens to hold.

At equality neither strict certificate can exist. In particular a rational/dyadic limit, or a known global description of that limit, does not make this particular strict-prefix search terminate at the boundary. The two strict searches can be interleaved or checked sequentially at each depth because every admitted finite evaluation terminates mathematically. Resource failure is an operational non-answer, as the proposal states.

### C. Finite global-proof exceptions: correctly retained

The prefix-only negative is not an indistinguishability theorem about complete generator ASTs. A finite zero prefix permits a later nonzero coefficient, but a source invariant may exclude every such tail. The proposal explicitly recognizes this distinction.

The uniform obstruction also survives arbitrary finite global-law proofs. Let `A(P,c)` be any computably enumerable acceptance relation, sound for `x_P=0`. If every true-zero program in the admitted bounded-halting image had some accepted finite c, dovetailing all certificates would semidecide nonhalting. That is impossible for the inherited machine model. No restriction to prefix certificates is used in this argument.

The statement does **not** exclude a finite proof for a particular nonhalting machine, a sound incomplete proof branch, a finite exceptional list, or an externally supplied noncomputable oracle. The last lies outside the effective-verifier contract rather than refuting it. Certificate strings are finitely encoded and effectively enumerable; neither an unspecified “true theorem” token nor a merely asserted invariant is automatically checked evidence.

### D. Actual grammar admission: correct, previously compressed

P02-L1 contains constants, registers, natural arithmetic and comparisons, finite sequencing and conditionals, and loops with bounds snapshotted once. Those suffice to simulate a finite two-counter table for exactly n+1 current instructions, retaining the change in a latched halt bit on the last iteration. The construction in the controls uses a unary input and fresh fixed registers; it never invokes an arbitrary function tag, unbounded search or an input-totality oracle.

The result is a finite well-formed unary AST whose value is 1 exactly at the first halting stage. Its translation from the finite table is effective syntactic construction. The required undecidability premise is the standard finite two-counter halting problem already used by P02, not a new claim of a kernel-checked universal-machine theorem. C2-03 additionally supplies a general effective PR-to-P02-L1 construction, but the explicit bounded-loop argument avoids relying only on that abstract expressiveness sentence.

No implementation/source correspondence of this **new unary construction** was executed or claimed. P02's existing Q8 compiler is binary-arity and has a different output contract.

### E. Compact-neighbourhood theorem: correct under the exact hypotheses

For nested nonempty compact `K_n` in a Hausdorff space, each `K_n \ U` is closed in compact `K_0`. If none were empty, finite intersection compactness would produce a point in `S \ U`, a contradiction. Thus `S⊆U` implies some `K_n⊆U`.

The result concerns an ambient open answer region. Continuity of the restricted query on S alone is insufficient. Nonunique survivors cause no problem when the whole survivor set is inside one answer region. A fixed finite observation block must use the **actual compact block images** and their nested intersection, not an independent Cartesian product that drops compatibility constraints. The proposal's reference to the finite-horizon argument is read in that correct sense.

For the concrete half-affine family the series estimate proves everything needed without abstract effective compactness. This separation is valuable: the negative cannot be blamed on an ineffective name or a missing convergence rate.

### F. Effective compactness and modulus search: correct as a promise-domain result

The required name must provide an effective upper-compact presentation sufficient to semidecide containment in an effectively open set. An arbitrary list of some true covers, a bare compactness assertion, or a program of unknown totality is not enough. The proposal calls for the stronger proper name and separately warrants name validity.

For a singleton survivor x, choose a named dense centre c sufficiently near x. A ball of radius ε/2 about c then contains x with positive margin; the compact-neighbourhood theorem eventually puts all `K_n` inside it. Dovetailing the correct containment tests finds a stage, and nestedness extends the diameter bound to later stages. This computes a coordinatewise modulus **relative to the supplied effective names and singleton promise**. It does not decide which arbitrary purported names satisfy that promise, or produce a common advance rate for all coordinates/models from compactness alone.

The ordinary compactness theorem still applies to ineffective mathematical data; its effective-search corollary does not. The controls include a noncomputable constant-map example and a noncompact escape example to keep both dependencies visible.

## Ownership and cross-programme consequence

The author's inherited/new distinctions are broadly sound. Retain the following allocation:

- **Tenth completion correction:** survivor/projection relation, complete-realization uniqueness, fixed-horizon forgetting and their compact-continuous hypotheses.
- **Historical V5/P02:** finite-prefix/infinite-property cautions, PR syntax, bounded simulation, defect hierarchy, nonenumerability of complete zero-defect certificates, dyadic rational-selector arithmetic, and distinctions among existence/effectivity/authority.
- **Ninth:** independent finite certificate syntax/checking, exact input binding, certificate soundness/completeness for its stated finite-rational policy-existence semantics, and its execution limits.
- **This addendum:** instantiate a robust-query finite-warrant theorem and a matching exact-boundary obstruction in one simple, everywhere-admissible inverse-system family with an explicitly computable state and geometric rate. The result tells a recipient which query follows from a finite enclosure and tells the programme which proposed transfer from infinite completion to finite certification fails.

Nothing reclassifies P02 defect: its functional and representation differ. Nothing contradicts decidable rational finite-Mealy computations. Nothing infers epistemic source authenticity or normative authority from exact input equality. Avenues 5/7 obtain only inherited scope-preserving transport cautions; Avenue 6 gets a one-recipient release boundary, not common knowledge or collective closure. Avenue 10 gets a representation/query distinction in the new completion setting, not a stronger hierarchy.

## Recommended endpoint and stop

Keep the written addendum, the explicit admissible halting-family construction, and the discriminatory mathematical controls. Record the additional rational-shift ownership and the unary-wrapper hazard. This is sufficient ordinary-mathematical admission; no author rewrite or implementation is necessary to preserve the result.

If formal validation later has an identified consumer, the smallest worthwhile leaf is the generic stream-level interval formula plus strict soundness/completeness, attached to the existing completion discussion. Do not port the universal evaluator, design a new byte codec, build a general proof calculus, or treat such activity as required progress. A stream theorem must also not be labelled a checked P02 source-to-limit theorem without its missing adapter/correspondence proof.

Stop at this boundary unless a concrete consumer requires more. No canonical closure, philosophical closure, P15 completion or external originality claim follows.

## Evidence and source use

This is independent ordinary reasoning with direct local-source inspection, not an independent human/specialist review or fresh Lean replay. The author manifest and the reviewed-input manifest identify bytes; they are not source-authentication theorems.

No additional primary-paper synopsis or quotation is introduced. `SOURCE_ACCOUNTING.md` in this review uses locator-only references and records zero additional words charged to the two shared primary-work budgets. Previously supplied source capsules remain under their original cumulative accounting.
