# Proposed boundary control: polymorphic identity without a normal source representative

Status: ordinary mathematical argument verified by source inspection; minimal contract proposed for independent design admission. No implementation or new kernel acceptance is claimed.

## Exact witness and argument

Let t = app(app(S,K),app(K,Omega)), and p = app(app(atom S,atom K),app(atom K,atom Omega)). Thus eval p η = t for every η. Keep the polynomial application structure; do not replace p by atom t or postulate an atom/application bridge.

For arbitrary type parameter alpha, old Has types K at alpha → Raw → alpha, and K Omega at alpha → Raw. The latter uses K : Raw → alpha → Raw and the existing raw certificate for atom Omega. S at (alpha → Raw → alpha) → (alpha → Raw) → alpha → alpha gives p : alpha → alpha. Old All introduction gives p : All(alpha → alpha). This is an explicit finite old-rule tree, closed and supported at zero, hence eligible for the accepted new legacy embedding with unchanged p. The new result type is fin(All(var0 → var0)), equivalently all(arr(param0,param0)). No unsound unshifted open-context All introduction is used: the free term telescope is empty.

For every raw argument a, t a takes an S head step to K a ((K Omega) a), then a K head step to a. This is exact two-step operational identity on applications, not a claim t is source-convertible to I. The unapplied t is already function-shaped weak-head syntax: absence of a normal form concerns the existing full contextual source reduction, not divergence of every evaluation strategy. Applying it to a normal argument terminates in those two head contractions; a weak-head strategy need never inspect Omega.

Before application, the outer S has only two arguments, and the inner K has only one. Neither is a root redex. S and K are normal constants. Consequently every source step from S K (K q) is induced by a step inside q and preserves this wrapper. Induction on Red gives every reduct of t the form S K (K q) with Red Omega q. Equivalently one can reuse the accepted Omega shape invariant to obtain q = omegaShape m n. Every such q has another step, by the inherited omega_no_normal_reduct or shape_has_step. Compatible right reduction twice gives a further step of the wrapper. Thus no reduct of t is normal.

If Conv t u and FiniteDerives u C, inherited finite_normal_form supplies u →* n with Normal n. Inherited conv_join and normal_red then force t →* n, contradicting the preceding result. Therefore no source-convertible FiniteDerives representative exists, at any finite type C. In particular t is not source-convertible to I.

## Scope and ownership

The nonempty closed polymorphic identity result type is material: I is its accepted finite inhabitant. This example strengthens the already-preserved warning from “Raw admits Omega” and “finite-result certificates need not be strongly normalizing” to failure of even weak source normalization and source-conversion-preserving finite reification at this finite polymorphic result type.

It does not establish lack of a PER-equivalent finite representative. Indeed its identity behavior is compatible with being related to I in the relational model. Do not confuse exact source conversion with extensional/PER equality. Nor does it refute the accepted FiniteDerives normalization theorem: p's certificate uses the larger judgement's Raw rule, not FiniteDerives. It does not refute an earlier full-normalization or full-section-reification claim, since those were excluded.

Prior ownership is substantial: raw typing and S/K/All rules, compatible source reduction, Omega's all-reduct shape/no-normal-reduct theorem, finite normalization and source confluence are inherited. P01Omega already proves Omega itself lacks a finite source-conversion representative; NormalisationAndNumerals already proves non-SN discarded expansions in every inhabited unary Code. Neither inspected owner states this precise closed polymorphic typed wrapper result. Targeted searches of the retained canonical P01 source store, retained obligation/review text and accepted Eleventh substitution/nucleus/All source trees located no exact theorem for S K (K Omega) or a no-normal-reduct/no-finite-representative witness at the polymorphic identity result. This is bounded absence, not historical novelty certification. Scientific credit should be “explicit boundary corollary/control from inherited machinery,” not new calculus capability or a general discovery.

## Minimal proposed implementation contract

If independently admitted, use one fresh control module outside accepted source trees, importing exact accepted owners. Prove only:

1. The concrete p/t definitions and universal literal eval equality.
2. A closed, support-certified Type-valued old derivation of p : All(alpha → alpha), its erased old Has certificate, and its exact accepted-translation new Has certificate. This avoids assuming compatibility or atom expansion.
3. For every a, the two displayed Step facts (or their exact two-step Red composition) from t a to a.
4. Wrapper reduction inversion/invariance sufficient to prove ∀u, Red t u → ¬ Normal u, reusing accepted Omega invariants.
5. ¬∃u C, FiniteDerives u C ∧ Conv t u, by inherited finite_normal_form/conv_join/normal_red.

A single conjunction/readback binds the same p and t across positive typing and negative normalization conclusions. I's inherited finite certificate witnesses nonemptiness of the exact target. No independent implementation of normalization or confluence, new conversion rules, new general calculus, mutation tests, target-language reduction claim, source-code refactor or canonical edit is necessary. Check exact theorem signatures and transitive axiom dependencies; rebuild only the required fresh control against pinned accepted inputs under the existing serial compiler policy. An independent reviewer should verify literal atom/application structure, the absence of an outer root redex, both compatible right lifts and the scope-zero legacy certificate.

Stopping condition: accepted small control plus a short report boundary paragraph, or an identified proof/contract blocker. If the argument requires changing accepted definitions or claiming PER nonrepresentability, reject that change rather than expanding scope.
