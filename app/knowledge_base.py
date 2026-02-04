"""
Knowledge base loading helpers for ASC troubleshooting content.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List


KnowledgeBaseType = Dict[str, Dict[str, List[str]]]


@lru_cache(maxsize=1)
def load_knowledge_base() -> KnowledgeBaseType:
    """
    Load troubleshooting content from data/knowledge_base.json.
    """
    kb_path = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
    with kb_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        return {}
    return data


def get_steps(product: str, problem: str) -> List[str]:
    """
    Return troubleshooting steps for a product/problem pair.
    """
    return list(load_knowledge_base().get(product, {}).get(problem, []))


def get_max_steps(product: str, problem: str, default: int = 3) -> int:
    """
    Return configured step count for a product/problem pair.
    """
    steps = get_steps(product, problem)
    return len(steps) if steps else max(1, int(default))

