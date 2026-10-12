# Actor-local clock correction, composition v2

This is a named successor to frozen v1 manifest `06591d2bb2810310182d7c534530352f99b763de702deaf4ff436e37c90222f3`. The v1 directory and ZIP remain byte-identical. Both mathematical predecessor packets remain unchanged.

## Reviewer finding and its scope

V1 `runBatch` passed `World.now` into `propose`, while Actor stored no time observation. Its live roots still checked actual time and all proved landing-safety results remain valid. The gap was the actor’s epistemic interface: the scheduler silently supplied a time fact not represented in the actor’s received state. V2 corrects that interface rather than claiming a newly discovered stale-clock landing vulnerability in v1.

## Exact correction

- Actor now stores an explicit `observedTime : Nat`.
- `propose` takes only Actor, action and path, and invokes the imported transition using `actor.observedTime`.
- `runBatch` uses that proposal without passing `World.now`.
- Actual root preparation/landing checks continue to use their warranted actual-time observation. Those checks and permission interval semantics are unchanged.
- `proposal_uses_actor_observation` exposes the exact input boundary by definition. It does not prove the stored observation authentic.
- The native artifact harness now predicts its installed Plant from the compiled transition on the actor’s own observations; the second stage consumes that guaranteed stable-batch successor rather than directly reading `installed.plant` into actor state.
- A test label now says “close exact envelope”; cancellation never claimed a global blacklist preventing reuse of a nonce with changed command contents. Unique nonces remain a correct-actor premise.

## Clock premise and boundary evidence

An honest actor’s stored time is a genuine observation, potentially older than the roots’ later observation. Proposal validity and liveness need an observation adequate for the relevant grant interval. A certificate updates policy only; obtaining a newer actor time observation is a separate input, not something the scheduler manufactures.

The new red test first reproduced v1’s substitution: with actor time 2 and actual time 100, the scheduler withheld even the proposal by inspecting hidden expired time. V2 instead makes the actor-local proposal, whose live root checks reject the expired lease, followed by exact-envelope cleanup. A future-time fixture (actor 100, actual 2) deliberately lies outside the honest-observation premise and verifies conservative proposal rejection without borrowing earlier world time. Neither fixture changes the root landing-time guard.

The full native suite contains 88 named assertions and the unchanged seven Python boundary tests. All previously claimed finite domains remain unchanged. The separate runtime mutation replay is repeated against the v2 accepted source, with the same five intentional deletions. See `VERIFICATION.md` and final receipts for actual terminal statuses.
