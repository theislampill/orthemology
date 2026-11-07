/- Proposed type-relative PER layer. Raw Conv and canonical Code are unchanged.
   New complete authored proof bodies, UNCOMPILED at Lean 4.19.0. -/
import P01Polynomials
namespace P01D
open OrthemologyV2 OrthemologyV3

structure PER where
  rel : Term → Term → Prop
  sym : ∀ {a b}, rel a b → rel b a
  trans : ∀ {a b c}, rel a b → rel b c → rel a c
  raw : ∀ {a b a' b'}, Conv a a' → Conv b b' → rel a b → rel a' b'

def PER.dom (P : PER) (a) := P.rel a a

theorem PER.left {P : PER} {a b} (h : P.rel a b) : P.dom a := P.trans h (P.sym h)
theorem PER.right {P : PER} {a b} (h : P.rel a b) : P.dom b := P.trans (P.sym h) h

@[ext] theorem per_ext {P Q : PER} (h : ∀a b, P.rel a b ↔ Q.rel a b) : P = Q := by
  have e : P.rel = Q.rel := funext fun a => funext fun b => propext (h a b)
  cases P; cases Q; cases e; rfl

def botPER : PER where
  rel := fun _ _ => False
  sym := id
  trans := fun h _ => h
  raw := fun _ _ h => h

def rawPER : PER where
  rel := Conv
  sym := Conv.symm
  trans := Conv.trans
  raw := fun h k r => .trans (.symm h) (.trans r k)

theorem conv_app {f g x y} (h : Conv f g) (k : Conv x y) :
    Conv (.app f x) (.app g y) := .trans (Conv.left h x) (Conv.right g k)

def PiPER (P : PER) (B : Term → PER)
    (coh : ∀ {x y}, P.rel x y → B x = B y) : PER where
  rel := fun f g => ∀ x y, P.rel x y → (B x).rel (.app f x) (.app g y)
  sym := by
    intro f g h x y hxy
    have e := coh hxy
    rw [e]
    exact (B y).sym (h y x (P.sym hxy))
  trans := by
    intro f g h hfg hgh x y hxy
    exact (B x).trans (hfg x x (PER.left hxy)) (hgh x y hxy)
  raw := fun hf hg h x y hxy =>
    (B x).raw (Conv.left hf x) (Conv.left hg y) (h x y hxy)

def ArrPER (P Q : PER) : PER := PiPER P (fun _ => Q) (fun _ => rfl)

/-- Relational environments carry their two endpoints explicitly. -/
structure Link (P Q : PER) where
  rel : Term → Term → Prop
  endpoints : ∀ {x y}, rel x y → P.dom x ∧ Q.dom y
  respect : ∀ {x x' y y'}, P.rel x x' → Q.rel y y' → rel x y → rel x' y'

theorem Link.raw {P Q} (R : Link P Q) {x y x' y'}
    (cx : Conv x x') (cy : Conv y y') (h : R.rel x y) : R.rel x' y' := by
  have hd := R.endpoints h
  exact R.respect (P.raw (.refl _) cx hd.1) (Q.raw (.refl _) cy hd.2) h

def diagonal (P : PER) : Link P P where
  rel := P.rel
  endpoints := fun h => ⟨PER.left h, PER.right h⟩
  respect := fun hx hy h => P.trans (P.sym hx) (P.trans h hy)

def arrowLink {P Q A B : PER} (R : Link P Q) (S : Link A B) :
    Link (ArrPER P A) (ArrPER Q B) where
  rel := fun f g => (ArrPER P A).dom f ∧ (ArrPER Q B).dom g ∧
    ∀ x y, R.rel x y → S.rel (.app f x) (.app g y)
  endpoints := fun h => ⟨h.1,h.2.1⟩
  respect := by
    intro f f' g g' hf hg h
    refine ⟨PER.right hf, PER.right hg, ?_⟩
    intro x y hxy
    have d := R.endpoints hxy
    exact S.respect (hf x x d.1) (hg y y d.2) (h.2.2 x y hxy)

theorem arrow_identity (P A : PER) (f g : Term) :
    (arrowLink (diagonal P) (diagonal A)).rel f g ↔ (ArrPER P A).rel f g := by
  constructor
  · intro h; exact h.2.2
  · intro h; exact ⟨PER.left h, PER.right h, h⟩

theorem pair_congr {x x' y y'} (hx : Conv x x') (hy : Conv y y') :
    Conv (pairTerm x y) (pairTerm x' y') := by
  unfold pairTerm
  exact conv_app (Conv.right .s (Conv.right (.app .s .i) (Conv.right .k hx)))
    (Conv.right .k hy)

def Represented (z : Term) := Conv z (pairTerm (firstTerm z) (secondTerm z))

theorem pair_represented (x y : Term) : Represented (pairTerm x y) :=
  .symm (pair_congr (pair_first x y) (pair_second x y))

theorem represented_raw {z w} (h : Conv z w) (hz : Represented z) : Represented w :=
  .trans (.symm h) (.trans hz (pair_congr (Conv.left h .k) (Conv.left h (.app .k .i))))

/-- Projection form of represented Sigma, proved equivalent to pair witnesses
    below. This is NOT the full ambient Cartesian product. -/
def SigmaPER (P : PER) (B : Term → PER)
    (coh : ∀ {x y}, P.rel x y → B x = B y) : PER where
  rel := fun z w => Represented z ∧ Represented w ∧
    P.rel (firstTerm z) (firstTerm w) ∧
    (B (firstTerm z)).rel (secondTerm z) (secondTerm w)
  sym := by
    intro z w h
    refine ⟨h.2.1,h.1,P.sym h.2.2.1,?_⟩
    rw [← coh h.2.2.1]
    exact (B (firstTerm z)).sym h.2.2.2
  trans := by
    intro z w v h k
    refine ⟨h.1,k.2.1,P.trans h.2.2.1 k.2.2.1,?_⟩
    have e := coh h.2.2.1
    exact (B (firstTerm z)).trans h.2.2.2 (e.symm ▸ k.2.2.2)
  raw := by
    intro z w z' w' hz hw h
    have fz := Conv.left hz .k
    have fw := Conv.left hw .k
    have sz := Conv.left hz (.app .k .i)
    have sw := Conv.left hw (.app .k .i)
    have e := coh (P.raw (.refl _) fz (PER.left h.2.2.1))
    refine ⟨represented_raw hz h.1,represented_raw hw h.2.1,
      P.raw fz fw h.2.2.1,?_⟩
    exact e ▸ (B (firstTerm z)).raw sz sw h.2.2.2

theorem sigma_pair {P B coh x x' y y'} (hx : P.rel x x')
    (hy : (B x).rel y y') :
    (SigmaPER P B coh).rel (pairTerm x y) (pairTerm x' y') := by
  have e := coh (P.raw (pair_first x y).symm (.refl _) (PER.left hx))
  refine ⟨pair_represented x y,pair_represented x' y',
    P.raw (pair_first x y).symm (pair_first x' y').symm hx,?_⟩
  rw [e]
  exact (B x).raw (pair_second x y).symm (pair_second x' y').symm hy

theorem sigma_witness_iff (P B coh z w) :
    (SigmaPER P B coh).rel z w ↔
    ∃x y x' y', Conv z (pairTerm x y) ∧ Conv w (pairTerm x' y') ∧
      P.rel x x' ∧ (B x).rel y y' := by
  constructor
  · intro h
    exact ⟨firstTerm z,secondTerm z,firstTerm w,secondTerm w,h.1,h.2.1,h.2.2.1,h.2.2.2⟩
  · rintro ⟨x,y,x',y',hz,hw,hx,hy⟩
    exact (SigmaPER P B coh).raw hz.symm hw.symm (sigma_pair hx hy)

theorem sigma_eta {P B coh z} (h : (SigmaPER P B coh).dom z) :
    Conv z (pairTerm (firstTerm z) (secondTerm z)) := h.1

def IdPER (P : PER) (x y : Term) : PER where
  rel := fun p q => P.rel x y ∧ Conv p .i ∧ Conv q .i
  sym := fun h => ⟨h.1,h.2.2,h.2.1⟩
  trans := fun h k => ⟨h.1,h.2.1,k.2.2⟩
  raw := fun cp cq h => ⟨h.1,.trans cp.symm h.2.1,.trans cq.symm h.2.2⟩

theorem id_intro {P x} (h : P.dom x) : (IdPER P x x).dom .i :=
  ⟨h,.refl _,.refl _⟩

/-- Motive coherence has BOTH endpoint and equality-proof coordinates. -/
structure BasedMotive (P : PER) (x : Term) where
  fibre : Term → Term → PER
  coherent : ∀ {y y' p p'}, P.rel y y' → Conv p p' →
    (IdPER P x y).dom p → (IdPER P x y').dom p' → fibre y p = fibre y' p'

theorem based_transport {P x y p d e} (M : BasedMotive P x)
    (h : (IdPER P x y).dom p) (hd : (M.fibre x .i).rel d e) :
    (M.fibre y p).rel d e := by
  have hx : P.dom x := PER.left h.1
  have e := M.coherent h.1 h.2.1.symm (id_intro hx) h
  exact e ▸ hd

def Jterm (d y p : Term) := Term.app (.app (.app .k (.app .k d)) y) p

theorem J_red (d y p : Term) : Red (Jterm d y p) d :=
  .tail (.left (.k (.app .k d) y) p) (.tail (.k d p) (.refl _))

theorem based_J {P x y p d e} (M : BasedMotive P x)
    (h : (IdPER P x y).dom p) (hd : (M.fibre x .i).rel d e) :
    (M.fibre y p).rel (Jterm d y p) (Jterm e y p) :=
  (M.fibre y p).raw (P01Source.red_conv (J_red d y p)).symm
    (P01Source.red_conv (J_red e y p)).symm (based_transport M h hd)

/-- A body interpretation at a fixed outer diagonal environment, with its
    explicit heterogeneous relations and its already-proved body IE law. -/
structure ParamFamily where
  obj : PER → PER
  link : ∀ {P Q}, Link P Q → Link (obj P) (obj Q)
  identity : ∀ P t u, (link (diagonal P)).rel t u ↔ (obj P).rel t u

def Parametric (F : ParamFamily) (t : Term) :=
  ∀ (P Q : PER) (R : Link P Q), (F.link R).rel t t

def AllPER (F : ParamFamily) : PER where
  rel := fun t u => Parametric F t ∧ Parametric F u ∧ ∀P, (F.obj P).rel t u
  sym := fun h => ⟨h.2.1,h.1,fun P => (F.obj P).sym (h.2.2 P)⟩
  trans := fun h k => ⟨h.1,k.2.1,fun P => (F.obj P).trans (h.2.2 P) (k.2.2 P)⟩
  raw := fun ct cu h => ⟨fun P Q R => (F.link R).raw ct ct (h.1 P Q R),
    fun P Q R => (F.link R).raw cu cu (h.2.1 P Q R),
    fun P => (F.obj P).raw ct cu (h.2.2 P)⟩

theorem all_domain (F : ParamFamily) (t) : (AllPER F).dom t ↔ Parametric F t := by
  constructor
  · exact fun h => h.1
  · intro h
    exact ⟨h,h,fun P => (F.identity P t t).mp (h P P (diagonal P))⟩

def AllDiagonal (F : ParamFamily) : Link (AllPER F) (AllPER F) where
  rel := fun t u => (AllPER F).dom t ∧ (AllPER F).dom u ∧
    ∀P Q (R : Link P Q), (F.link R).rel t u
  endpoints := fun h => ⟨h.1,h.2.1⟩
  respect := fun ht hu h => ⟨PER.right ht,PER.right hu,
    fun P Q R => (F.link R).respect (ht.2.2 P) (hu.2.2 Q) (h.2.2 P Q R)⟩

theorem all_identity_extension (F : ParamFamily) (t u) :
    (AllDiagonal F).rel t u ↔ (AllPER F).rel t u := by
  constructor
  · intro h
    exact ⟨h.1.1,h.2.1.1,fun P => (F.identity P t u).mp (h.2.2 P P (diagonal P))⟩
  · intro h
    refine ⟨PER.left h,PER.right h,?_⟩
    intro P Q R
    have ht := (F.link R).endpoints (h.1 P Q R)
    exact (F.link R).respect ht.1 (h.2.2 Q) (h.1 P Q R)

theorem all_eliminate {F t u} (h : (AllPER F).rel t u) (P : PER) :
    (F.obj P).rel t u := h.2.2 P

/-- Self-instantiation is literal and legal, but supplies no object-level
    universe/decoder or full-section reification. -/
theorem all_self_eliminate {F t u} (h : (AllPER F).rel t u) :
    (F.obj (AllPER F)).rel t u := h.2.2 (AllPER F)

end P01D
