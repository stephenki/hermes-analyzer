"""报告生成器"""

from datetime import datetime
from typing import List, Dict
from .parser import SessionStats
from .stats import aggregate_sessions


def format_number(n: int) -> str:
    """千位分隔格式化"""
    return f"{n:,}"


def format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs}s"


def generate_markdown_summary(stats: Dict, sessions: List[SessionStats]) -> str:
    """生成 Markdown 摘要报告"""
    lines = []
    
    lines.append("# 📊 Hermes 会话分析报告\n")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"**时间范围**: {stats['date_range']['start']} ~ {stats['date_range']['end']}\n")
    lines.append(f"**会话总数**: {stats['total_sessions']} 个\n\n")
    
    lines.append("## 总体概况\n")
    lines.append("| 指标 | 数值 |\n")
    lines.append("|------|------|\n")
    lines.append(f"| 总消耗 tokens | {format_number(stats['tokens']['total'])} |\n")
    lines.append(f"| 输入 tokens | {format_number(stats['tokens']['input'])} |\n")
    lines.append(f"| 输出 tokens | {format_number(stats['tokens']['output'])} |\n")
    lines.append(f"| 平均每次会话 | {format_number(stats['tokens']['avg_per_session'])} |\n")
    lines.append(f"| 总耗时 | {format_duration(stats['duration_sec'])} |\n")
    lines.append(f"| 估算成本 | ${stats['cost_usd']:.3f} |\n\n")
    
    if stats.get("top_sessions"):
        lines.append("## 🔥 消耗 Top 5 会话\n")
        lines.append("| 日期 | 会话 ID | tokens | 成本 | 主要操作 |\n")
        lines.append("|------|---------|--------|------|----------|\n")
        for s in stats["top_sessions"]:
            cost = s.input_tokens * 0.0000008 + s.output_tokens * 0.000002
            op = "定时任务" if "cron" in s.session_id else "手动交互" if "manual" in s.session_id else "未知"
            lines.append(f"| {s.date} | {s.session_id[:30]}... | {format_number(s.total_tokens)} | ${cost:.3f} | {op} |\n")
        lines.append("\n")
    
    if stats.get("tools"):
        lines.append("## 🔧 工具调用统计\n")
        lines.append("| 工具 | 调用次数 | 总耗时 | 占比 |\n")
        lines.append("|------|----------|--------|------|\n")
        for tool in stats["tools"][:10]:
            lines.append(
                f"| {tool['name']} | {tool['count']} | {format_duration(tool['time_sec'])} | {tool['percentage']:.1f}% |\n"
            )
        lines.append("\n")
    
    lines.append("## 💡 优化建议\n")
    if stats["total_sessions"] > 0:
        avg_tokens = stats["tokens"]["avg_per_session"]
        if avg_tokens > 10000:
            lines.append("1. 🔴 平均会话 token 消耗较高，建议：\n")
            lines.append("   - 检查 prompt 长度，精简系统提示\n")
            lines.append("   - 考虑分块处理长文本\n")
        if stats.get("tools") and stats["tools"][0]["count"] > 20:
            top_tool = stats["tools"][0]
            lines.append(f"2. 🟡 `{top_tool['name']}` 工具调用频繁（{top_tool['count']} 次），可尝试合并调用。\n")
        lines.append("3. 📈 关注高消耗会话，分析是否可缓存中间结果。\n")
    
    return "".join(lines)


def generate_html_report(stats: Dict, sessions: List[SessionStats], output_path: str):
    """生成 HTML 可视化报告（简化版）"""
    tool_rows = []
    for tool in stats.get("tools", [])[:10]:
        tool_rows.append(
            f"                <tr>\n"
            f"                    <td>{tool['name']}</td>\n"
            f"                    <td>{tool['count']}</td>\n"
            f"                    <td>{tool['time_sec']:.1f}s</td>\n"
            f"                    <td>{tool['percentage']:.1f}%</td>\n"
            f"                </tr>\n"
        )
    
    total_sessions = stats['total_sessions']
    total_tokens = format_number(stats['tokens']['total'])
    cost_usd = stats['cost_usd']
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hermes Analyzer Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .card {{ border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 8px; }}
        .metric {{ font-size: 24px; font-weight: bold; color: #0066cc; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>📊 Hermes 会话分析报告</h1>
    <p><strong>生成时间</strong>: {now}</p>
    <p><strong>会话总数</strong>: <span class="metric">{total_sessions}</span></p>
    <p><strong>总消耗 tokens</strong>: <span class="metric">{total_tokens}</span></p>
    <p><strong>估算成本</strong>: ${cost_usd:.3f}</p>
    
    <div class="card">
        <h2>工具调用排行</h2>
        <table>
            <tr><th>工具</th><th>调用次数</th><th>总耗时</th><th>占比</th></tr>
{''.join(tool_rows)}
        </table>
    </div>
</body>
</html>
'''
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML 报告已生成: {output_path}")
