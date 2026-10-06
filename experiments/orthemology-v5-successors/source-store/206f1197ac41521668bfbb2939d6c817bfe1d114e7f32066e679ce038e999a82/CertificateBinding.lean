import CertificateSyntax

namespace OrthemicCertificate

/-- Optional transport envelope binds the actual structured input. It contains
neither a trusted acceptance bit nor a semantic proof. -/
structure BoundBody (q n k : ℕ) where
  input : Input q n k
  body : Body q n k
  deriving DecidableEq

/-- Recheck on the actual input only after exact structured identity succeeds.
Labels, equal hashes, and purported old acceptance are not substituted for it. -/
def boundCheck {q n k : ℕ} (actual : Input q n k) (package : BoundBody q n k)
    (B : Support q) (s : Fin n) : Bool :=
  if actual.sameInput package.input then check actual package.body B s else false

@[simp] theorem boundCheck_iff {q n k : ℕ} (actual : Input q n k) (package : BoundBody q n k)
    (B : Support q) (s : Fin n) : boundCheck actual package B s = true ↔
      actual = package.input ∧ check actual package.body B s = true := by
  simp [boundCheck]

theorem boundCheck_stale {q n k : ℕ} {actual : Input q n k} {package : BoundBody q n k}
    (h : actual ≠ package.input) (B : Support q) (s : Fin n) : boundCheck actual package B s = false := by
  simp [boundCheck,Input.sameInput,h]
end OrthemicCertificate
