# Shared image-model benchmark protocol

This file defines the RTX 4090 comparison run using the frozen prompt pack: [ARC_IMAGE_MODEL_SHARED_TEST_PROMPTS_20261115.json](ARC_IMAGE_MODEL_SHARED_TEST_PROMPTS_20261115.json).

## Run plan

1. Confirm the exact model repository/revision, license terms, weight files, quantization, and required runtime before downloading.
2. Use the six prompts verbatim at 1024×1024 with seeds 42 and 1234: 12 images per model.
3. Use settings recommended for each model, but record sampler/scheduler, steps, guidance/CFG, precision, backend, and all deviations. Do not hide model-specific tuning.
4. Record download, runtime startup, cold model load, first compile/warmup, prompt encoding, image generation/denoising, VAE decode, PNG write, and end-to-end time separately wherever measurable. Use `null` when a stage is unavailable; do not estimate it from a total.
5. Record peak VRAM and system RAM, image dimensions/bytes, output SHA-256, errors, and whether CPU offload occurred.
6. Apply the objective pass checks in the JSON before subjective scoring. Report pass rate separately from preference/quality; do not count an image that misses explicit requirements as a correct output.
7. Keep one result row per generated image and a model-level summary. Preserve the exact prompt, seed, settings, output path, and timings so another run can be reproduced.

## Candidate scope

The initial RTX 4090 list is Qwen-Image-2512, HiDream-O1-Image, and Stable Diffusion 3.5 Large. Do not repeat the exact model configurations already benchmarked on the Intel Arc laptop. Verify each model's current license and any commercial-use limits at its official model card before the run.

## Output handling

Store generated images and logs on the benchmark machine. Publish prompt definitions and result metadata to the repository; add image files only when separately intended. Never publish credentials or access tokens.
