import SourceController
-- Intentionally expected to fail native evaluation. This is a code-generation
-- boundary, not a semantic counterexample to the model's proved propositions.
#eval SharedAlias.Progress.labelList ({0, 1} : Finset (Fin 2))
