# Author verification notes

The first file-write attempt encountered a transient `exec-server transport disconnected` error before creating the packet. A subsequent command succeeded; the packet was then created entirely in its new additive directory.

The initial controls run used an unnecessarily expansive `expand`/`simplify` sequence and produced no completed report. It was interrupted with exit status 130 after the optimized run passed. The final checker first applies exact rational cancellation and only invokes further symbolic/trigonometric simplification if needed; this does not weaken the equality-to-zero assertions. It also emits periodic progress. The abandoned run's empty output directory was removed, and the completed optimized output was named `author-run`.

`author-run/EXACT_CHECKS.json` is the completed run with nine original predecessor hashes checked in addition to the nine copied inputs. `portable-author-run/EXACT_CHECKS.json` is a separate completed run using only the copied inputs, suitable for byte-for-byte report comparison after extraction. The count difference is exactly those nine optional original-path checks. Neither run is independent review or a formal-kernel proof.
