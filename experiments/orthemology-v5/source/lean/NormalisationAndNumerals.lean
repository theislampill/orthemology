/-
Further elementary consequences of the SAME invariant-set universe.
STATUS: authored source, NOT kernel-verified. No general normalisation theorem
is asserted. In fact every inhabited semantic code admits non-SN expansions.
-/
import EffectsAndDependence

namespace OrthemologyV3
open OrthemologyV2

def duplicator : Term := .app (.app .s .i) .i
def omega : Term := .app duplicator duplicator
def omega1 : Term := .app (.app .i duplicator) (.app .i duplicator)
def omega2 : Term := .app duplicator (.app .i duplicator)

theorem omega_step1 : Step omega omega1 := .s .i .i duplicator
theorem omega_step2 : Step omega1 omega2 := .left (.i duplicator) _
theorem omega_step3 : Step omega2 omega := .right duplicator (.i duplicator)

def StronglyNormalising (t : Term) : Prop :=
  Acc (fun u t => Step t u) t

theorem three_cycle_not_SN {a b c : Term}
    (ab : Step a b) (bc : Step b c) (ca : Step c a) :
    ¬ StronglyNormalising a := by
  intro h
  have aux : ∀ a, Acc (fun u t => Step t u) a →
      ∀ b c, Step a b → Step b c → Step c a → False := by
    intro a ha
    induction ha with
    | intro a next ih =>
        intro b c ab bc ca
        exact ih b ab c a bc ca ab
  exact aux a h b c ab bc ca

def discard (t u : Term) : Term := .app (.app .k t) u

theorem every_inhabited_code_contains_non_SN (A : Code) (t : Term)
    (ht : A.accepts t) :
    ∃ u, A.accepts u ∧ ¬ StronglyNormalising u := by
  refine ⟨discard t omega, (A.stable (.k t omega)).mpr ht, ?_⟩
  exact three_cycle_not_SN
    (Step.right (.app .k t) omega_step1)
    (Step.right (.app .k t) omega_step2)
    (Step.right (.app .k t) omega_step3)

def iterateTerm (f : Term) : Nat → Term → Term
  | 0,x => x
  | n+1,x => .app f (iterateTerm f n x)

def orbitCode (f x : Term) : Code where
  accepts := fun t => ∃ n, Conv t (iterateTerm f n x)
  stable := fun h =>
    ⟨fun ⟨n,ht⟩ => ⟨n,.trans (.symm (.step h)) ht⟩,
     fun ⟨n,hu⟩ => ⟨n,.trans (.step h) hu⟩⟩

def naturalCode : Code := Code.all fun A =>
  Code.arrow (Code.arrow A A) (Code.arrow A A)

theorem replace_iterate (n : Nat) (f x : Term) :
    replaceMarkers f x (iterateTerm .zero n .one) = iterateTerm f n x := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [iterateTerm,replaceMarkers,ih]

theorem numeral_representability {t : Term} (free : MarkerFree t)
    (ht : naturalCode.accepts t) :
    ∃ n, ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x) := by
  have hm : (Code.arrow (orbitCode .zero .one)
    (orbitCode .zero .one)).accepts .zero := by
    intro a ha
    obtain ⟨n,hn⟩ := ha
    exact ⟨n+1,Conv.right .zero hn⟩
  have hx : (orbitCode .zero .one).accepts .one := ⟨0,.refl _⟩
  obtain ⟨n,hn⟩ := ht (orbitCode .zero .one) .zero hm .one hx
  refine ⟨n,?_⟩
  intro f x
  have hr := conv_replace hn f x
  simpa only [replaceMarkers,replace_free free,replace_iterate] using hr

end OrthemologyV3

#print axioms OrthemologyV3.three_cycle_not_SN
#print axioms OrthemologyV3.every_inhabited_code_contains_non_SN
#print axioms OrthemologyV3.numeral_representability
