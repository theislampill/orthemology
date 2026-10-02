#!/usr/bin/env python3
"""Exact rational reference for the restricted dyadic-square cluster policy.

Statistical support promises are documented in DESIGN_AND_CONTRACT.md.
This program does not certify those promises or acquire observations.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
import re
from typing import Optional

MAX_WORD_LENGTH = 1_000_000
MAX_INPUT_BITS = 4096
MAX_DECIMAL_COMPONENT = 1234
BOUNDARY_FACTOR = 128


@dataclass(frozen=True)
class Decision:
    n: int
    k: int
    epsilon: Fraction
    delta: Fraction
    mode: str
    index: int
    centre: Fraction
    boundary: Fraction
    previous_boundary: Optional[Fraction]
    empirical_mean: Fraction
    floored_mean: Fraction
    report: Fraction
    branch: str
    visited: int
    search_bound: int
    rank: int


def _checked_fraction(value: Fraction, name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise TypeError(f"{name} must be fractions.Fraction")
    if abs(value.numerator).bit_length() > MAX_INPUT_BITS or value.denominator.bit_length() > MAX_INPUT_BITS:
        raise ValueError(f"{name} exceeds the {MAX_INPUT_BITS}-bit input limit")
    return value


def _validate_parameters(epsilon: Fraction, delta: Fraction, mode: str) -> None:
    if not isinstance(epsilon, Fraction) or not isinstance(delta, Fraction):
        raise TypeError("epsilon and delta must be fractions.Fraction")
    if not 0 < epsilon <= Fraction(1, 4):
        raise ValueError("epsilon must be in (0, 1/4]")
    if mode == "strict_width":
        if not 0 <= delta < epsilon or delta > Fraction(1, 16):
            raise ValueError("strict_width needs 0 <= delta < epsilon and delta <= 1/16")
    elif mode == "uniform_critical":
        if delta != epsilon or epsilon > Fraction(1, 16):
            raise ValueError("uniform_critical needs delta = epsilon <= 1/16")
    else:
        raise ValueError("unknown mode")


def dyadic_rank(ratio: Fraction) -> int:
    """Return the unique integer m >= 1 with 2^-m <= ratio < 2^-(m-1)."""
    if not isinstance(ratio, Fraction):
        raise TypeError("ratio must be fractions.Fraction")
    if not 0 < ratio <= Fraction(1, 2):
        raise ValueError("ratio must be in (0, 1/2]")
    numerator, denominator = ratio.numerator, ratio.denominator
    rank = max(1, denominator.bit_length() - numerator.bit_length())
    while numerator << rank < denominator:
        rank += 1
    while rank > 1 and numerator << (rank - 1) >= denominator:
        rank -= 1
    return rank


def _support(index: int) -> Fraction:
    return Fraction(1, 1 << ((index + 1) ** 2))


def _boundary(index: int) -> tuple[Fraction, Fraction, int]:
    centre = _support(index)
    ratio = _support(index + 1) / centre
    rank = dyadic_rank(ratio)
    boundary = centre * min(Fraction(3, 4), max(Fraction(3, 2) * ratio, Fraction(1, BOUNDARY_FACTOR * rank)))
    return centre, boundary, rank


def decide_counts_unbounded(n: int, k: int, epsilon: Fraction = Fraction(1, 4),
                  delta: Fraction = Fraction(0), mode: str = "strict_width") -> Decision:
    """Total rational rule on finite typed inputs, with no preset size ceiling.

    Arithmetic/search terminate mathematically; no finite-memory or latency
    guarantee is asserted. A count summary does not authenticate receipts.
    """
    if type(n) is not int or type(k) is not int:
        raise TypeError("n and k must be integers, not bool or floating point")
    if n < 1 or not 0 <= k <= n:
        raise ValueError("need n >= 1 and 0 <= k <= n")
    _validate_parameters(epsilon, delta, mode)
    mean = Fraction(k, n)
    floor = max(mean, Fraction(1, n))
    bound = (n - 1).bit_length()  # ceil(log2 n), exactly, including n = 1
    previous = None
    selected = None
    for index in range(bound + 1):
        centre, boundary, rank = _boundary(index)
        if floor > boundary:
            selected = (index, centre, boundary, rank)
            break
        previous = boundary
    if selected is None:
        raise RuntimeError("certified search bound failed")
    index, centre, boundary, rank = selected
    if mode == "strict_width":
        if centre > (epsilon - delta) / (2 * epsilon):
            report = Fraction(1, 2) + epsilon * mean
            branch = "empirical_head"
        else:
            report = Fraction(1, 2) + epsilon * centre * (1 - delta * epsilon)
            branch = "shifted_tail"
    elif centre > Fraction(1, 8):
        report = Fraction(1, 2) + epsilon * mean
        branch = "empirical_head"
    else:
        shift = epsilon * centre * (1 - epsilon ** 2)
        correction = 2 * epsilon ** 2 * centre ** 2
        if mean <= centre:
            report = Fraction(1, 2) + shift - correction
            branch = "critical_left"
        else:
            report = Fraction(1, 2) + shift + correction
            branch = "critical_right"
    if not 0 <= report <= 1:
        raise RuntimeError("coherence invariant failed")
    return Decision(n, k, epsilon, delta, mode, index, centre, boundary, previous,
                    mean, floor, report, branch, index + 1, bound, rank)


def decide_counts(n: int, k: int, epsilon: Fraction = Fraction(1, 4),
                  delta: Fraction = Fraction(0), mode: str = "strict_width") -> Decision:
    """Guarded finite-domain wrapper around the uncapped mathematical rule."""
    if type(n) is not int or type(k) is not int:
        raise TypeError("n and k must be integers, not bool or floating point")
    if n.bit_length() > MAX_INPUT_BITS:
        raise ValueError(f"n exceeds the {MAX_INPUT_BITS}-bit summary limit")
    _checked_fraction(epsilon, "epsilon")
    _checked_fraction(delta, "delta")
    return decide_counts_unbounded(n, k, epsilon, delta, mode)


def decide_word_unbounded(word: str, epsilon: Fraction = Fraction(1, 4),
                         delta: Fraction = Fraction(0), mode: str = "strict_width") -> Decision:
    """Apply the uncapped rule to any finite nonempty binary string.

    No explicit word-length ceiling; physical representability is not promised.
    """
    if not isinstance(word, str):
        raise TypeError("word must be a binary string")
    if not word:
        raise ValueError("word must be nonempty")
    if any(character not in "01" for character in word):
        raise ValueError("word contains a nonbinary character")
    return decide_counts_unbounded(len(word), word.count("1"), epsilon, delta, mode)


def decide_word(word: str, epsilon: Fraction = Fraction(1, 4),
                delta: Fraction = Fraction(0), mode: str = "strict_width") -> Decision:
    """Decide after a nonempty complete binary prefix."""
    if not isinstance(word, str):
        raise TypeError("word must be a binary string")
    if not 1 <= len(word) <= MAX_WORD_LENGTH:
        raise ValueError(f"word length must be between 1 and {MAX_WORD_LENGTH}")
    if any(character not in "01" for character in word):
        raise ValueError("word contains a nonbinary character")
    return decide_counts(len(word), word.count("1"), epsilon, delta, mode)


def decimal_integer(value: int) -> str:
    """Exact serialization without changing the global integer digit guard.

    Bounded base-10^9 chunks follow the same established strategy as the
    predecessor's corrected rational reference; no new serialization claim.
    """
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    chunks = []
    while value:
        value, remainder = divmod(value, 1_000_000_000)
        chunks.append(remainder)
    return sign + str(chunks[-1]) + "".join(f"{chunk:09d}" for chunk in reversed(chunks[:-1]))


def _rational_json(value: Fraction) -> dict[str, str]:
    return {"numerator": decimal_integer(value.numerator), "denominator": decimal_integer(value.denominator)}


def to_jsonable(decision: Decision) -> dict:
    result = {
        "family": "dyadic_square",
        "n": decimal_integer(decision.n),
        "k": decimal_integer(decision.k),
        "mode": decision.mode,
        "index": decision.index,
        "branch": decision.branch,
        "visited": decision.visited,
        "search_bound": decision.search_bound,
        "rank": decision.rank,
        "previous_boundary": None if decision.previous_boundary is None else _rational_json(decision.previous_boundary),
        "scope": "Exact rational report; component-law and truthful-prefix promises are external inputs",
    }
    for name in ["epsilon", "delta", "centre", "boundary", "empirical_mean", "floored_mean", "report"]:
        result[name] = _rational_json(getattr(decision, name))
    return result


def _decimal_input(text: str) -> int:
    """Parse an already validated decimal component in at most nine-digit chunks.

    Unlike int(full_component), this does not depend on the host's digit guard.
    """
    negative = text.startswith("-")
    digits = text[1:] if text.startswith(("-", "+")) else text
    value = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        value = value * (10 ** len(chunk)) + int(chunk)
    return -value if negative else value


def parse_fraction(text: str) -> Fraction:
    if not isinstance(text, str) or not re.fullmatch(r"[+-]?[0-9]+(?:/[0-9]+)?", text):
        raise ValueError("expected a decimal integer or numerator/positive-denominator fraction")
    pieces = text.split("/")
    if any(len(piece.lstrip("+-")) > MAX_DECIMAL_COMPONENT for piece in pieces):
        raise ValueError("fraction decimal component too long")
    numerator = _decimal_input(pieces[0])
    denominator = _decimal_input(pieces[1]) if len(pieces) == 2 else 1
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    return _checked_fraction(Fraction(numerator, denominator), "fraction")


def _parse_integer(text: str) -> int:
    value = parse_fraction(text)
    if value.denominator != 1:
        raise ValueError("summary entries must be integers")
    return value.numerator


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    observations = parser.add_mutually_exclusive_group(required=True)
    observations.add_argument("--word")
    observations.add_argument("--summary", nargs=2, metavar=("N", "ONES"))
    parser.add_argument("--epsilon", default="1/4")
    parser.add_argument("--delta")
    parser.add_argument("--mode", choices=["strict_width", "uniform_critical"], default="strict_width")
    args = parser.parse_args()
    try:
        epsilon = parse_fraction(args.epsilon)
        delta = parse_fraction(args.delta) if args.delta is not None else (epsilon if args.mode == "uniform_critical" else Fraction(0))
        if args.word is not None:
            decision = decide_word(args.word, epsilon, delta, args.mode)
        else:
            n, k = map(_parse_integer, args.summary)
            decision = decide_counts(n, k, epsilon, delta, args.mode)
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(to_jsonable(decision), indent=2))


if __name__ == "__main__":
    main()
