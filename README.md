# md2html-batch

> **Cross-Platform Markdown-to-HTML Batch Converter**
> Dark/Light theme toggle · Alert components · Risk/Grade tags · Responsive layout · Zero external dependencies

---

## Features

| Feature | Description |
|:---|:---|
| **Dark/Light Theme Toggle** | One-click switch (top-right corner), auto-saves preference via `localStorage` |
| **Alert Components** | Supports `[!NOTE]` `[!TIP]` `[!WARNING]` `[!IMPORTANT]` `[!CAUTION]` blockquotes |
| **Risk Level Tags** | Four-level risk labels: highest / high / medium / low |
| **Grade Score Styles** | A/B/C/D/F five-tier visual grading |
| **Back to Top** | Floating button appears after scrolling 300px |
| **Responsive** | Adapts to mobile / tablet / desktop |
| **Print Optimized** | `@media print` rules for clean black-and-white output |
| **Zero Dependencies** | Outputs a single self-contained HTML file — no CDN, no external assets |
| **Cross-Platform** | Works on Windows (`.bat`) and macOS/Linux (`.sh`) |

---

## Requirements

- **Python 3.6+** (no third-party packages needed)
- **Pandoc** (must be installed and in system PATH)
  - Windows: [Download pandoc](https://pandoc.org/installing.html)
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc` or `sudo dnf install pandoc`

---

## Quick Start

### Windows

#### Option 1: Double-click (Simplest)

1. Copy `md2html.bat` into any folder containing `.md` files
2. Double-click `md2html.bat`
3. Enter the directory or file path when prompted

#### Option 2: Command-line

```cmd
:: Convert all .md files in the current directory
md2html.bat

:: Convert files in a specific directory
md2html.bat -d C:\Docs

:: Output to a specific directory
md2html.bat -d C:\Docs -o C:\Output

:: Convert specific files only
md2html.bat file1.md file2.md

:: Skip confirmation prompt
md2html.bat -y
```

### macOS / Linux

#### Option 1: Shell script (Recommended)

```bash
# First time: make executable
chmod +x md2html.sh

# Convert all .md files in the current directory
./md2html.sh

# Convert files in a specific directory
./md2html.sh -d ~/Documents

# Output to a specific directory
./md2html.sh -d ~/Documents -o ~/Output

# Convert specific files only
./md2html.sh file1.md file2.md

# Skip confirmation prompt
./md2html.sh -y
```

#### Option 2: Direct Python Invocation

```bash
# Works on all platforms
python3 md2html_batch.py -d . -o ./html_output
```

---

## Theme System

The generated HTML includes a complete dark/light theme variable system:

```css
/* Dark theme (default) */
[data-theme="dark"] {
    --bg-color: #1e1e1e;
    --text-color: #dddddd;
    --link-color: #6ea8fe;
    /* ... */
}

/* Light theme */
[data-theme="light"] {
    --bg-color: #ffffff;
    --text-color: #333333;
    --link-color: #2E67D3;
    /* ... */
}
```

Click the ☀️/🌙 button in the top-right corner to toggle. Your preference is automatically saved to `localStorage` and restored on next visit.

---

## Alert Component Examples

````markdown
> [!NOTE]
> This is a NOTE

> [!TIP]
> This is a TIP

> [!WARNING]
> This is a WARNING

> [!IMPORTANT]
> This is IMPORTANT

> [!CAUTION]
> This is a CAUTION
````

Rendered appearance (dark theme):

- **NOTE** — Blue border, semi-transparent blue background
- **TIP** — Green border, green text
- **IMPORTANT** — Purple border
- **WARNING** — Orange border
- **CAUTION** — Red border

---

## Risk Tag Examples

```html
<span class="risk-tag" data-level="highest">Highest Risk</span>
<span class="risk-tag" data-level="high">High Risk</span>
<span class="risk-tag" data-level="medium">Medium Risk</span>
<span class="risk-tag" data-level="low">Low Risk</span>
```

Grade tags:

```html
<span class="grade-tag" data-grade="A">Excellent</span>
<span class="grade-tag" data-grade="B">Good</span>
<span class="grade-tag" data-grade="C">Pass</span>
<span class="grade-tag" data-grade="D">Poor</span>
<span class="grade-tag" data-grade="F">Fail</span>
```

---

## File Structure

```
md2html_batch/
├── md2html_batch.py   # Core script (Python, no third-party deps)
├── md2html.bat        # Windows batch entry point
├── md2html.sh         # macOS/Linux shell entry point
├── README.md          # English documentation
└── README-cn.md       # Chinese documentation
```

---

## How It Works

1. The Python script calls the system-installed Pandoc (`pandoc -f markdown -t html`) to convert Markdown to base HTML
2. It injects a complete `<style>` block (theme variables, responsive layout, alerts, tag styles) and `<script>` block (theme toggle, back-to-top, alert parsing) into the base HTML
3. The output is a **fully self-contained single HTML file** with zero external dependencies

---

## Use Cases

- Batch generation of judicial document quality analysis reports
- Converting internal knowledge base documents to styled HTML
- Any scenario requiring offline-readable, beautifully styled Markdown reports

---

## License

MIT
