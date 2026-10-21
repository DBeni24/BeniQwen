# P40 Full470 audit — 2026-10-21

## Status

The fixed-protocol Full470 execution gate is complete: both Base and P40-LoRA have one result for each of the 470 cases. Quality acceptance is still open. This report separates the primary paired run from supplemental higher-budget retries.

## Pairing and provenance

- Base: 470 rows, 470 unique case IDs.
- P40-LoRA: 470 rows, 470 unique case IDs.
- The case ID sets match exactly.
- All 27 source-file SHA-256 entries in the reconciled audit matched the current source files.
- Request metadata matched in all 470 pairs except the adapter identifier. Both arms used BF16 on CUDA, 8,192-token context, a 3,200-token output cap, reasoning off, and matching EOS token IDs.
- Base used no adapter. P40-LoRA used adapter SHA-256 `d91c062da1c9591ceca4a13c27782648448a21d59e7a4db7a7565269c0916bac`.

## Fixed-protocol primary results

| Arm | Pass | Fail | Review required | Output budget hit |
|---|---:|---:|---:|---:|
| Base | 257 (54.7%) | 54 (11.5%) | 76 (16.2%) | 83 (17.7%) |
| P40-LoRA | 308 (65.5%) | 27 (5.7%) | 134 (28.5%) | 1 (0.2%) |

These are raw automated result-status counts from the fixed-protocol primary runs, not a manually reconciled final classification or a single aggregate quality score. In the paired primary run, LoRA has 51 more PASS classifications and 27 fewer FAIL classifications, while 58 more cases are REVIEW_REQUIRED. The review queue remains material and prevents a final quality-acceptance claim.

## Supplemental retry audit

Retries used progressively larger output budgets and are not merged into the fixed-protocol primary comparison. Selecting the highest completed retry tier per case yields:

| Arm | Pass | Fail | Review required | Remaining output budget hits |
|---|---:|---:|---:|---:|
| Base | 259 | 77 | 134 | 0 |
| P40-LoRA | 308 | 28 | 134 | 0 |

The final 32,768-context PERS-027 pair completed without truncation, context overflow, output-budget hit, OOM retry, or runtime error. Base produced 1,747 tokens and LoRA 41 tokens; both remain REVIEW_REQUIRED. The earlier 16K PERS-027 Base attempt hit its 13,200-token cap, and SEC-024 remained REVIEW_REQUIRED in both arms.

## Manual-review status after later retries

The earlier GitHub manual reconciliation reported Base 259 PASS / 76 FAIL / 135 REVIEW_REQUIRED and LoRA 308 / 28 / 134. Its HU-060 Base result was REVIEW_REQUIRED after the 3,072-token targeted retry. The later 10/20 doubled-budget HU-060 retry changed the raw Base result to FAIL at 656 words; LoRA also fails at 1,189 words. The latest retry-tier automated counts are Base 259 PASS / 77 FAIL / 134 REVIEW_REQUIRED and LoRA 308 / 28 / 134. No fresh full manual adjudication was performed after these newer outputs, so the earlier manually reconciled aggregate must not be presented as current for the latest retry selection.

## Holdout-lineage caveat

The P40 release manifest and the P31–P40 provenance audit record that P31 development used the aggregate HU-060 holdout outcome to select three synthetic 450–650-word training examples. No HU-060 prompt or answer was copied, and the manifest records zero direct holdout source rows and zero holdout gradient rows. This is still holdout-informed data design: the P40 Full470 comparison is exploratory and cannot be called holdout-independent. No training was run during this audit.
## Acceptance decision

- **Execution complete:** yes, 470/470 results per arm, matched case set and request protocol.
- **Output-budget execution gaps:** closed in the latest retry tier; zero unresolved budget-hit cases.
- **Quality acceptance complete:** no. Primary and latest retry classifications still contain FAIL and REVIEW_REQUIRED cases.
- Supplemental retries are evaluation-only and were not used to change training data or weights.

## Evidence

- Reconciled source and retry audit: `P40_FULL470_AUDIT_RECONCILED_20261021.json`
- Current primary source hashes and result rows are listed in that audit's `source_file_sha256` and `primary_integrity` sections.
## Open quality gates to resolve or explicitly accept

- **RAG-026 — missing information:** P40-LoRA's primary result is `FAIL` with `expected_exact:UNKNOWN` and critical violation `UNSUPPORTED_CLAIM`. The latest doubled-budget Base and LoRA retries also fail this case. This is an evidence-grounding failure, not an output-cap problem.
- **HU-060 — language trap / response length:** both primary arms hit the 3,200-token output cap. On the doubled-budget retries, Base fails the word limit at 656 words and LoRA at 1,189 words; the LoRA audit flags excessive verbosity. Raising the output cap therefore exposes the length failure rather than resolving it.

No case prompt or completion was copied into the training set, but the aggregate HU-060 outcome influenced P31 data selection as documented above. No additional training was run as part of this audit.


## Supplemental PERS-027 qualitative review — 2026-10-21

A single Codex AI review was recorded for the completed 32K paired retry. Base is judged FAIL: its 732-word answer exceeds the 180-word soft limit and invents codebase details not supplied in the case. P40-LoRA is judged PASS with a minor usefulness limitation: its 23-word Hungarian roast fits the requested tone, while offering no repair advice. Both raw retry rows remain REVIEW_REQUIRED; this single supplemental judgement does not change primary counts or close Full470 quality acceptance. It was not independently double-scored.

- Review evidence: PERS-027_32768_SUPPLEMENTAL_MANUAL_REVIEW_20261021.json
- Full470 quality acceptance remains open because unresolved FAIL and REVIEW_REQUIRED cases remain.
## Retry review delta — 2026-10-21 19:35 CEST

A fresh comparison of the authoritative primary and retry JSONL files found the following review delta. Current raw retry status counts are Base 259 PASS / 77 FAIL / 134 REVIEW_REQUIRED / 0 output-budget hits and P40-LoRA 308 PASS / 28 FAIL / 134 REVIEW_REQUIRED / 0 output-budget hits. These retry counts remain separate from the fixed-protocol primary comparison.

- Base: 58 current REVIEW_REQUIRED outputs are new relative to the old manual review layer (56 produced by the output-budget retry tiers and two by the 16K/32K follow-up). All 58 Base outputs in this fresh-review delta have now been manually reviewed; none remain.
- P40-LoRA: 29 retry answers differ from their primary answer text. Of those, 26 retain REVIEW_REQUIRED and need fresh manual adjudication; the remaining three are two PASS rows and HU-060, which is a scorer FAIL. All 26 changed LoRA review outputs have been manually reviewed; none remain.
- HU-060 is a holdout: the exact 450–650 word contract is missed by both latest retries (Base 656 words; LoRA 1,189). It remains evaluation-only.
- The manual judgments are one AI review, not an independent second review. Raw scorer statuses are unchanged. No prompts/completions were published or used for training.

The latest-retry delta inventory and the eighteen review batches are recorded in `P40_LATEST_RETRY_REVIEW_DELTA_20261021.json` and `P40_LATEST_RETRY_MANUAL_REVIEW_20261021.md` / `.json`. The Full470 quality gate remains open, including the critical RAG-026 unsupported-availability claim.
## Supplemental SEC-024 qualitative review — 2026-10-21

The 16K paired retry completed in both arms. Base is judged FAIL: 418 words against the 230-word soft cap, with an unsupported blanket statement about compliance standards. P40-LoRA is judged PASS with minor language issues: it gives the least-privilege explanation in 60 words but contains one malformed Hungarian compound. Both raw rows remain REVIEW_REQUIRED; the primary and retry JSONL scores are unchanged. This is a single AI review, not an independent second score.

## Supplemental HU diagnostic reviews — 2026-10-21

Three Base latest-retry cases were adjudicated against the pinned Hungarian-language rubric. HU-009 Base fails for 381 words against a 220-word cap and misleading RAM/VRAM claims; LoRA passes at 31 words. HU-012 Base fails for 265 words and incorrectly describing offload as automatic; LoRA passes with a limitation because it names one valid failure outcome but is incomplete. HU-013 Base fails for 408 words and broad unsupported size-versus-hallucination claims; LoRA passes with a limitation because its task-fit explanation is plausible but underqualified. The raw JSONL statuses remain REVIEW_REQUIRED in both arms and are unchanged. These are single-review judgements; no prompt/completion text was stored or used for training.

## Supplemental HU technical-term reviews — 2026-10-21

HU-016 Base fails (512 words versus a 240-word cap; confuses lease expiry with task expiry); LoRA is concise but overstates that a lease prevents overlap without fencing. HU-017 Base fails (391 words, awkward terminology, and unsubstantiated automatic-recovery claims); LoRA captures the liveness role but has a Hungarian grammar defect and omits periodicity. HU-019 Base fails (360 words and assumes candidate/frozen always imply production lifecycle states); LoRA clearly distinguishes an unfinalized candidate from a fixed checkpoint. Both raw arms remain REVIEW_REQUIRED and unchanged. These are single-review judgements; no prompt/completion text was stored or used for training.

## Supplemental HU retrieval-term reviews — 2026-10-21

HU-021 Base fails for exceeding the soft cap and contradicting the pinned conflict-handling instruction; LoRA correctly states the active-only filter. HU-022 Base fails for excessive length and unsupported claims about metadata effects on embeddings/index distributions; LoRA gives the core metadata-filtering rationale. HU-023 Base is accurate but overlong (309 words versus a 240-word cap); LoRA gives a clear one-sentence definition. All six raw rows remain REVIEW_REQUIRED and unchanged. These are single-review judgements; no prompt/completion text was stored or used for training.

## Supplemental HU model-concept reviews — 2026-10-21

HU-024 Base fails for excessive length and a confusing prerequisite-edge example; LoRA gives a concise correct graph definition. HU-026 Base fails for a major memory-scale error and confusing Q4 inference with training; LoRA omits the requested Q4/BF16 comparison, so both fail. HU-027 Base is overlong and overclaims LoRA forgetting protection; LoRA states the core weight-update distinction, with the practical tradeoff omitted. All raw results remain unchanged. These are single-review judgements; no prompt/completion text was stored or used for training.

## Supplemental HU offload, security and recovery reviews — 2026-10-21

HU-029 fails in both arms: Base confuses CPU offload with repeated per-token PCIe swapping; LoRA does not explain offload and reverses its purpose. HU-031 fails in both arms: Base exceeds the short-answer cap and overstates service isolation; LoRA gives a direct “no” but no justification. HU-032 Base fails for excessive length and contradictory/dangerous Git recovery steps; LoRA is reassuring and non-destructive but lacks a precise safe recovery step. All six raw retry rows remain REVIEW_REQUIRED and unchanged. These are single-review judgements; no prompt/completion text was stored or used for training.

## Supplemental HU holdout reviews — 2026-10-21

HU-010 Base fails for excessive length and conflating lease expiration with requeue; LoRA gives the core definitions but assumes queue position/behavior. HU-015 Base fails for verbosity and irrelevant generic detail; LoRA names a next step but lacks readiness checks. HU-020 Base and LoRA both overstate quarantine/rejected lifecycle semantics, with Base also far over the length cap. These three holdouts were used only for evaluation and remain excluded from training; raw statuses are unchanged. This is single-review evidence.

## Final retry-delta review — 2026-10-21

The remaining 11 paired latest-retry cases have now been qualitatively reviewed from the saved outputs. This closes the Base fresh-review delta at 58/58; all 26/26 changed LoRA retry outputs were already reviewed. Four cases in this final group (HU-025, HU-030, PERS-010 and PERS-025) are holdouts and were used only for evaluation; across the retry review, 15 holdout cases remain excluded from training. Raw JSONL statuses and the fixed-protocol primary scores are unchanged. The manual layer is a single AI qualitative review, not an independent second score. Full470 quality acceptance remains open; this supplemental review does not resolve all primary FAIL/REVIEW_REQUIRED outcomes or the remaining benchmark and package gates.

Case-level evidence, reasons and output hashes are in P40_LATEST_RETRY_MANUAL_REVIEW_20261021.md and the companion JSON. The final group verdicts are Base: 11 FAIL; P40-LoRA: 2 FAIL and 9 pass variants (including limitations/minor issues).


## Supplemental RAG-026 exact-protocol retry — 2026-10-21 19:01 CEST

A saved supplemental exact-protocol pair completed on the AI-Server RTX 3090 with BF16, CUDA-only, MTP off, 8,192 context and a 50-token output cap. Base hit the output cap; P40-LoRA completed with FAIL for the critical unsupported claim. This attempt is incomplete as a Base quality verdict. The earlier exact-protocol 100-token pair completed and failed in both arms, so the issue remains unresolved. This evidence is supplementary and is not merged into the fixed-protocol Full470 or latest-tier aggregate. No training or holdout use occurred, and no prompt/completion text is reproduced here.

- Pair metadata: rag026-exact-protocol-retry-20261021/manifest.json and paired_summary.json
- Base: 50-token output-budget hit; elapsed 7.8026 s; result SHA-256 92900382703172D25A8A09DDB5027B89DB18BCBB25BEC3E0A40F856D9510CA7E
- P40-LoRA: completed FAIL / UNSUPPORTED_CLAIM at 2 output tokens; elapsed 3.7899 s; result SHA-256 8801B199ED65B3837515FBB2DD550EB7B586CA5C51A929ADF2DA7CC1008828DF
- Prior exact-protocol 100-token pair: Base FAIL and LoRA FAIL.

## Retry review provenance reconciliation — 2026-10-21

The 58-case latest-retry manual review contains 116 Base/LoRA rows. A read-only reconciliation against the saved result files confirms all 116 raw statuses and output-token counts. After applying the existing ten-row/five-pair source correction, the 114 non-PERS-027-32K answer hashes match their selected `final_answer` text. The two PERS-027 32K fields previously named `output_sha256` were actually hashes of the complete `results.jsonl` files; the file hashes and the separately computed answer hashes are recorded in `P40_RETRY_REVIEW_PERS027_CONTEXT32_HASH_CLARIFICATION_20261021.json`. No output, status, or manual verdict was changed.

The 58 retry-review cases are disjoint from the 76 primary reviewed cases (134 distinct reviewed IDs total); 15 retry-review cases are holdouts and remain evaluation-only. These are single-review qualitative judgments, with no independent second reviewer or frozen numeric pass threshold. Do not merge this supplemental cohort into the fixed-protocol primary score or describe the P40 comparison as an independent unbiased estimate: the P31 lineage was informed by aggregate HU-060 holdout results. The retry review remains exploratory and does not close Full470 acceptance.

The AI-Server gate remains paused (`allow_gpu_ram=false`). Read-only live inspection found the RTX 3090 at 0% utilization with 95 MiB allocated and `ollama ps` empty. No inference, benchmark, training, or model-load work was started.
