# Initial author control run

The first run passed nine control families, then stopped in the rare-zero-mass control with `NameError: name 'prod' is not defined`. The partial stdout is retained in INITIAL_CONTROL_STDOUT.log. The cause was a missing standard-library import in the new test harness, not a failed mathematical inequality or a statistical sample outcome.

The import of math.prod was added, and the entire control suite was rerun with shell pipe-failure propagation before accepting its final receipt. No prior-stage artifact or mathematical constant was changed to make this check pass.
