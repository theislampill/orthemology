import RestrictedCompiler
namespace P01AC.RestrictedIdentityV2
abbrev Exponent (r : Nat) := Fin r → Nat
abbrev Sparse (r : Nat) := List (Exponent r × Nat)
abbrev Mask (r : Nat) := Fin r → Bool

/-- Explicit executable equality on finite coordinate functions. -/
def finFunctionDecEq {α : Type} [DecidableEq α] : (r : Nat) → DecidableEq (Fin r → α)
  | 0, _f, _g => isTrue (funext fun i => Fin.elim0 i)
  | r+1, f, g =>
    if h0 : f 0 = g 0 then
      match finFunctionDecEq r (fun i => f i.succ) (fun i => g i.succ) with
      | isTrue hs => isTrue (funext fun i => Fin.cases h0 (fun j => congrFun hs j) i)
      | isFalse hs => isFalse (fun h => hs (funext fun j => congrFun h j.succ))
    else isFalse (fun h => h0 (congrFun h 0))

instance exponentDecidableEq (r : Nat) : DecidableEq (Exponent r) := finFunctionDecEq r
instance maskDecidableEq (r : Nat) : DecidableEq (Mask r) := finFunctionDecEq r

def coefficient {r} : Sparse r → Exponent r → Nat
  | [], _ => 0
  | (b,n) :: ps, a => (if b = a then n else 0) + coefficient ps a

def coeffEqual {r} (p q : Sparse r) : Bool :=
  ((p.map Prod.fst) ++ (q.map Prod.fst)).all
    (fun a => decide (coefficient p a = coefficient q a))

def zeroTest {r} (p : Sparse r) : Bool := p.all (fun t => decide (t.2 = 0))

def masks : (r : Nat) → List (Mask r)
  | 0 => [fun i => Fin.elim0 i]
  | r+1 => (masks r).map (fun s i => Fin.cases false s i) ++
    (masks r).map (fun s i => Fin.cases true s i)

end P01AC.RestrictedIdentityV2
