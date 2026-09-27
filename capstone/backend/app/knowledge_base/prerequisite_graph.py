from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

# Curated, domain-informed prerequisite rules for online education
# Key: Target Skill, Value: List of Direct Prerequisite Skills
PREREQUISITE_RULES: Dict[str, List[str]] = {
    # Programming & Foundations
    'Python': ['Programming'],
    'Java': ['Programming'],
    'C++': ['Programming'],
    'JavaScript': ['Programming'],
    'Data Structures': ['Programming'],
    'Algorithms': ['Data Structures'],
    'Software Development': ['Algorithms', 'Programming'],
    'APIs': ['Programming', 'Networking'],
    'Databases': ['Programming'],
    'SQL': ['Databases'],

    # Data Analytics & Science
    'Excel': [],
    'Statistics': ['Mathematics'],
    'Mathematics': [],
    'Programming': [],
    'Data Analysis': ['Python', 'SQL', 'Statistics'],
    'Data Visualization': ['Data Analysis'],
    'Pandas': ['Python'],
    'NumPy': ['Python'],
    'Power BI': ['Data Analysis', 'Excel'],
    'Tableau': ['Data Analysis'],

    # Machine Learning & AI
    'Machine Learning': ['Python', 'Statistics', 'Mathematics', 'NumPy', 'Pandas'],
    'Scikit-learn': ['Python', 'Machine Learning'],
    'Deep Learning': ['Machine Learning', 'Mathematics'],
    'TensorFlow': ['Deep Learning', 'Python'],
    'PyTorch': ['Deep Learning', 'Python'],
    'NLP': ['Deep Learning', 'Python'],
    'Computer Vision': ['Deep Learning', 'Python'],
    'Model Deployment': ['Machine Learning', 'Docker', 'APIs'],

    # Cloud & DevOps
    'Linux': [],
    'Networking': [],
    'Cloud Computing': ['Linux', 'Networking'],
    'AWS': ['Cloud Computing'],
    'Azure': ['Cloud Computing'],
    'GCP': ['Cloud Computing'],
    'Docker': ['Linux'],
    'Kubernetes': ['Docker', 'Cloud Computing'],
    'DevOps': ['Docker', 'Cloud Computing', 'Git'],
    'Git': [],
    'GitHub': ['Git'],

    # Data Engineering
    'Data Engineering': ['SQL', 'Python', 'Databases', 'Cloud Computing'],
    'Big Data': ['Data Engineering'],
    'Spark': ['Big Data', 'Python'],
    'Kafka': ['Data Engineering'],
}

# Human-readable educational rationale for prerequisites
PREREQUISITE_EXPLANATIONS: Dict[str, str] = {
    'Machine Learning': 'Machine Learning relies on statistical concepts (distributions, hypothesis testing) and Python vector manipulation (NumPy/Pandas) for feature engineering and model training.',
    'Deep Learning': 'Deep Learning requires understanding machine learning loss functions, optimization, gradient descent, and linear algebra.',
    'Data Analysis': 'Data Analysis combines querying structured datasets via SQL with exploratory data manipulation in Python and basic statistics.',
    'Model Deployment': 'Deploying models in production requires building REST APIs, containerizing environments with Docker, and cloud hosting.',
    'Cloud Computing': 'Cloud platforms build heavily on operating systems (Linux) and computer networking fundamentals (IP, subnets, DNS, HTTP).',
    'Kubernetes': 'Kubernetes orchestrates containerized workloads, making containerization with Docker a necessary stepping stone.',
    'Algorithms': 'Algorithms require understanding elementary data structures like arrays, trees, and linked lists to analyze time/space complexity.',
    'Scikit-learn': 'Scikit-learn provides standard Python implementations of machine learning models, requiring solid Python and ML principles.',
    'NLP': 'Natural Language Processing applies deep learning sequence models and word embeddings to text token streams.',
    'Computer Vision': 'Computer Vision utilizes convolutional neural networks and tensor image transformations on top of deep learning.',
    'Data Engineering': 'Data Engineering builds robust pipelines moving data from transactional SQL databases into cloud warehouses.',
    'Spark': 'Apache Spark provides distributed in-memory computing for big data architectures using Python/Scala.',
}


def get_prerequisites_for_skill(skill: str) -> List[str]:
    """Retrieve direct prerequisites for a given canonical skill."""
    return PREREQUISITE_RULES.get(skill, [])


def explain_prerequisite_need(skill: str) -> str:
    """Provide rule-based educational reasoning for why prerequisites are required."""
    if skill in PREREQUISITE_EXPLANATIONS:
        return PREREQUISITE_EXPLANATIONS[skill]
    prereqs = get_prerequisites_for_skill(skill)
    if prereqs:
        return f"{skill} builds on prerequisite competencies: {', '.join(prereqs)}."
    return f"{skill} is a foundational or self-contained skill with no strict prerequisites."


def detect_cycle(graph: Dict[str, List[str]]) -> bool:
    """Detect if there is any circular dependency cycle in the directed prerequisite graph."""
    visited: Set[str] = set()
    recursion_stack: Set[str] = set()

    def _has_cycle(node: str) -> bool:
        visited.add(node)
        recursion_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if _has_cycle(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True
        recursion_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if _has_cycle(node):
                return True
    return False


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """
    Perform topological sort on graph adjacency list where edges u -> v represent u precedes v.
    """
    if detect_cycle(graph):
        raise ValueError("Cycle detected in prerequisite graph. Cannot compute valid learning sequence.")

    all_nodes = set(graph.keys())
    for nxt_list in graph.values():
        all_nodes.update(nxt_list)

    indegree: Dict[str, int] = {node: 0 for node in all_nodes}
    for nxt_list in graph.values():
        for nxt in nxt_list:
            indegree[nxt] += 1

    queue = deque(sorted([node for node, deg in indegree.items() if deg == 0]))
    ordered: List[str] = []

    while queue:
        curr = queue.popleft()
        ordered.append(curr)
        for nxt in graph.get(curr, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(ordered) != len(all_nodes):
        raise ValueError("Cycle detected in prerequisite graph.")

    return ordered


def build_prerequisite_subgraph(skills: List[str]) -> Dict[str, List[str]]:
    """Build a prerequisite subgraph for a specific set of skills, including direct and indirect prerequisites."""
    subgraph: Dict[str, List[str]] = {}
    to_visit = list(skills)
    seen: Set[str] = set()

    while to_visit:
        skill = to_visit.pop(0)
        if skill in seen:
            continue
        seen.add(skill)
        prereqs = get_prerequisites_for_skill(skill)
        subgraph[skill] = prereqs
        for p in prereqs:
            if p not in seen:
                to_visit.append(p)

    return subgraph
