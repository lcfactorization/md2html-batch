#!/bin/bash
# ============================================================
#  md2html.sh — macOS/Linux 一键运行入口
#  用法:
#    chmod +x md2html.sh
#    ./md2html.sh                    # 转换当前目录所有 .md
#    ./md2html.sh -d ~/Documents     # 转换指定目录
#    ./md2html.sh -d ~/Docs -o ~/Out # 输出到指定目录
#    ./md2html.sh file1.md file2.md  # 只转换指定文件
#    ./md2html.sh -y                 # 跳过确认
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/md2html_batch.py"

# 检查 Python3
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[ERROR] 未找到 Python，请先安装 Python 3.6+"
    exit 1
fi

# 检查 Pandoc
if ! command -v pandoc &>/dev/null; then
    echo "[ERROR] 未找到 Pandoc，请先安装: brew install pandoc"
    echo "  或访问 https://pandoc.org/installing.html"
    exit 1
fi

# 检查脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "[ERROR] 未找到 $PYTHON_SCRIPT"
    echo "  请确保 md2html_batch.py 与 md2html.sh 在同一目录"
    exit 1
fi

# 传递所有参数给 Python 脚本
exec "$PYTHON" "$PYTHON_SCRIPT" "$@"
