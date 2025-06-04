#!/bin/bash

# ================================================
# Flask SQLi-Labs 环境安装脚本 (Linux版)
# 功能: 检查并安装uv包管理器和项目依赖
# 版本: 1.0
# 日期: 2025-06-04
# ================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 输出函数
print_step() {
    echo -e "${BLUE}[$1/5]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# 脚本开始
echo
echo "========================================"
echo " Flask SQLi-Labs 环境安装脚本"
echo "========================================"
echo

# 检查是否为root用户运行
if [[ $EUID -eq 0 ]]; then
    print_warning "建议不要以root用户运行此脚本"
    read -p "是否继续？(y/N): " continue_as_root
    if [[ ! $continue_as_root =~ ^[Yy]$ ]]; then
        echo "脚本退出"
        exit 1
    fi
fi

# 1. 检查Python环境
print_step "1" "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "未找到Python，请先安装Python 3.8+"
        echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "Fedora: sudo dnf install python3 python3-pip"
        echo "Arch: sudo pacman -S python python-pip"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_success "Python已安装: $PYTHON_VERSION"

echo

# 2. 检查pip
print_step "2" "检查pip包管理器..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_error "pip不可用，请检查Python安装"
    echo "尝试安装pip: curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD"
    exit 1
else
    print_success "pip可用"
fi

echo

# 3. 检查uv是否安装
print_step "3" "检查uv包管理器..."
if ! command -v uv &> /dev/null; then
    print_warning "uv未安装，正在安装..."
    
    # 尝试通过pip安装uv
    if $PYTHON_CMD -m pip install uv; then
        print_success "通过pip安装uv成功"
    else
        print_warning "通过pip安装uv失败，尝试官方安装方式..."
        
        # 使用官方安装脚本
        if curl -LsSf https://astral.sh/uv/install.sh | sh; then
            # 重新加载环境变量
            export PATH="$HOME/.cargo/bin:$PATH"
            source ~/.bashrc 2>/dev/null || true
            source ~/.zshrc 2>/dev/null || true
            
            if command -v uv &> /dev/null; then
                print_success "uv安装成功"
            else
                print_error "uv安装失败，请重新打开终端或手动安装"
                echo "手动安装命令: pip install uv"
                echo "或访问: https://github.com/astral-sh/uv"
                exit 1
            fi
        else
            print_error "uv安装失败"
            echo "请手动安装: pip install uv"
            exit 1
        fi
    fi
else
    UV_VERSION=$(uv --version 2>&1 | cut -d' ' -f2)
    print_success "uv已安装: $UV_VERSION"
fi

echo

# 4. 检查requirements.txt
print_step "4" "检查项目依赖文件..."
if [[ ! -f "requirements.txt" ]]; then
    print_error "未找到requirements.txt文件"
    echo "请确保在项目根目录下运行此脚本"
    exit 1
else
    print_success "找到requirements.txt"
fi

echo

# 5. 创建虚拟环境并安装依赖
print_step "5" "安装项目依赖..."

# 检查是否已存在虚拟环境
if [[ -d ".venv" ]]; then
    print_info "虚拟环境已存在，跳过创建"
else
    echo "📦 创建虚拟环境..."
    if uv venv; then
        print_success "虚拟环境创建成功"
    else
        print_error "创建虚拟环境失败"
        exit 1
    fi
fi

echo "📥 安装项目依赖..."
if uv pip install -r requirements.txt; then
    print_success "依赖安装成功"
else
    print_warning "依赖安装失败，尝试传统方式..."
    # 激活虚拟环境并使用pip安装
    source .venv/bin/activate
    if pip install -r requirements.txt; then
        print_success "依赖安装成功"
    else
        print_error "依赖安装失败"
        exit 1
    fi
fi

echo
echo "========================================"
echo -e "${GREEN}✅ 环境安装完成！${NC}"
echo "========================================"
echo
echo "📋 接下来的步骤:"
echo "1. 激活虚拟环境: source .venv/bin/activate"
echo "2. 启动应用: python app.py"
echo "3. 访问地址: http://localhost:5000"
echo
echo "💡 提示: 可以直接运行 ./start.sh 启动应用"
echo

# 询问是否立即启动
read -p "是否现在启动应用？(y/N): " start_app
if [[ $start_app =~ ^[Yy]$ ]]; then
    echo
    echo "🚀 启动应用..."
    source .venv/bin/activate
    python app.py
else
    echo
    echo "�� 安装完成，随时可以启动应用！"
fi 