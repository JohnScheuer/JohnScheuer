# João Felipe De Souza
**AI Systems Engineer | LLM Infrastructure & GPU Optimization**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaofelipescheuer)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:johnfelipe13@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/5541997054864)
[![WeChat](https://img.shields.io/badge/WeChat-07C160?style=for-the-badge&logo=wechat&logoColor=white)](#)

Building high-performance foundations for Next-Gen AI. Expert in squeezing maximum TFLOPS out of consumer hardware and scaling LLM inference across distributed clusters.

---

## 🚀 Flagship Infrastructure Projects

### ⚡ [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75)
**CUDA Kernel Engineering & Hardware Optimization**
- Developed a bit-perfect INT4 weight-only quantization kernel using raw **PTX assembly**.
- Achieved **1.000 Cosine Similarity** against FP16 baselines.
- Optimized for NVIDIA Turing (RTX 2070) with specialized Shared Memory padding.

### 🌐 [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine)
**LLM Scaling & Distributed Systems**
- Multi-process runtime implementing **Megatron-style Tensor Parallelism** and **Pipeline Parallelism**.
- **GPipe Scheduler:** Fill-drain micro-batching to minimize idle bubbles.
- **KV Cache Sharding:** Distributed attention state to scale beyond single-GPU VRAM limits.

### 📉 [quantization-runtime](https://github.com/JohnScheuer/quantization-runtime)
**Mathematical Model Compression**
- From-scratch implementation of **AWQ** and **GPTQ** algorithms.
- Validated intelligence preservation on Qwen2-0.5B with **26.05 Perplexity** at 4-bit.
- Deep-dive study on Hessian-based error compensation vs activation salience.

### 🛠️ [agent-tooling-runtime](https://github.com/JohnScheuer/agent-tooling-runtime)
**AI-as-a-Service Platform (SaaS Ready)**
- High-concurrency Agent Engine with an **OpenAI-compatible API**.
- **ACID Billing:** PostgreSQL-backed financial ledger with **Decimal precision** and Redis rate-limiting.
- Production-ready stack with Docker, Gunicorn, and Prometheus metrics.

---

## 🧪 R&D & Specialized Runtimes

- **[rag-inference-stack](https://github.com/JohnScheuer/rag-inference-stack):** High-speed local RAG using ChromaDB and sentence-transformers.
- **[speculative-decoding-runtime](https://github.com/JohnScheuer/speculative-decoding-runtime):** Accelerated inference (1.4x speedup) via draft-model verification.
- **[vlm-inference-runtime](https://github.com/JohnScheuer/vlm-inference-runtime):** Multi-modal deployment for Vision-Language Models.
- **[lora-inference-runtime](https://github.com/JohnScheuer/lora-inference-runtime):** Multi-tenant serving with O(1) adapter hot-swapping.

---

## 🛠️ Technical Arsenal

| Layer | Technologies |
| :--- | :--- |
| **Silicon & Hardware** | CUDA C++, PTX Assembly, Tensor Cores (WMMA), SIMD, GPU Profiling |
| **AI Frameworks** | PyTorch, Transformers, PEFT, Tokenizers, Datasets, ONNX, LangChain |
| **Distributed & Infra** | NCCL/Gloo, DDP, Tensor Parallelism, Docker Compose, Gunicorn |
| **Data & Scaling** | Redis (ZSET Rate Limiting), PostgreSQL (ACID), ChromaDB, Prometheus |

---

## 📊 GitHub Stats

![John's GitHub stats](https://github-readme-stats.vercel.app/api?username=JohnScheuer&show_icons=true&theme=tokyonight)  
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=JohnScheuer&layout=compact&theme=tokyonight&hide=html,css)

---

## 📬 Connect & Collaborate

- **LinkedIn:** [linkedin.com/in/joaofelipescheuer](https://www.linkedin.com/in/joaofelipescheuer)
- **Email:** [johnfelipe13@gmail.com](mailto:johnfelipe13@gmail.com)
- **WeChat:** `JohnScheuer7`
- **Location:** Curitiba, Brazil (GMT-3)

`Code the math, scale the intelligence.`
