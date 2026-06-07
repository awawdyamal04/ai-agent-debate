"""
Verification script — run after a debate to confirm all requirements are met.
Usage: python tests/verify.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RESULTS = Path(__file__).resolve().parent.parent / "results"
SRC = Path(__file__).resolve().parent.parent / "src"
PASS = "PASS"
FAIL = "FAIL"


def check(label: str, ok: bool, detail: str = "") -> bool:
    tag = f"[{PASS}]" if ok else f"[{FAIL}]"
    msg = f"{tag} {label}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return ok


def main() -> int:
    results: list[bool] = []

    # 1. transcript.json exists and is valid JSON
    t_path = RESULTS / "transcript.json"
    try:
        transcript = json.loads(t_path.read_text())
        results.append(check("transcript.json exists and is valid JSON", True))
    except Exception as exc:
        results.append(check("transcript.json exists and is valid JSON", False, str(exc)))
        transcript = {}

    # 2. At least 10 exchanges
    msgs = transcript.get("messages", [])
    pro_msgs = [m for m in msgs if m.get("speaker") == "Pro"]
    con_msgs = [m for m in msgs if m.get("speaker") == "Con"]
    results.append(check("≥ 10 Pro messages", len(pro_msgs) >= 10, f"found {len(pro_msgs)}"))
    results.append(check("≥ 10 Con messages", len(con_msgs) >= 10, f"found {len(con_msgs)}"))

    # 3. Pro and Con maintain opposite stances
    pro_stances = {m.get("stance") for m in pro_msgs}
    con_stances = {m.get("stance") for m in con_msgs}
    results.append(check("Pro stance is PRO", pro_stances == {"PRO"}, str(pro_stances)))
    results.append(check("Con stance is CON", con_stances == {"CON"}, str(con_stances)))

    # 4. verdict.json has exactly one winner
    v_path = RESULTS / "verdict.json"
    try:
        verdict = json.loads(v_path.read_text())
        winner = verdict.get("winner", "")
        results.append(check("verdict.json valid and has winner", winner in ("Pro", "Con"), f"winner={winner}"))
    except Exception as exc:
        results.append(check("verdict.json valid", False, str(exc)))

    # 5. Required files exist
    for fname in ["transcript.json", "evidence.json", "verdict.json", "run_summary.json"]:
        p = RESULTS / fname
        results.append(check(f"results/{fname} exists", p.exists()))

    events = (RESULTS / "events.jsonl").exists() or (RESULTS / "debate.log").exists()
    results.append(check("results/events.jsonl or debate.log exists", events))

    # 6. All Python files under src/ are ≤ 150 lines
    py_files = list(SRC.rglob("*.py"))
    over_limit = []
    for f in py_files:
        lines = len(f.read_text(encoding="utf-8").splitlines())
        if lines > 150:
            over_limit.append(f"{f.relative_to(SRC.parent)}:{lines}")
    results.append(check("All src/ .py files ≤ 150 lines", not over_limit,
                         ", ".join(over_limit) if over_limit else "all OK"))

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*50}")
    print(f"Result: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
