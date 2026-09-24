# João Felipe De Souza
### Senior AI Systems Engineer | LLM Inference Infrastructure, GPU/NPU Optimization & Heterogeneous Serving

[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaofelipescheuer-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/joaofelipescheuer)
[![Email](https://img.shields.io/badge/Email-johnfelipe13%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:johnfelipe13@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-%2B55%2041%2099705--4864-25D366?style=flat-square&logo=whatsapp&logoColor=white)](https://wa.me/5541997054864)
![WeChat](https://img.shields.io/badge/WeChat-JohnScheuer7-07C160?style=flat-square&logo=wechat&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-JohnScheuer-181717?style=flat-square&logo=github&logoColor=white)

Focused on high-performance LLM inference, GPU/NPU kernel optimization, and heterogeneous distributed runtime design across NVIDIA CUDA and Huawei Ascend CANN ecosystems.

Currently based in Curitiba, Brazil (GMT-3). **Actively relocating to China (Hangzhou/Shanghai/Beijing)** — Z-Visa sponsorship required.

---

## Flagship Infrastructure Projects

### hybrid-inference-runtime (NEW — 2026)
**Heterogeneous PD Serving: NVIDIA Blackwell x Huawei Ascend 910B2**

- Disaggregated Prefill-Decode serving engine connecting NVIDIA RTX 5060 (Blackwell CC 12.0) and Huawei Ascend 910B2 (DaVinci V300 / CANN 8.6) across a live intercontinental WAN bridge.
- **32 empirical JSON artifacts and 39 high-resolution microarchitectural figures** from physical silicon characterization.
- Validated end-to-end between Curitiba (Brazil) and Peng Cheng CloudBrain 3 (China): TTFT 35.43 ms, TPOT 0.65 ms/token.
- Comprehensive DaVinci V300 reverse engineering: Fractal-16 flat-latency law, L1 buffer spill at 1024 KB, 32 AI Core saturation at 3.23M tok/s, HBM2e stride collapse (-99.1% at s=256).
- Proved Ascend 910B2 achieves **83.5% silicon efficiency** (317.16 / 380 TFLOPS) — the ~60% gap vs NVIDIA H100 is fabrication node (SMIC 7nm DUV vs TSMC 4N EUV), not architecture.
- Advanced algorithm benchmarks: DeepSeek MLA (93% VRAM cut), DeepSeekMoE E=64/K=8 (2.85x), PagedAttention B=16 sweet spot, Zero-Copy CoW Forking (286x), FlashAttention Online Softmax (17 MB at 64k tokens), INT4 quantization (4.00x).
- Production kernels (Ascend C C++ VLIW, HCCL sharding) maintained in private enterprise repository.
- **Repository:** [github.com/JohnScheuer/hybrid-inference-runtime](https://github.com/JohnScheuer/hybrid-inference-runtime)

---

### mini-llm-inference-engine
**Full C++/CUDA Runtime**

- Transformer inference engine in pure C++/CUDA (no PyTorch execution path).
- 32.4k tok/s peak, achieving 87% of INT8 Tensor Core ceiling on RTX 2070.
- Custom Flash Attention, cuBLASLt INT8, CUDA Graphs, Megatron-style TP.
- Runs TinyStories 110M and TinyLlama 1.1B end-to-end.

---

### paged-attention-runtime
**PagedAttention + Scheduling Runtime (Single-GPU Study)**

- Custom CUDA implementation of block-based PagedAttention (logical to physical KV mapping).
- 2.89M tok/s kernel microbenchmark (small-head configuration, RTX 2070).
- 29x kernel optimization gain (v1 to v3): warp reduction + online softmax + shared memory tiling + half2 vectorization.
- 205-397x vs naive PyTorch attention (non-Flash baseline, attention-layer only).
- 66.7% memory reduction via block-based KV allocation.
- Includes continuous batching, swap-first preemption, and cost-based victim policy.

---

### sm75-tensorcore-microkernel
**PTX-Level GEMM Engineering**

- Manual PTX instruction emission for Tensor Core GEMM.
- Outperforms cuBLAS on specific 2048x2048x2048 configuration (SM75 tuned).
- Achieves 60-65% of cuBLAS performance at 8192^3.
- Auto-tuning over WARPS / STAGE_K / ILP_DEPTH configuration space.

---

### fused-int4-gemm-sm75
**INT4 CUDA Kernel + LLM Integration**

- Bit-accurate INT4 weight-only quantization kernel using raw PTX assembly.
- 1.000 cosine similarity vs FP16 baseline (layer-level validation).
- End-to-end Qwen2-0.5B integration: -14.7% VRAM usage with coherent outputs.
- Documents SM75 structural limits (no cp.async, no native INT4 MMA operands).

---

### llm-fusion-compiler
**Compiler MVP with CUDA Codegen**

- Full pipeline: IR to CUDA codegen to nvcc to GPU execution.
- 9 Transformer fusion patterns (GEMM+Bias+GeLU, LayerNorm fusion, etc.).
- 10.5 TFLOPS peak on RTX 2070 (37% of SM75 theoretical peak).
- Templated CUDA generation with type/shape specialization.

---

### distributed-inference-engine
**Distributed LLM Runtime**

- Multi-process runtime implementing Megatron-style Tensor Parallelism and Pipeline Parallelism.
- GPipe-style fill-drain micro-batching.
- KV cache sharding across processes.
- Bit-identical validation on Qwen2-0.5B weights (controlled setup).

---

### custom-llm-serving-engine
**OpenAI-Compatible Serving Runtime**

- Continuous batching, SSE streaming, KV cache management.
- Prometheus metrics, graceful shutdown, health checks.
- 33/33 unit tests + 6/6 end-to-end scenarios passing.

---

### quantization-runtime
**Model Compression Research Implementation**

- From-scratch AWQ and GPTQ implementations.
- Validated on Qwen2-0.5B with 26.05 perplexity at 4-bit.
- Explores Hessian-based compensation vs activation-aware weighting.

---

## Selected R&D Systems

- **flash-attention-sm75-register-fused** — Register-fused FlashAttention (5.0 TFLOPS peak, roofline-validated).
- **flash-attention-sm75** — FlashAttention v1 forward pass in CUDA (SM75).
- **fused-backward-kernels-sm75** — Fused GEMM+Bias+GeLU backward kernels (3.1x vs autograd at M=1024).
- **speculative-decoding-runtime** — 1.41x speedup via draft-model verification.
- **vlm-inference-runtime** — Vision-Language deployment wrapper.
- **lora-inference-runtime** — Multi-tenant adapter serving with hot-swapping.
- **npu-performance-model** — Cycle-approximate DaVinci V300 microarchitectural emulator (Ascend 910B2).
- **vllm-multinode-diagnostics** — Multi-node telemetry harness with coordinated-omission-safe latency reporting.

---

## Technical Stack

| Layer | Technologies |
|-------|-------------|
| GPU & Low-Level (NVIDIA) | CUDA C++, PTX, Tensor Cores (WMMA), CUDA Graphs, Nsight Compute |
| NPU & Low-Level (Huawei) | Ascend C (C++ VLIW), CANN 8.6, DaVinci V300 (Cube/Vector/MTE), HCCL, torch_npu |
| Compilers | IR design, CUDA codegen, MLIR/LLVM concepts, Ascend Tiling Engine |
| AI Frameworks | PyTorch, PyTorch-NPU, HuggingFace, PEFT, ONNX, vLLM, SGLang |
| Distributed | NCCL, HCCL, torch.distributed, Tensor Parallelism, Pipeline Parallelism, PD Disaggregation |
| Serving | FastAPI, Continuous Batching, PagedAttention, KV Management, Chunked Prefill |
| Backend | Redis, PostgreSQL, Prometheus |
| DevOps | Docker, GitHub Actions |
| Languages | C, C++17/20, CUDA, PTX, Python, Rust |

---

## Selected Quantitative Results

| Achievement | Project / Platform |
|-------------|---------|
| 83.5% silicon efficiency (317 / 380 TFLOPS) | Ascend 910B2 physical characterization |
| 1189.25 GB/s HBM2e saturation | Ascend 910B2 memory subsystem |
| 1378.62 GB/s HBM2e write peak | Ascend 910B2 R/W asymmetry |
| 3.23M tok/s (32 AI Core saturation) | Ascend 910B2 multi-core scaling |
| 0.65 ms/token TPOT (intercontinental) | hybrid-inference-runtime |
| 286x Zero-Copy CoW Forking speedup | Ascend 910B2 PagedAttention |
| 93% VRAM reduction (DeepSeek MLA) | Ascend 910B2 serving algorithms |
| 314.18 GB/s GDDR7 saturation | NVIDIA RTX 5060 Blackwell |
| 32.4k tok/s peak | mini-llm-inference-engine |
| 87% INT8 Tensor Core ceiling | mini-llm-inference-engine |
| 2.89M tok/s kernel microbenchmark | paged-attention-runtime |
| 29x kernel optimization gain | paged-attention-runtime |
| 10.5 TFLOPS compiler-generated | llm-fusion-compiler |
| 1.41x speedup speculative decoding | speculative-decoding-runtime |
| 26.05 PPL at 4-bit (AWQ) | quantization-runtime |

---

## Experience

**AI Infrastructure Engineer (Contract)** — Confidential Leading Chinese LLM Company (Under NDA) | Sep 2025 – Mar 2026
Built Rust-based ingestion pipelines with Tokio async and backpressure-safe systems for production LLM infrastructure.

**Software Architecture Lead** — ZBrasil | Apr 2025 – Aug 2025
Led backend architecture and GPU infrastructure decisions.

---

## Open Source

Contributed to LLM Inference Handbook (llm-inference-at-scale) — module on observability signal coverage for LLM serving.

---

## Contact

**LinkedIn:** [linkedin.com/in/joaofelipescheuer](https://linkedin.com/in/joaofelipescheuer)
**Email:** johnfelipe13@gmail.com
**WeChat:** JohnScheuer7
**Location:** Curitiba, Brazil — Actively relocating to China (Hangzhou/Shanghai/Beijing)
