# Project TODO

## Complete — reproducible ARC-AGI-2 baseline and compliant submission artifact

- [x] Provide an interpretable, deterministic solver that learns only from each task's demonstrations, validates a candidate against all demonstrations, and emits exactly two candidate grids per test input in the competition payload format.
- [x] Include a self-contained Kaggle notebook, local submission builder, training-only data profile, solver unit tests, research notes, MIT-licensed source, and a paper-track draft under the word limit.
- [x] Keep all performance claims honest: no Kaggle submission ID, competition score, private-evaluation result, or paper-track entry is claimed.

## In progress — quantify within-task generalization without evaluation-set leakage

- [ ] Run `scripts/evaluate_demonstrations.py` on the official training task files only; preserve top-1/top-2 exact-match rates, fit coverage, and support-count breakdowns as an explicitly non-leaderboard diagnostic.
- [ ] Review the resulting error cases and identify a small, interpretable solver extension only when supported by the training-only analysis.
- [ ] After any solver change, rebuild the self-contained Kaggle notebook and rerun all local tests.

## Pending account-owner actions — Kaggle publication and submission

- [ ] In Kaggle, attach the public notebook to the ARC-AGI-2 competition and execute the offline notebook after joining the competition.
- [ ] Submit through Kaggle and record the actual submission ID, score, runtime, and hardware only after Kaggle reports them; do not tune iteratively against the public evaluation data.
- [ ] Publish the notebook publicly and submit the paper-track write-up with its public notebook link and cover image before the official deadline.
