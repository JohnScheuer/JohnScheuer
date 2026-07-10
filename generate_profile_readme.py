from pathlib import Path

README = """\
# Joao Felipe De Souza

Systems engineer focused on LLM inference infrastructure.
I build simulators and tools to understand the tradeoffs inside serving systems.

---

## LLM Inference Stack -- 6-Project Series

I implemented the full memory and serving layer of an LLM server from scratch,
one component at a time, then integrated everything into an end-to-end simulator.

| # | Project | Focus | Key Finding |
|---|---------|-------|-------------|
| 1 | [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab) | KV-cache page compaction | ThresholdCompaction dominates; 11 free-compaction points (delta_P95 = 0ms) |
| 2 | [prefix-cache-sim](https://github.com/JohnScheuer/prefix-cache-sim) | Prefix sharing with RadixTree | LFU dominates small cache under Zipf; multi-turn hit rate 60%+ |
| 3 | [llm-inference-scheduler](https://github.com/JohnScheuer/llm-inference-scheduler) | Continuous batching scheduler | ChunkedPrefill eliminates starvation; FCFS collapses under load |
| 4 | [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator) | GPU tensor memory allocation | Free-list beats buddy/slab for continuous size distributions |
| 5 | [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim) | End-to-end integration | ChunkedPrefill + LFU: 41% lower TTFT p95, 94% prefix hit rate |
| 6 | [speculative-decoding-sim](https://github.com/JohnScheuer/speculative-decoding-sim) | Speculative decoding | 6.06x max speedup; breakeven at cost_ratio = 0.25 |

All projects: C++20 core, Python sweep/plots, quantitative results, open source.

### The systems insight from building all six

Optimizing one component in isolation is not enough.

- The scheduler that minimizes TTFT hits OOM first under memory pressure
- The prefix cache that saves compute consumes memory of its own
- The allocator that reduces fragmentation increases lookup cost
- Speculative decoding that doubles throughput can hurt if the draft model is too expensive

End-to-end systems thinking matters more than any single optimization.

---

## Stack

    C++20       Systems core -- allocators, schedulers, caches, simulators
    Python      Sweeps, plots, analysis (pandas, matplotlib)
    CMake       Build system
    Git         All projects open source on GitHub

---

## Currently exploring

- Validating simulation results against real PyTorch/CUDA behavior
- Mixture-of-Experts routing and load balancing
- Multi-GPU placement and NVLink memory transfer modeling
"""

out = Path("README.md")
out.write_text(README)
print("Wrote", out)

