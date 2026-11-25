"""The Moon Finally Answers Back -- make.fun entry.

Writes a single line of text (1 to 240 characters) in which the Moon
finally answers everyone who has ever stared up at it: an answer to
the wishes, the howls and the late-night promises. Deterministic,
no network, no randomness, no input.

The line: "I heard every wish, every howl, every 2 a.m. promise.
I'm a rock -- I don't do refunds, I do tides."

It opens by proving the Moon was listening all along (wishes, howls,
2 a.m. promises -- the whole brief, in one breath), then undercuts
four billion years of reverence with the flattest possible job
description: a rock. The comeback lands in the last clause: no
refunds, only tides -- the one thing the Moon actually delivers,
served deadpan.
"""

import os

# The entry: the Moon's comeback, in one line. 98 characters, under
# the 240 cap.
LINE = "I heard every wish, every howl, every 2 a.m. promise. I'm a rock \u2014 I don't do refunds, I do tides."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 240:
        raise ValueError(f"line is {len(LINE)} characters, over the 240 cap")
    if len(LINE) < 1:
        raise ValueError("entry must not be empty")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in LINE or "\r" in LINE:
        # Craft: exactly one line -- the comeback has to land in a
        # single read, so no embedded line breaks are allowed.
        raise ValueError("entry must be a single line, no line breaks")
    if not LINE.rstrip().endswith((".", "!", "?")):
        # The line is a comeback: it must end on a beat, not trail off.
        raise ValueError("entry must end with terminal punctuation")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
