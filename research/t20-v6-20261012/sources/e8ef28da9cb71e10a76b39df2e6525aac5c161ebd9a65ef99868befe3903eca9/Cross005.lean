import SourceResources
set_option maxRecDepth 200000
set_option maxHeartbeats 0
open P03Source OrthemologyV2 OrthemologyV3
-- scope120: scope-or-depth; Python refuse
theorem source_scope120_matches : sourceCheck 0 (SourceProof.i (TypeCode.var 0)) = none := by decide
-- scope121: scope-or-depth; Python refuse
theorem source_scope121_matches : sourceCheck 0 (SourceProof.i (TypeCode.var 1)) = none := by decide
-- scope122: scope-or-depth; Python accept
theorem source_scope122_matches : sourceCheck 0 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
-- scope123: scope-or-depth; Python refuse
theorem source_scope123_matches : sourceCheck 0 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = none := by decide
-- scope124: scope-or-depth; Python refuse
theorem source_scope124_matches : sourceCheck 0 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = none := by decide
-- scope125: scope-or-depth; Python accept
theorem source_scope125_matches : sourceCheck 1 (SourceProof.i TypeCode.bottom) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by decide
-- scope126: scope-or-depth; Python accept
theorem source_scope126_matches : sourceCheck 1 (SourceProof.i (TypeCode.var 0)) = some (Term.i, (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
-- scope127: scope-or-depth; Python refuse
theorem source_scope127_matches : sourceCheck 1 (SourceProof.i (TypeCode.var 1)) = none := by decide
-- scope128: scope-or-depth; Python accept
theorem source_scope128_matches : sourceCheck 1 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
-- scope129: scope-or-depth; Python accept
theorem source_scope129_matches : sourceCheck 1 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = some (Term.i, (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) := by decide
-- scope130: scope-or-depth; Python accept
theorem source_scope130_matches : sourceCheck 1 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1)))) := by decide
-- scope131: scope-or-depth; Python accept
theorem source_scope131_matches : sourceCheck 2 (SourceProof.i TypeCode.bottom) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by decide
-- scope132: scope-or-depth; Python accept
theorem source_scope132_matches : sourceCheck 2 (SourceProof.i (TypeCode.var 0)) = some (Term.i, (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
-- scope133: scope-or-depth; Python accept
theorem source_scope133_matches : sourceCheck 2 (SourceProof.i (TypeCode.var 1)) = some (Term.i, (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))) := by decide
-- scope134: scope-or-depth; Python accept
theorem source_scope134_matches : sourceCheck 2 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
-- scope135: scope-or-depth; Python accept
theorem source_scope135_matches : sourceCheck 2 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = some (Term.i, (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) := by decide
-- scope136: scope-or-depth; Python accept
theorem source_scope136_matches : sourceCheck 2 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1)))) := by decide
-- scope137: scope-or-depth; Python accept
theorem source_scope137_matches : sourceCheck 100 (SourceProof.i TypeCode.bottom) = some (Term.i, (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) := by decide
-- scope138: scope-or-depth; Python accept
theorem source_scope138_matches : sourceCheck 100 (SourceProof.i (TypeCode.var 0)) = some (Term.i, (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
-- scope139: scope-or-depth; Python accept
theorem source_scope139_matches : sourceCheck 100 (SourceProof.i (TypeCode.var 1)) = some (Term.i, (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))) := by decide
-- scope140: scope-or-depth; Python accept
theorem source_scope140_matches : sourceCheck 100 (SourceProof.i (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
-- scope141: scope-or-depth; Python accept
theorem source_scope141_matches : sourceCheck 100 (SourceProof.i (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom)) = some (Term.i, (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom) (TypeCode.arrow (TypeCode.var 0) TypeCode.bottom))) := by decide
-- scope142: scope-or-depth; Python accept
theorem source_scope142_matches : sourceCheck 100 (SourceProof.i (TypeCode.all (TypeCode.var 1))) = some (Term.i, (TypeCode.arrow (TypeCode.all (TypeCode.var 1)) (TypeCode.all (TypeCode.var 1)))) := by decide
-- scope143: scope-or-depth; Python refuse
theorem source_scope143_matches : sourceCheck 101 (SourceProof.i TypeCode.bottom) = none := by decide
