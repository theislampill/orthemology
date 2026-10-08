/- A closed old-rule boundary corollary. No change to inherited calculi. -/
import AllLegacyDerivations
import P01Omega
namespace P01NormalizationBoundary
open OrthemologyV2 OrthemologyV3 P01D P01Source
open P01AC.Legacy

def wrapper (q : Term) : Term := .app (.app .s .k) (.app .k q)
def t : Term := wrapper omega
def p : Poly := .app (.app (.atom .s) (.atom .k)) (.app (.atom .k) (.atom omega))
def oldIdentity : P01DF.Ty := .all (.arrow (.param 0) (.param 0))

theorem eval_p (η : Env) : eval p η = t := rfl

def tree : Derivation p oldIdentity :=
  .allIntro (.app (.app (.s (.param 0) .raw (.param 0)) (.k (.param 0) .raw))
    (.app (.k .raw (.param 0)) (.raw (.atom omega))))

theorem tree_supported : Supported 0 tree := by
  simp [tree,p,Supported,TypeSupported,P01AC.Scoped]

theorem old_typed : P01DF.Has p oldIdentity := erase tree

theorem new_typed : P01AC.Has [] p (.all (P01AC.arr (.param 0) (.param 0))) :=
  tree_supported.raw_embed

theorem new_finite_target : P01AC.Has [] p (P01AC.fin identityCode) := new_typed

theorem target_inhabited : FiniteDerives .i identityCode := .allI (.i (.var 0))

theorem application_S (a : Term) :
    Step (.app t a) (.app (.app .k a) (.app (.app .k omega) a)) := .s .k (.app .k omega) a

theorem application_K (a : Term) :
    Step (.app (.app .k a) (.app (.app .k omega) a)) a := .k a _

theorem application_returns (a : Term) : Red (.app t a) a :=
  .tail (application_S a) (.one (application_K a))

theorem wrapper_step {q u : Term} (h : Step (wrapper q) u) :
    ∃ q', Step q q' ∧ u = wrapper q' := by
  cases h with
  | left h x =>
      cases h with
      | left h x => cases h
      | right f h => cases h
  | right f h =>
      cases h with
      | left h x => cases h
      | right f h => exact ⟨_,h,rfl⟩

theorem wrapper_red {q u : Term} (h : Red (wrapper q) u) :
    ∃ q', Red q q' ∧ u = wrapper q' := by
  have aux : ∀ {v u}, Red v u → ∀ q, v = wrapper q → ∃ q', Red q q' ∧ u = wrapper q' := by
    intro v u r
    induction r with
    | refl v => intro q he; exact ⟨q,.refl q,he⟩
    | tail h r ih =>
        intro q he
        rw [he] at h
        obtain ⟨q',hq,he⟩ := wrapper_step h
        obtain ⟨q'',hr,he'⟩ := ih q' he
        exact ⟨q'',.tail hq hr,he'⟩
  exact aux h q rfl

theorem wrapper_normal {q : Term} (h : Normal (wrapper q)) : Normal q := by
  intro q' hs
  exact h (wrapper q') (.right (.app .s .k) (.right .k hs))

theorem no_normal_reduct {u : Term} (h : Red t u) : ¬ Normal u := by
  obtain ⟨q,hq,rfl⟩ := wrapper_red h
  exact fun hn => omega_no_normal_reduct hq (wrapper_normal hn)

theorem no_finite_source_representative :
    ¬ ∃ u C, FiniteDerives u C ∧ Conv t u := by
  rintro ⟨u,C,hu,hc⟩
  obtain ⟨n,hr,hn⟩ := finite_normal_form hu
  have hc' : Conv t n := .trans hc (P01Source.red_conv hr)
  obtain ⟨w,hw,hnw⟩ := conv_join hc'
  have he : w = n := normal_red hn hnw
  subst w
  exact no_normal_reduct hw hn

theorem boundary_control :
    P01DF.Has p oldIdentity ∧
    P01AC.Has [] p (P01AC.fin identityCode) ∧
    (∀ η, eval p η = t) ∧
    (∀ a, Red (.app t a) a) ∧
    (∀ u, Red t u → ¬ Normal u) ∧
    (¬ ∃ u C, FiniteDerives u C ∧ Conv t u) ∧
    FiniteDerives .i identityCode :=
  ⟨old_typed,new_finite_target,eval_p,application_returns,
   fun _ => no_normal_reduct,no_finite_source_representative,target_inhabited⟩
end P01NormalizationBoundary
