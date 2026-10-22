#!/usr/bin/env python3
"""Build a self-contained Kaggle notebook from solver.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
solver = (ROOT / 'solver.py').read_text()
markdown = '''# ARC-AGI-2 RuleLab — ARC Prize 2026\n\nAn interpretable program-synthesis baseline. This notebook uses no network calls. It searches a bounded language of grid symmetries, background crops, and global colour mappings; emits exactly two guesses per test input; and writes `submission.json`.\n\n**Research status:** This is a baseline, not a leaderboard claim. No private-set score or Kaggle submission ID is asserted. Do not use the public evaluation split for iterative tuning.\n\n## 1. Solver\nThe following cell is inlined so this notebook remains runnable when submitted offline on Kaggle.\n'''
runtime = '''from pathlib import Path\nimport json\n\nINPUT_ROOT = Path('/kaggle/input')\nOUTPUT_PATH = Path('/kaggle/working/submission.json')\n\ndef is_task(x):\n    return isinstance(x, dict) and isinstance(x.get('train'), list) and isinstance(x.get('test'), list)\n\ndef discover_tasks(root):\n    paths = [p for p in root.rglob('*.json')\n             if 'sample_submission' not in p.name.lower()\n             and 'solution' not in p.name.lower()]\n    explicit_test = [p for p in paths\n                     if 'test' in p.name.lower() and 'challenge' in p.name.lower()]\n    candidates = explicit_test or [p for p in paths\n                                   if 'training' not in str(p).lower()\n                                   and 'train_' not in p.name.lower()]\n    found = {}\n    for path in candidates:\n        try:\n            obj = json.loads(path.read_text())\n        except Exception:\n            continue\n        if is_task(obj):\n            found[path.stem] = obj\n        elif isinstance(obj, dict):\n            for task_id, task in obj.items():\n                if is_task(task):\n                    found[str(task_id)] = task\n    return found\n\ntasks = discover_tasks(INPUT_ROOT)\nif not tasks:\n    raise FileNotFoundError(f'No ARC test challenge JSON found under {INPUT_ROOT}. Attach the ARC-AGI-2 competition dataset to this notebook.')\nsubmission = kaggle_payload(tasks)\nOUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)\nOUTPUT_PATH.write_text(json.dumps(submission, separators=(',', ':')))\nprint(f'Tasks: {len(submission)} | test outputs: {sum(len(v) for v in submission.values())}')\nprint(f'Saved: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)')\nassert all(len(items) == len(tasks[task_id]['test']) for task_id, items in submission.items())\nassert all(set(item) == {'attempt_1', 'attempt_2'} for items in submission.values() for item in items)\n'''
cells = [
    {'cell_type': 'markdown', 'metadata': {}, 'source': markdown.splitlines(True)},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': solver.splitlines(True)},
    {'cell_type': 'markdown', 'metadata': {}, 'source': ['## 2. Discover attached test challenges and create the file\n', 'This cell prefers competition files explicitly named as test challenges, excludes training/solution files, and writes the two-attempt prediction object. It makes no network calls.\n']},
    {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': runtime.splitlines(True)},
]
notebook = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'name': 'python', 'version': '3.10+'}}, 'nbformat': 4, 'nbformat_minor': 5}
out = ROOT / 'notebooks' / 'arc_prize_2026_rulelab.ipynb'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(notebook, indent=1) + '\n')
print(f'Wrote {out}')
