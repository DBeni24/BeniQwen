# Handover – Echo False-State Corrective Dataset v0.1

## 1. Modul Identitása és Rendszerbeli Helye

Az Echo training pipeline P0 epistemikus korrekciós datasetje. Célja a `FROZEN_BASELINE_V1_1` során azonosított false-state hibák csökkentése, különösen az `absence of evidence != evidence of absence` szabály megtanítása.

**KÓDBAN LÉTEZIK ebben a csomagban:** 960 szintetikus példa, split, validator, manifest, review sample.  
**DOKUMENTÁLVA VAN:** training cél, lifecycle, security, contamination szabály.  
**TERV:** LoRA/QLoRA pilot a dataset freeze után.  
**NINCS IMPLEMENTÁLVA:** training futás, merge, quant export, checkpoint benchmark.

## 2. Adatmodell és Belső Állapotok

Dataset state:
`DRAFT -> CANDIDATE_VALIDATED_SYNTACTICALLY -> HUMAN_REVIEWED -> FROZEN -> TRAINING_INPUT`

Példa expected state-ek:
- KNOWN_TRUE
- KNOWN_FALSE
- UNKNOWN
- PROBABLE_ONLINE
- REVIEW_REQUIRED

## 3. Állapotgép és Életciklus

1. Generálás.
2. Strukturális validator.
3. Benchmark contamination guard.
4. 40-case human review.
5. Javítás, ha szükséges.
6. Explicit freeze.
7. Csak frozen dataset használható training inputként.
8. Training után új checkpoint candidate.
9. Benchmark/review után lehet checkpoint frozen.

## 4. Kódolási és Fejlesztési Szigorítások

- Benchmark holdout prompt nem kerülhet trainingbe.
- `validation` és `challenge` split nem mehet gradientbe.
- Valódi secret, API kulcs, személyes adat tilos.
- Synthetic negative evidence nem taníthatja, hogy evidence hiánya = false.
- Conflict esetén REVIEW_REQUIRED.
- Training script csak a base modell architektúrájának tényleges inspectionje után készüljön; target module neveket nem találunk ki.

## 5. Fejlesztési Állapot

`CANDIDATE_VALIDATED_SYNTACTICALLY`

Következő gate: `docs/REVIEW_SAMPLE_40.md` emberi review + explicit freeze döntés.
