import FullPER

/- New semantic contract only. The source grammar is unchanged. -/
namespace GenericFoldTransport
open OpenTermStandardness (T SatPER Conv Arrow arrowPER churchPER iter UniformIter)

/-- A square need commute only at supported arguments. -/
def Commutes (A B : SatPER) (f g h : T) : Prop :=
  ∀ x, A.rel x x → B.rel (h ⬝ (f ⬝ x)) (g ⬝ (h ⬝ x))

/-- The finite-iteration calculation, with the relation orientation explicit. -/
theorem iter_transport (A B : SatPER) {f g h a : T}
    (ff : Arrow A.rel A.rel f f) (gg : Arrow B.rel B.rel g g)
    (hh : Arrow A.rel B.rel h h) (aa : A.rel a a)
    (square : Commutes A B f g h) (k : Nat) :
    B.rel (h ⬝ iter f a k) (iter g (h ⬝ a) k) := by
  induction k with
  | zero => exact hh a a aa
  | succ k ih =>
    exact B.trans (square _ (OpenTermStandardness.iter_related A ff aa k)) (gg _ _ ih)

/-- Uniform-count standardness suffices. No heterogeneous relation or graph
    admission is needed for this particular full-PER carrier. -/
theorem uniform_fold_transport (A B : SatPER) {n f g h a : T}
    (standard : UniformIter n)
    (ff : Arrow A.rel A.rel f f) (gg : Arrow B.rel B.rel g g)
    (hh : Arrow A.rel B.rel h h) (aa : A.rel a a)
    (square : Commutes A B f g h) :
    B.rel (h ⬝ (n ⬝ f ⬝ a)) (n ⬝ g ⬝ (h ⬝ a)) := by
  obtain ⟨k, count⟩ := standard
  exact B.saturated (Conv.app (.refl h) (count f a)).symm
    (count g (h ⬝ a)).symm (iter_transport A B ff gg hh aa square k)

/-- Generic algebra-morphism transport in the inherited intended model. -/
theorem fold_transport (A B : SatPER) {n f g h a : T}
    (nn : churchPER.rel n n)
    (ff : Arrow A.rel A.rel f f) (gg : Arrow B.rel B.rel g g)
    (hh : Arrow A.rel B.rel h h) (aa : A.rel a a)
    (square : Commutes A B f g h) :
    B.rel (h ⬝ (n ⬝ f ⬝ a)) (n ⬝ g ⬝ (h ⬝ a)) :=
  uniform_fold_transport A B (OpenTermStandardness.church_standard n nn) ff gg hh aa square

/-- Cross-input version. Only the LEFT supported square is assumed; Church
    relatedness transports the right fold, so no equality of extracted counts
    and no diagonal-only replacement of PER arrows is smuggled in. -/
theorem fold_transport_related (A B : SatPER) {n m f f' g g' h h' a a' : T}
    (nm : churchPER.rel n m)
    (ff' : Arrow A.rel A.rel f f') (gg' : Arrow B.rel B.rel g g')
    (hh' : Arrow A.rel B.rel h h') (aa' : A.rel a a')
    (square : Commutes A B f g h) :
    B.rel (h ⬝ (n ⬝ f ⬝ a)) (m ⬝ g' ⬝ (h' ⬝ a')) := by
  have nn := churchPER.trans nm (churchPER.symm nm)
  have ff := (arrowPER A A).trans ff' ((arrowPER A A).symm ff')
  have gg := (arrowPER B B).trans gg' ((arrowPER B B).symm gg')
  have hh := (arrowPER A B).trans hh' ((arrowPER A B).symm hh')
  have aa := A.trans aa' (A.symm aa')
  exact B.trans (fold_transport A B nn ff gg hh aa square)
    (nm B g g' gg' (h ⬝ a) (h' ⬝ a') (hh' a a' aa'))

#print axioms iter_transport
#print axioms uniform_fold_transport
#print axioms fold_transport
#print axioms fold_transport_related
end GenericFoldTransport
