/- Target-beta/source-Conv nonreflection, separated from the direct source
   normalisation route. New attempt-0003 candidate; UNCOMPILED. -/
import P01Omega
import P01Translation
namespace P01F
open OrthemologyV2

theorem bstar_under {t u} (h : BStar t u) : BStar (.lam t) (.lam u) := by
  induction h with
  | refl => exact .refl _
  | tail s r ih => exact .tail (.under s) ih

/-- The target really identifies the two distinct source normal forms. -/
theorem SKK_beta_I :
    BStar (translate (.app (.app .s .k) .k)) (translate .i) := by
  let k : LTerm := translate .k
  let b : LTerm := .app (.app k (.var 0)) (.app (.var 1) (.var 0))
  let c : LTerm := .app (.app k (.var 0)) (.app k (.var 0))
  refine .tail (show Beta (translate (.app (.app .s .k) .k))
      (.app (.lam (.lam b)) k) from ?_) ?_
  · apply Beta.left
    simpa [translate, k, b, inst, sub, up, single, ren, OrthemologyV3.liftRen] using
      Beta.root (.lam (.lam (.app (.app (.var 2) (.var 0))
        (.app (.var 1) (.var 0))))) k
  · refine .tail (show Beta (.app (.lam (.lam b)) k) (.lam c) from ?_) ?_
    · simpa [b,c,k,translate,inst,sub,up,single,ren,OrthemologyV3.liftRen] using
        Beta.root (.lam b) k
    · refine .tail (show Beta (.lam c)
        (.lam (.app (.lam (.var 1)) (.app k (.var 0)))) from ?_) ?_
      · apply Beta.under
        apply Beta.left
        exact Beta.root (.lam (.var 1)) (.var 0)
      · exact .tail (.under (Beta.root (.var 1) (.app k (.var 0)))) (.refl _)

theorem target_conversion_reflection_false :
    ¬ (∀ t u, BConv (translate t) (translate u) → OrthemologyV3.Conv t u) := by
  intro h
  exact P01Source.I_SKK_not_convertible
    (h .i (.app (.app .s .k) .k) (.symm (bstar_conv SKK_beta_I)))
end P01F
