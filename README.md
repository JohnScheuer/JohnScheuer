# João Felipe De Souza
### AI Systems Engineer | LLM Infrastructure & GPU Optimization

[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaofelipescheuer-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/joaofelipescheuer)
[![Email](https://img.shields.io/badge/Email-johnfelipe13%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:johnfelipe13@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-%2B55%2041%2099705--4864-25D366?style=flat-square&logo=whatsapp&logoColor=white)](https://wa.me/5541997054864)
![WeChat](https://img.shields.io/badge/WeChat-JohnScheuer7-07C160?style=flat-square&logo=wechat&logoColor=white)

**Building high-performance foundations for Next-Gen AI.** Expert in squeezing maximum TFLOPS out of consumer hardware and scaling LLM inference across distributed clusters.

Currently based in Curitiba, Brazil (GMT-3). Open to relocation worldwide.

---

## 🚀 Flagship Infrastructure Projects

### ⚡ mini-llm-inference-engine
**Full C++/CUDA Runtime**

- Transformer inference engine in pure **C++/CUDA**, no PyTorch execution path.
- **32.4k tok/s peak**, achieving **87% of INT8 Tensor Core ceiling** on RTX 2070.
- Custom Flash Attention, cuBLASLt INT8, CUDA Graphs, Megatron-style TP.
- Runs TinyStories 110M and TinyLlama 1.1B end-to-end.

### ⚡ paged-attention-runtime
**PagedAttention from Scratch (Optimized)**

- Custom CUDA implementation of vLLM's core algorithm.
- **2.89M tok/s** at 8 concurrent sequences (**5.32x scaling**).
- **29x kernel optimization gain** (v1 to v3): warp reduction + online softmax + shared memory tiling + half2 vectorization.
- **205-397x speedup** vs HuggingFace on attention layer.
- **66.7% memory reduction** via block-based KV allocation.
- Block-based KV cache, copy-on-write, GQA-aware attention.

### ⚡ sm75-tensorcore-microkernel
**PTX-Level GEMM Engineering**

- Manual **PTX instruction emission** for Tensor Core GEMM.
- **Beats cuBLAS** at 2048×2048×2048; achieves 60-65% at 8192×8192×8192.
- Auto-tuning over WARPS / STAGE_K / ILP_DEPTH configuration space.

### ⚡ fused-int4-gemm-sm75
**CUDA Kernel + End-to-End LLM Integration**

- Bit-perfect INT4 weight-only quantization kernel using **raw PTX assembly**.
- Achieved **1.000 Cosine Similarity** against FP16 baselines.
- End-to-end Qwen2-0.5B integration: **-14.7% VRAM** with coherent output.
- Documented SM75 structural limits (no cp.async, no INT4 MMA operands).

### 🏗️ llm-fusion-compiler
**Compiler MVP with CUDA Codegen**

- Full pipeline: **IR → CUDA codegen → nvcc → GPU execution**.
- 9 Transformer fusion patterns (GEMM+Bias+GeLU, LayerNorm fusion, etc.).
- **10.5 TFLOPS peak** on RTX 2070 (37% of SM75 theoretical peak).
- Templated CUDA generation via Jinja2 with type/shape specialization.

### 🌐 distributed-inference-engine
**LLM Scaling & Distributed Systems**

- Multi-process runtime implementing **Megatron-style Tensor Parallelism** and **Pipeline Parallelism**.
- **GPipe Scheduler:** Fill-drain micro-batching to minimize idle bubbles.
- **KV Cache Sharding:** Distributed attention state to scale beyond single-GPU VRAM limits.
- Bit-identical validation on Qwen2-0.5B weights.

### 🛠️ custom-llm-serving-engine
**Production Serving Runtime**

- OpenAI-compatible inference server (/v1/completions, /v1/chat/completions).
- **Continuous batching, SSE streaming**, KV cache management.
- Prometheus metrics, graceful shutdown, health checks.
- 33/33 unit tests + 6/6 end-to-end scenarios passing.

### 🌍 llm-gateway-saas
**LLM-as-a-Service Platform (Production-Ready)**

- High-concurrency backend with **OpenAI-compatible API**.
- **ACID Billing:** PostgreSQL-backed financial ledger with Decimal precision.
- **Distributed Rate Limiting:** Redis ZSET sliding window (multi-worker safe).
- Tool calling execution layer, Stripe integration, admin dashboard.
- Production stack: Docker Compose, Gunicorn, Prometheus.

### 📉 quantization-runtime
**Mathematical Model Compression**

- From-scratch implementation of **AWQ** and **GPTQ** algorithms.
- Validated intelligence preservation on Qwen2-0.5B with **26.05 Perplexity at 4-bit**.
- Deep-dive study on Hessian-based error compensation vs activation salience.

---

## 🧪 R&D & Specialized Runtimes

- **flash-attention-sm75-register-fused:** Register-fused FlashAttention for Turing (5.0 TFLOPS peak, roofline-validated).
- **flash-attention-sm75:** FlashAttention v1 forward pass in CUDA for SM75.
- **fused-backward-kernels-sm75:** Fused GEMM+Bias+GeLU backward kernels (3.1× faster than autograd at M=1024).
- **rag-inference-stack:** High-speed local RAG using ChromaDB and sentence-transformers.
- **speculative-decoding-runtime:** Accelerated inference (1.41× speedup) via draft-model verification.
- **vlm-inference-runtime:** Multi-modal deployment wrapper for Vision-Language Models.
- **lora-inference-runtime:** Multi-tenant serving with sub-3ms adapter hot-swapping.

---

## 🛠️ Technical Arsenal

| Layer | Technologies |
|---|---|
| **Silicon & Hardware** | CUDA C++, PTX Assembly, Tensor Cores (WMMA), CUDA Graphs, Nsight Compute |
| **Compilers & Codegen** | IR design, CUDA codegen (Jinja2), MLIR/LLVM (studied), TVM concepts |
| **AI Frameworks** | PyTorch, HuggingFace Transformers, PEFT, Tokenizers, ONNX |
| **Distributed & Infra** | NCCL/Gloo, torch.distributed, Tensor Parallelism, Pipeline Parallelism |
| **Serving & Runtime** | FastAPI, Continuous Batching, PagedAttention, KV Cache Management, SSE Streaming |
| **Backend & Scaling** | Redis (ZSET Rate Limiting), PostgreSQL (ACID), ChromaDB, Prometheus |
| **DevOps** | Docker Compose, Gunicorn, Nginx, GitHub Actions |
| **Languages** | C, C++ (17/20), CUDA, PTX, Python, Rust, TypeScript (basic) |

---

## 🔬 Key Metrics Across Portfolio

| Achievement | Project |
|---|---|
| **32.4k tok/s** peak throughput | mini-llm-inference-engine |
| **87% INT8 Tensor Core ceiling** | mini-llm-inference-engine |
| **2.89M tok/s** at 8 concurrent sequences | paged-attention-runtime |
| **29x kernel optimization gain** | paged-attention-runtime |
| **205-397x vs HuggingFace** (attention layer) | paged-attention-runtime |
| **66.7% memory reduction** (block allocation) | paged-attention-runtime |
| **10.5 TFLOPS** compiler-generated | llm-fusion-compiler |
| **Beats cuBLAS** at 2048² GEMM | sm75-tensorcore-microkernel |
| **1.000 Cosine Similarity** INT4 vs FP16 | fused-int4-gemm-sm75 |
| **Bit-identical** distributed TP | distributed-inference-engine |
| **1.41× speedup** speculative decoding | speculative-decoding-runtime |
| **26.05 PPL 4-bit AWQ** | quantization-runtime |
| **R² = 0.9996** comm cost model | comm-cost-modeling |

---

## 💼 Experience

**AI Infrastructure Engineer (Contract)** — Confidential Leading Chinese LLM Company (Under NDA) | Sep 2025 – Mar 2026  
Built Rust-based ingestion pipelines with Tokio async and backpressure-safe systems supporting an in-production LLM stack.

**Software Architecture Lead & Operations Manager** — ZBrasil (Cross-border E-commerce) | Apr 2025 – Aug 2025  
Led backend architecture and GPU infrastructure decisions.

---

## 🌟 Open Source

- Contributed to [LLM Inference Handbook (llm-inference-at-scale)](https://github.com/harshuljain13/llm-inference-at-scale) — module on observability signal coverage for LLM serving.

---

## 📬 Connect & Collaborate

- **LinkedIn:** [linkedin.com/in/joaofelipescheuer](https://linkedin.com/in/joaofelipescheuer)
- **Email:** johnfelipe13@gmail.com
- **WhatsApp:** [+55 41 99705-4864](https://wa.me/5541997054864)
- **WeChat:** JohnScheuer7
- **Location:** Curitiba, Brazil (GMT-3) — **Open to Relocation Worldwide**

---

*Code the math, scale the intelligence.*
