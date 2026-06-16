---
name: html-ppt-learning
description: 学习课件生成器 — 先拆解知识再编排幻灯片。8 种教学模型 × 12 个内容块，产出信息密度高、支持 KaTeX 公式、可用于复习的 HTML 培训课件。当用户要做培训材料、课程讲义、知识总结、技术分享课件时使用。
---

# html-ppt-learning — 学习课件生成器

产出**信息密度高、支持数学公式、可用于复习**的 HTML 学习课件。

## 核心铁律（违者重写）

> ### 1. 先拆解，再写作
> 进入 Phase 2 前，**必须**为每个 subtopic 输出知识卡片。卡片 7 个维度缺一不可。
>
> ### 2. 先选模型，再选 blocks
> 根据知识类型从 8 个教学模型中选择。不允许不选模型就堆 blocks。
>
> ### 3. 每 slide ≥ 2 blocks
> 单个 block 不能构成一页——那是演讲 PPT 的做法。学习课件必须组合。
>
> ### 4. 公式必须用 KaTeX
> `$...$` 行内，`$$...$$` 块公式。**禁止**纯文本表示数学公式。
>
> ### 5. 必须有复习页
> 课件末尾必须有 `review-final.html`（全知识点表 + 公式汇总 + 自测 FAQ）。
>
> ### 6. 侧栏不可省略
> 每页左侧必须显示知识导图 + 当前位置高亮。

---

## 工作流程

### Phase 1: 知识拆解

拿到课件主题后，先确定 subtopic 列表（通常 3-6 个），然后**为每个 subtopic 输出一张知识卡片**：

```markdown
## 知识卡片: [概念名]

| 维度 | 内容 |
|------|------|
| 一句话定义 | （≤40 字，能被路人看懂） |
| 数学公式 | $$...$$ （如适用，无则写"不适用"） |
| 为什么需要它 | （解决了什么痛点？没有它会怎样？） |
| 常见误解 | （新手最容易搞错的一个点） |
| 前置知识 | （必须先懂什么才能理解它） |
| 一个例子 | （具体、可验证的例子——不是比喻） |
| 关联概念 | （和本课件中哪些其他 subtopic 有关系？什么关系？） |
| 难度 | ⭐ / ⭐⭐ / ⭐⭐⭐ |
```

**所有卡片通过后**才能进入 Phase 2。不允许跳过。

### Phase 2: 课件编排

#### Step 1: 选模型

根据知识卡片的内容特征，从以下 8 个模型中选择主导模型（一个课件可混合多个，但主模型只一个）：

| # | 模型 | 结构 | 何时用 |
|---|------|------|--------|
| 1 | **WWH** | What → Why → How | 介绍"XX是什么"——概念、工具、理论 |
| 2 | **Problem-First** | 痛点 → 探索 → 解法 → 反思 | "我们遇到了一个难题"——工程方案、算法设计 |
| 3 | **Layered Reveal** | 全景 → 拆解 → 连接 → 回归全景 | "XX系统怎么设计的"——架构、框架 |
| 4 | **Case-Driven** | 案例 → 分析 → 提炼理论 → 推广 | "从XX案例中学到什么"——商业、法律、历史 |
| 5 | **Compare-Contrast** | 论点A → 论点B → 合题 | "XX和YY到底有什么区别"——易混淆概念 |
| 6 | **3P** | Principle → Practice → Pitfalls | "怎么上手XX"——技能、编程、操作 |
| 7 | **Timeline** | 起源 → 演进 → 转折点 → 现状 | "XX怎么发展到今天的"——技术史、学科史 |
| 8 | **FAQ-Kill** | 问题 → 答案 → 为什么 → 常见错误 | "关于XX最常见的N个问题"——考前复习、扫盲 |

详见 [references/learning-models.md](references/learning-models.md)。

#### Step 2: 选 blocks

每个 slide 由 2-4 个 blocks 组合而成。Block 列表：

| # | Block | 语义 | CSS class |
|---|-------|------|-----------|
| 1 | 定义 | 概念精确定义 + 术语标注 | `.block-def` |
| 2 | 公式 | KaTeX 公式 + 变量逐一说明 | `.block-formula` |
| 3 | 动机 | 为什么需要它 | `.block-why` |
| 4 | 例子 | 具体可验证的实例 | `.block-example` |
| 5 | 反例 | 常见错误/不该怎么做 | `.block-counter` |
| 6 | 代码 | 代码示例 | `.block-code` |
| 7 | 图示 | 架构图/流程图(Mermaid) | `.block-diagram` |
| 8 | 对比 | 多维度对比表 | `.block-compare` |
| 9 | 步骤 | 1-2-3 操作步骤 | `.block-steps` |
| 10 | 要点 | 重点/注意事项 | `.block-callout` |
| 11 | 自测 | 翻转问题卡 | `.block-check` |
| 12 | 总结 | 章节总结表 | `.block-summary` |

详见 [references/blocks-catalog.md](references/blocks-catalog.md)。

#### Step 3: 编排 slide 序列

根据模型的 slide 序列 + 每 slide 的 block 组合，生成完整 deck。

**信息密度规则：**
- ⭐ 难度 → 4 blocks/slide（概念简单，信息可以密集）
- ⭐⭐ 难度 → 3 blocks/slide
- ⭐⭐⭐ 难度 → 2 blocks/slide（概念难，需要更多空间解释）

---

## 快速开始

### 1. 脚手架

从 `templates/deck.html` 复制到你的输出目录：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>课件标题</title>
<link rel="stylesheet" href="../assets/fonts.css">
<link rel="stylesheet" href="../assets/base.css">
<link rel="stylesheet" href="../assets/themes/learning-light.css" id="theme-link">
<!-- KaTeX -->
<link rel="stylesheet" href="../assets/katex/katex.min.css">
<script src="../assets/katex/katex.min.js"></script>
<script src="../assets/katex/auto-render.min.js"></script>
<script>
// Blocking KaTeX render — must complete BEFORE Chrome --print-to-pdf snapshot
(function(){if(typeof renderMathInElement!=="undefined"){renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});}})();
</script>
</head>
<body class="lrn-deck" data-themes="learning-light,learning-dark,learning-print,learning-colorful">
<div class="deck">
  <!-- slides go here -->
</div>
<script src="../assets/runtime.js"></script>
</body>
</html>
```

### 2. 写 slide

每个 slide 使用 `.lrn-2` / `.lrn-3` / `.lrn-4` 控制列数（对应 2/3/4 个 blocks）：

```html
<section class="slide lrn-3">
  <aside class="lrn-sidebar">
    <!-- 知识导图侧栏 ← 每页必含 -->
  </aside>
  <div class="lrn-main">
    <div class="block-def">...</div>
    <div class="block-formula">...</div>
    <div class="block-callout">...</div>
  </div>
</section>
```

### 3. 侧栏模板（每页复制，更新 current 位置）

```html
<aside class="lrn-sidebar">
  <div class="lrn-toc">
    <div class="lrn-chapter">第1章 · 虚拟内存</div>
    <ul class="lrn-tree">
      <li class="done">虚拟内存
        <ul>
          <li class="done current">概念定义</li>
          <li>为什么需要</li>
          <li>实现原理</li>
        </ul>
      </li>
      <li>页面置换</li>
      <li>TLB</li>
    </ul>
  </div>
  <div class="lrn-formula-ref">
    <div class="lrn-formula-title">📐 本节公式</div>
    $$EAT = (1-p) \times T_{mem} + p \times T_{disk}$$
  </div>
</aside>
```

### 4. 复习页（课件末尾必须包含）

```html
<section class="slide lrn-review">
  <h2>📋 本章总结</h2>
  <div class="block-summary">...</div>
  <div class="block-formula">...</div>
  <div class="block-check">...</div>
</section>
```

---

## 主题

| 主题 | CSS 文件 | 适合场景 |
|------|---------|---------|
| `learning-light` | `assets/themes/learning-light.css` | **默认** — 白天阅读 |
| `learning-dark` | `assets/themes/learning-dark.css` | 夜间/暗色模式 |
| `learning-print` | `assets/themes/learning-print.css` | 打印/PDF 导出 |
| `learning-colorful` | `assets/themes/learning-colorful.css` | 教学投影/直播 |

---

## 键盘导航

```
← → Space PgUp PgDn   导航
F                      全屏
O                      幻灯片概览
T                      切换主题
```

---

## 参考文档

- [references/learning-models.md](references/learning-models.md) — 8 个模型的详细说明 + slide 序列模板
- [references/blocks-catalog.md](references/blocks-catalog.md) — 12 个 block 的 HTML 结构 + CSS
- [references/math-formulas.md](references/math-formulas.md) — KaTeX 常用公式速查

---

## 文件结构

```
html-ppt-learning/
├── SKILL.md
├── assets/
│   ├── base.css             ← 学习专用 token 系统
│   ├── fonts.css
│   ├── runtime.js           ← 键盘导航 + KaTeX 渲染
│   └── themes/              ← 4 个学习主题
├── templates/
│   ├── deck.html            ← 课件骨架
│   ├── blocks/              ← 12 个 block HTML 片段（参考用）
│   ├── slides/              ← 8 个模型的示例 slide
│   └── shell/               ← chapter-cover + review-final
├── references/              ← 3 个参考文档
└── examples/                ← 示例课件
```
