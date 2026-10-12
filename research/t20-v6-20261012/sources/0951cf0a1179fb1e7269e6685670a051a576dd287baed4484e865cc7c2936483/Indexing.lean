import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-! The exceptional monomial indexing and its global midpoint property. -/
namespace FullFunctionalIndexing

abbrev Exponent := ℕ × ℕ

def degree (p : Exponent) : ℕ := p.1 + p.2

def triangle : ℕ → ℕ
  | 0 => 0
  | n + 1 => triangle n + n + 1

@[simp] theorem triangle_zero : triangle 0 = 0 := rfl
@[simp] theorem triangle_succ (n : ℕ) : triangle (n+1) = triangle n + n + 1 := rfl

theorem twice_triangle (n : ℕ) : 2 * triangle n = n * (n+1) := by
  induction n with
  | zero => simp
  | succ n ih => rw [triangle_succ]; nlinarith

theorem triangle_formula (n : ℕ) : triangle n = n * (n+1) / 2 := by
  have h := twice_triangle n
  omega

theorem triangle_mono : Monotone triangle := by
  apply monotone_nat_of_le_succ
  intro n
  simp only [triangle_succ]
  omega

def seedIndex : Exponent → ℕ
  | (0, 0) => 1
  | (2, 1) => 2
  | (1, 2) => 3
  | (1, 1) => 4
  | (1, 0) => 5
  | (0, 1) => 6
  | (2, 0) => 7
  | (0, 2) => 8
  | (3, 0) => 9
  | (0, 3) => 10
  | _ => 0

/-- The one-based exceptional enumeration, followed by the ordinary degree shells. -/
def index (p : Exponent) : ℕ :=
  if degree p ≤ 3 then seedIndex p else triangle (degree p) + p.2 + 1

/-- The integer midpoint, used only when both coordinate sums are even. -/
def midpoint (p q : Exponent) : Exponent := ((p.1+q.1)/2, (p.2+q.2)/2)

def Compatible (p q : Exponent) : Prop :=
  (p.1 + q.1) % 2 = 0 ∧ (p.2 + q.2) % 2 = 0

theorem small_cases {p : Exponent} (h : degree p ≤ 3) :
    p = (0,0) ∨ p = (2,1) ∨ p = (1,2) ∨ p = (1,1) ∨
    p = (1,0) ∨ p = (0,1) ∨ p = (2,0) ∨ p = (0,2) ∨
    p = (3,0) ∨ p = (0,3) := by
  rcases p with ⟨a,b⟩
  simp only [degree, Prod.mk.injEq] at *
  omega

theorem index_small {p : Exponent} (h : degree p ≤ 3) :
    1 ≤ index p ∧ index p ≤ 10 := by
  rcases small_cases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [index, degree, seedIndex]

theorem index_large {p : Exponent} (h : 4 ≤ degree p) :
    index p = triangle (degree p) + p.2 + 1 := by
  simp [index, show ¬degree p ≤ 3 by omega]

theorem index_pos (p : Exponent) : 0 < index p := by
  by_cases h : degree p ≤ 3
  · exact (index_small h).1
  · rw [index_large (by omega)]
    omega

theorem index_upper {p : Exponent} (h : 4 ≤ degree p) :
    index p ≤ triangle (degree p + 1) := by
  rw [index_large h, triangle_succ]
  have hcoord : p.2 ≤ degree p := by simp [degree]
  omega

theorem index_degree_lt {p q : Exponent}
    (hq : 4 ≤ degree q) (hpq : degree p < degree q) : index p < index q := by
  rw [index_large hq]
  by_cases hp : degree p ≤ 3
  · have hi := (index_small hp).2
    have ht := triangle_mono hq
    have ht4 : triangle 4 = 10 := rfl
    omega
  · have hu := index_upper (show 4 ≤ degree p by omega)
    have ht := triangle_mono (show degree p + 1 ≤ degree q by omega)
    omega

theorem midpoint_degree (p q : Exponent) (h : Compatible p q) :
    2 * degree (midpoint p q) = degree p + degree q := by
  rcases p with ⟨a,b⟩
  rcases q with ⟨c,d⟩
  simp only [Compatible, midpoint, degree] at *
  omega

theorem midpoint_precedes_small {p q : Exponent}
    (hp : degree p ≤ 3) (hq : degree q ≤ 3)
    (hne : p ≠ q) (h : Compatible p q) :
    index (midpoint p q) < max (index p) (index q) := by
  rcases small_cases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
  rcases small_cases hq with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [Compatible, midpoint, index, degree, seedIndex] at *

/-- Global midpoint precedence: every off-diagonal even moment is already defined. -/
theorem midpoint_precedes {p q : Exponent} (hne : p ≠ q) (h : Compatible p q) :
    index (midpoint p q) < max (index p) (index q) := by
  have hd := midpoint_degree p q h
  by_cases hp : degree p ≤ 3
  · by_cases hq : degree q ≤ 3
    · exact midpoint_precedes_small hp hq hne h
    · have hm : degree (midpoint p q) < degree q := by omega
      exact lt_of_lt_of_le (index_degree_lt (by omega) hm) (le_max_right _ _)
  · by_cases hq : degree q ≤ 3
    · have hm : degree (midpoint p q) < degree p := by omega
      exact lt_of_lt_of_le (index_degree_lt (by omega) hm) (le_max_left _ _)
    · by_cases he : degree p = degree q
      · have hm : degree (midpoint p q) = degree p := by omega
        have hc : p.2 ≠ q.2 := by
          intro hc
          apply hne
          apply Prod.ext
          · simp only [degree] at he
            omega
          · exact hc
        have hm2 : (midpoint p q).2 < max p.2 q.2 := by
          rcases h with ⟨ha,hb⟩
          simp only [midpoint]
          omega
        rw [index_large (by omega), index_large (by omega), index_large (by omega)]
        rw [hm, ← he]
        omega
      · rcases lt_or_gt_of_ne he with hlt | hgt
        · have hm : degree (midpoint p q) < degree q := by omega
          exact lt_of_lt_of_le (index_degree_lt (by omega) hm) (le_max_right _ _)
        · have hm : degree (midpoint p q) < degree p := by omega
          exact lt_of_lt_of_le (index_degree_lt (by omega) hm) (le_max_left _ _)

theorem index_injective : Function.Injective index := by
  intro p q he
  by_cases hp : degree p ≤ 3
  · by_cases hq : degree q ≤ 3
    · rcases small_cases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      rcases small_cases hq with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
        norm_num [index, degree, seedIndex] at *
    · have hi := index_degree_lt (show 4 ≤ degree q by omega)
        (show degree p < degree q by omega)
      omega
  · by_cases hq : degree q ≤ 3
    · have hi := index_degree_lt (show 4 ≤ degree p by omega)
        (show degree q < degree p by omega)
      omega
    · have hd : degree p = degree q := by
        by_contra hne
        rcases lt_or_gt_of_ne hne with hl | hg
        · have hi := index_degree_lt (show 4 ≤ degree q by omega) hl
          omega
        · have hi := index_degree_lt (show 4 ≤ degree p by omega) hg
          omega
      rw [index_large (by omega), index_large (by omega), hd] at he
      apply Prod.ext
      · simp only [degree] at hd
        omega
      · omega

theorem index_successor (p : Exponent) : ∃ q, index q = index p + 1 := by
  by_cases hp : degree p ≤ 3
  · rcases small_cases hp with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact ⟨(2,1), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(1,2), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(1,1), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(1,0), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(0,1), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(2,0), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(0,2), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(3,0), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(0,3), by norm_num [index, degree, seedIndex]⟩
    · exact ⟨(4,0), by norm_num [index, degree, seedIndex, triangle]⟩
  · rcases p with ⟨a,b⟩
    cases a with
    | zero =>
      refine ⟨(b+1,0), ?_⟩
      have hb : 4 ≤ b := by simpa [degree] using (show 4 ≤ degree (0,b) by omega)
      rw [index_large (by simp [degree]; omega), index_large (by simp [degree]; omega)]
      simp [degree, triangle_succ]
    | succ a =>
      refine ⟨(a,b+1), ?_⟩
      have hd : degree (a,b+1) = degree (a+1,b) := by simp [degree]; omega
      rw [index_large (by rw [hd]; omega), index_large (by omega), hd]
      simp
      omega

/-- Every positive integer is attained, with no finite degree bound. -/
theorem index_surjective (n : ℕ) : ∃ p, index p = n+1 := by
  induction n with
  | zero => exact ⟨(0,0), rfl⟩
  | succ n ih =>
    obtain ⟨p,hp⟩ := ih
    obtain ⟨q,hq⟩ := index_successor p
    exact ⟨q, by omega⟩

/-- A bijection from exponents to the positive natural numbers. -/
def positiveIndex (p : Exponent) : {n : ℕ // 0 < n} := ⟨index p, index_pos p⟩

theorem positiveIndex_bijective : Function.Bijective positiveIndex := by
  constructor
  · intro p q h
    exact index_injective (congrArg Subtype.val h)
  · intro ⟨n,hn⟩
    obtain ⟨p,hp⟩ := index_surjective (n-1)
    refine ⟨p, Subtype.ext ?_⟩
    change index p = n
    omega

@[simp] theorem index_seed_one : index (0,0) = 1 := rfl
@[simp] theorem index_seed_two : index (2,1) = 2 := rfl
@[simp] theorem index_seed_three : index (1,2) = 3 := rfl
@[simp] theorem index_seed_four : index (1,1) = 4 := rfl

theorem seed_cases {p : Exponent} (hp : index p ≤ 4) :
    p = (0,0) ∨ p = (2,1) ∨ p = (1,2) ∨ p = (1,1) := by
  have hs : degree p ≤ 3 := by
    by_contra h
    have hl := index_large (show 4 ≤ degree p by omega)
    have ht := triangle_mono (show 4 ≤ degree p by omega)
    have ht4 : triangle 4 = 10 := rfl
    omega
  rcases small_cases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    norm_num [index, degree, seedIndex] at *

/-- The first four exponent pairs have distinct parity classes. -/
theorem seed_parity_separated {p q : Exponent}
    (hp : index p ≤ 4) (hq : index q ≤ 4) (hne : p ≠ q) :
    ¬ Compatible p q := by
  rcases seed_cases hp with rfl | rfl | rfl | rfl <;>
  rcases seed_cases hq with rfl | rfl | rfl | rfl <;>
    norm_num [Compatible] at *

/-- The zero-based inverse of the one-based index. -/
noncomputable def exponentAt (n : ℕ) : Exponent := (index_surjective n).choose

@[simp] theorem index_exponentAt (n : ℕ) : index (exponentAt n) = n+1 :=
  (index_surjective n).choose_spec

@[simp] theorem exponentAt_index (p : Exponent) : exponentAt (index p - 1) = p := by
  apply index_injective
  rw [index_exponentAt]
  have h := index_pos p
  omega

theorem exponentAt_injective : Function.Injective exponentAt := by
  intro i j h
  have hi := congrArg index h
  simpa only [index_exponentAt, Nat.add_right_cancel_iff] using hi

@[simp] theorem exponentAt_zero : exponentAt 0 = (0,0) := by
  apply index_injective
  rw [index_exponentAt]
  rfl

@[simp] theorem exponentAt_one : exponentAt 1 = (2,1) := by
  apply index_injective
  rw [index_exponentAt]
  rfl

@[simp] theorem exponentAt_two : exponentAt 2 = (1,2) := by
  apply index_injective
  rw [index_exponentAt]
  rfl

@[simp] theorem exponentAt_three : exponentAt 3 = (1,1) := by
  apply index_injective
  rw [index_exponentAt]
  rfl

@[simp] theorem compatible_self (p : Exponent) : Compatible p p := by
  simp only [Compatible]
  omega

theorem compatible_symm {p q : Exponent} (h : Compatible p q) : Compatible q p := by
  simpa only [Compatible, Nat.add_comm] using h

@[simp] theorem midpoint_self (p : Exponent) : midpoint p p = p := by
  apply Prod.ext <;> simp [midpoint] <;> omega

theorem midpoint_comm (p q : Exponent) : midpoint p q = midpoint q p := by
  simp only [midpoint, Nat.add_comm]

/-- The form used to justify a newly appended Gram-matrix column. -/
theorem midpoint_precedes_of_index_lt {p q : Exponent}
    (hpq : index p < index q) (h : Compatible p q) :
    index (midpoint p q) < index q := by
  have hne : p ≠ q := by intro he; simp [he] at hpq
  simpa only [max_eq_right (Nat.le_of_lt hpq)] using midpoint_precedes hne h

/-- The form used to prove that an earlier Gram matrix stays unchanged. -/
theorem midpoint_index_le {p q : Exponent} (h : Compatible p q) :
    index (midpoint p q) ≤ max (index p) (index q) := by
  by_cases he : p = q
  · subst q
    simp
  · exact Nat.le_of_lt (midpoint_precedes he h)

#print axioms midpoint_precedes
#print axioms index_injective
#print axioms positiveIndex_bijective
#print axioms seed_parity_separated
#print axioms exponentAt_index
end FullFunctionalIndexing
