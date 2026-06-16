# 学习模型参考（8 种教学模型）

> 在编排课件 slide 序列之前，**必须先选择主导模型**。一个课件可以混合多个模型，但主模型只能有一个。
> 选择模型的依据是：知识卡片的内容特征、目标受众、以及你想让学生形成的认知结构。

---

## 模型总览

| # | 模型 | 一句话 | 代表人物 |
|---|------|--------|----------|
| 1 | **WWH** | "什么东西、为什么需要、怎么实现" | 经典教学法 |
| 2 | **Problem-First** | "痛点驱动：先砸问题再给解法" | 工程培训 |
| 3 | **Layered Reveal** | "上帝视角 → 拆解 → 再拼回去" | 架构讲解 |
| 4 | **Case-Driven** | "从一个真实案例中提炼出一般规律" | 哈佛案例法 |
| 5 | **Compare-Contrast** | "正反对照，在对比中建立辨别力" | 辩证法 |
| 6 | **3P** | "原理 → 实操 → 踩坑指南" | 技能教学 |
| 7 | **Timeline** | "沿着时间线讲一个东西怎么发展到今天" | 技术史 |
| 8 | **FAQ-Kill** | "用问题轰开认知壁垒" | 考前冲刺 |

---

## 1. WWH 模型

### 结构

```
What（概念定义）
  ↓
Why（为什么需要 / 解决了什么痛点）
  ↓
How（怎么实现的 / 怎么用）
```

### 何时使用

- 介绍一个**新概念**、**新工具**、**新理论**（如"虚拟内存"、"Git 暂存区"、"RESTful API"）
- 受众对此概念**几乎零基础**
- 知识的结构是"定义 → 动机 → 方法"的线性关系

### 典型 slide 序列（以"虚拟内存"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-3` | 什么是虚拟内存 | block-def + block-formula + block-callout |
| 3 | `lrn-2` | 为什么需要虚拟内存 | block-why + block-example |
| 4 | `lrn-4` | 工作原理（4步） | block-steps + block-diagram + block-code + block-callout |
| 5 | `lrn-2` | 常见误解 | block-counter + block-compare |
| 6 | `lrn-review` | 本章复习 | block-summary + block-check |

### 常用 blocks

`block-def`, `block-formula`, `block-why`, `block-steps`, `block-diagram`, `block-callout`, `block-counter`

---

## 2. Problem-First 模型

### 结构

```
痛点（真实场景中的失败 / 灾难 / 性能瓶颈）
  ↓
探索（试了几个方案，为什么不行）
  ↓
解法（最终方案 + 核心洞察）
  ↓
反思（为什么这个方案是"对的"，边界在哪里）
```

### 何时使用

- 讲解**工程方案选择**、**算法设计决策**、**架构演进**
- 受众有一定基础，想要理解"为什么这样做而不是那样做"
- 知识的核心是"在约束条件下做权衡决策"

### 典型 slide 序列（以"页面置换算法选择"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-2` | 痛点：内存不够用 | block-why + block-example |
| 3 | `lrn-3` | 探索：FIFO 失败案例 | block-code + block-counter + block-diagram |
| 4 | `lrn-4` | 解法：LRU + Clock | block-def + block-steps + block-example + block-callout |
| 5 | `lrn-2` | 对比：各算法适用场景 | block-compare + block-summary |
| 6 | `lrn-review` | 复习 | block-summary + block-check |

### 常用 blocks

`block-why`, `block-example`, `block-counter`, `block-steps`, `block-compare`, `block-callout`

---

## 3. Layered Reveal 模型

### 结构

```
全景（鸟瞰图：整个系统长什么样，有哪些层/模块）
  ↓
拆解（一层一层剥开，每层讲清楚职责和接口）
  ↓
连接（层与层之间怎么交互，数据怎么流动）
  ↓
回归全景（再看鸟瞰图，这次你能看懂每一块了）
```

### 何时使用

- 讲解**复杂系统**、**架构设计**、**框架源码**（如"Linux 内核内存管理"、"浏览器渲染流水线"）
- 受众需要**建立整体 mental model**，不能只见树木不见森林
- 知识是**层级结构**，层与层之间有明确的接口

### 典型 slide 序列（以"Linux 内存管理全景"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-full` | 全景图：5 层架构 | block-diagram + block-def |
| 3 | `lrn-3` | 第 1 层：物理内存管理 | block-def + block-code + block-callout |
| 4 | `lrn-3` | 第 2 层：虚拟内存 | block-def + block-formula + block-diagram |
| 5 | `lrn-2` | 第 3 层：页面置换 | block-steps + block-compare |
| 6 | `lrn-2` | 层间交互：缺页中断流程 | block-diagram + block-steps |
| 7 | `lrn-full` | 回归全景：这次你能看懂 | block-diagram + block-summary |
| 8 | `lrn-review` | 复习 | block-summary + block-check |

### 常用 blocks

`block-diagram`, `block-def`, `block-steps`, `block-code`, `block-formula`, `block-callout`

---

## 4. Case-Driven 模型

### 结构

```
案例（讲一个真实的故事，包含足够的细节）
  ↓
分析（从案例中抽象出关键变量 / 决策点 / 模式）
  ↓
提炼理论（上升为可迁移的原则 / 框架 / 公式）
  ↓
推广（用这个理论去解另一个类似的案例）
```

### 何时使用

- 讲解**需要判断力的主题**（如"什么场景用哪种页面置换算法"）
- 案例本身有**戏剧性**（失败代价大、转折明显、结果出乎意料）
- 受众需要**迁移能力**——学一个案例，能解决同类问题

### 典型 slide 序列（以"某电商大促内存 OOM 事故"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-3` | 案例：事故经过 | block-def + block-diagram + block-example |
| 3 | `lrn-3` | 分析：根因定位 | block-steps + block-code + block-callout |
| 4 | `lrn-2` | 提炼：内存管理的 5 条原则 | block-summary + block-why |
| 5 | `lrn-2` | 推广：另一个场景的应用 | block-example + block-check |
| 6 | `lrn-review` | 复习 | block-summary + block-check |

### 常用 blocks

`block-def`, `block-example`, `block-steps`, `block-code`, `block-summary`, `block-callout`

---

## 5. Compare-Contrast 模型

### 结构

```
论点A（完整阐述方案/概念 A）
  ↓
论点B（完整阐述方案/概念 B，用和 A 相同的维度）
  ↓
合题（在什么场景下 A 优于 B？什么场景下 B 优于 A？有没有超越二者的第三条路？）
```

### 何时使用

- 讲解**易混淆概念**（如"分段 vs 分页"、"LRU vs LFU"、"进程 vs 线程"）
- 受众**已经分别知道 A 和 B**，但不能区分何时用哪个
- 目标是建立**辨别力**而非引入新概念

### 典型 slide 序列（以"分页 vs 分段"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-3` | 分页（Paging） | block-def + block-formula + block-diagram |
| 3 | `lrn-3` | 分段（Segmentation） | block-def + block-formula + block-diagram |
| 4 | `lrn-2` | 多维度对比表 | block-compare + block-callout |
| 5 | `lrn-3` | 合题：现代 OS 用页式 + 段页式 | block-def + block-example + block-check |
| 6 | `lrn-review` | 复习 | block-summary + block-check |

### 常用 blocks

`block-def`, `block-formula`, `block-diagram`, `block-compare`, `block-example`, `block-callout`

---

## 6. 3P 模型

### 结构

```
Principle（原理 —— 为什么要这样做，底层机制是什么）
  ↓
Practice（实践 —— 具体怎么做，给出可复制的步骤）
  ↓
Pitfalls（踩坑指南 —— 新手常犯的错误 + 如何避免）
```

### 何时使用

- 讲解**操作型知识**：手写代码、配置工具、调试技巧
- 目标是**能动手做**，而不仅仅是"知道"
- 实践环节必须有**具体的、可验证的例子**（不是比喻）

### 典型 slide 序列（以"用 /proc/meminfo 排查内存泄漏"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-3` | Principle：/proc/meminfo 的数据来源 | block-def + block-diagram + block-why |
| 3 | `lrn-2` | Practice：一步步排查 | block-steps + block-code |
| 4 | `lrn-2` | Practice：解读输出 | block-example + block-callout |
| 5 | `lrn-2` | Pitfalls：3 个常见误判 | block-counter + block-compare |
| 6 | `lrn-review` | 复习 | block-summary + block-check |

### 常用 blocks

`block-def`, `block-steps`, `block-code`, `block-example`, `block-counter`, `block-callout`

---

## 7. Timeline 模型

### 结构

```
起源（问题最初是怎么产生的，当时的约束条件）
  ↓
演进（每个阶段解决了什么问题，又引入了什么新问题）
  ↓
转折点（关键论文 / 技术突破 / 范式转移）
  ↓
现状（现在的主流方案 + 前沿方向）
```

### 何时使用

- 讲解**技术发展史**（如"Linux 调度器演变"、"JavaScript 模块化演进"）
- 受众有一个**模糊的认知**，但不知道这些技术"为什么要这样演进"
- 目标是理解"现状是历史约束的产物"——每个设计决策都有历史原因

### 典型 slide 序列（以"Linux 内存管理子系统演进"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-2` | 起源：早期 Linux 的内存管理 | block-def + block-why |
| 3 | `lrn-3` | 演进 1：引入虚拟内存（2.x） | block-def + block-formula + block-callout |
| 4 | `lrn-3` | 演进 2：NUMA 支持（2.6） | block-diagram + block-example + block-compare |
| 5 | `lrn-3` | 转折点：透明大页 THP（3.x） | block-def + block-why + block-counter |
| 6 | `lrn-2` | 现状：多代页面回收 + MGLRU | block-summary + block-check |
| 7 | `lrn-review` | 复习时间线 | block-summary + block-check |

### 常用 blocks

`block-def`, `block-why`, `block-diagram`, `block-compare`, `block-callout`, `block-counter`

---

## 8. FAQ-Kill 模型

### 结构

```
问题 1 → 答案 → 为什么这个答案是对的 → 常见的错误答案和原因
  ↓
问题 2 → 答案 → 为什么 → 常见错误
  ↓
...（通常 5-8 个问题）
```

### 何时使用

- **考前复习**、**面试准备**、**知识扫盲**
- 受众已经有碎片化认知，需要**系统化纠错**
- 每个问题都是"高频误解点"——问得越犀利越好

### 典型 slide 序列（以"内存管理高频面试题"为例）

| Slide | 布局 | 内容 | Blocks |
|-------|------|------|--------|
| 1 | `lrn-cover` | 封面 | — |
| 2 | `lrn-2` | Q1-Q2：基础概念辨析 | block-check × 2 |
| 3 | `lrn-2` | Q3-Q4：公式与计算 | block-check + block-formula |
| 4 | `lrn-3` | Q5-Q7：场景题 | block-check × 3 |
| 5 | `lrn-review` | 错题汇总 | block-summary + block-check |

### 常用 blocks

`block-check`, `block-formula`, `block-counter`, `block-def`, `block-callout`

---

## 混合使用

一个课件可以混合多个模型。例如：

- 主线用 **WWH** 引入虚拟内存，中间插入 **Problem-First** 讲页面置换算法选择
- 主线用 **Layered Reveal** 讲内核架构，末尾用 **FAQ-Kill** 做复习

**原则**：主模型决定 slide 序列的**骨架**，辅模型只影响特定 slide 的内部编排。

---

## 模型选择决策树

```
知识的结构是？
  ├─ "定义 → 动机 → 实现"   → WWH
  ├─ "一个问题驱动的探索过程" → Problem-First
  ├─ "层级系统全景图"        → Layered Reveal
  ├─ "从一个故事到一般规律"   → Case-Driven
  ├─ "A vs B，何时用哪个"    → Compare-Contrast
  ├─ "动手做 + 踩坑"          → 3P
  ├─ "历史演进脉络"           → Timeline
  └─ "高频 Q&A 纠错"         → FAQ-Kill
```
