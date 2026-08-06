# PMR-007 Deep BB rereview harness timeout and optimization log

The first distinct all-word trace implementation exceeded the 300-second tool
limit before writing a result.  No semantic failure was reported and no result
file was produced.  The frozen candidate bytes were not changed.

The issue was repeated recomputation of all traces for each label-pair.  A new
independent harness caches state trajectories and individual interface
quotients for each transition system, then performs the same direct trace and
set-product checks.  The timed-out script remains preserved as procedural
evidence; it is not an authority result.

The cached V3 harness still exceeded the tool limit because the larger random
three-action systems enumerated all action words through length `n-1`.  A V4
harness retains the exhaustive n=3 class, uses two-action systems for the
larger independent sample, and reduces the larger sample to 1,000 systems per
state size.  This changes only the rereview execution budget, not the theorem
or frozen candidate.
