#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / "PMR-007_DEEP_A_V1_FROZEN_HASHES.sha256"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_hashes() -> list[str]:
    failures=[]
    for line in HASH_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split(maxsplit=1)
        rel = rel.strip().lstrip("*")
        p = ROOT / rel
        actual = sha256(p)
        if actual != expected:
            failures.append(f"{rel}: {actual} != {expected}")
    return failures


def fibre_constant(profile: tuple[int, ...], target: tuple[int, ...]) -> bool:
    classes: dict[int, set[int]] = {}
    for p,t in zip(profile,target):
        classes.setdefault(p,set()).add(t)
    return all(len(v)==1 for v in classes.values())


def brute_factorable(profile: tuple[int, ...], target: tuple[int, ...]) -> bool:
    image=sorted(set(profile))
    for bits in itertools.product((0,1), repeat=len(image)):
        f=dict(zip(image,bits))
        if all(f[p] == t for p,t in zip(profile,target)):
            return True
    return False


def main() -> None:
    rng=random.Random(7007001)
    failures=[]
    cases=0
    # Exhaustive small profile maps, including redundant codomain labels.
    for n in range(1,7):
        for k in range(1,min(4,n+1)+1):
            for profile in itertools.product(range(k), repeat=n):
                for target in itertools.product((0,1), repeat=n):
                    cases += 1
                    a=fibre_constant(profile,target)
                    b=brute_factorable(profile,target)
                    if a != b:
                        failures.append({"n":n,"k":k,"profile":profile,"target":target,"fibre":a,"brute":b})
                        if len(failures)>=10: break
                if len(failures)>=10: break
            if len(failures)>=10: break
        if len(failures)>=10: break
    random_cases=0
    for n in range(7,13):
        for _ in range(3000):
            k=rng.randint(1,min(7,n))
            profile=tuple(rng.randrange(k) for _ in range(n))
            target=tuple(rng.randrange(2) for _ in range(n))
            random_cases += 1
            a=fibre_constant(profile,target)
            b=brute_factorable(profile,target)
            if a != b:
                failures.append({"n":n,"k":k,"profile":profile,"target":target,"fibre":a,"brute":b})
                if len(failures)>=10: break
        if len(failures)>=10: break
    # Scope/firewall controls are semantic assertions deliberately separate
    # from theorem validity.
    firewalls={
      "independent_target_required": True,
      "truth_link_not_warrant": True,
      "function_not_teleology": True,
      "fitrah_school_internal_without_bridge": True,
      "proper_function_not_wisdom": True,
    }
    out={
      "schema":"PMR007_DEEP_A_DISTINCT_REREVIEW_RESULTS_V1",
      "frozen_hash_failures":verify_hashes(),
      "exhaustive_cases":cases,
      "random_cases":random_cases,
      "factorization_mismatches":len(failures),
      "first_failures":failures,
      "firewall_controls":firewalls,
    }
    out["overall"]="PASS" if not out["frozen_hash_failures"] and not failures and all(firewalls.values()) else "FAIL"
    (Path(__file__).with_name("PMR-007_DEEP_A_DISTINCT_REREVIEW_RESULTS.json")).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
