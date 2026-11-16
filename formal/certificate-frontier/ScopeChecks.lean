import CertificateFrontier

open CertificateFrontier

-- Concrete specialization to an available ordered cost type.
example {E : Type*} [DecidableEq E] (A B : Finset (Pair E ℕ)) :
    frontier A = frontier B ↔ ∀ U, cost A U = cost B U :=
  frontier_eq_iff_cost

-- Empty catalogue and empty support are covered, without exceptional premises.
example {E : Type*} [DecidableEq E] (U : Finset E) :
    cost (∅ : Finset (Pair E ℕ)) U = ⊤ := by
  simp [cost]

example {E : Type*} [DecidableEq E] (U : Finset E) (c : ℕ) :
    cost ({(∅, c)} : Finset (Pair E ℕ)) U = (c : WithTop ℕ) := by
  simp [cost]

example {E : Type*} [DecidableEq E] (c : ℕ) :
    frontier ({(∅, c)} : Finset (Pair E ℕ)) = {(∅, c)} := by
  ext p
  simp only [frontier, Finset.mem_filter, Finset.mem_singleton]
  constructor
  · exact And.left
  · intro hp
    subst p
    exact ⟨rfl, by intro q hq _; subst q; exact le_rfl⟩

-- A top-valued element of C is still a proper value below the NEW WithTop top.
-- This generality must not be read as allowing infeasible infinite certificate
-- costs to collapse to the same observation as an empty catalogue.
example : ((⊤ : WithTop ℕ) : WithTop (WithTop ℕ)) < ⊤ :=
  WithTop.coe_lt_top _

#print axioms CertificateFrontier.frontier_inverse
#print axioms CertificateFrontier.summary_necessity
