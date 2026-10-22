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

## Training-demonstration diagnostic

`scripts/evaluate_demonstrations.py` provides a leave-one-demonstration-out diagnostic. It was run on the official `data/training` directory at upstream revision `f3283f7`, covering 1,000 tasks and 3,232 held-out demonstrations. Before adding uniform integer scaling, the solver matched 52/3,232 held-out outputs as top-1 (1.61%) and 54/3,232 as top-2 (1.67%). A shape-stratified probe found zero matches among 289 larger-area outputs. A separate train-only rule probe found seven held-out examples where the remaining demonstrations imply a uniform integer scale; all seven reproduced exactly.

The solver now searches that scale operation only when dimensions of transformed demonstrations imply a shared integer factor. In the repeated full-training diagnostic, top-1 was 62/3,232 (1.92%), top-2 was 64/3,232 (1.98%), and exact-fit coverage was 60/3,232 (1.86%). It matched 7/289 larger-area examples (2.42%). Both files are saved under `reports/training_demo_diagnostic*`. These within-task training diagnostics are not task-disjoint validation, competition accuracy, or a Kaggle score. The loader requires `train` in the input path and excludes known evaluation, test, solution, and sample-submission paths. The official repository explicitly says not to iteratively tune on its public evaluation split. [3]

`scripts/kaggle_pipeline.py` prepares a public, offline notebook package and the paper-track draft/cover package. It validates the two-attempt JSON shape and gates public notebook upload and file submission behind explicit command-line flags. The current sandbox has no Kaggle CLI executable or authenticated Kaggle session, so nothing has been published or submitted. Kaggle's CLI documents public notebook metadata, notebook push behavior, and file-based competition submission commands; its official command reference does not provide a paper-track write-up publishing command. Final write-up publication remains an account-owner action in Kaggle. [6] [7] [8]

## References

[1]: https://arcprize.org/competitions/2026/arc-agi-2 "ARC Prize 2026 ARC-AGI-2 Competition"
[2]: https://www.kaggle.com/competitions/arc-prize-2026-paper-track "ARC Prize 2026 Paper Track"
[3]: https://github.com/arcprize/ARC-AGI-2 "ARC-AGI-2 Official Dataset Repository"
[4]: https://arcprize.org/blog/arc-agi-2-technical-report "ARC-AGI-2 Technical Report"
[5]: https://arcprize.org/blog/arc-prize-2025-results-analysis "ARC Prize 2025 Results and Analysis"
[6]: https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels_metadata.md "Kaggle CLI kernel metadata"
[7]: https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md "Kaggle CLI kernel commands"
[8]: https://github.com/Kaggle/kaggle-cli/blob/main/docs/competitions.md "Kaggle CLI competition commands"
