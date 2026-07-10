# Design Document -- speculative-decoding-sim

## 1. Motivation

Autoregressive language model decoding generates one token per forward pass.
Each pass is memory-bandwidth-bound and costs ~200us on modern hardware.
For 128 output tokens, that is 128 sequential forward passes -- strictly
sequential, with no parallelism.

Speculative decoding breaks this bottleneck:

    1. A small, fast draft model generates K candidate tokens cheaply
    2. The large verifier model validates all K tokens in a single forward pass
    3. Accepted tokens are emitted together; rejected tokens are discarded
    4. At the rejection point, the verifier provides the corrected token

The result: the verifier does one forward pass but produces up to K+1 tokens.

    Standard autoregressive:
      verify("The")          -> "cat"    [1 pass -> 1 token]
      verify("The cat")      -> "sat"    [1 pass -> 1 token]
      verify("The cat sat")  -> "on"     [1 pass -> 1 token]
      Total: 3 passes, 3 tokens

    Speculative decoding:
      draft("The")           -> ["cat", "sat", "on"]   [3 cheap passes]
      verify("The" + draft)  -> accept "cat", "sat", reject "on" -> "upon"
      Total: 1 expensive pass, 3 tokens produced

The core tradeoff:
- If the draft model agrees with the verifier often -> speedup approaches K+1x
- If the draft model disagrees often -> wasted compute, potential slowdown
- Draft model cost directly reduces the net gain

This project simulates this tradeoff over 576 configurations to find:
  - The optimal K for a given draft quality and cost ratio
  - The breakeven point where speculative decoding stops being worth it
  - How different draft model behaviors affect the speedup curve

---

## 2. Architecture

    IDraftModel
      draft(prefix, k) -> DraftResult (k candidate tokens + probabilities)
      |
      +-- FixedAccuracyDraft      constant P(accept) per token
      +-- PositionDecayDraft      P(accept_i) = base * decay^i (degrades with position)
      +-- EntropyAwareDraft       P(accept) varies by token entropy (easy vs hard tokens)

    Verifier
      verify(prefix, draft) -> VerifyResult (verifier probabilities + first rejection)

    AcceptanceSampler
      sample(draft, verify) -> AcceptanceResult (accepted_count + bonus token)

    SpeculativeDecoder
      run_cycle(prefix) -> SpecCycleResult
        1. draft->draft(prefix, K)
        2. verifier->verify(prefix, draft)
        3. sampler->sample(draft, verify)
        4. return accepted_count + bonus token

    StandardDecoder
      decode_sequence(n_tokens) -> BaselineResult
        simply: n_tokens * verify_cost_us (no batching)

    SpecSimulator
      run() -> SpecMetrics
        for each sequence:
          while remaining_tokens > 0:
            result = speculator->run_cycle(prefix)
            record CycleRecord
            advance prefix
        finalize metrics (speedup, acceptance, waste, overhead)

---

## 3. Draft Model Designs

### 3.1 FixedAccuracyDraft

    P(accept_i) = acceptance_rate_cfg   for all i

The simplest model. Every draft token is accepted with the same probability,
independent of position or context. Best for systematic sweeps over the
(acceptance_rate, K) space.

Realistic for: tasks where draft model quality is approximately uniform
across token positions (e.g., highly repetitive text, constrained generation).

### 3.2 PositionDecayDraft

    P(accept_i) = decay_base_rate * decay_factor^i

Accuracy starts high at position 0 and decays exponentially.
With default parameters (base=0.9, decay=0.95):

    Position 0: P = 0.900
    Position 1: P = 0.855
    Position 2: P = 0.812
    Position 3: P = 0.772
    ...

This models the real behavior of speculative decoding: the draft model
is most accurate for the next immediate token and becomes less reliable
as it speculates further ahead. The verifier is more likely to reject
late positions.

Consequence: increasing K beyond a certain point adds mostly unreliable
tokens that are likely to be rejected. The optimal K is lower for this
model than for FixedAccuracy at the same nominal accuracy.

### 3.3 EntropyAwareDraft

    For each token i:
      if random() < high_entropy_fraction:
        P(accept_i) = entropy_low_accuracy   (hard token)
      else:
        P(accept_i) = entropy_high_accuracy  (easy token)

Models the observation that some tokens are predictable ("the", "a", "is")
while others are unpredictable (named entities, numbers, rare words).

Easy tokens (low entropy in the verifier distribution) are accepted at high
rate. Hard tokens are rejected more often. This produces bimodal acceptance:
many cycles either accept most tokens or reject early.

Consequence: higher variance in tokens_per_cycle compared to FixedAccuracy.
The distribution of accepted counts is bimodal rather than geometric.

---

## 4. Acceptance Sampling

The standard rejection sampling rule for speculative decoding:

    For each draft token i:
      r ~ Uniform(0, 1)
      if r < P_draft(token_i) / P_verifier(token_i):
        accept token_i
      else:
        reject token_i
        sample corrected token from adjusted distribution
        stop

In our simulation, since we model acceptance probability directly:

    accept_i = (random() < draft_prob_i)

If all K tokens are accepted, the verifier produces a bonus token
(the next token after the K speculated positions).

Total tokens produced per cycle = accepted_count + 1 (bonus or corrected).

---

## 5. Cost Model

    draft_phase_cost = K * draft_cost_us
    verify_phase_cost = verify_cost_us   (one forward pass regardless of K)
    cycle_cost = draft_phase_cost + verify_phase_cost

    baseline_cost = n_tokens * verify_cost_us

    speedup = baseline_cost / total_spec_cost

The verify cost is fixed at 200us (representing a 7B-parameter model at
~200us per decode step). Draft costs are swept from 10us to 100us,
representing draft model sizes from ~100M to ~1B parameters.

cost_ratio = draft_cost_us / verify_cost_us
  Low (0.05): small draft, cheap speculation, high potential speedup
  High (0.50): expensive draft, speedup advantage narrows or disappears

---

## 6. Metrics

### Per-cycle

    accepted_count         how many draft tokens were accepted
    total_produced         accepted + 1 (bonus/corrected token)
    tokens_wasted          K - accepted_count
    acceptance_rate        accepted / K (0 to 1)
    tokens_per_us          total_produced / cycle_cost

### Aggregate

    speedup_vs_baseline    baseline_cost / total_spec_cost
    tokens_per_cycle       mean tokens produced per verifier call
    acceptance_rate_mean   mean per-cycle acceptance rate
    acceptance_rate_p5     5th percentile (worst-case cycles)
    all_accepted_fraction  fraction of cycles where all K tokens accepted
    draft_tokens_wasted    total_wasted / total_drafted
    compute_overhead_frac  total_draft_cost / total_cost

---

## 7. Results Summary

576-run sweep: 3 draft models x 8 K values x 6 acceptance rates x 4 draft costs

### Key findings

Finding 1: Maximum speedup is 6.06x
Config: fixed model, K=15, acceptance=0.95, draft_cost=10us (cost_ratio=0.05)
Theoretical max for K=15: 16x. Practical ~6x because not all cycles fully accept.

Finding 2: Breakeven is at cost_ratio ~= 0.25
    cost_ratio = 0.05 -> speedup = 2.55x   (clear win)
    cost_ratio = 0.10 -> speedup = 2.10x
    cost_ratio = 0.25 -> speedup = 1.43x
    cost_ratio = 0.50 -> speedup = 0.96x   (loses to baseline)

If the draft model costs more than 25% of the verifier, speculative decoding
starts losing advantage for typical acceptance rates.

Finding 3: Optimal K grows with acceptance rate
    acc = 0.50: K* = 1-3
    acc = 0.70: K* = 2-5
    acc = 0.80: K* = 3-7
    acc = 0.90: K* = 5-15
    acc = 0.95: K* = 7-15

There is no universal optimal K. The right K depends entirely on draft quality.

Finding 4: 80/576 configs (14%) lose to baseline
All losing configs have cost_ratio >= 0.25 and acceptance <= 0.70.
Speculative decoding requires both a cheap draft and a good draft to be useful.

Finding 5: Waste fraction is the key diagnostic
waste_fraction = (K - accepted) / K

At high acceptance rates and low K, waste is low. At low acceptance rates
and high K, waste exceeds 90%, meaning most of the compute is thrown away.
monitoring waste_fraction at runtime is the best signal for adaptive K.

### Heatmap: optimal K by acceptance x cost

    acc\cost   10us   20us   50us  100us
    0.50         3      2      1     1
    0.60         4      3      2     1
    0.70         5      4      2     1
    0.80         7      5      3     2
    0.90        15     10      5     3
    0.95        15     15      7     5

---

## 8. Design Decisions

### Why simulate acceptance probability directly?

In production, acceptance rate depends on the KL divergence between draft
and verifier distributions, which is task- and model-specific. By sweeping
acceptance_rate as an explicit parameter, we can map the full speedup surface
without needing a real model pair. The results bound the achievable speedup
for any real system with a given effective acceptance rate.

### Why three draft model types?

FixedAccuracy gives clean analytical results for the K-acceptance-cost tradeoff.
PositionDecay captures the most common real-world behavior (accuracy degrades
with speculated distance). EntropyAware captures the bimodal nature of natural
language (easy tokens vs hard tokens). Together they bound the realistic range.

### Why not model KV-cache interactions?

Speculative decoding requires storing KV-cache for the draft tokens during
verification. If all K tokens are rejected early, those KV entries are wasted.
This is modeled implicitly through the cost model but not explicitly as page
allocations. That extension would connect this project to kv-cache-compaction-lab
via CopyCostModel.

---

## 9. Connections to Prior Projects

    Component            Source project           Integration
    ────────────────────────────────────────────────────────────────
    Cost model           llm-serving-sim          verify_cost_us maps to decode_cost
    Batch efficiency     llm-inference-scheduler  tokens_per_cycle maps to batch throughput
    KV page sharing      kv-cache-compaction-lab  draft KV pages can be shared with verifier
    Memory per token     tensor-memory-allocator  each speculated token uses scratch space

---

## 10. Future Work

    1. Adaptive K: adjust K at runtime based on observed acceptance rate.
       If acceptance drops, reduce K to avoid waste. If acceptance is high, increase K.

    2. KV cache modeling: track how many KV pages are allocated for draft tokens
       and freed on rejection. Connect to kv-cache-compaction-lab cost model.

    3. Multi-draft: run multiple draft models in parallel, pick the best token
       per position. Higher acceptance at higher cost.

    4. Tree-speculative decoding: instead of a linear sequence of K tokens,
       build a token tree. The verifier validates multiple branches simultaneously.
       Higher expected tokens per verify call at the cost of complexity.

    5. Calibrated acceptance: replace Bernoulli sampling with real draft/verifier
       probability ratios using sampled vocabulary distributions.
