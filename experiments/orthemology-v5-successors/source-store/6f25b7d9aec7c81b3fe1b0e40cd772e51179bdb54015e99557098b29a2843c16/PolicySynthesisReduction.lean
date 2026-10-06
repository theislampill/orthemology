import SkeletonUnion

/-! Actual code-level source and target maps. No hierarchy class is defined by
reference to this construction, and no source-program totality is assumed. -/
namespace PolicySynthesis
open EffectiveRenewal
open Nat.Partrec (Code)
open Encodable Denumerable

abbrev Matrix := Nat × Nat × Nat × Nat → Bool

def matrixSearch (R : Matrix) (n : Nat) : Part Nat :=
  Nat.rfindOpt fun z => if R (n.unpair.1, n.unpair.2.unpair.1, n.unpair.2.unpair.2, z) = true
    then some 0 else none

theorem matrixSearch_partrec (R : Matrix) (hR : Computable R) : Partrec (matrixSearch R) := by
  have harg : Computable fun a : Nat × Nat =>
      (a.1.unpair.1, a.1.unpair.2.unpair.1, a.1.unpair.2.unpair.2, a.2) :=
    ((Computable.fst.comp (Primrec.unpair.to_comp.comp Computable.fst))).pair
      (((Computable.fst.comp (Primrec.unpair.to_comp.comp
        (Computable.snd.comp (Primrec.unpair.to_comp.comp Computable.fst))))).pair
        ((Computable.snd.comp (Primrec.unpair.to_comp.comp
          (Computable.snd.comp (Primrec.unpair.to_comp.comp Computable.fst)))).pair Computable.snd))
  have htest : Computable fun a : Nat × Nat =>
      if R (a.1.unpair.1, a.1.unpair.2.unpair.1, a.1.unpair.2.unpair.2, a.2) = true
        then some 0 else none := by
    apply (Computable.cond (hR.comp harg) (Computable.const (some 0)) (Computable.const none)).of_eq
    intro a
    cases hb : R (a.1.unpair.1, a.1.unpair.2.unpair.1, a.1.unpair.2.unpair.2, a.2) <;> simp [hb]
  exact Partrec.rfindOpt htest.to₂

theorem matrixSearch_dom (R : Matrix) (n : Nat) : (matrixSearch R n).Dom ↔
    ∃ z, R (n.unpair.1, n.unpair.2.unpair.1, n.unpair.2.unpair.2, z) = true := by
  rw [matrixSearch, Nat.rfindOpt_dom]
  constructor
  · rintro ⟨z,v,hv⟩
    by_cases hz : R (n.unpair.1, n.unpair.2.unpair.1, n.unpair.2.unpair.2, z) = true
    · exact ⟨z,hz⟩
    · simp [hz] at hv
  · rintro ⟨z,hz⟩
    exact ⟨z,0, by simp [hz]⟩

theorem matrixSearch_dom_pair (R : Matrix) (a x y : Nat) :
    (matrixSearch R (Nat.pair a (Nat.pair x y))).Dom ↔ ∃ z, R (a,x,y,z) = true := by
  simp [matrixSearch_dom, Nat.unpair_pair]

def specializeIndex (c : Code) (a : Nat) : Nat := encode (Code.curry c a)

theorem specializeIndex_primrec (c : Code) : Primrec (specializeIndex c) :=
  Primrec.encode.comp (Code.curry_prim.comp (Primrec.const c) Primrec.id)

@[simp] theorem specializeIndex_eval (c : Code) (a n : Nat) :
    Code.eval (ofNat Code (specializeIndex c a)) n = Code.eval c (Nat.pair a n) := by
  simp [specializeIndex, Code.eval_curry]

theorem source_search_code_equations (R : Matrix) (hR : Computable R) :
    ∃ c : Code, ∀ a n,
      Code.eval (ofNat Code (specializeIndex c a)) n = matrixSearch R (Nat.pair a n) := by
  obtain ⟨c,hc⟩ := Code.exists_code.mp (Partrec.nat_iff.mp (matrixSearch_partrec R hR))
  refine ⟨c, ?_⟩
  intro a n
  rw [specializeIndex_eval, hc]

theorem source_search_code (R : Matrix) (hR : Computable R) :
    ∃ c : Code, ∀ a x y,
      (Code.eval (ofNat Code (specializeIndex c a)) (Nat.pair x y)).Dom ↔
        ∃ z, R (a,x,y,z) = true := by
  obtain ⟨c,hc⟩ := source_search_code_equations R hR
  refine ⟨c, ?_⟩
  intro a x y
  rw [hc]
  exact matrixSearch_dom_pair R a x y

theorem computable_matrix_reduction (R : Matrix) (hR : Computable R) :
    ∃ r : Nat → Nat, Primrec r ∧ ∀ a,
      (∃ x, ∀ y, ∃ z, R (a,x,y,z) = true) ↔ HasComputablePath (synthesisTree (r a)) := by
  obtain ⟨c,hc⟩ := source_search_code R hR
  refine ⟨specializeIndex c, specializeIndex_primrec c, ?_⟩
  intro a
  rw [synthesis_computablePath_iff]
  constructor
  · rintro ⟨x,hx⟩
    exact ⟨x, fun y => (hc a x y).mpr (hx y)⟩
  · rintro ⟨x,hx⟩
    exact ⟨x, fun y => (hc a x y).mp (hx y)⟩

/-! Total Boolean tree code. Malformed finite-word numbers decode to the empty
word. This convention is total and does not alter correctly encoded words. -/
def natChecker (p n : Nat) : Nat :=
  bitNat (synthesisCheck p ((decode (α := Word) n).getD []))

theorem natChecker_primrec : Primrec₂ natChecker :=
  bitNat_primrec.comp (synthesisCheck_primrec.comp Primrec.fst
    (Primrec.option_getD.comp (Primrec.decode.comp Primrec.snd) (Primrec.const [])))

@[simp] theorem natChecker_encode (p : Nat) (w : Word) :
    natChecker p (encode w) = bitNat (synthesisCheck p w) := by simp [natChecker]

theorem total_checker_code_family :
    ∃ e : Nat → Nat, Primrec e ∧ ∀ p n,
      Code.eval (ofNat Code (e p)) n = Part.some (natChecker p n) := by
  have hc : Computable fun n : Nat => natChecker n.unpair.1 n.unpair.2 :=
    (natChecker_primrec.comp (Primrec.fst.comp Primrec.unpair)
      (Primrec.snd.comp Primrec.unpair)).to_comp
  obtain ⟨c,hc⟩ := Code.exists_code.mp (Partrec.nat_iff.mp hc.partrec)
  refine ⟨specializeIndex c, specializeIndex_primrec c, ?_⟩
  intro p n
  rw [specializeIndex_eval, hc]
  simp [Nat.unpair_pair]

def codeAccepts (e : Nat) (w : Word) : Prop :=
  1 ∈ Code.eval (ofNat Code e) (encode w)

def validTreeCode (e : Nat) : Prop :=
  (∀ n, ∃ b : Bool, Code.eval (ofNat Code e) n = Part.some (bitNat b)) ∧
    codeAccepts e [] ∧ PrefixClosed (codeAccepts e)

def policyCodeIndex (e : Nat) : Prop := validTreeCode e ∧ HasComputablePath (codeAccepts e)

theorem checker_code_accepts {e : Nat → Nat}
    (he : ∀ p n, Code.eval (ofNat Code (e p)) n = Part.some (natChecker p n))
    (p : Nat) (w : Word) : codeAccepts (e p) w ↔ synthesisTree p w := by
  rw [codeAccepts, he, natChecker_encode]
  change (1 ∈ Part.some (bitNat (synthesisCheck p w))) ↔ synthesisCheck p w = true
  cases hb : synthesisCheck p w <;> simp [bitNat]

theorem checker_code_valid {e : Nat → Nat}
    (he : ∀ p n, Code.eval (ofNat Code (e p)) n = Part.some (natChecker p n)) (p : Nat) :
    validTreeCode (e p) := by
  refine ⟨?_, (checker_code_accepts he p []).mpr (synthesisTree_empty p), ?_⟩
  · intro n
    exact ⟨synthesisCheck p ((decode (α := Word) n).getD []), he p n⟩
  · intro s t hp ht
    exact (checker_code_accepts he p s).mpr
      (synthesis_prefix_closed p hp ((checker_code_accepts he p t).mp ht))

theorem checker_code_path_iff {e : Nat → Nat}
    (he : ∀ p n, Code.eval (ofNat Code (e p)) n = Part.some (natChecker p n)) (p : Nat) :
    policyCodeIndex (e p) ↔ HasComputablePath (synthesisTree p) := by
  constructor
  · rintro ⟨hv,f,hf,hp⟩
    exact ⟨f,hf,fun n => (checker_code_accepts he p _).mp (hp n)⟩
  · rintro ⟨f,hf,hp⟩
    exact ⟨checker_code_valid he p, f,hf,fun n => (checker_code_accepts he p _).mpr (hp n)⟩

/-- The exact constructive lower bound, with a primitive-recursive many-one
map into ordinary total Boolean tree-decider indices. Every output tree is
mathematically infinite, including at negative source instances. -/
theorem policy_synthesis_reduction (R : Matrix) (hR : Computable R) :
    ∃ r : Nat → Nat, Primrec r ∧ ∀ a,
      validTreeCode (r a) ∧
      (∃ f : Nat → Bool, ∀ n, codeAccepts (r a) (prefixWord f n)) ∧
      ((∃ x, ∀ y, ∃ z, R (a,x,y,z) = true) ↔ policyCodeIndex (r a)) := by
  obtain ⟨source,hsource,hRsource⟩ := computable_matrix_reduction R hR
  obtain ⟨target,htarget,heval⟩ := total_checker_code_family
  refine ⟨fun a => target (source a), htarget.comp hsource, ?_⟩
  intro a
  refine ⟨checker_code_valid heval _, ?_, ?_⟩
  · obtain ⟨f,hf⟩ := synthesis_mathematical_path (source a)
    exact ⟨f,fun n => (checker_code_accepts heval _ _).mpr (hf n)⟩
  · exact (hRsource a).trans (checker_code_path_iff heval (source a)).symm

end PolicySynthesis
