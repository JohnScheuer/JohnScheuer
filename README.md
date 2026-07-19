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

> 33 projects covering the full LLM inference stack —
> from memory management and scheduling to distributed parallelism,
> speculative decoding, and long-context serving.

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

### 🔀 [request-routing-sim](https://github.com/JohnScheuer/request-routing-sim)

> *How do you distribute requests across multiple LLM serving instances to minimize TTFT?*

Discrete-event simulator comparing four routing strategies (round-robin, least-load,
prefix-aware, hybrid) across variable arrival rates, prefix sharing fractions, and
workload skew. Models KV cache locality, queue cost, and load imbalance to find the
optimal routing policy under realistic serving conditions.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · Zipf workload · prefix cache model · hybrid threshold sweep |

**Key findings:**
- Pure prefix-aware routing increases hit rate but **degrades TTFT** — queue builds faster than cache saves
- Hybrid(thr=1) matches prefix_aware on hit rate (**0.895**) and round-robin on TTFT (**104.7ms**) simultaneously
- Optimal threshold = **1** across all regimes — route to cached instance only if queue is empty or has 1 pending
- prefix_aware at high skew: imbalance=**0.856** — traffic concentrates, TTFT collapses to **280.3ms**
- Round-robin and least-load are **equivalent** under homogeneous instances — routing intelligence only pays with skewed workloads
- Cache locality and load balance are **not fundamentally in conflict** — a single queue-depth threshold resolves both

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

### 📡 [comm-cost-modeling](https://github.com/JohnScheuer/comm-cost-modeling)

> *Where does tensor parallelism stop scaling?*

Communication cost modeling with TP vs PP vs hybrid parallelism, combining real GPU
compute measurements with analytical alpha-beta models across PCIe 3.0 → NVLink v4.

| | |
|---|---|
| Stack | Python · PyTorch |
| Method | Compute instrumentation · alpha-beta model · scaling simulation · regime detection |
| Hardware | NVIDIA RTX 2070 (compute measurement) |

**Key findings:**
- PCIe 3.0 at 8 GPUs: **19.6% TP efficiency** — communication dominated (ratio=0.29)
- NVLink v3 at 8 GPUs: **68.0% TP efficiency** for LLaMA-7B, **87.8%** for Falcon-180B
- Pipeline parallelism wastes **46.7% of GPU time** in bubble at 8 stages — 4–6× slower than TP
- LLaMA-70B crosses compute/comm boundary at PCIe 4.0 (ratio=1.66) — on PCIe 3.0 it falls to 0.80
- LLaMA-13B achieves **96.9% efficiency** at TP=2 on NVLink v3 — near-perfect linear speedup
- PCIe 2-GPU TP costs **$0.092/1M tokens** — cheapest option for LLaMA-7B serving
- Alpha-beta model validated empirically: R²=0.9996, Gloo adds **54× latency overhead** vs hardware

---

### 📄 [paged-attention-sim](https://github.com/JohnScheuer/paged-attention-sim)

> *How does vLLM eliminate memory fragmentation?*

Discrete-event simulator of the PagedAttention memory management system
(Kwon et al., SOSP 2023). Implements physical block manager, logical block
tables, copy-on-write prefix cache, and two schedulers from scratch.
Validates all five core claims of the vLLM paper with measurable results.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · fragmentation analysis · block size sweep · prefix sharing |

**Key findings:**
- Contiguous allocation wastes **60.8% of KV cache memory** — confirmed vLLM paper claim
- PagedAttention delivers **+154.9% effective capacity** with 0% external fragmentation
- Prefix sharing (CoW): **+76% throughput** at 100% sharing ratio — 76 extra sequences served
- Block size tradeoff: optimal=8 tokens, vLLM uses 16 (score diff=0.015) for CUDA alignment
- Memory budget gain: **+287% throughput** from 4K to 64K token budget
- All 5 vLLM paper claims reproduced and quantified ✓

---

### 🗜️ [kv-cache-quantization-bench](https://github.com/JohnScheuer/kv-cache-quantization-bench)

> *How much KV cache memory can you recover without discarding tokens?*

Benchmark of five KV cache quantization schemes (FP16, INT8-sym, INT8-per-token,
INT4-per-token, FP8-e4m3) applied via runtime hooks on GPT-2 and GPT-2-medium,
with perplexity, memory, and latency measurement across sequence lengths and layers.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · Pandas · Matplotlib |
| Method | DynamicCache hooks · prefix-continuation split · per-layer sensitivity · Pareto frontier |
| Hardware | CPU (WSL) |

**Key findings:**
- INT8-per-token delivers **50% memory reduction** with ppl_delta < 0.04 — effectively free compression
- INT4-per-token achieves **75% reduction** at bounded quality cost (+0.12 to +0.15 ppl_delta over INT8)
- Quantization error concentrates in **later layers** — early layers tolerate INT4 with near-zero impact
- Mixed-precision policy (INT4 early, INT8 late) could recover most of 75% reduction at INT8 quality
- On CPU, quantization value is **capacity, not speed** — identical conclusion to weight quantization

---

### 🔀 [disaggregated-prefill-decode-sim](https://github.com/JohnScheuer/disaggregated-prefill-decode-sim)

> *What if prefill and decode ran on separate nodes?*

Discrete-event simulator comparing coupled vs. disaggregated LLM serving across
540 configurations — 3 models, 4 interconnects, 5 arrival rates, 3 prompt lengths,
3 output lengths. Models prefill micro-batching, decode contention, GQA-aware KV
cache sizing, transfer overlap, GPU memory limits, and drop behavior under saturation.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · Poisson arrivals · Pareto frontier · saturation analysis |

**Key findings:**
- Mean throughput gain: **10.76x** — median **8.26x**, max **32.37x**
- Mean TTFT speedup: **312.62x** — median **173.73x**, max **1428.11x**
- Mean transfer overhead: **0.16% of E2E latency** — transfer cost is negligible
- Mean transfer latency: **3.96 ms** — PCIe 3.0 already sufficient in most regimes
- Gains driven by **eliminating queueing**, not by bandwidth — 70B benefits most
- Coupled baseline collapses under load: long decode blocks all subsequent prefills

---

### ⚡ [cuda-graph-decode-profiler](https://github.com/JohnScheuer/cuda-graph-decode-profiler)

> *How much decode latency comes from kernel launch overhead — and what eliminates it?*

Profiler comparing four decode execution modes (eager dynamic, eager static,
torch.compile, CUDA Graph) on GPT-2 and GPT-2-medium on RTX 2070. Measures
per-token latency, speedup vs baseline, batch-size crossover, and sequence-length
sensitivity to isolate kernel launch and runtime dispatch overhead.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · CUDA 13.0 |
| Method | Per-token timing · warmup · CUDA Graph capture · torch.compile · StaticCache |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- torch.compile: **3.31x** mean speedup (GPT-2), **2.65x** (GPT-2-medium) over eager dynamic
- CUDA Graph: **2.53x** mean speedup (GPT-2), **2.18x** (GPT-2-medium) over eager dynamic
- On RTX 2070 + PyTorch 2.13, **torch.compile outperforms CUDA Graph alone**
- StaticCache is **slower** than DynamicCache in eager mode — speedup only materializes with graph capture
- Graph benefit is largest at **small batch sizes** — shrinks as compute dominates launch overhead
- Production systems (vLLM, TensorRT-LLM, SGLang) use compile + graph together — neither alone is sufficient

---

### 🌳 [tree-speculative-decoding](https://github.com/JohnScheuer/tree-speculative-decoding)

> *Given the same verification budget, does a tree accept more tokens than a linear chain?*

From-scratch implementation and benchmark of tree-based speculative decoding
(SpecInfer-style) vs. linear speculative decoding under a fair equal-node-budget
comparison. Implements custom tree attention masks, best-first tree expansion,
and a full sweep over branch factor, depth, budget, and draft quality.

| | |
|---|---|
| Stack | Python · PyTorch |
| Method | Tree attention mask · equal-budget sweep · node efficiency analysis |

**Key findings:**
- Mean accepted tokens per target call: tree **0.317** vs linear **0.120**
- Mean tree vs linear speedup: **6.97x** — median **4.16x**, max at bf=8: **13.47x**
- Mean node efficiency ratio: **5.81x** — tree extracts 5.8x more accepted tokens per verified node
- **Branch factor dominates** under fixed budget — wider+shallower consistently beats narrow+deep
- Depth shows **diminishing returns** — budget better spent on breadth than depth
- At draft quality=0.9, tree and linear **converge** — tree solves a specific failure mode, not a general one
- Tree advantage largest when draft is unreliable: quality=0.3 → **14.22x speedup**

---

### 🔬 [speculative-decoding-real](https://github.com/JohnScheuer/speculative-decoding-real)

> *Speculative decoding failed on my GPU. Here's exactly why.*

Three-phase empirical study of speculative decoding using Qwen2-0.5B (draft)
and Qwen2-1.5B (target) on a single RTX 2070. Measures acceptance rate,
wall-clock speedup, per-phase time breakdown, and validates the Leviathan et al.
(2023) analytical model.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | 3-phase benchmark · time breakdown · alpha dynamics · corrected analytical model |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Speedup **< 1.0 for all 32 configurations** — speculative decoding failed on single GPU
- cost_ratio = **1.18x measured** vs 3.1x expected from parameter count — memory bandwidth equalization
- KV sync overhead = **31.8% of step time** at gamma=1 — not in the analytical model
- Temperature kills alpha: greedy=**0.767**, T=1.0=**0.083** — sampling is incompatible
- gamma=8 has **highest alpha (0.750)** but lowest speedup — draft "in flow" effect
- Analytical model correctly predicted failure: **zero false positives**
- At cost_ratio=4.0 (7B target): simulated mean speedup **1.24x** — viable with right hardware

---

### 🏗️ [inference-pipeline-e2e](https://github.com/JohnScheuer/inference-pipeline-e2e)

> *The capstone: a complete LLM serving pipeline with streaming and per-phase metrics.*

End-to-end inference server with tokenize → prefill → decode → detokenize,
SSE streaming, and async load testing.

| | |
|---|---|
| Stack | Python · PyTorch · FastAPI · SSE · httpx |
| Method | Per-phase timing · streaming output · concurrent load testing |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Tokenization + detokenization = **<0.2%** of total pipeline
- Streaming reduces TTFT from **89ms → 32ms** (2.8× faster first token)
- Decode throughput stays at **~41 tok/s** regardless of concurrency
- TTFT degrades under concurrent streaming without batching

---

### 📏 [long-context-benchmark](https://github.com/JohnScheuer/long-context-benchmark)

> *How far can you push context on a consumer GPU?*

Long-context benchmark reaching 32K tokens on RTX 2070 by stacking SDPA + chunked prefill,
with FP16 vs INT4 comparison.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · bitsandbytes |
| Method | Chunked prefill · SDPA · INT4 · capacity mapping |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- FP16 + SDPA reaches **32K context** at 12.6 tok/s (was OOM before)
- **40× speedup** at 8K vs vanilla attention
- INT4 **OOMs at 32K** — KV-cache is the real bottleneck, not model weights
- Quantization is NOT a long-context solution

---

### 🔌 [multi-lora-serving-sim](https://github.com/JohnScheuer/multi-lora-serving-sim)

> *How do you serve 50 LoRA adapters simultaneously without exhausting VRAM?*

Discrete-event simulator comparing three multi-LoRA scheduling strategies
(naive swap, hot-set preloading, batch-by-adapter) under variable VRAM pressure,
arrival rates, and adapter popularity distributions. Models CPU-to-GPU swap cost,
adapter cache eviction, and batch window effects.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · Poisson arrivals · Zipf distribution · VRAM pressure sweep |

**Key findings:**
- Swap overhead = **29.3% of TTFT** in naive serving at high VRAM pressure
- Batch-swap reduces TTFT by **20%** and swap rate by **64%** vs naive at 64 req/s
- Hot-set wins only at **low arrival rates** with skewed distributions (Zipf, arr=4)
- Strategy crossover at **~10–16 req/s** — below: preloading wins; above: batching wins
- TTFT is **output-length invariant** — swap happens before first token regardless of decode length
- Batch window has **diminishing returns beyond 25ms** — gain comes from density, not window width
- Naive swap never dominates both alternatives simultaneously across any high-pressure scenario

---

### 🧩 [moe-inference-sim](https://github.com/JohnScheuer/moe-inference-sim)

> *How much GPU capacity does vanilla MoE routing waste?*

MoE inference simulator with routing, load balancing, expert parallelism,
and memory analysis across 360+ configurations.

| | |
|---|---|
| Stack | Python · PyTorch |
| Method | Discrete simulation · load balance · expert parallelism |

**Key findings:**
- Vanilla routing on 8 shards: **19.3% efficiency** (81% waste)
- Penalty routing on 8 shards: **99.4% efficiency**
- Load imbalance drops from **56.89× → 1.01×** with penalty routing
- Token dropping eliminated from **76% → 0%** with penalty strategy

---

### 🔄 [rope-vs-absolute-pe-benchmark](https://github.com/JohnScheuer/rope-vs-absolute-pe-benchmark)

> *How does positional encoding affect attention sinks and KV-cache eviction?*

Compares GPT-2-medium (absolute PE) vs Qwen2-0.5B (RoPE) across attention patterns,
eviction tolerance, perplexity, and throughput.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Attention extraction · eviction simulation · perplexity scaling |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Absolute PE produces **37% stronger attention sinks** than RoPE
- RoPE tolerates KV-cache eviction **~25% better**
- Both PE types need sink-preserving policies for extreme compression
- Perplexity scaling is similar between PE types

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

### 🧭 [guided-decoding-bench](https://github.com/JohnScheuer/guided-decoding-bench)

> *How much does enforcing JSON/schema cost per decode token?*

Benchmark isolating the per-token overhead of constrained decoding for structured
output generation. Compares free decoding, token healing, and FSM guided decoding
across schema types, string lengths, and oracle confidence levels. Breaks down FSM
step cost into model logits, mask build, mask apply, and state update components.

| | |
|---|---|
| Stack | Python · PyTorch |
| Method | Per-token timing · FSM component breakdown · valid JSON rate · cold vs warm build |

**Key findings:**
- Token healing: **0.99x** overhead — effectively free, but cannot enforce online validity
- FSM guided decoding: **1.96x** per-token slowdown — consistent across all configurations
- Mask build + mask apply = **84.2%** of FSM step time — grammar state update = **0.2%**
- Overhead is **structural, not model-dependent** — changing confidence does not change slowdown
- Valid JSON rate: free **93.3%**, healing **92.9%**, FSM **78.4%** — syntactic constraint ≠ semantic validity
- Cold FSM build: **33.0 ms** — warm build: **22.0 ms** — warm cost is the operationally relevant number
- Optimization target for guided decoding serving: **mask construction**, not grammar or model

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

### 🎲 [sampling-strategy-bench](https://github.com/JohnScheuer/sampling-strategy-bench)

> *How much does sampling strategy cost in latency — and what does each buy in quality?*

Latency and quality benchmark for five autoregressive decoding strategies (greedy,
top-k, top-p, min-p, beam search) on GPT-2 and GPT-2-medium on RTX 2070. Measures
ms/token overhead, type-token ratio, perplexity, and repetition rate. Identifies
the Pareto frontier across latency, diversity, and quality axes.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Per-token timing · TTR · perplexity · repetition rate · Pareto frontier |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Stochastic sampling (top-k, top-p, min-p) adds only **3–13% latency** over greedy — strategy choice should be driven by quality, not cost
- Greedy decoding degenerates at long outputs: **RepRate=0.430** — 43% of trigrams repeat
- top_p(0.95) reduces RepRate from 0.430 to **0.010** at only **1.06x** overhead — best for open-ended generation
- min_p achieves **better PPL than top-k** at similar diversity — adapts vocabulary size to model confidence dynamically
- Beam search is **Pareto-dominated** on all axes — slower, less diverse, more repetitive than nucleus sampling
- Pareto frontier: **greedy → top_k(k=10) → top_p(0.95)** — beam search lies strictly inside

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

    +--------------------------------------------------------------------------+
    |            LLM Inference Server (simulated)                              |
    +-------+--------+----------+-------+--------+-------+---------+----------+
    |Schedul|Prefix  |KV        |Paged  |KV      |Disagg.|Multi    |Request   |
    |er     |Cache   |Compact.  |Mem    |Quant.  |Serving|LoRA     |Routing   |
    |llm-   |prefix- |kv-cache- |paged- |kv-cache|disagg-|multi-   |request-  |
    |infer  |cache   |compact   |attn   |quant   |prefill|lora-sim |routing   |
    +-------+--------+----------+-------+--------+-------+---------+----------+
     "what   "what    "how to    "how to "how to  "split  "adapter  "which
      to run" to reuse" defrag"   alloc"  compress" phases" sched"   instance"

    +----------------------------------------------------------+
    |          Hardware & Scaling Layer                        |
    +-------------+---------------+----------+---------------+
    |  Parallelism |  Context Len  | Attention| Kernel Launch |
    |              |               |          |               |
    |  comm-cost-  |  long-context-| flash-   | cuda-graph-   |
    |  modeling    |  benchmark    | attention | decode-prof   |
    +-------------+---------------+----------+---------------+
      "how to scale" "how far to    "which     "eliminate
                      push"          kernel"    overhead"

    +------------------------------------------------------------------+
    |          Decoding & Generation Layer                             |
    +---------+---------+---------+---------+-----------+------------+
    |Specul.  |Tree     |Quantiz. |Long Ctx |Guided     |Sampling    |
    |(linear) |Spec.    |         |         |Decoding   |Strategy    |
    |specul-  |tree-    |quantiz- |long-ctx-|guided-    |sampling-   |
    |decoding |spec-dec |profiler |benchmark|decode-bench|strat-bench|
    +---------+---------+---------+---------+-----------+------------+
      "when it  "more     "precision "how far  "constraint "which
       helps"    per step"  vs speed"  to push"  cost"       sampler"

    +----------------------------------------------------------+
    |          Analysis & Visualization (across all)           |
    |                                                          |
    |  inference-dashboard  +  attention-sink-profiler         |
    |  (interactive plots)     (attention mechanics)           |
    +----------------------------------------------------------+

Each project is independent and fully reproducible.
Together they cover the full lifecycle of a request in an LLM server:
from scheduling and caching to memory allocation, compression, multi-adapter
serving, disaggregated execution, and multi-instance request routing, parallelism
modeling, kernel-level execution optimization, hardware limits, and decoding
optimization — including linear and tree-based speculative decoding, constrained
structured output generation, and sampling strategy benchmarking.

---

## Tech Stack

| Area | Tools |
|---|---|
| Core simulation | C++20, STL, CMake, Ninja |
| Deep learning | PyTorch, Transformers, CUDA |
| Distributed modeling | Alpha-beta comm model, TP/PP/Hybrid simulation, regime detection |
| Analysis & plots | Python, pandas, numpy, matplotlib, Plotly |
| Dashboard | Streamlit, Plotly |
| Research output | Pareto frontier, regime classification, cost efficiency, P99 tail latency |
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
