---
layout: post
title_en: "LLM Inference Optimization: Caching, Quantization, and Model Routing for Cost Control"
title_cn: "LLM推理优化：缓存、量化与模型路由实战指南"
date: 2026-08-17 00:34:12 +0800
category: ai
content_type: tool_guide
content_type_cn: "工具攻略"
content_type_en: "Tool Guide"
tags:
  - "LLM推理"
  - "推理优化"
  - "TensorRT-LLM"
  - "模型路由"
  - "成本控制"
summary_en: "A practical guide to reducing LLM inference costs without touching model weights. Covers prompt caching, quantization with TensorRT-LLM, model routing, and async batching—all implementable today with open-source tools."
summary_cn: "不碰模型权重，也能大幅降低推理成本。本文介绍提示缓存、TensorRT-LLM量化、模型路由和异步批处理四种方法，均可用开源工具落地。"
---

<!-- Chinese Version -->
<div class="lang-cn" markdown="1">

## LLM推理优化：缓存、量化与模型路由实战指南

# LLM推理优化：缓存、量化与模型路由实战指南

## 这是什么

LLM推理成本正在成为AI应用规模化最大的瓶颈。缓存、量化和模型路由是三种经过验证的优化手段，可以在不改变模型权重的前提下显著降低延迟和成本。缓存利用重复提示减少计算，量化压缩模型体积加速推理，模型路由根据任务复杂度动态选择合适模型。这三者组合使用，通常能将推理成本降低50%-80%，同时保持响应质量。

## 怎么用

### 第一步：工作负载审计

在动手优化前，先分析你的推理请求特征。记录三类数据：

- **提示重复率**：有多少请求的提示前缀或完整提示完全相同？重复率超过20%时，缓存效果显著。
- **复杂度需求**：任务是否需要大模型（如复杂推理、代码生成）？还是小模型（如分类、摘要）足够？
- **延迟敏感度**：用户是否等待实时响应？还是可以接受异步批处理？

审计结果直接决定优化优先级。

### 第二步：启用提示缓存

**API级缓存**：如果使用OpenAI、Anthropic等托管API，检查是否支持自动提示缓存。OpenAI的`prompt caching`功能在2025年已普遍可用，对重复前缀自动打折。AWS Bedrock也支持按需端点的提示缓存。

**自建缓存**：使用vLLM部署开源模型时，启用`--enable-prefix-caching`。vLLM会自动缓存公共前缀的KV缓存，对多轮对话或固定系统提示的场景特别有效。部署命令示例：

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --enable-prefix-caching --max-model-len 8192
```

**本地测试**：Ollama默认支持上下文缓存，重复提示自动复用计算。

### 第三步：实施模型路由

模型路由的核心是“用对的模型处理对的任务”。实现方式有两种：

- **规则路由**：根据提示长度、关键词、任务类型（如分类 vs 生成）硬编码路由逻辑。例如：短文本分类用`Llama-3.2-1B`，代码生成用`Llama-3.1-70B`。
- **智能路由**：使用轻量级分类器（如BERT）预测任务复杂度，动态路由到不同模型。开源项目如`RouteLLM`、`OpenRouter`提供现成方案。

生产建议：先做规则路由，再逐步引入智能路由。路由逻辑本身延迟应低于10ms。

### 第四步：模型量化

量化将模型权重从FP16压缩到INT8或INT4，减少显存占用并加速推理。主流工具：

- **TensorRT-LLM**（NVIDIA GPU）：支持FP8、INT8、INT4量化，配合Triton推理服务器可获得最佳性能。官方提供量化脚本，例如将Llama 3.1 8B量化为INT4：
  ```bash
  python quantize.py --model_dir meta-llama/Llama-3.1-8B-Instruct --dtype float16 --qformat int4_awq --output_dir ./llama_int4
  ```
- **llama.cpp / Ollama**（CPU/GPU混合）：使用GGUF格式，支持Q4_K_M等量化级别。Ollama拉取模型时自动选择量化版本（如`llama3.1:8b-q4_K_M`）。
- **vLLM**：内置AWQ、GPTQ量化支持，加载量化模型时自动优化。

注意：INT4量化在复杂推理任务上可能损失1-3%的准确率，建议先用INT8或FP8。

### 第五步：异步批处理

对延迟不敏感的任务（如离线分析、批量分类），将请求排队后批量推理。vLLM原生支持动态批处理（continuous batching），无需额外配置。Triton推理服务器也支持调度策略。关键参数：`max_num_batched_tokens`和`max_num_seqs`。

### 工具选择速查

| 场景 | 推荐工具 | 关键特性 |
|------|----------|----------|
| 高并发生产环境 | vLLM + TensorRT-LLM | 连续批处理、前缀缓存、量化支持 |
| 本地开发/测试 | Ollama | 一键部署、自动量化、CPU友好 |
| 多模型路由 | RouteLLM / OpenRouter | 基于成本或质量的动态路由 |
| 企业级服务 | NVIDIA Triton | 多框架支持、GPU调度、监控集成 |

## 适合谁

- **AI应用开发者**：需要降低API调用成本或自建推理服务。
- **MLOps/DevOps工程师**：负责推理基础设施的选型和调优。
- **SaaS团队**：LLM推理成本占运营支出大头，急需优化。
- **独立开发者**：预算有限，希望用最小成本跑通产品。

**不适合**：仅使用闭源API且无重复提示的业务（缓存无效）；对模型精度零容忍且无法接受量化的场景（如医疗诊断）。

## 限制和注意事项

- **缓存**：依赖提示重复率；动态提示（如包含时间戳）会破坏缓存。需设计提示模板保持前缀稳定。
- **量化**：INT4量化可能降低长文本生成质量；FP8在H100上原生支持，但旧GPU不支持。量化后需做质量回归测试。
- **模型路由**：增加系统复杂度；路由决策错误可能导致成本上升或质量下降。建议设置兜底策略（如路由失败时回退到大模型）。
- **生产风险**：vLLM的prefix caching在极高并发下可能内存溢出，需设置`max_num_batched_tokens`限制。TensorRT-LLM的量化需要重新编译模型，部署流程变长。
- **成本**：自建推理需要GPU硬件投入，短期可能比API贵。建议先用API缓存和路由优化，再评估自建。

## 我的判断

**优先顺序**：缓存 > 模型路由 > 量化 > 批处理。缓存和路由几乎零成本，适合所有团队立即实施。量化需要模型修改和测试，适合有ML工程能力的团队。批处理是默认选项，vLLM已内置。

**推荐组合**：vLLM + 前缀缓存 + INT8量化 + 规则路由。这套组合在延迟、成本和质量之间平衡最好，且社区成熟度高。如果预算紧张，先用Ollama本地测试量化版本，再迁移到vLLM生产。

**不推荐**：一开始就上TensorRT-LLM + Triton，除非你有专门的GPU集群和MLOps团队。对于大多数团队，vLLM已经足够。

**未来趋势**：模型路由将越来越智能，结合成本和质量的多目标优化会成为标配。缓存技术会扩展到跨请求的语义缓存（而非仅前缀匹配）。量化标准（如FP4）正在统一，工具链会越来越简单。现在开始优化，半年后你的竞争对手可能已经用上这些技术了。

</div>

---

<!-- English Version -->
<div class="lang-en" markdown="1">

## LLM Inference Optimization: Caching, Quantization, and Model Routing for Cost Control

# LLM Inference Optimization: Caching, Quantization, and Model Routing for Cost Control

## What It Is

LLM inference optimization refers to techniques that reduce latency and cost when running models in production—without modifying the underlying model. The key methods covered here are caching, quantization, and model routing, plus supporting techniques like batching, streaming, and adapter-based serving.

## Why It Matters Now

As AI applications scale from prototypes to production, inference costs dominate infrastructure spend. A single high-traffic agent can consume thousands of dollars per month in GPU compute. Meanwhile, latency directly impacts user experience—slow responses kill adoption. The good news: most cost and latency issues can be addressed at the infrastructure and API layer without retraining models or hiring ML engineers.

## Practical Next Steps

1. **Audit your workload.** Categorize requests by prompt repetition rate, complexity, and latency sensitivity. This determines which optimizations apply.

2. **Enable API-level prompt caching.** If your traffic includes repeated or similar prompts (e.g., support chatbots with templated queries), caching can cut costs by 50-80%. AWS and other providers now support prompt caching for on-demand endpoints.

3. **Implement model routing.** Route simple queries to smaller, cheaper models (e.g., 7B or 8B parameter) and complex ones to larger models. A smart router can handle this transparently in <50ms.

4. **Use quantization.** Reduce model precision from FP16 to INT4/INT8 with minimal accuracy loss, cutting memory and compute by 2-4x. Tools like TensorRT-LLM and llama.cpp make this straightforward.

5. **Move latency-tolerant workloads to async batch processing.** Non-real-time tasks (e.g., nightly report generation) can be batched and processed off-peak, using vLLM or Triton for efficient batch inference.

## Risks and Operational Notes

- **Quantization may degrade accuracy** on edge cases—always benchmark on your specific task.
- **Caching works best with deterministic prompts**; variable content or personalization reduces hit rate.
- **Model routing requires careful benchmarking**—routing a complex legal query to a small model can produce bad output.
- **Adapters (LoRA/QLoRA) simplify multi-task serving** but add operational complexity—manage via tools like Predibase or TensorRT-LLM.
- **Open-source inference servers (vLLM, Triton)** give full control but require DevOps effort; managed services (AWS Bedrock, Vertex AI) trade cost for simplicity.

## Who This Is For

Engineering teams building production AI applications—especially indie hackers, SaaS builders, and enterprise AI teams. Not suited for research projects or one-off experiments.

## Take

The highest-impact wins are zero-infrastructure changes: caching and routing. Quantization and batching come next. Start with a workload audit, then apply techniques in priority order—don't optimize what you don't measure. The tools exist today; the bottleneck is operational discipline, not technology.

</div>

---

### 参考来源 / Sources

- [LLM Serving Guide: How to Build Faster Inference for Open-source Models | Rubrik](https://www.rubrik.com/blog/ai/25/guide-how-to-serve-llms-faster-inference)
- [Mastering LLM Techniques: Inference Optimization](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization)
- [Mastering LLM Inference Optimization From Theory to Cost Effective ...](https://www.youtube.com/watch?v=9tvJ_GYJA-o)
- [Accelerating AI Agent Inference & Performance in Production](https://medium.com/@kyeg/accelerating-ai-agent-inference-performance-in-production-874b427cb41b)
- [The AI Inference Optimisation Playbook — Caching, Quantization, and Model Routing in Priority Order - SoftwareSeni](https://www.softwareseni.com/the-ai-inference-optimisation-playbook-caching-quantization-and-model-routing-in-priority-order)
