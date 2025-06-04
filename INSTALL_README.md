# Flask SQLi-Labs 环境安装指南

这个指南将帮助你在Windows和Linux系统上快速安装和运行Flask SQL注入测试平台。

## 📋 系统要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+ 或 Linux (Ubuntu, CentOS, Fedora, Arch等)
- **网络连接**: 用于下载依赖包

## 🪟 Windows 安装

### 1. 自动安装（推荐）

直接双击运行安装脚本：

```batch
setup.bat
```

或在命令行中运行：

```cmd
setup.bat
```

### 2. 手动安装

如果自动安装失败，可以手动执行以下步骤：

```cmd
# 1. 安装uv包管理器
pip install uv

# 2. 创建虚拟环境
uv venv

# 3. 激活虚拟环境
.venv\Scripts\activate.bat

# 4. 安装依赖
uv pip install -r requirements.txt

# 5. 启动应用
python app.py
```

### 3. 启动应用

安装完成后，使用快速启动脚本：

```cmd
start.bat
```

## 🐧 Linux 安装

### 1. 自动安装（推荐）

给脚本添加执行权限并运行：

```bash
chmod +x setup.sh
./setup.sh
```

### 2. 手动安装

如果自动安装失败，可以手动执行以下步骤：

```bash
# 1. 安装uv包管理器
pip install uv
# 或使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
uv venv

# 3. 激活虚拟环境
source .venv/bin/activate

# 4. 安装依赖
uv pip install -r requirements.txt

# 5. 启动应用
python app.py
```

### 3. 启动应用

安装完成后，使用快速启动脚本：

```bash
chmod +x start.sh
./start.sh
```

## 🎯 使用说明

1. **访问应用**: 打开浏览器访问 `http://localhost:5000`
2. **SQL注入练习**: 选择不同的课程（Less-1 到 Less-12）进行练习
3. **停止应用**: 在终端中按 `Ctrl+C` 停止服务器

## 📁 文件说明

| 文件 | 描述 |
|------|------|
| `setup.bat` | Windows环境安装脚本 |
| `setup.sh` | Linux环境安装脚本 |
| `start.bat` | Windows快速启动脚本 |
| `start.sh` | Linux快速启动脚本 |
| `requirements.txt` | Python依赖列表 |
| `app.py` | Flask应用主文件 |

## 🔧 脚本功能

### 安装脚本功能：

1. ✅ **检查Python环境** - 确保Python 3.8+已安装
2. ✅ **检查pip包管理器** - 验证pip可用性
3. ✅ **安装uv包管理器** - 如果未安装则自动安装
4. ✅ **检查项目依赖文件** - 验证requirements.txt存在
5. ✅ **创建虚拟环境** - 使用uv创建.venv虚拟环境
6. ✅ **安装项目依赖** - 安装Flask及相关依赖
7. ✅ **启动确认** - 询问是否立即启动应用

### 启动脚本功能：

1. ✅ **检查虚拟环境** - 确保.venv目录存在
2. ✅ **激活虚拟环境** - 自动激活Python虚拟环境
3. ✅ **启动Flask应用** - 运行app.py启动服务器

## 🚨 常见问题

### 问题1: Python未找到
**解决方案**: 
- Windows: 从 [python.org](https://www.python.org/downloads/) 下载安装
- Linux: 使用包管理器安装，如 `sudo apt install python3 python3-pip`

### 问题2: uv安装失败
**解决方案**: 
```bash
# 方法1: 通过pip安装
pip install uv

# 方法2: 使用官方安装脚本
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 问题3: 权限错误
**解决方案**: 
- Linux: 确保脚本有执行权限 `chmod +x setup.sh`
- Windows: 以管理员权限运行命令行

### 问题4: 网络连接问题
**解决方案**: 
- 检查网络连接
- 如果在公司网络，可能需要配置代理
- 可以尝试使用国内镜像源

### 问题5: 端口5000被占用
**解决方案**: 
- 检查是否有其他程序占用5000端口
- 修改app.py中的端口号
- 或者停止占用端口的程序

## 💡 提示

- 建议使用 **uv** 包管理器，它比pip快10-100倍
- 首次安装可能需要下载较多依赖包，请耐心等待
- 如果遇到问题，可以查看脚本输出的详细错误信息
- 在企业网络环境下，可能需要配置代理设置

## 🔗 相关链接

- [uv 官方文档](https://github.com/astral-sh/uv)
- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Python 官方网站](https://www.python.org/)

---

**享受SQL注入学习之旅！** 🎓 