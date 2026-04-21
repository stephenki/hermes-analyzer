"""会话日志解析器"""

import json
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionStats:
    """单个会话统计"""
    session_id: str
    date: str
    model: str
    total_tokens: int
    input_tokens: int
    output_tokens: int
    duration_sec: float
    tool_calls: list
    file_path: Path


def parse_session(file_path: Path) -> SessionStats:
    """解析单个会话 JSON 文件"""
    with open(file_path) as f:
        data = json.load(f)
    
    messages = data.get("messages", [])
    
    # 计算 token 分布
    total_tokens = sum(m.get("token_count", 0) for m in messages)
    input_tokens = sum(
        m.get("token_count", 0) 
        for m in messages 
        if m.get("role") in ["user", "system"]
    )
    output_tokens = sum(
        m.get("token_count", 0) 
        for m in messages 
        if m.get("role") == "assistant"
    )
    
    # 工具调用耗时
    tool_time_ms = sum(
        call.get("duration_ms", 0)
        for msg in messages
        for call in msg.get("tool_calls", [])
    )
    duration_sec = tool_time_ms / 1000.0
    
    # 提取工具调用列表
    tool_calls = []
    for msg in messages:
        for call in msg.get("tool_calls", []):
            tool_calls.append({
                "tool": call.get("name", "unknown"),
                "duration_ms": call.get("duration_ms", 0),
            })
    
    return SessionStats(
        session_id=data.get("id", "unknown"),
        date=data.get("created_at", "")[:10],
        model=data.get("model", "unknown"),
        total_tokens=total_tokens,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        duration_sec=duration_sec,
        tool_calls=tool_calls,
        file_path=file_path,
    )
