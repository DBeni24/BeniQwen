# Handover – Echo P0 Cloud Training Bootstrap v1

## 1. Modul Identitása és Rendszerbeli Helye
Az Echo első fizetős false-state corrective LoRA training bootstrapja.

## 2. Adatmodell és Belső Állapotok
Dataset:
`CANDIDATE_R2 -> HUMAN_REVIEW_R2_PASS -> FROZEN`

Training:
`BOOTSTRAPPED -> MODEL_DOWNLOADED -> MODULES_INSPECTED -> DRYRUN_PASS -> TRAINING -> CHECKPOINT_CANDIDATE`

## 3. Állapotgép és Életciklus
- frozen dataset nélkül dry-run tiltott;
- dry-run PASS nélkül full P0 training tiltott;
- training után csak candidate adapter keletkezik;
- benchmark/review előtt nincs merge és nincs frozen checkpoint.

## 4. Kódolási és Fejlesztési Szigorítások
- vision tower trainable parameter = 0;
- benchmark validation/challenge nem mehet gradientbe;
- secretet scriptbe írni tilos;
- HF token csak környezeti változó / provider secret lehet;
- adapter-only save;
- target module lista actual model inspectionből.

## 5. Fejlesztési Állapot
`READY_FOR_CLOUD_BOOTSTRAP`, de dataset freeze gate még függőben.
