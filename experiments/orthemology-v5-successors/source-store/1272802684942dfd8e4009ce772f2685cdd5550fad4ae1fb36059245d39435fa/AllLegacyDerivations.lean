/- Whole retained-typing-tree support and exact polynomial translation, including All. -/
import AllLegacySyntax
namespace P01AC.Legacy
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Every displayed term and type is scoped at its actual term-binder depth.
Implicit replacements and J motives are checked explicitly. Conversion certificates
are unchanged: their displayed endpoints are checked, never hidden proof history. -/
def Supported {p : Poly} {A : P01DF.Ty} (n : Nat) (h : Derivation p A) : Prop :=
  Scoped n p ∧ TypeSupported n A ∧
  match h with
  | .raw _ | .finite _ | .i _ | .k _ _ | .s _ _ _ | .identityIntro _ => True
  | .allIntro hb => Supported n hb
  | @P01TC.Legacy.Derivation.allElim _ _ A hb => TypeSupported n A ∧ Supported n hb
  | .app hf ha => Supported n hf ∧ Supported n ha
  | .piIntro hb => Supported (n+1) hb
  | @P01TC.Legacy.Derivation.piElim _ a B hf =>
      TypeSupported (n+1) B ∧ Scoped n a ∧ Supported n hf
  | @P01TC.Legacy.Derivation.sigmaIntro a _ B hb =>
      TypeSupported (n+1) B ∧ Scoped n a ∧ Supported n hb
  | @P01TC.Legacy.Derivation.sigmaSnd _ B hz => TypeSupported (n+1) B ∧ Supported n hz
  | @P01TC.Legacy.Derivation.j x y _ _ B he hd =>
      TypeSupported (n+2) B ∧ Scoped n x ∧ Scoped n y ∧ Supported n he ∧ Supported n hd
  | .conv hp _ => Supported n hp

theorem Supported.scoped {n p A} {h : Derivation p A} (hs : Supported n h) : Scoped n p := by
  cases h <;> exact hs.1

theorem Supported.type {n p A} {h : Derivation p A} (hs : Supported n h) : TypeSupported n A := by
  cases h <;> exact hs.2.1

theorem Supported.formed {n p A} {h : Derivation p A} (hs : Supported n h)
    {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n) : Form Γ (translate A) := hs.type.form hΓ hlen

/-- Every old rule translates with exactly the indexed old polynomial.
No Prop-to-Type reification and no reconstruction of finite atoms is used. -/
theorem supported_embed {p : Poly} {A : P01DF.Ty} (h : Derivation p A) :
    ∀ n, Supported n h → ∀ Γ, RawContext Γ → Γ.length = n → Has Γ p (translate A) := by
  induction h with
  | raw p =>
      intro n hs Γ hΓ hlen
      exact raw_term hΓ (by simpa only [hlen] using hs.scoped)
  | finite ht =>
      intro n hs Γ hΓ hlen
      rw [translate_finite]
      exact finite_import hΓ.ctx ht
  | i A =>
      intro n hs Γ hΓ hlen
      exact .i (hs.type.1.form hΓ hlen) (hs.formed hΓ hlen)
  | k A B =>
      intro n hs Γ hΓ hlen
      exact .k (hs.type.1.form hΓ hlen) (hs.type.2.1.form hΓ hlen) (hs.formed hΓ hlen)
  | s A B C =>
      intro n hs Γ hΓ hlen
      exact .s (hs.type.1.1.form hΓ hlen) (hs.type.1.2.1.form hΓ hlen)
        (hs.type.1.2.2.form hΓ hlen) (hs.formed hΓ hlen)
  | allIntro hb ih =>
      intro n hs Γ hΓ hlen
      exact .allIntro (hs.formed hΓ hlen)
        (ih n hs.2.2 (twkTel Γ) hΓ.twk (by simpa only [twkTel,List.length_map] using hlen))
  | allElim hb ih =>
      intro n hs Γ hΓ hlen
      rw [translate_tinst]
      exact .allElim (hs.2.2.2.formed hΓ hlen) (hs.2.2.1.form hΓ hlen)
        (by simpa only [translate_tinst] using hs.formed hΓ hlen)
        (ih n hs.2.2.2 Γ hΓ hlen)
  | app hf ha iff ia =>
      intro n hs Γ hΓ hlen
      have hf' := iff n hs.2.2.1 Γ hΓ hlen
      have ha' := ia n hs.2.2.2 Γ hΓ hlen
      simpa only [inst_wk] using Has.piElim (has_form hf')
        (by simpa only [inst_wk] using hs.formed hΓ hlen) hf' ha'
  | piIntro hb ih =>
      intro n hs Γ hΓ hlen
      exact .piIntro (hs.formed hΓ hlen)
        (ih (n+1) hs.2.2 (.raw :: Γ) hΓ.ext (congrArg Nat.succ hlen))
        (by simpa only [hlen] using hs.scoped)
  | piElim hf ih =>
      intro n hs Γ hΓ hlen
      rw [translate_inst]
      have hf' := ih n hs.2.2.2.2 Γ hΓ hlen
      exact .piElim (has_form hf')
        (by simpa only [translate_inst] using hs.formed hΓ hlen) hf'
        (raw_term hΓ (by simpa only [hlen] using hs.2.2.2.1))
  | sigmaIntro hb ih =>
      intro n hs Γ hΓ hlen
      have hb' := ih n hs.2.2.2.2 Γ hΓ hlen
      simp only [translate_inst] at hb'
      exact .sigmaIntro (hs.formed hΓ hlen) (has_form hb')
        (raw_term hΓ (by simpa only [hlen] using hs.2.2.2.1)) hb'
  | sigmaSnd hz ih =>
      intro n hs Γ hΓ hlen
      rw [translate_inst]
      have hz' := ih n hs.2.2.2 Γ hΓ hlen
      exact .sigmaSnd (has_form hz')
        (by simpa only [translate_inst] using hs.formed hΓ hlen) hz'
  | identityIntro hc =>
      intro n hs Γ hΓ hlen
      exact .identityIntro (hs.formed hΓ hlen)
        (raw_term hΓ (by simpa only [hlen] using hs.type.1))
        (raw_term hΓ (by simpa only [hlen] using hs.type.2)) hc
  | @j x y e d B he hd ihe ihd =>
      intro n hs Γ hΓ hlen
      have hB := hs.2.2.1
      have hx := hs.2.2.2.1
      have hy := hs.2.2.2.2.1
      have he' := ihe n hs.2.2.2.2.2.1 Γ hΓ hlen
      have hd' := ihd n hs.2.2.2.2.2.2 Γ hΓ hlen
      rw [translate_motiveAt]
      simp only [translate_motiveAt] at hd'
      exact .j (.raw hΓ.ctx)
        (hB.theta_form hΓ hlen (by simpa only [hlen] using hx))
        (has_form he') (has_form hd')
        (by simpa only [translate_motiveAt] using hs.formed hΓ hlen)
        (raw_term hΓ (by simpa only [hlen] using hx))
        (raw_term hΓ (by simpa only [hlen] using hy)) he' hd'
  | conv hp hc ih =>
      intro n hs Γ hΓ hlen
      exact .conv (hs.formed hΓ hlen) (ih n hs.2.2 Γ hΓ hlen) hc
        (by simpa only [hlen] using hs.scoped)

theorem Supported.embed {n p A} {h : Derivation p A} (hs : Supported n h)
    {Γ : Tel} (hΓ : RawContext Γ) (hlen : Γ.length = n) : Has Γ p (translate A) :=
  supported_embed h n hs Γ hΓ hlen

theorem Supported.raw_embed {n p A} {h : Derivation p A} (hs : Supported n h) :
    Has (rawTel n) p (translate A) := hs.embed (rawTel_context n) (rawTel_length n)

theorem Supported.old_judgment {n p A} {h : Derivation p A} (_hs : Supported n h) : P01DF.Has p A := erase h

/-- The newly included All introduction tree retains the old exact source I. -/
def identityTree : Derivation (.atom .i) (.all (.arrow (.param 0) (.param 0))) :=
  .allIntro (.i (.param 0))

theorem identityTree_supported (n : Nat) : Supported n identityTree := by
  simp only [identityTree,Supported,TypeSupported,Scoped,and_self]

/-- A genuinely open, term-dependent old replacement, not just a finite type image. -/
def openIdentityInstance : Derivation (.atom .i)
    (P01DF.instantiateType (.arrow (.param 0) (.param 0)) (.identity (.var 0) (.atom .i))) :=
  .allElim identityTree

theorem openIdentityInstance_supported : Supported 1 openIdentityInstance := by
  simp [openIdentityInstance,Supported,TypeSupported,P01DF.instantiateType,
    P01DF.substType,P01F.cons,Scoped,identityTree]

/-- The exact inherited non-finite dependent-All type, with its retained old tree. -/
def dependentTree : Derivation (abstract (.atom .k)) P01DF.dependentPolyType :=
  .allIntro (.piIntro (.k (.param 0) P01DF.anchoredIdentity))

theorem dependentTree_supported : Supported 0 dependentTree := by
  simp [dependentTree,Supported,TypeSupported,P01DF.dependentPolyType,
    P01DF.dependentPolyBody,P01DF.anchoredIdentity,Scoped,abstract,freeZero,drop,pren,psub]

theorem dependent_polymorphic_typed :
    Has [] (abstract (.atom .k)) (translate P01DF.dependentPolyType) :=
  dependentTree_supported.raw_embed

def dependentSelfTree : Derivation (abstract (.atom .k))
    (P01DF.instantiateType P01DF.dependentPolyBody P01DF.dependentPolyType) :=
  .allElim dependentTree

theorem dependentSelfTree_supported : Supported 0 dependentSelfTree := by
  simp [dependentSelfTree,dependentTree,Supported,TypeSupported,P01DF.instantiateType,
    P01DF.substType,P01DF.liftIndices,P01DF.substIndex,P01DF.liftTypes,
    P01DF.renameType,P01DF.dependentPolyType,P01DF.dependentPolyBody,
    P01DF.anchoredIdentity,P01F.cons,Scoped,abstract,freeZero,drop,psub,pren,pup]

theorem dependent_polymorphic_self_typed :
    Has [] (abstract (.atom .k))
      (tinst (translate P01DF.dependentPolyBody) (translate P01DF.dependentPolyType)) := by
  simpa only [translate_tinst] using dependentSelfTree_supported.raw_embed

end P01AC.Legacy
