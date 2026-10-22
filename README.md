# ARC-AGI-2 RuleLab

**An interpretable, task-adaptive program-synthesis baseline for ARC Prize 2026.**

RuleLab tries to infer one compact transformation from a task's demonstrations, then reuses that transformation on each unseen test grid. It searches a deliberately bounded hypothesis class: the eight dihedral grid symmetries, optional cropping around a chosen background colour, optional uniform integer cell scaling inferred from demonstration dimensions, and one globally consistent bijective colour remapping. The inferred program is checked against every demonstration before it can be used. If none fits, the solver returns deterministic geometric fallbacks. It emits exactly two candidate grids for every test input, as required by ARC-AGI-2.

This repository is a research prototype, not a leaderboard claim. No Kaggle score, Kaggle submission ID, private-set access, or paper-track entry is claimed. The accompanying Kaggle notebook is prepared for the user to attach to the 2026 ARC-AGI-2 competition and execute after joining it.

## Repository map

- `solver.py` — standalone inference and submission-payload implementation.
- `notebooks/arc_prize_2026_rulelab.ipynb` — self-contained Kaggle notebook with the solver inlined, data discovery, inference, and `submission.json` export.
- `tests/test_solver.py` — deterministic unit tests for transformations and exact output formatting.
- `scripts/profile_training.py` and `reports/training_profile/` — reproducible training-only data profile with CSVs, observations, and a grid-shape chart. It does not read evaluation tasks.
- `scripts/evaluate_demonstrations.py` — leave-one-demonstration-out diagnostics over an explicitly training-named path, with top-1/top-2 exact match and fit-coverage breakdowns. These are not competition scores.
- `reports/training_demo_diagnostic_before_scale.*` and `reports/training_demo_diagnostic.*` — preserved pre/post scale-extension reports from the official training split.
- `scripts/kaggle_pipeline.py` — guarded Kaggle package generation, JSON validation, public kernel upload, and file-submission commands.
- `scripts/build_notebook.py` — rebuilds the self-contained notebook from `solver.py`.
- `writeup/arc_prize_2026_paper_track.md` — draft Kaggle paper-track write-up (under the 1,500-word limit; competition results are intentionally left unclaimed).
- `docs/research_notes.md` — sources and verified competition constraints.
- `assets/cover.png` — write-up cover visual.

## Run locally

Python 3.10+ is recommended. The solver itself uses only the Python standard library.

```bash
python -m unittest discover -s tests -v
python scripts/make_submission.py /path/to/task_json_directory submission.json
python scripts/evaluate_demonstrations.py /path/to/arc-agi_training_challenges.json
```

The submission script accepts individual task JSON files or a single JSON mapping task IDs to task objects. It ignores files that are not ARC tasks.

The diagnostic accepts only an input path containing `train` in its name or a parent directory. It excludes known evaluation, test, solution, and sample-submission paths. Its leave-one-demonstration-out score asks whether a rule inferred from a task's other training examples predicts the held-out demonstration; it is neither task-disjoint validation nor Kaggle test accuracy. Do not use Kaggle evaluation files as input.

## Kaggle use

1. Join the ARC Prize 2026 ARC-AGI-2 competition on Kaggle and create a notebook attached to that competition.
2. Import or copy `notebooks/arc_prize_2026_rulelab.ipynb` as a **public** notebook and enable the competition data input.
3. Run the notebook offline. It locates task JSONs attached under `/kaggle/input`, runs inference, and writes `/kaggle/working/submission.json`.
4. Commit the notebook and use Kaggle's competition submission controls. Record the resulting submission ID and leaderboard score in the write-up only after Kaggle reports them.
5. Create and submit the separate ARC Prize 2026 Paper Track write-up with the public notebook link and cover image before the official deadline.

Kaggle's private evaluation score cannot be reproduced locally. Do not use the public evaluation tasks for iterative tuning. The project has not been run or submitted on Kaggle from this environment because no Kaggle account credentials or logged-in Kaggle session were available.

### Automated Kaggle package and guarded actions

Install and authenticate the official Kaggle CLI on the machine used for publishing (`pip install kaggle`, then `kaggle auth login`). Do not place tokens in this repository. Build the account-specific bundle with `python scripts/kaggle_pipeline.py prepare --username <your-kaggle-username>`. The bundle includes a notebook configured for public visibility, the ARC-AGI-2 competition source, internet disabled, plus the paper-track draft and cover image. Review it before using `python scripts/kaggle_pipeline.py publish --confirm-publication`; this saves a public notebook version without running it. The confirmation flag prevents accidental public uploads.

After joining the competition, review and execute the notebook in Kaggle. Check its `submission.json` with `python scripts/kaggle_pipeline.py validate-submission /path/to/submission.json`. The pipeline exposes a file-based `submit` command only behind `--confirm-submission`; confirm the current competition's accepted route in Kaggle first. Kaggle's paper-track write-up must still be posted through its competition interface, with the public notebook URL and cover image. The package's `PUBLICATION_CHECKLIST.md` contains the steps and exact commands.

## Method and limitations

The hypothesis class is intentionally interpretable and small. It can solve tasks expressible by one shared global transform, including uniform integer scaling, but does not handle object-level reasoning, rule composition, conditional rules, counting, recoloring that is not a one-to-one global map, or generated patterns. The fallback guesses are legal-format outputs, not evidence of reasoning. A high ARC score should not be expected from this baseline without substantially richer program synthesis and carefully controlled validation.

## License

MIT. The ARC-AGI-2 benchmark data remains subject to its upstream terms; it is not redistributed in this repository.
