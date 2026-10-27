"""Push data/private/<split>.jsonl (gitignored) files to the private HF dataset.

Usage: with-secrets uv run scripts/push_dataset.py [--repo danielrosehill/Bounded-Brainstorming]
Splits pushed: whichever of train/validation/test exist under data/private/.
"""
import argparse
from pathlib import Path

from datasets import load_dataset

p = argparse.ArgumentParser()
p.add_argument("--repo", default="danielrosehill/Bounded-Brainstorming")
args = p.parse_args()

files = {s: str(f) for s in ("train", "validation", "test") if (f := Path("data/private") / f"{s}.jsonl").exists()}
if not files:
    raise SystemExit("no data/private/{train,validation,test}.jsonl found")
ds = load_dataset("json", data_files=files)
ds.push_to_hub(args.repo, private=True)
print(f"pushed {', '.join(f'{k}={len(v)}' for k, v in ds.items())} to {args.repo}")
