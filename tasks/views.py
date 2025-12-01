import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .scoring import analyze_tasks

@csrf_exempt
def analyze_view(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        data = json.loads(request.body.decode('utf-8'))
        if isinstance(data, dict) and data.get('tasks') is not None:
            tasks = data.get('tasks')
        elif isinstance(data, list):
            tasks = data
        else:
            return HttpResponseBadRequest('Invalid payload: expected list or {"tasks": [...] }')
        out = analyze_tasks(tasks)
        return JsonResponse(out, safe=False)
    except Exception as e:
        return HttpResponseBadRequest(str(e))

from .scoring import calculate_task_score
from datetime import date
def explain_score(task):
    # create a short explanation
    parts = []
    today = date.today()
    due = task.get('due_date')
    if due:
        parts.append(f"Due {due}")
    parts.append(f"Importance {task.get('importance',5)}")
    parts.append(f"Est hours {task.get('estimated_hours',1)}")
    return '; '.join(parts)

def suggest_view(request):
    # For demo, load sample tasks from query param or fallback example
    sample = request.GET.get('sample')
    import json
    tasks = []
    if sample:
        try:
            tasks = json.loads(sample)
        except:
            tasks = []
    else:
        # Minimal example
        tasks = [
            {"id":"1","title":"Fix login","due_date":None,"importance":9,"estimated_hours":2,"dependencies":[]},
            {"id":"2","title":"Write docs","due_date":None,"importance":6,"estimated_hours":1,"dependencies":[]},
            {"id":"3","title":"Release v1","due_date":None,"importance":10,"estimated_hours":8,"dependencies":["1"]},
        ]
    out = analyze_tasks(tasks)
    top3 = out['results'][:3]
    suggestions = []
    for t in top3:
        suggestions.append({
            'task': t,
            'explanation': explain_score(t)
        })
    return JsonResponse({'suggestions': suggestions, 'has_cycle': out['has_cycle']})
