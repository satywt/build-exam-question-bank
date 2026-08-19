#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_KINDS = {"multiple_choice", "recall"}
ALLOWED_CONFIDENCE = {"high", "medium", "verify"}

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_question_bank.py BANK.json")
        return 2
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions") if isinstance(data, dict) else data
    if not isinstance(questions, list):
        print("ERROR: expected a questions array or a top-level array")
        return 1
    errors, seen = [], set()
    for i, q in enumerate(questions, 1):
        where = f"question {i}"
        qid = q.get("id")
        if not qid: errors.append(f"{where}: missing id")
        elif qid in seen: errors.append(f"{where}: duplicate id {qid}")
        else: seen.add(qid)
        if not str(q.get("stem", "")).strip(): errors.append(f"{where}: empty stem")
        if q.get("kind") not in ALLOWED_KINDS: errors.append(f"{where}: invalid kind")
        if q.get("confidence") not in ALLOWED_CONFIDENCE: errors.append(f"{where}: invalid confidence")
        if not q.get("sourceRefs"): errors.append(f"{where}: missing sourceRefs")
        if q.get("kind") == "multiple_choice":
            options = q.get("options", [])
            labels = {str(o.get("label")) for o in options if isinstance(o, dict)}
            if len(options) < 2: errors.append(f"{where}: fewer than two options")
            if str(q.get("answer")) not in labels: errors.append(f"{where}: answer does not match an option")
        if q.get("kind") == "recall" and not str(q.get("answerText", "")).strip():
            errors.append(f"{where}: recall question missing answerText")
        table = q.get("table")
        if table is not None:
            if not isinstance(table, dict):
                errors.append(f"{where}: table must be an object")
            else:
                headers, rows = table.get("headers"), table.get("rows")
                if not isinstance(headers, list) or not headers or any(not str(x).strip() for x in headers):
                    errors.append(f"{where}: table requires non-empty headers")
                if not isinstance(rows, list) or not rows:
                    errors.append(f"{where}: table requires rows")
                elif isinstance(headers, list):
                    for j, row in enumerate(rows, 1):
                        if not isinstance(row, list) or len(row) != len(headers):
                            errors.append(f"{where}: table row {j} does not match header count")
        media = q.get("media", [])
        if media and not isinstance(media, list):
            errors.append(f"{where}: media must be an array")
        elif isinstance(media, list):
            for j, item in enumerate(media, 1):
                if not isinstance(item, dict):
                    errors.append(f"{where}: media {j} must be an object")
                    continue
                if not str(item.get("type", "")).strip(): errors.append(f"{where}: media {j} missing type")
                if not str(item.get("file", item.get("url", ""))).strip(): errors.append(f"{where}: media {j} missing file or url")
                if not str(item.get("alt", "")).strip(): errors.append(f"{where}: media {j} missing alt text")
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors))
        print(f"FAILED: {len(errors)} issue(s) in {len(questions)} questions")
        return 1
    print(f"OK: {len(questions)} questions, {len(seen)} unique IDs")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
