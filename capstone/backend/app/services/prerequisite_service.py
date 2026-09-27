from __future__ import annotations
from typing import Dict, List, Set

from backend.app.knowledge_base.prerequisite_graph import (
    PREREQUISITE_RULES,
    PREREQUISITE_EXPLANATIONS,
    get_prerequisites_for_skill as kb_get_prereqs,
    explain_prerequisite_need,
    detect_cycle,
    topological_sort,
    build_prerequisite_subgraph,
)


def get_prerequisites_for_skill(skill: str) -> List[str]:
    """Retrieve direct rule-based prerequisites for a skill."""
    return kb_get_prereqs(skill)


def build_prerequisite_graph(skills: List[str]) -> Dict[str, List[str]]:
    """Build a prerequisite dictionary mapping each skill to its direct prerequisites."""
    graph: Dict[str, List[str]] = {}
    for skill in skills:
        graph[skill] = get_prerequisites_for_skill(skill)
    return graph


def order_skills(graph: Dict[str, List[str]]) -> List[str]:
    """
    Topologically order skills so that prerequisite skills precede dependent skills.
    Detects and raises ValueError on cycle.
    """
    return topological_sort(graph)


def explain_prerequisites(skill: str) -> str:
    """Explain why a skill requires its prerequisites (marked clearly as rule-based educational guidance)."""
    return explain_prerequisite_need(skill)


def get_all_prerequisites_transitive(skill: str) -> List[str]:
    """Compute all transitive prerequisites for a skill in topological order."""
    subgraph = build_prerequisite_subgraph([skill])
    try:
        ordered = topological_sort(subgraph)
        # Exclude the target skill itself
        return [s for s in ordered if s != skill]
    except ValueError:
        return []
