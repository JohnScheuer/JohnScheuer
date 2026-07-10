# Joao Felipe De Souza

Systems engineer focused on LLM inference infrastructure, GPU memory systems, and serving optimization.

I build simulators and tools to study the latency, memory, throughput, routing, and quantization tradeoffs inside LLM serving systems.

[LinkedIn](https://www.linkedin.com/in/joaofelipescheuer/)

---

## LLM Inference Stack — 13-Project Series

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
| [speculative-decoding-validation](https://github.com/JohnScheuer/speculative-decoding-validation) | Real GPU validation | Simulation predictions confirmed: median 1.14x speedup |
| [quantization-impact-analyzer](https://github.com/JohnScheuer/quantization-impact-analyzer) | Weight quantization sensitivity | INT8-g32: 1.8x compression, +0.13 PPL; group-wise reduces INT4 error 99% |
| [latency-breakdown-simulator](https://github.com/JohnScheuer/latency-breakdown-simulator) | Where each millisecond goes | Compute = 99.8%; prefix cache saves 17% TTFT; disagg adds 8-20% overhead |
| [request-lifecycle-tracker](https://github.com/JohnScheuer/request-lifecycle-tracker) | Per-request event tracing | 24 event types; full lifecycle from arrival to memory release |

All projects: C++20 or Python, quantitative results, open source.

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
- Quantization that maximizes compression destroys model quality
- The breakdown shows: compute dominates, overhead is real but small
- The lifecycle tracker reveals: every decision leaves a trace

End-to-end systems thinking matters more than any single optimization.

---

## Stack

- **C++20** -- allocators, schedulers, caches, routers, simulators, tracers
- **Python + PyTorch** -- real model validation, quantization analysis, sweeps
- **CMake + Ninja** -- build system
- Quantitative results with reproducible CSVs and plots

---

## Currently Exploring

- Waterfall/Gantt chart visualization from lifecycle traces
- Concurrency model for realistic queue buildup under load
- Integration with real GPU timing traces
