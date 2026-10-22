# Training-split profile

This profile was computed from the official ARC-AGI-2 `data/training` directory only. The script never reads `data/evaluation`; its pair loop processes demonstrations only. The data source documents 1,000 public training tasks. [1]

The run found 1,000 task files and summarized 6,464 demonstration grids (input and output grids across the training demonstrations). The median number of demonstrations per task was 3. Demonstration inputs and outputs differ in height or width in 320 tasks. These are dataset-shape observations, not solver performance metrics.

Files:

- `task_summary.csv` — one row per task.
- `grid_summary.csv` — one row per demonstration input/output grid.
- `training_grid_shapes.png` — most frequent demonstration shapes.

Reproduce from a local clone of the official benchmark repository:

```bash
python scripts/profile_training.py /path/to/ARC-AGI-2/data/training --out reports/training_profile
```

No evaluation tasks were inspected for this profile. Because the files summarize the training data, they should not be confused with private competition results or public-evaluation performance.

[1]: https://github.com/arcprize/ARC-AGI-2 "ARC-AGI-2 Official Dataset Repository"
