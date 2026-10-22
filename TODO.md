# Project TODO

## Complete — reproducible ARC-AGI-2 baseline and compliant artifacts

- [x] Provide an interpretable, deterministic solver that learns from each task's demonstrations, validates a candidate against every demonstration, and emits exactly two candidate grids per test input in the competition payload format.
- [x] Include a self-contained Kaggle notebook, local submission builder, training-only data profile, solver tests, research notes, MIT-licensed source, and a paper-track draft under the word limit.
- [x] Keep performance claims honest: no Kaggle submission ID, competition score, private-evaluation result, or paper-track entry is claimed.
- [x] Run the leave-one-demonstration-out evaluator against the official ARC-AGI-2 training directory only; save complete JSON and Markdown results, including support-count and output-shape breakdowns, and preserve the pre-extension report.
- [x] Inspect training-only errors, find that the prior solver matched 0 of 289 held-out cases with larger-area outputs, and confirm a uniform integer cell-scale rule on seven demonstrations using only their remaining examples.
- [x] Add demonstration-derived uniform integer cell scaling, require exact consistency with every available demonstration, rebuild the self-contained Kaggle notebook, and rerun the local suite.
- [x] Add a Kaggle pipeline utility that prepares kernel metadata and the paper-track/cover package, validates the exact two-attempt JSON structure, and requires explicit flags before a public upload or competition file submission.

## Pending account-owner actions — Kaggle access and publication

- [ ] Install/authenticate the official Kaggle CLI or connect an authenticated Kaggle account, then prepare the account-specific package with the Kaggle username.
- [ ] Review the public notebook, join and accept the ARC-AGI-2 competition rules, and publish the notebook using the gated pipeline command; execute it on Kaggle with competition data attached and internet disabled.
- [ ] Validate the Kaggle-produced `submission.json` and submit using the current competition-approved route. Record the actual submission ID, score, runtime, and hardware only after Kaggle reports them; do not tune iteratively against evaluation data.
- [ ] Add the public notebook URL to the paper-track write-up and submit the write-up and cover through Kaggle's competition interface before the official deadline.
