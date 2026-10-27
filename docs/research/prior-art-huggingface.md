# Prior art on the Hugging Face Hub: bounded brainstorming

Dated 2026-10-27. Researcher: Claude. Scope: Hub models, datasets and Spaces, plus a few web searches for blog and forum posts. Task searched for: given a task, priors (existing items), optional context, a format and N, output N new items that match the format and family of the priors, do not repeat or paraphrase them, and are diverse among themselves.

## Method

Queries ran against the public API (no auth), `https://huggingface.co/api/{models,datasets,spaces}?search=<term>&limit=50&sort=downloads&direction=-1`. A result count of 50 means the limit was hit, so more exist. I then read the top hits by title and opened the cards (`/<id>/resolve/main/README.md` for models, `/datasets/<id>/resolve/main/README.md` for datasets) for the shortlisted ones. "Confirmed" below means I read the card; "inferred" means title or search snippet only.

Result counts per query:

| Query | models | datasets | spaces |
|---|---|---|---|
| `brainstorm` | 50 | 27 | 47 |
| `brainstorming` | 7 | 9 | 15 |
| `ideation` | 50 | 30 | 45 |
| `idea generation` | 1 | 2 | 2 |
| `idea-generation` | 1 | 2 | 2 |
| `divergent` | 28 | 10 | 14 |
| `creativity` | 50 | 34 | 50 |
| `list expansion` | 0 | 0 | 0 |
| `list continuation` | 0 | 0 | 0 |
| `set expansion` | 0 | 0 | 0 |
| `novelty` | 29 | 50 | 10 |
| `diverse generation` | 0 | 0 | 1 |
| `more like this` | 0 | 0 | 1 |
| `exclusion` | 8 | 25 | 3 |
| `negative examples` | 0 | 0 | 0 |
| `career path` | 9 | 3 | 50 |
| `career recommendation` | 2 | 0 | 20 |
| `podcast ideas` | 0 | 0 | 0 |
| `research idea` | 14 | 15 | 5 |
| `idea` | 50 | 50 | 50 |
| `creative writing diversity` | 0 | 0 | 0 |
| `diversity` | 50 | 50 | 24 |
| `SciMON` | 2 | 0 | 0 |
| `idea evaluation` | 1 | 1 | 0 |

Extra queries (counts of models / datasets): `TinyTim` 9 / 0; `verbalized sampling` 1 / 5; `NoveltyBench` 0 / 27; `entity set expansion` 0 / 0; `Sparse list` 0 / 0; `item-list` 1 / 1; `name generation` 1 / 3; `dedup generation` 0 / 0; `creative-writing` 50 / 50. Web searches (WebSearch, standard mode) on: exclusion-list brainstorming fine-tuning; discuss.huggingface.co brainstorming diversity; HF blog on diverse outputs / mode collapse. No HF forum thread or HF blog post on this task was returned.

Zero-hit queries (`list expansion`, `list continuation`, `set expansion`, `more like this`, `negative examples`, `podcast ideas`, `diverse generation` for models and datasets) are themselves informative: the Hub has no vocabulary for this task. Most keyword hits are noise (Brainstorm20x GGUF models are DavidAU layer-duplication merges named "Brainstorm", not training for brainstorming; `IDEA-Research` and `IDEA-CCNL` match "idea"; "suicide ideation" classifiers match "ideation").

## Relevant hits

Closeness: none / partial / close. "Priors" = conditions on existing items; "novelty" = enforces novelty against them.

| Name | Link | Type | Size / base | What it does | Closeness | Notes |
|---|---|---|---|---|---|---|
| stindardlogic/brainstorming-ideation-sft-100k | https://huggingface.co/datasets/stindardlogic/brainstorming-ideation-sft-100k | dataset | 100k ShareGPT rows, synthetic, apache-2.0 | Prompt = situation, constraints, request ("generate 10 ideas"); response = numbered ideas with bold title and description across 22 domains. Metadata has `format_note` and `idea_count` (N). | partial | Confirmed. Closest in shape: has N and a format note. Priors are not a field; the situation may mention existing assets, but no exclusion list and no novelty check. 41 downloads, last modified 2026-07-21. Quality unknown; synthetic, generator not stated in the part I read. |
| Wanfq/Explore_Instruct_Brainstorming_{10k,16k} and Explore-LM-{,Ext-}7B-Brainstorming | https://huggingface.co/datasets/Wanfq/Explore_Instruct_Brainstorming_16k , https://huggingface.co/Wanfq/Explore-LM-Ext-7B-Brainstorming | dataset + model | LLaMA-7B fine-tune, cc-by-nc-4.0 | Instruction-coverage method (Explore-Instruct, arXiv 2310.09168): tree search over sub-tasks to widen domain coverage; models are tuned on brainstorming instructions. | none | Confirmed. The "brainstorming" is a task category (Vicuna/BELLE style), and diversity is of instructions, not of outputs against priors. Non-commercial licence. |
| chimbiwide/brainstorming-thinking | https://huggingface.co/datasets/chimbiwide/brainstorming-thinking | dataset | 1K-10K rows, apache-2.0 | Qwen3-14B reasoning traces and answers for Explore_Instruct_Brainstorming_10k. | none | Confirmed. RL-suited, no priors. |
| DevQuasar/brainstorm-v3.1_vicnua_1k (and v2.1, vicuna_1k, 10k) | https://huggingface.co/datasets/DevQuasar/brainstorm-v3.1_vicnua_1k | dataset | 1k, Llama 3.1 70B generated | Multi-turn human-LLM brainstorming chats plus a markdown summary, topic list for diversity. | none | Confirmed. Conversational, not list-in list-out. |
| TeichAI/Qwen3-4B-Instruct-grok-4-fast-brainstorming-distill and TeichAI/brainstorm-v3.1-grok-4-fast-200x | https://huggingface.co/TeichAI/Qwen3-4B-Instruct-grok-4-fast-brainstorming-distill | model + dataset | Qwen3-4B-Instruct, 200 rows | Small distill of Grok 4 Fast answers on the DevQuasar brainstorm prompts. | none | Confirmed (two-line card). Same size class as our target, no priors, no eval. |
| yimingzhang/novelty-bench | https://huggingface.co/datasets/yimingzhang/novelty-bench | dataset (benchmark) | 100 curated + 1,000 WildChat prompts | NoveltyBench: 10 samples per prompt, counts distinct equivalence classes and quality-weighted utility. Results for many models stored under `results/`. Also mirrored runs under `alon-albalak/*-noveltybench-*` (27 datasets). | partial (eval only) | Confirmed. Measures set-level diversity across samples of one prompt. No priors or exclusion. Code: https://github.com/novelty-bench/novelty-bench . |
| tax-free/scientific-ideation-diversity | https://huggingface.co/datasets/tax-free/scientific-ideation-diversity | dataset (raw outputs + judgments) | 1M-10M rows, cc-by-4.0 | Ideas from Claude Sonnet 4.6, GPT-5.4, Gemini 3.1 Pro under reasoning-effort and diversification prompts (Verbalized Sampling, String Seed of Thought), with embeddings and about 1.4M pairwise LLM-judge diversity judgments. | partial (eval) | Confirmed. Rich source of idea sets with diversity labels; no priors. Repo: https://github.com/bioinfo-tsukuba/scientific-ideation-diversity . |
| CHATS-Lab/Verbalized-Sampling-* (Synthetic-Data-Generation, Open-Ended-QA, others) | https://huggingface.co/datasets/CHATS-Lab/Verbalized-Sampling-Synthetic-Data-Generation | dataset | 1k-4k rows per model | Responses elicited by Verbalized Sampling (ask for several responses with probabilities) vs direct and CoT, across models. | partial (inference trick, not training) | Partly confirmed (split names and schema; I did not read the method text). Useful baseline: prompt-only way to get diverse sets. |
| Pageshift-Entertainment/pagestorm-research-diversity-14b | https://huggingface.co/Pageshift-Entertainment/pagestorm-research-diversity-14b | model | 14B, finetune of pagestorm-research-preview-14b-full-book | GRPO with quality reward plus a prompt-aware semantic-diversity reward that ignores elements the prompt required; similarity cutoff caps the push. Blog: https://pageshift.ai/research/pagestorm-diversity | partial | Confirmed. Diversity across samples for story premises. Not conditioned on priors. The reward design (diversity computed on model-chosen content only) transfers to us. |
| scasella91/qwen3-30b-a3b-answer-diversity-lora | https://huggingface.co/scasella91/qwen3-30b-a3b-answer-diversity-lora | model (LoRA) | Qwen3-30B-A3B-Instruct-2507 | 50 GRPO steps on "random integer 1-100"; total variation from uniform 0.953 to 0.413, transfers to other random-pick tasks. Card carries honest corrections. | none | Confirmed. Evidence that a tiny RL run shifts output distributions; closed-world picks only. |
| bdeepakreddy/creativity-slm | https://huggingface.co/bdeepakreddy/creativity-slm | model | Qwen2.5-1.5B-Instruct, QLoRA, 764 examples | Distilled "creative cognition" (cross-domain analogy, constraint violation) in 5 structured sub-tasks; reports 96.1% structural validity. | partial | Confirmed. Small, structured outputs, validity metric, but no priors and no novelty measure beyond validity. |
| creativityschapiro/qwen2.5-7b-instruct-cn-ideation-* (many) and creativityschapiro/openreview_raw | https://huggingface.co/creativityschapiro/qwen2.5-7b-instruct-cn-ideation-kr0.05-a2.0-creative | model family | Qwen2.5-7B / Llama-3.1-8B weight-scaled | CreativityNeuro: scale weights found important for creative prompts; no training data. | none | Confirmed (one card). Interpretability trick. |
| wop/Creativity-lfm2-5-350M | https://huggingface.co/wop/Creativity-lfm2-5-350M | model | LFM2.5-350M, 60 steps | CoT fine-tune on creativity datasets. | none | Confirmed. Sub-1B example. |
| almuallim/gpt2-idea-generation | https://huggingface.co/almuallim/gpt2-idea-generation | model | GPT-2, from a Kaggle GPT-3 business-ideas set | Generates business ideas. | none | Confirmed (one-line card). Free generation, no priors. |
| InternScience/SGI-IdeaGeneration (+Lite) | https://huggingface.co/datasets/InternScience/SGI-IdeaGeneration | dataset | under 1K, mit | Scientific idea-generation tasks from SGI-Bench, auto-gated. | none | Metadata read via API only; gated, so card unread. |
| yolo1213811/research-ideation-arena-dataset | https://huggingface.co/datasets/yolo1213811/research-ideation-arena-dataset | dataset | 1M-10M, cc-by-nc-4.0 | Ideation Arena: pairwise expert judgments of LLM research ideas, queries included. | none | Confirmed. Eval of idea quality. |
| allenai/novelty-judge-bench | https://huggingface.co/datasets/allenai/novelty-judge-bench | dataset | under 1K | Expert and machine labels for novelty of AI-generated research ideas, for validating LLM judges. | partial (judge calibration) | Confirmed from front matter. Novelty vs literature, not vs a list. |
| Salesforce/ttcw_creativity_eval ; joeyhou/creativityprism_v1 ; chengq9/CreativityBench ; Kombai/design-creativity-bench | https://huggingface.co/datasets/joeyhou/creativityprism_v1 | datasets (benchmarks) | small | Creative-writing and divergent-thinking (AUT, TTCT) evals; tool-repurposing. | none | Confirmed first three, Kombai inferred. Human-style creativity tests, not list tasks. |
| SolimanBa/Tech-Career-Paths-Dataset ; eshern/careerpath-data ; khandy123/career_path_datasets | https://huggingface.co/datasets/SolimanBa/Tech-Career-Paths-Dataset | datasets | 1K-10K CSV | Tabular career data. | none | SolimanBa card is empty (licence only); the other two are inferred from titles. No LLM recommendation-with-bridge-steps data found. Career models (ElenaSenger/career-path-representation-mpnet-*, tgkamal/student_career_path-llama) are embeddings or classifiers, inferred. |
| rinad12/Syn-Item-Lists | https://huggingface.co/datasets/rinad12/Syn-Item-Lists | dataset | 1K-10K | Synthetic travel packing lists for structured-output fine-tuning. | none | Confirmed. Lists, but conditioned on scenario, not on priors. |
| npc-worldwide/TinyTimV1 | https://huggingface.co/npc-worldwide/TinyTimV1 | model | TinyLlama-1.1B-Chat on Finnegans Wake | Joyce-style text. | none | Confirmed it is a style fine-tune. Whether it is the model of the TinyTim paper (arXiv 2508.11607, cited in the README) is inferred, not checked. |
| Spaces (brainstorm 47, ideation 45, career_path 50, career_recommendation 20) | e.g. https://huggingface.co/spaces/ping98k/LLM-Brainstorming , https://huggingface.co/spaces/yasserrmd/CareerPath | spaces | n/a | Chat or form front-ends to hosted LLMs. | none | Inferred from names only, none opened. A few hundred, all demos with 0-2 likes. No Space does exclusion-aware list expansion. |

Papers surfaced by web search, not Hub assets (inferred from snippets, not opened): Possibility Exploration Fine-Tuning, https://arxiv.org/pdf/2412.03343v1 (task-agnostic fine-tune so one prompt yields several distinct responses); Examining and Addressing Barriers to Diversity in LLM-Generated Ideas, https://arxiv.org/pdf/2602.20408 ; Group-Aware RL for Output Diversity (GAPO), https://arxiv.org/html/2511.12596v1 ; MoDA mode-conditioned RL, https://huggingface.co/papers/2609.14896 ; Prompting Diverse Ideas, https://arxiv.org/pdf/2502.12700v1.

## Reusable assets

Training (format and N only, priors must be synthesised): `stindardlogic/brainstorming-ideation-sft-100k` has request/format/count structure across 22 domains and can seed the `OPN` archetype after relabelling. `Explore_Instruct_Brainstorming_*` and `chimbiwide/brainstorming-thinking` give prompt diversity only; licences (cc-by-nc on Explore) matter.

Hold-out lists and priors: `tax-free/scientific-ideation-diversity` ideas files (many ideas per keyword, with embeddings) can be split into "priors" and "held-out" sets to build `EXT` examples with a known diversity structure. `Syn-Item-Lists` and the Verbalized-Sampling sets give ready-made multi-item outputs that could be re-framed with a subset as priors.

Eval: NoveltyBench (`yimingzhang/novelty-bench`, prompts plus stored model generations and partition labels) for set-level distinctness; the scientific-ideation-diversity judgments (about 1.4M pairwise) to calibrate an LLM or embedding diversity judge; `allenai/novelty-judge-bench` to sanity-check a novelty judge. None of these test novelty against a supplied prior list, so that metric (max similarity to any prior, near-duplicate rate, format-validity rate, within-set pairwise distance) must be built here.

## Verdict

No one on the Hub has published this exact task. Across the queries above I found no model or dataset where the input contains priors plus a format plus N and the target is N items that are format-matched, non-duplicating against the priors and diverse among themselves, and no Space that does it. The nearest neighbours each cover one piece: `stindardlogic/brainstorming-ideation-sft-100k` covers format and N without priors; NoveltyBench and the scientific-ideation-diversity data cover within-set diversity without priors; Pagestorm Diversity and the answer-diversity LoRA cover training for diversity by RL without conditioning on an exclusion list. The real gap is the exclusion-conditioned, structured, small-model case. Caveats: Hub search is keyword-only and matches names and tags, so a model with a different vocabulary (for example "dedup", "negative-prompted generation") could be missed; private and gated repos are invisible; 12 of the 22 hits were assessed from cards alone with no model run.
