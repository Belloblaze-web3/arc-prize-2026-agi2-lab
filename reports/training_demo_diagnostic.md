# RuleLab training-demonstration diagnostic

> **Not competition accuracy.** This leave-one-demonstration-out diagnostic uses only ARC training tasks. It does not evaluate Kaggle test/evaluation tasks or estimate a leaderboard score.

- Training tasks: 1000
- Held-out demonstrations: 3232
- Top-1 exact match: 0.019183
- Top-2 exact match: 0.019802
- Exact-fit coverage on remaining demonstrations: 0.018564

## By number of remaining demonstrations

| Remaining demonstrations | Held-out examples | Top-1 exact match | Top-2 exact match | Exact-fit coverage |
|---:|---:|---:|---:|---:|
| 1 | 316 | 0.018987 | 0.018987 | 0.025316 |
| 2 | 1725 | 0.02029 | 0.021449 | 0.02087 |
| 3 | 756 | 0.019841 | 0.019841 | 0.021164 |
| 4 | 245 | 0.008163 | 0.008163 | 0.0 |
| 5 | 108 | 0.0 | 0.0 | 0.0 |
| 6 | 56 | 0.035714 | 0.035714 | 0.0 |
| 7 | 16 | 0.125 | 0.125 | 0.0 |
| 9 | 10 | 0.0 | 0.0 | 0.0 |

## By held-out output shape

| Output shape relation | Held-out examples | Top-1 exact match | Top-2 exact match | Exact-fit coverage |
|---|---:|---:|---:|---:|
| larger_output | 289 | 0.024221 | 0.024221 | 0.024221 |
| same_shape | 2114 | 0.020341 | 0.021287 | 0.018448 |
| smaller_output | 829 | 0.014475 | 0.014475 | 0.016888 |

Rates are descriptive only. The held-out examples remain part of the official training split; this protocol is not a substitute for task-disjoint validation.
