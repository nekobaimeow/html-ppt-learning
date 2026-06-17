---
name: html-ppt-learning
description: 学习课件生成器 — 先拆解知识再编排幻灯片。8 种教学模型 × 12 个内容块，产出信息密度高、支持 KaTeX 公式、可用于复习的 HTML 培训课件。当用户要做培训材料、课程讲义、知识总结、技术分享课件时使用。
version: 1.0.0
category: creative
---

# html-ppt-learning — 学习课件生成器

产出**信息密度高、支持数学公式、可用于复习**的 HTML 学习课件。

## 核心铁律（违者重写）

1. **先拆解，再写作。** 必须为每个 subtopic 输出 7 维知识卡片（定义/公式/动机/误解/前置/例子/关联）。缺一项不可进入 Phase 2。
2. **先选模型，再选 blocks。** 根据知识类型从 8 个教学模型中选择。不允许不选模型就堆 blocks。
3. **每 slide ≥ 2 blocks。** 单个 block 不能构成一页——那是演讲 PPT 的做法。
4. **公式必须用 KaTeX。** `$...$` 行内，`$$...$$` 块公式。禁止纯文本表示数学公式。
5. **必须有复习页。** 课件末尾必须有 review-final（全知识点表 + 公式汇总 + 自测 FAQ）。
6. **侧栏不可省略。** 每页左侧必须显示知识导图 + 当前位置高亮。

## 工作流程

### Phase 1: 知识拆解

为每个 subtopic 输出知识卡片：

```markdown
## 知识卡片: [概念名]

| 维度 | 内容 |
|------|------|
| 一句话定义 | （≤40 字） |
| 数学公式 | $$...$$ （如适用） |
| 为什么需要它 | （解决什么痛点） |
| 常见误解 | （新手最容易搞错的点） |
| 前置知识 | （必须先懂什么） |
| 一个例子 | （具体可验证） |
| 关联概念 | （和本课件中哪些其他 subtopic 相关） |
| 难度 | ⭐ / ⭐⭐ / ⭐⭐⭐ |
```

**所有卡片通过后**才能进入 Phase 2。

### Phase 2: 课件编排

**Step 1: 选模型**（8 选 1，根据知识类型）

| # | 模型 | 结构 | 何时用 |
|---|------|------|--------|
| 1 | WWH | What → Why → How | "XX 是什么"——概念、工具、理论 |
| 2 | Problem-First | 痛点 → 探索 → 解法 → 反思 | "我们遇到了一个难题"——工程方案 |
| 3 | Layered Reveal | 全景 → 拆解 → 连接 → 回归 | "XX 系统怎么设计"——架构 |
| 4 | Case-Driven | 案例 → 分析 → 理论 → 推广 | "从 XX 案例学什么"——商业/法律/历史 |
| 5 | Compare-Contrast | 论点A → 论点B → 合题 | "XX 和 YY 有什么区别"——辨析 |
| 6 | 3P | Principle → Practice → Pitfalls | "怎么上手 XX"——技能培训 |
| 7 | Timeline | 起源 → 演进 → 转折点 → 现在 | "XX 怎么发展到今天"——技术史 |
| 8 | FAQ-Kill | 问题 → 答案 → 为什么 → 常见错误 | "关于 XX 最常见的 N 个问题" |

**Step 2: 选 blocks**（12 种，每 slide 组合 2-4 个）

| Block | CSS class | 语义 |
|-------|-----------|------|
| 定义 | `.block-def` | 概念精确定义 |
| 公式 | `.block-formula` | KaTeX + 变量说明 |
| 动机 | `.block-motivation` | 为什么需要它 |
| 例子 | `.block-example` | 具体实例 |
| 反例 | `.block-counter` | 常见错误 |
| 代码 | `.block-code` | 代码示例 |
| 图示 | `.block-diagram` | 架构图/流程图 |
| 对比 | `.block-compare` | 多维度对比表 |
| 步骤 | `.block-steps` | 1-2-3 操作步骤 |
| 要点 | `.block-callout` | 重点/注意事项 |
| 自测 | `.block-check` | 翻转问题卡 |
| 总结 | `.block-summary` | 章节总结表 |

**Step 3: 编排** — ⭐→4 blocks, ⭐⭐→3 blocks, ⭐⭐⭐→2 blocks

## 主题

| 主题 | CSS 文件 | 适合 |
|------|---------|------|
| `learning-light` | `assets/themes/learning-light.css` | **默认** 白天阅读 |
| `learning-dark` | `assets/themes/learning-dark.css` | 夜间/暗色 |
| `learning-print` | `assets/themes/learning-print.css` | 打印/PDF |
| `learning-colorful` | `assets/themes/learning-colorful.css` | 教学投影 |

## 部署

详见 [references/deployment.md](references/deployment.md) — Hub 部署、nginx 权限、deck 静态文件路由。

### Hub 部署（多课件分类门户 · 自动发现模式）

Hub `server.py` v2 支持**自动发现**——扫描 `decks/*/*/deck.json` 自动构建目录，**不再需要手动编辑 `categories.json`**。

**每个课件的自描述结构：**
```
decks/<category>/<slug>/
├── index.html
├── images/
│   └── *.jpg
└── deck.json          ← 课件元数据：title, category, difficulty (int 1-3), slides, description, tags

decks/<category>/
└── category.json      ← 分类元数据：name, icon
```

**部署只需三步**（详见 [references/hub-deploy-workflow.md](references/hub-deploy-workflow.md)）：
1. SCP 上传 HTML + 图片
2. 同时上传 `deck.json` + `category.json`（或在本地先写入 deck 目录）
3. 修复目录权限（nginx `o+x`）→ **60 秒内首页自动出现**

不再需要拉取/编辑/推送 `categories.json`。

- **nginx 反代**：80 → 127.0.0.1:9210，`/shared/` 直接走 nginx 静态文件
- **systemd**：`html-ppt-hub.service` 守护 server.py，挂了自动拉起
- **权限**：nginx 以 `www-data` 运行，需 `chmod o+x /home/ubuntu/` 允许目录遍历
- **auto-reload**：后台线程每 60 秒重扫 `decks/`，新增课件自动上线
- **手动重载**：`POST /reload` 立即触发扫描
- 课件内 `../../assets/` 自动重写为 `/shared/assets/`（regex，任何深度适配）

当前公网实例：`http://114.132.53.150/`（80 端口，nginx → 9210）。

## Pitfalls

### ❌ KaTeX 渲染脚本放 `<head>` → `document.body` 为 null，公式不渲染

**症状**：PDF 显示原始 `$公式$` 文本，`renderMathInElement` 静默失败。

**根因**：`<head>` 中的脚本执行时 `document.body` 尚未被浏览器解析，为 `null`。`renderMathInElement(null, ...)` 是空操作，不报错。

**正解**：渲染脚本必须放在 `</body>` 之前，DOM 构建完成后执行：

```html
<!-- ✅ 正确位置：</body> 前 -->
<script>
(function(){if(typeof renderMathInElement!=="undefined"){renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});}})();
</script>
</body>
```

### ❌ Deck内图片 404 → server.py 没走 decks/ 前缀

**症状**：课件中的 `<img src="images/img_01.jpg">` 返回 404。URL 是 `/photography/photography-basics/images/img_01.jpg`，但文件实际在 `HUB_ROOT/decks/photography/photography-basics/images/img_01.jpg`。

**根因**：`server.py` 的静态文件处理器直接用裸路径拼到 `HUB_ROOT`，缺少 `decks/` 前缀。`serve_deck_page()` 方法内部加了这个前缀，但通用静态文件路由没有。

**正解**：在 `server.py` 的静态文件 404 回退处加 `decks/` fallback：

```python
if not os.path.isfile(result):
    # Fallback: try under decks/ for deck-local static files
    fallback = os.path.normpath(os.path.join(HUB_ROOT, 'decks', path))
    if fallback.startswith(HUB_ROOT + os.sep) and os.path.isfile(fallback):
        result = fallback
    else:
        self.send_error(404, 'Not found')
        return
```

课件中引用图片直接用相对路径（`images/img_01.jpg`），不需加 `decks/` 前缀。

### ❌ 不要用 CDN KaTeX

项目 `assets/katex/` 已包含本地 KaTeX（432KB），用相对路径引用：
```html
<link rel="stylesheet" href="../../assets/katex/katex.min.css">
<script src="../../assets/katex/katex.min.js"></script>
<script src="../../assets/katex/auto-render.min.js"></script>
```

详见 [references/deployment.md](references/deployment.md)。

### ❌ LAN 其他设备无法访问 WSL2 HTTP 服务 → 缺 portproxy 转发

**症状**：`python3 -m http.server 8899` 在 WSL 里跑，Windows 本机 `localhost:8899` 通的，但 LAN 上其他设备访问 `192.168.x.x:8899` 超时。

**根因**：WSL2 运行在 NAT 后面（IP `172.x.x.x`），外部流量到的是 Windows 物理网卡，上面没进程监听 8899。需要 `netsh interface portproxy` 做转发。

**正解**：两步——netsh portproxy + 防火墙放行。详见 [references/deployment.md](references/deployment.md)。

### ❌ PDF 页面下半截空白 → A4 landscape + 垂直居中

**症状**：每页只用了上半截，下半截全白。内容堆在顶部。

**根因**：
1. `@page { size: A4 portrait }` — 纵向比例完全不对
2. base.css 残留 `@media print { .slide { min-height: auto } }` — 导致 slide 高度只撑到内容
3. `.lrn-2, .lrn-3 { align-content: start }` — 内容贴顶

**正解 — 完整的 `learning-print.css` 配置：**

```css
@media print {
  @page { size: A4 landscape; margin: 0 }
  html, body { margin: 0; padding: 0; width: 100%; height: 100% }
  .deck { max-width: 100%; margin: 0; padding: 0 }

  /* 所有 slide：固定最小高度 + 垂直居中 */
  .slide {
    display: grid !important;
    min-height: 595pt;                      /* A4 landscape 页高 */
    padding: 32px 40px;
    page-break-after: always;
    page-break-inside: avoid;
    break-inside: avoid-page;
  }
  .slide.lrn-2, .slide.lrn-3, .slide.lrn-4 { align-content: center }
  .slide.lrn-cover { min-height: 595pt; align-content: center }

  /* 总结页：不限制高度，允许跨页 */
  .slide.lrn-review { page-break-inside: auto; break-inside: auto }
}
```

**关键**：必须从 base.css 中**完全删除**所有 `@media print` 规则，否则和 learning-print.css 冲突。

### ❌ PDF 页数翻倍（18-19 页而非 9 页）→ runtime.js overview 网格被打印

**症状**：每个 slide 出现两次——一次是正常内容，一次带 "Slide N" 标签的副本。

**根因**：`runtime.js` 在 `document.body` 注入 `.overview` 容器，内含 `.mini-slide` 克隆（class=`slide is-active`）。打印 CSS 的 `.slide { display: grid !important }` 把克隆也激活了。即使父容器 `.overview` 是 `display: none`，子元素的 `display: grid !important` 在 Chrome 打印中可能覆盖父级隐藏。

**正解**：打印 CSS 中显式 kill 所有 UI chrome：

```css
@media print {
  .overview, .overview .slide, .overview *,   /* overview 网格 + 内部克隆 */
  .progress-bar, .notes-overlay, .slide-number /* 其他 UI chrome */
  { display: none !important }
}
```

### ❌ 用 `display: grid !important` 做打印布局 → 每页分裂为 2 页

**症状**：每个 slide 在 PDF 中正好占 2 页——内容在页 1 居中，页 2 几乎空白。

**根因**：`display: grid` + `min-height: 595pt` + `align-content: center` 组合在 Chrome 打印引擎中，当内容超出可视化区域时，grid 在第二页创建新上下文。`page-break-after: always` 然后应用于原本的 slide，导致每个 slide 变成 2 个物理页。

**正解**：打印时使用普通块流布局，不用 grid：
```css
.slide { max-height: 595pt; overflow: hidden !important; contain: layout paint; }
```
不要 `display: grid !important`，不要 `min-height: 595pt`，不要 `align-content: center`。

### 🔍 PDF 布局验证方法

验证页数是否匹配幻灯片数：

```bash
python3 -c "
import fitz
doc = fitz.open('output.pdf')
expected = 9  # 你的幻灯片数
actual = len(doc)
print(f'Pages: {actual} (expected {expected}) — {\"OK\" if actual == expected else \"FAIL\"}')
# 检查页面尺寸
p0 = doc[0]
print(f'Page size: {p0.rect.width:.0f}x{p0.rect.height:.0f}pts (should be ~842x595 for A4 landscape)')
"
```

### ❌ 复习页"公式墙"挡内容 → Chrome 连 inline KaTeX 都撕碎，别修了，删

**症状**：复习页（`.lrn-review`）的公式墙区块中，哪怕用 `$...$` inline 公式，Chrome `--print-to-pdf` 也会把上下标（`_{\text{TLB}}`）撕成独立行。公式碎片覆盖下方 Q&A 内容，把 Q&A 答案挤出页面。

**根因**：KaTeX 对内联公式也用绝对定位的 span 渲染上下标，Chrome 打印引擎不认定位偏移。`$$...$$` display 和 `$...$` inline 都一样碎——**打印 PDF 里必然碎裂，与 CSS 无关**。

**正解**：删掉复习页的公式墙。公式已经在各自 slide 里展示过了。复习页只需：汇总表（表内简单公式用 `$...$` 受影响较小）+ Q&A 自测。

**Q&A 答案必须默认展开**（`class="check-q open"`），否则 PDF 看不到：

```html
<div class="check-q open" onclick="this.classList.toggle('open')">Q: ...</div>
<div class="check-a">答案内容</div>
```

总结页不加高度限制，允许自然溢出到第二页：
```css
.slide.lrn-review { page-break-inside: auto; break-inside: auto; }
```\n\n### 🔍 KaTeX 渲染验证（pymupdf 文本提取不可靠）\n\n`pymupdf.get_text()` 提取的文本中 KaTeX 公式可能显示为碎片（上下标分到独立行），但这**不代表 PDF 视觉渲染有问题**——只是 Chrome PDF 引擎的内部文本流和 pymupdf 的交互方式导致的。\n\n真正可靠的验证：在浏览器（非 headless）打开 HTML 文件，肉眼确认公式显示正常。或截图后用 vision 模型检查。\n\n验证 PDF 中无原始 `$` 残留（表明 KaTeX 至少被执行了）：\n\n```bash\npython3 -c \"\nimport fitz\ndoc = fitz.open('output.pdf')\nfor i in range(len(doc)):\n    if '$' in doc[i].get_text():\n        print(f'Page {i+1}: raw $ found — NOT rendered!')\n\"\n```\n\n## render-pdf.sh 关键配置

```bash
# WSL 环境：通过 powershell.exe 调用 Windows Chrome
powershell.exe -Command "Start-Process -FilePath 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe' \
  -ArgumentList '--headless=new','--disable-gpu','--no-sandbox',\
  '--print-to-pdf=$OUTPUT_WIN','--no-pdf-header-footer','$HTML_URL' \
  -Wait -WindowStyle Hidden"
```

关键 flag：
- `--headless=new`：新版 headless，等 JS 执行完才打印
### 🔍 KaTeX 渲染验证（pymupdf 文本提取不可靠）

`pymupdf.get_text()` 提取的文本中 KaTeX 公式可能显示为碎片（上下标分到独立行），但这**不代表 PDF 视觉渲染有问题**。pymupdf 提取的是 Chrome PDF 引擎的内部文本流，和实际视觉效果不同。

可靠验证：浏览器打开 HTML 肉眼确认，或截图后用 vision 模型检查。

验证 PDF 中无原始 `$` 残留（表明 KaTeX 至少被执行了）：
```bash
python3 -c "
import fitz
doc = fitz.open('output.pdf')
for i in range(len(doc)):
    if '\$' in doc[i].get_text():
        print(f'Page {i+1}: raw \$ found — NOT rendered!')
"
```

### ❌ Deck-local static files (images etc.) return 404 → server.py doesn't look under `decks/`

**症状**：HTML 中 `<img src="images/img_01.jpg">` 在 hub 上返回 404。

**根因**：`server.py` 的静态文件路由直接把 URL path 拼到 `HUB_ROOT` 下查找：
- URL: `/photography/photography-basics/images/img_01.jpg`
- 查找: `HUB_ROOT/photography/photography-basics/images/img_01.jpg` ❌
- 实际: `HUB_ROOT/decks/photography/photography-basics/images/img_01.jpg` ✅

路由缺少 `decks/` 前缀。`serve_deck_page()` 手动加了这个前缀，但静态文件处理走的是另一个分支。

**正解**：在 `server.py` 的文件未找到检查前加 fallback：

```python
if not os.path.isfile(result):
    # Fallback: try under decks/ for deck-local static files
    fallback = os.path.normpath(os.path.join(HUB_ROOT, 'decks', path))
    if fallback.startswith(HUB_ROOT + os.sep) and os.path.isfile(fallback):
        result = fallback
    else:
        self.send_error(404, 'Not found')
        return
```

**注意**：`path` 变量来自 `do_GET` 方法中的 `path = self.path.split('?')[0].lstrip('/')`，非 `is_safe_path` 内部的 `decoded` 变量。

### ❌ 新建课件 CSS/JS 全不生效 → 缺 base.css + fonts.css + data-theme 属性

**症状**：所有 slide 同时展开（无幻灯片模式）、侧栏错位到底部、无导航点、图片无样式。Chrome DevTools Network 显示 CSS/JS 全部 200 OK 但页面完全不正常。

**根因**：
1. 只引用了 `learning-light.css` 和 `learning-print.css`，**没引用 `base.css` 和 `fonts.css`**
2. `<html>` 标签缺少 `data-theme`、`data-themes`、`data-theme-base` 属性

`base.css` 包含核心结构布局（侧栏 flexbox、slide grid 容器、block 样式），`fonts.css` 提供字体。**缺 `base.css` = 整个课件没有骨架。**

**正解 — 课件 `<head>` 完整模板**：

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="learning-light" data-themes="learning-light,learning-dark,learning-print" data-theme-base="../../assets/themes/">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>课件标题</title>
<link rel="stylesheet" href="../../assets/fonts.css">
<link rel="stylesheet" href="../../assets/base.css">
<link rel="stylesheet" id="theme-link" href="../../assets/themes/learning-light.css">
<link rel="stylesheet" media="print" href="../../assets/themes/learning-print.css">
<link rel="stylesheet" href="../../assets/katex/katex.min.css">
<!-- 自定义 deck 样式 -->
</head>
```

**关键：**
| 资源 | 作用 | 缺失后果 |
|------|------|---------|
| `base.css` | 侧栏 · slide 网格 · block 容器 · flexbox 布局 | 全部 slide 展开、侧栏错位 |
| `fonts.css` | Google Fonts 字体（Inter / Noto Sans SC） | 降级到系统字体（可接受） |
| `data-theme` | runtime.js 主题初始化 | 无幻灯片模式 |
| `data-themes` | 可选主题列表 | 主题切换失效 |
| `data-theme-base` | 主题 CSS 路径前缀 | 主题切换 404 |
| `id="theme-link"` | runtime.js 动态换主题的目标 `<link>` | 主题切换失效 |

server.py 的路径重写会自动把 `../../assets/` 转成 `/shared/assets/`（无论 deck 在几层子目录下）。

### ❌ nginx 403 on static files → parent directories lack `o+x`

**症状**：nginx 日志显示 `open() ... failed (13: Permission denied)`，curl 返回 403。

**根因**：nginx 以 `www-data` 用户运行。`/home/ubuntu/` 目录默认权限 `drwxr-x---`，other 无 traverse 权限。即使文件本身 `o+r`，nginx 进不去父目录。

**正解**：
```bash
chmod o+x /home/ubuntu/
find /home/ubuntu/html-ppt-hub -type d -exec chmod o+x {} \;
chmod -R o+r /home/ubuntu/html-ppt-hub/
```

### ❌ 图片与上下文不匹配 → 换流站图配 AC 变电站、绝缘子串配串联补偿

**症状**：用户检查课件时发现图片和文字对不上号——特高压交流页用了直流换流站照片，串联补偿设备配了绝缘子串图。

**根因**：批量生图时每张图只有一个语义，但课件中同一个技术概念在不同 slide 中被重复引用时容易张冠李戴。AI 生成的图片缺乏天然的技术分类标签。

**正解 — 部署前自检三问**：
1. 每张图片的 prompt 是否精确匹配它要展示的概念？（如"串联电容器组"≠"绝缘子串"）
2. AC 交流设备 ≠ DC 直流设备——换流站图不能出现在交流变电站页
3. 同一张图被多个 slide 引用时，每次的 caption 是否对应当前上下文？

**工作流建议**：图片命名用数字前缀（`01_`, `02_`…）对应 slide 编号，方便追踪哪个 slide 用了哪张图。生成完图片后先过一遍 captions 映射。

在 html-ppt-learning 课件中嵌入图片的最佳实践：

1. **图片放 deck 目录内**：`decks/<category>/<deck>/images/`，HTML 中用相对路径 `src="images/img_01.jpg"`
2. **排版多样性**：`.photo-grid` (2 列图+文), `.photo-img` (全宽), `.photo-img-sm` (居中 60%)
3. **AI 生图管线**：优先用 MiniMax image-01（已有 key），其次 Pollinations.ai（免费），最次 ComfyUI（需 GPU）

### ❌ photo-2x1 2:1 列宽 → 图片下方留白 + 文字列过度挤压

**症状**：`.photo-2x1` 使用 `grid-template-columns: 2fr 1fr`，左侧文字区过宽、右侧图片列过窄。图片受 `aspect-ratio: 16/9` 约束，填不满窄列高度 → 下方大片空白。窄列文字被压缩。

**根因**：`2fr 1fr` 对图文混排不适合——文字需要合理行宽（~60-80 字符），图片需要足够宽度展示。2:1 比例让双方都难受。

**正解**：使用 `1fr 1fr` 等宽 + `align-items: start` 顶部对齐：
```css
.photo-2x1 { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:12px 0; align-items:start; }
```

### ❌ 手机端 photo grid 多列并排 → 图片过小 + 文字断行

**症状**：手机上 4 列品种卡片的图片缩成指甲盖大小，caption 单字断行。

**正解**：添加 `@media (max-width: 768px)` 断点，所有 grid 改为单列：
```css
@media (max-width: 768px) {
  .photo-2, .photo-2x1, .photo-3, .photo-4 {
    grid-template-columns: 1fr !important;
  }
  .photo-img { max-height: 220px; }
  .deck { padding: 0 8px; }
  .slide { padding: 12px 16px !important; }
  .slide h2 { font-size: 1.1em !important; }
  .slide .block { padding: 6px 10px !important; }
  .compare-table th, .compare-table td { padding: 3px 5px !important; font-size: 11px !important; }
}
```

### ❌ deck.json `difficulty` 用字符串 → 主页 502 Bad Gateway

**症状**：主页加载返回 HTTP 502，`server.py` stderr 显示 `TypeError: '<' not supported between instances of 'int' and 'str'`。

**根因**：`server.py` 的 `stars(n)` 函数用 `i < n` 做整数比较生成 ★☆ 评级，但 `deck.json` 写了 `"difficulty": "beginner"` 这样的字符串。

**正解**：`deck.json` 中的 `difficulty` 字段必须用**整数 1-3**：
```json
{
  "title": "课件标题",
  "difficulty": 1,
  ...
}
```
`1` = 入门 · `2` = 进阶 · `3` = 高级

如果确实写了字符串，则需在 `stars(n)` 函数开头补类型转换（已在 `scripts/hub-server.py` 中修复）：
```python
def stars(n):
    if isinstance(n, str):
        n = {'beginner': 1, 'intermediate': 2, 'advanced': 3}.get(n, 1)
    return ''.join('★' if i < n else '☆' for i in range(3))
```

**症状**：改了 learning-print.css 的 `min-height` 或 `align-content` 不生效，PDF 表现不符合预期。

**根因**：base.css 里可能有残留的 `@media print` 规则，CSS 特异性相同时最后加载的胜出——但 `media="print"` 属性的 link 和普通 link 在打印模式下的优先级可能不按字面顺序。safe 起见：**base.css 中不能有任何 `@media print`**。

**正解**：在 base.css 中 `grep -n '@media print'`，全部删除。所有打印规则集中到 learning-print.css。

零输出 = 全部渲染成功。详见 `references/katex-debugging.md`。

## 项目位置

全部源码在 `~/.hermes/skills/creative/html-ppt-learning/`（40+ 个文件，含 KaTeX 本地 ~1.5MB）。

详见该项目的 SKILL.md、references/、templates/、examples/（os-memory 虚拟内存 · ctf-intro CTF 全栈入门）。

图片密集型课件（建筑、艺术、摄影等）参考 `references/image-heavy-decks.md`——含图片网格 CSS、批量生图脚本模板、PDF 打印适配。

### ⚠️ Profile 下缺 assets → 建 symlink

当在非 default profile（如 `yinlang`）下构建课件时，profile 下的 skill 目录只有 SKILL.md + references/templates/，**不包含 `assets/` 和 `examples/`**。本地开发需手动建立 assets 软链接：

```bash
cd /path/to/deck/repo
ln -sf /home/trade/.hermes/skills/creative/html-ppt-learning/assets assets
```

### ⚠️ 打印 CSS 不可跨 profile 编辑 → 内联方案

`learning-print.css` 属于 default profile，从其他 profile（如 yinlang）无法直接 patch（cross-profile write guard）。如需自定义打印样式，直接在 deck HTML 的 `<style>` 中加入 `@media print { ... }` 覆盖规则。
