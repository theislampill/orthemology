import CodecStmt
import CodecNumeric
import PRSpecialize

/-! P02-L1 program envelope, expression/statement stream roundtrip, and numeric
sentinel composition. Binary seq is serialized as the valid variadic seq of
length two; skip is the empty seq. The parser accepts all finite sequence
lengths and lowers them with sequenceList, whose execution theorem is proved.
The roundtrip theorem concerns generated codes; equality with every Python
failure/resource path is outside its statement. -/
namespace P02.Codec
open P02A2.ObserverCore

structure PackedProgram where
  arity : ℕ
  output : ℕ
  body : Stmt
  deriving DecidableEq, Repr

def pack {n : ℕ} (p : P02A2.PRProgram.Program n) : PackedProgram := ⟨n,p.output,p.body⟩

def magic : List ℕ := [80,48,50,76,1]

def stripMagic (bs : List ℕ) : Option (List ℕ) :=
  if bs.take 5 = magic then some (bs.drop 5) else none

theorem stripMagic_append (bs : List ℕ) : stripMagic (magic++bs) = some bs := by
  simp [stripMagic, magic]

def encodeBytes (p : PackedProgram) : List ℕ := magic ++ uv p.arity ++ uv p.output ++ stmtBytes p.body

def decodeBytes (bs : List ℕ) : Option PackedProgram := do
  let bs ← stripMagic bs
  let (arity,bs) ← uvRead bs
  let (output,bs) ← uvRead bs
  let (body,rest) ← readStmt bs.length bs
  if rest = [] then some ⟨arity,output,body⟩ else none

theorem encodeBytes_bytes (p : PackedProgram) : Bytes (encodeBytes p) := by
  apply bytes_append (bytes_append (bytes_append ?_ (uv_bytes p.arity)) (uv_bytes p.output)) (stmtBytes_bytes p.body)
  intro b hb
  simp only [magic, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hb
  omega

theorem readStmt_self (s : Stmt) : readStmt (stmtBytes s).length (stmtBytes s) = some (s,[]) := by
  simpa using readStmt_append s [] (stmtBytes s).length (stmtDepth_le_length s)

theorem decodeBytes_encodeBytes (p : PackedProgram) : decodeBytes (encodeBytes p) = some p := by
  simp [decodeBytes, encodeBytes, List.append_assoc, stripMagic_append, uvRead_append, readStmt_self]

def programIndex (p : PackedProgram) : ℕ := encodeNumeric (encodeBytes p)
def decodeIndex (n : ℕ) : Option PackedProgram := do let bs ← decodeNumeric n; decodeBytes bs

theorem decodeIndex_programIndex (p : PackedProgram) : decodeIndex (programIndex p) = some p := by
  simp [decodeIndex, programIndex, decodeNumeric_encodeNumeric, encodeBytes_bytes, decodeBytes_encodeBytes]

def binaryStore (n word : ℕ) : Store := fun r => if r=0 then n else if r=1 then word else 0

def evaluateIndex (index n word : ℕ) : ℕ :=
  match decodeIndex index with
  | none => 0
  | some p => if p.arity=2 then (exec p.body (binaryStore n word) p.output)%2 else 0

theorem binaryStore_extend (n word : ℕ) :
    binaryStore n word = P02A2.LoopPrimrec.extend ![n,word] := by
  funext r
  by_cases h0 : r=0
  · subst r; simp [binaryStore, P02A2.LoopPrimrec.extend]
  · by_cases h1 : r=1
    · subst r; simp [binaryStore, P02A2.LoopPrimrec.extend]
    · have h2 : ¬ r < 2 := by omega
      simp [binaryStore, P02A2.LoopPrimrec.extend, h0,h1,h2]

theorem evaluateIndex_programIndex (p : P02A2.PRProgram.Program 2) (n word : ℕ) :
    evaluateIndex (programIndex (pack p)) n word = P02A2.PRProgram.denote p ![n,word] % 2 := by
  rw [evaluateIndex, decodeIndex_programIndex]
  simp [pack, binaryStore_extend, P02A2.PRProgram.denote]

end P02.Codec
