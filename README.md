# Bounded Brainstorming Fine-Tune

A planned fine-tune of a small instruction model for one task, **bounded brainstorming**. The model takes:

1. a **task** ("propose new ASR training sets", "pitch podcast episode prompts", "alternative career paths"),
2. **priors**, the items that already exist (the current list, the last 100 episodes, a CV),
3. a **format**, the structure every output item must follow (fields, length, style), and
4. **N**, how many to produce.

It returns **N new items** that match the format and the domain of the priors but **do not repeat or near-duplicate** any of them.

Status (2026-10-27): idea and spec only. No data, training or weights yet.

## Why

"Give me 20 more like these, but not these" is a common and very useful LLM task. General chat models handle it unevenly:

- **They drift back to the priors.** Outputs paraphrase items already on the list.
- **They collapse.** The 20 outputs cluster around 3–4 ideas.
- **They break the format.** The structure slips by item 12, or the model adds commentary.
- **They take the obvious route.** They give the most generic member of the category rather than ones that extend the pattern the priors set up.

These are learnable, measurable behaviours, which makes the task a good fit for a narrow fine-tune rather than prompt engineering alone.

## Motivating use cases

| Task | Priors | Format |
|---|---|---|
| ASR training-set ideation | current list of targeted sets (each aimed at a known ASR defect) | name, defect targeted, example utterances |
| Podcast prompt ideation (My Weird Prompts) | last ~100 episode prompts | one-paragraph prompt in house style |
| Podcast character ideation | existing characters and show beats | character card fields |
| Career trajectories | CV | role, why it fits, bridge steps |
| Open-ended ideation | none or a few examples | free list |

The last row is the degenerate case with no priors. The model should still work there, but the main target is the case where priors are present.

## Prior art (checked 2026-10-27)

No public model or dataset was found that trains this exact task (priors, format and N in; novel, format-matched items out). Related work:

- [Prompting Diverse Ideas: Increasing AI Idea Variance](https://www.themoonlight.io/en/review/prompting-diverse-ideas-increasing-ai-idea-variance) uses prompt strategies only. Its metrics (cosine similarity, uniqueness, exhaustion rate) are reusable here.
- [TinyTim](https://arxiv.org/abs/2508.11607) is a fine-tune aimed at *divergent* generation in general, not at structured generation conditioned on priors.
- [Divergent-Convergent Thinking for Creative Problem Generation](https://arxiv.org/html/2512.23601v1) is a brainstorm-then-select prompting pipeline.
- [LLMs as Innovators: latent-space exploration](https://arxiv.org/html/2507.13874v1) notes that raising temperature gives only modest originality gains, which argues for training rather than sampling tricks.

Re-check the Hugging Face Hub before training (`brainstorm`, `ideation`, `divergent`, `list expansion`).

## I/O contract

See [`docs/schema.md`](docs/schema.md). Summary:

```json
{
  "task": "Propose new targeted ASR fine-tuning sets",
  "priors": ["Hebrew place names in English speech", "Spoken URLs and email addresses"],
  "format": {"fields": ["name", "defect", "examples"], "examples_count": 3},
  "n": 20,
  "constraints": ["each set must target a distinct failure mode"]
}
```

The output is a JSON array of exactly `n` objects, each conforming to `format`, with no preamble.

## Approach ladder

1. **Baseline:** a frontier model with a strong prompt, scored with the eval below. If it already passes, there is no need to fine-tune.
2. **Synthetic SFT data:** build (task, priors, format, N) tuples across many domains. Generate candidates with a frontier model at high N, filter out near-duplicates of priors and of each other with embedding similarity, check the format, and keep the survivors as targets. A useful trick is **hold-out-as-target**: take a real list, hide K items, use the rest as priors, and treat the hidden items as gold-standard "novel but in-pattern" examples.
3. **SFT** of a small instruct base (roughly 3–8B, open weights) with LoRA.
4. **Preference tuning (DPO)** on pairs where the rejected output paraphrases priors or collapses, and the chosen output is diverse and in-pattern.

## Eval

| Metric | How |
|---|---|
| Format adherence | Output parses, has exactly N items and the required fields |
| Novelty vs priors | Max embedding cosine of each output item to any prior, below a threshold |
| Intra-set diversity | Mean pairwise distance and cluster count among the N outputs |
| In-domain fit | LLM judge: does the item belong to the same family as the priors? |
| Usefulness | LLM judge or human rating on a held-out set of real lists (ASR sets, MWP prompts) |

The tension to watch is novelty against fit. A model that rewards distance alone will produce off-topic items, so both metrics must be reported together.

## Layout

- `docs/schema.md`: input/output contract
- `data/` (planned): seed lists, synthetic tuples, splits
- `eval/` (planned): scoring scripts
