import Std

/- A nonempty Boolean-set mereology with four atoms. All predicate pluralities
   are admitted. This is a relational interpretation, not a metaphysical world. -/
namespace TotalExplainerBooleanControl

abbrev Atom := Fin 4
abbrev Fact := { P : Atom → Prop // ∃ t, P t }
abbrev Plurality := Fact → Prop

def atomFact (t : Atom) : Fact := ⟨fun k => k = t, ⟨t, rfl⟩⟩
def q : Fact := atomFact 0
def a : Fact := atomFact 1
def b : Fact := atomFact 2
def e : Fact := atomFact 3

def singleton (x : Fact) : Plurality := fun y => y = x
def Part (x y : Fact) : Prop := ∀ t, x.val t → y.val t
def Overlap (x y : Fact) : Prop := ∃ z, Part z x ∧ Part z y

def E (x : Fact) (S : Plurality) : Prop :=
  (∃ y, S y) ∧ (x = q ∨ ((x = a ∨ x = b) ∧ ∀ y, S y → y = e))
def PE (x : Fact) (S : Plurality) : Prop := ∃ z, Part x z ∧ E z S

theorem fact_ext {x y : Fact} (h : ∀ t, x.val t ↔ y.val t) : x = y := by
  apply Subtype.ext
  funext t
  exact propext (h t)

@[simp] theorem atomFact_eq_iff (i j : Atom) : atomFact i = atomFact j ↔ i = j := by
  constructor
  · intro h
    have hi : (atomFact j).val i := h ▸ (show (atomFact i).val i from rfl)
    exact hi
  · intro h
    exact congrArg atomFact h

theorem part_order :
    (∀ x, Part x x) ∧
    (∀ x y z, Part x y → Part y z → Part x z) ∧
    (∀ x y, Part x y → Part y x → x = y) := by
  exact ⟨fun _ _ h => h,
    fun _ _ _ hxy hyz t ht => hyz t (hxy t ht),
    fun _ _ hxy hyx => fact_ext (fun t => ⟨hxy t, hyx t⟩)⟩

theorem part_atom_eq {x : Fact} {t : Atom} (h : Part x (atomFact t)) :
    x = atomFact t := by
  apply fact_ext
  intro k
  constructor
  · exact h k
  · intro hk
    obtain ⟨j, hj⟩ := x.property
    have hjt : j = t := h j hj
    have ht : x.val t := hjt ▸ hj
    exact hk.symm ▸ ht

theorem overlap_iff (x y : Fact) : Overlap x y ↔ ∃ t, x.val t ∧ y.val t := by
  constructor
  · rintro ⟨z, hzx, hzy⟩
    obtain ⟨t, ht⟩ := z.property
    exact ⟨t, hzx t ht, hzy t ht⟩
  · rintro ⟨t, hx, hy⟩
    refine ⟨atomFact t, ?_, ?_⟩
    · intro k hk
      exact hk.symm ▸ hx
    · intro k hk
      exact hk.symm ▸ hy

theorem strong_supplementation (x y : Fact) (hnot : ¬ Part x y) :
    ∃ z, Part z x ∧ ¬ Overlap z y := by
  classical
  have hw : ∃ t, x.val t ∧ ¬ y.val t := by
    apply Classical.byContradiction
    intro h
    apply hnot
    intro t ht
    apply Classical.byContradiction
    intro hny
    exact h ⟨t, ht, hny⟩
  obtain ⟨t, hx, hny⟩ := hw
  refine ⟨atomFact t, ?_, ?_⟩
  · intro k hk
    exact hk.symm ▸ hx
  · intro hover
    obtain ⟨k, hk, hy⟩ := (overlap_iff (atomFact t) y).mp hover
    exact hny (hk ▸ hy)

-- Fusion is the nonempty union of all member facts, for any nonempty plurality.
def fusion (S : Plurality) (hne : ∃ x, S x) : Fact :=
  ⟨fun t => ∃ x, S x ∧ x.val t, by
    obtain ⟨x, hx⟩ := hne
    obtain ⟨t, ht⟩ := x.property
    exact ⟨t, x, hx, ht⟩⟩

theorem all_nonempty_fusions (S : Plurality) (hne : ∃ x, S x) :
    ∃ f, (∀ x, S x → Part x f) ∧
      (∀ z, Overlap z f ↔ ∃ x, S x ∧ Overlap z x) := by
  refine ⟨fusion S hne, ?_, ?_⟩
  · intro x hx t ht
    exact ⟨x, hx, ht⟩
  · intro z
    constructor
    · intro hz
      obtain ⟨t, hzt, hft⟩ := (overlap_iff z (fusion S hne)).mp hz
      obtain ⟨x, hx, hxt⟩ := hft
      exact ⟨x, hx, (overlap_iff z x).mpr ⟨t, hzt, hxt⟩⟩
    · rintro ⟨x, hx, hzx⟩
      obtain ⟨t, hzt, hxt⟩ := (overlap_iff z x).mp hzx
      exact (overlap_iff z (fusion S hne)).mpr ⟨t, hzt, x, hx, hxt⟩

theorem fusion_least_upper_bound (S : Plurality) (hne : ∃ x, S x) (y : Fact) :
    Part (fusion S hne) y ↔ ∀ x, S x → Part x y := by
  constructor
  · intro h x hx t ht
    exact h t ⟨x, hx, ht⟩
  · intro h t ht
    obtain ⟨x, hx, hxt⟩ := ht
    exact h x hx t hxt

-- A witnessed proper part prevents mistaking this for equality parthood.
def qa : Fact := ⟨fun t => t = 0 ∨ t = 1, ⟨0, Or.inl rfl⟩⟩

theorem q_proper_part_qa : Part q qa ∧ q ≠ qa := by
  constructor
  · intro t ht
    exact Or.inl ht
  · intro h
    have hqa1 : qa.val 1 := Or.inr rfl
    have hq1 : q.val 1 := h.symm ▸ hqa1
    exact (by decide : (1 : Atom) ≠ 0) hq1

theorem full_explainers_atomic (x : Fact) (S : Plurality) (h : E x S) :
    ∃ t, x = atomFact t := by
  rcases h.2 with hq | ⟨ha | hb, _⟩
  · exact ⟨0, hq⟩
  · exact ⟨1, ha⟩
  · exact ⟨2, hb⟩

theorem no_composite_explanation (x : Fact) (S : Plurality)
    (h : ¬ ∃ t, x = atomFact t) : ¬ E x S := by
  intro he
  exact h (full_explainers_atomic x S he)

theorem partial_iff_full (x : Fact) (S : Plurality) : PE x S ↔ E x S := by
  constructor
  · rintro ⟨z, hxz, hz⟩
    obtain ⟨t, hzt⟩ := full_explainers_atomic z S hz
    have hxt : x = atomFact t := part_atom_eq (hzt ▸ hxz)
    have hxz' : x = z := hxt.trans hzt.symm
    exact hxz'.symm ▸ hz
  · intro h
    exact ⟨x, part_order.1 x, h⟩

theorem full_implies_partial (x : Fact) (S : Plurality) (h : E x S) : PE x S := by
  exact (partial_iff_full x S).mpr h

theorem partial_source_closure (x y : Fact) (S : Plurality)
    (hpart : Part x y) (h : PE y S) : PE x S := by
  obtain ⟨z, hyz, hz⟩ := h
  exact ⟨z, part_order.2.1 x y z hpart hyz, hz⟩

theorem unrestricted_psr (S : Plurality) (hne : ∃ x, S x) : ∃ x, E x S := by
  exact ⟨q, hne, Or.inl rfl⟩

theorem no_empty_explanation (x : Fact) : ¬ E x (fun _ => False) := by
  rintro ⟨⟨y, hy⟩, _⟩
  exact hy

theorem e_explains_nothing (S : Plurality) : ¬ E e S := by
  simp [E, e, q, a, b]

theorem complete_transitivity (x : Fact) (S : Plurality) (y : Fact) (T : Plurality)
    (hx : E x S) (hy : S y) (hyt : E y T) : E x T := by
  rcases hx with ⟨_, hq | ⟨_, hlocal⟩⟩
  · exact ⟨hyt.1, Or.inl hq⟩
  · have hye := hlocal y hy
    exact False.elim (e_explains_nothing T (hye ▸ hyt))

theorem partial_transitivity (x : Fact) (S : Plurality) (y : Fact) (T : Plurality)
    (hx : PE x S) (hy : S y) (hyt : E y T) : PE x T := by
  exact (partial_iff_full x T).mpr
    (complete_transitivity x S y T ((partial_iff_full x S).mp hx) hy hyt)

theorem member_projection (x : Fact) (S : Plurality) (y : Fact)
    (hx : E x S) (hy : S y) : E x (singleton y) := by
  refine ⟨⟨y, rfl⟩, ?_⟩
  rcases hx.2 with hq | ⟨hab, hlocal⟩
  · exact Or.inl hq
  · refine Or.inr ⟨hab, ?_⟩
    intro z hz
    exact hz.trans (hlocal y hy)

theorem distribution (x : Fact) (S : Plurality) (y z : Fact)
    (hx : E x S) (hy : S y) (hz : z = y ∨ Part z y) : E x (singleton z) := by
  rcases hx.2 with hq | ⟨hab, hlocal⟩
  · exact ⟨⟨z, rfl⟩, Or.inl hq⟩
  · have hye : y = e := hlocal y hy
    have hze : z = e := by
      rcases hz with hzy | hpart
      · exact hzy.trans hye
      · have hpart' : Part z e := hye ▸ hpart
        exact part_atom_eq hpart'
    refine ⟨⟨z, rfl⟩, Or.inr ⟨hab, ?_⟩⟩
    intro w hw
    exact hw.trans hze

theorem no_extended_circles (x : Fact) (S : Plurality) (y : Fact)
    (hx : PE x S) (hy : S y) (hne : y ≠ x) (_hnotpart : ¬ Part y x) :
    ¬ PE y (singleton x) := by
  intro hback
  have hxfull := (partial_iff_full x S).mp hx
  have hyfull := (partial_iff_full y (singleton x)).mp hback
  rcases hxfull.2 with hq | ⟨_, hlocal⟩
  · rcases hyfull.2 with hyq | ⟨_, htarget⟩
    · exact hne (hyq.trans hq.symm)
    · have hxe := htarget x rfl
      have hqe : q = e := hq.symm.trans hxe
      exact (by simp [q, e] : q ≠ e) hqe
  · have hye := hlocal y hy
    exact e_explains_nothing (singleton x) (hye ▸ hyfull)

theorem unique_total_explainer :
    E q (fun _ => True) ∧ ∀ x, E x (fun _ => True) → x = q := by
  constructor
  · exact ⟨⟨q, trivial⟩, Or.inl rfl⟩
  · intro x hx
    rcases hx.2 with hq | ⟨_, hlocal⟩
    · exact hq
    · exact False.elim ((by simp [q, e] : q ≠ e) (hlocal q trivial))

theorem two_distinct_explainers_of_narrow_target :
    a ≠ b ∧ E a (singleton e) ∧ E b (singleton e) ∧
    ¬ singleton e a ∧ ¬ singleton e b := by
  simp [E, singleton, q, a, b, e]

theorem local_explainers_exactly (x : Fact) :
    E x (singleton e) ↔ x = q ∨ x = a ∨ x = b := by
  simp [E, singleton, or_assoc]

theorem restricted_external_explainers :
    ∀ S, (∃ y, S y) → (∀ y, S y → y = e) →
      E a S ∧ E b S ∧
      (∀ y, S y → a ≠ y ∧ ¬ Part a y ∧ b ≠ y ∧ ¬ Part b y) := by
  intro S hne hlocal
  refine ⟨⟨hne, Or.inr ⟨Or.inl rfl, hlocal⟩⟩,
    ⟨hne, Or.inr ⟨Or.inr rfl, hlocal⟩⟩, ?_⟩
  intro y hy
  have hye := hlocal y hy
  subst y
  have hae : a ≠ e := by simp [a, e]
  have hbe : b ≠ e := by simp [b, e]
  exact ⟨hae, fun h => hae (part_atom_eq h), hbe, fun h => hbe (part_atom_eq h)⟩

end TotalExplainerBooleanControl

#print axioms TotalExplainerBooleanControl.part_order
#print axioms TotalExplainerBooleanControl.strong_supplementation
#print axioms TotalExplainerBooleanControl.all_nonempty_fusions
#print axioms TotalExplainerBooleanControl.fusion_least_upper_bound
#print axioms TotalExplainerBooleanControl.q_proper_part_qa
#print axioms TotalExplainerBooleanControl.full_explainers_atomic
#print axioms TotalExplainerBooleanControl.no_composite_explanation
#print axioms TotalExplainerBooleanControl.partial_iff_full
#print axioms TotalExplainerBooleanControl.partial_source_closure
#print axioms TotalExplainerBooleanControl.unrestricted_psr
#print axioms TotalExplainerBooleanControl.complete_transitivity
#print axioms TotalExplainerBooleanControl.partial_transitivity
#print axioms TotalExplainerBooleanControl.distribution
#print axioms TotalExplainerBooleanControl.no_extended_circles
#print axioms TotalExplainerBooleanControl.unique_total_explainer
#print axioms TotalExplainerBooleanControl.two_distinct_explainers_of_narrow_target
#print axioms TotalExplainerBooleanControl.local_explainers_exactly
#print axioms TotalExplainerBooleanControl.restricted_external_explainers
