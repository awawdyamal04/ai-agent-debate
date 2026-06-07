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

    # 2b. All transcript messages are valid JSON objects
    bad_msgs = [i for i, m in enumerate(msgs) if not isinstance(m, dict)]
    results.append(check("all transcript messages are valid JSON objects", not bad_msgs,
                         f"bad at indices: {bad_msgs[:3]}" if bad_msgs else "all OK"))

    # 2c. All messages include 'status' field
    no_status = [i for i, m in enumerate(msgs) if "status" not in m]
    results.append(check("all messages include 'status' field", not no_status,
                         f"missing at: {no_status[:3]}" if no_status else "all have status"))

    # 3. Pro and Con maintain opposite stances
    pro_stances = {m.get("stance") for m in pro_msgs}
    con_stances = {m.get("stance") for m in con_msgs}
    results.append(check("Pro stance is PRO", pro_stances == {"PRO"}, str(pro_stances)))
    results.append(check("Con stance is CON", con_stances == {"CON"}, str(con_stances)))

    # 4. verdict.json has exactly one winner (no tie)
    v_path = RESULTS / "verdict.json"
    winner = ""
    try:
        verdict = json.loads(v_path.read_text())
        winner = verdict.get("winner", "")
        results.append(check("verdict.json valid and has winner", winner in ("Pro", "Con"), f"winner={winner!r}"))
        results.append(check("no tie — winner is exactly Pro or Con", winner in ("Pro", "Con"), f"winner={winner!r}"))
    except Exception as exc:
        results.append(check("verdict.json valid", False, str(exc)))
        results.append(check("no tie — winner is exactly Pro or Con", False, "verdict.json unreadable"))

    # 5. Required files exist
    for fname in ["transcript.json", "evidence.json", "verdict.json", "run_summary.json"]:
        p = RESULTS / fname
        results.append(check(f"results/{fname} exists", p.exists()))

    events = (RESULTS / "events.jsonl").exists() or (RESULTS / "debate.log").exists()
    results.append(check("results/events.jsonl or debate.log exists", events))

    # 5b. Demo/fallback evidence is clearly labelled
    fallback_msgs = [m for m in msgs if isinstance(m, dict) and m.get("tool_metadata", {}).get("fallback_used")]
    if fallback_msgs:
        unlabelled = []
        for m in fallback_msgs:
            for ev in m.get("evidence", []):
                if isinstance(ev, dict):
                    lbl = ev.get("label", "")
                    snip = ev.get("snippet", "")
                    if "fallback" not in lbl and "[DEMO" not in snip:
                        unlabelled.append(snip[:40])
        results.append(check("fallback evidence clearly labelled [DEMO]/fallback", not unlabelled,
                             f"{len(unlabelled)} unlabelled items" if unlabelled else "all labelled"))
    else:
        results.append(check("fallback label check (no fallback messages)", True, "no fallback messages found"))

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
