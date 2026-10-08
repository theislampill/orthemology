/- Negative controls for the exact admitted boundaries. -/
import AllInheritedPositiveControls
import AllContextualJ
namespace P01AC.Negative
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def totalRaw : Link P01DF.totalPER rawPER where
  rel := fun _ _ => True
  endpoints := fun _ => ⟨trivial,.refl _⟩
  respect := fun _ _ _ => trivial

def rawTotal : Link rawPER P01DF.totalPER where
  rel := fun _ _ => True
  endpoints := fun _ => ⟨.refl _,trivial⟩
  respect := fun _ _ _ => trivial

def rightSeparating : REnv where
  left := fun _ => P01DF.totalPER
  right := fun _ => rawPER
  rel := fun _ => totalRaw.rel
  endpoints := fun _ => totalRaw.endpoints
  respect := fun _ => totalRaw.respect

def leftSeparating : REnv where
  left := fun _ => rawPER
  right := fun _ => P01DF.totalPER
  rel := fun _ => rawTotal.rel
  endpoints := fun _ => rawTotal.endpoints
  respect := fun _ => rawTotal.respect

def pairContext : Tel := [.param 0,.param 0]
def equalEnv : Env := cons .i (cons .i zeroEnv)
def splitEnv : Env := cons P01DF.skk (cons .i zeroEnv)
def equalityTest : Ty := .identity (.param 0) (.var 1) (.var 0)

theorem pair_context_formed : Ctx pairContext :=
  .ext (.ext .nil (.param .nil)) (.param (.ext .nil (.param .nil)))

theorem equality_test_formed : Form pairContext equalityTest := by
  have a : Form pairContext (.param 0) := .param pair_context_formed
  exact .identity a (.var a (.succ .zero)) (.var a .zero)

theorem right_cross_links_without_equality :
    H pairContext rightSeparating equalEnv splitEnv ∧
    F equalityTest rightSeparating.left equalEnv .i .i ∧
    ¬ F equalityTest rightSeparating.right splitEnv .i .i ∧
    ¬ G equalityTest rightSeparating equalEnv splitEnv .i .i := by
  refine ⟨⟨⟨⟨rfl,rfl⟩,trivial⟩,trivial⟩,⟨trivial,.refl _,.refl _⟩,?_,?_⟩
  · intro h; exact P01Source.I_SKK_not_convertible h.1
  · intro h; exact P01Source.I_SKK_not_convertible h.2.1

theorem left_cross_links_without_equality :
    H pairContext leftSeparating splitEnv equalEnv ∧
    F equalityTest leftSeparating.right equalEnv .i .i ∧
    ¬ F equalityTest leftSeparating.left splitEnv .i .i ∧
    ¬ G equalityTest leftSeparating splitEnv equalEnv .i .i := by
  refine ⟨⟨⟨⟨rfl,rfl⟩,trivial⟩,trivial⟩,⟨trivial,.refl _,.refl _⟩,?_,?_⟩
  · intro h; exact P01Source.I_SKK_not_convertible h.1
  · intro h; exact P01Source.I_SKK_not_convertible h.1

theorem no_universal_raw_variable : ¬ Has [.param 0] (.var 0) .raw := by
  intro h
  let ρ : OEnv := fun _ => (P01R.interpret identityCode).obj (fun _ => rawPER)
  have ii : F (.param 0) ρ zeroEnv .i P01DF.skk :=
    ((P01R.interpret identityCode).identity (fun _ => rawPER) _ _).mp
      (recursive_polymorphic_I_skk (diagEnv (fun _ => rawPER)))
  have e : E [.param 0] ρ (cons .i zeroEnv) (cons P01DF.skk zeroEnv) := ⟨⟨rfl,rfl⟩,ii⟩
  exact P01Source.I_SKK_not_convertible (unary_fundamental h e)

/-- The actual telescope relation records endpoint equality and proof conversion.
    These obligations cannot disappear from a sound J transport proof. -/
theorem j_transport_requires_both_coordinates {Γ A x ρ η y e}
    (h : E (theta Γ A x) ρ (cons .i (cons (eval x η) η)) (cons e (cons y η))) :
    F A ρ η (eval x η) y ∧ Conv e .i := ⟨h.1.2,h.2.2.2⟩

theorem j_endpoint_omission_fails :
    ¬ E (theta [] .raw (.atom .i)) (fun _ => rawPER)
      (cons .i (cons .i zeroEnv)) (cons .i (cons P01DF.skk zeroEnv)) := by
  intro h
  exact P01Source.I_SKK_not_convertible h.1.2

theorem j_proof_coordinate_omission_fails :
    ¬ E (theta [] .raw (.atom .i)) (fun _ => rawPER)
      (cons .i (cons .i zeroEnv)) (cons P01DF.skk (cons .i zeroEnv)) := by
  intro h
  exact P01Source.I_SKK_not_convertible h.2.2.2.symm

theorem conversion_scope_premise_necessary :
    ∃ p q, P01DF.PolyConv p q ∧ Scoped 0 p ∧ ¬ Scoped 0 q := by
  refine ⟨.atom .i,.app (.app (.atom .k) (.atom .i)) (.var 0),.symm (.k _ _),trivial,?_⟩
  intro h
  exact Nat.not_lt_zero 0 h.2

end P01AC.Negative
