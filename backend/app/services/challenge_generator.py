"""
Adaptive math/logic challenge generator for the Chaperone "speed bump".

The generator is deterministic (seeded), needs no LLM and no API key, and
supports adaptive difficulty: difficulty rises with success and falls with
failure, matching the "adaptive speed bump" concept from the Ubicomp paper.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional


# --- Difficulty bands ---------------------------------------------------------

# Each band: (operand_min, operand_max, allowed_operators)
DIFFICULTY_BANDS: List[Dict[str, Any]] = [
    # Level 1: single-digit addition/subtraction
    {"level": 1, "lo": 1, "hi": 10, "ops": ["+", "-"]},
    # Level 2: two-digit add/sub, single-digit multiply
    {"level": 2, "lo": 2, "hi": 20, "ops": ["+", "-", "x"]},
    # Level 3: two-digit multiply, simple division (exact)
    {"level": 3, "lo": 3, "hi": 25, "ops": ["+", "-", "x", "/"]},
    # Level 4: larger operands, mixed operations
    {"level": 4, "lo": 10, "hi": 99, "ops": ["+", "-", "x", "/"]},
    # Level 5: multi-step expressions
    {"level": 5, "lo": 5, "hi": 50, "ops": ["+", "-", "x"]},
]


def _band_for_level(level: int) -> Dict[str, Any]:
    clamped = max(1, min(level, len(DIFFICULTY_BANDS)))
    return DIFFICULTY_BANDS[clamped - 1]


def _division_problem(rng: random.Random, lo: int, hi: int) -> tuple[int, int]:
    """Generate a clean division problem (quotient is an integer)."""
    divisor = rng.randint(max(1, lo // 2), max(lo, hi // 2))
    quotient = rng.randint(max(1, lo // 2), max(lo, hi // 2))
    dividend = divisor * quotient
    return dividend, divisor


def generate_math_challenge(level: int = 1, rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generate one adaptive math challenge.

    Returns a dict: {type, prompt, answer, options, difficulty}
    `options` is a list of 4 answer choices (shuffled) so the modal can
    render buttons instead of a free-text input.
    """
    rng = rng or random.Random()
    band = _band_for_level(level)
    op = rng.choice(band["ops"])

    a = rng.randint(band["lo"], band["hi"])
    b = rng.randint(band["lo"], band["hi"])

    if op == "/":
        a, b = _division_problem(rng, band["lo"], band["hi"])
        prompt = f"What is {a} ÷ {b}?"
        answer = str(a // b)
    elif op == "x":
        if band["level"] >= 5:
            c = rng.randint(band["lo"], band["hi"])
            result = (a + b) * c
            prompt = f"Compute: ({a} + {b}) × {c}"
            answer = str(result)
        else:
            prompt = f"What is {a} × {b}?"
            answer = str(a * b)
    elif op == "-":
        if a < b:
            a, b = b, a
        prompt = f"What is {a} − {b}?"
        answer = str(a - b)
    else:  # +
        prompt = f"What is {a} + {b}?"
        answer = str(a + b)

    # Build plausible distractors around the correct answer
    correct = int(answer)
    distractors: set[int] = set()
    while len(distractors) < 3:
        delta = rng.choice([1, 2, 3, 5, 10])
        variant = correct + delta if rng.random() < 0.5 else correct - delta
        if variant >= 0 and variant != correct:
            distractors.add(variant)
    options = [str(correct), *[str(d) for d in distractors]]
    rng.shuffle(options)

    return {
        "type": "math",
        "prompt": prompt,
        "answer": answer,
        "options": options,
        "difficulty": band["level"],
    }


def generate_logic_challenge(level: int = 1, rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generate a simple logic challenge (number/letter pattern)."""
    rng = rng or random.Random()

    # Number sequence with arithmetic progression
    start = rng.randint(1, 10)
    step = rng.choice([2, 3, 5, 10])
    seq = [start + i * step for i in range(4)]
    prompt = f"Complete the sequence: {', '.join(str(n) for n in seq)}, …"
    answer = str(seq[-1] + step)

    correct = int(answer)
    distractors: set[int] = set()
    while len(distractors) < 3:
        delta = rng.choice([1, 2, step])
        variant = correct + delta if rng.random() < 0.5 else correct - delta
        if variant != correct:
            distractors.add(variant)
    options = [str(correct), *[str(d) for d in distractors]]
    rng.shuffle(options)

    return {
        "type": "logic",
        "prompt": prompt,
        "answer": answer,
        "options": options,
        "difficulty": max(1, min(level, 4)),
    }


def generate_challenge(challenge_type: str = "math", level: int = 1,
                       rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Generate a challenge of the requested type (math or logic)."""
    if challenge_type == "logic":
        return generate_logic_challenge(level=level, rng=rng)
    return generate_math_challenge(level=level, rng=rng)


def adaptive_level(recent_accuracy: Optional[float] = None, current_level: int = 1) -> int:
    """Pick the next difficulty level based on recent accuracy.

    - accuracy >= 0.8 -> bump up one level
    - accuracy <= 0.5 -> drop one level
    - otherwise keep current
    """
    if recent_accuracy is None:
        return current_level
    if recent_accuracy >= 0.8:
        return min(current_level + 1, len(DIFFICULTY_BANDS))
    if recent_accuracy <= 0.5:
        return max(current_level - 1, 1)
    return current_level


def points_for(is_correct: bool, difficulty: int) -> int:
    """Points awarded for an answer (difficulty-scaled)."""
    if not is_correct:
        return 0
    return 5 + difficulty * 2
