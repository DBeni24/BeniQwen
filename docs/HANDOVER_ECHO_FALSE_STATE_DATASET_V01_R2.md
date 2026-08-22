# Handover – Echo False-State Corrective Dataset v0.1 R2

## 1. Modul Identitása és Rendszerbeli Helye
Az Echo P0 false-state corrective dataset R2 nyelvi javítása.

## 2. Adatmodell és Belső Állapotok
`CANDIDATE_R1 -> HUMAN_REVIEW_NEEDS_FIX -> CANDIDATE_R2_VALIDATED_SYNTACTICALLY -> HUMAN_REVIEW_R2 -> FROZEN`

## 3. Állapotgép és Életciklus
1. R1 logikai review PASS, nyelvi review NEEDS_FIX.
2. R2 target rewrite.
3. Strukturális és contamination validáció.
4. Ugyanazon 40 ID R2 human review-ja.
5. Explicit PASS után FROZEN.
6. Csak FROZEN dataset használható training inputként.

## 4. Kódolási és Fejlesztési Szigorítások
- validation/challenge nem mehet gradientbe;
- benchmark prompt nem kerülhet trainingbe;
- real secret/user data tilos;
- language rewrite nem módosíthat evidence->state mappinget;
- conflict -> REVIEW_REQUIRED;
- UNKNOWN -> unsupported state tilos.

## 5. Fejlesztési Állapot
`CANDIDATE_R2_VALIDATED_SYNTACTICALLY`

Következő gate: `docs/REVIEW_SAMPLE_40_R2.md`.
