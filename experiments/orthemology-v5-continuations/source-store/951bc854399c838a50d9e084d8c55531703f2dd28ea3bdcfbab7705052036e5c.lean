import CodecParameter
import CodecPrimrec

namespace P02.Codec
open P02A2.ObserverCore P02A2.PRProgram P02A2.PRSpecialize P02A2.LoopRenaming

theorem stmtBytes_seq_primrec {s t : ℕ → Stmt}
    (hs : Primrec (fun a => stmtBytes (s a))) (ht : Primrec (fun a => stmtBytes (t a))) :
    Primrec (fun a => stmtBytes (.seq (s a) (t a))) := by
  exact Primrec.list_cons.comp (Primrec.const 17)
    (Primrec.list_append.comp (Primrec.list_append.comp (Primrec.const (uv 2)) hs) ht)

theorem stmtBytes_constant_primrec (r : ℕ) : Primrec (fun a => stmtBytes (.set r (.constant a))) := by
  exact Primrec.list_cons.comp (Primrec.const 16)
    (Primrec.list_append.comp (Primrec.const (uv r))
      (Primrec.list_cons.comp (Primrec.const 1) uv_primrec))

theorem parameterAssignments (n a : ℕ) :
    inputAssignments (parameterArgs n a) =
      (0,Expr.constant a) :: List.ofFn (fun i : Fin n => (i.val+1,Expr.reg i.val)) := by
  simp [inputAssignments, List.ofFn_succ, parameterArgs]

theorem specialize_body_bytes_primrec {n : ℕ} (p : Program (n+1)) :
    Primrec (fun a => stmtBytes (specialize p a).body) := by
  unfold specialize call inlineCode
  apply stmtBytes_seq_primrec (Primrec.const _)
  apply stmtBytes_seq_primrec ?_ (Primrec.const _)
  simp only [parameterAssignments, loadArgs]
  exact stmtBytes_seq_primrec (stmtBytes_constant_primrec _) (Primrec.const _)

theorem specialize_bytes_primrec {n : ℕ} (p : Program (n+1)) :
    Primrec (fun a => encodeBytes (pack (specialize p a))) := by
  exact Primrec.list_append.comp (Primrec.const (magic ++ uv n ++ uv n)) (specialize_body_bytes_primrec p)

/-- The exact recovered sentinel numeric codec turns literal specialization of
one fixed program into a primitive-recursive numeric index function. -/
theorem parameterIndex_primrec (p : Program 3) : Primrec (parameterIndex p) :=
  encodeNumeric_primrec.comp (specialize_bytes_primrec p)

end P02.Codec
