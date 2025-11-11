# 🚀 推送到 GitHub 指南

## 快速推送方案（推荐）

### 方案 A：使用 GitHub Desktop（最简单）

1. 下载项目文件夹 `/workspace/mouse_recorder/`
2. 打开 GitHub Desktop
3. File → Add Local Repository → 选择 `mouse_recorder` 文件夹
4. 点击 "Publish repository"
5. 仓库名填写：`mouse-controller`
6. 取消勾选 "Keep this code private"（如果是公开仓库）
7. 点击 "Publish Repository"

### 方案 B：命令行推送（已准备好）

项目已经完全配置好了，你只需要：

```bash
# 1. 进入项目目录（如果你在 Cursor 终端）
cd /workspace/mouse_recorder

# 2. 直接推送
git push -u origin main
```

如果提示需要认证，使用你的 GitHub 用户名和 Personal Access Token。

### 方案 C：从零开始（适合下载到本地后）

如果你把项目文件夹下载到了本地：

```bash
# 进入项目目录
cd mouse_recorder

# 查看状态（已经有提交）
git log --oneline

# 直接推送
git push -u origin main
```

## 🔑 如果需要认证

### 生成 GitHub Personal Access Token

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token
5. 推送时使用 token 作为密码

### 配置凭据（可选）

```bash
# 缓存凭据（避免重复输入）
git config --global credential.helper cache

# 或者直接在 URL 中使用 token
git remote set-url origin https://YOUR_TOKEN@github.com/dccdc/mouse-controller.git
git push -u origin main
```

## 📦 项目当前状态

✅ Git 仓库已初始化  
✅ 所有文件已提交（10 个文件，941 行代码）  
✅ 分支已设置为 main  
✅ 远程仓库已配置：https://github.com/dccdc/mouse-controller.git  
⏳ 等待推送...

## 🎯 推送后验证

访问：https://github.com/dccdc/mouse-controller

你应该能看到：
- README.md 显示在首页
- 10 个项目文件
- 完整的文档和运行脚本

## ❓ 遇到问题？

### 403 权限错误
- 确保你有该仓库的写入权限
- 确保仓库已在 GitHub 上创建
- 使用 Personal Access Token 而不是密码

### 仓库不存在
```bash
# 在 GitHub 创建仓库后，重新设置远程地址
git remote set-url origin https://github.com/dccdc/mouse-controller.git
```

### 推送冲突
```bash
# 如果远程有 README，先拉取
git pull origin main --allow-unrelated-histories
git push -u origin main
```
