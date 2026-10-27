# Architecture options: base model, training stack, venue, enforcement, data cost

Dated 2026-10-27. Research for the proof-of-concept fine-tune described in `README.md` and `docs/planning/taxonomy.md`.

Conventions: **[C]** = confirmed from a model card, config.json, doc page or API response opened on 2026-10-27 (source given). **[A]** = assumed or estimated from general knowledge or arithmetic; verify before relying on it. Hub metadata came from `https://huggingface.co/api/models/<id>` and `https://huggingface.co/<id>/raw/main/config.json`.

Requirement recap: text in, JSON array out; inputs up to about 32k tokens (100 podcast prompts is about 12k), outputs up to a few thousand tokens; must run locally on a consumer GPU or CPU; trained with LoRA/QLoRA on a rented or free GPU.

## 1. Landscape (what is current)

Searches of the Hub by author, sorted by creation date, show the small-model field has moved a lot since 2025 [C]:

- **Qwen3.5** (released 2026-02-27/28): dense 0.8B, 2B, 4B, 9B, plus larger dense and MoE sizes. Apache 2.0. Newer Qwen lines exist but have no small sizes: Qwen3.6 (2026-04) ships only 27B dense and 35B-A3B MoE; Qwen3.8 (2026-08) ships 27B, a 180B "Flash-Next" and a 2.4T model. Qwen3.5 is therefore still the current small Qwen family.
- **Gemma 4** (E2B/E4B 2026-03-02, 12B 2026-05-23, 26B-A4B MoE, 31B). Apache 2.0 (Gemma 3 used the Gemma licence).
- **Granite 4.2** (3B, 8B, 30B, 2026-08-07), Apache 2.0, with thinking modes.
- **Ministral 3** (3B, 8B, 14B, Instruct and Reasoning, Dec 2025 "2512"). No newer small Mistral text model found in 2026 (Mistral's recent uploads are Small 4 119B, Medium 3.5 128B and specialist models).
- **Phi-4-mini** (2025-02) is still Microsoft's latest general small instruct model in the listing I saw; **SmolLM3-3B** (2025-07) is Hugging Face's latest; **Llama 3.2/3.1** (2024) have had no small successor on the Hub (Llama 4 is 17B-active MoE).
- **LFM3-1.7B** (Liquid AI, 2026-10-23, licence `lfm1.0`) is new but custom-licensed and early.

## 2. Base model comparison

All are Apache 2.0 unless stated. "Native ctx" is `max_position_embeddings` from config.json [C] unless marked.

| Model | Params | Native ctx | Thinking toggle | Multilingual / Hebrew | JSON / structured | Tooling | Notes |
|---|---|---|---|---|---|---|---|
| [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | 4.66B total (incl. vision encoder) [C] | 262,144 [C] | Yes, `enable_thinking=False` via chat template kwargs; thinks by default at 4B and 9B [C]; 0.8B/2B default to non-thinking [C] | "201 languages and dialects" [C]; Hebrew not named in the card, so test it | Not a headline claim in the card; Qwen family is strong at JSON [A] | Unsloth bf16 LoRA 10 GB with free Colab notebook [C]; unsloth GGUF (1.2M downloads) [C]; Ollama `qwen3.5` page exists [C]; vLLM, SGLang [C] | Hybrid: 3 of every 4 layers are Gated DeltaNet linear attention, so long-context cost is low [C]. Needs Transformers v5; custom Triton kernels slow to compile, worst on T4 [C] |
| [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | 9.65B [C] | 262,144 [C] | Yes, thinks by default [C] | as above | as above | Unsloth bf16 LoRA 22 GB [C]; GGUF 1.46M downloads [C]; Ollama [C] | Same architecture as 4B. Unsloth says do not QLoRA Qwen3.5 (quantisation error higher than normal) [C] |
| [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B) | 2.27B [C] | 262,144 [C] | Yes; non-thinking by default [C] | as above | as above | Unsloth LoRA 5 GB, free Colab [C]; GGUF, Ollama [C] | Smaller fallback |
| [Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | 0.87B [C] | 262,144 [C] | Yes; non-thinking default (assumed same as 2B) [A] | as above | likely weak at 12k-token priors [A] | Unsloth LoRA 3 GB, free Colab [C] | CPU-friendly floor |
| [Gemma 4 E4B-it](https://huggingface.co/google/gemma-4-E4B-it) | 4.5B effective, 8.0B with embeddings [C] | 128K [C] | Yes; `<|think|>` token in system prompt, or `enable_thinking` [C] | 35+ languages supported, trained on 140+ [C]; Hebrew not named | Native function calling; native `system` role [C] | Unsloth LoRA 17 GB (page also says 10 GB for training; inconsistent) [C]; unsloth GGUF [C]; Ollama `gemma4` [C] | Sliding-window attention (512), full layer every 6th [C]. Unsloth notes loss of 13-15 is normal for E2B/E4B [C] |
| [Gemma 4 12B-it](https://huggingface.co/google/gemma-4-12B-it) | 11.95B [C] | 256K [C] | Yes [C] | as above | as above | unsloth GGUF [C]; no Unsloth VRAM figure found [C] | Above the 9B ceiling; too heavy for 16k+ LoRA on 24 GB [A] |
| [Granite 4.2 3B](https://huggingface.co/ibm-granite/granite-4.2-3b) | 3.66B [C] | 131,072 in config [C]; card for 8B claims 512K via extension [C] | Yes: full, non-thinking, low-effort [C, 8B card] | Tested: en, de, es, fr, ja, pt, ar, cs, it, ko, nl, zh. No Hebrew [C, 8B card] | Tool calling; enterprise focus [C] | Standard `GraniteForCausalLM`, so Unsloth/TRL/llama.cpp should work [A]; Ollama `granite4.2` [C] | Plain dense GQA transformer: simple, but full attention at 32k costs more memory |
| [Granite 4.2 8B](https://huggingface.co/ibm-granite/granite-4.2-8b) | 8.79B [C] | 131,072 [C] | Yes [C] | as above | as above | as above | Release date on card 2026-08-25 [C] |
| [Ministral-3-3B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512) | 3.85B [C] | 262,144 [C] | Separate Reasoning checkpoint, no toggle [C] | "dozens of languages" incl. Arabic; Hebrew not listed [C] | "native function calling and JSON outputting" [C] | vLLM recommended [C]; Ollama `ministral-3` [C]; Unsloth support [A] | Multimodal wrapper (`Mistral3ForConditionalGeneration`) |
| [Ministral-3-8B-Instruct-2512](https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512) | 8.92B [C] | 262,144 [C] | as above | as above | as above | as above | Dense GQA, 34 layers, 8 KV heads [C] |
| [SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) | 3.08B [C] | 65,536 in config, 128k via YaRN [C] | Yes: `/think`, `/no_think` or `enable_thinking` [C] | 6 languages [C]; no Hebrew | tool calling via `xml_tools` [C] | Full TRL support (Hugging Face model) [A]; GGUF exists [C]; no Ollama library page (404) [C] | Fully open recipe; weaker multilingual |
| [Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | 3.84B [C] | 131,072 [C] | No (separate reasoning model) [C] | Card says trained mostly on English; non-English worse [C] | function-call format [C]; MIT licence [C] | GGUF, Ollama [C] | 2025-02 vintage; skip |
| [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 4.02B [C] | 262,144 [C] | No (non-thinking only; separate Thinking checkpoint) [A] | Qwen3 multilingual (119 languages) [A] | Good [A] | Most mature Qwen tooling (Unsloth, TRL, Axolotl, Ollama) [A] | Older, plain transformer: the safe, boring option |
| [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8.19B [C] | 40,960 in config (YaRN to 131k) [C] | Yes [A] | as above | Good [A] | As above | Short native context |
| [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 8.03B [C] | 128K [A] | No | 8 official languages, no Hebrew [A] | Fair [A] | Everything supports it [A] | Llama 3.1 community licence (not Apache) [C]; 2024 vintage |
| [LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) | 1.73B [C] | 262,144 [C] | Not checked | 16 languages, no Hebrew [C] | Not checked | `custom_code` tag [C] | Licence `lfm1.0` (custom); released 4 days ago; skip |

Reading the table:

- **Context.** Everything credible is at or above 128k natively, so 32k input is within native range for all of them. Context length is not the discriminator; memory cost of training at 16-32k is (section 4).
- **Hebrew.** No model lists Hebrew explicitly in its card. Qwen3.5 (201 languages) and Gemma 4 (140+ pretraining languages) are the best bets; Granite, Phi, SmolLM3, LFM3 and Llama list languages without Hebrew [C]. This must be tested directly (a 20-item Hebrew prompt/format check) before choosing, because the podcast use case is English but the CV use case may not be.
- **Thinking.** For a brainstorming task, thinking is optional. A fine-tune should train in non-thinking mode (empty think block, using the model's own template) so the output is only the JSON array, with no `<think>` text to strip. Qwen3.5 4B/9B think by default [C], so the training template must set `enable_thinking=False` and inference must do the same. Mismatched chat templates are the most common cause of degraded results after export [C, Unsloth Qwen3.5 page].
- **JSON strength.** Model cards give no comparable structured-output benchmark. Treat JSON ability as "adequate for all; enforce at decode time" (section 5) rather than a selection criterion.

## 3. Training stack

Versions on PyPI today [C]: Unsloth 2026.10.9, TRL 1.16.0, Axolotl 0.21.1.

| | Unsloth | TRL (with PEFT) | Axolotl |
|---|---|---|---|
| What it is | Optimised LoRA/QLoRA/full fine-tuning wrapper, runs on TRL trainers | Hugging Face reference trainers | YAML-config training framework |
| SFT | Yes | `SFTTrainer` [C] | Yes [A] |
| DPO and preference | DPO, ORPO, KTO, GRPO, GSPO listed in its guide [C] | `DPOTrainer`, `KTOTrainer`, `GRPOTrainer`, `RLOOTrainer`; ORPO/CPO experimental [C] | DPO/ORPO/KTO [A] |
| Qwen3.5 / Gemma 4 | Both have dedicated Unsloth pages and free notebooks [C] | Works via Transformers v5 [A] | Not verified |
| Long sequences | Claims 4x longer context and chunked loss [C, guide]; no Qwen3.5-specific max given [C] | Padding-free, packing, Liger kernels, Ulysses sequence parallelism (HF blog 2026-03-09) [C, listed on index; details not read] | Sample packing, sequence parallel [A] |
| Single-GPU speed/memory | Best of the three [A] | Slower, more memory unless Liger and gradient checkpointing are on [A] | Similar to TRL [A] |
| Multi-GPU | Limited [A] | Strong (accelerate, DeepSpeed, FSDP) | Strong |
| Export | `save_pretrained_gguf` to `q4_k_m`/`q8_0`/`f16`, `push_to_hub_gguf` [C] | Merge adapter, convert with llama.cpp [A] | Same [A] |

Decisions:

- **LoRA vs QLoRA.** For Qwen3.5, Unsloth explicitly advises against 4-bit QLoRA (dense or MoE) and recommends bf16 LoRA [C]. For Gemma 4 it says QLoRA on E4B has a "minuscule" accuracy cost and suggests QLoRA E4B over LoRA E2B [C]. For Ministral/Granite/Qwen3 (plain transformers) QLoRA is the usual choice on 16-24 GB cards [A]. For this task, 4B bf16 LoRA fits where QLoRA would otherwise be needed, so use bf16 LoRA at 4B and keep QLoRA for 8-9B on small cards.
- **DPO.** The README plans DPO pairs (chosen = passes all filters; rejected = paraphrases priors, collapses, or breaks format). Both TRL and Unsloth support it [C]. DPO with 12k-token prompts is expensive: each step holds chosen and rejected sequences, and a reference-model pass (with LoRA the reference is the adapter-disabled base, so no second copy) [A]. Plan SFT first, DPO as a short second stage (a few hundred to 1-2k pairs).
- **Pick Unsloth** for the POC (single GPU, free notebooks, GGUF export in one call) and fall back to plain TRL if Unsloth lags a new architecture; TRL is the escape hatch because Unsloth runs on it. Axolotl is not needed for one GPU.

## 4. Compute: memory, time, venues

### Memory for LoRA SFT at 16k-32k tokens

Hard numbers [C] are only Unsloth's short-sequence VRAM figures for bf16 LoRA: Qwen3.5 0.8B 3 GB, 2B 5 GB, 4B 10 GB, 9B 22 GB; Gemma 4 E2B 8-10 GB, E4B 17 GB. The Unsloth pages give no Qwen3.5 or Gemma 4 figure at 16-32k. Everything below is my estimate [A] from first principles and should be measured with a 1-step dry run.

Method: weights + LoRA optimiser state (small) + checkpointed activations + loss logits. With gradient checkpointing, stored activations are about `layers x seq x hidden x 2 bytes`. For Qwen3.5-4B (32 layers, hidden 2560) at 32k tokens that is about 5 GB; at 16k about 2.7 GB. The per-layer recompute peak adds a few GB, and only 8 of 32 layers use full attention [C], which keeps it low. The big trap is the loss: Qwen3.5's vocabulary is 248,320 [C], so full fp32 logits at 32k tokens would be about 32 GB. The training stack must use chunked cross-entropy (Unsloth does; in TRL enable Liger or equivalent) [A].

| Model | Config | 16k seq | 32k seq | Fits |
|---|---|---|---|---|
| Qwen3.5-4B | bf16 LoRA, r=16-32, grad ckpt, chunked loss | about 16-20 GB [A] | about 24-32 GB [A] | 16k on 24 GB card; 32k wants 40-48 GB (L40S/A6000) or 80 GB (A100) |
| Qwen3.5-9B | bf16 LoRA | about 32-38 GB [A] | about 45-60 GB [A] | 80 GB card for 32k; L40S 48 GB for 16k |
| Qwen3-8B / Ministral-3-8B / Granite-4.2-8B | QLoRA 4-bit | about 14-20 GB at 16k [A] | about 24-34 GB [A] (full-attention KV/activations grow faster than Qwen3.5's hybrid) | 24 GB at 16k |
| Gemma 4 E4B | LoRA | about 24-30 GB at 16k [A] | about 36-44 GB [A] | 80 GB to be safe |

Practical consequence: most training examples need not be 32k. The taxonomy's own bins show 100 podcast priors at about 12k and short lists far below that. Cap training at 16k tokens for the POC, include a handful of 24-32k examples only if the use case demands it, and test long-input behaviour at inference (Qwen3.5's native 262k leaves headroom) [A].

### Time

Throughput guesses [A]: Unsloth on an A100 80 GB at roughly 4-6k tokens/s for 4B and 1.5-2.5k tokens/s for 9B in LoRA. Dataset size is the lever. Example: 3,000 examples averaging 6k tokens is 18M tokens per epoch: 4B about 1-1.3 h/epoch, 9B about 2-3.5 h/epoch. A 1,000-example, 2-epoch POC at 4B is therefore about 1-1.5 h. Qwen3.5 Mamba-style kernels compile slowly on first run, especially T4 [C].

### Venues and indicative prices

| Venue | Price | Fit |
|---|---|---|
| Local GPU | none on this machine: `nvidia-smi` is not installed [C] | Inference only (CPU/GGUF) |
| Google Colab free | T4 16 GB, free [A: could not fetch current plan page, 403] | Qwen3.5 0.8B/2B/4B Unsloth notebooks exist for it [C], but T4 plus Mamba kernel compile plus 16k context makes 4B at 16k unrealistic; use only for a 2B smoke test at 2-4k |
| Colab paid (Pro / Pay-As-You-Go) | about $10/month Pro; A100/H100/L4 via compute units [A, unverified] | Convenient notebook route for 4B at 16k |
| Kaggle | about 30 GPU h/week, 2x T4 or P100, 16 GB each [A, doc fetch returned no body] | Free smoke tests; not for 16k |
| HF Jobs | a10g-small 24 GB $1.00/h; l40sx1 48 GB $1.80/h; a100-large 80 GB $2.50/h; h200 141 GB $5.00/h; rtx-pro-6000 96 GB $2.75/h; per-minute billing, needs positive credit balance, default 30 min timeout so set `--timeout` [C, huggingface_hub Jobs doc] | Good fit: `hf jobs uv run` with a TRL/Unsloth script, data and checkpoints on the Hub. Note HF-native dataset is already private on the Hub |
| RunPod (on-demand pods) | Community / Secure per hour: RTX 4090 24 GB $0.34 / $0.89; L40S 48 GB $0.79 / $1.09; A100 80 GB PCIe $1.19 / $1.79; H100 80 GB PCIe $1.99 / $2.89; H100 SXM $2.69 / $3.99 [C, runpod.io/pricing] | Cheapest per hour; you manage the pod |
| Modal | per second: L40S $0.000542 (about $1.95/h), A100 40 GB $0.000583 (about $2.10/h), A100 80 GB $0.000694 (about $2.50/h), H100 $0.001097 (about $3.95/h); $30/month free credit on Starter [C, modal.com/pricing] | Scripted runs, no idle billing; the free credit covers a POC |

Indicative POC compute cost [A, arithmetic from [C] prices]:

- 4B SFT, 1,000-3,000 examples, 2 epochs, 16k cap: 1.5-4 h on an A100 80 GB at $1.19-2.50/h, so about $2-10. A 24 GB L4/4090 route costs less per hour but forces a shorter cap.
- 9B SFT same data: 4-8 h, so about $5-20.
- DPO stage: add 25-50% to SFT time.
- Eval/inference sweeps: negligible if run with GGUF locally or on a cheap GPU.
- Budget a 3x multiplier for failed runs and hyperparameter retries: still under about $50 for a 4B POC. That fits inside the standing $5-per-task approval only for single runs, so confirm before launching the real run.

## 5. Format adherence: train it or enforce it?

Recommendation: **both, with different jobs.** Enforce structure at decode time; train the things a grammar cannot express.

What a grammar can guarantee: valid JSON, an array, the exact field names and types from the request's `format`, and a fixed item count (`minItems = maxItems = N`). The schema.md output is a JSON array of objects whose fields come from `format.fields`, so a per-request JSON Schema can be generated mechanically.

What a grammar cannot do: novelty versus the priors, diversity across the N items, length and style limits beyond simple `maxLength`, domain fit, or semantic compliance with per-field guidance. Those are the point of the fine-tune and must be trained (SFT then DPO on the pairs described in the README).

Tools:

| Tool | Facts | Fit |
|---|---|---|
| llama.cpp GBNF grammars | Works in CLI and server; `--json-schema` / `-j`, `response_format` on `/chat/completions`, raw `grammar` field. Schema constrains output but is not added to the prompt, so the format must also be described in the prompt. Silently skips unsupported keywords (`uniqueItems`, `if/then/else`, `contains`; no `patternProperties`; `pattern` must be anchored; `additionalProperties` defaults to false) [C, ggml-org/llama.cpp grammars/README.md] | Primary local route (GGUF, Ollama's backend). Check the generated grammar after conversion |
| vLLM structured outputs | Backends `xgrammar` and `guidance` (`auto` default); options `json`, `regex`, `choice`, `grammar`, `structural_tag`; request via `extra_body={"structured_outputs": {...}}` or `response_format: json_schema`; old `guided_*` fields removed in v0.12.0; lm-format-enforcer deprecated; works with reasoning models via `--reasoning-parser` [C, docs.vllm.ai]. One Unsloth note says vLLM 0.16.0 did not support Qwen3.5 [C]; recheck the current vLLM version | GPU serving and batch evaluation |
| Outlines | Current PyPI release 1.3.3 [C]. Supports Transformers, llama.cpp and vLLM backends [A]; not read in detail | Useful for Python-level generation and eval harnesses; not needed if llama.cpp or vLLM suffices |
| Provider-side | Ollama accepts a JSON schema in `format` [A] | Convenient for a local app |

Interaction with thinking: grammars that start at the first token will also constrain the thinking block. Run in non-thinking mode (recommended above), or apply the grammar after `</think>` using the backend's structural-tag option [C, vLLM doc].

Trained-in format still matters because constrained decoding can force-complete a bad generation into valid-but-poor JSON (for example truncated items, repeated items to satisfy `minItems`) [A]. Include the schema-valid-rate, item-count-match and per-field-length checks in the eval so you can compare "trained, unconstrained" with "trained plus constrained" and see whether the grammar is rescuing the model. The existing validator (`Data plumbing` commit) can be reused as the training-data filter.

## 6. Synthetic data generation cost (Claude Batch API)

From `platform.claude.com/docs/en/about-claude/pricing` and `.../models/overview` [C, fetched 2026-10-27]:

- Current Haiku: **Claude Haiku 5.5, API ID `claude-haiku-5-5`** (dateless ID is a pinned snapshot; no separate alias). 1M context, 128K max output, adaptive thinking, default effort `medium`. Retirement "not sooner than October 7, 2027".
- Batch API gives **50% off both input and output** [C].
- Haiku 5.5 is priced by prompt length: up to 100,000 tokens $0.10 in / $0.50 out per MTok standard; **$0.05 in / $0.25 out batch**. Over 100k prompt tokens it is $0.25 / $1.25 batch [C]. This project's prompts are far below 100k.
- Comparators, batch per MTok in/out [C]: Haiku 4.5 $0.50/$2.50; Sonnet 5.5 $1/$5 (Sonnet 5 same); Opus 5.5 $2/$10; Fable 5.1 $5/$25. Standard Sonnet 5.5 is $2/$10, Opus 5.5 $4/$20.
- Batches can raise output to 300k tokens with a beta header, not needed here [C].

Estimate for **5,000 examples at about 4k input and 2k output tokens each** (20M input tokens, 10M output tokens):

| Model | Batch in | Batch out | Total batch | Total standard (no batch) |
|---|---|---|---|---|
| Haiku 5.5 | 20 x 0.05 = $1.00 | 10 x 0.25 = $2.50 | **$3.50** | $7.00 |
| Haiku 4.5 | $10.00 | $25.00 | $35.00 | $70.00 |
| Sonnet 5.5 | $20.00 | $50.00 | **$70.00** | $140.00 |
| Opus 5.5 | $40.00 | $100.00 | $140.00 | $280.00 |

Sensitivities [A]:

- **Thinking tokens bill as output.** Haiku 5.5 uses adaptive thinking at `medium` effort by default [C]; whether thinking can be fully disabled on Haiku 5.5 was not confirmed (the Models API reports it cannot be disabled on Sonnet 5.5 [C]). If thinking doubles output, Haiku 5.5 batch is about $6; set `effort` low to limit it.
- **Longer priors.** If the average input is 8k instead of 4k (to cover 12k-token podcast lists), add $1.00 for Haiku 5.5, $20 for Sonnet 5.5.
- **Prompt caching** reads cost 10% of base input on Haiku 5.5 [C] and stack with batch [C]; it helps only if many examples share the same priors list (for example several different tasks over one 12k priors block).
- **Multiple candidates for DPO.** Rejected samples can come from the small base model locally at no API cost; only chosen outputs and any judge pass need Claude.
- **Quality caveat.** Whether Haiku 5.5 is creative and novelty-aware enough as the teacher is untested. Cheap plan: generate 200 with Haiku 5.5 ($0.14) and 200 with Sonnet 5.5 ($2.80), compare on the novelty/diversity metrics, then scale the winner. A hybrid (Haiku 5.5 for bulk, Sonnet 5.5 as filter/judge on about 20% of rows) costs under $20 for 5,000 rows.
- Use the Claude API route with the Message Batches endpoint; results within 24 h typically [A].

## 7. Recommendation for the POC

**Primary base: [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)** (instruct/post-trained checkpoint, non-thinking mode).

Reasons:
1. Native 262k context and a hybrid linear-attention design [C] make 16-32k training and inference cheaper than any plain-transformer 4B (Granite, Phi, SmolLM3, Qwen3-4B), which matters for the 12k-token priors case.
2. 201-language coverage [C] is the best available chance of workable Hebrew among small models; Granite, Phi, SmolLM3, LFM3 and Llama do not list it [C].
3. Apache 2.0 [C]; official Unsloth bf16 LoRA path at 10 GB with a free notebook and one-call GGUF export [C]; GGUF and Ollama both exist [C].
4. 4B at Q4 is roughly 3 GB on disk [A, from a partial scrape of the Ollama page], runnable on CPU or an 8 GB GPU for private CV inputs.
5. Newer, and benchmarked as at or near much larger models in its own card [C], so the fine-tune has headroom to work on novelty rather than basic competence.

Risks to check in the first hour: Transformers v5 and kernel compile time [C]; template/`enable_thinking` mismatch after GGUF export [C]; Qwen3.5-4B thinks by default [C], so training data should use the non-thinking template; confirm vLLM version supports Qwen3.5 before planning GPU serving [C, older note].

**Smaller fallback: [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B)** (non-thinking default, 5 GB LoRA, free Colab notebook) for smoke tests and for CPU-only deployment; the 0.8B is the floor if the 2B is still too slow on CPU. Same tokenizer and chat template, so the pipeline carries over unchanged. A different-family safety net if Qwen3.5 tooling bites: Gemma 4 E4B (Apache 2.0, 128k, native system role, cleaner QLoRA story) or the older, boringly reliable Qwen3-4B-Instruct-2507.

**Step-up (not for the POC): Qwen3.5-9B** (22 GB bf16 LoRA at short sequences) if the 4B plateaus on novelty or long-priors cases.

**Stack:** Unsloth with TRL under it. SFT first (bf16 LoRA, r=16-32, 16k max length, chunked loss, non-thinking template). DPO as a second short stage using TRL `DPOTrainer` or Unsloth's DPO path. Export GGUF `q4_k_m` and `q8_0`. At inference use llama.cpp `--json-schema` generated from `format.fields` with `minItems=maxItems=N`, in non-thinking mode.

**Venue:** Modal or HF Jobs on one A100 80 GB (about $2.50/h) for the real run, using the $30/month Modal credit if available; RunPod community A100 at $1.19/h if cost matters and manual pod management is acceptable. Smoke-test the pipeline on the free Colab 2B notebook first. Expected compute for the POC: about $2-10 per 4B SFT run, under $50 including retries and DPO [A].

**Synthetic data:** `claude-haiku-5-5` via Message Batches: about $3.50 for 5,000 examples at 4k in / 2k out ($7 without batching), up to about $6 if thinking inflates output; pilot 200 Haiku vs 200 Sonnet 5.5 ($0.14 vs $2.80) on the novelty metrics before scaling. Total POC budget (data + compute) is roughly $15-60.

**Open items before committing:** (1) test Hebrew on Qwen3.5-4B and Gemma 4 E4B with a small format-matched prompt; (2) do a one-step dry run at 16k and 32k to replace the memory estimates in section 4; (3) re-check Colab/Kaggle quotas (pages could not be read, section 4); (4) confirm the Haiku 5.5 thinking-disable behaviour in the batch endpoint; (5) confirm the current vLLM release supports Qwen3.5 if GPU serving is wanted.
