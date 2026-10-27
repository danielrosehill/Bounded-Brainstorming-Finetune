# Decisions and open questions

Newest first. Each decision: date, what, why, what would reverse it.

## Decided

- **2026-10-27: Prior-art verdict: nobody has published this exact task.** The Hub has no model, dataset or Space that conditions on a priors/exclusion list and returns N novel, format-matched items (`../research/prior-art-huggingface.md`). The literature supports each component: mode collapse is real and fixable with diversity-aware DPO (DivPO, arXiv 2501.18101), and single-pass N beats independent sampling (2509.17570). Training to *exclude given priors* is untested, and that is what this POC tests (`../research/prior-art-papers.md`). Baselines to beat: the base model prompted, and Verbalized Sampling prompting (2510.01171).
- **2026-10-27 (tentative, confirm after the Hebrew test and 16k dry run): Base = Qwen3.5-4B, non-thinking; fallback Qwen3.5-2B; alternative Gemma 4 E4B.** Stack Unsloth + TRL, bf16 LoRA (not 4-bit QLoRA on Qwen3.5), SFT then DPO, training sequence capped at 16k. Inference: llama.cpp/Ollama GGUF with `--json-schema` enforcing exactly N items. Reasons and costs: `../research/architecture-options.md`.
- **2026-10-27: Teacher = `claude-haiku-5-5` via Message Batches, but not alone.** About $3.50 per 5k tuples at 4k in / 2k out, according to Anthropic's pricing docs as read by the research pass. Single-teacher data is homogeneous (Artificial Hivemind, 2510.22954), so the pilot compares Haiku 5.5 against Sonnet 5.5 on 200 tuples each, the bulk mixes in hold-out tuples from real lists, and the judge comes from a different model family from the teacher.

- **2026-10-27: The project is a proof of concept.** Success = a LoRA adapter on a small open base that beats the base on novelty and diversity at equal fit. Production polish, multimodal input and a public release are out of scope until that is shown.
- **2026-10-27: The model is text-in, JSON-out only.** Files (PDF, DOCX, CSV) are converted by a wrapper; live checks (HF Hub, domains) run in the wrapper. See `context-requirements.md`.
- **2026-10-27: Architecture before data.** The base model's context length and template fix the tuple sizes, so the base is chosen before any synthetic data is generated.
- **2026-10-27: Synthetic data comes from a cheap batch generator** (Claude Haiku via the Message Batches API is the first candidate), plus hold-out tuples from real lists so that the targets are not all one generator's style.

## Open

| # | Question | Blocks | Notes |
|---|---|---|---|
| 1 | Confirm base: Hebrew check on Qwen3.5-4B vs Gemma 4 E4B; does vLLM serve Qwen3.5? | phase 3 | tentative pick above |
| 2 | Input budget: 16k or 32k? | data generation | 16k for POC; estimates 16–20 GB (16k) vs 24–32 GB (32k) at 4B, to replace with a dry run |
| 9 | Can Haiku 5.5 thinking be turned off or limited in batch? | data cost | thinking bills as output; set low effort |
| 3 | Enforce JSON with constrained decoding, or train it in? | eval design | probably both: train it, enforce at inference |
| 4 | Single-pass N vs batched calls for large N? | wrapper, data | batching assumed for `O3`/`O4` above ~20 items |
| 5 | Adopt schema v0.2 (`exclude`, typed `context`, `meta`)? | validator, data | proposal in `context-requirements.md` |
| 6 | Novelty threshold per archetype | eval, filtering | start 0.85 cosine; tune on real lists |
| 7 | Which embedding model for filtering and eval? | phase 4 | small local model for cost; must handle Hebrew if MWP/ASR priors include it |
| 8 | Where do real CVs for `PRJ` come from? | phase 7 | own CV only (private); synthetic CVs rendered to PDF and re-extracted for volume |
