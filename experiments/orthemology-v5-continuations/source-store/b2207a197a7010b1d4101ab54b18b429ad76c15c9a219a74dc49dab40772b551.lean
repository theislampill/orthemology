import MicroReplay
import PhysicalFlattening

noncomputable section
open Filter
namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding PhysicalFlattening
variable {Θ A Y : Type*} [DecidableEq A]

omit [DecidableEq A] in
lemma headD_mem_of_nonempty (as : List A) (d : A) (h : as ≠ []) : as.headD d ∈ as := by
  cases as with
  | nil => exact (h rfl).elim
  | cons a as => simp

def macroBlocks (plan : Θ → List A) (choose : History A Y → Θ) (X : A → ℕ → Y) (n : ℕ) : List A :=
  plan (macroSelected plan choose X n)

lemma macro_length_eq_prefix (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (n : ℕ) :
    (macroHistory plan choose X n).length = prefixLength (macroBlocks plan choose X) n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [macro_history_length,prefixLength_succ,ih]; rfl

/-- Each actual action before the next boundary belongs to that block's plan. -/
theorem micro_action_mem_block (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (hne : ∀ σ, plan σ ≠ []) (X : A → ℕ → Y) (n i : ℕ)
    (hi : i < (macroBlocks plan choose X n).length) :
    policy plan choose d ()
      (microRun plan choose d X [] ((macroHistory plan choose X n).length + i)) ∈
        macroBlocks plan choose X n := by
  let h := macroHistory plan choose X n
  let as := macroBlocks plan choose X n
  have hi' : i < as.length := hi
  have hdrop : as.drop i ≠ [] := by
    intro he
    have hl := congrArg List.length he
    simp only [List.length_drop,List.length_nil] at hl
    omega
  have hq : queue plan choose h = as.take i ++ as.drop i := by
    rw [List.take_append_drop]
    exact macro_queue plan choose hne X n
  have hr := microRun_eq_feed_partial plan choose d X h (as.take i) (as.drop i) hdrop hq
  have hlen : (as.take i).length = i := List.length_take_of_le (Nat.le_of_lt hi)
  rw [hlen] at hr
  rw [microRun_add,macro_eq_micro_boundary plan choose d hne X n]
  change policy plan choose d () (microRun plan choose d X h i) ∈ as
  rw [hr]
  unfold policy
  rw [queue_feed_partial plan choose X h (as.take i) (as.drop i) hdrop hq]
  exact List.mem_of_mem_drop (headD_mem_of_nonempty _ d hdrop)

/-- Eventual goodness in support-block time transfers to the literal causal
micro-policy action sequence. This statement uses no completed-record decoder. -/
theorem micro_eventually_good (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (hne : ∀ σ, plan σ ≠ []) (X : A → ℕ → Y) (Good : A → Prop)
    (hgood : ∀ᶠ n in atTop, ∀ a ∈ macroBlocks plan choose X n, Good a) :
    ∀ᶠ t in atTop, Good (policy plan choose d () (microRun plan choose d X [] t)) := by
  let blocks := macroBlocks plan choose X
  have hn : ∀ n, blocks n ≠ [] := fun n => hne _
  have hu := unbounded_of_nonempty blocks hn
  obtain ⟨N,hN⟩ := eventually_atTop.mp hgood
  apply eventually_atTop.mpr
  refine ⟨prefixLength blocks N,fun t ht => ?_⟩
  let n := blockIndex blocks hu t
  have hl := blockIndex_lower blocks hu t
  have hi := offset_lt_length blocks hu t
  have hnN := late_index blocks hu N t ht
  have hm := micro_action_mem_block plan choose d hne X n
    (t-prefixLength blocks n) hi
  rw [macro_length_eq_prefix] at hm
  have he : prefixLength blocks n + (t-prefixLength blocks n) = t := Nat.add_sub_of_le hl
  rw [he] at hm
  exact hN n hnN _ hm

end Orthemology.Tranche2.MicroPolicy
