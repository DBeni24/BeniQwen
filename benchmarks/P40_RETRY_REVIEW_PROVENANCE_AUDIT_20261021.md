# P40 retry-review provenance audit — 2026-10-21

## Scope and verification

This audit covers the separate latest-retry qualitative review, not the fixed-protocol Full470 score. It contains 58 case IDs and 116 Base/LoRA output rows. The case set is disjoint from the 76 primary reviewed pairs, for 134 distinct reviewed case IDs. Fifteen retry-review cases are holdouts and remain evaluation-only.

A read-only reconciliation against the saved result files confirmed:

- 116/116 raw status values match.
- 116/116 output-token counts match.
- 114/114 ordinary final-answer SHA-256 values match after applying the existing ten-row source correction for five pairs.
- The remaining two rows are the PERS-027 32K pair. Their old fields named `output_sha256` were the SHA-256 values of the whole `results.jsonl` files. The whole-file hashes were retained as `result_file_sha256`, and the exact `final_answer` hashes are separately recorded in `P40_RETRY_REVIEW_PERS027_CONTEXT32_HASH_CLARIFICATION_20261021.json`.

No result file, completion, raw status, token count, or manual verdict was modified. All 116 answer hashes reconcile after applying the two provenance addenda.

## Qualitative verdict counts

| Cohort | Base | P40-LoRA |
|---|---:|---:|
| FAIL | 53 | 13 |
| PASS | 0 | 9 |
| PASS_WITH_LIMITATION | 2 | 25 |
| PASS_WITH_MINOR_GRAMMAR_ISSUE | 0 | 2 |
| PASS_WITH_MINOR_ISSUES | 3 | 8 |
| PASS_WITH_MINOR_USEFULNESS_LIMITATION | 0 | 1 |
| **Total** | **58** | **58** |

These are qualitative labels from one AI reviewer. There was no independent second reviewer and no frozen numeric pass threshold, so they are not a calibrated percentage improvement. Raw automatic statuses remain `REVIEW_REQUIRED`; the retry cohort must not be merged into the primary score.

## Limitations and current resource state

P40's training lineage was informed by aggregate HU-060 holdout results through P31 data selection. Full470 and this retry review are therefore exploratory, not an independent unbiased final estimate. Holdouts were used only for evaluation and not for training.

The shared AI-Server GPU/RAM gate is paused (`allow_gpu_ram=false`). Read-only inspection found the RTX 3090 at 0% utilization with 95 MiB VRAM allocated and `ollama ps` empty. No inference, benchmark, training, or model-load job was started.

## Evidence files

- `P40_LATEST_RETRY_MANUAL_REVIEW_20261021.md` and `.json`
- `P40_RETRY_REVIEW_PROVENANCE_CORRECTION_20261021.json` — source/hash correction for five paired cases
- `P40_RETRY_REVIEW_PERS027_CONTEXT32_HASH_CLARIFICATION_20261021.json` — separates result-file and final-answer hashes
- `P40_FULL470_AUDIT_REPORT_20261021.md`
