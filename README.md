# 🔍 Hermes Analyzer

**Hermes AI Agent Conversation Analyzer** - Track token usage, tool calls, and cost estimation to optimize your AI agent performance.

---

## ✨ Features

- 📊 **Session Statistics** - Total tokens, input/output breakdown, duration tracking
- 🔧 **Tool Analysis** - Per-tool call count and time consumption ranking
- 💰 **Cost Estimation** - Automatic cost calculation by model pricing (supports step, claude, gpt series)
- 📈 **Trend Reports** - HTML visualization with charts and trends
- 🎯 **Optimization Suggestions** - Data-driven performance improvement tips
- 🗂️ **Bilingual** - Full Chinese/English support

---

## 🚀 Quick Start

### Installation

```bash
# From PyPI (after release)
pip install hermes-analyzer

# Or local install
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
pip install -e .
```

### Basic Usage

```bash
# Analyze last 7 days of Hermes sessions
hermes-analyzer analyze --days 7

# Analyze specific date range
hermes-analyzer analyze --since 2026-04-01 --until 2026-04-20

# Deep dive into single session
hermes-analyzer session ~/.hermes/sessions/session_cron_c846e16e31f9_20260420_070713.json

# Generate HTML visualization report
hermes-analyzer report --days 30 --output-dir ~/projects/hermes-reports/
```

### Command Line Interface

```bash
# Show help
hermes-analyzer --help

# Analyze sessions
hermes-analyzer analyze [OPTIONS]
  --days N              Analyze last N days (default: 7)
  --sessions-dir PATH   Hermes sessions directory (default: ~/.hermes/sessions)
  --output PATH         Save report to file (default: stdout)

# Single session analysis
hermes-analyzer session SESSION_FILE

# Generate HTML report
hermes-analyzer report [OPTIONS]
  --days N              Analyze last N days (default: 30)
  --output-dir PATH     Output directory for HTML report
```

---

## 📊 Report Examples

### Markdown Summary

```markdown
# 📊 Hermes Session Analysis Report

**Generated**: 2026-04-21 14:30
**Period**: 2026-04-14 ~ 2026-04-20 (7 sessions)

## Overview

| Metric | Value |
|--------|-------|
| Total Tokens | 98,450 |
| Input Tokens | 82,450 |
| Output Tokens | 42,130 |
| Avg per Session | 8,305 |
| Total Duration | 347.2s |
| Estimated Cost | $0.374 |

## 🔥 Top 5 Sessions

| Date | Session ID | Tokens | Cost | Operation |
|------|------------|--------|------|-----------|
| 04-20 | Chapter 23 study | 12,450 | $0.037 | Cron Task |
| 04-18 | OpenClaw migration | 9,820 | $0.029 | Manual |

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

### HTML Visualization

The HTML report includes:
- 📈 Token usage trend charts
- 🔧 Tool call distribution pie chart
- 📊 Cost breakdown by model
- 🎯 Performance metrics dashboard

---

## 🔧 Data Sources

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

## 🛠️ Development

### Project Structure

```
hermes-analyzer/
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
├── README.md           # English documentation (default)
├── README.zh.md        # 中文文档 / Chinese documentation
├── requirements.txt    # Python dependencies
├── setup.py            # Package installation configuration
├── docs/               # Additional documentation ( upcoming )
├── examples/           # Example usage and configurations ( upcoming )
├── tests/              # Unit and integration tests ( upcoming )
└── hermes_analyzer/    # Core Python package
    ├── __init__.py     # Package metadata (version: 0.1.0)
    ├── cli.py          # Command-line interface entry point
    ├── parser.py       # Hermes session JSON log parser
    ├── stats.py        # Statistics aggregation & cost estimation
    └── reporter.py     # Markdown & HTML report generators
```

### Local Development

```bash
# Clone and setup
git clone https://github.com/stephenki/hermes-analyzer.git
cd hermes-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest tests/

# Try it out
hermes-analyzer analyze --days 1
```

### Adding New Models

Edit `hermes_analyzer/stats.py`:
```python
PRICING = {
    "step-3.5-flash-2603": {"input": 0.0000008, "output": 0.000002},
    "claude-3-opus": {"input": 0.000015, "output": 0.000075},
    "gpt-4": {"input": 0.00003, "output": 0.00006},  # Add your model
}
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---
