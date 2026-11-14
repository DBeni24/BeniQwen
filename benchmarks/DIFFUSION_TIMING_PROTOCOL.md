# Diffúziós benchmark – időmérési szabályzat

Kutatási / naplózási frissítés: 2026-11-14

## Alapelv

Minden ténylegesen mérhető idő külön mezőbe kerül, futásonként és az egyes képekre bontva. Nem következtetünk ki szakaszidőt egy összesített időből. Ha a backend egy szakaszt nem tesz megfigyelhetővé, annak értéke `not_exposed`; ha az adott modellnél nem releváns, `not_applicable`; ha hibás vagy hiányzó mérés, `invalid` vagy `missing`. A nullát csak valóban mért nulla jelentheti.

Egy időrekord tartalmazza: futásazonosító, UTC kezdés és befejezés, monotón órával mért idő ms-ban, mért szakasz, adatforrás (`backend_metric`, `timestamped_log`, `external_stopwatch`, `client_clock`), hideg/meleg státusz, valamint rövid megjegyzés. Az átfedő szakaszokat külön jelöljük, és nem adjuk össze őket.

## Kötelező időfázisok

| Szakasz | Mit mérünk |
|---|---|
| Súlyletöltés | Kérés/átvitel indítása → utolsó bájt; külön a fájlellenőrzés és SHA-256 számítás. Ezt nem keverjük az inference-idővel. |
| Runtime előkészítése | Futócsomag letöltése, kicsomagolása és a tényleges környezet összeállítása, külön-külön, ha mind megtörténik. |
| Folyamatindítás | Program indítása → API/UI vagy CLI mérésre kész állapot. A szerver „ready” jelét/ellenőrzését meg kell nevezni. |
| Modellbetöltés | Teljes modellbetöltés, illetve a transformer/UNet, minden text encoder, VAE, LoRA/adapter és prompt-upsampler külön ideje, ha a futtató megmutatja. |
| Első használat/JIT | Első shader/kernel fordítás, cache felépítése, első prompt vagy más egyszeri inicializálás. Ha ez csak az első kérés összidejébe olvad, ezt így jelöljük; nem vonjuk le becsléssel. |
| Várakozás és előkészítés | Kliensoldali küldés, szerver-várólista, execution lock/ütemezés, prompt előfeldolgozás/tokenizálás és szövegkódolás, mind külön, ahol látható. |
| Képgenerálás | Conditioning, denoising/sampling teljes ideje; high/low-noise vagy több pass esetén passonként is, ha a backend megadja. Rögzítjük a lépésszámot és a lépésenkénti időt, ha mérhető. |
| VAE | Dekódolás külön; img2img esetén VAE-encode is. Tiled VAE esetén a használt módot és az időt is rögzítjük. |
| Utómunka és kimenet | Upscaler/ADetailer egyéb utómunka, pixel/postprocess, PNG/JPEG/WebP-kódolás, fájlírás, majd válasz-/képátvitel a klienshez. |
| Teljes idő | Szerverkérés beküldése → teljes kép/kimenet átvehető. Külön számoljuk a folyamatindítástól az első használható képig tartó end-to-end időt. |
| Leállítás | Modell kiürítése/folyamat leállítása, ha ez a futtatóval mérhető és releváns a manuális esti munkamenethez. |

Minden képnél külön megőrizzük a teljes kérésidőt és a fenti szakaszidőket. Minden egyedi minőségteszt-prompt és seed saját időrekordot kap. A hideg indulás/első kép külön fut; utána legalább három meleg ismétlés készül. Az összefoglaló közli az összes nyers futást, valamint a mediánt, minimumot, maximumot és átlagot. A hibás, megszakadt és újrapróbált futások is szerepelnek.

## Futásmód és összehasonlítás

- Az Intel A730M-en GPU-only, CPU-offload nélküli teszt az elsődleges, ha a modell és a 12 GB VRAM ezt engedi.
- **Ami az Intelen sikeresen fut, azt nem futtatjuk le újra a 4090-en.** A 4090-es szakasz külön jelöltlistát kap, csak olyan modellekhez, amelyek az Intel gépen VRAM- vagy kompatibilitási korlát miatt nem tesztelhetők megfelelően. Ismételt futás más GPU-n csak későbbi, külön összehasonlítási kérésre történhet.
- A 4090-es teszt is ugyanazt a fázislistát használja; a CUDA-s aszinkron műveletek időmérése előtt/után szinkronizálni kell, ha közvetlen GPU-időt állítunk.
- A modell seed/prompt/minőségtesztje azonos marad, amennyiben az architektúra és a licenc engedi; a felbontást, lépésszámot, quantot és runtime-ot külön rögzítjük. Eltérő konfigurációból nem állítunk közvetlen sebességgyőzelmet.

## Mit tesznek lehetővé a jelenlegi futtatók?

- A jelenlegi stable-diffusion.cpp szerverprotokoll szakaszokat nevez meg: queued/waiting, preparing, conditioning, sampling, VAE encode/decode, upscaling, ADetailer, encoding; tartalmaz szakaszidőt és queue nélküli feladatidőt. Az aktuális laptop-bináris e92e86f régebbi, ezért előbb verzió- és API-ellenőrzés kell; az új dokumentációs mezőket nem feltételezzük visszamenőleg.
- Az OpenVINO GenAI `ImageGenerationPerfMetrics` dokumentáltan mérheti a modellbetöltést, teljes generálási időt, text encoder(ek), transformer/UNet és VAE szakaszok idejét. Ez a GenAI pipeline mérőfelülete; az OVMS REST útvonalon külön csak azt tekintjük mérhetőnek, amit a használt OVMS build ténylegesen logol vagy metricsként kitesz.
- ComfyUI-nál a szerver „Prompt executed” ideje és a node logok rögzíthetők. A core végrehajtás összes ideje nem tartalmazza automatikusan a szerver-várakozást; ezért kliensoldali kérés→kimenet falióra is kell. A kikapcsolt PyTorch XPU útvonal miatt ezt nem tekintjük jelenlegi A730M tesztbackendnek.
- Ha a backend csak összesített request-időt ad, a részek `not_exposed` értéket kapnak. A teljes időből tilos text encoder, sampling, VAE vagy PNG időkülönbséget kitalálni.

## A meglévő tesztek időadatai

A korábbi CSV-k részben már tartalmazzák a `ProcessReadySeconds`, `TensorLoadSeconds`, `GenerateSeconds`, `WallSeconds`, illetve FLUX/OVMS esetén a `ColdModelLoadSeconds`, `RequestSeconds` és `PNGWriteSeconds` mezőket. Ezeket a meglevő méréseket változatlanul megőrizzük. Csak a forrásnaplóban ténylegesen látható részeredmény kerülhet utólag kitöltésre; hiányzó encoder/sampling/VAE idők nem rekonstruálhatók az összidőből.

A korábbi futások nem minősülnek teljes fázisbontásúnak ott, ahol csak aggregált mezőjük van. Az új, hiányzó fázisokra vonatkozó rekordok `not_exposed` megjelöléssel készülnek; nem futtatjuk újra automatikusan a már elkészült modellteszteket.

## Források

- [stable-diffusion.cpp szerver API – progress szakaszok és stage_elapsed_ms](https://github.com/leejet/stable-diffusion.cpp/blob/master/examples/server/api.md#progress)
- [OpenVINO GenAI ImageGenerationPerfMetrics](https://docs.openvino.ai/2026/api/genai_api/_autosummary/openvino_genai.ImageGenerationPerfMetrics.html)
- [OpenVINO Model Server – usage monitoring és /metrics](https://docs.openvino.ai/2026/model-server/ovms_docs_troubleshooting.html#usage-monitoring)
- [ComfyUI core – prompt végrehajtási idő](https://github.com/Comfy-Org/ComfyUI/blob/master/main.py)

