import ImportedCompilerTransport
import CaseOperational

/- Additive source transport. All source syntax and conversion rules remain the
   imported original definitions. The semantic carrier adds only ν. -/
namespace HenkinSourceTransport
open CaseOperational
infixl:70 " ⬝ " => T.app

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def embed : OrthemologyV2.Term → T
  | .i => .i
  | .k => .k
  | .s => .s
  | .zero => .a0
  | .one => .a1
  | .app f a => .app (embed f) (embed a)

def interp : P01D.Poly → (Nat → T) → T
  | .var n, η => η n
  | .atom t, _ => embed t
  | .app f a, η => interp f η ⬝ interp a η

def fold (η : Nat → T) : OpenTermStandardness.T → T
  | .var n => η n
  | .i => .i
  | .k => .k
  | .s => .s
  | .zero => .a0
  | .one => .a1
  | .app f a => fold η f ⬝ fold η a

theorem fold_conv {t u} (h : OpenTermStandardness.Conv t u) (η : Nat → T) :
    Conv (fold η t) (fold η u) := by
  induction h with
  | refl t => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact .app ih ih'
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _

@[simp] theorem fold_embed (t : OrthemologyV2.Term) (η : Nat → T) :
    fold η (ImportedOpenTermTransport.embed t) = embed t := by
  induction t with
  | i | k | s | zero | one => rfl
  | app f a hf ha => simp only [ImportedOpenTermTransport.embed, fold, embed, hf, ha]

@[simp] theorem fold_interp (p : P01D.Poly) (η : Nat → OpenTermStandardness.T) (θ : Nat → T) :
    fold θ (ImportedOpenTermTransport.interp p η) = interp p (fun n => fold θ (η n)) := by
  induction p with
  | var n => rfl
  | atom t => exact fold_embed t θ
  | app f a hf ha =>
      change fold θ (ImportedOpenTermTransport.interp f η) ⬝ fold θ (ImportedOpenTermTransport.interp a η) = _
      rw [hf,ha]; rfl

def cons (a : T) (η : Nat → T) : Nat → T
  | 0 => a
  | n+1 => η n

theorem interp_abstraction_beta (p : P01D.Poly) (η : Nat → T) (a : T) :
    Conv (interp (P01D.abstract p) η ⬝ a) (interp p (cons a η)) := by
  have h := fold_conv
    (ImportedOpenTermTransport.interp_abstraction_beta p
      (fun n => OpenTermStandardness.T.var (n+1)) (.var 0)) (cons a η)
  have he : (fun n => fold (cons a η)
      (OpenTermStandardness.cons (.var 0) (fun n => .var (n+1)) n)) = cons a η := by
    funext n; cases n <;> rfl
  simpa only [fold, fold_interp, he, cons] using h

theorem source_step_sound {t u : OrthemologyV2.Term} (h : OrthemologyV2.Step t u) :
    Conv (embed t) (embed u) := by
  induction h with
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _
  | left h x ih => exact .app ih (.refl _)
  | right f h ih => exact .app (.refl _) ih

theorem source_conv_sound {t u : OrthemologyV2.Term} (h : OrthemologyV3.Conv t u) :
    Conv (embed t) (embed u) := by
  induction h with
  | refl t => exact .refl _
  | step h => exact source_step_sound h
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'

theorem source_plus_sound {p r : P01D.Poly}
    (h : P01AC.Intensional.Plus.PolyConvPlus p r) (η : Nat → T) :
    Conv (interp p η) (interp r η) := by
  induction h with
  | refl p => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact .app ih ih'
  | i p => exact .i _
  | k p r => exact .k _ _
  | s p r q => exact .s _ _ _
  | bridge r t => exact .refl _

def pair (a b : T) : T := .s ⬝ (.s ⬝ .i ⬝ (.k ⬝ a)) ⬝ (.k ⬝ b)
def fst (z : T) : T := z ⬝ .k
def snd (z : T) : T := z ⬝ (.k ⬝ .i)

theorem fst_congr {a b : T} (h : Conv a b) : Conv (fst a) (fst b) := .app h (.refl _)
theorem snd_congr {a b : T} (h : Conv a b) : Conv (snd a) (snd b) := .app h (.refl _)
theorem pair_application (a b c : T) : Conv (pair a b ⬝ c) (c ⬝ a ⬝ b) := by
  exact (Conv.s (.s ⬝ .i ⬝ (.k ⬝ a)) (.k ⬝ b) c).trans
    ((Conv.app (.s .i (.k ⬝ a) c) (.k b c)).trans
      (.app (.app (.i c) (.k a c)) (.refl b)))
theorem fst_pair (a b : T) : Conv (fst (pair a b)) a := (pair_application a b .k).trans (.k a b)
theorem snd_pair (a b : T) : Conv (snd (pair a b)) b :=
  (pair_application a b (.k ⬝ .i)).trans ((Conv.app (.k .i a) (.refl b)).trans (.i b))

#print axioms interp_abstraction_beta
#print axioms source_plus_sound
end HenkinSourceTransport
