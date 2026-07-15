<h1 align="center">João Felipe De Souza</h1>

<p align="center">
  <b>Systems Engineer · LLM Infrastructure · C++20 · Python</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Focus-LLM%20Inference%20Systems-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/C%2B%2B-20-00599C?style=flat-square&logo=cplusplus"/>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python"/>
  <img src="https://img.shields.io/badge/Build-CMake%20%2B%20Ninja-064F8C?style=flat-square"/>
  <img src="https://img.shields.io/badge/Platform-WSL%20%7C%20Linux-lightgrey?style=flat-square"/>
</p>

---

## About

I build **low-level simulators and tools for LLM inference infrastructure**,
focusing on memory management, scheduling, caching, and attention analysis.

Each project is designed as a standalone research lab:
measurable findings, reproducible pipelines, and paper-ready analysis.

---

## Portfolio

> Five projects that together cover the full LLM inference stack —
> from scheduling to attention mechanics.

---

### 🔧 [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab)

> *How should an LLM server defragment its KV-cache memory?*

A discrete-tick simulator comparing three compaction policies:
**NoCompaction**, **GreedyCompaction**, and **ThresholdCompaction**.

| | |
|---|---|
| Stack | C++20 + Python · CMake + Ninja |
| Method | 2D parameter sweep (31 configurations) · Pareto frontier analysis |

**Key findings:**
- ThresholdCompaction dominates GreedyCompaction across the entire Pareto frontier
- 11 "free compaction" configurations — zero observable latency impact
- Optimal point: τ=0.473, κ=128 → 2 events in 120s, ΔP95 = 0.00ms

---

### 🌲 [prefix-cache-sim](https://github.com/JohnScheuer/prefix-cache-sim)

> *How much latency can be saved by reusing KV-cache across requests?*

A RadixTree-based prefix cache simulator with four eviction policies:
**LRU**, **LFU**, **FIFO**, and **SizeLRU**.

| | |
|---|---|
| Stack | C++20 + Python · CMake + Ninja |
| Method | Hit rate sweep · multi-turn workloads · Zipf distribution |

**Key findings:**
- LFU dominates in small caches with skewed (Zipf) workloads
- Multi-turn sessions push hit rate to 60%+
- SizeLRU degrades with high alpha — blocks eviction of large nodes

---

### ⚡ [llm-inference-scheduler](https://github.com/JohnScheuer/llm-inference-scheduler)

> *Which requests should run, in what order, and when to preempt?*

A continuous-batching scheduler simulator with five scheduling policies:
**FCFS**, **ContinuousBatching**, **Priority**, **SLOAware**, and **ChunkedPrefill**.

| | |
|---|---|
| Stack | C++20 + Python · CMake + Ninja |
| Method | Arrival rate sweep · SLO compliance analysis · preemption cost model |

**Key findings:**
- ChunkedPrefill eliminates prefill starvation — best TTFT across all loads
- SLOAware achieves highest SLO compliance under mixed-priority workloads
- FCFS collapses at high arrival rates — gpu_utilization drops below 40%

---

### 📊 [inference-dashboard](https://inference-dashboard-elt5ygbauvqecfukshtwew.streamlit.app/)

> *Consolidated interactive dashboard for 20 research projects.*

A single Streamlit dashboard aggregating all simulation and profiling results:
10 subsystems, 1700+ runs, interactive Plotly visualizations.

| | |
|---|---|
| Stack | Python · Streamlit · Plotly · Pandas |
| Content | Speculative decoding, tensor allocator, MoE routing, KV disaggregation, attention kernels, prefix cache, real hardware profiling, continuous batching |

**Key findings:**
- Single link for portfolio presentation
- Side-by-side simulation vs. real hardware comparison
- Interactive charts — recrutadores não precisam instalar nada

---

### 🔤 [tokenizer-throughput-benchmark](https://github.com/JohnScheuer/tokenizer-throughput-benchmark)

> *Is Tiktoken really faster? Not under concurrent serving.*

Tokenization benchmark across GPT-2, LLaMA, Qwen2, and Tiktoken with
concurrency analysis, serving simulation, and RPS capacity planning.

| | |
|---|---|
| Stack | Python · Transformers · Tiktoken · SentencePiece |
| Method | Thread/process parallelism · serving simulation · saturation test |

**Key findings:**
- Tiktoken is 2-4× faster single-threaded but **6.5× worse** under 1ms SLO
- GPT-2 (HF) sustains **6536 RPS** at p99 < 1ms vs Tiktoken's **999 RPS**
- HuggingFace releases GIL during Rust execution; Tiktoken holds it
- Tiktoken wins 10-18× on detokenization (streaming decode)

---

### ⚡ [flash-attention-benchmark](https://github.com/JohnScheuer/flash-attention-benchmark)

> *What attention optimization works on consumer Turing GPUs?*

Benchmark of 4 attention backends including a custom Triton FlashAttention
implementation that runs on RTX 2070 (sm 7.5) where official FlashAttention
is unsupported.

| | |
|---|---|
| Stack | Python · PyTorch · Triton |
| Method | Latency/memory profiling · custom Triton kernel |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- SDPA efficient achieves **130× less memory** and **10× faster** than vanilla at seq=4096
- Custom Triton FlashAttention: **O(n) memory** but 64× slower than SDPA efficient
- Vanilla and SDPA math OOM at batch≥2, seq≥16384
- For Turing GPUs, SDPA efficient is the correct choice

---

### 🔍 [multi-query-attention-profiler](https://github.com/JohnScheuer/multi-query-attention-profiler)

> *How much KV-cache do GQA and MQA save — and at what quality cost?*

Profiler comparing MHA, GQA, and MQA attention variants in KV-cache memory,
decode throughput, and output fidelity via weight-collapsing proxy.

| | |
|---|---|
| Stack | Python · PyTorch |
| Method | KV-cache measurement · fidelity proxy · 3x repeated benchmark |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- MQA reduces KV-cache by **92%** but drops cosine similarity to **0.269**
- GQA-g2 halves KV-cache while preserving **~70%** fidelity — the industry sweet spot
- Decode throughput differs by only ~10–20% across variants

---

### 📅 [continuous-batching-scheduler](https://github.com/JohnScheuer/continuous-batching-scheduler)

> *Which scheduling policy should serve LLM requests?*

Iteration-level continuous batching simulator comparing FCFS, SJF, Fair, and Preemptive
policies on real GPU inference, validated across 5 random seeds.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Discrete-step simulation · Jain fairness · multi-seed validation |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- SJF reduces short-job TTFT by **81.5%** vs FCFS (17.1 vs 92.3 steps)
- SJF achieves best throughput (5.43 tok/step)
- SJF pays 34% lower Jain fairness vs FCFS
- Preemptive scheduling consistently underperforms due to re-prefill overhead

---

### ⏱️ [inference-latency-breakdown](https://github.com/JohnScheuer/inference-latency-breakdown)

> *Where does every millisecond go in the LLM inference pipeline?*

End-to-end latency profiler measuring tokenization, prefill, decode, and detokenization,
plus sensitivity analysis and a predictive latency model.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Per-phase timing · sensitivity analysis · linear model fitting |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Decode accounts for **94–97%** of total latency
- 2× faster decode improves e2e latency by **~47%**
- 2× faster prefill improves e2e by only **~2.2–2.5%**
- Total latency predicted with **~2–3% MAPE** using prompt and output length

---

### 🧮 [gpu-memory-profiler](https://github.com/JohnScheuer/gpu-memory-profiler)

> *Where does GPU memory actually go during transformer inference?*

VRAM breakdown profiler separating weights, KV-cache, and runtime overhead,
with per-layer analysis, activation hooks, and a predictive memory model.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | CUDA memory stats · forward hooks · linear model fitting |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- FFN layers dominate static VRAM (56.8% of weights in GPT-2-medium)
- Per-layer weight memory is perfectly uniform (std = 0.0000)
- Runtime overhead explains why analytical KV-cache estimates underpredict by 2–4×
- A fitted model predicts VRAM with R² = 0.999970 and <1.2% error

---

### ⏱️ [prefill-chunking-profiler](https://github.com/JohnScheuer/prefill-chunking-profiler)

> *Is chunked prefill a latency optimization — or a scheduling optimization?*

Empirical profiling of full vs chunked prefill in both isolated and mixed-workload settings,
showing that chunking hurts single-request TTFT but improves fairness under long-request interference.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | TTFT profiling · interleaving benchmark · fairness analysis |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Full prefill always wins isolated TTFT
- Chunking only reduces peak memory modestly
- In mixed workloads, chunking reduces short-request TTFT by ~20–23%
- Chunk256 gives the best compromise between long-request latency and fairness

---

### 🧠 [kv-cache-eviction-benchmark](https://github.com/JohnScheuer/kv-cache-eviction-benchmark)

> *Which tokens should an LLM keep when it cannot retain the full KV-cache?*

Real benchmark of KV-cache eviction policies on GPT-2-medium, comparing
sliding windows, sink-preserving windows, random eviction, and attention-based eviction.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | DynamicCache manipulation · teacher-forced perplexity · budget sweep |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- At tiny cache budgets, sink-preserving heuristics massively beat sliding windows
- At budget 64, sink8+window56 improves perplexity by ~59× over sliding_64 at the same memory
- At moderate budgets, attention-based eviction becomes superior
- attention_384 matches full-cache quality while cutting KV-cache by ~33%

---

### ⚡ [speculative-decoding-impl](https://github.com/JohnScheuer/speculative-decoding-impl)

> *Does speculative decoding actually speed up inference on consumer GPUs?*

Real implementation of draft+verify speculative decoding measuring when it helps in practice.
Compares GPT-2 → GPT-2-medium vs GPT-2 → GPT-2-large across 12 prompt types.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Greedy speculative decode · KV-cache management · prompt sweep |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- GPT-2 → GPT-2-large: mean best speedup **1.253×**, best case **1.846×**, 8/12 prompts positive
- GPT-2 → GPT-2-medium: mean best speedup **1.013×**, 6/12 prompts positive
- Speedup requires both high draft-target agreement and sufficiently expensive target
- Speculative decoding is not universal — it is a conditional systems optimization

---

### 🔢 [quantization-profiler](https://github.com/JohnScheuer/quantization-profiler)

> *Does lower precision actually speed up inference on consumer GPUs?*

Empirical profiling of FP32, FP16, INT8, and INT4 quantization across 80 runs
on GPT-2 and GPT-2-medium, with batch size sweep and perplexity tracking.

| | |
|---|---|
| Stack | Python · PyTorch · bitsandbytes · Transformers |
| Method | KV-cache decode benchmark · perplexity · batch sweep |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- FP16 is the best performance setting — 1.26–1.53× faster than FP32 at 50% memory
- INT4 reduces model memory by 76–82% with perplexity delta < 0.003
- On Turing-class GPUs, bitsandbytes quantization hurts decode throughput
- The value of INT4/INT8 here is capacity, not speed

---

### 💰 [inference-cost-calculator](https://github.com/JohnScheuer/inference-cost-calculator)

> *How much does it cost to run 1 million tokens? When does buying a GPU pay off?*

Cost analysis tool using real throughput measurements from my benchmarks.
Covers 13 GPU configurations, 9 API providers, and 10 analyses.

| | |
|---|---|
| Stack | Python · Pandas · Matplotlib · Rich |
| Method | Cost model · Pareto frontier · ROI · sensitivity analysis |

**Key findings:**
- RTX-2070 local ($0.0008/1M tok) beats every cloud option on cost per token
- No A100 cloud configuration beats local RTX in $/token — crossover needs 55× speedup
- GPT-4o API costs 18,750× more than local electricity per token
- RTX-2070 ($300 used) pays for itself in ~1 month vs A100 GCP spot at 250h/mo usage

---

### 🖥️ [model-serving-benchmark](https://github.com/JohnScheuer/model-serving-benchmark)

> *How much does serving strategy matter vs hardware?*

Benchmark comparing three LLM serving strategies on identical hardware:
**Naive**, **KV-Cache only**, and **Continuous Batching**.

| | |
|---|---|
| Stack | Python · PyTorch · FastAPI · httpx |
| Method | Async load generator · TTFT · throughput · client latency |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Naive and KV-cache collapse under load — client latency grows 30× at concurrency=8
- Batched server maintains 7–9ms TTFT regardless of concurrency
- Batched reaches 4521 tok/s at concurrency=32 — 25.8× single-request throughput
- KV-cache value only materializes when combined with batching

---

### 📈 [decode-batching-profiler](https://github.com/JohnScheuer/decode-batching-profiler)

> *How does batch size affect decode throughput, latency, and GPU memory?*

Empirical profiling of the decode path in GPT-2 and GPT-2-medium across
batch sizes 1–64 and context lengths 128–960.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · Matplotlib |
| Method | CUDA-event timing · Pareto frontier · regime detection · 3x repeats |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Batching gives near-free throughput gains up to the compute-to-memory-bandwidth crossover
- Crossover shifts left with longer context and larger models
- At gpt2-medium ctx=960 bs=64, throughput collapses to 1.4% of linear expectation
- Peak throughput batch is often not the best operating point — 90–97% of peak at ~half the latency

---

### 🔬 [attention-sink-profiler](https://github.com/JohnScheuer/attention-sink-profiler)

> *Empirical measurement of the attention sink phenomenon in real transformers.*

Measures attention distribution in GPT-2 and GPT-2-medium, with per-head
classification and masked-key ablation to assess functional impact on
tail perplexity and output distribution.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · Matplotlib |
| Method | Attention map extraction · per-head analysis · ablation experiments |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Sink is structural/positional, not semantic (random > natural text > repeated)
- Boost over uniform baseline reaches 82× for first 4 tokens at seq=1024
- 60% of GPT-2 heads are sink-oriented; effect concentrates in deep layers
- GPT-2-medium dilutes the sink compared to GPT-2 small
- Masking first 8 tokens degrades tail perplexity more than middle or random windows

---

## How They Fit Together

    +----------------------------------------------------------+
    |          LLM Inference Server (simulated)                |
    +------------------+-------------------+------------------+
    |   Scheduler      |   Prefix Cache    |  KV Compaction   |
    |                  |                   |                  |
    |  llm-inference   |  prefix-cache-sim |  kv-cache-       |
    |  -scheduler      |                   |  compaction-lab  |
    +------------------+-------------------+------------------+
      "what to run"      "what to reuse"    "how to manage RAM"

    +----------------------------------------------------------+
    |          Analysis & Visualization (across all)            |
    |                                                          |
    |  inference-dashboard  +  attention-sink-profiler         |
    |  (interactive plots)     (attention mechanics)           |
    +----------------------------------------------------------+

Each project is independent and fully reproducible.
Together they cover the full lifecycle of a request in an LLM server.

---

## Tech Stack

| Area | Tools |
|---|---|
| Core simulation | C++20, STL, CMake, Ninja |
| Deep learning | PyTorch, Transformers, CUDA |
| Analysis & plots | Python, pandas, numpy, matplotlib, Plotly |
| Dashboard | Streamlit, Plotly |
| Research output | LaTeX tables, Pareto frontier, regime classification |
| Environment | WSL, VS Code, GCC 15, Python 3.14 |

---

## Contact

- GitHub: [@JohnScheuer](https://github.com/JohnScheuer)
- Dashboard: [inference-dashboard.streamlit.app](https://inference-dashboard-elt5ygbauvqecfukshtwew.streamlit.app/)
- Projects: see pinned repositories below

---

<p align="center">
  <i>MIT License · Copyright (c) 2026 João Felipe De Souza</i>
</p>
