# 🔍 Hermes Analyzer

**Hermes AI 代理对话分析工具** - 追踪 token 消耗、工具调用、成本估算，优化你的 AI 代理性能。

---

## ✨ 功能特性

- 📊 **会话统计** - 总 tokens、输入/输出拆分、耗时统计
- 🔧 **工具分析** - 各工具调用次数和耗时排行
- 💰 **成本估算** - 自动按模型价格计算费用（支持 step、claude、gpt 系列）
- 📈 **趋势报告** - HTML 可视化报告，图表展示消耗趋势
- 🎯 **优化建议** - 基于数据自动给出性能优化提示
- 🗂️ **中英双语** - 完整的中英文支持

---

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装（发布后）
pip install hermes-analyzer

# 或本地安装
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
pip install -e .
```

### 基础用法

```bash
# 分析最近 7 天的 Hermes 会话
hermes-analyzer analyze --days 7

# 分析指定日期范围
hermes-analyzer analyze --since 2026-04-01 --until 2026-04-20

# 深度分析单个会话
hermes-analyzer session ~/.hermes/sessions/session_cron_c846e16e31f9_20260420_070713.json

# 生成 HTML 可视化报告
hermes-analyzer report --days 30 --output-dir ~/projects/hermes-reports/
```

### 命令行界面

```bash
# 显示帮助
hermes-analyzer --help

# 分析会话
hermes-analyzer analyze [OPTIONS]
  --days N              分析最近 N 天（默认：7）
  --sessions-dir PATH   Hermes 会话目录（默认：~/.hermes/sessions）
  --output PATH         保存报告到文件（默认：stdout）

# 单个会话分析
hermes-analyzer session SESSION_FILE

# 生成 HTML 报告
hermes-analyzer report [OPTIONS]
  --days N              分析最近 N 天（默认：30）
  --output-dir PATH     HTML 报告输出目录
```

---

## 📊 报告示例

### Markdown 摘要

```markdown
# 📊 Hermes 会话分析报告

**生成时间**: 2026-04-21 14:30
**时间范围**: 2026-04-14 ~ 2026-04-20 (7 个会话)

## 总体概况

| 指标 | 数值 |
|------|------|
| 总消耗 tokens | 98,450 |
| 输入 tokens | 82,450 |
| 输出 tokens | 42,130 |
| 平均每次会话 | 8,305 |
| 总耗时 | 347.2s |
| 估算成本 | $0.374 |

## 🔥 消耗 Top 5 会话

| 日期 | 会话 ID | tokens | 成本 | 主要操作 |
|------|---------|--------|------|----------|
| 04-20 | Chapter 23 学习 | 12,450 | $0.037 | 定时任务 |
| 04-18 | OpenClaw 迁移 | 9,820 | $0.029 | 手动交互 |

## 🔧 工具调用统计

| 工具 | 调用次数 | 总耗时 | 占比 |
|------|----------|--------|------|
| execute_code | 45 | 89.2s | 62% |
| read_file | 32 | 12.1s | 8% |

## 💡 优化建议

1. 🔴 平均会话 token 消耗偏高，建议精简 prompt
2. 🟡 `execute_code` 工具调用频繁，可尝试合并调用
3. 📈 关注高消耗会话，分析是否可缓存中间结果
```

### HTML 可视化

HTML 报告包括：
- 📈 Token 消耗趋势图
- 🔧 工具调用分布饼图
- 📊 按模型划分的成本
- 🎯 性能指标面板

---

## 🔧 数据源

工具自动扫描以下目录：

| 路径 | 说明 |
|------|------|
| `~/.hermes/sessions/` | Hermes 会话日志（JSON 格式）|
| `~/.hermes/memory/` | 每日记忆文件（可选）|

**Hermes 会话 JSON 结构示例**：
```json
{
  "id": "session_cron_...",
  "created_at": "2026-04-20T07:07:13Z",
  "model": "step-3.5-flash-2603",
  "messages": [
    {
      "role": "assistant",
      "content": "...",
      "token_count": 4200,
      "tool_calls": [
        {
          "name": "execute_code",
          "duration_ms": 2100
        }
      ]
    }
  ]
}
```

---

## 🛠️ 开发指南

### 项目结构

```
hermes-analyzer/
├── hermes_analyzer/
│   ├── __init__.py      # 包元数据
│   ├── cli.py           # 命令行入口
│   ├── parser.py        # 会话 JSON 解析器
│   ├── stats.py         # 统计引擎
│   └── reporter.py      # 报告生成器
├── setup.py             # 打包配置
├── requirements.txt     # 依赖列表
├── README.md           # 英文版（默认）
├── README.zh.md        # 中文版
├── LICENSE             # MIT 许可证
└── .gitignore          # Git 忽略规则
```

### 本地开发

```bash
# 克隆并设置
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 开发模式安装
pip install -e .

# 运行测试（如有）
python -m pytest tests/

# 试用
hermes-analyzer analyze --days 1
```

### 添加新模型定价

编辑 `hermes_analyzer/stats.py`：
```python
PRICING = {
    "step-3.5-flash-2603": {"input": 0.0000008, "output": 0.000002},
    "claude-3-opus": {"input": 0.000015, "output": 0.000075},
    "gpt-4": {"input": 0.00003, "output": 0.00006},  # 添加你的模型
}
```

---

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

### 步骤：
1. Fork 仓库
2. 创建功能分支 (`git checkout -b feat/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feat/amazing-feature`)
5. 提交 Pull Request

---

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---
