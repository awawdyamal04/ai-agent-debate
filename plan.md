# Plan — AI Agent Debate System (Senior Architecture v2)

## Architecture Overview

```
ai-agent-debate/
├── src/
│   ├── main.py                   # Entry: python -m src.main
│   ├── cli.py                    # click CLI (debate, show-config, check-health, show-transcript)
│   ├── watchdog.py               # Dedicated watchdog: retry + circuit breaker
│   ├── gatekeeper.py             # Context/cost tracker
│   ├── skills/                   # Agent skills (WHAT each agent thinks — markdown)
│   │   ├── judge_skill.md
│   │   ├── pro_skill.md
│   │   └── con_skill.md
│   ├── agents/
│   │   ├── base.py               # BaseAgent ABC
│   │   ├── debater.py            # DebaterAgent(BaseAgent) — shared Pro/Con logic
│   │   ├── pro.py                # ProAgent(DebaterAgent)
│   │   ├── con.py                # ConAgent(DebaterAgent)
│   │   ├── judge.py              # JudgeAgent(BaseAgent) — active orchestrator
│   │   └── demo.py               # Pre-written args for demo/no-key mode
│   ├── tools/                    # Tools (WHAT agents can do)
│   │   ├── search.py             # SearchTool: Serper API + fallback demo evidence
│   │   └── logging_tool.py       # LoggingTool: structured JSONL event log
│   ├── debate/
│   │   ├── protocol.py           # DebateMessage JSON schema (all required fields)
│   │   ├── runner.py             # DebateRunner: ping-pong loop delegated by Judge
│   │   └── demo_runner.py        # DemoRunner: no-API full run
│   ├── config/
│   │   └── settings.py           # Env vars, constants, validate_config()
│   └── utils/
│       ├── logger.py             # Loguru setup
│       └── results.py            # Save transcript/evidence/verdict/summary
├── tests/
│   └── verify.py                 # 12-point verification script
├── results/                      # All outputs (committed as proof of execution)
│   ├── transcript.json
│   ├── evidence.json
│   ├── verdict.json
│   ├── run_summary.json
│   ├── events.jsonl
│   └── debate.log
├── pyproject.toml
├── .env.example
└── requirements.txt
```

---

## File Size Rule

Every Python file under `src/` must be **at most 150 lines**.

| Rule | Detail |
|---|---|
| Scope | All `.py` files under `src/` |
| Hard limit | 150 lines (blank + comments count) |
| When exceeded | Split into focused submodules |
| Verification | `find src -name "*.py" \| xargs wc -l \| sort -n` |

---

## Skills vs Tools Separation

| Concept | Location | Purpose |
|---|---|---|
| **Skill** | `src/skills/*.md` | Defines HOW the agent thinks — system prompt, persona, position, evaluation criteria |
| **Tool** | `src/tools/*.py` | Defines WHAT the agent can do — search, log events, track state |

Agents load skills at init time via `BaseAgent._load_skill()`.
Agents call tools explicitly within their `respond()` method.

---

## OOP Agent Hierarchy

```
BaseAgent (ABC)          src/agents/base.py
  ├── DebaterAgent       src/agents/debater.py   (shared Pro/Con logic)
  │     ├── ProAgent     src/agents/pro.py
  │     └── ConAgent     src/agents/con.py
  └── JudgeAgent         src/agents/judge.py     (active orchestrator)
```

All agents expose `respond(context: dict) -> dict` returning a `DebateMessage`-compatible dict.

---

## Structured JSON Communication Protocol

Every debate message is a `DebateMessage` dataclass (`src/debate/protocol.py`) with:

```json
{
  "round_number": 1,
  "exchange_number": 1,
  "speaker": "Pro",
  "stance": "PRO",
  "claim": "...",
  "evidence": [{"snippet": "...", "url": "...", "source": "serper", "label": "live"}],
  "tool_metadata": {
    "tools_used": ["search", "anthropic"],
    "search_queries": ["..."],
    "search_results_count": 3,
    "fallback_used": false
  },
  "rebuttal_target": "opponent's prior claim (first 120 chars)",
  "confidence_score": 0.85,
  "timestamp": "ISO-8601",
  "status": "complete"
}
```

---

## Judge as Active Orchestrator

`JudgeAgent.run_debate(pro, con, num_rounds)` is the debate entry point.
It delegates the exchange loop to `DebateRunner` (keeping judge.py under 150 lines),
which calls `judge.evaluate_exchange()` after every round and
`judge.declare_winner()` after all rounds.

Judge evaluation criteria:
1. Factual Evidence Quality
2. Relevance
3. Consistency
4. Rebuttal Strength
5. Use of External Sources
6. Logical Clarity

No tie is allowed. Winner is parsed from `WINNER: Pro` or `WINNER: Con` line.

---

## Watchdog Design (`src/watchdog.py`)

- `with_retry(max_attempts, wait_min, wait_max, fallback)` — decorator factory
- Exponential back-off: 2s → 4s → 8s
- `fallback` value returned if all retries fail (never crashes whole debate)
- `CircuitBreaker` — opens after 5 failures, resets after 120s
- `global_circuit_breaker` — shared instance protecting Serper calls

---

## Gatekeeper Design (`src/gatekeeper.py`)

Tracks per-run: rounds, exchanges, characters used (~tokens/4), search calls,
retries, failures recovered. Saved to `results/run_summary.json`.

---

## Required Result Files

| File | Contents |
|---|---|
| `results/transcript.json` | All DebateMessage objects (Pro + Con × 10+) |
| `results/evidence.json` | Evidence by round (Pro + Con evidence items) |
| `results/verdict.json` | Winner + full verdict text |
| `results/events.jsonl` | JSONL event log (one event per line) |
| `results/run_summary.json` | Gatekeeper stats |
| `results/debate.log` | Loguru rotating file log |

---

## Search / Fallback Strategy

- **Live mode** (SERPER_API_KEY set): calls `https://google.serper.dev/search`
- **Fallback mode** (no key): uses pre-defined demo evidence labelled `[DEMO]`
- Evidence always embedded in every DebateMessage's `evidence` list

---

## CLI Commands

```bash
# Demo run (no API key needed)
python -m src.main debate --demo

# Live run (requires ANTHROPIC_API_KEY in .env)
python -m src.main debate

# Custom rounds
python -m src.main debate --rounds 12

# Show config
python -m src.main show-config

# Health check
python -m src.main check-health

# Show saved transcript
python -m src.main show-transcript

# Verification
python tests/verify.py

# Line count check
find src -name "*.py" | xargs wc -l | sort -n
```
