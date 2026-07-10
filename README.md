# Joao Felipe De Souza

Systems engineer focused on LLM inference infrastructure.

I build simulators and tools to study the tradeoffs inside LLM serving systems:
memory allocation, KV-cache management, prefix reuse, batching, and decoding.

---

## LLM Inference Stack — 6-Project Series

I implemented the memory and serving layer of an LLM server from scratch,
one component at a time, then integrated everything into an end-to-end simulator.

| Project | Focus | Key Finding |
|---------|-------|-------------|
| [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab) | KV-cache page compaction | ThresholdCompaction dominates; 11 free-compaction points |
| [prefix-cache-sim](https://github.com/JohnScheuer/prefix-cache-sim) | Prefix sharing with RadixTree | LFU dominates under Zipf; multi-turn hit rate 60%+ |
| [llm-inference-scheduler](https://github.com/JohnScheuer/llm-inference-scheduler) | Continuous batching scheduler | ChunkedPrefill eliminates starvation; FCFS collapses |
| [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator) | GPU tensor memory allocation | Free-list beats buddy/slab for continuous sizes |
| [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim) | End-to-end LLM serving | ChunkedPrefill + LFU: 41% lower TTFT p95, 94% prefix hit rate |
| [speculative-decoding-sim](https://github.com/JohnScheuer/speculative-decoding-sim) | Speculative decoding | 6.06x max speedup; breakeven at cost_ratio = 0.25 |

---

## Main Systems Insight

Optimizing one component in isolation is not enough.

- The scheduler that minimizes TTFT can hit OOM first
- The prefix cache that saves compute also consumes memory
- The allocator that reduces fragmentation can increase lookup cost
- Speculative decoding can hurt throughput if the draft model is too expensive

End-to-end systems thinking matters more than any single optimization.

---

## Stack

- C++20
- Python
- CMake
- Quantitative sweeps and reproducible plots

---

## Currently Exploring

- Validation of simulation results against real PyTorch/CUDA behavior
- Mixture-of-Experts routing and load balancing
- Multi-GPU placement and memory transfer modeling
