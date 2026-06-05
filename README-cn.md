# md2html-batch

> **跨平台 Markdown 批量转 HTML 工具**
> 支持明暗主题自动切换 · Alert 组件 · 风险/等级标签 · 响应式布局 · 零外部依赖

---

## 功能特性

| 特性 | 说明 |
|:---|:---|
| **明暗主题切换** | 右上角一键切换，自动记忆用户偏好（`localStorage`） |
| **Alert 组件** | 支持 `[!NOTE]` `[!TIP]` `[!WARNING]` `[!IMPORTANT]` `[!CAUTION]` 五种标注块 |
| **风险等级标签** | 司法文书分析输出 highest / high / medium / low 四级风险标签 |
| **Grade 评分样式** | A/B/C/D/F 五级评分可视化 |
| **回到顶部** | 滚动超过 300px 右上角出现按钮 |
| **响应式** | 手机 / 平板 / 桌面自适应 |
| **打印优化** | `@media print` 优化黑白打印效果 |
| **零依赖** | 输出为单文件 HTML，浏览器直接打开，无任何外部 CDN 依赖 |
| **跨平台** | 支持 Windows（`.bat`）和 macOS/Linux（`.sh`） |

---

## 环境要求

- **Python 3.6+**（无需安装任何第三方包）
- **Pandoc**（需提前安装并加入系统 PATH）
  - Windows：[下载 pandoc](https://pandoc.org/installing.html)
  - macOS：`brew install pandoc`
  - Linux：`sudo apt install pandoc` 或 `sudo dnf install pandoc`

---

## 快速开始

### Windows

#### 方式一：双击运行（最简单）

1. 把 `md2html.bat` 复制到任意含 `.md` 文件的目录
2. 双击 `md2html.bat`
3. 屏幕右上角显示「请输入路径」时，输入要转换的目录或文件路径

#### 方式二：命令行参数

```cmd
:: 转换当前目录所有 .md 文件
md2html.bat

:: 转换指定目录
md2html.bat -d C:\Docs

:: 输出到指定目录
md2html.bat -d C:\Docs -o C:\Output

:: 只转换指定文件
md2html.bat file1.md file2.md

:: 跳过确认提示
md2html.bat -y
```

### macOS / Linux

#### 方式一：Shell 脚本（推荐）

```bash
# 首次使用：添加执行权限
chmod +x md2html.sh

# 转换当前目录所有 .md 文件
./md2html.sh

# 转换指定目录
./md2html.sh -d ~/Documents

# 输出到指定目录
./md2html.sh -d ~/Documents -o ~/Output

# 只转换指定文件
./md2html.sh file1.md file2.md

# 跳过确认提示
./md2html.sh -y
```

#### 方式二：直接调用 Python

```bash
# 所有平台通用
python3 md2html_batch.py -d . -o ./html_output
```

---

## 主题系统

HTML 文件内置完整的明暗主题变量系统：

```css
/* 暗色主题（默认） */
[data-theme="dark"] {
    --bg-color: #1e1e1e;
    --text-color: #dddddd;
    --link-color: #6ea8fe;
    /* ... */
}

/* 亮色主题 */
[data-theme="light"] {
    --bg-color: #ffffff;
    --text-color: #333333;
    --link-color: #2E67D3;
    /* ... */
}
```

用户点击右上角 ☀️/🌙 按钮即可切换，偏好自动保存到 `localStorage`，下次打开自动应用。

---

## Alert 组件示例

````markdown
[!NOTE]
这是一条 NOTE 提示

[!TIP]
这是一条 TIP 提示

[!WARNING]
这是一条 WARNING 警告

[!IMPORTANT]
这是一条 IMPORTANT 重要提示

[!CAUTION]
这是一条 CAUTION 注意事项
````

渲染效果（暗色主题）：

- **NOTE** — 蓝色边框，蓝色背景透明度
- **TIP** — 绿色边框，绿色文字
- **IMPORTANT** — 紫色边框
- **WARNING** — 橙色边框
- **CAUTION** — 红色边框

---

## 风险标签示例

```html
<span class="risk-tag" data-level="highest">极高风险</span>
<span class="risk-tag" data-level="high">高风险</span>
<span class="risk-tag" data-level="medium">中风险</span>
<span class="risk-tag" data-level="low">低风险</span>
```

评分等级：

```html
<span class="grade-tag" data-grade="A">优秀</span>
<span class="grade-tag" data-grade="B">良好</span>
<span class="grade-tag" data-grade="C">合格</span>
<span class="grade-tag" data-grade="D">较差</span>
<span class="grade-tag" data-grade="F">不及格</span>
```

---

## 文件结构

```
md2html_batch/
├── md2html_batch.py   # 核心脚本（Python，无第三方依赖）
├── md2html.bat        # Windows 批处理入口
├── md2html.sh         # macOS/Linux Shell 入口
├── README.md          # 英文文档
└── README-cn.md       # 中文文档
```

---

## 工作原理

1. Python 脚本调用系统已安装的 Pandoc（`pandoc -f markdown -t html`）将 Markdown 转为基础 HTML
2. 在基础 HTML 上注入完整的 `<style>`（主题变量、响应式、Alert、标签样式）和 `<script>`（明暗切换、回到顶部、Alert 解析）
3. 生成的文件为**完全自包含的单文件 HTML**，无任何外部依赖

---

## 适用场景

- 司法文书质量分析报告批量生成
- 内部知识库文档批量 HTML 化
- 任何需要生成可离线阅读、带美观样式 Markdown 报告的场景

---

## License

MIT
