#!/bin/bash
# macOS/Linux 运行脚本

echo "🖱️  鼠标录制回放工具"
echo "===================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi

# 检查依赖
if ! python3 -c "import pynput" &> /dev/null; then
    echo "📦 正在安装依赖..."
    pip3 install -r requirements.txt
fi

# 运行程序
echo "🚀 启动程序..."
python3 main.py
