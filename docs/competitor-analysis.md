# GitHub 同类项目竞品分析

> *知己知彼，百战不殆。以下为 2026.06 调研结果。*

## 全景对比

| 项目 | Stars | 覆盖范围 | 与 Opus 对比 |
|------|-------|---------|-------------|
| **dreammis/social-auto-upload** | ⭐9.5K | 多平台视频发布（B站/抖音/TikTok/小红书/快手/视频号） | 🔶 做了 Rubedo 的一半（只发布，不创作） |
| **cyfyifanchen/one-person-company** | ⭐2.7K | 一人公司工具推荐（AI 模型/设计/代码/生产力） | 🔶 资源列表，不是蓝图。我们的"怎么做"，它只是"用什么" |
| **OrangeViolin/content-pipeline** | 新兴 | AI内容管道：一个prompt→多平台发布 | 🔶 概念相似！但没有知识库支撑、没有验证层、面向纯内容分发 |
| **Libr-AI/OpenFactVerification (LOKI)** | ⭐1K+ | 事实核查五步管线 | 🔶 做了 Albedo 的一部分（声明提取+验证），但不支持中文、非跨文档 |
| **IshanRai9/Document-Semantic-Contradiction-Detector** | ⭐0 | 跨文档矛盾检测 7 步 NLI 管道 | 🔶 架构可借鉴，但不支持中文、无 D-S 融合 |
| **bilibili-api-python** | ⭐高 | B站全量 API 封装 | 🟢 可作为 Nigredo 的数据采集轮子 |

## 关键发现

> 🎯 **目前没有项目覆盖「摄入→验证→存储→创作→分发」的完整闭环。**
>
> social-auto-upload 是 Rubedo 最直接的竞品，但它只做了「分发」这一步，前面的「从什么内容分发」完全不管。  
> content-pipeline 概念最近似，但缺乏知识库和验证层，本质是一个 Claude Code Skill。  
> Opus 的护城河在于**五器联动**——单个工具可以被替代，整个飞轮难以复制。

## 可借用的轮子

| 轮子 | 用途 | 对应子项目 |
|------|------|-----------|
| `dreammis/social-auto-upload` | 多平台发布引擎 | ✨ Rubedo |
| `bilibili-api-python` | B站数据采集（弹幕/评论/UP主） | ⚗️ Nigredo |
| `biliup-rs` | B站视频上传 CLI | ✨ Rubedo |
| LOKI 声明提取管线 | 声明提取 + 核查价值评估 | 🔬 Albedo |
| Document Contradiction NLI | 跨文档矛盾检测架构参考 | 🔬 Albedo |
