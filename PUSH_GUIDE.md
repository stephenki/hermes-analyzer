# 🚀 GitHub 推送指南

## 方式一：手动创建 + 推送（推荐）

### 第 1 步：在 GitHub 创建仓库

1. 打开浏览器，访问：https://github.com/new
2. 填写信息：
   - **Repository name**: `hermes-analyzer`
   - **Description**: `Hermes AI Agent conversation analyzer - Track token usage, tool calls, and costs`
   - **Visibility**: Public ✅
   - ❌ **不要**勾选 "Add a README file"（我们已有本地仓库）
   - ❌ **不要**勾选 "Add .gitignore"（已有）
   - ❌ **不要**勾选 "Choose a license"（已有 LICENSE）
3. 点击 **Create repository**

### 第 2 步：添加远程仓库并推送

创建成功后，GitHub 会显示一个 "Quick setup" 页面，选择 **SSH** 标签，然后运行以下命令：

```bash
cd ~/projects/hermes-analyzer

# 添加远程仓库（SSH 方式，需要配置 SSH key）
git remote add origin git@github.com:stephenki/hermes-analyzer.git

# 推送 main 分支
git push -u origin main
```

### 第 3 步：验证

访问：https://github.com/stephenki/hermes-analyzer

应该能看到所有代码文件。

---

## 方式二：使用 gh CLI（如果已安装）

如果你本地安装了 `gh` 命令行工具，可以自动创建：

```bash
cd ~/projects/hermes-analyzer
gh repo create hermes-analyzer --public --source=. --remote=origin --description="Hermes AI Agent conversation analyzer"
git push -u origin main
```

---

## 🔐 SSH Key 配置检查

如果推送时出现 "Permission denied" 错误，说明 SSH key 未配置。运行：

```bash
# 检查是否有 SSH key
ls -la ~/.ssh/

# 应该看到 id_rsa 和 id_rsa.pub（或 ed25519 相关文件）
# 如果没有，生成新的：
ssh-keygen -t ed25519 -C "stephenki@users.noreply.github.com"

# 添加 SSH key 到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add -K ~/.ssh/id_ed25519

# 复制公钥到剪贴板
pbcopy < ~/.ssh/id_ed25519.pub

# 然后访问 GitHub Settings → SSH and GPG keys → New SSH key
# 粘贴公钥，标题任意
```

---

## 📝 当前项目状态

- **本地分支**: `main`
- **提交数**: 3 次
- **文件数**: 9 个（含 setup.py, README.md, LICENSE 等）
- **远程仓库**: ❌ 未配置

---

## ⚠️  常见问题

### 问题 1：`fatal: remote origin already exists.`
```bash
# 先删除旧的远程
git remote remove origin
# 再重新添加
git remote add origin git@github.com:stephenki/hermes-analyzer.git
```

### 问题 2：`remote: Repository not found.`
- 确认仓库已创建（访问 https://github.com/stephenki/hermes-analyzer）
- 确认远程 URL 拼写正确
- 确认 SSH key 已添加到 GitHub 账户

### 问题 3：`error: src refspec main does not match any`
```bash
# 确认分支名
git branch

# 如果是 master 而不是 main，推送时用：
git push -u origin master
```

---

## 🎯 快速命令摘要

```bash
# 完整推送流程
cd ~/projects/hermes-analyzer
git remote add origin git@github.com:stephenki/hermes-analyzer.git
git push -u origin main

# 后续更新推送
git add .
git commit -m "更新说明"
git push
```
