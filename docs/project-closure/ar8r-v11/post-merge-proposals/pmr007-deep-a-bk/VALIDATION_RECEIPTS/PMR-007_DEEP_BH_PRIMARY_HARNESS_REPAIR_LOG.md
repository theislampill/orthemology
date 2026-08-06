# PMR-007 Deep BH — primary harness repair log

The first pre-freeze execution raised a `KeyError` because a tree edge stored in
canonical orientation was read only in parent-to-child orientation. The checker
was repaired to use the declared antisymmetric oriented-edge accessor. The
candidate theorem and model bytes were unchanged. The repaired checker was run
from the beginning and only then frozen as V1 primary evidence.

```text
pre-freeze failed execution:
PRESERVED_AS_RECORDED_HARNESS_FINDING

candidate scientific defect:
NONE ESTABLISHED BY THAT EXCEPTION

repaired primary run:
PASS
```
