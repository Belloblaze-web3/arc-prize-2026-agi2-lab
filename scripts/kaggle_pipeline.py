#!/usr/bin/env python3
"""Prepare and safely gate ARC Prize 2026 Kaggle publication/submission actions.

This tool never reads or stores Kaggle credentials. Kaggle CLI authentication is
managed by Kaggle. Public publication and competition submission require their
own explicit confirmation flags.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMPETITION = "arc-prize-2026-arc-agi-2"
DEFAULT_BUNDLE = ROOT / "kaggle" / "arc-prize-2026-rulelab"


def _read_submission(path: Path) -> dict[str, Any]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read submission JSON at {path}: {exc}") from exc
    if not isinstance(obj, dict) or not obj:
        raise ValueError("Submission must be a non-empty object keyed by task ID")
    for task_id, outputs in obj.items():
        if not isinstance(task_id, str) or not isinstance(outputs, list):
            raise ValueError(f"Invalid task entry: {task_id!r}")
        for index, item in enumerate(outputs):
            if not isinstance(item, dict) or set(item) != {"attempt_1", "attempt_2"}:
                raise ValueError(f"{task_id}[{index}] must contain exactly attempt_1 and attempt_2")
            for key, grid in item.items():
                if not isinstance(grid, list) or not grid or not all(isinstance(row, list) and row for row in grid):
                    raise ValueError(f"{task_id}[{index}].{key} must be a non-empty grid")
                width = len(grid[0])
                if any(len(row) != width for row in grid):
                    raise ValueError(f"{task_id}[{index}].{key} is not rectangular")
                if any(type(value) is not int or not 0 <= value <= 9 for row in grid for value in row):
                    raise ValueError(f"{task_id}[{index}].{key} must contain only integer colors 0..9")
    return obj


def prepare(username: str, bundle: Path) -> tuple[Path, Path]:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
        raise ValueError("Kaggle username must contain only letters, numbers, '_' or '-'")
    kernel_dir = bundle / "kernel"
    paper_dir = bundle / "paper-track"
    kernel_dir.mkdir(parents=True, exist_ok=True)
    paper_dir.mkdir(parents=True, exist_ok=True)

    notebook_source = ROOT / "notebooks" / "arc_prize_2026_rulelab.ipynb"
    notebook = json.loads(notebook_source.read_text(encoding="utf-8"))
    notebook_text = notebook_source.read_text(encoding="utf-8")
    if notebook.get("nbformat") != 4 or "def predict_task" not in notebook_text:
        raise ValueError("Notebook is not a valid self-contained RuleLab notebook")
    code_file = "arc_prize_2026_rulelab.ipynb"
    shutil.copy2(notebook_source, kernel_dir / code_file)

    kernel_id = f"{username}/arc-agi-2-rulelab"
    metadata = {
        "id": kernel_id,
        "title": "ARC-AGI-2 RuleLab",
        "code_file": code_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": "false",
        "enable_gpu": "false",
        "enable_internet": "false",
        "machine_shape": "",
        "dataset_sources": [],
        "competition_sources": [COMPETITION],
        "kernel_sources": [],
        "model_sources": [],
    }
    (kernel_dir / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    shutil.copy2(ROOT / "writeup" / "arc_prize_2026_paper_track.md", paper_dir / "paper_track_writeup.md")
    shutil.copy2(ROOT / "assets" / "cover.png", paper_dir / "cover.png")
    checklist = f"""# Kaggle ARC Prize 2026 publication package

Prepared without Kaggle credentials. The notebook kernel metadata is configured for a public notebook attached to `{COMPETITION}` with internet disabled.

## Before publishing

1. Join the competition and accept its rules using the intended Kaggle account.
2. Make the source repository and methods publicly accessible before representing the work as open-source or prize-eligible. This script does not change GitHub visibility.
3. Authenticate the official Kaggle CLI with `kaggle auth login` or Kaggle's supported API-token setup. Never commit token files.
4. Review the write-up and cover in `paper-track/`; add the public notebook URL after publishing.

## Commands

From the repository root:

```bash
python scripts/kaggle_pipeline.py prepare --username {username}
python scripts/kaggle_pipeline.py publish --confirm-publication
```

The publish command uses `kaggle kernels push --no-run`, so it saves a public notebook version but does not launch a run. Review the uploaded notebook on Kaggle, then execute it there with the competition attached. Validate the generated `submission.json` before using Kaggle's competition submission control.

For a file-based Kaggle CLI submission, after confirming that this competition/account accepts that route, use:

```bash
python scripts/kaggle_pipeline.py validate-submission /path/to/submission.json
python scripts/kaggle_pipeline.py submit /path/to/submission.json --kernel {kernel_id} --confirm-submission
```

The final paper-track write-up must be posted through Kaggle's competition write-up interface. The supported Kaggle CLI reference documents kernel publishing and competition file submissions, but not paper-track write-up publication; complete that final form in Kaggle after adding the public notebook link and cover image.
"""
    (bundle / "PUBLICATION_CHECKLIST.md").write_text(checklist, encoding="utf-8")
    return kernel_dir, paper_dir


def _kaggle_cli() -> str:
    cli = shutil.which("kaggle")
    if not cli:
        raise RuntimeError("Kaggle CLI is not installed. Install the official Kaggle CLI and authenticate through Kaggle before continuing.")
    return cli


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)

    prep = sub.add_parser("prepare", help="Build the notebook metadata and paper-track package")
    prep.add_argument("--username", required=True, help="Your Kaggle username slug")
    prep.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE)

    publish = sub.add_parser("publish", help="Publish a public notebook version without running it")
    publish.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE)
    publish.add_argument("--confirm-publication", action="store_true",
                         help="Confirm uploading this notebook with public visibility")

    validate = sub.add_parser("validate-submission", help="Check ARC two-attempt JSON structure")
    validate.add_argument("submission_json", type=Path)

    submit = sub.add_parser("submit", help="Submit an ARC JSON artifact through Kaggle CLI")
    submit.add_argument("submission_json", type=Path)
    submit.add_argument("--kernel", required=True, help="Kaggle kernel id owner/slug")
    submit.add_argument("--message", default="ARC-AGI-2 RuleLab submission")
    submit.add_argument("--confirm-submission", action="store_true",
                        help="Confirm sending this artifact to the competition evaluator")

    args = parser.parse_args()
    try:
        if args.action == "prepare":
            kernel_dir, paper_dir = prepare(args.username, args.bundle_dir)
            print(f"Prepared Kaggle kernel bundle: {kernel_dir}")
            print(f"Prepared paper-track package: {paper_dir}")
            print(f"Next: python scripts/kaggle_pipeline.py publish --bundle-dir {args.bundle_dir} --confirm-publication")
        elif args.action == "publish":
            if not args.confirm_publication:
                raise ValueError("Public upload not run. Pass --confirm-publication after reviewing the public notebook package.")
            metadata_path = args.bundle_dir / "kernel" / "kernel-metadata.json"
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata.get("is_private") != "false" or metadata.get("enable_internet") != "false":
                raise ValueError("Refusing publish: metadata must be public and internet-disabled for this competition.")
            cli = _kaggle_cli()
            subprocess.run([cli, "kernels", "push", "-p", str(metadata_path.parent), "--no-run"], check=True)
        elif args.action == "validate-submission":
            obj = _read_submission(args.submission_json)
            print(f"Valid ARC two-attempt payload: {len(obj)} tasks, {sum(len(v) for v in obj.values())} test outputs")
        elif args.action == "submit":
            if not args.confirm_submission:
                raise ValueError("Submission not sent. Pass --confirm-submission after reviewing the exact JSON file and Kaggle route.")
            _read_submission(args.submission_json)
            cli = _kaggle_cli()
            subprocess.run([cli, "competitions", "submit", COMPETITION,
                            "-f", str(args.submission_json), "-m", args.message,
                            "-k", args.kernel], check=True)
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Kaggle pipeline stopped: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
