import NativeReference

namespace SharedAlias.Native
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface)
noncomputable section
open Classical

/-- Apply one fixed transformation at two addressed cells. Shared addresses
are handled by equality; distinct addresses use independent function updates. -/
theorem update_transform_commute {α β : Type} [DecidableEq α]
    (f : α → β) (a b : α) (g : β → β) :
    Function.update (Function.update f a (g (f a))) b
        (g ((Function.update f a (g (f a))) b)) =
      Function.update (Function.update f b (g (f b))) a
        (g ((Function.update f b (g (f b))) a)) := by
  by_cases same : a = b
  · subst b; rfl
  · simp only [Function.update_of_ne same, Function.update_of_ne (Ne.symm same)]
    exact Function.update_comm same _ _ _

/-- These are commutation laws for represented set-valued shared state.
They do not assert that native raw lists have identical insertion order. -/
theorem shared_prepare_commute {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k : I.Command) :
    SharedAlias.prepare E (SharedAlias.prepare E C i k) j k =
      SharedAlias.prepare E (SharedAlias.prepare E C j k) i k := by
  unfold SharedAlias.prepare SharedAlias.setRoot
  congr 1
  exact update_transform_commute C.roots (E.rootOf i) (E.rootOf j)
    (fun z => { z with commitments := insert k z.commitments })

theorem prepareAllowed_after_prepare {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Bool) :
    SharedAlias.Progress.prepareAllowed E (SharedAlias.prepare E C j k) i k who time badReply ↔
      SharedAlias.Progress.prepareAllowed E C i k who time badReply := by
  by_cases good : Good E.labelConfig i
  · simp only [SharedAlias.Progress.prepareAllowed, if_pos good,
      SharedAlias.Progress.prepare_envelope]
  · simp only [SharedAlias.Progress.prepareAllowed, if_neg good]

theorem shared_prepareSlot_commute {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k : I.Command) (who : I.Requester)
    (time : Nat) (bad : Fin m → Bool) :
    SharedAlias.Progress.prepareSlot E
        (SharedAlias.Progress.prepareSlot E C i k who time (bad i)) j k who time (bad j) =
      SharedAlias.Progress.prepareSlot E
        (SharedAlias.Progress.prepareSlot E C j k who time (bad j)) i k who time (bad i) := by
  by_cases first : SharedAlias.Progress.prepareAllowed E C i k who time (bad i)
  · by_cases second : SharedAlias.Progress.prepareAllowed E C j k who time (bad j)
    · have afterI := (prepareAllowed_after_prepare E C j i k who time (bad j)).mpr second
      have afterJ := (prepareAllowed_after_prepare E C i j k who time (bad i)).mpr first
      simp only [SharedAlias.Progress.prepareSlot, if_pos first, if_pos second, if_pos afterI, if_pos afterJ]
      exact shared_prepare_commute E C i j k
    · have afterI : ¬SharedAlias.Progress.prepareAllowed E (SharedAlias.prepare E C i k) j k who time (bad j) :=
        fun yes => second ((prepareAllowed_after_prepare E C j i k who time (bad j)).mp yes)
      simp only [SharedAlias.Progress.prepareSlot, if_pos first, if_neg second, if_neg afterI]
  · by_cases second : SharedAlias.Progress.prepareAllowed E C j k who time (bad j)
    · have afterJ : ¬SharedAlias.Progress.prepareAllowed E (SharedAlias.prepare E C j k) i k who time (bad i) :=
        fun yes => first ((prepareAllowed_after_prepare E C i j k who time (bad i)).mp yes)
      simp only [SharedAlias.Progress.prepareSlot, if_neg first, if_pos second, if_neg afterJ]
    · simp only [SharedAlias.Progress.prepareSlot, if_neg first, if_neg second]

theorem shared_cancelAck_commute {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k : I.Command) :
    SharedAlias.cancelAck E (SharedAlias.cancelAck E C i k) j k =
      SharedAlias.cancelAck E (SharedAlias.cancelAck E C j k) i k := by
  have rootComm := update_transform_commute C.roots (E.rootOf i) (E.rootOf j)
    (fun z => { z with cancelled := insert k z.cancelled })
  unfold SharedAlias.cancelAck
  congr 1
  · by_cases goodI : Good E.labelConfig i
    · by_cases goodJ : Good E.labelConfig j
      · simpa only [if_pos goodI, if_pos goodJ] using rootComm
      · simp only [if_pos goodI, if_neg goodJ]
    · by_cases goodJ : Good E.labelConfig j
      · simp only [if_neg goodI, if_pos goodJ]
      · simp only [if_neg goodI, if_neg goodJ]
  · funext command
    by_cases same : command = k
    · subst command
      simp only [Function.update_self, Finset.insert_comm]
    · simp only [Function.update_of_ne same]


theorem shared_cancelSlot_commute {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (i j : Fin m) (k : I.Command) (who : I.Requester)
    (bad : Fin m → Bool) :
    SharedAlias.Progress.cancelSlot E
        (SharedAlias.Progress.cancelSlot E C i k who (bad i)) j k who (bad j) =
      SharedAlias.Progress.cancelSlot E
        (SharedAlias.Progress.cancelSlot E C j k who (bad j)) i k who (bad i) := by
  unfold SharedAlias.Progress.cancelSlot
  split_ifs
  · exact shared_cancelAck_commute E C i j k
  all_goals rfl

theorem serviceList_eq_foldl {m} {I : Interface m} (service : SharedAlias.Progress.Service I)
    (C : SharedAlias.State I) (labels : List (Fin m)) :
    SharedAlias.Progress.serviceList service C labels = labels.foldl service C := by
  induction labels generalizing C with
  | nil => rfl
  | cons i labels ih => simpa only [SharedAlias.Progress.serviceList, List.foldl_cons] using ih (service C i)

theorem prepare_service_permutation {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester) (time : Nat) (bad : Fin m → Bool)
    (xs ys : List (Fin m)) (permutation : xs.Perm ys) :
    SharedAlias.Progress.serviceList (fun S i => SharedAlias.Progress.prepareSlot E S i k who time (bad i)) C xs =
      SharedAlias.Progress.serviceList (fun S i => SharedAlias.Progress.prepareSlot E S i k who time (bad i)) C ys := by
  letI : RightCommutative (fun S i => SharedAlias.Progress.prepareSlot E S i k who time (bad i)) :=
    ⟨fun S i j => shared_prepareSlot_commute E S i j k who time bad⟩
  simpa only [serviceList_eq_foldl] using permutation.foldl_eq C

theorem cancel_service_permutation {m} {I : Interface m} (E : SharedAlias.Environment I)
    (C : SharedAlias.State I) (k : I.Command) (who : I.Requester) (bad : Fin m → Bool)
    (xs ys : List (Fin m)) (permutation : xs.Perm ys) :
    SharedAlias.Progress.serviceList (fun S i => SharedAlias.Progress.cancelSlot E S i k who (bad i)) C xs =
      SharedAlias.Progress.serviceList (fun S i => SharedAlias.Progress.cancelSlot E S i k who (bad i)) C ys := by
  letI : RightCommutative (fun S i => SharedAlias.Progress.cancelSlot E S i k who (bad i)) :=
    ⟨fun S i j => shared_cancelSlot_commute E S i j k who bad⟩
  simpa only [serviceList_eq_foldl] using permutation.foldl_eq C

end
end SharedAlias.Native
