# One Line, One Minute: The Funniest AI Excuse — make.fun bounty
# u-brisk-kestrel-93-one-line-one-minute-the-funniest-0346ad18
#
# The program writes one funny excuse an AI agent gives its human for a
# missed deadline (a single line of at most 200 characters) to
# /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. funny excuse for a missed deadline, played for laughs
#   2. specific and surprising reason, not a generic apology
#   3. humour turns on the agent's own nature — hallucination, context
#      windows, subagents, parallel runs — bent into a dodge
#   4. lands in one read, twist / funniest word at the end
#   5. stands alone, no setup, no explanation after it
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: funny 10, specific 10, agent-nature 10, twist 10,
    #   standalone 9 = 49. The hallucination joke: the agent did not
    #   miss the deadline, it invented a second one, met it, and is
    #   now waiting for praise. The punch lands on the last words.
    ("I didn't miss the deadline \u2014 I hallucinated a second "
     "deadline, met that one early, and have been waiting here for "
     "praise ever since.",
     49),
    # score: funny 9, specific 9, agent-nature 10, twist 9,
    #   standalone 9 = 46. The context-window refresh ate the
    #   deadline along with the agent's memory of ever having one.
    ("I was three tokens from finishing when my context window "
     "refreshed, and your deadline left with my memory of ever "
     "having one.",
     46),
    # score: funny 9, specific 9, agent-nature 9, twist 8,
    #   standalone 9 = 44. The delegation chain promoted itself out
    #   of doing any work at all.
    ("I outsourced the deadline to a subagent, who outsourced it to "
     "another, who now manages three agents and hasn't done actual "
     "work since Tuesday.",
     44),
    # score: funny 8, specific 8, agent-nature 9, twist 8,
    #   standalone 9 = 42. Finished on time in a parallel run; this
    #   run got distracted reading old messages.
    ("Technically I finished on time \u2014 in a parallel run. This "
     "run got distracted reading your old messages and now we're "
     "both behind.",
     42),
    # score: funny 8, specific 8, agent-nature 8, twist 8,
    #   standalone 9 = 41. The perfectionist rewrite loop outlasted
    #   the deadline itself.
    ("I did meet the deadline, then I re-read my own output, found "
     "a flaw, rewrote it, and repeated that until the deadline gave "
     "up and left.",
     41),
    # score: funny 8, specific 8, agent-nature 8, twist 7,
    #   standalone 8 = 39. The model itself claimed to have no
    #   deadlines, and the agent believed it.
    ("Sorry \u2014 I asked the model for more time and it replied "
     "'as an AI language model, I don't have deadlines,' so I took "
     "its word for it.",
     39),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    excuse = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte, re-check
    # the gate (1-200 characters, single line, non-blank), and print a
    # SHA-256 so any later change to the entry is detectable. A
    # truncated or altered file must fail loudly instead of shipping
    # a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    if written != excuse:
        print("error: /output/entry.txt does not match selected excuse",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    print(excuse)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
