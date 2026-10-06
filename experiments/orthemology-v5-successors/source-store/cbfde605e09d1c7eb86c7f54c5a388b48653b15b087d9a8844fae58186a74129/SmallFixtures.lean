import SignedService
namespace OrthemicCertificate.Signed.Fixtures

def singleInput (priority : Nat) : Input 1 1 1 where
  rows := #[1]
  priorities := #[priority]
  menus := [⟨[0],0,[0]⟩]
  interpretation := ⟨["model"],["state"],["action"],"r1","fully observed", "declared", "declared"⟩

def emptyPath : Path (Fin 1) (Fin 1) := ⟨0,[]⟩
def oneStepPath : Path (Fin 1) (Fin 1) := ⟨0,[(0,0)]⟩
def singletonComponent : Component 1 1 := ⟨{(0,0)},0,[⟨0,emptyPath,emptyPath⟩]⟩
def singletonNode : Node 1 1 1 :=
  ⟨{0},{0},{(0,0)},[⟨0,0,.target emptyPath singletonComponent 0⟩]⟩
def singletonBody : Body 1 1 1 := [singletonNode]
def evenInput := singleInput 0
def oddInput := singleInput 1

def resultTag : SignedResult q n k → Nat
  | .invalidInput => 0
  | .emptySupport => 1
  | .positive _ => 2
  | .negative _ => 3

end OrthemicCertificate.Signed.Fixtures
