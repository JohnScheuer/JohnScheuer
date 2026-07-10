# Joao Felipe De Souza

Systems engineer focused on LLM inference infrastructure, GPU memory systems, and serving optimization.

I build simulators and tools to study the latency, memory, throughput, and routing tradeoffs inside LLM serving systems.

[LinkedIn](https://www.linkedin.com/in/joaofelipescheuer/)

---

## LLM Inference Stack — 9-Project Series

I implemented the memory and serving layer of an LLM server from scratch,
one component at a time, then integrated everything into an end-to-end simulator.

| Project | Focus | Key Finding |
|---------|-------|-------------|
| [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab) | KV-cache page compaction | ThresholdCompaction dominates; 11 free-compaction points |
| [prefix-cache-sim](https://github.com/JohnScheuer/prefix-cache-sim) | Prefix sharing with RadixTree | LFU dominates under Zipf; multi-turn hit rate 60%+ |
| [llm-inference-scheduler](https://github.com/JohnScheuer/llm-inference-scheduler) | Continuous batching scheduler | ChunkedPrefill eliminates starvation; FCFS collapses under load |
| [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator) | GPU tensor memory allocation | Free-list beats buddy/slab for continuous size distributions |
| [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim) | End-to-end LLM serving | ChunkedPrefill + LFU: 41% lower TTFT p95, 94% prefix hit rate |
| [speculative-decoding-sim](https://github.com/JohnScheuer/speculative-decoding-sim) | Speculative decoding | 6.06x max speedup; breakeven at cost_ratio = 0.25 |
| [moe-router-sim](https://github.com/JohnScheuer/moe-router-sim) | MoE routing and load balancing | ExpertChoice best balance; NoisyTopK best practical tradeoff |
| [admission-control-sim](https://github.com/JohnScheuer/admission-control-sim) | Admission control under overload | Tight token budget maximizes goodput; proactive beats reactive |
| [kv-cache-disaggregation-sim](https://github.com/JohnScheuer/kv-cache-disaggregation-sim) | Prefill/decode disaggregation | Disagg wins only at arrival>=20 AND prompt>=1024; 29% TTFT gain |

All projects: C++20 core, Python sweeps and plots, quantitative results, open source.

---

## Core Systems Insight

Optimizing one component in isolation is not enough.

- The scheduler that minimizes TTFT hits OOM first under memory pressure
- The prefix cache that saves compute also consumes memory
- The allocator that reduces fragmentation can increase lookup cost
- Speculative decoding can hurt throughput if the draft model is too expensive
- The MoE router that achieves perfect balance sacrifices expert specialization
- Admission control that accepts everything destroys goodput under overload
- Disaggregation that eliminates interference pays KV transfer cost instead

End-to-end systems thinking matters more than any single optimization.

---

## Stack

- **C++20** — allocators, schedulers, caches, routers, simulators
- **Python** — sweeps, plots, analysis (pandas, matplotlib)
- **CMake + Ninja** — build system
- Quantitative sweeps with reproducible plots and CSV results

---

## Currently Exploring

- Validating simulation results against real PyTorch and CUDA behavior
- Chunked KV transfer and pipeline overlap with decode
- Dynamic disaggregation: switching modes based on observed load
