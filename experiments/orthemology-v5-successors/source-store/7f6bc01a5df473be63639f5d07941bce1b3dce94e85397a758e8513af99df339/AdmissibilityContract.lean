import SubstitutionAdmissibility
open P01D P01DF
example {p : Poly} {A : Ty} (h : Has p A) (σ : Nat → Poly) :
    Has (psub σ p) (substIndex σ A) :=
  P01DF.Syntactic.has_index_substitution h σ
example {p : Poly} {A : Ty} (h : Has p A) (τ : Nat → Ty) :
    Has p (substType τ A) :=
  P01DF.Syntactic.has_type_substitution h τ
