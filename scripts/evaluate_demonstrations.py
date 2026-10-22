#!/usr/bin/env python3
"""Evaluate ARC RuleLab by holding out demonstrations within training tasks.

This is a diagnostic of within-task demonstration generalization. It is not
competition test accuracy and must never be run on evaluation/test task files.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from solver import predict_task  # noqa: E402


def _is_task(value: Any) -> bool:
    return (isinstance(value, dict)
            and isinstance(value.get("train"), list)
            and isinstance(value.get("test"), list))


def load_training_tasks(source: Path) -> dict[str, dict]:
    """Load ARC task objects only from a path explicitly identified as training.

    The path itself or one of its parent directories must include 'train'.
    Directories are recursively filtered to training-named paths, and known
    evaluation/test/solution paths are excluded even if nested below them.
    """
    if "train" not in str(source).lower():
        raise ValueError("Input path must explicitly identify training data (include 'train' in its path).")
    if not source.exists():
        raise FileNotFoundError(source)

    if source.is_file():
        paths = [source]
    else:
        paths = [p for p in sorted(source.rglob("*.json"))
                 if "train" in str(p).lower()
                 and not any(word in str(p).lower()
                             for word in ("evaluation", "test", "solution", "sample_submission"))]

    tasks: dict[str, dict] = {}
    for path in paths:
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if _is_task(obj):
            tasks[path.stem] = obj
        elif isinstance(obj, dict):
            for task_id, task in obj.items():
                if _is_task(task):
                    tasks[str(task_id)] = task
    if not tasks:
        raise ValueError(f"No ARC training tasks found under {source}")
    return tasks


def evaluate(tasks: dict[str, dict]) -> dict[str, Any]:
    """Hold out each training demonstration in turn and collect exact-match metrics."""
    total = top1 = top2 = fit_coverage = 0
    by_support: dict[int, dict[str, int]] = defaultdict(
        lambda: {"examples": 0, "top1_correct": 0, "top2_correct": 0, "fit_coverage": 0}
    )
    by_task: dict[str, dict[str, int]] = {}

    for task_id, task in sorted(tasks.items()):
        demos = task.get("train", [])
        task_counts = {"examples": 0, "top1_correct": 0, "top2_correct": 0, "fit_coverage": 0}
        for held_index, held in enumerate(demos):
            remaining = [demo for index, demo in enumerate(demos) if index != held_index]
            probe = {"train": remaining, "test": [{"input": held["input"]}]}
            guesses = predict_task(probe, n_attempts=2)[0]
            truth = held["output"]
            correct1 = int(guesses[0] == truth)
            correct2 = int(any(guess == truth for guess in guesses))
            # Coverage means a candidate program exactly fits the remaining
            # demonstrations; it is separate from prediction correctness.
            has_fit = int(bool(remaining) and _has_exact_fit(probe))
            total += 1
            top1 += correct1
            top2 += correct2
            fit_coverage += has_fit
            bucket = by_support[len(remaining)]
            for counts in (bucket, task_counts):
                counts["examples"] += 1
                counts["top1_correct"] += correct1
                counts["top2_correct"] += correct2
                counts["fit_coverage"] += has_fit
        by_task[task_id] = task_counts

    def rate(numerator: int, denominator: int) -> float | None:
        return round(numerator / denominator, 6) if denominator else None

    def summarize(counts: dict[str, int]) -> dict[str, Any]:
        n = counts["examples"]
        return {
            **counts,
            "top1_exact_match_rate": rate(counts["top1_correct"], n),
            "top2_exact_match_rate": rate(counts["top2_correct"], n),
            "remaining_demo_fit_coverage": rate(counts["fit_coverage"], n),
        }

    return {
        "evaluation_protocol": "leave-one-demonstration-out within official training tasks",
        "metric_warning": "Diagnostic only; not competition test or leaderboard accuracy.",
        "tasks": len(tasks),
        "examples": total,
        "overall": summarize({"examples": total, "top1_correct": top1,
                              "top2_correct": top2, "fit_coverage": fit_coverage}),
        "by_remaining_demonstrations": {
            str(k): summarize(v) for k, v in sorted(by_support.items())
        },
        "by_task": {task_id: summarize(counts) for task_id, counts in by_task.items()},
    }


def _has_exact_fit(task: dict) -> bool:
    # Local import keeps the public evaluator surface small and tests isolated.
    from solver import _programs_for_task
    return bool(_programs_for_task(task))


def render_markdown(result: dict[str, Any]) -> str:
    overall = result["overall"]
    lines = [
        "# RuleLab training-demonstration diagnostic",
        "",
        "> **Not competition accuracy.** This leave-one-demonstration-out diagnostic uses only ARC training tasks. It does not evaluate Kaggle test/evaluation tasks or estimate a leaderboard score.",
        "",
        f"- Training tasks: {result['tasks']}",
        f"- Held-out demonstrations: {result['examples']}",
        f"- Top-1 exact match: {overall['top1_exact_match_rate']}",
        f"- Top-2 exact match: {overall['top2_exact_match_rate']}",
        f"- Exact-fit coverage on remaining demonstrations: {overall['remaining_demo_fit_coverage']}",
        "",
        "## By number of remaining demonstrations",
        "",
        "| Remaining demonstrations | Held-out examples | Top-1 exact match | Top-2 exact match | Exact-fit coverage |",
        "|---:|---:|---:|---:|---:|",
    ]
    for support, counts in result["by_remaining_demonstrations"].items():
        lines.append(
            f"| {support} | {counts['examples']} | {counts['top1_exact_match_rate']} "
            f"| {counts['top2_exact_match_rate']} | {counts['remaining_demo_fit_coverage']} |"
        )
    lines.extend(["", "Rates are descriptive only. The held-out examples remain part of the official training split; this protocol is not a substitute for task-disjoint validation.", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("training_input", type=Path,
                        help="Training-named JSON file or directory; test/evaluation paths are excluded")
    parser.add_argument("--json", type=Path, default=Path("reports/training_demo_diagnostic.json"),
                        help="JSON report destination (default: reports/training_demo_diagnostic.json)")
    parser.add_argument("--markdown", type=Path, default=Path("reports/training_demo_diagnostic.md"),
                        help="Markdown report destination (default: reports/training_demo_diagnostic.md)")
    args = parser.parse_args()
    result = evaluate(load_training_tasks(args.training_input))
    for path, content in ((args.json, json.dumps(result, indent=2) + "\n"),
                          (args.markdown, render_markdown(result))):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"Training-only demonstration diagnostic: {result['examples']} held-out examples")
    print(f"Top-1={result['overall']['top1_exact_match_rate']} | Top-2={result['overall']['top2_exact_match_rate']}")
    print(f"Not competition accuracy. Reports: {args.json}, {args.markdown}")


if __name__ == "__main__":
    main()
