import ScalarFusionCore

namespace P01AC.ExtensionalRepair.ExactScalarFusion
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

def V (k : Poly) : Ty := .all (.pi End (.pi A (Leaf k)))
def V2 (k : Poly) : Ty := .pi End (.pi A (Leaf k))
def V1 (k : Poly) : Ty := .pi A (Leaf k)

theorem V_form {k : Poly} (hk : Has [] k T) : Form [N, W k] (V k) := by
  have hw := W_form hk .nil
  have hΓ : Ctx [W k] := .ext .nil hw
  have hn : Ctx [N, W k] := .ext hΓ (N_form hΓ)
  apply Form.all hn
  change Form [N, W k] (V2 k)
  exact .pi (End_form hn) (.pi (A_form (.ext hn (End_form hn)))
    (scalar_leaf_form hΓ (closed_has_T hk (scalar_context hΓ))))

theorem V2_form {k : Poly} (hk : Has [] k T) : Form [N, W k] (V2 k) := by
  have h := V_form hk
  cases h with
  | all _ hb => exact hb

theorem V1_form {k : Poly} (hk : Has [] k T) : Form [End, N, W k] (V1 k) := by
  have h := V2_form hk
  cases h with
  | pi _ hb => exact hb

theorem Leaf_form {k : Poly} (hk : Has [] k T) : Form [A, End, N, W k] (Leaf k) := by
  have h := V1_form hk
  cases h with
  | pi _ hb => exact hb

/-- Eliminate the locally assumed w. No supplied HasE proof is weakened. -/
theorem local_scalar {k : Poly} (hk : Has [] k T) :
    Has [A, End, N, W k] (.app (.app (.app (.var 3) (.var 2)) (.var 1)) (.var 0)) (Leaf k) := by
  have hs := has_scoped hk
  have hW := W_form hk .nil
  have h0 : Ctx [W k] := .ext .nil hW
  have hN := N_form h0
  have h1 : Ctx [N, W k] := .ext h0 hN
  have hE := End_form h1
  have h2 : Ctx [End, N, W k] := .ext h1 hE
  have hA := A_form h2
  have h3 : Ctx [A, End, N, W k] := .ext h2 hA
  have hw : Has [N, W k] (.var 1) (W k) := .var (W_form hk h1) (by
    simpa only [wk, W_subst hs] using (Lookup.succ (Lookup.zero (A := W k) (Γ := [])) (B := N)))
  have hn : Has [N, W k] (.var 0) N := .var (N_form h1) .zero
  have hv : inst (V k) (.var 0) = V k := by
    simp [V, Leaf, scalarL, scalarR, End, A, arr, inst, wk, subst, psub, pup, pren, P01F.cons, psub_closed hs]
  have hwn : Has [N, W k] (.app (.var 1) (.var 0)) (V k) := by
    have h := Has.piElim (B := V k) (W_form hk h1) (by rw [hv]; exact V_form hk) hw hn
    simpa only [hv] using h
  have ht : tinst (V2 k) A = V2 k := by
    simp [V2, V1, Leaf, scalarL, scalarR, A, End, arr, tinst, tsubst, mixed, wk, subst, psub, pup, pren, P01F.cons, psub_closed hs]
  have hwnt : Has [N, W k] (.app (.var 1) (.var 0)) (V2 k) := by
    have h := Has.allElim (B := V2 k) (V_form hk) (A_form h1) (by rw [ht]; exact V2_form hk) hwn
    simpa only [ht] using h
  have hf : Has [End, N, W k] (.var 0) End := .var (End_form h2) .zero
  have hwnt' := has_wk hwnt h1 hE
  have hff : Form [End, N, W k] (wk (V2 k)) := has_form hwnt'
  have hfi : inst (subst (pup (fun n => Poly.var (n+1))) (V1 k)) (.var 0) = V1 k := by
    simp [V1, Leaf, scalarL, scalarR, End, A, arr, inst, wk, subst, psub, pup, pren, P01F.cons, psub_closed hs]
  have hwnf : Has [End, N, W k] (.app (.app (.var 2) (.var 1)) (.var 0)) (V1 k) := by
    have h := Has.piElim (B := subst (pup (fun n => Poly.var (n+1))) (V1 k)) hff (by rw [hfi]; exact V1_form hk) hwnt' hf
    simpa only [hfi, pren, psub] using h
  have ha : Has [A, End, N, W k] (.var 0) A := .var (A_form h3) .zero
  have hwnf' := has_wk hwnf h2 hA
  have hai : inst (subst (pup (fun n => Poly.var (n+1))) (Leaf k)) (.var 0) = Leaf k := by
    simp [Leaf, scalarL, scalarR, End, A, arr, inst, wk, subst, psub, pup, pren, P01F.cons, psub_closed hs]
  have h := Has.piElim (has_form hwnf') (by rw [hai]; exact Leaf_form hk) hwnf' ha
  simpa only [hai, pren, psub] using h

/-- Convenience wrapper which supplies every unchanged piExt premise. -/
theorem ext_arr {Γ : Tel} {D C : Ty} {p q h : Poly}
    (hp : Has Γ p (arr D C)) (hq : Has Γ q (arr D C))
    (hf : Form Γ (.pi D (.identity (wk C) (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0)))))
    (he : HasE Γ h (.pi D (.identity (wk C) (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))))) (hs : Scoped Γ.length h) :
    HasE Γ i (.identity (arr D C) p q) := by
  have hpF := has_form hp
  have hD : Form Γ D := by cases hpF with | pi hd _ => exact hd
  have hC : Form (D :: Γ) (wk C) := by cases hpF with | pi _ hc => exact hc
  have hleaf : Form (D :: Γ) (.identity (wk C) (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))) := by cases hf with | pi _ hb => exact hb
  exact .piExt (form_inclusion hD) (form_inclusion hC) (form_inclusion hpF)
    (has_inclusion hp) (has_inclusion hq) (form_inclusion hleaf) (form_inclusion hf)
    he (form_inclusion (.identity hpF hp hq)) (has_scoped hp) (has_scoped hq) hs
    (form_scoped hD) (form_scoped hC)

def PointA (k : Poly) : Ty := .identity End (.app (.var 1) (.var 0))
  (.app (.app k (.var 1)) (.var 0))
def PointN (k : Poly) : Ty := .identity N (.var 0) (.app k (.var 0))

theorem local_End_endpoints {k : Poly} (hk : Has [] k T) :
    Has [End, N, W k] (.app (.var 1) (.var 0)) End ∧
    Has [End, N, W k] (.app (.app k (.var 1)) (.var 0)) End := by
  have hW := W_form hk .nil
  have h0 : Ctx [W k] := .ext .nil hW
  have h1 : Ctx [N, W k] := .ext h0 (N_form h0)
  have hc : Ctx [End, N, W k] := .ext h1 (End_form h1)
  have hn : Has [End, N, W k] (.var 1) N := .var (N_form hc) (.succ .zero)
  have hf : Has [End, N, W k] (.var 0) End := .var (End_form hc) .zero
  have he := End_form hc
  have ninst : Has [End, N, W k] (.var 1) (arr End End) :=
    .allElim (N_form hc) (A_form hc) (form_arr he he) hn
  have hkn := app_has (T_form hc) (N_form hc) (closed_has_T hk hc) hn
  have kninst : Has [End, N, W k] (.app k (.var 1)) (arr End End) :=
    .allElim (N_form hc) (A_form hc) (form_arr he he) hkn
  exact ⟨app_has (form_arr he he) he ninst hf, app_has (form_arr he he) he kninst hf⟩

theorem local_End_identity {k : Poly} (hk : Has [] k T) :
    HasE [End, N, W k] i (PointA k) := by
  obtain ⟨hp, hq⟩ := local_End_endpoints hk
  have hs := has_scoped hk
  have eqLeaf : .identity (wk A)
      (.app (pren Nat.succ (.app (.var 1) (.var 0))) (.var 0))
      (.app (pren Nat.succ (.app (.app k (.var 1)) (.var 0))) (.var 0)) = Leaf k := by
    simp [Leaf, scalarL, scalarR, A, wk, subst, pren, psub, psub_closed hs]
  have hf : Form [End, N, W k] (.pi A (.identity (wk A)
      (.app (pren Nat.succ (.app (.var 1) (.var 0))) (.var 0))
      (.app (pren Nat.succ (.app (.app k (.var 1)) (.var 0))) (.var 0)))) := by
    rw [eqLeaf]; exact V1_form hk
  have he := HasE.piIntro (form_inclusion (V1_form hk)) (has_inclusion (local_scalar hk))
    (scoped_abstract (has_scoped (local_scalar hk)))
  exact ext_arr hp hq hf (by rw [eqLeaf]; exact he)
    (scoped_abstract (has_scoped (local_scalar hk)))

theorem local_N_endpoints {k : Poly} (hk : Has [] k T) :
    Has [N, W k] (.var 0) N ∧ Has [N, W k] (.app k (.var 0)) N := by
  have h0 : Ctx [W k] := .ext .nil (W_form hk .nil)
  have hc : Ctx [N, W k] := .ext h0 (N_form h0)
  have hn : Has [N, W k] (.var 0) N := .var (N_form hc) .zero
  exact ⟨hn, app_has (T_form hc) (N_form hc) (closed_has_T hk hc) hn⟩

theorem local_NBody_endpoints {k : Poly} (hk : Has [] k T) :
    Has [N, W k] (.var 0) NBody ∧ Has [N, W k] (.app k (.var 0)) NBody := by
  obtain ⟨hp, hq⟩ := local_N_endpoints hk
  have h0 : Ctx [W k] := .ext .nil (W_form hk .nil)
  have hc : Ctx [N, W k] := .ext h0 (N_form h0)
  have he := End_form hc
  exact ⟨.allElim (N_form hc) (A_form hc) (form_arr he he) hp,
    .allElim (N_form hc) (A_form hc) (form_arr he he) hq⟩

theorem PointA_form {k : Poly} (hk : Has [] k T) : Form [End, N, W k] (PointA k) := by
  obtain ⟨hp, hq⟩ := local_End_endpoints hk
  exact .identity (has_form hp) hp hq

theorem local_NBody_identity {k : Poly} (hk : Has [] k T) :
    HasE [N, W k] i (.identity NBody (.var 0) (.app k (.var 0))) := by
  obtain ⟨hp, hq⟩ := local_NBody_endpoints hk
  have hs := has_scoped hk
  have h0 : Ctx [W k] := .ext .nil (W_form hk .nil)
  have hc : Ctx [N, W k] := .ext h0 (N_form h0)
  have eqBody : .identity (wk End) (.app (pren Nat.succ (.var 0)) (.var 0))
      (.app (pren Nat.succ (.app k (.var 0))) (.var 0)) = PointA k := by
    simp [PointA, End, A, arr, wk, subst, pren, psub, psub_closed hs]
  have hf : Form [N, W k] (.pi End (PointA k)) := .pi (End_form hc) (PointA_form hk)
  have he := HasE.piIntro (form_inclusion hf) (local_End_identity hk) (scoped_abstract trivial)
  exact ext_arr (D := End) (C := End) (h := abstract i) hp hq (by rw [eqBody]; exact hf) (by rw [eqBody]; exact he) (scoped_abstract trivial)

theorem PointN_form {k : Poly} (hk : Has [] k T) : Form [N, W k] (PointN k) := by
  obtain ⟨hp, hq⟩ := local_N_endpoints hk
  exact .identity (has_form hp) hp hq

theorem local_N_identity {k : Poly} (hk : Has [] k T) : HasE [N, W k] i (PointN k) := by
  obtain ⟨hp, hq⟩ := local_N_endpoints hk
  obtain ⟨hpb, hqb⟩ := local_NBody_endpoints hk
  exact .allExt (form_inclusion (has_form hpb)) (form_inclusion (has_form hp))
    (has_inclusion hp) (has_inclusion hq)
    (form_inclusion (.identity (has_form hpb) hpb hqb)) (local_NBody_identity hk)
    (form_inclusion (PointN_form hk)) (has_scoped hp) (has_scoped hq) trivial
    (form_scoped (has_form hpb))

def OuterPoint (k : Poly) : Ty := .identity N (.app i (.var 0)) (.app k (.var 0))
def PM : Ty := .identity N (.app i (.var 2)) (.var 1)
def B (k : Poly) : Ty := .identity T i k

theorem B_subst {k : Poly} (hs : Scoped 0 k) (σ : Nat → Poly) : subst σ (B k) = B k := by
  simp [B, T, i, N, NBody, arr, wk, subst, psub_closed hs, psub]

theorem B_form {k : Poly} (hk : Has [] k T) {Γ : Tel} (hΓ : Ctx Γ) : Form Γ (B k) :=
  .identity (T_form hΓ) (i_T hΓ) (closed_has_T hk hΓ)

theorem OuterPoint_form {k : Poly} (hk : Has [] k T) : Form [N, W k] (OuterPoint k) := by
  obtain ⟨hp, hq⟩ := local_N_endpoints hk
  have hc := form_ctx (has_form hp)
  exact .identity (N_form hc) (app_has (T_form hc) (N_form hc) (i_T hc) hp) hq

/-- Change the left endpoint with actual J, retaining its literal motive and formations. -/
theorem local_outer_identity {k : Poly} (hk : Has [] k T) : HasE [N, W k] i (OuterPoint k) := by
  obtain ⟨hp, hq⟩ := local_N_endpoints hk
  have hc := form_ctx (has_form hp)
  have ht := ctx_theta hc (N_form hc) hp
  have hn2 : Has (theta [N, W k] N (.var 0)) (.var 2) N :=
    .var (N_form ht) (.succ (.succ .zero))
  have hy1 : Has (theta [N, W k] N (.var 0)) (.var 1) N :=
    .var (N_form ht) (.succ .zero)
  have hm : Form (theta [N, W k] N (.var 0)) PM :=
    .identity (N_form ht) (app_has (T_form ht) (N_form ht) (i_T ht) hn2) hy1
  have hleft := app_has (T_form hc) (N_form hc) (i_T hc) hp
  have baseF : Form [N, W k] (motiveAt PM (.var 0) i) :=
    .identity (N_form hc) hleft hp
  have baseH : Has [N, W k] i (motiveAt PM (.var 0) i) :=
    .identityIntro baseF hleft hp (.i (.var 0))
  have target_eq : motiveAt PM (.app k (.var 0)) i = OuterPoint k := rfl
  have targetF : Form [N, W k] (motiveAt PM (.app k (.var 0)) i) := by
    rw [target_eq]; exact OuterPoint_form hk
  have hj := HasE.j (form_inclusion (N_form hc)) (form_inclusion hm)
    (form_inclusion (PointN_form hk)) (form_inclusion baseF) (form_inclusion targetF)
    (has_inclusion hp) (has_inclusion hq) (local_N_identity hk) (has_inclusion baseH)
  rw [target_eq] at hj
  exact .conv (form_inclusion (OuterPoint_form hk)) hj (j_conversion i (.app k (.var 0)) i) trivial

theorem local_closed_identity {k : Poly} (hk : Has [] k T) : HasE [W k] i (B k) := by
  have hc : Ctx [W k] := .ext .nil (W_form hk .nil)
  have hp := i_T hc
  have hq := closed_has_T hk hc
  have hs := has_scoped hk
  have eqPoint : .identity (wk N) (.app (pren Nat.succ i) (.var 0))
      (.app (pren Nat.succ k) (.var 0)) = OuterPoint k := by
    simp [OuterPoint, N, NBody, arr, wk, subst, pren_closed hs, psub_closed hs, i, pren, psub]
  have hf : Form [W k] (.pi N (OuterPoint k)) := .pi (N_form hc) (OuterPoint_form hk)
  have he := HasE.piIntro (form_inclusion hf) (local_outer_identity hk) (scoped_abstract trivial)
  exact ext_arr (D := N) (C := N) (h := abstract i) hp hq
    (by rw [eqPoint]; exact hf) (by rw [eqPoint]; exact he) (scoped_abstract trivial)

/-- Close under w first, apply the supplied closed witness only afterward. -/
theorem reverse_fixed {k h : Poly} (hk : Has [] k T) (hh : HasE [] h (W k)) :
    HasE [] i (B k) := by
  have hc : Ctx [W k] := .ext .nil (W_form hk .nil)
  have hf : Form [] (.pi (W k) (B k)) := .pi (W_form hk .nil) (B_form hk hc)
  have hfun : HasE [] (abstract i) (.pi (W k) (B k)) :=
    .piIntro (form_inclusion hf) (local_closed_identity hk) (scoped_abstract trivial)
  have hi : inst (B k) h = B k := B_subst (has_scoped hk) _
  have happ := HasE.piElim (form_inclusion hf)
    (by rw [hi]; exact form_inclusion (B_form hk .nil)) hfun hh
  rw [hi] at happ
  exact .conv (form_inclusion (B_form hk .nil)) happ (by simpa [i, abstract, freeZero, drop, pren, psub] using (PolyConvPlus.k i h)) trivial

/-- Four precise propositions, with no claimed inhabitant of any of them. -/
theorem generic_four_way_iff {k : Poly} (hk : Has [] k T) :
    ((∃ r, HasE [] r (B k)) ↔ HasE [] i (B k)) ∧
    ((∃ r, HasE [] r (B k)) ↔ ∃ h, HasE [] h (W k)) ∧
    ((∃ r, HasE [] r (B k)) ↔ HasE [] c3 (W k)) := by
  have toW : (∃ r, HasE [] r (B k)) → HasE [] c3 (W k) := by
    rintro ⟨r, hr⟩; exact forward_fixed hk hr
  have toB : (∃ h, HasE [] h (W k)) → HasE [] i (B k) := by
    rintro ⟨h, hh⟩; exact reverse_fixed hk hh
  exact ⟨⟨fun h => toB ⟨c3, toW h⟩, fun h => ⟨i, h⟩⟩,
    ⟨fun h => ⟨c3, toW h⟩, fun h => ⟨i, toB h⟩⟩,
    ⟨toW, fun h => ⟨i, reverse_fixed hk h⟩⟩⟩

end P01AC.ExtensionalRepair.ExactScalarFusion
