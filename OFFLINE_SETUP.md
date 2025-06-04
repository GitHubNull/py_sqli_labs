# Python SQLi-Labs 离线部署指南

## 📦 已完成的本地化资源

当前项目已经将以下CDN资源本地化：

### ✅ 已下载的依赖
- **Bootstrap 5.1.3** → `static/vendor/bootstrap/`
  - `bootstrap.min.css` (160KB)
  - `bootstrap.bundle.min.js` (76KB)

- **Font Awesome 6.0.0** → `static/vendor/fontawesome/`
  - `all.min.css` (87KB) - 原始文件
  - `all-fixed.min.css` (自定义) - 修复字体路径的版本 ⭐
  - `webfonts/fa-solid-900.woff2` (124KB)
  - `webfonts/fa-regular-400.woff2` (23KB)
  - `webfonts/fa-brands-400.woff2` (102KB)

- **jQuery 3.6.0** → `static/vendor/jquery/`
  - `jquery.min.js` (87KB)

### 🔧 Font Awesome 图标修复

**问题描述：** 图标显示为方块

**解决方案：** 创建了 `all-fixed.min.css` 文件，修复了字体路径问题：
- 原始路径：`url(../webfonts/fa-*.woff2)`
- 修复路径：`url(webfonts/fa-*.woff2)`

**当前使用：** `templates/base.html` 已配置使用修复版本的CSS文件。

### 🔤 字体处理

#### 当前状态
- 已创建本地Inter字体CSS文件：`static/fonts/inter.css`
- 配置了系统字体备选方案
- 支持中文字体（Microsoft YaHei / 微软雅黑）
- Font Awesome图标字体已完全本地化 ✅

#### 可选：下载Inter字体文件
如果需要完全离线的Inter字体支持，可以下载以下文件到 `static/fonts/` 目录：

```
Inter字体文件下载链接：
https://fonts.google.com/specimen/Inter

需要的文件：
- Inter-Light.woff2 (300 weight)
- Inter-Regular.woff2 (400 weight)  
- Inter-Medium.woff2 (500 weight)
- Inter-SemiBold.woff2 (600 weight)
- Inter-Bold.woff2 (700 weight)
```

**PowerShell下载命令：**
```powershell
# 创建字体目录（如果不存在）
New-Item -ItemType Directory -Path "static\fonts" -Force

# 下载Inter字体文件（这些是示例URL，实际需要从Google Fonts获取）
# 注意：Google Fonts 的实际woff2文件URL需要通过开发者工具获取
```

## 🚀 完全离线部署状态

### ✅ 已完成
- [x] Bootstrap CSS/JS本地化
- [x] Font Awesome图标+字体本地化 
- [x] jQuery本地化
- [x] 字体路径修复（图标正常显示）
- [x] 中文字体支持配置
- [x] 系统字体备选方案

### 📋 部署检查清单

1. **依赖安装**
   ```bash
   pipenv install
   ```

2. **启动应用**
   ```bash
   pipenv run python app.py
   ```

3. **检查图标显示**
   - 访问 http://localhost:5000
   - 确认导航栏图标正常显示
   - 确认各关卡页面图标正常显示

4. **功能测试**
   - 点击"初始化数据库"
   - 测试各个SQLi关卡

## 🎯 内网环境优势

- **零外网依赖** - 所有静态资源完全本地化
- **图标完美显示** - 字体路径已修复
- **字体兼容性强** - 多级备选字体方案
- **部署便捷** - 单一pipenv环境

## 🔄 故障排除

### 图标显示为方块
- **原因：** 字体文件路径错误
- **解决：** 已通过 `all-fixed.min.css` 修复
- **检查：** 确认使用的是修复版CSS文件

### 字体显示异常
- **解决：** 系统会自动回退到微软雅黑等系统字体
- **可选：** 下载Inter字体文件到 `static/fonts/` 目录

### 样式加载失败
- **检查：** 确认 `static/vendor/` 目录下所有文件存在
- **重启：** 重新启动Flask应用

---

**🎉 恭喜！您的Python SQLi-Labs已完全适配内网环境！**

## 📝 完全离线部署流程

1. 确认所有vendor文件已下载
2. 可选：下载Inter字体文件
3. 复制整个项目目录到目标环境
4. 安装Python依赖：`pipenv install`
5. 启动应用：`pipenv run python app.py`
6. 验证功能正常

## 🌐 内网部署建议

- 使用内网DNS或hosts文件解析域名
- 配置内网访问地址：修改app.py中的host参数
- 建议使用反向代理（如Nginx）进行生产部署
- 定期备份数据库文件

---

**注意：** 此配置确保应用在完全离线环境下正常运行，所有外部依赖已本地化。 