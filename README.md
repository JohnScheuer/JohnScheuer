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

> 55 projects covering the full LLM inference stack —
> from memory management and scheduling to distributed parallelism,
> speculative decoding, and long-context serving.

---

### 🧩 [continuous-batching-fragmentation-sim](https://github.com/JohnScheuer/continuous-batching-fragmentation-sim)

> *How does KV cache fragmentation accumulate over time in a running continuous batching server?*

Discrete-event simulation measuring fragmentation growth, compaction policy
effectiveness, and allocation strategy tradeoffs across workload intensities and
request size distributions. Closes a loop with kv-cache-compaction-lab,
paged-attention-sim, and kv-cache-tiering-bench.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · fragmentation timeseries · compaction efficiency · Pareto frontier |

**Key findings:**
- Fragmentation without compaction reaches **44–52%** under heavy workloads in 60 minutes
- Paged allocation wins for **uniform** workloads — loses for **bimodal** (internal frag blocks long requests)
- paged_16kb rejects **400+ more** requests than contiguous_adaptive_q8 under heavy_mixed load
- Adaptive compaction: **718 compactions** vs greedy **2422** — 3.4x fewer, fewer rejections
- Greedy compaction under bimodal load is **worse than no compaction** — serializes the server
- Compaction pause time = **max 1.6% of server time** — cost is fragmented state, not pause itself
- **No universal optimal policy** — selection requires knowing the workload size distribution

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

### 💾 [system-prompt-cache-bench](https://github.com/JohnScheuer/system-prompt-cache-bench)

> *How much does caching the system prompt KV state save — and when does the cache stop paying off?*

Simulation measuring system prompt KV cache reuse across 540 configurations —
5 system prompt sizes, 5 user prompt sizes, 3 output lengths, 4 arrival rates,
2 cache budgets, 3 competing prompt counts, 2 popularity distributions.
Derives closed-form savings ratio and validates against simulation.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · LRU/LFU eviction · savings ratio derivation · budget sweep |

**Key findings:**
- Prefill savings follow a closed-form ratio: **savings = sys_len / (sys_len + user_len)**
- System prompt caching reduces prefill work by up to **99%** when system prompt dominates
- Final TTFT gain (~13%) is smaller than prefill savings (~35%) — decode and queuing unaffected
- Cache most valuable in short-output workloads: output=8 tokens → **17.7% TTFT reduction**
- At output=128 tokens, prefill share falls to 72.8% and TTFT reduction drops to **12.6%**
- LFU marginally better than LRU under skewed workloads — **cache sizing matters more than policy**
- Cache collapses when too many prompts compete for budget — size by **hot working set**, not total count

---

### 💬 [multi-turn-kv-reuse-bench](https://github.com/JohnScheuer/multi-turn-kv-reuse-bench)

> *How does KV cache reuse evolve across turns — and which routing strategy captures it?*

Simulation measuring KV cache reuse evolution across conversation turns under five
routing strategies (random, least_load, sticky_session, hybrid_sticky, cost_aware)
using real ShareGPT conversation traces. Quantifies the compound cost of routing
misses and the tradeoff between cache locality and load balance.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib · ShareGPT V3 |
| Method | Turn-level simulation · per-turn reuse tracking · Pareto frontier · cost-aware sweep |

**Key findings:**
- Sticky reaches **0.875 reuse by turn 1** — least-load reaches only 0.620 by turn 7
- hybrid_5000ms: best mean TTFT (**4602ms**) — retains 70% of sticky hit rate at 14% better latency
- cost_aware_a0.25: best p99 TTFT (**15987ms**) — per-request tradeoff beats fixed policies on tail
- Sticky: 0.771 hit rate but **p99 33% worse** than least-load — queue concentration negates cache benefit
- Routing misses **compound over turns** — a miss at turn 2 permanently destroys accumulated locality
- Routing is a **multi-objective problem** — no single strategy dominates all metrics simultaneously
- Reuse benefit is **front-loaded**: largest relative gain at turn 1, diminishing returns beyond turn 5

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

### 🧊 [model-cold-start-bench](https://github.com/JohnScheuer/model-cold-start-bench)

> *Where does startup delay actually come from — and what eliminates it?*

Benchmark measuring each phase of LLM instance cold start separately (weight
loading, PCIe transfer, CUDA init, KV cache allocation, warmup forward pass)
on RTX 2070. Closes the loop with slo-aware-autoscaling-sim by grounding
startup_delay parameters in real measurements.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Per-phase timing · pre-warming savings · model size extrapolation |
| Hardware | NVIDIA RTX 2070 (8.6 GB) · PCIe ~3.1 GB/s effective |

**Key findings:**
- Weight loading from disk = **74–78%** of cold start — storage, not compute, is the bottleneck
- PCIe transfer is **fastest-growing phase** with model size — 36% at 774M, major fraction at 7B+
- CUDA init + KV alloc + JIT = **under 10% combined** — not the bottleneck
- Pre-warming weights on GPU eliminates **92–98%** of cold start (551–1337ms → 15–45ms)
- Cold start multiplier: **68x** warmed TTFT for GPT-2 — 400x+ at 7B scale
- Extrapolated cold start: 7B=**~20s**, 13B=**~37s**, 70B=**~200s** without warm pool
- Autoscaling startup delays now grounded: 5s=GPU warm, 15s=CPU RAM, 30s=7B disk, 60s=13B disk

---

### 📈 [slo-aware-autoscaling-sim](https://github.com/JohnScheuer/slo-aware-autoscaling-sim)

> *How many instances do you need to guarantee p99 TTFT under 500ms?*

Discrete-event simulator comparing four autoscaling policies (reactive,
predictive_headroom, conservative, fixed) across five workload patterns and
four instance startup delays. Measures SLO violation rate, p99 TTFT, mean
instance count, and cost-compliance tradeoff.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · Poisson + burst workloads · startup delay sweep |

**Key findings:**
- Startup delay is the **dominant factor** — same policy: SLO=0.050 at 5s vs 0.176 at 60s
- Conservative wins at **fast startup** (5–15s) — simple headroom absorbs bursts before queues build
- Predictive + headroom wins at **slow startup** (30–60s) — trend detection gives head start
- Reactive is **consistently worst** — responds after violations already occurred
- fixed_4 is **simultaneously more expensive and less compliant** than adaptive policies
- Pure prediction without headroom **fails** — explicit headroom required regardless of forecast quality
- Practical lesson: invest in **fast instance startup** before tuning autoscaling algorithms

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

### 🔭 [output-length-predictor-bench](https://github.com/JohnScheuer/output-length-predictor-bench)

> *How much does output length prediction quality affect KV-cache-aware scheduling?*

Benchmark measuring effective throughput under 7 predictors (oracle, noisy_10/30/50,
prompt_ratio, mean_only, none), 4 safety margins, 3 scheduling policies, and 4
arrival rates. Closes a three-part loop with sharegpt-workload-bench and
kv-cache-aware-scheduler.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Predictor sweep · safety margin sweep · effective throughput · preemption analysis |

**Key findings:**
- noisy_10 @ 1.5x margin achieves **99.7% of oracle gain** — calibration matters more than accuracy
- Optimal safety margin is **1.5x** across almost all predictors — asymmetry favors overestimation
- Greedy is **insensitive to prediction quality** — prediction only helps with admission-control scheduling
- none → mean_only: **+500x effective throughput** — biggest gain from any calibrated prediction at all
- mean_only → noisy_30: **+36%** — noisy_30 → oracle: **+2.3%** — returns are heavily front-loaded
- Raw prediction accuracy and **scheduling calibration are separate concerns**
- Engineering priority: build any calibrated predictor first — refinement yields diminishing returns

---

### 🧠 [kv-cache-aware-scheduler](https://github.com/JohnScheuer/kv-cache-aware-scheduler)

> *What happens when the scheduler uses KV cache pressure as a signal, not just queue depth?*

Simulator comparing three KV-cache-aware scheduling policies (greedy, admission
control, memory-first) under uniform, heavy-tail, and mixed workloads. Measures
raw vs effective throughput, preemption rate, rejection rate, and P99 TTFT to
find the Pareto-dominant policy under memory pressure.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · KV budget tracking · effective throughput analysis |

**Key findings:**
- Greedy raw throughput: **8.41** vs memory-first **6.06** — greedy looks 39% faster
- Greedy effective throughput: **3.46** vs memory-first **6.06** — greedy is **43% worse**
- Greedy wastes **59% of GPU compute** on preemptions under mixed workloads
- memory-first **Pareto-dominates**: lower rejection than admission_control, lower tail than greedy, zero preemptions
- Effective throughput is the **correct metric** under KV pressure — raw throughput is misleading
- Controlled rejection wastes **zero compute** — preemption wastes **all compute** done before eviction
- KV-aware scheduling only differentiates under **heterogeneous workloads** — uniform workloads converge

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

### ⚔️ [prefill-decode-interference-bench](https://github.com/JohnScheuer/prefill-decode-interference-bench)

> *How much does prefill inflate TTFT for new requests when decode is already running on the GPU?*

Real hardware benchmark measuring TTFT inflation and decode slowdown when prefill
and decode are co-located on the same GPU. Closes the loop on the disaggregated
serving simulation with actual RTX 2070 measurements across two models, three
prompt lengths, and two batch sizes.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Cold vs hot prefill timing · parallel CUDA stream measurement · wall overlap efficiency |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- TTFT inflation at prompt=512, 1.5B, batch=4: **4.96x** — new request waits **+420ms** before prefill starts
- TTFT inflation at prompt=512, 0.5B: **1.25–1.27x** — penalty **+12–14ms** consistently
- Decode slowdown: **0.95–1.07x** — decode nearly immune (memory-bound vs compute-bound)
- wall_overlap_efficiency: **~0.91–1.02x** — co-location is serial execution with TTFT inflation, not parallelism
- TTFT penalty **grows with prompt length** — longer prompts amplify the interference effect
- Larger models show **severely worse pollution** — 1.5B prompt=256: **1.74x** inflation vs 0.5B **1.19x**
- Grounds disaggregated-prefill-decode-sim: analytical 10.76x gain now backed by real interference data

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

### 🔢 [batched-speculative-decoding-bench](https://github.com/JohnScheuer/batched-speculative-decoding-bench)

> *Does speculative decoding maintain its gains at batch_size > 1 — and how does gamma interact with batch?*

Analytical benchmark for speculative decoding across 7 batch sizes, 7 gammas,
4 quality modes, and 2 serving modes. Measures speedup, acceptance rate, optimal
gamma, and crossover point where speculation becomes slower than greedy. Closes
the speculative decoding series.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Analytical model · gamma sweep · quality mode sweep · continuous refill simulation |

**Key findings:**
- Speculative decoding scales to batch=64 **with no degradation** — 2.03x at bs=1, 2.09x at bs=64
- **Gamma is the critical tuning knob**, not batch size — optimal gamma depends on draft quality only
- Over-speculating at q~0.65: gamma=12 → **15% slower** than greedy, gamma=16 → **31% slower**
- Crossover point: **gamma~10** for medium-quality drafts — regression risk beyond this
- Batch heterogeneity **caps speedup at ~1.5x** regardless of gamma — weakest request limits the batch
- **gamma=2 is the safe default** for unknown draft quality — 1.37–1.50x across all modes, no regression
- gamma=4 optimal **only when draft quality is confirmed high** (q~0.85)

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

### 🎯 [draft-model-selection-bench](https://github.com/JohnScheuer/draft-model-selection-bench)

> *Given a fixed target model, which draft model maximizes speculative decoding speedup?*

Systematic benchmark for draft model selection — measuring tokenizer compatibility,
cost ratio, acceptance rate, and predicted speedup for every candidate draft against
Qwen2-1.5B as target. Closes a five-project speculative decoding arc.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · BitsAndBytes |
| Method | Compatibility audit · cost ratio sweep · acceptance simulation · analytical speedup model |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Cross-family drafts (GPT-2, TinyLlama) fail **all 4 compatibility checks** — tokenizer, vocab, specials, encoding
- int4 quantization makes draft **slower**, not faster — BitsAndBytes dequantization overhead at bs=1
- GPT-2 fp16 would give cost_ratio=**4.62x** — but incompatible; compatibility constrains the search space
- Qwen2-0.5B fp16: cost_ratio=**1.22x** — all predicted speedups **below 1.0x** on RTX 2070
- **Alpha trap**: Qwen2-1.5B int4 achieves alpha=0.875 but speedup=0.35–0.57x — acceptance is not enough
- **Compatibility trap**: viable drafts must share tokenizer with target — same family, rarely 3x cheaper
- Speculative decoding on consumer GPU requires **3x+ cost ratio** — conditions more restrictive than literature suggests

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

### 📊 [sharegpt-workload-bench](https://github.com/JohnScheuer/sharegpt-workload-bench)

> *How does serving behavior change under real conversation traces vs synthetic Poisson workloads?*

Benchmark replaying 9562 real ShareGPT conversation turns through a discrete-event
serving simulator, comparing TTFT, SLO compliance, and scheduling policy effectiveness
against mean-matched and median-matched Poisson workloads. Validates workload
assumptions used across the portfolio.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Trace replay · Poisson comparison · scheduling policy sweep · SLO crossover analysis |

**Key findings:**
- Real prompt distribution: median=22, p99=1872 — **85x difference** — no synthetic param captures this
- ShareGPT P99 TTFT at low load: **212ms** vs 22ms (mean-matched) vs 5ms (median-matched)
- ShareGPT is **9.6x worse** than mean-matched Poisson — **42x worse** than median-matched
- SLO violations appear **one arrival-rate step earlier** under real traces vs synthetic
- Under Poisson: all scheduling policies **identical** — under ShareGPT: shortest-first **-29% SLO violations**
- All prior portfolio simulation results are **conservative estimates** of real-traffic behavior
- Synthetic benchmarks make scheduling look irrelevant — real distributions reveal the difference

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
- Interactive charts — no installation required

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

### 🌀 [rope-scaling-bench](https://github.com/JohnScheuer/rope-scaling-bench)

> *How far can you extend context beyond training — and which RoPE scaling method degrades least?*

Benchmark measuring perplexity degradation for three RoPE scaling methods
(linear, NTK-aware, YaRN) at 2x/4x/8x extension on TinyLlama-1.1B
(training context=2048, evaluated to 8192). Closes a three-part long-context
series with rope-vs-absolute-pe-benchmark and long-context-benchmark.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Sliding-window perplexity · absolute position_ids · extension ratio sweep |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- NTK-aware scaling: PPL **flat from 2048 to 8192** (4.627 → 4.628) — 4x extension at zero quality cost
- Linear scaling **fails inside training window**: linear_4x PPL=**187.7** at 2048 tokens — model is broken
- YaRN competitive but below NTK: yarn_4x baseline PPL=**5.737** vs NTK=**4.620**
- NTK wins at every tested extension ratio (1.5x, 2x, 3x, 4x)
- Tradeoff is **entirely about quality, not latency** — RoPE scaling adds negligible compute
- Linear interpolation distorts **high-frequency components** — fine-grained local position collapses

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

### ✂️ [prompt-compression-bench](https://github.com/JohnScheuer/prompt-compression-bench)

> *How much can you compress the prompt before prefill — and what does it cost in quality?*

Benchmark comparing four prompt compression strategies (attention_oracle, lexical,
stride, random) across two models, three prompt lengths, and five keep fractions.
Measures prefill speedup, KL divergence, delta-NLL, and top-1 agreement. Closes
a triangle with attention-sparsity-bench and kv-cache-eviction-benchmark.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Per-strategy timing · KL divergence · delta-NLL · top-1 agreement · tradeoff frontier |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- keep=0.25 at prompt_len=512: GPT-2 **3.03x** speedup — GPT-2-medium **4.04x** speedup
- Lexical heuristics **outperform attention oracle** on GPT-2-medium at long prompts
- GPT-2-medium, keep=0.75: lexical KL=**0.090** vs attention_oracle KL=**0.117**
- Attention mass is a **noisier signal in larger models** — not a reliable compression criterion
- Lexical compression requires **zero forward pass** — deployable with no GPU cost
- Attention oracle requires full prefill to score tokens — **net-negative for single requests**
- Protected positions (first 4, last 16 tokens) essential — removing them collapses quality

---

### 🎛️ [mixed-precision-kv-policy](https://github.com/JohnScheuer/mixed-precision-kv-policy)

> *INT8 on early layers + INT4 on late layers — how much KV budget recovered at near-INT8 quality?*

Layer-aware mixed-precision KV cache quantization benchmark. Tests 9 INT8/INT4
split policies on GPT-2 to find the Pareto-optimal point between uniform INT8
(50% reduction) and uniform INT4 (75% reduction, high quality cost). Closes a
triangle with attention-sparsity-bench and kv-cache-quantization-bench.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Per-layer KV hook · delta-NLL · mean-KL · top-1 agreement · Pareto frontier |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- int8_first10_int4_last2: **54% reduction** at delta_nll=**0.016** vs uniform INT4 delta_nll=**0.917**
- Ablation confirms: INT4 early + INT8 late is **12x worse** than INT8 early + INT4 late at same ratio
- Early layer sensitivity from attention-sparsity-bench **transfers directly to quantization**
- INT4 collapses at long prompts: prompt=512 → uniform INT4 delta_nll=**1.696**, mixed=**0.007**
- Practical operating point: **int8_first10_int4_last2** — 4% extra vs INT8, near-zero quality cost
- Split point is **not a hyperparameter search** — layer KL profile determines it analytically
- For 7B models, 4% extra reduction = **hundreds of MB** of KV budget recovered

---

### 🔬 [attention-sparsity-bench](https://github.com/JohnScheuer/attention-sparsity-bench)

> *How sparse is the attention matrix — and is that sparsity safe to exploit via token eviction?*

Systematic measurement of structural attention sparsity in GPT-2 and GPT-2-medium
across layers, heads, sequence lengths, and text domains. Introduces KL divergence
as the ground-truth eviction safety metric — separating retained weight fraction
(optimistic) from distribution distortion (real). Produces head-structured eviction
recommendations per pattern type and layer depth.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Attention extraction · sparsity CV · Jaccard overlap · KL divergence · head pattern classification |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- **99.5%** of attention entries below 0.05 at seq=512 — architectural limit, not capacity-dependent
- Sparsity CV across 4 text domains: **0.013%** — Jaccard overlap: **98.6%** — structural, not content-driven
- keep=20% retains **95.6%** attention weight but KL=**0.72** — distribution is materially distorted
- Safe operating point: **keep=50%** where KL drops to **0.11**
- global heads (7% of total): KL=**3.84** at keep=20% — concentrate nearly all eviction risk
- local heads (46% of total): KL=**0.29** at keep=20% — eviction nearly free
- Early layers **2x riskier** than late layers — all top-5 riskiest heads in layers 0–1
- Head-structured policy: **40–60% KV reduction** with near-zero distortion vs 80% uniform at KL=0.72

---

### ⚡ [flash-decoding-bench](https://github.com/JohnScheuer/flash-decoding-bench)

> *Flash Decoding vs SDPA at decode time — when does KV-parallelism pay off?*

Benchmark comparing standard SDPA against Flash-Decoding-style chunked attention
(sequential and parallel CUDA streams) at the decode step (q_len=1). Measures
crossover point, chunk size sensitivity, and batch size effect. Closes a pair
with flash-attention-benchmark — prefill vs decode attention regimes.

| | |
|---|---|
| Stack | Python · PyTorch · CUDA |
| Method | Per-kernel timing · KV length sweep · chunk size sweep · stream parallelism |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- SDPA wins at **short KV lengths** — fused kernel dominates, chunk overhead not justified
- Parallel chunked decode wins above **~8K KV tokens** — 1.38x speedup vs SDPA at kv=8192, bs=1
- Sequential chunked only reaches **1.13x at kv=16384** — Python loop overhead limits gains
- Batch size 4 shows **no benefit** from chunked decode — SDPA already utilizes GPU well
- Measured gains are a **lower bound** — fused CUDA kernel moves crossover to shorter KV
- Flash Decoding is a **kernel engineering problem**, not just an algorithmic idea
- Production crossover (FlashInfer, vLLM, SGLang): **kv~1024** vs Python impl **kv~8192**

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

### 🧩 [chunked-prefill-kv-sim](https://github.com/JohnScheuer/chunked-prefill-kv-sim)

> *What happens when chunked prefill meets KV cache pressure in continuous batching?*

Step-level simulator measuring the interaction between chunked prefill and KV cache
pressure under four policies (no_chunk, reserve, block, steal). Measures chunk waste
rate — GPU compute discarded on blocked prefills — as the critical metric hidden by
standard throughput reporting. Closes a loop with prefill-chunking-profiler and
kv-cache-aware-scheduler.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Step-level simulation · chunk waste tracking · block/retry analysis · KV budget sweep |

**Key findings:**
- no_chunk **strictly dominates** block: same effective throughput, **0% vs 89.6%** chunk waste
- block_rate=**1.539** — requests retry 1.5x on average, discarding all prior chunks each time
- chunk_waste_rate is the **critical hidden metric** — standard metrics miss partial prefill waste
- steal is **catastrophic**: 73.1% chunk waste + 20.1% preemption — creates destructive retry cycle
- Upfront rejection wastes **zero compute** — mid-prefill blocking wastes **all prior chunk compute**
- Chunked prefill under KV pressure requires **full KV reservation before first chunk** or projected footprint admission
- Naive incremental allocation wastes GPU compute with **no throughput benefit**

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

### 📦 [kv-cache-prefetch-bench](https://github.com/JohnScheuer/kv-cache-prefetch-bench)

> *Can speculative prefetching eliminate the CPU-to-GPU KV reload stall in multi-turn conversations?*

Simulation of speculative KV cache prefetching across six policies (reactive,
next_turn, confidence_05/07, utility_005/010) under variable workloads and
model sizes. Measures stall reduction, hit rate, and wasted prefetches.
Closes a loop with kv-cache-tiering-bench and multi-turn-kv-reuse-bench.

| | |
|---|---|
| Stack | Python · NumPy · Pandas · Matplotlib |
| Method | Discrete-event simulation · per-turn event log · hit/waste tradeoff · stall reduction |

**Key findings:**
- next_turn prefetch reduces stall by **73x** (0.5B) and **11x** (1.5B) vs reactive baseline
- confidence_05 captures **82-88%** of stall reduction with **~40% less** wasted prefetches
- Utility scoring (p_reuse/size_mb) **fails on large models** — size penalty collapses hit rate to 26.9%
- Bimodal workloads **amplify prefetch benefit** — heavy_mixed stall 4.847ms → 0.426ms
- confidence_05 is the **best practical policy**: p(next_turn) >= 0.50 threshold, robust across model sizes
- Size normalization must use **reload_cost in numerator**, not raw MB in denominator
- Prefetch buffer design: **confidence threshold as gate**, size as tiebreaker for capacity limits

---

### 🗄️ [kv-cache-tiering-bench](https://github.com/JohnScheuer/kv-cache-tiering-bench)

> *Where does evicted KV cache go — and when does reloading from a tier beat recomputing?*

Benchmark measuring spill and reload cost for six KV cache tiers (CPU fp16 pinned
pool, CPU fp16 unpinned, CPU fp16 pinned, CPU int8, disk fp16, disk int8) across
two models and three prompt lengths. Computes breakeven reuse probability and
optimal tier policy. Connects four prior KV cache projects.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers · safetensors |
| Method | Per-tier timing · bandwidth measurement · breakeven analysis · pool amortization |
| Hardware | NVIDIA RTX 2070 (8.6 GB) · PCIe ~3.1 GB/s measured |

**Key findings:**
- CPU fp16 pinned pool: reload=**2.96ms** vs prefill=**251ms** at prompt=1024 — **85x faster**
- Pool amortizes at **1 reuse** — alloc=0.09ms, saved_per_reuse=5.40ms
- Optimal policy is **binary**: p_reuse < 0.02 → discard, p_reuse >= 0.02 → cpu_fp16_pinned_pool
- Disk tiering **fails after fsync**: 129–226ms reload at prompt=1024 — threshold exceeds 1.0
- cpu_int8 is **5–6x slower** than cpu_fp16_pinned_pool — INT8 halves size but 5x hurts reload
- Reuse threshold: **1–2%** — any workload with repeated prompts benefits from CPU tiering
- No other tier appears in the **optimal policy** at any reuse probability

---

### 🎯 [attention-sink-eviction-policy](https://github.com/JohnScheuer/attention-sink-eviction-policy)

> *Head-structured KV eviction from per-head KL profiles -- does it beat uniform eviction at matched compression?*

Builds and validates head-structured KV cache eviction policies using per-head
KL divergence profiles from attention-sparsity-bench. Tests the claim that
structured masks achieve 40-60% KV reduction with near-zero distortion.
Closes a four-part arc with attention-sparsity-bench, kv-cache-eviction-benchmark,
and mixed-precision-kv-policy.

| | |
|---|---|
| Stack | Python - PyTorch - Transformers |
| Method | Per-head keep_frac assignment - KL bucket mapping - Pareto frontier - budget-matched comparison |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- kl_conservative: **57% reduction** at KL=0.032 vs uniform_50: 50% reduction at KL=0.113 -- **3.5x better**
- kl_moderate at keep=42%: **4.2x lower KL** than budget-matched uniform eviction
- Pattern-based labels **worse than KL scores** -- pattern_structured KL=0.290 vs kl_structured KL=0.098 at same ratio
- Structured advantage **largest at short prompts**: KL gain +0.120 at 128 tokens, +0.045 at 512 tokens
- Profile computed **once, applied universally** -- Jaccard 98.6% means same mask works across all domains
- Continuous KL score contains **more information than discrete pattern label** -- use KL for assignment
- Claim from attention-sparsity-bench **validated**: 40-60% reduction with near-zero distortion achievable

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

### 🛑 [token-budget-controller](https://github.com/JohnScheuer/token-budget-controller)

> *Can chain-of-thought generation be stopped early without hurting accuracy — and how much is actually saved?*

Benchmark testing runtime plateau detection for CoT generation across three
detector families (strict_confidence, loose_entropy, answer_terminator) with
oracle analysis to measure the real savings ceiling. Corrects the inference from
inference-time-scaling-bench about the magnitude of wasted reasoning compute.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | Token-by-token trace collection · oracle stop analysis · detector sweep · false positive rate |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- Oracle savings ceiling: **18–27 tokens** — not 200+ as fixed-budget analysis implied
- Loose entropy detector: accuracy **6.25%**, false positive **65.6%** — destroys correctness
- strict_confidence: accuracy **71.9%**, saved **8.78 tokens**, oracle capture **48.0%**
- answer_terminator_4: accuracy **71.9%**, saved **8.63 tokens**, zero false positives
- Strict prompt forcing answer format: accuracy collapses to **6–9%** — not a substitute
- Problem is **not detecting end of reasoning** — it is trimming tail after answer stabilizes
- **Answer-aware tail trimming** is the only practical direction — generic plateau signals too noisy

---

### 🧮 [inference-time-scaling-bench](https://github.com/JohnScheuer/inference-time-scaling-bench)

> *How much does each inference-time scaling strategy improve accuracy — and at what latency cost?*

Systematic benchmark of inference-time scaling across chain-of-thought, repeated
sampling, and self-consistency on 32 synthetic arithmetic reasoning tasks. Measures
accuracy, latency multiplier, token multiplier, and efficiency frontier across
Qwen2-0.5B and Qwen2-1.5B.

| | |
|---|---|
| Stack | Python · PyTorch · Transformers |
| Method | 6 task types · 5 strategies · accuracy/latency frontier · efficiency analysis |
| Hardware | NVIDIA RTX 2070 (8.6 GB) |

**Key findings:**
- CoT is the **dominant lever**: direct=3–6% → cot_greedy_256=**65–72%** accuracy
- Repeated sampling without CoT: **6.2% at N=8** — diversity over weak reasoning is useless
- cot_greedy_256 is **most efficient**: accuracy/latency = 0.0623 (0.5B), 0.0758 (1.5B)
- cot_greedy_512 adds **nothing** over 256 — reasoning plateau at **170–180 tokens**
- Diminishing returns severe: N=4→N=8 majority: **+3.1pp at 2x cost** (74x total latency)
- **Depth vs diversity is model-size dependent**: 0.5B favors depth, 1.5B favors diverse voting
- Scaling **cannot rescue capability gaps** — conditional tasks: 0% at direct = 0% with CoT = 0% with N=4

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

    +-------------------------------------------------------------------------------------+
    |            LLM Inference Server (simulated)                                         |
    +-------+--------+--------+-------+--------+-------+--------+---------+-------------+
    |Schedul|Prefix  |KV      |Paged  |KV      |Disagg.|Multi   |Request  |Autoscaling  |
    |er     |Cache   |Compact.|Mem    |Quant.  |Serving|LoRA    |Routing  |             |
    |llm-   |prefix- |kv-     |paged- |kv-cache|disagg-|multi-  |request- |slo-aware-   |
    |infer  |cache   |compact |attn   |quant   |prefill|lora-sim|routing  |autoscaling  |
    +-------+--------+--------+-------+--------+-------+--------+---------+-------------+
     "what   "what    "how to  "how to "how to  "split  "adapter "which    "how many
      to run" to reuse" defrag"  alloc"  compress" phases" sched"  instance" instances"

    +------------------------------------------------------------------+
    |          Hardware & Scaling Layer                                |
    +----------+----------+----------+----------+-------------------+
    |Parallelism|Context   |Attention |Kernel    |Decode Attention   |
    |           |Length    |(prefill) |Launch    |(decode)           |
    |comm-cost- |long-ctx- |flash-    |cuda-graph|flash-decoding-    |
    |modeling   |benchmark |attention |decode-prof|bench             |
    +----------+----------+----------+----------+-------------------+
      "how to    "how far   "which     "eliminate  "KV-parallel
       scale"     to push"   kernel"    overhead"   decode"

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
from scheduling and caching to memory allocation, fragmentation dynamics,
compression, mixed-precision KV quantization, prompt compression, KV-cache-aware
scheduling with output length prediction, chunked prefill under memory pressure,
multi-turn KV reuse, system prompt caching, KV cache tiering, attention sparsity
profiling, prefill-decode interference profiling, multi-adapter serving,
disaggregated execution, multi-instance request routing, SLO-aware autoscaling,
cold start profiling, and real-trace workload validation, parallelism modeling,
kernel-level execution optimization including prefill and decode attention kernels,
hardware limits, long-context extension via RoPE scaling, inference-time scaling,
and decoding optimization — including linear, tree-based, batched, and
draft-selection-guided speculative decoding, constrained structured output
generation, chain-of-thought reasoning, and sampling strategy benchmarking.

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
