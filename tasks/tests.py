from django.test import TestCase
from .scoring import analyze_tasks, calculate_task_score

class ScoringTests(TestCase):
    def test_simple_scoring(self):
        tasks = [
            {'id':'a','title':'T1','due_date': None, 'importance': 5, 'estimated_hours':1, 'dependencies': []},
            {'id':'b','title':'T2','due_date': None, 'importance': 9, 'estimated_hours':4, 'dependencies': []},
        ]
        out = analyze_tasks(tasks)
        self.assertEqual(len(out['results']), 2)
        # Ensure higher importance gets higher score
        self.assertTrue(out['results'][0]['score'] >= out['results'][1]['score'])

    def test_overdue_boost(self):
        import datetime
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        tasks = [{'id':'x','title':'Overdue','due_date': yesterday, 'importance':1, 'estimated_hours':5, 'dependencies': []}]
        out = analyze_tasks(tasks)
        self.assertTrue(out['results'][0]['score'] > 0)
