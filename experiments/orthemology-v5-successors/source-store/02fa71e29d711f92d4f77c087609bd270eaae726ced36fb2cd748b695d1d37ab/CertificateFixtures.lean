import CertificateSyntax
namespace OrthemicCertificate.Fixtures

/-- Fixture-only explicit table materialization; not a checker dependency. -/
def rows (q n k : ℕ) (f : ℕ → ℕ → ℕ → ℕ → ℚ) : Array ℚ :=
  ((List.range q).flatMap fun m => (List.range n).flatMap fun s =>
    (List.range k).flatMap fun a => (List.range n).map (f m s a)).toArray

def priorities (q n k : ℕ) (f : ℕ → ℕ → ℕ → ℕ) : Array ℕ :=
  ((List.range q).flatMap fun m => (List.range n).flatMap fun s =>
    (List.range k).map (f m s)).toArray

def interpretation (q n k : ℕ) : Interpretation :=
  ⟨(List.range q).map toString,(List.range n).map toString,(List.range k).map toString,
   "fixture-v1","observed state only","declared source","declared menu authority"⟩

def emptyPath {n k : ℕ} (s : Fin n) : Path (Fin n) (Fin k) := ⟨s,[]⟩
def singletonComponent {n k : ℕ} (s : Fin n) (a : Fin k) : Component n k :=
  ⟨{(s,a)},s,[⟨s,emptyPath s,emptyPath s⟩]⟩

/-- Exact approved three-model revealing-action input. -/
def reveal : Input 3 3 3 where
  rows := rows 3 3 3 fun m s a y =>
    if s = 0 ∧ a = 0 then
      if m = 0 then (if y = 1 ∨ y = 2 then 1/2 else 0)
      else if m = 1 then (if y = 1 then 1 else 0)
      else (if y = 2 then 1 else 0)
    else if y = s then 1 else 0
  priorities := priorities 3 3 3 fun _ s a => if (s = 1 ∧ a = 1) ∨ (s = 2 ∧ a = 2) then 2 else 1
  menus := [⟨[0,1,2],0,[0]⟩,⟨[0,1],1,[1]⟩,⟨[0,2],2,[2]⟩]
  interpretation := interpretation 3 3 3

def child₀ : Node 3 3 3 :=
  ⟨{0,1},{1},{(1,1)},[
    ⟨1,0,.target (emptyPath 1) (singletonComponent 1 1) 1⟩,
    ⟨1,1,.target (emptyPath 1) (singletonComponent 1 1) 1⟩]⟩
def child₁ : Node 3 3 3 :=
  ⟨{0,2},{2},{(2,2)},[
    ⟨2,0,.target (emptyPath 2) (singletonComponent 2 2) 2⟩,
    ⟨2,2,.target (emptyPath 2) (singletonComponent 2 2) 2⟩]⟩
def parent (alphaReceipt : Fin 3 := 1) : Node 3 3 3 :=
  ⟨{0,1,2},{0},{(0,0)},[
    ⟨0,0,.exit (emptyPath 0) (0,0) alphaReceipt⟩,
    ⟨0,1,.exit (emptyPath 0) (0,0) 1⟩,
    ⟨0,2,.exit (emptyPath 0) (0,0) 2⟩]⟩
def revealedBody : Body 3 3 3 := [child₀,child₁,parent]

/-- Two hidden Bernoulli models, unobserved model-dependent action priorities. -/
def latent : Input 2 2 2 where
  rows := rows 2 2 2 fun m _ _ y => if m = 0 then (if y = 1 then 1/3 else 2/3)
    else (if y = 1 then 2/3 else 1/3)
  priorities := priorities 2 2 2 fun m _ a => if a = m then 2 else 1
  menus := [⟨[0,1],0,[0,1]⟩,⟨[0,1],1,[0,1]⟩]
  interpretation := {interpretation 2 2 2 with observation := "Bernoulli outcome only; latent priority is not observed"}

def latentComponent (a : Fin 2) : Component 2 2 :=
  ⟨{(0,a),(1,a)},0,[⟨0,emptyPath 0,emptyPath 0⟩,
    ⟨1,⟨1,[(a,0)]⟩,⟨0,[(a,1)]⟩⟩]⟩
def latentNode : Node 2 2 2 :=
  ⟨{0,1},{0,1},Finset.univ,[
    ⟨0,0,.target (emptyPath 0) (latentComponent 0) 0⟩,
    ⟨1,0,.target (emptyPath 1) (latentComponent 0) 1⟩,
    ⟨0,1,.target (emptyPath 0) (latentComponent 1) 0⟩,
    ⟨1,1,.target (emptyPath 1) (latentComponent 1) 1⟩]⟩

def latentEqualRows : Input 2 2 2 :=
  {latent with rows := rows 2 2 2 fun _ _ _ y => if y = 1 then 1/3 else 2/3}

/-- Distinct supplied nonmaximal targets and distinct valid paths, same input. -/
def choices : Input 1 3 2 where
  rows := rows 1 3 2 fun _ s _ y => if s = 0 then (if y = 1 ∨ y = 2 then 1/2 else 0)
    else if y = s then 1 else 0
  priorities := priorities 1 3 2 fun _ _ _ => 2
  menus := [⟨[0],0,[0,1]⟩,⟨[0],1,[0,1]⟩,⟨[0],2,[0,1]⟩]
  interpretation := interpretation 1 3 2

def choicesNode (destination : Fin 3) (a : Fin 2) : Node 1 3 2 :=
  ⟨{0},Finset.univ,Finset.univ,[
    ⟨0,0,.target ⟨0,[(a,destination)]⟩ (singletonComponent destination a) destination⟩,
    ⟨1,0,.target (emptyPath 1) (singletonComponent 1 a) 1⟩,
    ⟨2,0,.target (emptyPath 2) (singletonComponent 2 a) 2⟩]⟩
end OrthemicCertificate.Fixtures
