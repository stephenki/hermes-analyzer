# 🔍 Hermes Analyzer

**Hermes AI 代理对话分析工具** - 追踪 token 消耗、工具调用、成本估算，优化你的 AI 代理性能。

---

## ✨ Features / 功能特性

- 📊 **Session Statistics** - Total tokens, input/output breakdown, duration tracking
- 🔧 **Tool Analysis** - Per-tool call count and time consumption ranking
- 💰 **Cost Estimation** - Automatic cost calculation by model pricing (supports step, claude, gpt series)
- 📈 **Trend Reports** - HTML visualization with charts and trends
- 🎯 **Optimization Suggestions** - Data-driven performance improvement tips
- 🗂️ **Multi-language** - Full Chinese/English bilingual support

**中文**：
- 📊 **会话统计** - 总 tokens、输入/输出拆分、耗时统计
- 🔧 **工具分析** - 各工具调用次数和耗时排行
- 💰 **成本估算** - 自动按模型价格计算费用
- 📈 **趋势报告** - HTML 可视化报告，图表展示
- 🎯 **优化建议** - 基于数据自动给出性能优化提示
- 🗂️ **中英双语** - 完整的中英文支持

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

```bash
# From PyPI (after release)
pip install hermes-analyzer

# Or local install / 或本地安装
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
pip install -e .
```

### Basic Usage / 基础用法

```bash
# Analyze last 7 days of Hermes sessions / 分析最近 7 天的 Hermes 会话
hermes-analyzer analyze --days 7

# Analyze specific date range / 分析指定日期范围
hermes-analyzer analyze --since 2026-04-01 --until 2026-04-20

# Deep dive into single session / 深度分析单个会话
hermes-analyzer session ~/.hermes/sessions/session_cron_c846e16e31f9_20260420_070713.json

# Generate HTML visualization report / 生成 HTML 可视化报告
hermes-analyzer report --days 30 --output-dir ~/projects/hermes-reports/
```

### Command Line Interface / 命令行界面

```bash
# Show help / 显示帮助
hermes-analyzer --help

# Analyze sessions / 分析会话
hermes-analyzer analyze [OPTIONS]
  --days N              Analyze last N days (default: 7)
  --sessions-dir PATH   Hermes sessions directory (default: ~/.hermes/sessions)
  --output PATH         Save report to file (default: stdout)

# Single session analysis / 单个会话分析
hermes-analyzer session SESSION_FILE

# Generate HTML report / 生成 HTML 报告
hermes-analyzer report [OPTIONS]
  --days N              Analyze last N days (default: 30)
  --output-dir PATH     Output directory for HTML report
```

---

## 📊 Report Examples / 报告示例

### Markdown Summary / Markdown 摘要

```markdown
# 📊 Hermes 会话分析报告

**生成时间**: 2026-04-21 14:30
**时间范围**: 2026-04-14 ~ 2026-04-20 (7 个会话)

## 总体概况 / Overview

| 指标 | Value |
|------|-------|
| 总消耗 tokens | 98,450 |
| 输入 tokens | 82,450 |
| 输出 tokens | 42,130 |
| 平均每次会话 | 8,305 |
| 总耗时 | 347.2s |
| 估算成本 | $0.374 |

## 🔥 Top 5 Sessions by Token Usage

| Date | Session ID | Tokens | Cost | Operation |
|------|------------|--------|------|-----------|
| 04-20 | Chapter 23 学习 | 12,450 | $0.037 | Cron Task |
| 04-18 | OpenClaw 迁移 | 9,820 | $0.029 | Manual |

## 🔧 Tool Call Statistics

| Tool | Calls | Total Time | % |
|------|-------|------------|----|
| execute_code | 45 | 89.2s | 62% |
| read_file | 32 | 12.1s | 8% |

## 💡 Optimization Suggestions

1. 🔴 High average token usage - consider shortening prompts
2. 🟡 Frequent `execute_code` calls - try batching operations
3. 📈 Monitor high-consumption sessions for caching opportunities
```

### HTML Visualization / HTML 可视化

The HTML report includes:
- 📈 Token usage trend charts
- 🔧 Tool call distribution pie chart
- 📊 Cost breakdown by model
- 🎯 Performance metrics dashboard

HTML 报告包括：
- 📈 Token 消耗趋势图
- 🔧 工具调用分布饼图
- 📊 按模型划分的成本
- 🎯 性能指标面板

---

## 🔧 Data Sources / 数据源

The tool automatically scans:

| Path | Description |
|------|-------------|
| `~/.hermes/sessions/` | Hermes session logs (JSON format) |
| `~/.hermes/memory/` | Daily memory files (optional) |

**Hermes Session JSON Structure Example**:
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

## 🛠️ Development / 开发指南

### Project Structure / 项目结构

```
hermes-analyzer/
├── hermes_analyzer/
│   ├── __init__.py      # Package metadata / 包元数据
│   ├── cli.py           # CLI entry point / 命令行入口
│   ├── parser.py        # Session JSON parser / 会话解析器
│   ├── stats.py         # Statistics engine / 统计引擎
│   └── reporter.py      # Report generators / 报告生成器
├── setup.py             # Package configuration / 打包配置
├── requirements.txt     # Dependencies / 依赖列表
├── README.md           # This file / 本文件
├── LICENSE             # MIT License / MIT 许可证
└── .gitignore          # Git ignore rules / Git 忽略规则
```

### Local Development / 本地开发

```bash
# Clone and setup / 克隆并设置
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode / 开发模式安装
pip install -e .

# Run tests / 运行测试（如果有）
python -m pytest tests/

# Try it out / 试用
hermes-analyzer analyze --days 1
```

### Adding New Models / 添加新模型定价

Edit `hermes_analyzer/stats.py`:
```python
PRICING = {
    "step-3.5-flash-2603": {"input": 0.0000008, "output": 0.000002},
    "claude-3-opus": {"input": 0.000015, "output": 0.000075},
    "gpt-4": {"input": 0.00003, "output": 0.00006},  # Add your model / 添加模型
}
```

---

## 📈 Roadmap / 路线图

### v0.1.x - Current / 当前版本
- ✅ Session parsing and statistics / 会话解析和统计
- ✅ Markdown and HTML reports / Markdown 和 HTML 报告
- ✅ Cost estimation for common models / 常见模型成本估算

### v0.2.x - Next / 下一版本
- 🔄 Real-time monitoring mode (logtail + SQLite) / 实时监控模式
- 🔄 Feishu/Lark webhook integration / 飞书通知集成
- 🔄 More model pricing (GPT-4, Claude Sonnet, etc.) / 更多模型定价
- 🔄 Chart visualizations (matplotlib/plotly) / 图表可视化

### v0.3.x - Future / 未来版本
- 📊 Web Dashboard (Streamlit/FastAPI) / Web 仪表板
- 📊 Hermes Skill integration / Hermes Skill 集成
- 📊 Comparative analysis (period vs period) / 对比分析
- 📊 Token usage optimization recommendations / Token 优化建议

---

## 🤝 Contributing / 贡献

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

欢迎贡献！请随时提交 Issue 或 Pull Request。

### Steps / 步骤：
1. Fork the repository / Fork 仓库
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request / 提交 Pull Request

---

## 📄 License / 许可证

MIT License - See [LICENSE](LICENSE) file for details.

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 Acknowledgments / 致谢

- Inspired by the need to optimize Hermes Agent token usage
- Special thanks to **Stephen (stephenki)** for real-world testing and feedback
- Built for the Hermes AI Agent community

- 灵感来源于优化 Hermes Agent 的 token 消耗需求
- 特别感谢 **Stephen (stephenki)** 的真实场景测试和反馈
- 为 Hermes AI Agent 社区而生

---

## 📞 Contact / 联系方式

- **GitHub**: [stephenki](https://github.com/stephenki)
- **Repository**: [hermes-analyzer](https://github.com/stephenki/hermes-analyzer)
- **Issues**: [Report a bug or request feature](https://github.com/stephenki/hermes-analyzer/issues)

---

## ⭐ Star History / Stars 历史

If you find this tool useful, please give it a star! ⭐

如果觉得这个工具好用，请给个 Star！⭐

[![GitHub stars](https://img.shields.io/github/stars/stephenki/hermes-analyzer?style=social)](https://github.com/stephenki/hermes-analyzer/stargazers)
