# Task taxonomy

Written 2026-10-27. Status: proposal, not yet used to tag data.

"Bounded brainstorming" covers thousands of surface tasks (episode ideas, dataset ideas, career paths, product names). For training and evaluation they differ only along a handful of **technical axes**: what goes in, in what form, how big, what the outputs must be novel against, and what they must fit. This document defines those axes and collapses the space into five **archetypes**. Every use case in [`use-cases.md`](use-cases.md) is tagged with them.

The point of the taxonomy is practical:

- **Data balancing:** the training mix should cover every archetype and every context size bin, not 80% podcast prompts.
- **Scope:** some cells (live web knowledge, images, 100k-token corpora) are out of reach for a small text model. The taxonomy makes those explicit so the wrapper handles them, not the model.
- **Eval:** novelty and fit are measured differently per archetype (see the last section).

## Axes

### A. Archetype (relation between priors, context and outputs)

The most important axis. It decides what "novel" and "fits" mean.

| Code | Archetype | Priors are… | Context is… | Outputs are… | Example |
|---|---|---|---|---|---|
| `EXT` | **List extension** | the same type as the outputs | optional background | more members of the same family, not repeating priors | 100 MWP episode prompts → 20 new prompts |
| `PRJ` | **Profile projection** | optional; things already considered or rejected | the main input: a profile of a subject (person, company, codebase) | a *different* type from the context, fitted to the subject | CV → career trajectories |
| `GAP` | **Coverage gap-fill** | partial coverage of a known space | optional description of the space (taxonomy, defect list) | items that cover regions the priors miss | ASR sets per defect → sets for untargeted defects |
| `VAR` | **Seed variation** | one seed item, plus any rejected variants | optional brief | short variants of the seed (names, titles, taglines) | product name + 10 rejected names → 30 more |
| `OPN` | **Open / cold start** | none | optional | a free list in the requested format | "20 weekend project ideas" |

`EXT` and `GAP` look alike. The difference is that `GAP` has an implicit or explicit **space** to cover, so outputs can be judged by *what they cover*, not only by distance from priors. `PRJ` is the one that differs most: the context is not a list, the outputs are grounded in a subject, and novelty is measured against an exclusion list rather than a family.

### B. Prior source (how the priors reach the model)

| Code | Source | Preprocessing needed |
|---|---|---|
| `P0` | none | none |
| `P1` | inline list pasted by the user | none |
| `P2` | structured export (CSV, JSON, DB rows, HF dataset list, RSS feed) | parse to a JSON list; pick fields |
| `P3` | embedded in a document (the jobs inside a CV, the features inside a README) | extraction (rule or LLM) into a list |
| `P4` | a large corpus (all 600+ episodes, a whole backlog) | retrieval or compression to fit the budget (see [`context-requirements.md`](context-requirements.md)) |

### C. Context modality (what the non-list background is)

| Code | Modality | Typical file | Handled by |
|---|---|---|---|
| `C0` | none | | |
| `C1` | short text (a brief, a show description) | | the model directly |
| `C2` | long text document | `.md`, `.txt`, `.html` | the model, after cleaning |
| `C3` | binary document | `.pdf`, `.docx`, `.pptx` | **wrapper**: extract to text/markdown, then `C2` |
| `C4` | tabular | `.csv`, `.xlsx` | **wrapper**: convert to JSON rows or a markdown table |
| `C5` | image / visual | moodboard, screenshot, diagram | **out of scope for v1**; a VLM caption can turn it into `C1` |
| `C6` | audio / video | episode audio, a talk | **out of scope for v1**; transcribe to `C2` |
| `C7` | live / external | "what's on the HF Hub now", job listings | **wrapper** (search, retrieval); the model never fetches |

Rule for v1: **the model sees text only.** Every binary input is converted upstream, and the conversion is part of the pipeline spec, not the model.

### D. Size bins (input tokens, priors plus context)

| Code | Budget | Example |
|---|---|---|
| `S` | ≤ 2k | 10 priors, short brief |
| `M` | ≤ 8k | a CV, or 50 short priors |
| `L` | ≤ 32k | 100 MWP prompts at ~120 tokens each (~12k) plus show notes |
| `XL` | > 32k | the full episode archive, a whole codebase. Needs compression (`P4`) |

### E. Output item shape

| Code | Shape | Typical tokens per item |
|---|---|---|
| `O1` | single string | 5–30 |
| `O2` | flat object, short fields | 20–80 |
| `O3` | flat object with a paragraph field | 80–250 |
| `O4` | nested object (lists of examples, sub-steps) | 150–500 |

Output budget = N × tokens per item. N = 50 at `O4` is ~25k output tokens, which is past what a small model does reliably in one pass; the wrapper should batch (several calls, each told about the earlier outputs as priors).

### F. Knowledge requirement

| Code | Needs | Example |
|---|---|---|
| `K0` | nothing beyond the input (closed world) | name variants, remix of priors |
| `K1` | general domain knowledge in the weights | ASR failure modes, career ladders in tech |
| `K2` | current or niche facts | "datasets that don't exist on HF yet", current job market, domain availability |

`K2` cannot be satisfied by a small model alone. The model generates; a wrapper verifies (search the Hub, check a registrar) and drops failures.

### G. Novelty reference (what outputs must not duplicate)

Always: **intra-set** (outputs vs each other). Plus one or more of:

| Code | Reference |
|---|---|
| `Np` | the priors |
| `Nx` | an explicit exclusion list (rejected ideas, things already tried) |
| `Nw` | the outside world (existing products, datasets, papers). Implies `K2` |

### H. Sensitivity

| Code | Meaning | Consequence |
|---|---|---|
| `Spub` | public inputs | any inference route |
| `Spriv` | private inputs (CV, unreleased episode list, client briefs) | local inference preferred; data stays in gitignored `data/private/` |

`Spriv` is a real argument for a small local model: the CV and unreleased-backlog cases are exactly the ones you would rather not send to an API.

## Tag string

Each use case gets a compact tag, in axis order A·B·C·D·E·F·G·H, for example:

```
EXT·P4·C1·L·O3·K1·Np·Spriv     MWP episode prompts from the archive
PRJ·P0·C3·M·O3·K1·Nx·Spriv     career trajectories from a CV PDF
```

Proposed as a `meta.tags` object in the training records (see [`context-requirements.md`](context-requirements.md#proposed-schema-v02)).

## How eval differs by archetype

| Archetype | Novelty measured against | Fit measured as |
|---|---|---|
| `EXT` | priors (embedding max-cosine) | judge: same family as priors |
| `PRJ` | exclusions, plus anything already in the context (current job is not a "new path") | judge: grounded in the subject's profile, with the reason traceable to the context |
| `GAP` | priors | judge or rule: covers a region of the space the priors don't |
| `VAR` | seed and rejected variants, with a looser threshold (variants are meant to be close) | judge: keeps the seed's intent |
| `OPN` | intra-set only | judge: on-task |
