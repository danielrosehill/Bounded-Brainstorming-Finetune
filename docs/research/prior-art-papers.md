# Prior art: papers relevant to the bounded-brainstorming fine-tune

Dated 2026-10-27. Status: literature scan, not a systematic review.

Verification convention. Every arXiv ID below was resolved against the arXiv API or the abs page on 2026-10-27 and the title matched. Findings marked `[A]` were taken from the abstract read during this scan. Findings marked `[M]` are from the researcher's recollection of the paper; title and ID are verified but the claim was not re-read, so check before citing. Items marked `[unverified]` were seen only in a search result and not opened. The arXiv API rate-limited (HTTP 429) late in the scan, so the last batch was checked through abs pages instead.

No paper was found that trains the exact task (priors + format + N in, N novel format-matched items out). The closest are the multi-answer RL papers (Q3) and DivPO / diversity-aware post-training (Q1), which train for diversity but not for exclusion of a given prior list.

## Q1. Mode collapse after RLHF / instruction tuning, and fixes

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| Understanding the Effects of RLHF on LLM Generalisation and Diversity (Kirk et al.) | 2023 | https://arxiv.org/abs/2310.06452 | RLHF improves OOD generalisation but reduces per-input output diversity versus SFT [A, partial]. | Diversity loss is real and stage-dependent; SFT hurts less than preference tuning, so DPO must be diversity-aware. |
| Does Writing with Language Models Reduce Content Diversity? (Padmakumar & He) | 2023 | https://arxiv.org/abs/2309.05196 | Co-writing with an instruction-tuned model reduces collective content diversity [M]. | Homogenisation is a user-level harm, supports the project's motivation. |
| Diverse Preference Optimization, DivPO (Lanchantin et al.) | 2025 | https://arxiv.org/abs/2501.18101 | Chosen = rarest response above a quality bar in a sampled pool, rejected = most common below it; 45.6% more diverse persona attributes, 74.6% more diverse stories, similar win rate [A]. | Direct template for the planned DPO stage. Pair construction by pool and embedding diversity is cheap. |
| Modifying LLM Post-Training for Diverse Creative Writing (Chung et al.) | 2025 | https://arxiv.org/abs/2503.17126 | Adding "deviation" (difference from other samples for the same prompt) to DPO/ORPO objectives raises diversity with little quality loss [A]. | Alternative weighting to DivPO; small models (8B) were enough. |
| Jointly Reinforcing Diversity and Quality, DARLING (Li et al.) | 2025 | https://arxiv.org/abs/2509.02534 | Online RL with a learned semantic-diversity partition function plus a quality reward beats quality-only RL on novelty and quality [A]. | Upper-bound option if DPO is not enough; needs an RL setup, out of scope for v1. |
| Preserving Diversity in SFT of LLMs (GEM) | 2024 | https://arxiv.org/abs/2408.16673 | Cross-entropy SFT reduces diversity; a game-theoretic reverse-KL-style objective keeps it [A]. | Diversity loss starts at SFT. Consider GEM or keep SFT short; log diversity after SFT, before DPO. |
| Verbalized Sampling (Zhang et al.) | 2025 | https://arxiv.org/abs/2510.01171 | Cause is typicality bias in preference data; asking for a set of responses with probabilities restores 1.6-2.1x diversity in creative writing; larger models benefit more [A]. | Strong zero-training baseline to beat. Also a cheap way to generate the teacher data. |
| Artificial Hivemind / Infinity-Chat (Jiang et al.) | 2025 | https://arxiv.org/abs/2510.22954 | Different LLMs converge on similar open-ended answers; inter-model homogeneity, not only intra-model [A, partial]. | A single teacher model's outputs are correlated; use two or more teachers for the SFT data. |
| Base Models Beat Aligned Models at Randomness and Creativity (West & Potts) | 2025 | https://arxiv.org/abs/2505.00047 | Base models beat aligned ones on random generation and creative tasks [A]. | Consider a base model, not instruct, as the LoRA target. |
| NoveltyBench (Zhang et al.) | 2025 | https://arxiv.org/abs/2504.05228 | 20 frontier models are far less diverse than humans; larger models within a family are often less diverse than smaller ones; in-context regeneration helps [A]. | Small student models are not handicapped on diversity; the benchmark is reusable for eval. |
| Evaluating the Diversity and Quality of LLM Generated Content (Shypula et al.) | 2025 | https://arxiv.org/abs/2504.12522 | Preference-tuned models lose diversity but "effective semantic diversity" (diversity among outputs above a quality threshold) can be higher, since they produce more usable output [A]. | Report diversity conditional on quality and format validity, not raw diversity. |

## Q2. LLM ideation / creativity, and fine-tuning for creativity

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| Can LLMs Generate Novel Research Ideas? (Si, Yang, Hashimoto) | 2024 | https://arxiv.org/abs/2409.04109 | Blind review of 100+ researchers: LLM ideas judged more novel (p<0.05), slightly weaker on feasibility; LLM agent lacks diversity in generation and self-evaluation fails [A]. | Novelty and diversity are separate axes; judge-based self-filtering is unreliable, so filter with embeddings plus a separate judge. |
| The Ideation-Execution Gap (Si et al.) | 2025 | https://arxiv.org/abs/2506.20803 | After 43 experts executed ideas, LLM ideas scored worse on outcomes than human ones; the novelty advantage did not survive execution [A, partial]. | Judged novelty is a weak proxy for usefulness; keep a usefulness check on real lists. |
| TinyTim: A Family of Language Models for Divergent Generation | 2025 | https://arxiv.org/abs/2508.11607 | Fine-tuning on Finnegans Wake yields a model that is a source of divergent output inside a larger system [A]. | Shows narrow fine-tuning can shift generative style, but it is style-only and unconditioned; no priors or format. Little to reuse beyond the "creative component inside a pipeline" framing. |
| Prompting Diverse Ideas: Increasing AI Idea Variance (Meincke et al.) | 2024 | https://arxiv.org/abs/2402.01727 | GPT-4 idea pools less varied than human groups; chain-of-thought prompting brought them near human-group variance; metrics: cosine similarity, unique idea count, exhaustion speed [A]. | Prompt-only baseline to beat; metrics reusable. Authors not confirmed in this scan. |
| Base Models Beat Aligned Models at Randomness and Creativity | 2025 | https://arxiv.org/abs/2505.00047 | See Q1. | See Q1. |

Not found in this scan: AUT / divergent-thinking benchmark papers verified by link. Searches were not run to completion on that sub-topic; treat AUT as untested ground.

## Q3. N items in one pass vs N samples; list/set generation; exclusion conditioning

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| Asking a Language Model for Diverse Responses (Troshin et al.) | 2025 | https://arxiv.org/abs/2509.17570 | Under matched budget, enumeration (n answers in one pass) and iterative sampling (condition each on earlier ones) beat parallel sampling on diversity at comparable quality; workshop paper [A, via abs page]. | Supports the single-pass-N design and the wrapper that feeds earlier batches back in as priors. |
| Reaching Beyond the Mode: RL for Distributional Reasoning | 2026 | https://arxiv.org/abs/2603.24844 | RL that trains a model to emit several answers in one pass improves diversity, coverage and set-level calibration over single-answer baselines [A, via abs page]. | Evidence that set-level training works. Reasoning/QA domain, not open-ended generation. |
| Vector Policy Optimization (training for diversity improves test-time search) | 2026 | https://arxiv.org/abs/2605.22817 | RL replacing GRPO advantages to train a set of diverse solutions; better pass@k and best@k at larger budgets [A, via abs page]. | Same direction; later candidates conditioning on earlier ones is the mechanism. |
| Escaping the Mode: Multi-Answer RL in LMs (ICML 2026 poster) | 2026 | https://icml.cc/virtual/2026/poster/60952 | Multi-answer RL, reported in a search snippet only [unverified]. | Do not cite until opened. |
| How Far Can We Extract Diverse Perspectives from LLMs? (Hayati et al.) | 2023 | https://arxiv.org/abs/2311.09799 | Criteria-based prompting grounds more diverse generations [A, partial]. | Condition items on explicit attributes/criteria in the synthetic-data prompt. |
| Diverse Beam Search (Vijayakumar et al.) | 2016 | https://arxiv.org/abs/1610.02424 | Group-wise diversity penalty at decode time [M]. | Decode-time fallback; not a substitute for training. |

Gap: no paper was found that directly tests exclusion conditioning (given prior items, generate items not near them) as a training target. A web search for "previously generated samples in prompt to avoid duplicates" found none. Self-Instruct (Q4) filters by ROUGE-L against the pool after the fact, which is the closest analogue. This is the project's main untested element.

## Q4. Distillation with synthetic data; data size for narrow LoRA tasks; diversity filtering

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| Self-Instruct (Wang et al.) | 2022 | https://arxiv.org/abs/2212.10560 | Bootstrapped instruction data from a model, filtered by ROUGE-L similarity to the pool, improves instruction following [M]. | The generate-then-filter pipeline is established; swap ROUGE-L for embeddings. |
| LIMA: Less Is More for Alignment (Zhou et al.) | 2023 | https://arxiv.org/abs/2305.11206 | 1,000 curated examples taught response formats and generalised; almost all knowledge comes from pretraining [A]. | A narrow format-following task may need only hundreds to low thousands of high-quality tuples; budget around 1-5k and measure the curve. |
| AlpaGasus (Chen et al.) | 2023 | https://arxiv.org/abs/2307.08701 | Filtering to a small high-quality subset beat training on all data [M]. | Aggressive filtering is fine; do not keep every candidate. |
| What Makes Good Data for Alignment? Deita (Liu et al.) | 2023 | https://arxiv.org/abs/2312.15685 | Data selection by complexity, quality and diversity gives strong results with few examples [M]. | Select on diversity of tuples (domain, archetype, N), not only item quality. |
| Data Diversity Matters for Robust Instruction Tuning (QDIT) | 2023 | https://arxiv.org/abs/2311.14736 | Quality-diversity trade-off; more diversity raises worst-case instruction-following performance [A]. | Balance the training mix across the taxonomy archetypes to protect worst-case behaviour. |
| Surveying the Effects of Quality, Diversity and Complexity in Synthetic Data | 2024 | https://arxiv.org/abs/2412.02980 | Quality helps in-distribution, diversity helps OOD, complexity both; quality and diversity trade off [A, via abs page]. | Tuple diversity matters for generalisation to unseen domains. |
| What Matters in LLM-generated Data: Diversity and Its Effect on Model Fine-Tuning | 2025 | https://arxiv.org/abs/2506.19262 | Moderately diverse generated data helps; highly diverse data hurt [A, via abs page]. | Do not maximise diversity of the training data blindly; cap similarity thresholds at moderate levels and test. |
| SemDeDup (Abbas et al.) | 2023 | https://arxiv.org/abs/2303.09540 | Embedding-based removal of semantic duplicates drops 50% of LAION with minimal loss [A]. | Validates the embedding dedup step (cluster, then threshold within cluster). |
| Deduplicating Training Data Makes LMs Better (Lee et al.) | 2021 | https://arxiv.org/abs/2107.06499 | Dedup reduces memorisation and does not hurt quality [M]. | Dedup training outputs against priors to avoid teaching copying. |
| The Curse of Recursion (Shumailov et al.) | 2023 | https://arxiv.org/abs/2305.17493 | Training on model-generated data loses distribution tails [M]. | Synthetic teacher data narrows tails; mix in hold-out-as-target gold items from real lists. |
| LoRA Learns Less and Forgets Less (Biderman et al.) | 2024 | https://arxiv.org/abs/2405.09673 | LoRA underperforms full fine-tuning on code/math at 100K-example scale but forgets less [A]. | For a format/behaviour task LoRA is reasonable; expect weaker new-knowledge acquisition (K2 tasks stay out of scope). |

## Q5. Metrics and pitfalls

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| The Vendi Score (Friedman & Dieng) | 2022 | https://arxiv.org/abs/2210.02410 | Diversity as the exponential of the entropy of the similarity-matrix eigenvalues, an effective number of distinct items [M]. | Primary intra-set metric: interpretable as "effective N" out of N. |
| A Diversity-Promoting Objective Function (Li et al.) | 2015 | https://arxiv.org/abs/1510.03055 | Introduces distinct-n [M]. | Cheap lexical check only; blind to paraphrase. |
| Texygen (Zhu et al.) | 2018 | https://arxiv.org/abs/1802.01886 | Introduces self-BLEU [M]. | Lexical; use only as a sanity metric. |
| Evaluating the Evaluation of Diversity in NLG (Tevet & Berant) | 2020 | https://arxiv.org/abs/2004.02990 | Compares diversity metrics against human judgement and finds they vary in reliability and in sensitivity to quality [M]. | Validate the chosen metric against a small human ranking. |
| Evaluating the Diversity and Quality of LLM Generated Content | 2025 | https://arxiv.org/abs/2504.12522 | Diversity must be conditioned on quality [A]. | See Q1. |
| NoveltyBench | 2025 | https://arxiv.org/abs/2504.05228 | Counts functionally distinct generations, not lexical variants [A, partial]. | Prefer semantic or functional equivalence classes. |
| Judging LLM-as-a-Judge with MT-Bench (Zheng et al.) | 2023 | https://arxiv.org/abs/2306.05685 | LLM judges agree with humans ~80% but show position, verbosity and self-enhancement bias [M]. | Randomise order, use a judge from a different family than the teacher. |
| Large Language Models are not Fair Evaluators (Wang et al.) | 2023 | https://arxiv.org/abs/2305.17926 | Judge verdicts flip with candidate order [M]. | Same. |
| Self-Preference Bias in LLM-as-a-Judge (Wataoka et al.) | 2024 | https://arxiv.org/abs/2410.21819 | Judges favour outputs with lower perplexity under themselves, i.e. their own style [M]. | Do not judge a Haiku-distilled student with Haiku. |

Pitfalls specific to this project: embedding novelty rewards off-topic outputs (needs the fit metric from the README); embedding cosine thresholds are model-dependent and should be calibrated on hold-out-as-target gold items; Si et al. show LLM self-evaluation of novelty fails; embedding distance can be satisfied by format drift.

## Q6. Resume / career-path generation

| Paper | Year | Link | Key finding | Implication |
|---|---|---|---|---|
| Generative Job Recommendations with LLM, GIRL (Zheng et al.) | 2023 | https://arxiv.org/abs/2307.02157 | SFT an LLM to generate job descriptions from a CV, then PPO against a CV-JD matching reward model [A]. | Closest precedent for PRJ: SFT then preference-style tuning works for CV-conditioned generation. It optimises recruiter fit, not novelty. |
| AdaptJobRec | 2025 | https://arxiv.org/abs/2508.13423 | Agentic conversational career recommender on Walmart data, faster and more accurate than baselines; fine-tuned 7-8B models on job-transition data [A, via abs page; fine-tune details from search snippet] | Small models are used in practice; the task is next-job prediction, not broad alternatives. |
| Augmented Fine-Tuned LLMs for Enhanced Recruitment Automation | 2025 | https://arxiv.org/abs/2509.06196 | Fine-tuned Llama/Mistral/Phi-4/Gemma on resume parsing and matching [unverified beyond search snippet] | Resume extraction (P3) is feasible with small fine-tuned models. |
| Toward more realistic career path prediction (Senger et al.) | 2025 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12415007/ | Compares linear, MLP, LSTM and LLM predictors; discusses scarce public benchmarks [unverified, search snippet; link returned a redirect] | Evaluation here is next-job accuracy against real histories, which does not measure the project's "diverse alternatives" goal. |
| JobHop (arXiv 2505.07653) | 2025 | https://arxiv.org/abs/2505.07653 | Dataset of career trajectories (seen in arXiv search results, abstract not read) [unverified] | Possible source for PRJ training data. |

Gap: no evaluation of "diverse alternative career paths" generation was found. PRJ has no benchmark; ground truth is undefined, so a judge-based usefulness eval is the only option.

## Viability assessment

Supported by the literature
- Mode collapse from preference tuning is well documented (Kirk, Shypula, NoveltyBench, Hivemind), and diversity can be partly restored by training (DivPO, Chung et al., DARLING) with preserved quality. A 8B-scale preference-tuning stage is established practice.
- Generating a set in one pass beats independent sampling on diversity at comparable quality (Troshin; Verbalized Sampling), and training for multi-answer output works (Reaching Beyond the Mode, VPO).
- Small curated sets are enough to teach a format-following behaviour (LIMA, AlpaGasus, Deita), and embedding dedup is a validated filter (SemDeDup). LoRA is adequate for behaviour change.
- CV-conditioned generation with SFT plus preference tuning has a precedent (GIRL).

Risky
- Teacher homogeneity: a single Haiku teacher is one voice (Hivemind, Curse of Recursion), so the student may inherit its blind spots and collapsed tails.
- Over-diverse data hurts (What Matters in LLM-generated Data); the novelty filter threshold needs tuning, not maximising.
- Diversity metrics and LLM judges are biased (Tevet, MT-Bench, self-preference); novelty judged by LLMs did not predict execution outcomes (Ideation-Execution Gap).
- SFT itself reduces diversity (GEM), and DPO may reduce it further unless pairs are built diversity-aware.
- Verbalized Sampling is a free training-free baseline that may already close much of the gap for frontier models; the fine-tune must be justified for cost, latency or small-model deployment instead.

Untested (no paper found)
- Exclusion conditioning against a given prior list as a training target, and its generalisation across archetypes (EXT, GAP, PRJ, VAR).
- Long priors (L/XL bins) for small models.
- Format adherence at N = 20-50 with O3/O4 items in a single pass.
- Open-ended profile projection quality (no benchmark).

Verdict: viable and well motivated, with the exclusion-conditioned training target being the novel and unproven part. The overall risk is moderate; the baseline step (frontier model plus Verbalized Sampling prompt) should come first, as the README already plans.

## Design implications

Objective
1. SFT with LoRA on a base or lightly instruct-tuned 3-8B model (West & Potts suggest the base); keep SFT short and measure diversity after SFT before DPO (GEM).
2. DPO with DivPO-style pairs: sample a pool per prompt, chosen = most diverse item set above the quality and format gate, rejected = prior-paraphrasing or collapsed set. Consider Chung et al.'s deviation weighting as an alternative. Treat DARLING/multi-answer RL as a later option.
3. Train on whole-set outputs (the N-item array) so later items condition on earlier ones (Troshin, Reaching Beyond the Mode). Wrapper handles N above ~20 by batching with prior batches appended to priors.

Data
4. Use two or more teacher families, or at least varied prompts with criteria/attributes (Hayati), to reduce teacher homogeneity. Mix in hold-out-as-target gold items from real lists.
5. Filter in three passes: format validity, near-duplicate of priors (calibrated embedding threshold), and intra-set dedup with SemDeDup-style clustering. Do not over-filter to maximum diversity.
6. Start with 1-2k tuples, balanced across taxonomy archetypes and size bins (QDIT), and run a small data-scaling curve (500/1k/2k) rather than assuming.
7. Create DPO rejected examples programmatically: paraphrases of priors, and sets collapsed onto 3-4 clusters.

Metrics
8. Report together, per archetype: format validity and exact-N rate; max cosine to any prior (calibrated on gold items); Vendi score over item embeddings (effective N); quality-conditioned diversity (Shypula); NoveltyBench-style distinct-class counts for a spot check; distinct-n/self-BLEU only as sanity checks.
9. In-domain fit and usefulness by LLM judge from a different family than the teacher, with randomised order; validate the judge and the diversity metric on a small human-ranked set (Tevet, MT-Bench, Wataoka).
10. Baselines: frontier model with a strong prompt, the same model with a Verbalized Sampling prompt, the untuned student, and the student with iterative (sequential) prompting.

Scope
11. Keep K2 (current facts) tasks out of the model; LoRA learns less new knowledge (Biderman).
12. PRJ: extract the CV to a list upstream (P3). Expect to evaluate it by judge only; GIRL is the reference for CV-to-JD generation.

## Open follow-ups

- Verify the `[M]` findings before citing in any public document.
- Search AUT/divergent-thinking benchmark papers and any exclusion-conditioning or "generate novel items not in list" work, which this scan did not find.
- Open the unverified items (Escaping the Mode, Senger et al., JobHop, 2509.06196).
