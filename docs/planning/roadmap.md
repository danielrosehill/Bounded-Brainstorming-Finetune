# Roadmap (POC)

Written 2026-10-27. This project is a **proof of concept**: the question is whether a small LoRA fine-tune beats its own base model, and comes close to a frontier model, on bounded brainstorming, measured by the eval in the README. Not a production model.

Order matters: decide the architecture before generating data, because the base model's context length and chat template fix the tuple size and format of the training set.

| Phase | Goal | Output | Gate to next phase | Status |
|---|---|---|---|---|
| 0. Spec | task, I/O schema, eval idea | `README.md`, `docs/schema.md` | | done 2026-10-27 |
| 1. Taxonomy | technical axes, use-case catalogue, context pipeline | `docs/planning/` | | done 2026-10-27 |
| 2. Prior art | HF Hub survey, literature on viability | `docs/research/prior-art-*.md` | no existing model already does it well | done 2026-10-27: no one has done it |
| 3. Architecture | pick base model, stack, venue, input budget | `docs/research/architecture-options.md`, entry in `decisions.md` | Hebrew test + 16k dry run pass | tentative: Qwen3.5-4B |
| 4. Eval harness | `eval/`: format, novelty, diversity, judge; 5–10 real held-out lists (MWP, ASR sets, CV) in `data/private/` | baseline scores for base model (plain and Verbalized Sampling prompt) and a frontier model | frontier clearly beats base (else nothing to distil) | |
| 5. Pilot data | ~200 tuples via cheap batch generation (Claude Haiku via the Message Batches API, or similar), filtered | `data/private/pilot.jsonl`, cost note | filter pass rate and spot-check quality acceptable; spend within $5 | |
| 6. Pilot SFT | LoRA on the chosen base, pilot data only | adapter + eval scores | any improvement over base on novelty/diversity without losing fit | |
| 7. Scale data | 2–5k tuples balanced per `use-cases.md` target mix; hold-out tuples from real lists | HF dataset (private) | cost estimate approved before running | |
| 8. Full SFT + DPO | SFT, then DPO on diverse-vs-collapsed pairs | adapter, merged weights, GGUF | beats base; report vs frontier | |
| 9. Release | model card, dataset card, `v1.0` tag | public HF model | Daniel decides to publish | |

## Synthetic data plan (phase 5 and 7)

1. **Tuple scaffolds:** sample (archetype, domain, size bin, item shape) from the target mix; a generator writes the task, format and priors (or takes priors from a real public list).
2. **Over-generate:** ask the generator for ~2× N candidates.
3. **Filter:** format check, embedding novelty vs priors, intra-set dedupe, optional judge for fit. Keep the best N as the target.
4. **Hold-out tuples:** from real lists (public RSS, HF dataset lists, own archives), hide K items; they become gold targets that do not come from any generator, which guards against just copying Haiku's style.
5. **Preference pairs (phase 8):** rejected = the filtered-out candidates (paraphrases of priors, collapsed sets); chosen = the kept set.

Spend: phase 5 pilot under the $5 per-task limit; phase 7 gets an estimate first (basis in `docs/research/architecture-options.md`).
