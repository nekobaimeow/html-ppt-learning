# KaTeX 常用公式速查

> 所有公式在 slide 中使用 `$$...$$`（块级）或 `$...$`（行内）。KaTeX CDN: katex@0.16.11。
> **禁止**用纯文本表示数学公式——必须用 KaTeX。

---

## 快速复制

### 基础

```
行内公式   $E = mc^2$
块级公式   $$E = mc^2$$
```

### 字号控制

在 `.block-formula .vars` 中 KaTeX 会自动缩小。如需手动调：

```
$$\small EAT = (1-p)T_{mem} + p T_{disk}$$
$${\footnotesize \text{...}}$$
```

`\small` 和 `\footnotesize` 只在块级公式的 `$$` 中有效。

---

## 希腊字母

| 符号 | 代码 | 符号 | 代码 | 符号 | 代码 |
|------|------|------|------|------|------|
| $\alpha$ | `\alpha` | $\beta$ | `\beta` | $\gamma$ | `\gamma` |
| $\delta$ | `\delta` | $\epsilon$ | `\epsilon` | $\theta$ | `\theta` |
| $\lambda$ | `\lambda` | $\mu$ | `\mu` | $\pi$ | `\pi` |
| $\rho$ | `\rho` | $\sigma$ | `\sigma` | $\tau$ | `\tau` |
| $\phi$ | `\phi` | $\omega$ | `\omega` |
| $\Gamma$ | `\Gamma` | $\Delta$ | `\Delta` | $\Theta$ | `\Theta` |
| $\Lambda$ | `\Lambda` | $\Pi$ | `\Pi` | $\Sigma$ | `\Sigma` |
| $\Phi$ | `\Phi` | $\Omega$ | `\Omega` |

---

## 分数

```
$$\frac{分子}{分母}$$
$$\frac{1}{\sqrt{2\pi\sigma^2}}$$
$$\frac{\sum_{i=1}^{n} x_i}{n}$$
```

复杂分数用 `\dfrac` 保持行内字号，或 `\tfrac` 缩小：

```
$$\dfrac{\partial f}{\partial x}$$
$$\tfrac{1}{2}$$
```

---

## 上下标

```
$x^2$          x²
$x^{n+1}$      复杂上标用花括号
$x_n$          下标
$x_{i,j}$      多级下标
$$T_{\text{mem}}$$      文本下标（用 \text{}）
```

---

## 求和、积分、乘积

```
$$\sum_{i=1}^{n} x_i$$
$$\sum_{i=1}^{\infty} \frac{1}{i^2}$$
$$\int_{0}^{\infty} e^{-x} dx$$
$$\iint_{D} f(x,y) dx dy$$
$$\prod_{i=1}^{n} p_i$$
$$\lim_{n \to \infty} \frac{1}{n}$$
```

---

## 矩阵

```
$$\begin{pmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{pmatrix}$$
```

矩阵括号变体：

```
\begin{pmatrix} ... \end{pmatrix}    →  圆括号  ( )
\begin{bmatrix} ... \end{bmatrix}    →  方括号  [ ]
\begin{Bmatrix} ... \end{Bmatrix}    →  花括号  { }
\begin{vmatrix} ... \end{vmatrix}    →  行列式   | |
\begin{Vmatrix} ... \end{Vmatrix}    →  双竖线   ‖ ‖
```

---

## 分段函数 (cases)

```
$$f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}$$
```

实际用例——页面状态：

```
$$\text{State}(p) = \begin{cases}
\text{Unallocated} & \text{if no PTE exists} \\
\text{In Memory} & \text{if PTE.P = 1} \\
\text{On Disk} & \text{if PTE.P = 0, swap_offset} \neq \text{NULL}
\end{cases}$$
```

---

## 多行公式对齐 (aligned)

```
$$\begin{aligned}
EAT &= P_{\text{hit}} \times T_{\text{mem}} + P_{\text{miss}} \times T_{\text{disk}} \\
    &= (1 - p) \times 100\text{ns} + p \times 10\text{ms} \\
    &\approx 100\text{ns} + p \times 10\text{ms}
\end{aligned}$$
```

对齐点用 `&`，换行用 `\\`。

带编号：

```
$$\begin{aligned}
x &= a + b  \tag{1}\\
y &= c + d  \tag{2}
\end{aligned}$$
```

---

## 箭头

| 符号 | 代码 |
|------|------|
| $\rightarrow$ | `\rightarrow` 或 `\to` |
| $\leftarrow$ | `\leftarrow` 或 `\gets` |
| $\Rightarrow$ | `\Rightarrow` |
| $\Leftarrow$ | `\Leftarrow` |
| $\Leftrightarrow$ | `\Leftrightarrow` |
| $\mapsto$ | `\mapsto` |
| $\longrightarrow$ | `\longrightarrow` |

带文字箭头（`\xrightarrow`）：

```
$$\text{CPU} \xrightarrow{\text{虚拟地址}} \text{MMU} \xrightarrow{\text{物理地址}} \text{RAM}$$
```

---

## 根号、绝对值、范数

```
$$\sqrt{x}$$          平方根
$$\sqrt[n]{x}$$        n次根
$$|x|$$               绝对值
$$\|x\|$$             范数
$$\lVert x \rVert$$   范数（推荐）
```

---

## 文字和空格

```
$$\text{这是一个文字块}$$         文字
$$x_{\text{disk}}$$                文本下标
$a\ b$                            空格（反斜杠+空格）
$a \quad b$                       一个 em 空格
$a \qquad b$                      两个 em 空格
```

---

## 实际公式示例（内存管理主题）

### 有效访问时间 (EAT)

```
$$EAT = (1-p) \times T_{\text{mem}} + p \times T_{\text{disk}}$$
```

### 缺页率定义

```
$$p = \frac{\text{Page Faults}}{\text{Total Memory Accesses}}$$
```

### 页面偏移计算

```
$$\text{offset} = \text{vaddr} \bmod \text{page\_size}$$
$$\text{page\_number} = \left\lfloor \frac{\text{vaddr}}{\text{page\_size}} \right\rfloor$$
```

### 页表大小

```
$$\text{PT Size} = \frac{\text{Virtual Address Space}}{\text{Page Size}} \times \text{PTE Size}$$
```

### TLB 命中率下的 EAT

```
$$\begin{aligned}
EAT_{\text{TLB}} &= h \times (T_{\text{TLB}} + T_{\text{mem}}) + (1-h) \times (T_{\text{TLB}} + k \times T_{\text{mem}}) \\
&\approx 0.99 \times 110\text{ns} + 0.01 \times 410\text{ns} \approx 113\text{ns}
\end{aligned}$$
```

其中 $h$ = TLB 命中率，$k$ = 页表级数。

### 工作集模型

```
$$\text{WS}(t, \Delta) = \{ \text{pages referenced in } [t-\Delta, t] \}$$
```

### LRU 栈距离

```
$$\text{Stack Distance} = |\{p \in \text{stack above } x\}|$$
```

---

## 常见错误

| 错误 | 正确 |
|------|------|
| `$ T_{mem} $` （多余空格） | `$T_{mem}$` |
| `\frac12` （省略花括号） | `\frac{1}{2}` |
| 在 `.vars` 中用 `$$` | `.vars` 内用行内 `$` |
| 文本不包裹 `\text{}` | `T_{\text{mem}}` |
| 公式太长不换行 | 用 `\begin{aligned}` |
