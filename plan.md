# Plan — AI Agent Debate System

## Modular Architecture

```
ai-agent-debate/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── judge.py          # JudgeAgent class
│   │   ├── pro.py            # ProAgent class
│   │   └── con.py            # ConAgent class
│   ├── tools/
│   │   ├── __init__.py
│   │   └── search.py         # SerperSearchTool class
│   ├── debate/
│   │   ├── __init__.py
│   │   ├── orchestrator.py   # DebateOrchestrator class
│   │   └── transcript.py     # DebateTranscript dataclass + serialization
│   ├── watchdog/
│   │   ├── __init__.py
│   │   └── retry.py          # with_retry decorator, CircuitBreaker
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py         # loguru configuration
│   │   └── results.py        # file save/load helpers
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py       # constants, env var loading
│   │   └── prompts.py        # all system prompts
│   └── cli.py                # click CLI entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # shared fixtures
│   ├── test_search.py
│   ├── test_watchdog.py
│   ├── test_pro_agent.py
│   ├── test_con_agent.py
│   ├── test_judge.py
│   ├── test_orchestrator.py
│   └── test_cli.py
├── results/
│   ├── transcripts/          # debate_<timestamp>.json
│   ├── verdicts/             # verdict_<timestamp>.txt
│   └── logs/                 # debate_<timestamp>.log
├── prd.md
├── plan.md
├── todo.md
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
└── .gitignore
```

---

## File Size Rule

Every Python file under `src/` must be **at most 150 lines**. This limit does not apply to documentation files (`README.md`, `prd.md`, `plan.md`, `todo.md`).

| Rule | Detail |
|---|---|
| Scope | All `.py` files under `src/` |
| Hard limit | 150 lines (blank lines and comments count) |
| When exceeded | Split the file into two or more focused submodules |
| Functionality | Never remove or stub out code just to hit the limit |
| Extra modules | Unlimited — create as many files as the design requires |

**Verification command:**
```bash
find src -name "*.py" -exec wc -l {} + | sort -n
```
Run this before every commit. Any result above 150 must be split before the commit proceeds.

**Example splits that may be needed:**
- `orchestrator.py` → `orchestrator.py` + `display.py` (if Rich printing inflates line count)
- `judge.py` → `judge_eval.py` + `judge_verdict.py` (if evaluation + verdict logic is too large)
- `cli.py` → `cli.py` + `cli_display.py` (if command handlers grow large)

---

## File and Folder Structure — Module Explanations

### `src/config/settings.py`
Loads `.env` via `python-dotenv`. Exposes typed constants: `ANTHROPIC_API_KEY`, `SERPER_API_KEY`, `MODEL_NAME`, `MIN_EXCHANGES`, `MAX_RETRIES`, `RETRY_DELAY`, `TIMEOUT_SECONDS`, `DEBATE_TOPIC`, `RESULTS_DIR`, etc. Raises `ConfigurationError` if required keys are missing.

### `src/config/prompts.py`
Contains all three system prompts as module-level string constants. No logic — pure data. Prompts define each agent's persona, position, constraints, and output format.

### `src/tools/search.py`
`SerperSearchTool` class. Single public method `search(query: str) -> list[SearchResult]`. Uses `requests.get` to call the Serper API. Returns a list of `SearchResult` dataclasses (query, snippet, url, source). A `format_for_agent(results)` helper converts results to a readable block of text for injection into agent context.

### `src/watchdog/retry.py`
`with_retry(max_attempts, wait_min, wait_max)` — a `tenacity`-based decorator factory. Retries on `anthropic.APITimeoutError`, `anthropic.RateLimitError`, `requests.Timeout`, `requests.ConnectionError`. Logs every retry event. `CircuitBreaker` class opens after N consecutive failures and resets after a cooldown period.

### `src/utils/logger.py`
Configures `loguru` with two sinks: rotating file sink in `results/logs/` and a console sink. Returns a `get_logger(name)` helper. Log format: `{time} | {level} | {name} | {message}`.

### `src/utils/results.py`
Functions: `save_transcript(transcript: DebateTranscript) -> Path`, `save_verdict(winner, text) -> Path`, `load_transcript(path) -> DebateTranscript`. All file I/O with `pathlib.Path`. Filenames use `datetime.now().strftime("%Y%m%d_%H%M%S")`.

### `src/debate/transcript.py`
`DebateTranscript` dataclass: `topic`, `timestamp`, `exchanges: list[Exchange]`, `search_evidence: dict`, `judge_notes: list[str]`, `winner`, `verdict_text`. `Exchange` dataclass: `round_number`, `pro_argument`, `con_argument`. Both are JSON-serializable via `dataclasses.asdict`.

### `src/agents/pro.py`
`ProAgent` class. Wraps the Anthropic client. Keeps a `conversation_history` list for multi-turn context. `generate_argument(round_num, last_con_arg, evidence)` builds a user message, calls `messages.create()` with the Pro system prompt, appends the response to history, and returns the argument text. The API call is wrapped with `with_retry`.

### `src/agents/con.py`
Mirror of `pro.py` but with `CON_SYSTEM_PROMPT` and the opposing position. Same interface: `generate_argument(round_num, last_pro_arg, evidence)`.

### `src/agents/judge.py`
`JudgeAgent` class. Methods: `evaluate_exchange(pro_arg, con_arg, evidence) -> str` (returns evaluation notes), `compile_transcript(exchanges) -> str` (formats all rounds as text), `declare_winner(transcript, notes) -> tuple[str, str]` (returns `(winner, verdict_text)`). Winner is strictly `"Pro"` or `"Con"`. If the model output is ambiguous, a `ValueError` is raised and the call retried.

### `src/debate/orchestrator.py`
`DebateOrchestrator` class. `run_debate()` method orchestrates the full flow: opening → 10+ exchange loop → closing → judge verdict → save results. Returns a `DebateResult` dict. Uses `rich.console.Console` for pretty printing. Delegates all agent calls and file saves to the relevant modules.

### `src/cli.py`
`click` group with subcommands:
- `debate` — runs the full debate (options: `--topic`, `--rounds`, `--verbose`, `--output-dir`).
- `show-config` — prints loaded configuration.
- `check-health` — pings the Anthropic API.
- `show-transcript` — loads and displays a saved transcript.

---

## Data Flow

```
User (CLI)
    │
    ▼
DebateOrchestrator.run_debate()
    │
    ├─► Judge: issue opening instructions
    │
    ├─► [Loop × MIN_EXCHANGES]
    │       │
    │       ├─► SearchTool.search(pro_query)  ──► Serper API
    │       ├─► ProAgent.generate_argument()  ──► Anthropic API
    │       │
    │       ├─► SearchTool.search(con_query)  ──► Serper API
    │       ├─► ConAgent.generate_argument()  ──► Anthropic API
    │       │
    │       └─► JudgeAgent.evaluate_exchange()
    │
    ├─► JudgeAgent.declare_winner()           ──► Anthropic API
    │
    └─► ResultsSaver: transcript, verdict, logs ──► results/
```

---

## Execution Flow

1. `uv run python -m src.cli debate` (or `debate-agents debate`)
2. `cli.py` validates env vars, instantiates `DebateOrchestrator`.
3. Orchestrator initializes Pro, Con, and Judge agents.
4. Judge agent generates an opening statement (round 0).
5. For rounds 1–10 (minimum):
   a. Pro agent queries Serper for evidence.
   b. Pro agent generates argument using evidence + prior Con argument.
   c. Con agent queries Serper for evidence.
   d. Con agent generates argument using evidence + prior Pro argument.
   e. Judge evaluates exchange and stores notes.
   f. Rich console prints both arguments in colored panels.
6. After 10 rounds, Judge compiles full transcript + notes.
7. Judge calls `declare_winner()` — returns one of `"Pro"` or `"Con"`.
8. Results saved to `results/`.
9. Console prints winner announcement and file paths.

---

## Search Tool Integration Strategy

- **Provider:** Serper.dev (`POST https://google.serper.dev/search`)
- **Auth:** `X-API-KEY` header from `SERPER_API_KEY` env var.
- **Query construction:** Each agent crafts a 3–8 word search query relevant to its current argument point.
- **Result injection:** Top 3 organic results (snippet + URL) are formatted and prepended to the agent's user message.
- **Evidence storage:** Each exchange's search queries and results are stored in `transcript.search_evidence[round]`.
- **Fallback:** If Serper fails after retries, agents proceed without external evidence and log a warning.

---

## Watchdog / Retry Strategy

| Scenario | Response |
|---|---|
| `anthropic.APITimeoutError` | Retry up to 3×, exponential back-off (2s, 4s, 8s) |
| `anthropic.RateLimitError` | Retry up to 3×, wait 10s flat |
| `requests.Timeout` (Serper) | Retry up to 3×, exponential back-off |
| `requests.ConnectionError` | Retry up to 3×, exponential back-off |
| 5 consecutive failures | Circuit breaker opens; pause 120s then reset |
| Ambiguous judge winner | Re-call `declare_winner()` up to 2 extra times |
| All retries exhausted | Log critical error, save partial transcript, exit cleanly |

All retry logic lives in `src/watchdog/retry.py`. Wrapped via the `@with_retry(...)` decorator applied at the call site.

---

## Logging / Result-Saving Strategy

- **Logger:** `loguru` with two sinks — file (`results/logs/debate_<ts>.log`) and console (INFO level, short format).
- **Log levels:**
  - DEBUG: individual API payloads, search raw results.
  - INFO: round start/end, argument lengths, winner declaration.
  - WARNING: retry events, missing evidence.
  - ERROR/CRITICAL: exhausted retries, unexpected exceptions.
- **Transcript JSON schema:**
  ```json
  {
    "topic": "...",
    "timestamp": "ISO-8601",
    "exchanges": [
      {
        "round": 1,
        "pro_argument": "...",
        "con_argument": "...",
        "pro_search_queries": [...],
        "con_search_queries": [...],
        "search_evidence": {...},
        "judge_notes": "..."
      }
    ],
    "winner": "Pro|Con",
    "verdict_text": "..."
  }
  ```
- **Verdict file:** plain text, human-readable summary of the judge's decision and reasoning.

---

## Testing Strategy

| Test Type | Tool | Coverage Target |
|---|---|---|
| Unit tests | `pytest` + `unittest.mock` | Each class and method in isolation |
| Integration tests | `pytest` (marked `@pytest.mark.integration`) | Full debate run against real APIs |
| CLI tests | `click.testing.CliRunner` | All CLI subcommands |
| Retry tests | Mocked exceptions | All retry/watchdog paths |

Key test scenarios:
- Pro agent generates argument that contains pro keywords.
- Con agent generates argument that contains con keywords.
- Debate completes 10+ exchanges without crashing.
- Judge declares exactly one winner.
- Transcript JSON is valid and complete.
- Retry decorator triggers on simulated `APITimeoutError`.
- Circuit breaker opens after 5 failures.
- Search tool parses Serper response correctly.

---

## CLI Commands

```bash
# Setup
uv venv .venv
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate            # Windows
uv pip install -r requirements.txt

# Copy and fill env vars
cp .env.example .env

# Run full debate (default 10 rounds)
python -m src.cli debate

# Run with custom rounds
python -m src.cli debate --rounds 12

# Check API health
python -m src.cli check-health

# Show loaded config
python -m src.cli show-config

# Show a saved transcript
python -m src.cli show-transcript results/transcripts/debate_<timestamp>.json

# Run tests
pytest tests/
pytest tests/ -m integration      # integration tests only
pytest tests/ -v --tb=short       # verbose
```

---

## GitHub Submission Plan

1. Create a public GitHub repository named `ai-agent-debate`.
2. Commit documentation files first (prd, plan, todo, README, requirements, .gitignore).
3. Commit source files in logical groups: config → tools → watchdog → agents → debate → cli → tests.
4. Add a `.env.example` (never commit `.env`).
5. Run the debate at least once; commit the `results/` output as proof of execution.
6. Tag the final commit: `git tag v1.0.0 && git push origin v1.0.0`.
7. Create a GitHub Release from the tag with a brief description.
8. Submit the repository URL.
