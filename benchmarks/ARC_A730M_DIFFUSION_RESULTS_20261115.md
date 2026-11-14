# Intel Arc A730M diffusion benchmark — 2026-11-15

## Results

- The commercial-use comparison contains 35 model/runtime configurations and 420 successful image results.
- Each configuration has 12 image cases. Resolution variants are separate configurations.
- The per-image CSV preserves every timing field present in the source runs, including model readiness, tensor loading, generation, client wall time, image write, and SHA-256 time where measured.
- The summary CSV records per-configuration mean timings, cold-load/compile time, suite wall time, peak dedicated/shared GPU memory, and minimum available system RAM where those fields were measured.
- Blank timing or revision fields mean the source run did not record that value; blank is not zero.
- 24 commercially eligible image results were removed from the blind pool after visual quality review. The blind pool contains 396 images, has no missing files, and supports username/alias and CSV/JSON result export.

## License exclusions

- FLUX1-Dev-Q4_K_S is excluded because its model license is non-commercial.
- RunDiffusion Juggernaut XL v9 and XL Lightning variants are excluded from commercial scoring and blind ranking. Their cards describe personal/creative use and require a separate license for paid API deployment. The stricter project filter keeps them out until explicit commercial-use rights are documented.
- Excluded runs remain in the local raw results tree; no model files or generated images were deleted.
- Conditional licenses remain conditional. The benchmark does not grant rights to third-party characters, brands, or people and does not establish copyright ownership of generated images.

## Files

- ARC_A730M_DIFFUSION_SUMMARY_20261115.csv — configuration-level summary.
- ARC_A730M_DIFFUSION_PER_IMAGE_20261115.csv — 420 per-image measurements and hashes.
- ARC_A730M_DIFFUSION_LICENSE_EXCLUSIONS_20261115.csv — excluded model families and reasons.
- Images are not embedded in these CSVs and have not been uploaded to GitHub.

## Test scope

Runs used the local Intel Arc A730M system and the recorded runtime/backend in each row. These results describe this laptop and the specific builds, settings, resolutions, and prompts in the CSVs; they should not be treated as hardware-independent rankings.
