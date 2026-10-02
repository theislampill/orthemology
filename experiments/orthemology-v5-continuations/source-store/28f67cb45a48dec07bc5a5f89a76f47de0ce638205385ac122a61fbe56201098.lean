import CanonicalHistoryBudget
import BernoulliPrefixLaw
import RepairEndpointCells

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Finset Filter Preorder
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3.AuditControlBridge
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding CanonicalMicro

/-- The same Bernoulli selector law at every available control action. -/
def actionBlindKernel {A : Type*} (a : ℝ) (_ : A) (b : Bool) : ℝ := coinMass a b
lemma actionBlindKernel_nonneg {A : Type*} (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    ∀ x : A, ∀ b, 0 ≤ actionBlindKernel a x b := fun _ b => coinMass_nonneg a ha0 ha1 b
lemma actionBlindKernel_normalized {A : Type*} (a : ℝ) :
    ∀ x : A, ∑ b, actionBlindKernel a x b = 1 := by intro x; simp [actionBlindKernel,coinMass]

def wordPMF (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (n : ℕ) : PMF (Bits n) :=
  PMF.ofFintype (fun w => ENNReal.ofReal (bernoulliMass n a w)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun w _ => bernoulliMass_nonneg n a ha0 ha1 w),
      bernoulliMass_sum,ENNReal.ofReal_one])

lemma wordPMF_zero (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) : wordPMF a ha0 ha1 0 = PMF.pure () := by
  apply PMF.ext
  intro w
  cases w
  simp [wordPMF,bernoulliMass]

lemma wordPMF_succ (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (n : ℕ) :
    wordPMF a ha0 ha1 (n+1) =
      (wordPMF a ha0 ha1 n).bind (fun w => (sourceCoin a ha0 ha1).map (fun b => (b,w))) := by
  classical
  apply PMF.ext
  rintro ⟨b,w⟩
  rw [PMF.bind_apply]
  have hm : ∀ v : Bits n, ((sourceCoin a ha0 ha1).map (fun c => (c,v))) (b,w) =
      if v = w then ENNReal.ofReal (coinMass a b) else 0 := by
    intro v
    rw [PMF.map_apply,tsum_fintype]
    by_cases hv : v = w
    · subst v
      cases b <;> simp [sourceCoin]
    · cases b <;> simp [hv,Ne.symm hv]
  change ENNReal.ofReal (bernoulliMass (n+1) a (b,w)) =
    ∑' v : Bits n, (wordPMF a ha0 ha1 n) v *
      ((sourceCoin a ha0 ha1).map (fun c => (c,v))) (b,w)
  simp_rw [hm]
  rw [tsum_eq_single w]
  · simp only [if_pos rfl]
    change ENNReal.ofReal (coinMass a b * bernoulliMass n a w) =
      ENNReal.ofReal (bernoulliMass n a w) * ENNReal.ofReal (coinMass a b)
    rw [ENNReal.ofReal_mul (coinMass_nonneg a ha0 ha1 b),mul_comm]
  · intro v hv
    simp [hv]

/-- The finite word PMF is identified with the actual infinite audit source. -/
theorem wordPMF_eq_audit_prefix (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (n : ℕ) :
    (wordPMF a ha0 ha1 n).toMeasure = (auditSourceLaw a ha0 ha1).map (observedPrefix n) := by
  apply Measure.ext_of_singleton
  intro w
  rw [PMF.toMeasure_apply_singleton _ w (measurableSet_singleton w),auditSource_prefix_mass]
  rfl

variable {A : Type} [Fintype A] [DecidableEq A]

def encodeHistory (π : History A Bool → A) : (n : ℕ) → Bits n → History A Bool
  | 0, _ => []
  | n+1, (b,w) => let h := encodeHistory π n w
                  (π h,b)::h

def auditHistory (π : History A Bool → A) (ω : ℕ → Bool) (n : ℕ) : History A Bool :=
  encodeHistory π n (observedPrefix n ω)

def auditActions (π : History A Bool → A) (ω : ℕ → Bool) (n : ℕ) : A :=
  π (auditHistory π ω n)

/-- The bit-input implementation consumes exactly one already-acquired bit per
physical action and has no latent action-coordinate access. -/
lemma auditHistory_succ (π : History A Bool → A) (ω : ℕ → Bool) (n : ℕ) :
    auditHistory π ω (n+1) = (π (auditHistory π ω n),ω n)::auditHistory π ω n := rfl

/-- Finite physical histories under the iid audit source have exactly the
controlled micro-PMF law for the action-independent kernel. -/
theorem encoded_wordPMF_eq_historyPMF (π : History A Bool → A)
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (n : ℕ) :
    (wordPMF a ha0 ha1 n).map (encodeHistory π n) =
      historyPMF π (actionBlindKernel a) (actionBlindKernel_nonneg a ha0 ha1)
        (actionBlindKernel_normalized a) n := by
  induction n with
  | zero => simp [wordPMF_zero,PMF.pure_map,encodeHistory,historyPMF]
  | succ n ih =>
    rw [wordPMF_succ,PMF.map_bind,historyPMF,← ih,PMF.bind_map]
    apply congrArg (PMF.bind (wordPMF a ha0 ha1 n))
    funext w
    rw [PMF.map_comp]
    unfold nextHistoryPMF
    have he : actionObsPMF (actionBlindKernel a) (actionBlindKernel_nonneg a ha0 ha1)
        (actionBlindKernel_normalized a) (π (encodeHistory π n w)) = sourceCoin a ha0 ha1 := by
      apply PMF.ext
      intro b
      rfl
    change (sourceCoin a ha0 ha1).map _ =
      (actionObsPMF (actionBlindKernel a) (actionBlindKernel_nonneg a ha0 ha1)
        (actionBlindKernel_normalized a) (π (encodeHistory π n w))).map _
    rw [he]
    rfl

lemma auditHistory_measurable [MeasurableSpace A] (π : History A Bool → A) :
    Measurable (auditHistory π) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_finite (encodeHistory π n)).comp (observedPrefix_measurable n)

lemma auditHistory_drop (π : History A Bool → A) (ω : ℕ → Bool) (n m : ℕ) (hm : m ≤ n) :
    (auditHistory π ω n).drop (n-m) = auditHistory π ω m := by
  induction n generalizing m with
  | zero =>
    have he : m = 0 := by omega
    subst m
    rfl
  | succ n ih =>
    by_cases he : m = n+1
    · subst m; simp
    · have hsub : n+1-m = (n-m)+1 := by omega
      rw [auditHistory_succ,hsub,List.drop_succ_cons]
      exact ih m (by omega)

lemma auditHistory_prefix_from_last (π : History A Bool → A) (ω : ℕ → Bool) (N : ℕ) :
    frestrictLe N (auditHistory π ω) = reconstructPrefix N (auditHistory π ω N) := by
  funext i
  exact (auditHistory_drop π ω N i.val (Finset.mem_Iic.mp i.property)).symm

/-- Receipt prefix n contains precisely the first n bits. -/
lemma observedPrefix_agrees (ω ω' : ℕ → Bool) (n : ℕ)
    (h : ∀ k < n, ω k = ω' k) : observedPrefix n ω = observedPrefix n ω' := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [observedPrefix]
    rw [h n (by omega),ih (fun k hk => h k (by omega))]

/-- Action n has no access to bit n or any later selector. -/
theorem auditActions_uses_only_past (π : History A Bool → A) (ω ω' : ℕ → Bool) (n : ℕ)
    (h : ∀ k < n, ω k = ω' k) : auditActions π ω n = auditActions π ω' n := by
  unfold auditActions auditHistory
  rw [observedPrefix_agrees ω ω' n h]

section Laws
variable {R : Type*} [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]

/-- Exact one-time marginal equality with the previous canonical law. -/
theorem auditHistory_marginal_eq_canonical (π : History A Bool → A)
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (ρ : Measure R) [IsProbabilityMeasure ρ] (n : ℕ) :
    (auditSourceLaw a ha0 ha1).map (fun ω => auditHistory π ω n) =
      (ρ.prod (feedbackLaw (actionBlindKernel a) (actionBlindKernel a)
        (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a)
        (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a))).map
        (fun z => historyTrajectory ∅ (ignoreSeed π) z n) := by
  calc
    _ = ((auditSourceLaw a ha0 ha1).map (observedPrefix n)).map (encodeHistory π n) := by
      rw [Measure.map_map (measurable_of_finite _) (observedPrefix_measurable n)]
      rfl
    _ = (wordPMF a ha0 ha1 n).toMeasure.map (encodeHistory π n) := by rw [wordPMF_eq_audit_prefix]
    _ = (historyPMF π (actionBlindKernel a) (actionBlindKernel_nonneg a ha0 ha1)
        (actionBlindKernel_normalized a) n).toMeasure := by
      rw [PMF.toMeasure_map _ _ (measurable_of_finite _),encoded_wordPMF_eq_historyPMF]
    _ = _ := historyPMF_eq_canonical_marginal π ρ _ _ _ n

/-- The complete acquired-history experiment under the actual audit source
matches the controlled experiment. No runner law equality is a premise. -/
theorem auditHistory_law_eq_canonical (π : History A Bool → A)
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (ρ : Measure R) [IsProbabilityMeasure ρ] :
    (auditSourceLaw a ha0 ha1).map (auditHistory π) =
      observedTraceLaw ∅ (ignoreSeed π) ρ (actionBlindKernel a) (actionBlindKernel a)
        (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a)
        (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a) := by
  haveI : IsFiniteMeasure (observedTraceLaw ∅ (ignoreSeed π) ρ (actionBlindKernel a) (actionBlindKernel a)
      (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a)
      (actionBlindKernel_nonneg a ha0 ha1) (actionBlindKernel_normalized a)) := by
    unfold observedTraceLaw
    infer_instance
  apply measure_eq_of_prefix_maps
  intro N
  rw [observed_prefix_map_from_last ∅ (ignoreSeed π) (ignoreSeed_measurable π)]
  rw [Measure.map_map (measurable_frestrictLe N) (auditHistory_measurable π)]
  have he : frestrictLe N ∘ auditHistory π = reconstructPrefix N ∘ (fun ω => auditHistory π ω N) := by
    funext ω
    exact auditHistory_prefix_from_last π ω N
  rw [he,← Measure.map_map (measurable_of_countable (reconstructPrefix (A := A) (Y := Bool) N))
    (show Measurable (fun ω => auditHistory π ω N) from
      (measurable_pi_apply N).comp (auditHistory_measurable π)),auditHistory_marginal_eq_canonical π a ha0 ha1 ρ N]

lemma auditActions_measurable (π : History A Bool → A) : Measurable (auditActions π) := by
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_countable π).comp ((measurable_pi_apply n).comp (auditHistory_measurable π))

/-- Actual iid selector receipts and the original causal control actionLaw
produce exactly the same finite-action sequence for this action-blind source. -/
theorem auditActions_law_eq_canonical (π : History A Bool → A)
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (ρ : Measure R) [IsProbabilityMeasure ρ] (d : A) :
    (auditSourceLaw a ha0 ha1).map (auditActions π) =
      actionLaw (ignoreSeed π) ρ (actionBlindKernel a) (actionBlindKernel_nonneg a ha0 ha1)
        (actionBlindKernel_normalized a) d := by
  have he : auditActions π = historyAction d ∘ auditHistory π := by
    funext ω n
    simp only [auditActions,Function.comp_apply,historyAction,auditHistory_succ,List.headD_cons,Prod.fst]
  rw [he,← Measure.map_map (historyAction_measurable d) (auditHistory_measurable π),
    auditHistory_law_eq_canonical π a ha0 ha1 ρ]
  rfl
end Laws
end Orthemology.Tranche3.AuditControlBridge
