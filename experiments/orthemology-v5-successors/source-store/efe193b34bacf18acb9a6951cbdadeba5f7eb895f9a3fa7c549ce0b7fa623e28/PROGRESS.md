# Execution ledger — plan: IMPLEMENTATION_PLAN.md

2026-10-07: Plan saved before implementation code. Proposal preserved; active citations and semantic-control scope corrected under review approval.

Pre-flight: the core module supplies predicates/theorems to controls and readbacks; all downstream tests use the same VeracityBoundary namespace. Control worlds are explicitly relative interpretations, and stronger ownership remains a separate model transformation.

Ruling: no git worktree or commit because the approved deliverable is isolated outside a repository; preserving the complete local package and hashes supplies the review boundary. No repository state is changed.

Task 1: core compiled without warnings; API red (missing module) then green. Evidence: development/001-api-red.log, 002-core.log, 003-api-green.log.

Task 2 diagnosis: Bool finite deciders exist (007); bundled conjunction instance synthesis exceeded the default size. Single-variable -DsynthInstance.maxSize=100000 probe passed (009), then the same local source option compiled all controls (010) and acceptance (011). No proposition or proof target was weakened.

Task 2: complete. Fourteen finite declarations compile; six exact removal/stress bundles and positive/nonconverse/local-global/strong-ownership controls pass. All eight false strengthenings fail specifically through ordinary kernel decide.

Task 3: source bindings and replayer complete. First fresh replay validation/20261007T092301.137940Z passed 17 steps and read back 23 declarations; 47 sealed source paragraphs and three external retained sources matched. Core proof bodies inspected. Only standard propext/Classical.choice/Quot.sound occur as reported individually; the constructive diagnostic and semantic projections use no axioms. Final replay and sealing follow without scientific-source changes.
