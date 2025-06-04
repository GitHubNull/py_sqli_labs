# SQLi-Labs 中文版

这是一个基于Flask的SQL注入漏洞学习平台，完全复制了原版SQLi-Labs的功能，并提供了现代化的中文界面。

## 🎯 项目特色

- **完整复制**: 包含原版SQLi-Labs的所有12个实验
- **现代界面**: 使用Bootstrap 5和现代CSS设计
- **中文支持**: 完全中文化的界面和教学内容
- **教育导向**: 每个实验都包含详细的学习指导
- **安全警告**: 明确标注仅供教育使用

## 📋 实验列表

### 基础注入类型
- **Less-1**: GET - 错误注入 - 单引号字符串
- **Less-2**: GET - 错误注入 - 整数型
- **Less-3**: GET - 错误注入 - 单引号字符串（带括号）
- **Less-4**: GET - 错误注入 - 双引号字符串

### 盲注类型
- **Less-5**: GET - 双查询盲注 - 单引号字符串
- **Less-6**: GET - 双查询盲注 - 双引号字符串
- **Less-8**: GET - 布尔盲注 - 单引号字符串
- **Less-9**: GET - 时间盲注 - 单引号字符串
- **Less-10**: GET - 时间盲注 - 双引号字符串

### POST注入类型
- **Less-11**: POST - 错误注入 - 单引号字符串
- **Less-12**: POST - 错误注入 - 双引号字符串

### 特殊注入
- **Less-7**: GET - 文件导出注入

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Flask 2.3+

### 安装步骤

1. **克隆项目**
```bash
git clone <your-repo-url>
cd py_sqli_lab
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **初始化数据库**
```bash
python app.py
# 或者访问 http://localhost:5000/setup
```

4. **运行应用**
```bash
python app.py
```

5. **访问应用**
打开浏览器访问: http://localhost:5000

## 🎓 使用指南

### 初次使用
1. 访问主页查看所有可用实验
2. 点击 "初始化数据库" 按钮设置测试数据
3. 选择感兴趣的实验开始学习

### 测试账户
系统预置了以下测试账户：
- admin / admin123
- user1 / password1
- dumb / dumb
- Angelina / I-kill-you

### 学习建议
1. **按顺序学习**: 从Less-1开始，逐步深入
2. **理解原理**: 仔细阅读每个实验的漏洞分析
3. **动手实践**: 使用提供的快速测试按钮
4. **工具结合**: 配合Burp Suite、SQLMap等工具

## ⚠️ 安全警告

**重要提醒**: 本项目仅供教育和学习使用！

- ❌ 禁止用于任何非法活动
- ❌ 禁止攻击他人系统
- ❌ 禁止用于商业用途
- ✅ 仅在授权环境中测试
- ✅ 用于安全研究和教育

## 🛠️ 技术栈

- **后端**: Flask (Python)
- **前端**: Bootstrap 5, HTML5, CSS3, JavaScript
- **数据库**: SQLite
- **图标**: Font Awesome
- **字体**: Google Fonts

## 📁 项目结构

```
py_sqli_lab/
├── app.py              # Flask主应用
├── requirements.txt    # Python依赖
├── README.md          # 项目说明
├── sqli_labs.db      # SQLite数据库（运行后生成）
├── templates/         # HTML模板
│   ├── base.html     # 基础模板
│   ├── index.html    # 主页
│   └── less*.html    # 各实验页面
└── static/           # 静态资源
    ├── css/
    │   └── style.css # 样式文件
    ├── js/           # JavaScript文件
    └── images/       # 图片资源
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 贡献方式
1. Fork本项目
2. 创建特性分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目基于MIT许可证开源，详见LICENSE文件。

## 🙏 致谢

- 感谢原版SQLi-Labs项目的作者
- 感谢所有为网络安全教育做出贡献的开发者

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件

---

**记住：学习网络安全是为了更好地保护系统，而不是破坏它们！** 