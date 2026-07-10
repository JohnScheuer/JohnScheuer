# speculative-decoding-sim

![C++20](https://img.shields.io/badge/C%2B%2B-20-blue.svg)
![CMake](https://img.shields.io/badge/CMake-3.22+-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)
![Sweep](https://img.shields.io/badge/Sweep-576_runs-orange.svg)
![Max Speedup](https://img.shields.io/badge/Max_Speedup-6.06x-purple.svg)

**Simulates speculative decoding to find the optimal speculation length K
as a function of draft model quality and cost.**

> For detailed architecture, algorithm descriptions, and design rationale
> see [DESIGN.md](DESIGN.md).

---

## Portfolio Context

Part of a six-project series modeling the full LLM inference stack:

| Project | Focus | Key Finding |
|---------|-------|-------------|
| [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab) | KV-cache compaction | ThresholdCompaction dominates; 11 free-compaction points |
| [prefix-cache-sim](https://github.com/JohnScheuer/prefix-cache-sim) | Prefix sharing | LFU dominates; multi-turn 60%+ hit rate |
| [llm-inference-scheduler](https://github.com/JohnScheuer/llm-inference-scheduler) | Continuous batching | ChunkedPrefill eliminates starvation |
| [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator) | GPU tensor allocation | Free-list beats buddy/slab for continuous sizes |
| [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim) | End-to-end integration | ChunkedPrefill + LFU: 41% lower TTFT, 94% hit rate |
| **speculative-decoding-sim** | **Breaking the autoregressive bottleneck** | **6.06x speedup; breakeven at cost_ratio = 0.25** |

---

## Problem

Autoregressive decoding is strictly sequential: one forward pass per token.
Speculative decoding parallelizes this by having a cheap draft model propose
K tokens and a single verifier forward pass validate all K simultaneously.

The speedup depends on:
- How often the draft model agrees with the verifier (acceptance rate)
- How cheap the draft model is relative to the verifier (cost ratio)
- How many tokens are speculated per cycle (K)

This project maps that three-way tradeoff over 576 configurations.

---

## Draft Model Types

| Model | Behavior | Best for |
|-------|----------|----------|
| **FixedAccuracy** | Constant P(accept) per token | Mapping the K-acceptance-cost surface |
| **PositionDecay** | P(accept) decays with position | Modeling real draft model degradation |
| **EntropyAware** | P(accept) varies by token difficulty | Modeling mixed easy/hard tokens |

---

## Key Findings

### 1. Maximum speedup: 6.06x

    Config: fixed model, K=15, acceptance=0.95, draft_cost=10us
    Theoretical max for K=15: 16x
    Practical limit: not all cycles fully accept -- waste reduces throughput

### 2. Breakeven at cost_ratio = 0.25

    cost_ratio = draft_cost / verify_cost

    cost_ratio = 0.05 -> speedup = 2.55x
    cost_ratio = 0.10 -> speedup = 2.10x
    cost_ratio = 0.25 -> speedup = 1.43x
    cost_ratio = 0.50 -> speedup = 0.96x  <- loses to baseline

    If the draft model costs more than 25% of the verifier,
    speculative decoding starts losing advantage.

### 3. Optimal K grows with acceptance rate

    acc = 0.50: K* = 1-3     acc = 0.90: K* = 5-15
    acc = 0.70: K* = 2-5     acc = 0.95: K* = 7-15
    acc = 0.80: K* = 3-7

    There is no universal K. The right K depends on the draft model quality.

### 4. Optimal K heatmap (fixed model)

    acc \ draft_cost   10us   20us   50us  100us
    0.50                  3      2      1     1
    0.70                  5      4      2     1
    0.80                  7      5      3     2
    0.90                 15     10      5     3
    0.95                 15     15      7     5

### 5. 14% of configs lose to baseline

    80/576 configs have speedup < 1.0
    All losing configs: cost_ratio >= 0.25 AND acceptance <= 0.70
    Speculative decoding is not universally beneficial.

---

## Quick Start

    # Build
    cmake -S . -B build -G Ninja
    cmake --build build -j

    # Single run
    ./build/speculative_decoding_sim \
        --draft-model fixed \
        --k 5 \
        --acceptance-rate 0.8 \
        --draft-cost-us 20 \
        --n-sequences 500 \
        --tokens-per-seq 128

    # Full sweep (576 runs)
    python3 experiments/sweep_spec.py

    # Plots (6 plots)
    python3 plots/plot_spec.py

    # Analysis
    python3 scripts/analyze_spec.py

---

## CLI Reference

    ./build/speculative_decoding_sim [options]

      --draft-model STR       fixed | position_decay | entropy_aware
      --k N                   speculation length (default: 5)
      --acceptance-rate F     draft acceptance probability (default: 0.8)
      --draft-cost-us F       cost per draft forward pass us (default: 20)
      --verify-cost-us F      cost per verify forward pass us (default: 200)
      --decay-base F          position_decay base rate (default: 0.9)
      --decay-factor F        position_decay factor (default: 0.95)
      --entropy-high F        entropy_aware high accuracy (default: 0.95)
      --entropy-low F         entropy_aware low accuracy (default: 0.5)
      --entropy-frac F        fraction of high-entropy tokens (default: 0.3)
      --n-sequences N         sequences to simulate (default: 500)
      --tokens-per-seq N      output tokens per sequence (default: 128)
      --seed N                random seed (default: 42)
      --summary-out FILE      append summary CSV

---

## Project Structure

    speculative-decoding-sim/
    |-- include/
    |   |-- config.hpp          SpecConfig (all parameters)
    |   |-- token.hpp           Token, DraftResult, VerifyResult
    |   |-- draft_model.hpp     IDraftModel + Fixed, Decay, Entropy
    |   |-- verifier.hpp        Verifier (rejection sampling)
    |   |-- acceptance.hpp      AcceptanceSampler, AcceptanceResult
    |   |-- speculator.hpp      SpeculativeDecoder (draft + verify loop)
    |   |-- baseline.hpp        StandardDecoder (autoregressive baseline)
    |   |-- metrics.hpp         CycleRecord, SpecMetrics, Collector
    |   +-- simulator.hpp       SpecSimulator (runs sequences)
    |-- src/
    |   |-- draft_model.cpp
    |   |-- verifier.cpp
    |   |-- acceptance.cpp
    |   |-- speculator.cpp
    |   |-- baseline.cpp
    |   |-- metrics.cpp
    |   |-- simulator.cpp
    |   +-- main.cpp
    |-- experiments/
    |   +-- sweep_spec.py       576-run sweep
    |-- plots/
    |   +-- plot_spec.py        6 plots
    |-- scripts/
    |   +-- analyze_spec.py     Analysis + optimal K table
    |-- results/
    |   |-- sweep_summary.csv   576 rows
    |   +-- plots/
    |       |-- 01_speedup_vs_k_fixed.png
    |       |-- 02_acceptance_vs_k_by_model.png
    |       |-- 03_waste_vs_k.png
    |       |-- 04_speedup_vs_cost_ratio.png
    |       |-- 05_pareto_speedup_vs_overhead.png
    |       +-- 06_optimal_k_heatmap.png
    |-- DESIGN.md
    |-- LICENSE
    +-- README.md
