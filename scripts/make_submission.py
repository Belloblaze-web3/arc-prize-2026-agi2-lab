#!/usr/bin/env python3
"""Build an ARC two-attempt JSON submission from task JSON files."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from solver import kaggle_payload  # noqa: E402


def load_tasks(source: Path) -> dict:
    tasks = {}
    files = [source] if source.is_file() else sorted(source.rglob("*.json"))
    for path in files:
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and "train" in data and "test" in data:
            tasks[path.stem] = data
        elif isinstance(data, dict):
            for task_id, task in data.items():
                if isinstance(task, dict) and "train" in task and "test" in task:
                    tasks[str(task_id)] = task
    if not tasks:
        raise SystemExit(f"No ARC task JSON objects found under {source}")
    return tasks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="ARC task JSON file or directory")
    parser.add_argument("output", type=Path, help="submission JSON destination")
    args = parser.parse_args()
    payload = kaggle_payload(load_tasks(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Wrote {len(payload)} task predictions to {args.output}")


if __name__ == "__main__":
    main()
