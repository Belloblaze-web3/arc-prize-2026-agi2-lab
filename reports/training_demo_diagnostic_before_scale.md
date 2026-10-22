# RuleLab training-demonstration diagnostic

> **Not competition accuracy.** This leave-one-demonstration-out diagnostic uses only ARC training tasks. It does not evaluate Kaggle test/evaluation tasks or estimate a leaderboard score.

- Training tasks: 1000
- Held-out demonstrations: 3232
- Top-1 exact match: 0.016089
- Top-2 exact match: 0.016708
- Exact-fit coverage on remaining demonstrations: 0.01547

## By number of remaining demonstrations

| Remaining demonstrations | Held-out examples | Top-1 exact match | Top-2 exact match | Exact-fit coverage |
|---:|---:|---:|---:|---:|
| 1 | 316 | 0.006329 | 0.006329 | 0.012658 |
| 2 | 1725 | 0.016812 | 0.017971 | 0.017391 |
| 3 | 756 | 0.019841 | 0.019841 | 0.021164 |
| 4 | 245 | 0.008163 | 0.008163 | 0.0 |
| 5 | 108 | 0.0 | 0.0 | 0.0 |
| 6 | 56 | 0.035714 | 0.035714 | 0.0 |
| 7 | 16 | 0.125 | 0.125 | 0.0 |
| 9 | 10 | 0.0 | 0.0 | 0.0 |

Rates are descriptive only. The held-out examples remain part of the official training split; this protocol is not a substitute for task-disjoint validation.
