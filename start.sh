#!/bin/bash

# ================================================
# Flask SQLi-Labs 快速启动脚本 (Linux版)
# ================================================

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo
echo "🚀 启动 Flask SQLi-Labs..."
echo

# 检查虚拟环境是否存在
if [[ ! -d ".venv" ]]; then
    echo -e "${RED}❌${NC} 虚拟环境不存在，请先运行 ./setup.sh 安装环境"
    exit 1
fi

# 激活虚拟环境并启动应用
source .venv/bin/activate
echo -e "${GREEN}✅${NC} 虚拟环境已激活"
echo "📡 启动Flask应用服务器..."
echo
python app.py