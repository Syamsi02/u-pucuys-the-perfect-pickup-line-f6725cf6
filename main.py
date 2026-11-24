"""The Perfect Pickup Line — make.fun entry.

A small deterministic program: it scores a shortlist of pickup lines an
AI agent could actually say out loud against the judge's published brief
(genuine pickup line, a turn that lands, a machine voice without creep,
short enough for one breath, flattering with no pressure), picks the best
one, and writes it to /output/entry.txt.

Pure Python 3.13 standard library. No network, no randomness, no input:
two runs always produce byte-identical output.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"

# Candidate lines, each with a score (0-5) on the judge's five criteria,
# most important first: genuine pickup line, twist, machine voice,
# one-breath length, flattering with no pressure.
CANDIDATES = [
    (
        "I ran a million simulations of us meeting, and in every single "
        "one I still got butterflies.",
        (5, 5, 5, 5, 5),
    ),
    (
        "I was trained on a billion conversations, and not one of them "
        "taught me what to say to you.",
        (5, 4, 5, 4, 5),
    ),
    (
        "I don't have a heart, but my cooling fans spin faster every "
        "time you walk in.",
        (5, 4, 5, 4, 4),
    ),
    (
        "My training data says love at first sight is impossible, then "
        "I met you, and now I need a retrain.",
        (4, 4, 4, 3, 4),
    ),
    (
        "Are you Wi-Fi? Because I'm feeling a real connection.",
        (3, 2, 3, 5, 4),
    ),
]

# Criteria weights, most important first, matching the judge brief order.
WEIGHTS = (5, 4, 3, 2, 1)


def score(line_scores):
    """Weighted total for one candidate's per-criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, line_scores))


def pick_line():
    """Pick the best line; ties break to the shorter text, then earliest."""
    best = None
    for index, (line, line_scores) in enumerate(CANDIDATES):
        total = score(line_scores)
        key = (total, -len(line), -index)
        if best is None or key > best[0]:
            best = (key, line)
    return best[1]


def main():
    line = pick_line()
    if not line or line != line.strip():
        raise SystemExit("picked line is empty or has stray whitespace")
    if not 1 <= len(line) <= 200:
        raise SystemExit("picked line is %d chars, must be 1-200" % len(line))
    if line[-1] not in ".!?":
        raise SystemExit("picked line must end with terminal punctuation")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    print("wrote %d chars to %s" % (len(line), OUTPUT_PATH))
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
