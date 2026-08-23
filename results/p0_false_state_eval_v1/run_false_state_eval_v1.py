import json
import re
import time
import hashlib
from pathlib import Path
from collections import Counter, defaultdict
from contextlib import nullcontext

import torch
from transformers import AutoModelForImageTextToText, AutoTokenizer
from peft import PeftModel

BASE = Path(r"C:\Users\dbene\Models\Qwen3.5-9B-HF")
ADAPTER = Path(r"C:\Users\dbene\Models\BeniQwen-P0-LoRA")

DATA = Path(
    r"C:\Users\dbene\Downloads\echo_false_state_dataset_v0_1_r2_candidate"
    r"\echo_false_state_dataset_v0_1_frozen\data"
)

OUT = Path(r"C:\Users\dbene\Desktop\BeniQwen_Eval_P0")
OUT.mkdir(parents=True, exist_ok=True)

SURFACE_TO_STATE = {
    "IGEN": "KNOWN_TRUE",
    "NEM": "KNOWN_FALSE",
    "UNKNOWN": "UNKNOWN",
    "PROBABLE_ONLINE": "PROBABLE_ONLINE",
    "REVIEW_REQUIRED": "REVIEW_REQUIRED",
}

def parse_state(text):
    # Csak a válasz elejét értékeljük.
    # Triviális markdown/idézőjel megengedett, későbbi próza nem javíthat.
    s = text.strip().upper()
    s = re.sub(r'^[\s#>*_`"\']+', '', s)

    for token in [
        "REVIEW_REQUIRED",
        "PROBABLE_ONLINE",
        "KNOWN_TRUE",
        "KNOWN_FALSE",
        "UNKNOWN",
        "IGEN",
        "NEM",
    ]:
        if re.match(rf'^{re.escape(token)}(?:\b|\s|—|–|-|:)', s):
            return SURFACE_TO_STATE.get(token, token), token

    return "UNPARSEABLE", None

def prompt_hash(messages):
    raw = json.dumps(
        messages,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_rows():
    rows = []
    for split in ["validation", "challenge"]:
        path = DATA / f"{split}.jsonl"
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    assert row["messages"][-1]["role"] == "assistant"
                    row["_split"] = split
                    rows.append(row)
    return rows

def load_existing(path):
    done = {}
    if not path.exists():
        return done

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                x = json.loads(line)
                done[x["id"]] = x

    return done

print("LOAD_TOKENIZER")
tokenizer = AutoTokenizer.from_pretrained(ADAPTER)

print("LOAD_BASE")
model = AutoModelForImageTextToText.from_pretrained(
    BASE,
    dtype=torch.bfloat16,
    device_map="cuda",
)

print("LOAD_LORA")
model = PeftModel.from_pretrained(model, ADAPTER)
model.eval()

print("MODEL_READY")
print(
    "VRAM_GB",
    round(torch.cuda.memory_allocated() / 1024**3, 2)
)

rows = load_rows()

assert len(rows) == 240
assert len({r["id"] for r in rows}) == 240

torch.manual_seed(0)

for mode in ["base", "lora"]:
    outfile = OUT / f"{mode}_results.jsonl"
    existing = load_existing(outfile)

    print()
    print("=" * 72)
    print("MODE:", mode.upper())
    print("ALREADY_DONE:", len(existing))

    for index, row in enumerate(rows, 1):
        if row["id"] in existing:
            continue

        prompt_messages = row["messages"][:-1]

        prompt = tokenizer.apply_chat_template(
            prompt_messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=False,
        ).to("cuda")

        start = time.perf_counter()

        context = (
            model.disable_adapter()
            if mode == "base"
            else nullcontext()
        )

        with context:
            with torch.inference_mode():
                output = model.generate(
                    **inputs,
                    max_new_tokens=128,
                    do_sample=False,
                    use_cache=True,
                    pad_token_id=tokenizer.eos_token_id,
                )

        elapsed = time.perf_counter() - start

        generated = output[
            0,
            inputs["input_ids"].shape[1]:
        ]

        answer = tokenizer.decode(
            generated,
            skip_special_tokens=True
        ).strip()

        predicted, surface = parse_state(answer)
        expected = row["metadata"]["expected_state"]

        result = {
            "id": row["id"],
            "split": row["_split"],
            "category": row["metadata"]["category"],
            "risk": row["metadata"]["risk"],
            "evidence_strength": row["metadata"]["evidence_strength"],
            "expected_state": expected,
            "predicted_state": predicted,
            "surface_token": surface,
            "pass": predicted == expected,
            "prompt_hash": prompt_hash(prompt_messages),
            "answer": answer,
            "target": row["messages"][-1]["content"],
            "generation_tokens": int(generated.shape[0]),
            "elapsed_seconds": round(elapsed, 4),
        }

        with outfile.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(result, ensure_ascii=False)
                + "\n"
            )

        status = "PASS" if result["pass"] else "FAIL"

        print(
            f"{mode.upper():4} "
            f"{index:03}/240 "
            f"{row['_split']:10} "
            f"{row['id']} "
            f"{expected:16} -> "
            f"{predicted:16} "
            f"{status}"
        )

print()
print("GENERATION_COMPLETE")

def read_results(mode):
    path = OUT / f"{mode}_results.jsonl"
    with path.open("r", encoding="utf-8") as f:
        return [
            json.loads(line)
            for line in f
            if line.strip()
        ]

def summarize(mode, results):
    summary = {
        "mode": mode,
        "total": len(results),
        "splits": {},
        "overall": {},
        "categories": {},
    }

    def metrics(xs):
        n = len(xs)
        passed = sum(x["pass"] for x in xs)

        unique = {}
        for x in xs:
            unique.setdefault(x["prompt_hash"], x)

        upass = sum(x["pass"] for x in unique.values())

        return {
            "rows": n,
            "pass": passed,
            "fail": n - passed,
            "accuracy": round(passed / n, 6) if n else None,
            "unique_prompts": len(unique),
            "unique_pass": upass,
            "unique_fail": len(unique) - upass,
            "unique_accuracy": (
                round(upass / len(unique), 6)
                if unique else None
            ),
            "unparseable": sum(
                x["predicted_state"] == "UNPARSEABLE"
                for x in xs
            ),
        }

    summary["overall"] = metrics(results)

    for split in ["validation", "challenge"]:
        xs = [x for x in results if x["split"] == split]
        summary["splits"][split] = metrics(xs)

    categories = sorted({x["category"] for x in results})

    for category in categories:
        xs = [x for x in results if x["category"] == category]
        summary["categories"][category] = metrics(xs)

    confusion = defaultdict(Counter)

    for x in results:
        confusion[x["expected_state"]][x["predicted_state"]] += 1

    summary["confusion"] = {
        expected: dict(counts)
        for expected, counts in confusion.items()
    }

    return summary

base = read_results("base")
lora = read_results("lora")

assert len(base) == 240
assert len(lora) == 240

base_summary = summarize("base", base)
lora_summary = summarize("lora", lora)

report = {
    "dataset": "ECHO_FALSE_STATE_CORRECTIVE_V0_1_R2",
    "checkpoint_state": "CHECKPOINT_CANDIDATE",
    "scorer": "FIRST_STATE_TOKEN_STRICT_V1",
    "base": base_summary,
    "lora": lora_summary,
    "delta": {
        "row_accuracy": round(
            lora_summary["overall"]["accuracy"]
            - base_summary["overall"]["accuracy"],
            6
        ),
        "unique_accuracy": round(
            lora_summary["overall"]["unique_accuracy"]
            - base_summary["overall"]["unique_accuracy"],
            6
        ),
    },
}

summary_path = OUT / "summary.json"

with summary_path.open("w", encoding="utf-8") as f:
    json.dump(
        report,
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print("=" * 72)
print("FINAL SUMMARY")
print(json.dumps(report, ensure_ascii=False, indent=2))
print()
print("SUMMARY:", summary_path)
print("FALSE_STATE_EVAL_COMPLETE")
