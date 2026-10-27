# I/O schema

## Input

| Field | Type | Required | Meaning |
|---|---|---|---|
| `task` | string | yes | What is being brainstormed, in one sentence |
| `priors` | string[] or object[] | no (may be empty) | Existing items. Outputs must not repeat or paraphrase them. They also define the "family" the outputs belong to |
| `context` | string | no | Free-text background (a CV, show description, defect notes) that is not itself a list of items |
| `format` | object | yes | Output item structure: `fields` (names), optional per-field guidance, length limits |
| `n` | int | yes | Exact number of items to return |
| `constraints` | string[] | no | Extra rules ("each targets a distinct failure mode", "no US-specific ideas") |

## Output

A JSON array of exactly `n` objects, each with exactly the `format.fields` keys. There is no prose before or after it.

## Training-tuple sources

- **hold-out:** a real list with K items hidden. The priors are the rest and the gold targets are the hidden items.
- **synthetic:** a frontier model generates candidates, which are then filtered for novelty against the priors, diversity within the set, and format.
- **preference pairs:** for DPO. The chosen output passes all filters. The rejected output paraphrases priors, collapses into a few ideas, or breaks the format.

## Example

```json
{
  "task": "Pitch new episode prompts for a podcast where two AI hosts discuss listener questions",
  "priors": ["Why do LLMs struggle with counting letters?", "Could a city be run by an agent swarm?"],
  "format": {"fields": ["title", "prompt"], "prompt_max_words": 80},
  "n": 3,
  "constraints": ["no topics already covered by priors"]
}
```
