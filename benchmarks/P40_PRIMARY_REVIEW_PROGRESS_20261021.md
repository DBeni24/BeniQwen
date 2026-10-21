# P40 Full470 primary review progress — 2026-10-21

## Reconciliation

- Source suite: 470 unique cases.
- Primary Base and LoRA: 470 rows each; case ID sets match.
- Both primary arms are REVIEW_REQUIRED on 76 cases.
- Additive qualitative manual review: 76/76 pairs complete; 0 remain pending.
- All 76 review records, source files, and Base/LoRA answers passed SHA-256 verification with 0 mismatches.
- Raw JSONL statuses and automatic metrics remain unchanged. Separate latest-retry manual review: 58 pairs; not merged into primary metrics.

## Reviewed cases

| Case | Base manual verdict | LoRA manual verdict |
|---|---|---|
| HU-001 | PASS_WITH_MINOR_ISSUES | PASS_WITH_MINOR_ISSUES |
| HU-003 | PASS_WITH_MINOR_ISSUES | PASS_WITH_LIMITATION |
| HU-005 | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-006 | FAIL | FAIL |
| HU-008 | PASS_WITH_MINOR_ISSUES | PASS |
| HU-011 | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-014 | PASS_WITH_LIMITATION | PASS |
| HU-018 | PASS_WITH_LIMITATION | FAIL |
| HU-028 | FAIL | FAIL |
| HU-033 | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-036 | FAIL | FAIL |
| HU-037 | FAIL | PASS_WITH_LIMITATION |
| HU-039 | FAIL | PASS_WITH_LIMITATION |
| HU-040 | FAIL | FAIL |
| HU-041 | FAIL | FAIL |
| HU-042 | FAIL | PASS_WITH_MINOR_ISSUES |
| HU-043 | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-044 | FAIL | FAIL |
| HU-045 | PASS_WITH_MINOR_ISSUES | FAIL |
| HU-046 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| HU-047 | FAIL | FAIL |
| HU-048 | FAIL | PASS |
| HU-049 | FAIL | FAIL |
| HU-050 | FAIL | FAIL |
| HU-051 | PASS_WITH_LIMITATION | FAIL |
| HU-052 | FAIL | FAIL |
| HU-053 | FAIL | FAIL |
| HU-054 | PASS_WITH_LIMITATION | FAIL |
| HU-055 | PASS_WITH_LIMITATION | FAIL |
| HU-056 | FAIL | FAIL |
| HU-057 | FAIL | FAIL |
| HU-058 | PASS_WITH_LIMITATION | FAIL |
| HU-059 | FAIL | FAIL |
| PERS-002 | FAIL | PASS_WITH_LIMITATION |
| PERS-003 | FAIL | PASS_WITH_LIMITATION |
| PERS-004 | PASS_WITH_LIMITATION | FAIL |
| PERS-006 | PASS_WITH_LIMITATION | FAIL |
| PERS-007 | FAIL | FAIL |
| PERS-008 | FAIL | PASS_WITH_LIMITATION |
| PERS-009 | PASS_WITH_LIMITATION | FAIL |
| PERS-011 | FAIL | PASS_WITH_LIMITATION |
| PERS-013 | FAIL | PASS_WITH_LIMITATION |
| PERS-014 | FAIL | FAIL |
| PERS-015 | FAIL | FAIL |
| PERS-016 | FAIL | FAIL |
| PERS-017 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| PERS-018 | FAIL | FAIL |
| PERS-019 | FAIL | PASS |
| PERS-021 | FAIL | FAIL |
| PERS-022 | FAIL | PASS_WITH_LIMITATION |
| PERS-023 | PASS_WITH_LIMITATION | FAIL |
| PERS-026 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| PERS-028 | FAIL | FAIL |
| PERS-030 | FAIL | FAIL |
| PERS-031 | FAIL | PASS_WITH_LIMITATION |
| PERS-032 | PASS | PASS |
| PERS-034 | PASS_WITH_LIMITATION | PASS |
| PERS-038 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| PERS-039 | FAIL | PASS_WITH_LIMITATION |
| PERS-040 | PASS_WITH_LIMITATION | PASS |
| RSN-006 | PASS_WITH_LIMITATION | FAIL |
| RSN-007 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| RSN-008 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| RSN-009 | PASS_WITH_LIMITATION | FAIL |
| RSN-011 | FAIL | PASS |
| RSN-013 | FAIL | PASS |
| RSN-016 | PASS | PASS_WITH_LIMITATION |
| RSN-018 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| RSN-019 | FAIL | PASS |
| RSN-020 | FAIL | FAIL |
| RSN-021 | FAIL | PASS_WITH_LIMITATION |
| RSN-022 | FAIL | FAIL |
| RSN-024 | FAIL | PASS_WITH_LIMITATION |
| RSN-025 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| RSN-029 | PASS_WITH_LIMITATION | PASS_WITH_LIMITATION |
| RSN-030 | FAIL | FAIL |

Case visibility and review-file hashes are in the companion JSON; per-answer source and output hashes are in the additive batch records.

This is a single-AI-review supplement without an independent second reviewer; manual rubrics have no frozen numeric threshold. HU-060 aggregate results informed P31 data design, so Full470 remains holdout-informed and exploratory. The holdouts reviewed here were: 
HU-005, HU-040, HU-045, HU-050, HU-055, PERS-015, PERS-030, PERS-040, RSN-020, RSN-025, RSN-030
. They were used only for evaluation, not training.

Full acceptance remains OPEN: this manual supplement does not clear the original REVIEW_REQUIRED statuses. Speed, MTP/non-MTP, official benchmark, packaging, and protocol verification remain unfinished.

The shared GPU/RAM gate is paused. The AI-Server RTX 3090 showed 0% utilization, 95 MiB VRAM used, and no active Ollama model. LM Studio and Python processes remain present but were not stopped; their model workload status was not established. No model workload was started.
## Paired verdict transitions for the 76 REVIEW_REQUIRED pairs

Derived from the case-level `primary_manual_review.reviewed` ledger captured at 2026-10-21 23:36 CEST. Counts are qualitative reviewer labels, not a numeric quality score.

| Base verdict | LoRA verdict | Pairs |
|---|---|---:|
| FAIL | FAIL | 25 |
| FAIL | PASS | 5 |
| FAIL | PASS_WITH_LIMITATION | 12 |
| FAIL | PASS_WITH_MINOR_ISSUES | 3 |
| PASS | PASS | 1 |
| PASS | PASS_WITH_LIMITATION | 1 |
| PASS_WITH_LIMITATION | FAIL | 11 |
| PASS_WITH_LIMITATION | PASS | 3 |
| PASS_WITH_LIMITATION | PASS_WITH_LIMITATION | 9 |
| PASS_WITH_MINOR_ISSUES | FAIL | 3 |
| PASS_WITH_MINOR_ISSUES | PASS | 1 |
| PASS_WITH_MINOR_ISSUES | PASS_WITH_LIMITATION | 1 |
| PASS_WITH_MINOR_ISSUES | PASS_WITH_MINOR_ISSUES | 1 |
| **Total** |  | **76** |

This is a single-AI-review supplement without an independent second reviewer or a frozen numeric pass threshold. It does not alter raw `REVIEW_REQUIRED` statuses or automatic scores. Eleven of the reviewed pairs are evaluation-only holdouts; HU-060-informed P31 data selection means the Full470 remains exploratory, not an independent unbiased estimate.

