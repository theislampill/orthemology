# V2 auxiliary reservation-domain correction

V1 independently passed against REVIEW_SNAPSHOT_V1.json. Its complete inputs are
preserved under frozen-candidate-v1; the V1 review remains in independent-review-v1.

The reviewer identified a non-blocking precision issue: Reservation unnecessarily
quantified over descriptor-authorized commands with invalid path cardinalities.
V2 adds ValidPath c k to that explicit external premise and supplies admitted.1
in the external-authorization corollary. This removes an unused extra assumption.

No state, event, gate, threshold, history invariant, admitted-write theorem,
cancellation theorem, target-preservation theorem or operational premise changes.
The accepted original dynamic V2 protocol and claim are unchanged. The statement
map now explicitly states the valid-path restriction. A full replay and narrow
independent recheck are required for the V2 bytes.
