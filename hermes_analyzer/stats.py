"""统计计算逻辑"""

from collections import Counter, defaultdict
from typing import List, Dict
from .parser import SessionStats


def aggregate_sessions(sessions: List[SessionStats]) -> Dict:
    """聚合多个会话的统计"""
    if not sessions:
        return {"error": "无会话数据"}
    
    total_tokens = sum(s.total_tokens for s in sessions)
    total_input = sum(s.input_tokens for s in sessions)
    total_output = sum(s.output_tokens for s in sessions)
    total_duration = sum(s.duration_sec for s in sessions)
    total_cost = estimate_cost(sessions)
    
    # 工具调用统计
    tool_counter = Counter()
    tool_time = defaultdict(float)
    for s in sessions:
        for call in s.tool_calls:
            tool = call["tool"]
            tool_counter[tool] += 1
            tool_time[tool] += call["duration_ms"] / 1000.0
    
    # 按 token 排序会话
    top_sessions = sorted(sessions, key=lambda s: s.total_tokens, reverse=True)[:5]
    
    return {
        "total_sessions": len(sessions),
        "date_range": {
            "start": sessions[-1].date if sessions else "",
            "end": sessions[0].date if sessions else "",
        },
        "tokens": {
            "total": total_tokens,
            "input": total_input,
            "output": total_output,
            "avg_per_session": total_tokens // len(sessions) if sessions else 0,
        },
        "cost_usd": total_cost,
        "duration_sec": total_duration,
        "top_sessions": top_sessions,
        "tools": [
            {
                "name": tool,
                "count": count,
                "time_sec": tool_time[tool],
                "percentage": tool_time[tool] / total_duration * 100 if total_duration > 0 else 0,
            }
            for tool, count in tool_counter.most_common()
        ],
    }


PRICING = {
    "step-3.5-flash-2603": {
        "input": 0.0000008,   # $0.80 / 1M tokens
        "output": 0.000002,   # $2.00 / 1M tokens
    },
    "claude-3-opus": {
        "input": 0.000015,
        "output": 0.000075,
    },
}


def estimate_cost(sessions: List[SessionStats]) -> float:
    """估算总成本（USD）"""
    total = 0.0
    for s in sessions:
        price = PRICING.get(s.model, {
            "input": 0.000001,
            "output": 0.000003,
        })
        total += s.input_tokens * price["input"]
        total += s.output_tokens * price["output"]
    return total
