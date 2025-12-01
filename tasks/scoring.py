from datetime import date, datetime
from typing import List, Dict, Set

def _parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value).date()
    except Exception:
        return None

def detect_cycle(tasks: List[Dict]) -> bool:
    # Simple cycle detection for dependency graph using DFS
    graph = {}
    for t in tasks:
        graph[t.get('id')] = t.get('dependencies', [])
    visited = {}
    def dfs(u):
        if visited.get(u) == 1:
            return True
        if visited.get(u) == 2:
            return False
        visited[u] = 1
        for v in graph.get(u, []):
            if dfs(v):
                return True
        visited[u] = 2
        return False
    for node in graph:
        if dfs(node):
            return True
    return False

def calculate_task_score(task: dict, tasks_by_id: dict):
    """Return a numeric score. Higher = higher priority."""
    score = 0
    today = date.today()
    due_date = _parse_date(task.get('due_date'))
    # Urgency
    if due_date:
        days_until = (due_date - today).days
        if days_until < 0:
            score += 200  # overdue gets a big boost
        elif days_until <= 3:
            score += 80
        elif days_until <= 7:
            score += 30
        else:
            score += max(0, 10 - days_until//30)  # small decay
    else:
        # no due date -> less urgent
        score += 0

    # Importance weighting
    importance = int(task.get('importance') or 5)
    score += importance * 5

    # Effort (quick wins)
    est = int(task.get('estimated_hours') or 1)
    if est <= 2:
        score += 20
    elif est <= 5:
        score += 5
    else:
        score -= 5

    # Dependencies: if other tasks depend on this task, raise its priority
    task_id = task.get('id')
    blocked_count = 0
    for t in tasks_by_id.values():
        if task_id in (t.get('dependencies') or []):
            blocked_count += 1
    score += blocked_count * 15

    # If this task has invalid data, penalize a bit to surface for manual fix
    if 'title' not in task or not task.get('title'):
        score -= 50

    return score

def analyze_tasks(tasks: List[dict]):
    # convert to dict by id (use index-based id if missing)
    tasks_by_id = {}
    for i, t in enumerate(tasks):
        tid = t.get('id') if t.get('id') is not None else str(i+1)
        t['id'] = tid
        tasks_by_id[tid] = t

    # detect cycle
    has_cycle = detect_cycle(tasks)
    results = []
    for t in tasks:
        score = calculate_task_score(t, tasks_by_id)
        results.append({**t, 'score': score})
    # sort descending by score
    results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)
    return {
        'has_cycle': has_cycle,
        'results': results_sorted
    }
