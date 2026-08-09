# Deep CM distinct-rereview checker repair log

The first independent bitset rereview returned `FAIL` because the
`false_installed_target_rows` counter was incremented outside the inner policy
loop. It therefore counted only the final policy for each truth target instead
of every unequal `(truth, installed=policy)` pair.

```text
scientific candidate changed: false
frozen V2 theorem/model changed: false
failed checker and result preserved: true
repair: move the counter into the policy loop
```

The failed result is retained as executable negative evidence. A corrected V2
rereview is run below; only its output may support admission.
