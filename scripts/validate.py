"""Validate bounded-brainstorming JSONL tuples against docs/schema.md.

Usage: uv run scripts/validate.py data/seed/*.jsonl
"""
import json
import sys

SOURCES = {"hold-out", "synthetic", "manual"}


def check(rec: dict) -> list[str]:
    errs = []
    for key in ("task", "format", "n", "output", "source"):
        if key not in rec:
            errs.append(f"missing {key}")
    if errs:
        return errs
    fields = rec["format"].get("fields")
    if not fields:
        errs.append("format.fields empty")
    if rec["source"] not in SOURCES:
        errs.append(f"source must be one of {sorted(SOURCES)}")
    out = rec["output"]
    if len(out) != rec["n"]:
        errs.append(f"output has {len(out)} items, n={rec['n']}")
    for i, item in enumerate(out):
        if fields and set(item) != set(fields):
            errs.append(f"output[{i}] keys {sorted(item)} != {sorted(fields)}")
    priors = {json.dumps(p, sort_keys=True).lower() for p in rec.get("priors", [])}
    for i, item in enumerate(out):
        if json.dumps(item, sort_keys=True).lower() in priors:
            errs.append(f"output[{i}] repeats a prior")
    return errs


def main(paths: list[str]) -> int:
    bad = 0
    for path in paths:
        with open(path) as f:
            for ln, line in enumerate(f, 1):
                if not line.strip():
                    continue
                for e in check(json.loads(line)):
                    print(f"{path}:{ln}: {e}")
                    bad += 1
    print(f"{bad} error(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
