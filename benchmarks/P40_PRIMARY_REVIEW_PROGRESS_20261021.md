# P40 Full470 primary review progress — 2026-10-21

## Scope and result

This note records a supplemental qualitative review of twenty-four paired cases whose Base and P40-LoRA primary outputs were both marked REVIEW_REQUIRED. The full primary run contains 470 aligned Base/LoRA case IDs; 76 pairs are jointly REVIEW_REQUIRED. Twenty-four of those pairs have now been manually reviewed, leaving 52 in that group.

| Case | Visibility | Base manual verdict | P40-LoRA manual verdict |
|---|---|---|---|
| HU-001 | diagnostic | PASS_WITH_MINOR_ISSUES | PASS_WITH_MINOR_ISSUES |
| HU-003 | diagnostic | PASS_WITH_MINOR_ISSUES | PASS_WITH_LIMITATION |
| HU-005 | holdout, evaluation-only | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-006 | diagnostic | FAIL | FAIL |
| HU-008 | diagnostic | PASS_WITH_MINOR_ISSUES | PASS |
| HU-011 | diagnostic | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-014 | diagnostic | PASS_WITH_LIMITATION | PASS |
| HU-018 | diagnostic | PASS_WITH_LIMITATION | FAIL |
| HU-028 | diagnostic | FAIL | FAIL |
| HU-033 | diagnostic | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-036 | diagnostic | FAIL | FAIL |
| HU-037 | diagnostic | FAIL | PASS_WITH_LIMITATION |
| HU-039 | diagnostic | FAIL | PASS_WITH_LIMITATION |
| HU-040 | holdout, evaluation-only | FAIL | FAIL |
| HU-041 | diagnostic | FAIL | FAIL |
| HU-042 | diagnostic | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-043 | diagnostic | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-044 | diagnostic | FAIL | FAIL |
| HU-045 | holdout, evaluation-only | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-046 | diagnostic | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| HU-047 | diagnostic | FAIL | FAIL |
| HU-048 | diagnostic | FAIL | PASS |
| HU-057 | diagnostic | FAIL | FAIL |
| PERS-006 | diagnostic | PASS_WITH_LIMITATION | FAIL |

These verdicts are qualitative judgments against the case prompt and named manual rubric dimensions. Those rubrics do not define a frozen numeric pass threshold. The review does not modify the original JSONL rows, automated statuses, or primary accuracy totals. HU-005, HU-040, and HU-045 are holdout and used only for evaluation; no holdout data was used for training.

## Provenance and limitations

- Frozen Full470 case file SHA-256: `ac48af14e39bb14bc8a2e2f494720e4ae507ce6cd24527c34be06be1cf84bbbe`.
- The companion local audit records contain source-file and answer hashes; raw prompts and completions are not published here.
- This is one AI review without an independent second reviewer. Do not treat these twenty-four judgments as an independently validated score.
- HU-060 aggregate results informed P31 training-data design. Full470 therefore remains holdout-informed and exploratory, not an independent unbiased final estimate.
- The separate 58-pair latest-retry review is supplemental and is not merged into the primary metrics.
- Full acceptance remains open: 52 jointly REVIEW_REQUIRED primary pairs remain in this review group, and the speed, MTP/non-MTP, and official benchmark comparison gates are still outstanding.

No inference, benchmark run, model loading, or training was started in this update. The AI-Server RTX 3090 was idle and the shared GPU/RAM gate was paused; this work reviewed existing outputs only.