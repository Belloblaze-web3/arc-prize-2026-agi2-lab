#!/usr/bin/env python3
"""Descriptive ARC task profile. Reads only an explicitly supplied training folder."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def profile(root: Path):
    files = sorted(root.glob('*.json'))
    if not files:
        raise SystemExit(f'No task JSON files in {root}')
    task_rows = []
    pair_rows = []
    for path in files:
        task = json.loads(path.read_text())
        if not isinstance(task, dict) or not isinstance(task.get('train'), list):
            continue
        pair_dimensions = []
        colors = set()
        for split in ('train',):  # Strictly demonstrations only; never inspect evaluation.
            for pair in task.get(split, []):
                for side in ('input', 'output'):
                    grid = pair.get(side)
                    if not grid:
                        continue
                    h, w = len(grid), len(grid[0])
                    colors.update(x for row in grid for x in row)
                    pair_dimensions.append((h, w))
                    pair_rows.append({
                        'task_id': path.stem,
                        'side': side,
                        'height': h,
                        'width': w,
                        'area': h * w,
                        'n_colors': len({x for row in grid for x in row}),
                    })
        task_rows.append({
            'task_id': path.stem,
            'n_demonstrations': len(task['train']),
            'n_test_inputs': len(task.get('test', [])),
            'n_colors_in_demonstrations': len(colors),
            'n_distinct_demonstration_shapes': len(set(pair_dimensions)),
            'any_size_change_in_demonstrations': any(
                len(p['input']) != len(p['output']) or len(p['input'][0]) != len(p['output'][0])
                for p in task['train']
            ),
        })
    return task_rows, pair_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('training_dir', type=Path, help='Path to official data/training only')
    ap.add_argument('--out', type=Path, default=Path('reports/training_profile'))
    args = ap.parse_args()
    tasks, pairs = profile(args.training_dir)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, rows in [('task_summary.csv', tasks), ('grid_summary.csv', pairs)]:
        with (args.out / name).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(f'Tasks profiled: {len(tasks)} (training demonstrations only)')
    print(f'Demonstration grids profiled: {len(pairs)}')
    print(f'Tasks with size changes in demonstrations: {sum(t["any_size_change_in_demonstrations"] for t in tasks)}')
    print(f'Median demonstrations/task: {sorted(t["n_demonstrations"] for t in tasks)[len(tasks)//2]}')
    try:
        import matplotlib.pyplot as plt
        counts = Counter((r['height'], r['width']) for r in pairs)
        top = counts.most_common(15)
        labels = [f'{h}×{w}' for (h, w), _ in top]
        values = [v for _, v in top]
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.barh(labels[::-1], values[::-1], color='#22b8a7')
        ax.set_xlabel('Count of demonstration grids')
        ax.set_title('ARC-AGI-2 training: most frequent demonstration grid shapes')
        ax.spines[['top', 'right']].set_visible(False)
        fig.tight_layout()
        fig.savefig(args.out / 'training_grid_shapes.png', dpi=180, bbox_inches='tight')
        plt.close(fig)
        print(f'Chart: {args.out / "training_grid_shapes.png"}')
    except ImportError:
        print('matplotlib unavailable; CSV summaries still written')


if __name__ == '__main__':
    main()
