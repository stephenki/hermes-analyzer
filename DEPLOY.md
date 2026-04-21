## 🚀 GitHub 仓库创建指南

### 方式一：自动部署（需安装 gh CLI）

```bash
cd ~/projects/hermes-analyzer
bash deploy.sh
# 或手动执行:
gh repo create hermes-analyzer --public --source=. --remote=origin --description="Hermes AI Agent conversation analyzer"
git push -u origin main
```

### 方式二：手动创建（推荐）

1. **访问** https://github.com/new
2. **填写信息**：
   - Owner: stephenki
   - Repository name: `hermes-analyzer`
   - Description: `Hermes AI Agent conversation analyzer - Track token usage, tool calls, and costs`
   - Visibility: Public
   - ✅ 勾选 "Add a README file"（创建空仓库）
3. **点击 Create repository**

4. **推送本地代码**：
```bash
cd ~/projects/hermes-analyzer

# 添加远程仓库（使用 SSH）
git remote add origin git@github.com:stephenki/hermes-analyzer.git

# 推送主分支
git push -u origin main
```

---

## 🎯 快速测试

```bash
# 本地安装（开发模式）
cd ~/projects/hermes-analyzer
pip install -e .

# 查看帮助
hermes-analyzer --help

# 测试分析最近 1 天的会话
hermes-analyzer analyze --days 1

# 生成 HTML 可视化报告
hermes-analyzer report --days 7 --output-dir ~/projects/hermes-reports/
```

---

## 📊 功能特性

- ✅ **会话统计**：总 tokens、输入/输出拆分、耗时
- ✅ **工具分析**：各工具调用次数和耗时排行
- ✅ **成本估算**：自动按模型价格计算费用
- ✅ **报告生成**：Markdown 文本报告 + HTML 可视化
- ✅ **灵活筛选**：按时间范围、单个会话深度分析
