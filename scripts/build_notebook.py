#!/usr/bin/env python3
"""Build a self-contained Kaggle notebook from solver.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
solver = (ROOT / "solver.py").read_text()
markdown = '''# ARC-AGI-2 RuleLab — ARC Prize 2026

An interpretable program-synthesis baseline. This notebook uses no network calls. It searches a bounded language of grid symmetries, background crops, demonstration-derived uniform integer cell scaling, and global colour mappings; emits exactly two guesses per test input; and writes `submission.json`.

**Research status:** This is a baseline, not a leaderboard claim. No private-set score or Kaggle submission ID is asserted. Do not use the public evaluation split for iterative tuning.

## 1. Solver
The following cell is inlined so this notebook remains runnable when submitted offline on Kaggle.
'''
runtime = '''from pathlib import Path
import json

INPUT_ROOT = Path('/kaggle/input')
OUTPUT_PATH = Path('/kaggle/working/submission.json')

def is_task(x):
    return isinstance(x, dict) and isinstance(x.get('train'), list) and isinstance(x.get('test'), list)

def discover_tasks(root):
    paths = [p for p in root.rglob('*.json')
             if 'sample_submission' not in p.name.lower()
             and 'solution' not in p.name.lower()]
    explicit_test = [p for p in paths
                     if 'test' in p.name.lower() and 'challenge' in p.name.lower()]
    candidates = explicit_test or [p for p in paths
                                   if 'training' not in str(p).lower()
                                   and 'train_' not in p.name.lower()]
    found = {}
    for path in candidates:
        try:
            obj = json.loads(path.read_text())
        except Exception:
            continue
        if is_task(obj):
            found[path.stem] = obj
        elif isinstance(obj, dict):
            for task_id, task in obj.items():
                if is_task(task):
                    found[str(task_id)] = task
    return found

tasks = discover_tasks(INPUT_ROOT)
if not tasks:
    raise FileNotFoundError(f'No ARC test challenge JSON found under {INPUT_ROOT}. Attach the ARC-AGI-2 competition dataset to this notebook.')
submission = kaggle_payload(tasks)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(json.dumps(submission, separators=(',', ':')))
print(f'Tasks: {len(submission)} | test outputs: {sum(len(v) for v in submission.values())}')
print(f'Saved: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)')
assert all(len(items) == len(tasks[task_id]['test']) for task_id, items in submission.items())
assert all(set(item) == {'attempt_1', 'attempt_2'} for items in submission.values() for item in items)
'''
cells = [
    {"cell_type": "markdown", "metadata": {}, "source": markdown.splitlines(True)},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": solver.splitlines(True)},
    {"cell_type": "markdown", "metadata": {}, "source": [
        "## 2. Discover attached test challenges and create the file\n",
        "This cell prefers competition files explicitly named as test challenges, excludes training/solution files, and writes the two-attempt prediction object. It makes no network calls.\n",
    ]},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": runtime.splitlines(True)},
]
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10+"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
out = ROOT / "notebooks" / "arc_prize_2026_rulelab.ipynb"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(notebook, indent=1) + "\n")
print(f"Wrote {out}")
