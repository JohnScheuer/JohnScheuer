# João Felipe De Souza
**AI Systems Engineer | LLM Infrastructure & GPU Optimization**

Building the high-performance foundations for the next generation of Intelligent Systems. My work spans from low-level CUDA kernel development to distributed multi-node inference and production-grade agent platforms.

---

## 🚀 Featured AI Infrastructure Projects

### ⚡ [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75)
**CUDA Kernel Engineering & Hardware Optimization**
- Developed a fused INT4 weight-only quantization kernel using raw **PTX m16n8k8 assembly**.
- Achieved **75% weight VRAM reduction** with bit-perfect fidelity (1.000 Cosine Similarity).
- Implemented specialized Shared Memory padding for efficient $M=1$ (decode) inference.

### 🌐 [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine)
**Scaling & Distributed Systems**
- Built a simulated multi-GPU runtime implementing **Tensor Parallelism (Megatron-style)** and **Pipeline Parallelism**.
- Implemented a **GPipe-style micro-batch scheduler** to optimize throughput and minimize pipeline bubbles.
- Designed **KV Cache Sharding** logic to enable model scaling beyond single-device memory limits.

### 📉 [quantization-runtime](https://github.com/JohnScheuer/quantization-runtime)
**Model Compression & Mathematical Research**
- From-scratch implementation of **AWQ** (Activation-Aware) and **GPTQ** (Hessian-based) algorithms.
- Achieved high-fidelity 4-bit compression on Qwen2-0.5B with competitive **26.05 Perplexity**.
- Comparative study on numerical stability and second-order error compensation in small-scale LLMs.

### 🛠️ [agent-tooling-runtime](https://github.com/JohnScheuer/agent-tooling-runtime)
**Full-Stack AI Platform & Monetization**
- Enterprise-grade Agent Engine with an **OpenAI-compatible API** and async tool execution.
- Engineered an **ACID Billing Engine** (PostgreSQL/Decimal) with real-time token tracking and Redis rate-limiting.
- Built-in observability with **Prometheus metrics** and granular per-step JSON tracing.

### 📚 [rag-inference-stack](https://github.com/JohnScheuer/rag-inference-stack)
**Data Integration & Retrieval**
- Modular RAG pipeline featuring PDF/TXT ingestion and **ChromaDB** vector storage.
- Optimized for sub-2s latency on consumer GPUs (8GB VRAM) using Qwen2 and sentence-transformers.

---

## 🛠️ Technical Stack

- **Lower-Level:** CUDA C++, PTX Assembly, Warp-level primitives, SIMD optimization.
- **System-Level:** Python, PyTorch, Distributed Data Parallel (DDP), NCCL/Gloo, Tensor Parallelism.
- **Inference & Serving:** FastAPI, Gunicorn, Redis (Rate Limiting), PostgreSQL (Transactional Billing), Docker.
- **Observability:** Prometheus, JSON Tracing, SLI/SLO monitoring.

---

## 📬 Connect with me

- **LinkedIn:** [linkedin.com/in/joaofelipedezouza](https://linkedin.com/in/joaofelipedezouza)
- **Email:** joao.felipe@example.com (Substitua pelo seu real)

`Build fast, serve smart.`
