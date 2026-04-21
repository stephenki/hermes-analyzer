"""命令行入口"""

import argparse
from pathlib import Path
from datetime import datetime
from .parser import parse_session
from .stats import aggregate_sessions
from .reporter import generate_markdown_summary, generate_html_report, format_number, format_duration


def find_sessions(sessions_dir: Path, days: int = 7) -> list:
    """查找最近的会话文件"""
    if not sessions_dir.exists():
        return []
    files = list(sessions_dir.glob("*.json"))
    # 按修改时间排序
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    # 筛选天数
    cutoff = datetime.now().timestamp() - days * 86400
    return [f for f in files if f.stat().st_mtime > cutoff]


def main():
    parser = argparse.ArgumentParser(
        prog="hermes-analyzer",
        description="Hermes AI 代理对话分析工具 - 统计 token 消耗、工具调用、成本估算",
        epilog="示例: hermes-analyzer analyze --days 7"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析会话统计")
    analyze_parser.add_argument("--days", type=int, default=7, help="分析最近 N 天的数据")
    analyze_parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".hermes" / "sessions",
                               help="Hermes 会话目录路径")
    analyze_parser.add_argument("--output", type=Path, default=None,
                               help="输出报告路径（默认打印到 stdout）")
    
    # session 命令（单个会话深度分析）
    session_parser = subparsers.add_parser("session", help="分析单个会话")
    session_parser.add_argument("session_file", type=Path, help="会话 JSON 文件路径")
    
    # report 命令（生成 HTML 报告）
    report_parser = subparsers.add_parser("report", help="生成可视化 HTML 报告")
    report_parser.add_argument("--days", type=int, default=30)
    report_parser.add_argument("--output-dir", type=Path, 
                              default=Path.home() / "projects" / "hermes-analyzer-reports")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        run_analyze(args)
    elif args.command == "session":
        run_session(args)
    elif args.command == "report":
        run_report(args)
    else:
        parser.print_help()


def run_analyze(args):
    sessions_dir = args.sessions_dir
    
    if not sessions_dir.exists():
        print(f"❌ 会话目录不存在: {sessions_dir}")
        return
    
    # 查找会话文件
    session_files = find_sessions(sessions_dir, args.days)
    
    if not session_files:
        print("⚠️  未找到会话文件")
        return
    
    print(f"🔍 找到 {len(session_files)} 个会话文件（最近 {args.days} 天）
")
    
    # 解析所有会话
    sessions = []
    for f in session_files:
        try:
            s = parse_session(f)
            sessions.append(s)
        except Exception as e:
            print(f"  ⚠️  跳过 {f.name}: {e}")
    
    if not sessions:
        print("❌ 没有可分析的会话数据")
        return
    
    # 按日期排序（新的在前）
    sessions.sort(key=lambda s: s.date, reverse=True)
    
    # 聚合统计
    stats = aggregate_sessions(sessions)
    
    # 生成报告
    report = generate_markdown_summary(stats, sessions)
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存: {args.output}")
    else:
        print("
" + "="*60)
        print(report)


def run_session(args):
    """分析单个会话"""
    file_path = args.session_file
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return
    
    s = parse_session(file_path)
    print(f"
📄 会话详情: {s.session_id}")
    print(f"   日期: {s.date}")
    print(f"   模型: {s.model}")
    print(f"   总 tokens: {format_number(s.total_tokens)}")
    print(f"   输入: {format_number(s.input_tokens)} | 输出: {format_number(s.output_tokens)}")
    print(f"   工具耗时: {format_duration(s.duration_sec)}")
    print(f"   工具调用: {len(s.tool_calls)} 次")
    
    if s.tool_calls:
        print("
   🔧 工具调用详情:")
        for i, call in enumerate(s.tool_calls[:10], 1):
            print(f"     {i}. {call['tool']} - {call['duration_ms']}ms")
        if len(s.tool_calls) > 10:
            print(f"     ... 还有 {len(s.tool_calls) - 10} 次调用")


def run_report(args):
    """生成 HTML 可视化报告"""
    sessions_dir = Path.home() / ".hermes" / "sessions"
    session_files = find_sessions(sessions_dir, args.days)
    
    sessions = []
    for f in session_files:
        try:
            sessions.append(parse_session(f))
        except:
            pass
    
    sessions.sort(key=lambda s: s.date, reverse=True)
    stats = aggregate_sessions(sessions)
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = args.output_dir / f"report-{datetime.now().strftime('%Y%m%d')}.html"
    generate_html_report(stats, sessions, str(output_file))


if __name__ == "__main__":
    main()
