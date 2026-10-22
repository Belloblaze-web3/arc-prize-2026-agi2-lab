# RuleLab: Compact Program Synthesis for ARC-AGI-2

**A transparent, task-adaptive baseline that tests whether a small transformation language can explain ARC demonstrations and transfer to unseen grids.**

## Abstract

ARC-AGI-2 asks a solver to infer a rule from a few input/output examples and apply it to new grids. RuleLab treats each task as a small program-synthesis problem. It searches a bounded language of eight grid symmetries, optional background-colour cropping, and a one-to-one global colour remapping. A candidate is accepted only if it reproduces every demonstration exactly. At inference time the program is applied to each test input and two distinct candidates are emitted. This is a transparent baseline, not a claim of competitive accuracy. No Kaggle leaderboard score or submission ID is available yet.

## Motivation and related work

ARC-AGI-2 is designed to measure generalization from a small number of demonstrations, with tasks intended to be easy for people but difficult for pattern-matching systems. The official report identifies symbolic interpretation, compositional reasoning, and context-sensitive rule use as recurring challenges. RuleLab begins with a narrower question: how often can an exact, simple global transform explain all examples, and how should a system behave when it cannot find one? [1]

Prior ARC solvers include hand-coded transformation systems, program search, neural models, and iterative refinement with language models. RuleLab is closest to symbolic program synthesis: it searches a human-readable hypothesis class rather than fitting a large model. Its differentiating emphasis is intentionally modest: exact demonstration consistency, interpretable hypotheses, deterministic execution, and a clean Kaggle submission path. This is a baseline contribution, not a claim that the component operations are individually novel.

## Method

For each task, the synthesizer enumerates eight dihedral transformations: identity, three rotations, horizontal and vertical reflection, transpose, and anti-transpose. It optionally crops the transformed grid to the bounding box of cells not equal to a candidate background colour. The candidate colour set is derived from the demonstration inputs. For every geometry/crop combination, the solver infers a global colour mapping from aligned demonstration cells. Mapping conflicts, non-bijective mappings, and shape mismatches reject the candidate.

Every surviving program must reproduce all training outputs exactly. Programs are ordered by a fixed simplicity preference, then applied to each test grid. The first two distinct outputs become the attempts. If fewer than two learned outputs exist, deterministic symmetry-based fallbacks fill the remaining slot. This keeps the output schema valid but does not make unsupported predictions meaningful. No internet, hosted model, or external API is used at inference time.

The hypothesis class captures transformations that are global and uniform. It does not model connected-object selection, counting, conditional rules, multi-stage compositions beyond geometry/crop/recolour, or creation of new structure. Failure on such tasks is expected and informs future extensions.

## Evaluation and reproducibility

The repository includes source, unit tests, and a self-contained Kaggle notebook. The notebook discovers the attached task JSON files, writes one pair of guesses per test input, and saves `submission.json`. Kaggle's official ARC-AGI-2 scoring grants a test output a point if either of two exact grids matches. The 2026 competition requires notebook submissions and offline evaluation. [2]

As a data-quality check, a separate profiling script examined only the 1,000 official training task files and their demonstrations. It summarized 6,464 input/output grids; the median task had three demonstrations, and 320 tasks showed a height or width change within their demonstrations. These descriptive training-set statistics are not model accuracy. The script and chart are included so the analysis can be reproduced. [3]

**Competition results: not yet available.** This project has no Kaggle submission ID, public leaderboard result, or private-evaluation score. No number is reported as accuracy. The Kaggle public evaluation set is not used for iterative development. After the owner runs and submits the notebook, this section should be updated with the actual submission ID, displayed score, runtime, and hardware, with the exact evaluation split identified. The public ARC-AGI-2 repository contains 1,000 training tasks and 120 public evaluation tasks, and explicitly cautions against tuning on that evaluation split. [3]

## Why it may help, and where it falls short

A useful property of exact synthesis is that one compact rule must explain every example, reducing the chance that a weak local resemblance is accepted as the task rule. The two-attempt output also permits the solver to preserve a small number of competing exact-fit hypotheses when demonstrations underdetermine the transformation. These are design motivations, not measured gains. The restricted language can still overfit a tiny set of examples, and two distinct fitting programs can make different predictions on the test input. The simple complexity ordering is a prior, not a learned estimate of correctness.

The most useful next research step is to grow the language carefully: add object extraction and matching, color/shape invariants, compositional operations, and a validation protocol based on task-disjoint training splits. Each extension should be tested by ablation and accompanied by candidate coverage, exact-match accuracy, runtime, and failure-category analysis. Public evaluation should be reserved for a final, non-iterative check under the dataset's guidance.

## Conclusion

RuleLab is a reproducible, interpretable starting point for task-level ARC program induction. It makes no leaderboard claim; its present value is a clear baseline and an auditable path from demonstrations to legal two-attempt predictions.

## References

[1]: https://arcprize.org/blog/arc-agi-2-technical-report "ARC-AGI-2 Technical Report"
[2]: https://arcprize.org/competitions/2026/arc-agi-2 "ARC Prize 2026 ARC-AGI-2 Competition"
[3]: https://github.com/arcprize/ARC-AGI-2 "ARC-AGI-2 Official Dataset Repository"
