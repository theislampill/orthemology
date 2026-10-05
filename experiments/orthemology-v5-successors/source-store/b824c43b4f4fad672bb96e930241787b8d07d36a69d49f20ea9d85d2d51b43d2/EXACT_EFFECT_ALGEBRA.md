# Exact finite open-fragment algebra

Status: mathematical definition sharpening DERIVED_INTERFACE_v1 before implementation.

## Basic normal form

Use a finite input stack s, top first, with |s|>=1. Every prefix of an admitted execution must leave at least one frame. A normal-form effect is E=(h,P,k,M):

- h>=1 is the least required input depth.
- P is a finite list of literal original-origin keys, top first.
- k>=0 is the number of consumed incoming frames.
- M maps selected fresh output occurrence IDs, in emission order, to expressions that are either literal origin keys or I_j.

The final stack is P concatenated with s[k:]. In a well-formed generated effect, h>=k+1, so this tail is nonempty. The execution does not pop the incoming stack entirely and recreate a root from nothing; such an execution would have crossed an invalid empty configuration.

Initialize (h,P,k,M)=(1,[],0,[]). Process events:

- enter(o): replace P by [o]+P.
- leave with P nonempty: remove P's first element.
- leave with P empty: increase k by 1 and replace h by max(h,k+1), using the new k.
- selected emit(t): append (t,P[0]) if P is nonempty, otherwise append (t,I_k).
- unselected emit: no change to M.

This explicitly computes the finite effect without role values. Each reference I_j in M has j<h. Induction over the events proves these invariants and the direct-execution substitution property. The depth h equals 1 minus the minimum, over event prefixes including the empty prefix, of (#enter-#leave). It is exact: every input depth at least h is admitted, and a smaller positive depth underflows at a prefix attaining that minimum.

## Composition formulas

Let E_f=(h_f,P_f,k_f,M_f), E_g=(h_g,P_g,k_g,M_g). Put p_f=|P_f| and delta_f=p_f-k_f. Define substitution rho_f by:

    rho_f(I_j)=P_f[j]                    when j<p_f
    rho_f(I_j)=I_(k_f+j-p_f)             when j>=p_f
    rho_f(o)=o                          for literal original keys.

The composite selected emissions are M_f followed by rho_f(M_g). Fresh target occurrence IDs prevent collisions; equal source keys may legitimately recur.

The least input depth is:

    h_fg = max(h_f, h_g-delta_f).

If k_g<p_f, the composite outgoing form is:

    P_fg=P_g + P_f[k_g:],     k_fg=k_f.

If k_g>=p_f, it is:

    P_fg=P_g,                k_fg=k_f+k_g-p_f.

These formulas use concatenation of lists, not union of source roles. All role values remain outside the effect.

**Exact domain proof.** f accepts precisely input depths d>=h_f and then has depth d+delta_f. g accepts this precisely when d+delta_f>=h_g. The conjunction is exactly d>=h_fg. Its actual returned stack is obtained by dropping g's k_g frames from f's finite prefix/tail, yielding the two cases above. Substitution gives the same target references. Consequently the formulas compute the exact concatenated effect; associativity follows from source-sequence associativity and canonical normal-form uniqueness.

## Optional keyed exits for cut integrity

The base calculus assumes an already source-justified scope skeleton. A checker should not accept arbitrary foreign closing markers merely because their number happens to match. One refinement adds exit(o), which requires the current origin to equal o before leaving.

The effect adds a finite conjunction C of origin-reference equalities. If the current symbolic top is a literal key a, exit(o) checks a=o; if unequal, the effect has empty domain. If the top is I_j, add I_j=o, then perform leave. Public key equality is exact equality of the bound source/snapshot/context tuple, not proposition equality.

Composition carries C_f together with rho_f(C_g). Contradictory literal equalities or two different required literal keys for one incoming slot make the domain empty. The depth condition remains as above on nonempty domains. This is ordinary symbolic checking of a prefix precondition, not a new source-authentication protocol.

The source-case suffix with exit(f);exit(p);emit(z) fixes I_0=f and I_1=p while z still refers to I_2. It does not manufacture the missing I_2->a identity map. That map remains a separately preserved or acquired source-boundary witness.

Any actual code test should include an exit from the wrong source snapshot, an unequal required origin at the same depth, and a valid positive same-origin composition. More sophisticated natural-language quotation boundaries remain a source-interpretation obligation.
