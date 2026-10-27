# Use-case catalogue

Written 2026-10-27. Tags follow [`taxonomy.md`](taxonomy.md) (A·B·C·D·E·F·G·H). The first four rows are the motivating cases from the README. The rest widen the training distribution; none of them needs its own model, they are points in the same space.

`Real data?` says whether a real prior list exists to build hold-out tuples from (best source of gold targets). `own` = Daniel's own material (keep in `data/private/` if unreleased), `pub` = a public list that can be scraped.

## Motivating cases

| # | Use case | Input in practice | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 1 | My Weird Prompts episode prompts | last ~100 episode prompts (from the MWP archive), show description | `{title, prompt}` one paragraph, house style | `EXT·P4·C1·L·O3·K1·Np·Spriv` | own |
| 2 | Targeted ASR fine-tuning sets | current list of sets, each with its defect | `{name, defect, examples[3]}` | `GAP·P1·C1·S·O4·K1·Np·Spub` | own |
| 3 | Career trajectories from a CV | **CV as PDF** + optional "paths I've ruled out" | `{role, why_it_fits, bridge_steps[]}` | `PRJ·P0·C3·M·O4·K1·Nx·Spriv` | own (1 CV), synthetic CVs for volume |
| 4 | New dataset ideas | list of datasets already published on HF + interests | `{name, purpose, collection_method}` | `EXT·P2·C1·M·O2·K2·Np+Nw·Spub` | own (HF profile) |
| 5 | Podcast character ideas | existing characters and show beats | character card fields | `EXT·P1·C2·M·O3·K0·Np·Spriv` | own |

## Content and media

| # | Use case | Input | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 6 | Blog post topics | sitemap / RSS of existing posts | `{title, angle}` | `EXT·P2·C0·M·O2·K1·Np·Spub` | pub (any blog RSS) |
| 7 | YouTube video ideas | channel's video titles | `{title, hook}` | `EXT·P2·C1·M·O2·K1·Np·Spub` | pub |
| 8 | Newsletter section ideas | past issue headings | `{section, description}` | `EXT·P1·C1·S·O2·K1·Np·Spub` | pub |
| 9 | Episode titles for a given script | **script/transcript** + rejected titles | string | `VAR·P1·C2·M·O1·K0·Nx·Spriv` | own |
| 10 | Interview questions for a guest | guest bio (**PDF/web page**) + questions already asked by other hosts | `{question, why}` | `PRJ·P1·C3·M·O2·K1·Nx·Spub` | pub (transcripts) |
| 11 | Social post variants | one seed post | string | `VAR·P1·C0·S·O1·K0·Nx·Spub` | synthetic |

## Data, ML and engineering

| # | Use case | Input | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 12 | Eval test cases for a model | existing eval items + capability description | `{input, expected_behaviour, category}` | `GAP·P2·C2·M·O3·K1·Np·Spub` | pub (open eval sets) |
| 13 | Edge-case unit tests | **source file** + existing tests | `{name, scenario, expected}` | `GAP·P3·C2·L·O3·K1·Np·Spub` | pub (GitHub repos) |
| 14 | Feature ideas for a project | README + issue titles | `{feature, rationale}` | `PRJ·P2·C2·M·O2·K1·Np·Spub` | pub |
| 15 | Fine-tune ideas (like this repo) | list of existing fine-tunes on a profile | `{name, task, data_source}` | `EXT·P2·C1·S·O2·K2·Np+Nw·Spub` | own |
| 16 | Synthetic-data prompt seeds | existing seed prompts for a generator | string or `{prompt, persona}` | `EXT·P1·C1·M·O2·K1·Np·Spub` | pub |
| 17 | Red-team / jailbreak categories | covered attack categories | `{category, example}` | `GAP·P1·C1·S·O2·K1·Np·Spub` | pub (taxonomies) |
| 18 | Agent skill / prompt ideas | names + descriptions of existing skills (the ~3,400-skill catalogue) | `{name, description}` | `EXT·P4·C0·XL·O2·K1·Np·Spriv` | own |

## Career, people and organisations

| # | Use case | Input | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 19 | Side-project ideas from a CV | **CV PDF** + current projects | `{project, skills_used, first_step}` | `PRJ·P3·C3·M·O3·K1·Np·Spriv` | own |
| 20 | Grant / funding angles | org profile (**PDF**) + grants already applied for | `{funder_type, angle}` | `PRJ·P1·C3·M·O2·K2·Nx·Spriv` | synthetic |
| 21 | Product ideas for a company | company profile + current product list | `{product, customer, why_us}` | `PRJ·P2·C2·M·O3·K1·Np·Spub` | pub (company sites) |
| 22 | Talk / conference proposals | speaker bio + past talks | `{title, abstract}` | `EXT·P1·C2·M·O3·K1·Np·Spub` | pub (conference archives) |

## Naming and short-form

| # | Use case | Input | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 23 | Product / repo names | brief + rejected names | string | `VAR·P1·C1·S·O1·K2·Nx·Spub` (availability checked by wrapper) | synthetic |
| 24 | Taglines | product description + existing taglines | string | `VAR·P1·C1·S·O1·K0·Np·Spub` | pub |
| 25 | Domain name ideas | brief + taken names | string | `VAR·P1·C1·S·O1·K2·Nx·Spub` | synthetic |

## Everyday and personal

| # | Use case | Input | Output item | Tag | Real data? |
|---|---|---|---|---|---|
| 26 | Meal ideas | recent meals + **pantry list (CSV)** + diet rules | `{dish, uses}` | `EXT·P2·C4·S·O2·K1·Np·Spriv` | own |
| 27 | Gift ideas | recipient notes + past gifts | `{gift, why}` | `PRJ·P1·C1·S·O2·K1·Nx·Spriv` | synthetic |
| 28 | Trip / day-out ideas | places already visited + constraints | `{place, why, logistics}` | `EXT·P1·C1·S·O3·K2·Np·Spriv` | own |
| 29 | Home automation ideas | **HA entity list export** + existing automations | `{automation, trigger, action}` | `GAP·P2·C4·L·O3·K1·Np·Spriv` | own |
| 30 | Open-ended list | task only | free string | `OPN·P0·C0·S·O1·K1·—·Spub` | synthetic |

## Coverage check

| Axis value | Count | Note |
|---|---|---|
| `EXT` | 13 | dominant; easiest to source from real lists (hold-out) |
| `PRJ` | 7 | needs synthetic profiles for volume; real CVs are private |
| `GAP` | 5 | needs the "space" made explicit in `context` |
| `VAR` | 5 | short outputs, high N; cheap to generate |
| `OPN` | 1 | keep a small share (~5%) so the degenerate case still works |
| `C3` binary docs | 5 | all converted to text by the wrapper; train on the *converted* text, including its extraction noise |
| `C4` tabular | 2 | train on the converted JSON/markdown form |
| `K2` | 6 | model output is unverified; the wrapper checks against the world |
| `XL` | 1 (+ #1 when the full archive is used) | needs compression before the model |

Target mix for the first SFT set (to revisit after the baseline): EXT 40%, PRJ 25%, GAP 15%, VAR 15%, OPN 5%; size bins S 30%, M 40%, L 30%.
