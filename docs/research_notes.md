# ARC Prize research notes

Checked on 22 October 2026. The competition schedule or platform instructions may change, so Kaggle is the final authority immediately before submission.

## Verified constraints

- The ARC Prize 2026 ARC-AGI-2 competition describes a target of 85% on its private evaluation within Kaggle efficiency limits. Competition submissions run as Kaggle notebooks, have no internet during evaluation, and must be open sourced for prize eligibility. Each test input needs exactly two candidate grids; a task output scores correct if either candidate matches exactly. [1]
- The 2026 paper track requires a Kaggle write-up documenting a submitted ARC-AGI-2 or ARC-AGI-3 solution. Its submission requires a media-gallery cover image and a publicly accessible notebook linked in the Project Links field; write-ups are capped at 1,500 words. The evaluation criteria are accuracy, universality, progress, theory, completeness, and novelty. A paper-track draft is not a submission. [2]
- The source ARC-AGI-2 repository documents 1,000 public training tasks and 120 public evaluation tasks. Each task is a JSON object with `train` and `test` lists; grids are rectangular matrices of colors 0–9, with dimensions up to 30×30. The repository explicitly warns against using public evaluation tasks for iterative development. [3]
- The ARC-AGI-2 report emphasizes tasks designed to reduce brute-force susceptibility and probe symbolic interpretation, compositional reasoning, and context-dependent rule use. Its human tests provide benchmark context, not a performance result for this project. [4]
- ARC Prize's 2025 results post reported a leading private ARC-AGI-2 result of 24.03% in its competition and discussed higher scores from separately evaluated commercial/refinement systems. These are not directly comparable to RuleLab and are not predictions for 2026. [5]

## Project-specific status

RuleLab implements a compact, deterministic synthesis baseline over dihedral geometry, background cropping, and globally consistent colour mapping. It has not been run against the private/semi-private competition data, does not have a Kaggle score or submission ID, and is not yet a Kaggle Paper Track entry. No numeric accuracy claim is made. The included notebook is a self-contained public-notebook candidate; publication and competition submission must be completed by the account owner in Kaggle.

## References

[1]: https://arcprize.org/competitions/2026/arc-agi-2 "ARC Prize 2026 ARC-AGI-2 Competition"
[2]: https://www.kaggle.com/competitions/arc-prize-2026-paper-track "ARC Prize 2026 Paper Track"
[3]: https://github.com/arcprize/ARC-AGI-2 "ARC-AGI-2 Official Dataset Repository"
[4]: https://arcprize.org/blog/arc-agi-2-technical-report "ARC-AGI-2 Technical Report"
[5]: https://arcprize.org/blog/arc-prize-2025-results-analysis "ARC Prize 2025 Results and Analysis"
