# Block 目录（12 个内容块）

> 每个 slide 由 2-4 个 blocks 组合而成。单个 block 不能构成一页——那是演讲 PPT 的做法。
> 学习课件必须组合 blocks：用"定义 + 公式 + 要点"或"代码 + 步骤 + 反例"的形式。

---

## Block 总览

| # | Block | 语义角色 | CSS class | 教学色 |
|---|-------|---------|-----------|--------|
| 1 | 定义 | 精确概念 + 术语 | `.block-def` | 🔵 蓝 (What) |
| 2 | 公式 | KaTeX 公式 + 变量说明 | `.block-formula` | 🔵 蓝 (What) |
| 3 | 动机 | 痛点/收益驱动 | `.block-why` | 🟠 橙 (Why) |
| 4 | 例子 | 具体可验证实例 | `.block-example` | 🔵 蓝 |
| 5 | 反例 | 常见错误示范 | `.block-counter` | 🔴 红 (Problem) |
| 6 | 代码 | 代码示例 | `.block-code` | 🟢 绿 (How) |
| 7 | 图示 | 流程图/架构图 | `.block-diagram` | 🟢 绿 (How) |
| 8 | 对比 | 多维度对比表 | `.block-compare` | 🟠 橙 |
| 9 | 步骤 | 1-2-3 操作步骤 | `.block-steps` | 🟢 绿 (How) |
| 10 | 要点 | 重点强调/注意 | `.block-callout` | 🟣 紫 (Tip) |
| 11 | 自测 | 翻转问题卡 | `.block-check` | 🟢 绿 (Solution) |
| 12 | 总结 | 章节总结表 | `.block-summary` | ⚫ 黑 |

---

## 1. 定义 block (`block-def`)

### 用途
引入一个新概念，给精确定义，标注核心术语。

### CSS class
`.block-def`

### 何时使用
- 每个新概念的**首次出现**
- 需要区分"通俗理解"和"精确定义"时
- 与 `block-formula` 配对：先定义概念，再给公式

### HTML snippet

```html
<div class="block-def">
  <span class="term">虚拟内存</span>
  <p>操作系统为每个进程提供的一个<strong>独立的、连续的</strong>地址空间抽象。进程看到的虚拟地址不等于物理内存地址，由 MMU 负责翻译。</p>
</div>
```

### 注意事项
- `term` 是核心术语，会以较大字号展示
- 定义正文不超过 2-3 句话，不要写长段落
- 与 `block-formula` 天然搭配（定义概念 → 公式表达）

---

## 2. 公式 block (`block-formula`)

### 用途
展示数学公式（KaTeX）+ 逐一说明每个变量含义。

### CSS class
`.block-formula`

### 何时使用
- 任何可以用公式**精确表达**的关系
- 需要对方程中每个符号做解释时
- 与 `block-def` 配对效果最好

### HTML snippet

```html
<div class="block-formula">
  <h4>有效访问时间 (Effective Access Time)</h4>
  $$EAT = (1-p) \times T_{\text{mem}} + p \times T_{\text{disk}}$$
  <div class="vars">
    <code>p</code> = 缺页率 &nbsp;|&nbsp;
    <code>T<sub>mem</sub></code> = 内存访问时间 (~100ns) &nbsp;|&nbsp;
    <code>T<sub>disk</sub></code> = 磁盘访问时间 (~10ms)
  </div>
</div>
```

### 注意事项
- 变量说明一定用 `.vars` 包裹
- 使用 `$$...$$` 展示块级公式，`$...$` 用于行内
- 公式块的 `h4` 给出公式名称/用途
- 如果公式很长，用 `\begin{aligned}` 拆分

---

## 3. 动机 block (`block-why`)

### 用途
回答"为什么需要这个东西"——展示痛点（没有它会怎样）和收益（有了它解决了什么）。

### CSS class
`.block-why`

### 何时使用
- 在引入概念之后，**立即**给动机（WWH 模型的 Why 阶段）
- 需要有"对比感"：之前不好，现在好了
- 与 `block-example` 搭配：动机是抽象理由，例子是具象化

### HTML snippet

```html
<div class="block-why">
  <h4>没有虚拟内存会怎样？</h4>
  <p class="pain">❌ 进程 A 的越界写入可能覆盖进程 B 的数据</p>
  <p class="pain">❌ 程序必须全部加载到物理内存才能运行</p>
  <p class="gain">✅ 虚拟内存提供进程间地址空间隔离</p>
  <p class="gain">✅ 按需换页——只需加载正在使用的页面</p>
</div>
```

### 注意事项
- `.pain` 用红色文本，`.gain` 用绿色文本
- 痛点 ≥ 2 个，收益 ≥ 2 个，形成"问题→方案"的张力
- 不要只写抽象的好处，要写**具体的失败场景**

---

## 4. 例子 block (`block-example`)

### 用途
给出一个**具体的、可验证的**实例来阐明概念。

### CSS class
`.block-example`

### 何时使用
- 定义/公式之后，需要具象化理解时
- 实例要有具体数字、具体场景，不要比喻
- 与 `block-counter` 联合使用：正面例子 + 反面典型

### HTML snippet

```html
<div class="block-example">
  <h4>具体例子：游戏加载</h4>
  <p>某 3A 游戏需要加载 <strong>60GB</strong> 纹理资源，但玩家电脑只有 <strong>16GB</strong> 物理内存。操作系统通过虚拟内存，让游戏进程"以为"拥有 60GB 地址空间——实际只将当前场景需要的页面（约 2-4GB）映射到物理内存，其余留在磁盘上的交换文件中。</p>
  <p style="margin-top:6px;font-size:12px;color:var(--text-3)">📊 缺页率 ≈ 0.0001% — 几乎没有性能损失</p>
</div>
```

### 注意事项
- 虚线边框区别于其他 block（表示"示例"的临时感）
- 具体数字比模糊描述好 10 倍
- 保留 `h4` 作为例子标题

---

## 5. 反例 block (`block-counter`)

### 用途
展示常见错误、典型陷阱、不该做的事。

### CSS class
`.block-counter`

### 何时使用
- 某个概念有**高发误解**时
- 代码/设计中有"看起来没问题但实际有坑"的做法
- 与 `block-example` 配对：一个正确例子 + 一个错误例子

### HTML snippet

```html
<div class="block-counter">
  <h4>Belady 异常：分配更多帧 ≠ 缺页更少</h4>
  <p>直觉上，给进程更多物理内存帧应该减少缺页。但对于 <strong>FIFO 页面置换算法</strong>，增加帧数反而可能<strong>增加</strong>缺页次数——这就是 Belady 异常。</p>
  <p style="margin-top:6px;font-size:12px;color:var(--text-3)">📐 引用串: 1,2,3,4,1,2,5,1,2,3,4,5 → 3帧(9次缺页) vs 4帧(10次缺页)</p>
</div>
```

### 注意事项
- CSS 会自动在顶部加"⚠️ 常见错误"标签（`::before` 伪元素）
- 错误内容必须**具体**：什么情况下会发生？后果是什么？
- 红色左边框 + 浅红背景，视觉上很突出

---

## 6. 代码 block (`block-code`)

### 用途
展示代码片段（C/Python/伪代码等），带语法高亮标注。

### CSS class
`.block-code`

### 何时使用
- 展示算法实现、系统调用、配置代码
- 不能只用伪代码——必须给出**可运行的语句**
- 与 `block-steps` 搭配：步骤描述做了什么，代码展示怎么做

### HTML snippet

```html
<div class="block-code">
<span class="cm">/* 触发缺页中断的典型场景 */</span>
<span class="kw">void</span> <span class="fn">handle_page_fault</span>(<span class="kw">uintptr_t</span> vaddr) {
    <span class="kw">pte_t</span> *pte = <span class="fn">walk_page_table</span>(current->pgd, vaddr);
    <span class="kw">if</span> (pte == <span class="kw">NULL</span> || !(*pte & PTE_P)) {
        <span class="kw">struct</span> page *p = <span class="fn">alloc_page</span>();     <span class="cm">// ① 分配物理页</span>
        <span class="fn">read_from_disk</span>(p, swap_offset(vaddr)); <span class="cm">// ② 从磁盘读入</span>
        *pte = <span class="fn">page_to_pfn</span>(p) | PTE_P | PTE_U; <span class="cm">// ③ 建立映射</span>
    }
}
</div>
```

### 注意事项
- 代码块自带深色背景（Catppuccin 风格），不要额外设置背景色
- 使用 `.kw`（keyword）、`.fn`（function）、`.str`（string）、`.cm`（comment）、`.num`（number）做语法标注
- 代码行数控制在 10-20 行为佳，太长影响可读性

---

## 7. 图示 block (`block-diagram`)

### 用途
插入架构图、流程图、数据流图（SVG 或 ASCII art）。

### CSS class
`.block-diagram`

### 何时使用
- 讲解系统架构、数据流动、模块交互关系
- 关系比文字更直观时
- 注意：这不是图表（那是 `block-compare` 用表格），是**结构图**

### HTML snippet

```html
<div class="block-diagram">
  <svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
    <rect x="20" y="50" width="100" height="40" rx="6" fill="var(--surface-2)" stroke="var(--accent)" stroke-width="2"/>
    <text x="70" y="74" text-anchor="middle" font-size="12" fill="var(--text-1)">CPU</text>
    <rect x="160" y="50" width="100" height="40" rx="6" fill="var(--surface-2)" stroke="var(--accent)" stroke-width="2"/>
    <text x="210" y="74" text-anchor="middle" font-size="12" fill="var(--text-1)">MMU</text>
    <rect x="300" y="50" width="100" height="40" rx="6" fill="var(--surface-2)" stroke="var(--accent)" stroke-width="2"/>
    <text x="350" y="74" text-anchor="middle" font-size="12" fill="var(--text-1)">RAM</text>
    <line x1="120" y1="70" x2="158" y2="70" stroke="var(--text-3)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <line x1="260" y1="70" x2="298" y2="70" stroke="var(--text-3)" stroke-width="1.5" marker-end="url(#arrow)"/>
    <text x="140" y="60" text-anchor="middle" font-size="10" fill="var(--text-3)">虚拟地址</text>
    <text x="280" y="60" text-anchor="middle" font-size="10" fill="var(--text-3)">物理地址</text>
    <!-- ... add more elements ... -->
  </svg>
</div>
```

### 注意事项
- SVG 内可以使用 CSS 变量（`var(--accent)` 等），运行时颜色会随主题变化
- 也可以用 `<pre>` ASCII art 做简单图（见 deck.html 参考）
- SVG 图不要太复杂，控制在 3-5 个节点 + 连线

---

## 8. 对比 block (`block-compare`)

### 用途
多维度对比两个或多个概念、方案、算法。

### CSS class
`.block-compare`

### 何时使用
- Compare-Contrast 模型的核心 block
- 任何需要"在几个选项中做选择"的场景
- 对比维度 ≥ 3 个才需要用表格

### HTML snippet

```html
<div class="block-compare">
  <table>
    <tr><th>维度</th><th>分页 (Paging)</th><th>分段 (Segmentation)</th></tr>
    <tr><td>划分单位</td><td>固定大小（4KB）</td><td>可变大小（逻辑段）</td></tr>
    <tr><td>外部碎片</td><td class="win">无</td><td>有</td></tr>
    <tr><td>内部碎片</td><td>有（最后一页）</td><td class="win">无</td></tr>
    <tr><td>程序员可见性</td><td>不可见</td><td class="win">可见（段寄存器）</td></tr>
    <tr><td>共享机制</td><td class="win">页级共享（COW）</td><td>段级共享</td></tr>
    <tr><td>现代 OS 使用</td><td class="win">主机制</td><td>Intel 兼容模式保留</td></tr>
  </table>
</div>
```

### 注意事项
- 用 `.win` 标注某个选项在特定维度上更优（绿色加粗）
- 第一列是维度名，用 `<th>` 标注
- 对比表格支持横向滚动（`overflow-x:auto`）

---

## 9. 步骤 block (`block-steps`)

### 用途
按 1-2-3 顺序展示一个操作流程或算法步骤。

### CSS class
`.block-steps`

### 何时使用
- 3P 模型或 WWH 模型的 How 阶段
- 流程有**明确的先后顺序**
- 每一步有名称 + 一句话说明

### HTML snippet

```html
<div class="block-steps">
  <div class="step">
    <h4>CPU 发出虚拟地址</h4>
    <p><code>mov eax, [0x7fff1234]</code> — 进程认为它在访问内存地址 0x7fff1234</p>
  </div>
  <div class="step">
    <h4>MMU 查询 TLB</h4>
    <p>快表（Translation Lookaside Buffer）缓存了最近使用的虚拟→物理地址映射。命中 → 直接得到物理地址（~1 cycle）</p>
  </div>
  <div class="step">
    <h4>TLB miss → 遍历页表</h4>
    <p>MMU 逐级访问多级页表（x86-64 使用 4 级页表），找到 PTE 获取物理页框号</p>
  </div>
  <div class="step">
    <h4>Page fault → 缺页中断</h4>
    <p>PTE 的 Present 位为 0，触发缺页异常。OS 从磁盘交换区读入页面，更新页表，重新执行指令</p>
  </div>
</div>
```

### 注意事项
- 每个 `.step` 自动编号（圆形绿色数字标签），无需手动写数字
- 步骤 4-6 个为佳，超过 8 个考虑拆成两页
- 每步用 `h4` 给步骤名，`p` 给说明

---

## 10. 要点 block (`block-callout`)

### 用途
突出一个关键洞察、核心要点、注意事项。

### CSS class
`.block-callout`

### 何时使用
- 任何 slide 都可以加一个——它是"老师敲黑板"的教学瞬间
- 放在 slide 底部效果最好：讲了概念/步骤之后，"但最重要的是——"
- 内容应该是一句话能记住的 insight，不要长篇大论

### HTML snippet

```html
<div class="block-callout">
  <p>缺页率从 <strong>0.1% → 0.01%</strong>，EAT 从 10μs → 1μs，性能差距达 <strong>10 倍</strong>。这就是为什么页面置换算法不是"学术玩具"——它在生产环境直接影响用户体验。</p>
</div>
```

### 注意事项
- CSS 自动加"💡 要点"标签（`::before` 伪元素）
- 紫色左边框 + 浅色背景，视觉上与定义/公式区分
- 内容一行到两行最佳，3 行是上限

---

## 11. 自测 block (`block-check`)

### 用途
复习用的翻转问题卡——点击问题，答案展开。

### CSS class
`.block-check`

### 何时使用
- FAQ-Kill 模型的核心 block
- 任何 slide 末尾的"检验理解"环节
- 复习页必须出现的 block

### HTML snippet

```html
<div class="block-check">
  <div class="check-q" onclick="this.classList.toggle('open')">
    Q: 为什么 LRU 几乎不会被直接实现？
  </div>
  <div class="check-a">
    真正的 LRU 需要在每次内存访问时更新链表（O(1) 也是 O，但常量很大），且需要硬件支持访问时间戳。实际 OS 使用 Clock 算法（LRU 的近似），用一个访问位 + 时钟指针实现接近 LRU 的效果，开销极小。
  </div>
</div>
```

### 注意事项
- 点击触发 class toggle（`onclick` 内联），无需外部 JS
- 在同一 slide 中放 2-3 个 `block-check`，形成 FAQ 阵列
- 答案要写清楚**为什么**，不只是"是/否"

---

## 12. 总结 block (`block-summary`)

### 用途
用表格形式总结本章所有关键概念。

### CSS class
`.block-summary`

### 何时使用
- 每章/每课件的**最后一张 slide** 必须用
- 与 `block-check` 搭配（总结表 + 自测问答）
- 表格列：概念名 | 定义 | 关键公式/要点

### HTML snippet

```html
<div class="block-summary">
  <table>
    <tr><th>概念</th><th>定义</th><th>关键公式/要点</th></tr>
    <tr><td>虚拟内存</td><td>进程地址空间的抽象，由 MMU 负责虚实转换</td><td>程序 > RAM 也能运行</td></tr>
    <tr><td>有效访问时间 (EAT)</td><td>考虑缺页代价后的平均内存访问时间</td><td>$$EAT = (1-p)T_{mem} + pT_{disk}$$</td></tr>
    <tr><td>缺页率</td><td>内存访问中触发缺页中断的比例</td><td>$$p = \frac{\text{faults}}{\text{accesses}}$$</td></tr>
    <tr><td>Belady 异常</td><td>FIFO 算法增大帧数反而增加缺页</td><td>仅 FIFO 存在此问题</td></tr>
    <tr><td>TLB</td><td>页表缓存，加速虚拟地址转换</td><td>命中率 > 99% 典型场景</td></tr>
  </table>
</div>
```

### 注意事项
- 表头黑底白字（`background: var(--text-1); color: var(--bg)`），视觉权重高
- 隔行底色（`:nth-child(even)`），增强可读性
- 支持横向滚动
- 不要超过 8 行，概念太多拆成两张总结 slide

---

## Block 组合建议

| 目标 | 推荐组合 | 说明 |
|------|---------|------|
| 引入新概念 | `block-def` + `block-formula` + `block-callout` | 定义 → 公式 → 敲黑板 |
| 讲动机 | `block-why` + `block-example` | 痛点 → 具象化 |
| 讲实现 | `block-steps` + `block-code` | 步骤 → 代码对照 |
| 纠错 | `block-counter` + `block-example` | 错误示范 → 正确做法 |
| 对比选择 | `block-compare` + `block-callout` | 对比表 → 选择建议 |
| 复习 | `block-summary` + `block-check` × 2-3 | 总结表 → 自测 |
| 架构讲解 | `block-diagram` + `block-def` + `block-callout` | 图 → 定义 → 要点 |

---

## 信息密度规则

根据 SKILL.md 的规定：

| 难度 | 每 slide blocks 数 | 原因 |
|------|-------------------|------|
| ⭐ (简单) | 4 blocks | 概念简单，信息可以密集 |
| ⭐⭐ (中等) | 3 blocks | 平衡信息量和理解空间 |
| ⭐⭐⭐ (难) | 2 blocks | 概念难，需要更多空间解释 |

**绝对禁止**：单 block 构成一页 slide。即使是最难的概念（⭐⭐⭐），至少也要配一个 `block-callout` 或 `block-example` 形成 2-block 组合。
