#!/usr/bin/env python3
"""
md2html_batch.py — 批量将当前目录下所有 Markdown 文件转换为模板 HTML

用法:
    python md2html_batch.py              # 转换当前目录所有 .md
    python md2html_batch.py -d ./docs    # 转换指定目录所有 .md
    python md2html_batch.py file1.md     # 只转换指定文件
    python md2html_batch.py -o ./out     # 输出到指定目录

依赖: Pandoc (需在 PATH 中)
"""

import subprocess, sys, os, re, argparse, glob

# ═══════════════════════════════════════════════════════════════
# CSS 模板（参考 V40 QA Report 样式）
# ═══════════════════════════════════════════════════════════════
CSS = r"""
/* ====== 主题变量系统 ====== */
:root, [data-theme="dark"] {
    --text-color: #dddddd; --bg-color: #1e1e1e; --bg-secondary: #2d2d2d;
    --scrollbar-color: #888; --muted-color: #aaaaaa; --muted-color-2: #666;
    --border-color: #444; --border-color-light: #555; --code-bg-color: #333;
    --link-color: #6ea8fe; --heading-color: #ffffff; --hr-color: #555;
    --quote-bg-color: #2a2a2a; --th-bg-color: #282828; --tr-even-bg-color: #202020;
    --alert-note-border: #1f6feb; --alert-note-bg: rgba(31,111,235,0.12);
    --alert-tip-border: #238636; --alert-tip-text: #3faa31; --alert-tip-bg: rgba(35,134,54,0.12);
    --alert-important-border: rgb(171,125,248); --alert-important-bg: rgba(171,125,248,0.12);
    --alert-warning-border: #d29722; --alert-warning-bg: rgba(210,151,34,0.12);
    --alert-caution-border: #f04843; --alert-caution-bg: rgba(240,72,67,0.12);
    --tag-highest-bg: rgba(240,72,67,0.15); --tag-highest-border: #f04843;
    --tag-high-bg: rgba(210,151,34,0.15); --tag-high-border: #d29722;
    --tag-medium-bg: rgba(31,111,235,0.15); --tag-medium-border: #1f6feb;
    --tag-low-bg: rgba(35,134,54,0.15); --tag-low-border: #238636;
    --checklist-color: #888; --toc-bg: rgba(42,42,42,0.8);
    --grade-a-color: #3fb950; --grade-b-color: #58a6ff; --grade-c-color: #d29922;
    --grade-d-color: #db6d28; --grade-f-color: #f85149;
}
[data-theme="light"] {
    --text-color: #333333; --bg-color: #ffffff; --bg-secondary: #f0f0f0;
    --scrollbar-color: #aaa; --muted-color: #666666; --muted-color-2: #999999;
    --border-color: #ddd; --border-color-light: #ddd; --code-bg-color: #f6f6f6;
    --link-color: #2E67D3; --heading-color: #1a1a1a; --hr-color: #ddd;
    --quote-bg-color: #f9f9f9; --th-bg-color: #f6f8fa; --tr-even-bg-color: #f6f8fa;
    --alert-note-border: #0969da; --alert-note-bg: #ddf4ff;
    --alert-tip-border: #1a7f37; --alert-tip-text: #1a7f37; --alert-tip-bg: #dafbe1;
    --alert-important-border: #8250df; --alert-important-bg: #fbefff;
    --alert-warning-border: #9a6700; --alert-warning-bg: #fff8c5;
    --alert-caution-border: #cf222e; --alert-caution-bg: #ffebe9;
    --tag-highest-bg: rgba(207,34,46,0.08); --tag-highest-border: #cf222e;
    --tag-high-bg: rgba(154,103,0,0.08); --tag-high-border: #9a6700;
    --tag-medium-bg: rgba(9,105,218,0.08); --tag-medium-border: #0969da;
    --tag-low-bg: rgba(26,127,55,0.08); --tag-low-border: #1a7f37;
    --checklist-color: #999; --toc-bg: rgba(246,248,250,0.9);
    --grade-a-color: #1a7f37; --grade-b-color: #0969da; --grade-c-color: #9a6700;
    --grade-d-color: #bc4c00; --grade-f-color: #cf222e;
}
html, body {
    font-family: "Latin Modern Roman","Latin Modern Roman 10","Times New Roman",
                 "宋体-简","华文宋体",serif;
    font-size: 16px; line-height: 1.618; word-wrap: break-word;
    color: var(--text-color); background: var(--bg-color);
    -webkit-font-smoothing: antialiased; height: 100%; margin: 0; padding: 0;
}
body::-webkit-scrollbar { width: 0.6em; }
body::-webkit-scrollbar-thumb { background: var(--scrollbar-color); border-radius: 0.2em; }
strong, b { font-weight: 900; }
h1,h2,h3,h4,h5,h6 { margin-top:1.5em; margin-bottom:0.5em; font-weight:900;
                      line-height:1.25; color:var(--heading-color); }
h1 { font-family:"Latin Modern Roman","宋体-简","华文宋体","SimHei",serif;
     font-size:2.2em; line-height:1.2; padding-bottom:0.3em;
     border-bottom:2px solid var(--scrollbar-color); margin-bottom:1em; text-align:center; }
h2 { font-family:"Latin Modern Roman","宋体-简","华文宋体","SimHei",serif;
     font-size:1.8em; padding-bottom:0.3em; border-bottom:2px solid var(--scrollbar-color); }
h3 { font-family:"Latin Modern Roman","宋体-简","华文宋体","SimHei",serif; font-size:1.5em; }
h4 { font-family:"Latin Modern Roman","华文楷体","KaiTi",serif; font-size:1.3em; }
h5 { font-family:"Latin Modern Roman","华文仿宋","FangSong",serif; font-size:1.2em; }
a, a:visited { text-decoration:none; color:var(--link-color); }
a:hover { text-decoration:underline; }
p { margin:0.5rem 0 1rem; color:var(--text-color); text-align:left; line-height:1.618; }
code { font-family:"Latin Modern Mono","Consolas","Courier New",monospace;
       color:var(--link-color); background:var(--code-bg-color); font-size:0.95em;
       padding:2px 4px; border-radius:3px; box-shadow:0 0 1px 1px var(--border-color);
       margin:0 2px; }
pre { font-family:"Latin Modern Mono","Consolas","Courier New",monospace;
      font-weight:normal; font-size:95%; line-height:1.5; margin:1.5em 0;
      padding:0; max-width:98%; border:none; overflow:auto; border-radius:4px;
      white-space:pre; background:var(--code-bg-color); color:var(--text-color); }
pre > code { white-space:pre; padding:1em!important; display:block;
             background:transparent; font-weight:normal; color:inherit;
             font-size:inherit; margin:0; box-shadow:none; }
table { width:100%; border-spacing:0; border-collapse:collapse; margin:1.5em auto;
        border-color:var(--scrollbar-color);
        font-family:"Latin Modern Roman","Times New Roman",Times,serif;
        color:var(--text-color); background:var(--code-bg-color); }
td, th { border:1px solid var(--scrollbar-color); padding:0.6em 1em;
         display:table-cell; vertical-align:top; color:var(--text-color); }
th { font-weight:900; background:var(--th-bg-color); text-align:center; }
tbody > tr:nth-child(even) { background:var(--tr-even-bg-color); }
ul, ol { padding-left:2em; margin-top:1em; margin-bottom:1em; color:var(--text-color); }
li { margin-bottom:0.3em; }
blockquote { color:var(--text-color); font-size:1.05em;
             font-family:"Latin Modern Roman","华文仿宋","FangSong",serif;
             border-left:4px solid var(--scrollbar-color); padding:15px 20px;
             margin:1em 0; background-color:var(--quote-bg-color); }
blockquote *:first-child { margin-top:0; }
blockquote *:last-child { margin-bottom:0; }
hr { border:0; border-top:1px solid var(--scrollbar-color); margin:2em 0; }

/* Alert 组件 */
.CAUTION,.IMPORTANT,.INFO,.INFORMATION,.ERROR,.TIP,.NOTE,.WARNING,.DANGER
  { position:relative; padding:1.2em 1.2em 1.2em 3.2em; margin:1.2em 0;
    border-radius:6px; font-size:1em; line-height:1.6; }
.CAUTION::before,.IMPORTANT::before,.INFO::before,.INFORMATION::before,
.ERROR::before,.TIP::before,.NOTE::before,.WARNING::before,.DANGER::before
  { content:""; position:absolute; left:0; top:0; width:6px; height:100%;
    border-radius:6px 0 0 6px; }
.CAUTION>h5,.IMPORTANT>h5,.INFO>h5,.INFORMATION>h5,.ERROR>h5,.TIP>h5,
.NOTE>h5,.WARNING>h5,.DANGER>h5
  { margin-top:0; margin-bottom:0.6em; font-size:1.05em; font-weight:900;
    display:flex; align-items:center; }
.NOTE { background:var(--alert-note-bg); }
.NOTE::before { background:var(--alert-note-border); }
.NOTE>h5 { color:var(--alert-note-border); }
.TIP { background:var(--alert-tip-bg); }
.TIP::before { background:var(--alert-tip-border); }
.TIP>h5 { color:var(--alert-tip-text); }
.WARNING { background:var(--alert-warning-bg); }
.WARNING::before { background:var(--alert-warning-border); }
.WARNING>h5 { color:var(--alert-warning-border); }
.DANGER,.ERROR { background:var(--alert-caution-bg); }
.DANGER::before,.ERROR::before { background:var(--alert-caution-border); }
.DANGER>h5,.ERROR>h5 { color:var(--alert-caution-border); }
.IMPORTANT { background:var(--alert-important-bg); }
.IMPORTANT::before { background:var(--alert-important-border); }
.IMPORTANT>h5 { color:var(--alert-important-border); }
.CAUTION { background:var(--alert-caution-bg); }
.CAUTION::before { background:var(--alert-caution-border); }
.CAUTION>h5 { color:var(--alert-caution-border); }

/* 风险/等级标签 */
.risk-tag { display:inline-block; padding:2px 10px; border-radius:12px;
            font-size:0.85em; font-weight:700; margin-left:6px;
            vertical-align:middle; white-space:nowrap; }
.risk-highest { background:var(--tag-highest-bg); border:1px solid var(--tag-highest-border);
               color:var(--tag-highest-border); }
.risk-high { background:var(--tag-high-bg); border:1px solid var(--tag-high-border);
            color:var(--tag-high-border); }
.risk-medium { background:var(--tag-medium-bg); border:1px solid var(--tag-medium-border);
              color:var(--tag-medium-border); }
.risk-low { background:var(--tag-low-bg); border:1px solid var(--tag-low-border);
           color:var(--tag-low-border); }
.grade-tag { display:inline-block; padding:4px 16px; border-radius:16px;
             font-size:1.1em; font-weight:900; letter-spacing:2px; margin:0 8px; }
.grade-A { background:rgba(63,185,80,0.15); border:2px solid var(--grade-a-color);
           color:var(--grade-a-color); }
.grade-B { background:rgba(88,166,255,0.15); border:2px solid var(--grade-b-color);
           color:var(--grade-b-color); }
.grade-C { background:rgba(210,153,34,0.15); border:2px solid var(--grade-c-color);
           color:var(--grade-c-color); }
.grade-D { background:rgba(219,109,40,0.15); border:2px solid var(--grade-d-color);
           color:var(--grade-d-color); }
.grade-F { background:rgba(248,81,73,0.15); border:2px solid var(--grade-f-color);
           color:var(--grade-f-color); }

/* 目录 */
.toc { background:var(--toc-bg); border:1px solid var(--border-color);
       border-radius:8px; padding:1.2em 1.8em; margin:1.5em 0; }
.toc-title { margin-top:0; font-size:1.2em; }
.toc ul { list-style:none; padding-left:0; }
.toc ul ul { padding-left:1.5em; }
.toc li { margin-bottom:0.3em; }
.toc a { color:var(--link-color); }

/* 主内容区 */
#MainContent { margin:0 auto; padding:0.2em 2.5em 2em 2.5em; max-width:960px;
               border:1px solid var(--border-color); border-radius:0.3em;
               background-color:var(--bg-color);
               box-shadow:0 0 24px 12px rgba(0,0,0,0.15); }
@media(max-width:980px) { #MainContent { border:none; padding:0.2em 0.8em; } }

/* 主题切换按钮 */
#theme-btn { position:fixed; top:20px; right:24px; z-index:99999;
             width:48px; height:48px; border:2px solid var(--border-color);
             border-radius:50%; background:var(--bg-secondary);
             color:var(--heading-color); font-size:22px; cursor:pointer;
             display:flex; align-items:center; justify-content:center;
             box-shadow:0 2px 12px rgba(0,0,0,0.25);
             transition:background-color .35s,color .35s,border-color .35s,
                        box-shadow .35s,transform .2s;
             outline:none; line-height:1; padding:0; }
#theme-btn:hover { transform:scale(1.12); border-color:var(--link-color); }
#theme-btn:active { transform:scale(0.95); }
#theme-btn .tip { position:absolute; top:56px; right:0;
                  background:var(--bg-secondary); color:var(--text-color);
                  border:1px solid var(--border-color); border-radius:6px;
                  padding:4px 12px; font-size:13px;
                  font-family:"微软雅黑","Microsoft YaHei",sans-serif;
                  white-space:nowrap; opacity:0; pointer-events:none;
                  transition:opacity .2s; box-shadow:0 2px 8px rgba(0,0,0,0.15); }
#theme-btn:hover .tip { opacity:1; }
@media(max-width:768px) { #theme-btn { top:12px; right:12px; width:40px;
                                      height:40px; font-size:18px; } }

/* 回到顶部按钮 */
#back-top { position:fixed; bottom:24px; right:24px; z-index:99998;
            width:44px; height:44px; border:2px solid var(--border-color);
            border-radius:50%; background:var(--bg-secondary);
            color:var(--heading-color); font-size:20px; cursor:pointer;
            display:none; align-items:center; justify-content:center;
            box-shadow:0 2px 8px rgba(0,0,0,0.2);
            transition:opacity .3s,transform .2s; outline:none; padding:0; }
#back-top:hover { transform:scale(1.1); border-color:var(--link-color); }
#back-top.show { display:flex; }

::selection { background-color:var(--link-color); color:var(--code-bg-color); }

@media print {
    html,body { text-rendering:optimizeLegibility; height:auto; margin:0;
                padding:40px; background-color:var(--bg-color)!important;
                color:var(--text-color)!important }
    #MainContent { width:100%!important; max-width:none!important; margin:0!important;
                   padding:0!important; border:none!important; border-radius:0!important;
                   box-shadow:none!important; background-color:var(--bg-color)!important }
    #theme-btn,#back-top { display:none!important }
}
"""

# ═══════════════════════════════════════════════════════════════
# JS 模板
# ═══════════════════════════════════════════════════════════════
JS = """
<script>
(function(){
    var s=localStorage.getItem("report-theme");
    if(s)document.documentElement.setAttribute("data-theme",s);
    updateThemeUI();
    window.addEventListener("scroll",function(){
        var b=document.getElementById("back-top");
        if(window.scrollY>300)b.classList.add("show");else b.classList.remove("show");
    });
})();
function toggleTheme(){
    var h=document.documentElement,c=h.getAttribute("data-theme");
    var n=c==="dark"?"light":"dark";h.setAttribute("data-theme",n);
    localStorage.setItem("report-theme",n);updateThemeUI();
}
function updateThemeUI(){
    var d=document.documentElement.getAttribute("data-theme");
    var icon=document.getElementById("themeIcon");
    var tip=document.getElementById("themeTip");
    if(d==="dark"){icon.innerHTML="&#9789;";tip.textContent="切换至浅色模式";}
    else{icon.innerHTML="&#9788;";tip.textContent="切换至深色模式";}
}
</script>
"""

# ═══════════════════════════════════════════════════════════════
# Alert 转换
# ═══════════════════════════════════════════════════════════════
ALERT_MAP = {
    '[!NOTE]':     ('NOTE',     'ℹ️ 注意：'),
    '[!TIP]':      ('TIP',      '💡 提示：'),
    '[!IMPORTANT]':('IMPORTANT', '❗ 重要：'),
    '[!WARNING]':  ('WARNING',  '⚠️ 警惕：'),
    '[!CAUTION]':  ('CAUTION',  '🔥 危险：'),
    '[!SUCCESS]':  ('TIP',      '✅ 达标：'),
}

def convert_alerts(html):
    for md_tag, (cls, title) in ALERT_MAP.items():
        pattern = r'<blockquote>\s*<p>' + re.escape(md_tag) + r'(.*?)</p>\s*</blockquote>'
        def replacer(m, _cls=cls, _title=title):
            content = m.group(1).strip()
            return f'<div class="{_cls}"><h5>{_title}</h5><p>{content}</p></div>'
        html = re.sub(pattern, replacer, html, flags=re.DOTALL)
    return html

# ═══════════════════════════════════════════════════════════════
# 核心：Markdown → 完整 HTML
# ═══════════════════════════════════════════════════════════════
def md_to_html(md_path, out_path=None, title=None):
    """将单个 Markdown 文件转换为完整模板 HTML。"""
    md_path = os.path.abspath(md_path)
    if not os.path.isfile(md_path):
        print(f"  [SKIP] 文件不存在: {md_path}")
        return False

    if title is None:
        title = os.path.splitext(os.path.basename(md_path))[0]
    if out_path is None:
        out_path = os.path.splitext(md_path)[0] + ".html"
    out_path = os.path.abspath(out_path)

    # Step 1: Pandoc 转换
    try:
        result = subprocess.run(
            ["pandoc", md_path, "-f", "markdown", "-t", "html", "--wrap=none"],
            capture_output=True, text=True, encoding="utf-8", timeout=60
        )
        if result.returncode != 0:
            print(f"  [ERROR] Pandoc 失败: {result.stderr.strip()}")
            return False
        body_html = result.stdout
    except FileNotFoundError:
        print("[FATAL] 未找到 pandoc，请先安装并加入 PATH: https://pandoc.org/installing.html")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"  [ERROR] Pandoc 超时: {md_path}")
        return False

    # Step 2: Alert 转换
    body_html = convert_alerts(body_html)

    # Step 3: 拼接完整 HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{CSS}
</style>
</head>
<body>
<button id="theme-btn" onclick="toggleTheme()" aria-label="Toggle light/dark theme">
<span id="themeIcon">&#9789;</span><span class="tip" id="themeTip">切换至浅色模式</span></button>
<button id="back-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">&#8679;</button>
<div id="MainContent">
{body_html}
</div>
{JS}
</body>
</html>"""

    # Step 4: 写入文件
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    size_kb = os.path.getsize(out_path) / 1024
    print(f"  [OK] {os.path.basename(md_path)} -> {os.path.basename(out_path)} ({size_kb:.1f} KB)")
    return True

# ═══════════════════════════════════════════════════════════════
# 批量入口
# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="批量将 Markdown 文件转换为模板 HTML（明暗主题、回到顶部、Alert 组件）",
        epilog="示例: python md2html_batch.py -d ./docs -o ./out"
    )
    parser.add_argument("-d", "--dir", default=".", help="扫描目录（默认当前目录）")
    parser.add_argument("-o", "--output", default="", help="输出目录（默认与源文件同目录）")
    parser.add_argument("files", nargs="*", help="指定文件（优先于 -d 扫描）")
    parser.add_argument("-y", "--yes", action="store_true", help="跳过确认直接转换")
    args = parser.parse_args()

    # 收集文件列表
    if args.files:
        md_files = [os.path.abspath(f) for f in args.files if f.endswith(".md")]
    else:
        scan_dir = os.path.abspath(args.dir)
        md_files = sorted(glob.glob(os.path.join(scan_dir, "*.md")))

    if not md_files:
        print("未找到任何 .md 文件。")
        sys.exit(0)

    # 排除自身（如果脚本所在目录有同名md）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_files = [f for f in md_files if not f.endswith("md2html_batch.md")]

    print(f"找到 {len(md_files)} 个 Markdown 文件：")
    for f in md_files:
        print(f"  - {os.path.basename(f)}")

    if not args.yes:
        answer = input("\n是否开始转换？[Y/n] ").strip().lower()
        if answer and answer not in ("y", "yes"):
            print("已取消。")
            sys.exit(0)

    print()
    success, fail = 0, 0
    for md_file in md_files:
        if args.output:
            out_dir = os.path.abspath(args.output)
            out_path = os.path.join(out_dir, os.path.splitext(os.path.basename(md_file))[0] + ".html")
        else:
            out_path = None  # 与源文件同目录

        if md_to_html(md_file, out_path):
            success += 1
        else:
            fail += 1

    print(f"\n完成：{success} 成功，{fail} 失败，共 {len(md_files)} 个文件。")

if __name__ == "__main__":
    main()
