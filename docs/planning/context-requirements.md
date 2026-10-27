# Context requirements and pipeline

Written 2026-10-27. Status: proposal for the POC.

How a request gets from "here is my CV as a PDF, give me 15 career paths" to a JSON array, which parts are the model and which are the wrapper, and what each archetype in [`taxonomy.md`](taxonomy.md) needs.

## Split of responsibilities

```
 user inputs                 wrapper (deterministic + tools)              model (fine-tune)        wrapper
 ───────────                 ──────────────────────────────              ─────────────────        ───────
 task text      ─┐
 priors (list,   │  1. ingest: PDF/DOCX → markdown, CSV → JSON rows
   file, corpus) ├─ 2. extract priors from documents (P3)          ─►  text-only request  ─►  JSON array ─► 5. parse + validate
 context files   │  3. compress priors if over budget (P4/XL)         (schema.md)                         6. novelty filter vs FULL priors
 format, N       ─┘  4. batch N if N × item tokens > output budget                                        7. world check (K2)
                                                                                                          8. top up shortfall (loop to 4)
```

**The model sees text only and never fetches anything.** Everything the taxonomy marks as "wrapper" stays outside the weights, so the fine-tune can stay small and the hard, changing parts (file formats, live checks) can be swapped without retraining.

## Per-stage requirements

### 1. Ingest (context modality `C3`, `C4`)

| Input | Tool (candidate) | Output to model | Note |
|---|---|---|---|
| PDF (CV, bio, org profile) | `pymupdf4llm` or `docling` | markdown | Scanned PDFs need OCR; out of scope for POC |
| DOCX / PPTX | `pandoc` / `docling` | markdown | |
| CSV / XLSX | `pandas` | JSON array of rows, or a markdown table under ~200 rows | Drop columns irrelevant to the task |
| HTML / web page | `trafilatura` | markdown | |
| Image, audio | not in POC | | VLM caption / transcription would turn them into `C1`/`C2` |

Training implication: the `context` text in training data must look like **converted** documents (markdown headings, extraction artefacts, broken bullet lists), not clean prose. Synthetic CVs should be generated, rendered to PDF and extracted back, or at least written in that style.

### 2. Prior extraction (`P3`)

When the priors live inside a document (jobs in a CV, features in a README), the wrapper extracts them into a list first. For `PRJ` the extracted items usually go to `exclude` (see below), not `priors`, because they are not the same type as the outputs.

### 3. Prior compression (`P4`, size bin `XL`)

When priors exceed the input budget:

1. Embed all priors.
2. Cluster; keep a representative per cluster plus the most recent K items (recency matters for "house style").
3. Pass the selection as `priors` and set `priors_omitted` to the count left out.
4. Keep the **full** set for the post-hoc novelty filter (stage 6). The model only needs enough priors to learn the family; the filter enforces novelty against all of them.

Budget for the POC: input ≤ 16k tokens, with `L` (≤ 32k) as a stretch goal depending on the base model chosen in [`../research/architecture-options.md`](../research/architecture-options.md).

### 4. Output batching

| Item shape | Tokens/item | Max N per call (≈ 4k output budget) |
|---|---|---|
| `O1` | ~20 | 100+ |
| `O2` | ~60 | ~60 |
| `O3` | ~180 | ~20 |
| `O4` | ~350 | ~10 |

For larger N the wrapper calls repeatedly, appending earlier outputs to `priors`. This also gives better diversity than one long list, which tends to collapse late.

### 5–8. Post-processing

- **Parse/validate:** `scripts/validate.py` logic. Constrained JSON decoding at inference can make this near-certain (see architecture research).
- **Novelty filter:** drop outputs whose max cosine to any prior or exclusion exceeds a threshold (start at 0.85, tune per archetype; `VAR` needs a looser one).
- **World check (`K2`):** optional hooks, e.g. HF Hub search for "dataset doesn't exist yet", registrar lookup for domain names.
- **Top-up:** if fewer than N survive, re-call with the survivors and rejects added to `exclude`.

## Requirements by archetype

| Archetype | Required inputs | Typical size | Wrapper stages used | Model must learn |
|---|---|---|---|---|
| `EXT` | task, priors (≥ 5 to define a family), format, N | M–L | 2–3 if corpus, 5–8 | infer the family and style from priors; avoid paraphrase |
| `PRJ` | task, context (profile), format, N | M | 1–2, 5–8 | ground every item in the context; cite why; skip what the subject already did |
| `GAP` | task, priors, context describing the space, format, N | S–M | 5–8 | infer what's covered; target what isn't |
| `VAR` | task, one seed, format, N | S | 5, 7 | stay on-intent while varying form; very high N |
| `OPN` | task, format, N | S | 5 | diversity without anchors |

## Proposed schema v0.2

Additive changes to [`../schema.md`](../schema.md). Not yet implemented in `scripts/validate.py`.

| Field | Type | Why |
|---|---|---|
| `context` | string **or** array of `{kind, title, text}` | Several documents (CV + job ad), each labelled. `kind` ∈ `brief`, `profile`, `document`, `table`, `space` |
| `exclude` | string[] or object[] | Items to avoid that do **not** define the family (rejected ideas, current job, things already tried). Separates "avoid" from "imitate" |
| `priors_omitted` | int | Tells the model the priors are a sample of a larger set |
| `format.fields` with per-field guidance | object | `{"name": "short noun phrase", "why": "≤ 30 words, cite the CV"}` |
| `meta` | object, **training records only** | `{archetype, tags, domain, generator, filter_scores}` for balancing and analysis; stripped before the prompt |

Example (`PRJ`, CV PDF already extracted by the wrapper):

```json
{
  "task": "Suggest career trajectories that build on this person's background",
  "priors": [],
  "exclude": ["Technical writer", "Developer relations engineer"],
  "context": [
    {"kind": "profile", "title": "CV (extracted from cv.pdf)", "text": "## Experience\n- Tech communications lead, 2019–2024 ..."}
  ],
  "format": {"fields": {"role": "job title", "why_it_fits": "≤ 40 words, cite the CV", "bridge_steps": "2-4 concrete steps"}},
  "n": 10,
  "constraints": ["remote-friendly", "no roles requiring a new degree"]
}
```
