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
