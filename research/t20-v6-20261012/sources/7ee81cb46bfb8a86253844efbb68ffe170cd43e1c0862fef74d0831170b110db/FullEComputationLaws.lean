/- Additive actual-E support for the literal retained total-space construction. -/
import FullEUniformSection
namespace RigidityInitiality.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem transport_has_erased {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxE Γ) (hX : FormE Γ X) (hP : FormE (X :: Γ) P)
    (hx : HasE Γ x X) (hy : HasE Γ y X)
    (he : HasE Γ e (.identity X x y)) (hd : HasE Γ d (inst P x)) :
    HasE Γ d (inst P y) := by
  have hM : FormE (theta Γ X x) (wk P) :=
    form_wk hP (.ext hc hX) (form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v :=
    subst_wk_cancel P r (cons v Poly.var)
  have h := HasE.j hX hM (.identity hX hx hy)
    ((at_eq x (.atom .i)).symm ▸ form_inst_source hc hP hx)
    ((at_eq y e).symm ▸ form_inst_source hc hP hy) hx hy he
    ((at_eq x (.atom .i)).symm ▸ hd)
  have h' : HasE Γ (jPoly d y e) (inst P y) := by simpa only [at_eq] using h
  exact conv_raw (form_inst_source hc hP hy) h'
    ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)) (has_scoped hd)


theorem dependent_apply_has {Γ : Tel} {P Q : Ty} {s x d : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hQ : FormE (N :: Γ) Q)
    (hs : HasE Γ s (.pi N (arr P Q))) (hx : HasE Γ x N)
    (hd : HasE Γ d (inst P x)) : HasE Γ (.app (.app s x) d) (inst Q x) := by
  have ht : inst (arr P Q) x = arr (inst P x) (inst Q x) := subst_arr P Q _
  have first := HasE.piElim (has_form hs)
    (ht.symm ▸ form_arr (form_inst_source hc hP hx) (form_inst_source hc hQ hx)) hs hx
  exact app_has (form_arr (form_inst_source hc hP hx) (form_inst_source hc hQ hx))
    (form_inst_source hc hQ hx) (ht ▸ first) hd

theorem dependent_action {Γ : Tel} {P Q : Ty} {s x y d e : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hQ : FormE (N :: Γ) Q)
    (hs : HasE Γ s (.pi N (arr P Q))) (hx : HasE Γ x N) (hy : HasE Γ y N)
    (hd : HasE Γ d (inst P x)) (he : HasE Γ e (.identity N x y)) :
    HasE Γ (jPoly ident y e)
      (.identity (inst Q y) (.app (.app s x) d) (.app (.app s y) d)) := by
  let H : Ty := .identity (wk N) (pren Nat.succ x) (.var 0)
  let P2 := shiftedFamily (shiftedFamily P)
  let Q2 := shiftedFamily (shiftedFamily Q)
  let x2 := pren Nat.succ (pren Nat.succ x)
  let d2 := pren Nat.succ (pren Nat.succ d)
  let s2 := pren Nat.succ (pren Nat.succ s)
  have cN := CtxE.ext hc (N_form hc)
  have hH : FormE (N :: Γ) H := form_theta_head hc (N_form hc) hx
  have ct : CtxE (theta Γ N x) := ctx_theta hc (N_form hc) hx
  have hP2 : FormE (N :: theta Γ N x) P2 :=
    shifted_family_form cN (shifted_family_form hc hP (N_form hc)) hH
  have hQ2 : FormE (N :: theta Γ N x) Q2 :=
    shifted_family_form cN (shifted_family_form hc hQ (N_form hc)) hH
  have hx2 : HasE (theta Γ N x) x2 N := by
    simpa only [wk, N_subst] using has_wk (has_wk hx hc (N_form hc)) cN hH
  have hd2 : HasE (theta Γ N x) d2 (inst P2 x2) := by
    simpa only [shifted_inst] using has_wk (has_wk hd hc (N_form hc)) cN hH
  have hs2 : HasE (theta Γ N x) s2 (.pi N (arr P2 Q2)) := by
    simpa only [shifted_piArr] using has_wk (has_wk hs hc (N_form hc)) cN hH
  have hv : HasE (theta Γ N x) (.var 1) N := .var (N_form ct) (.succ .zero)
  have hep : HasE (theta Γ N x) (.var 0) (.identity N x2 (.var 1)) := by
    have h : HasE (theta Γ N x) (.var 0) (wk H) := .var (form_wk hH cN hH) .zero
    simpa only [H, wk, subst, N_subst, psub, pren] using h
  have hdv := transport_has_erased ct (N_form ct) hP2 hx2 hv hep hd2
  have left0 := dependent_apply_has ct hP2 hQ2 hs2 hx2 hd2
  have left := transport_has_erased ct (N_form ct) hQ2 hx2 hv hep left0
  have right := dependent_apply_has ct hP2 hQ2 hs2 hv hdv
  let M : Ty := .identity (inst Q2 (.var 1))
    (.app (.app s2 x2) d2) (.app (.app s2 (.var 1)) d2)
  have hM : FormE (theta Γ N x) M := .identity (form_inst_source ct hQ2 hv) left right
  have at_eq (v r : Poly) : motiveAt M v r =
      .identity (inst Q v) (.app (.app s x) d) (.app (.app s v) d) := by
    simp only [M, motiveAt, subst, subst_inst, Q2, shiftedFamily, subst_comp,
      x2, d2, s2, pren, psub_comp, psub, cons, psub_id]
    congr 2
    conv_rhs => rw [← subst_id Q]
    congr 1
    funext k
    cases k <;> rfl
  have hleft := dependent_apply_has hc hP hQ hs hx hd
  have base := FormE.identity (form_inst_source hc hQ hx) hleft hleft
  have target : FormE Γ (motiveAt M y e) := by
    -- The motive itself supplies the transported endpoint typings after J.
    -- Construct those endpoints using already-proved dependent transport.
    have hdy := transport_source hc (N_form hc) hP hx hy he (hd)
    have hdy' : HasE Γ d (inst P y)  := conv_raw ((form_inst_source hc hP hy)) hdy
      ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)) (has_scoped hd)
    have hly := transport_source hc (N_form hc) hQ hx hy he (hleft)
    have hly' : HasE Γ (.app (.app s x) d) (inst Q y)  := conv_raw
      ((form_inst_source hc hQ hy)) hly
      ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)) (has_scoped hleft)
    have ht : inst (arr P Q) y = arr (inst P y) (inst Q y) := subst_arr P Q _
    have hf := HasE.piElim (has_form hs)
      (ht.symm ▸ form_arr (form_inst_source hc hP hy) (form_inst_source hc hQ hy)) hs hy
    have hf' := ht ▸ hf
    have right' := HasE.piElim ((has_form hf'))
      ((show FormE Γ (inst (wk (inst Q y)) d) from by
        simpa only [inst_wk] using form_inst_source hc hQ hy)) (hf') hdy'
    rw [at_eq]
    exact .identity ((form_inst_source hc hQ hy)) hly'
      (by simpa only [inst_wk] using right')
  have proof := HasE.j ((N_form hc)) (hM)
    ((.identity (N_form hc) hx hy))
    (((at_eq x ident).symm ▸ base)) target
    (hx) (hy) he
    (show HasE Γ ident (motiveAt M x ident) from
      (at_eq x ident).symm ▸ (identityIntro_raw base hleft hleft (.refl _)))
  simpa only [at_eq] using proof



theorem dependent_action_converted_left {Γ : Tel} {P Q : Ty} {s x y d e l : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hQ : FormE (N :: Γ) Q)
    (hs : HasE Γ s (.pi N (arr P Q))) (hx : HasE Γ x N) (hy : HasE Γ y N)
    (hd : HasE Γ d (inst P x)) (he : HasE Γ e (.identity N x y))
    (hlc : P01DF.PolyConv l (.app (.app s x) d)) (hls : Scoped Γ.length l) :
    HasE Γ (jPoly ident y e)
      (.identity (inst Q y) l (.app (.app s y) d)) := by
  have hleftOriginal := dependent_apply_has hc hP hQ hs hx hd
  have hl : HasE Γ l (inst Q x)  := conv_raw (form_inst_source hc hQ hx) hleftOriginal hlc.symm hls
  let H : Ty := .identity (wk N) (pren Nat.succ x) (.var 0)
  let P2 := shiftedFamily (shiftedFamily P)
  let Q2 := shiftedFamily (shiftedFamily Q)
  let x2 := pren Nat.succ (pren Nat.succ x)
  let d2 := pren Nat.succ (pren Nat.succ d)
  let l2 := pren Nat.succ (pren Nat.succ l)
  let s2 := pren Nat.succ (pren Nat.succ s)
  have cN := CtxE.ext hc (N_form hc)
  have hH : FormE (N :: Γ) H := form_theta_head hc (N_form hc) hx
  have ct : CtxE (theta Γ N x) := ctx_theta hc (N_form hc) hx
  have hP2 : FormE (N :: theta Γ N x) P2 :=
    shifted_family_form cN (shifted_family_form hc hP (N_form hc)) hH
  have hQ2 : FormE (N :: theta Γ N x) Q2 :=
    shifted_family_form cN (shifted_family_form hc hQ (N_form hc)) hH
  have hx2 : HasE (theta Γ N x) x2 N := by
    simpa only [wk, N_subst] using has_wk (has_wk hx hc (N_form hc)) cN hH
  have hd2 : HasE (theta Γ N x) d2 (inst P2 x2) := by
    simpa only [shifted_inst] using has_wk (has_wk hd hc (N_form hc)) cN hH
  have hs2 : HasE (theta Γ N x) s2 (.pi N (arr P2 Q2)) := by
    simpa only [shifted_piArr] using has_wk (has_wk hs hc (N_form hc)) cN hH
  have hv : HasE (theta Γ N x) (.var 1) N := .var (N_form ct) (.succ .zero)
  have hep : HasE (theta Γ N x) (.var 0) (.identity N x2 (.var 1)) := by
    have h : HasE (theta Γ N x) (.var 0) (wk H) := .var (form_wk hH cN hH) .zero
    simpa only [H, wk, subst, N_subst, psub, pren] using h
  have hdv := transport_has_erased ct (N_form ct) hP2 hx2 hv hep hd2
  have left0 : HasE (theta Γ N x) l2 (inst Q2 x2) := by
    simpa only [shifted_inst] using has_wk (has_wk hl hc (N_form hc)) cN hH
  have left := transport_has_erased ct (N_form ct) hQ2 hx2 hv hep left0
  have right := dependent_apply_has ct hP2 hQ2 hs2 hv hdv
  let M : Ty := .identity (inst Q2 (.var 1))
    l2 (.app (.app s2 (.var 1)) d2)
  have hM : FormE (theta Γ N x) M := .identity (form_inst_source ct hQ2 hv) left right
  have at_eq (v r : Poly) : motiveAt M v r =
      .identity (inst Q v) l (.app (.app s v) d) := by
    simp only [M, motiveAt, subst, subst_inst, Q2, shiftedFamily, subst_comp,
      x2, d2, s2, l2, pren, psub_comp, psub, cons, psub_id]
    congr 2
    conv_rhs => rw [← subst_id Q]
    congr 1
    funext k
    cases k <;> rfl
  have hright := dependent_apply_has hc hP hQ hs hx hd
  have base := FormE.identity (form_inst_source hc hQ hx) hl hright
  have target : FormE Γ (motiveAt M y e) := by
    -- The motive itself supplies the transported endpoint typings after J.
    -- Construct those endpoints using already-proved dependent transport.
    have hdy := transport_source hc (N_form hc) hP hx hy he (hd)
    have hdy' : HasE Γ d (inst P y)  := conv_raw ((form_inst_source hc hP hy)) hdy
      ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)) (has_scoped hd)
    have hly := transport_source hc (N_form hc) hQ hx hy he (hl)
    have hly' : HasE Γ l (inst Q y)  := conv_raw
      ((form_inst_source hc hQ hy)) hly
      ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)) hls
    have ht : inst (arr P Q) y = arr (inst P y) (inst Q y) := subst_arr P Q _
    have hf := HasE.piElim (has_form hs)
      (ht.symm ▸ form_arr (form_inst_source hc hP hy) (form_inst_source hc hQ hy)) hs hy
    have hf' := ht ▸ hf
    have right' := HasE.piElim ((has_form hf'))
      ((show FormE Γ (inst (wk (inst Q y)) d) from by
        simpa only [inst_wk] using form_inst_source hc hQ hy)) (hf') hdy'
    rw [at_eq]
    exact .identity ((form_inst_source hc hQ hy)) hly'
      (by simpa only [inst_wk] using right')
  have proof := HasE.j ((N_form hc)) (hM)
    ((.identity (N_form hc) hx hy))
    (((at_eq x ident).symm ▸ base)) target
    (hx) (hy) he
    (show HasE Γ ident (motiveAt M x ident) from
      (at_eq x ident).symm ▸ (identityIntro_raw base hl hright hlc))
  simpa only [at_eq] using proof



theorem successorFamily_form {Γ : Tel} {P : Ty} (hc : CtxE Γ)
    (hP : FormE (N :: Γ) P) : FormE (N :: Γ) (successorFamily P) := by
  have cN := CtxE.ext hc (N_form hc)
  have hP' := shifted_family_form hc hP (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have hsn := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) (succ_has_NT cN) hn
  have h := form_inst_source cN hP' hsn
  have eq : inst (shiftedFamily P) (.app succPoly (.var 0)) = successorFamily P := by
    simp only [inst, shiftedFamily, successorFamily, subst_comp]
    congr 1
    funext k
    cases k <;> rfl
  exact eq ▸ h


theorem section_zero_law {Γ : Tel} {P : Ty} {p s : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) :
    HasE Γ ident (.identity (inst P zero) (sectionBody p s zero) p) := by
  have hf := form_inst_source hc hP (zero_has_N hc)
  have hleft : HasE Γ (sectionBody p s zero) (inst P zero)  := conv_raw hf hp
    (section_zero_beta p s).symm (sectionBody_scoped hc hP hp hs (zero_has_N hc))
  exact identityIntro_raw (.identity hf hleft hp) hleft hp (section_zero_beta p s)


theorem projection_returns_input {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) (hr : HasE Γ r Rigidity) (hn : HasE Γ n N) :
    ∃ e, HasE Γ e (.identity N
      (fstPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p))) n) := by
  let D := totalStep (uncurriedStep s)
  let a := totalSeed p
  let u := projectedFold D a
  let run : Poly := .app (.app n D) a
  have hd := uncurried_step_has hc hP hs
  have hD := total_step_has hc hP hd
  have ha := total_seed_has hc hP hp
  have hu : HasE Γ u NT := projectedFold_has hc hP hD ha
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have hrun : HasE Γ run (total P) := fold_has hc hE hn hD ha
  have hfst : HasE Γ (fstPoly run) N := .sigmaFst (N_form hc) hE hrun
  have huN := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hn
  have rid := rigidity_elim hc hu hr
    ((projected_zero_evidence hc hP hp hd))
    ((projected_step_evidence hc hP hp hd))
  have point := rigidity_pointwise hc hu hn rid
  have link : HasE Γ ident (.identity N (fstPoly run) (.app u n)) :=
    identityIntro_raw (.identity (N_form hc) hfst huN) hfst huN (projectedFold_beta D a n).symm
  exact ⟨_, nat_identity_trans hc hfst huN hn (link) point⟩

theorem section_successor_law {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : CtxE Γ) (hP : FormE (N :: Γ) P) (hp : HasE Γ p (inst P zero))
    (hs : HasE Γ s (dependentStepType P)) (hr : HasE Γ r Rigidity) (hn : HasE Γ n N) :
    ∃ e, HasE Γ e (.identity (inst P (.app succPoly n))
      (sectionBody p s (.app succPoly n)) (.app (.app s n) (sectionBody p s n))) := by
  let D := totalStep (uncurriedStep s)
  let a := totalSeed p
  let run : Poly := .app (.app n D) a
  have hE : FormE Γ (total P) := .sigma (N_form hc) hP
  have hD := total_step_has hc hP (uncurried_step_has hc hP hs)
  have ha := total_seed_has hc hP hp
  have hrun : HasE Γ run (total P) := fold_has hc hE hn hD ha
  have hx : HasE Γ (fstPoly run) N := .sigmaFst (N_form hc) hE hrun
  have hd : HasE Γ (sndPoly run) (inst P (fstPoly run)) :=
    .sigmaSnd hE (form_inst_source hc hP hx) hrun
  obtain ⟨e, he⟩ := projection_returns_input hc hP hp hs hr hn
  have hsn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) (succ_has_NT hc) hn
  have result := dependent_action_converted_left hc hP (successorFamily_form hc hP)
    hs hx hn hd he (section_succ_beta p s n) (sectionBody_scoped hc hP hp hs hsn)
  exact ⟨_, by simpa only [successorFamily_at] using result⟩


end RigidityInitiality.FullE
