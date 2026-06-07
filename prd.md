# PRD — AI Agent Debate System

## Project Title
**"Do Smartphones Make Us Less Smart?" — Multi-Agent AI Debate System**

---

## Assignment Goal
Build a CLI-based multi-agent system in which two AI agents debate a controversial topic while a third Judge agent moderates the debate, evaluates argument quality, and declares exactly one winner. The system demonstrates orchestration of AI agents, tool use, structured prompt engineering, and robust error handling.

---

## Problem Definition
Human debates are subjective and hard to automate fairly. This project explores whether LLM-based agents can sustain contradictory positions over multiple rounds, incorporate real external evidence through web search, and be evaluated objectively by a moderating agent — all without human intervention during execution.

---

## Debate Topic
**"Do smartphones make us less smart?"**

---

## Agent Roles

### Judge Agent (Father / Moderator)
- Controls the debate flow from start to finish.
- Issues the opening instructions and closing verdict.
- After every exchange, tracks argument quality, evidence usage, consistency, and relevance.
- After at least 10 exchanges, compiles the full transcript and declares **one winner only** (Pro or Con). Ties are strictly forbidden.
- Evaluation criteria: argument quality, factual evidence, logical consistency, relevance to the topic, rebuttal strength.

### Pro Agent
- **Position:** Yes, smartphones make us less smart.
- Must argue that smartphones reduce attention span, weaken memory, increase dependency on quick answers, distract from deep thinking, and reduce independent problem-solving.
- Must maintain this position consistently throughout all rounds.
- Must use external search to support claims with real statistics, studies, or reports.

### Con Agent
- **Position:** No, smartphones do not make us less smart.
- Must argue that smartphones increase access to knowledge, support learning, improve productivity, enhance communication, and extend human cognitive capabilities when used correctly.
- Must maintain this position consistently throughout all rounds.
- Must use external search to support claims with real evidence.

---

## Inputs

| Input | Source | Description |
|---|---|---|
| Debate topic | Config / CLI flag | The debate question posed to both agents |
| Pro position | System prompt | Fixed stance for the Pro agent |
| Con position | System prompt | Fixed stance for the Con agent |
| Round count | CLI flag (`--rounds`) | Minimum 10, configurable |
| ANTHROPIC_API_KEY | `.env` file | Key for Claude API calls |
| SERPER_API_KEY | `.env` file | Key for Google Search via Serper |

---

## Outputs

| Output | Location | Format |
|---|---|---|
| Debate transcript | `results/transcripts/` | JSON |
| Final verdict | `results/verdicts/` | Plain text + JSON |
| Search evidence log | `results/transcripts/` | Embedded in transcript JSON |
| Application log | `results/logs/` | Plain text (loguru) |
| Console output | stdout | Rich-formatted panels |

---

## Required Methods / Tools

| Tool/Method | Purpose |
|---|---|
| `anthropic.messages.create()` | Generate agent responses (Pro, Con, Judge) |
| `SerperSearchTool.search()` | Retrieve real-world evidence via Google Search |
| `tenacity.retry` | Automatic retry on API errors and timeouts |
| `loguru.logger` | Structured logging to file and console |
| `click` | CLI command parsing |
| `rich` | Formatted console output |
| `json` | Transcript serialization |

---

## Debate Rules

1. The Pro Agent speaks first in each exchange.
2. The Con Agent responds directly to the Pro Agent's most recent argument.
3. A minimum of **10 exchanges** (Pro → Con = 1 exchange) must occur before the Judge may issue a verdict.
4. Each agent **must** use search evidence in each round.
5. Agents must not drift from their assigned positions.
6. The Judge evaluates after every exchange and issues one final verdict after all exchanges are complete.
7. **No ties are permitted.** The Judge must name either "Pro" or "Con" as the winner.
8. The Judge may not participate in the argument exchanges — only in evaluation and verdict.

---

## Watchdog Requirement

- All API calls (Anthropic, Serper) must be wrapped in a retry decorator using `tenacity`.
- Retry on: `anthropic.APITimeoutError`, `anthropic.RateLimitError`, `requests.Timeout`, `requests.ConnectionError`.
- Maximum retries: 3, with exponential back-off starting at 2 seconds.
- A hard per-call timeout of 60 seconds must be enforced.
- A circuit breaker pattern must open after 5 consecutive failures and reset after 120 seconds.
- All retry events must be logged with attempt number, exception type, and wait time.

---

## External Search Requirement

- Use the **Serper API** (`https://google.serper.dev/search`) as the search backend.
- Both Pro and Con agents must query relevant keywords before each argument.
- Search results (snippets + source URLs) must be injected into the agent's context before it generates its argument.
- All search queries and results must be saved in the transcript JSON under `search_evidence`.
- The Judge must have access to the search evidence when evaluating arguments.

---

## Lecturer Constraints

| Constraint | Requirement |
|---|---|
| Environment manager | UV (`uv venv`, `uv pip install`) |
| Interface | CLI only — no web UI, no notebooks |
| Code organization | All Python inside `src/` |
| File size limit | No single `.py` file under `src/` may exceed 150 lines. If a file would exceed this limit, split it into smaller focused modules. Never remove functionality to reduce line count. |
| Minimum exchanges | At least 10 Pro↔Con exchanges before verdict |
| Winner | Exactly one winner — no ties |
| Results persistence | All outputs saved inside `results/` |
| Module structure | Each agent, tool, and concern in its own module |

---

## File Size Rule

Every Python file under `src/` must be **at most 150 lines** (blank lines and comments included in the count). This rule does not apply to `README.md`, `prd.md`, `plan.md`, or `todo.md`.

**Enforcement rules:**
- If any module would exceed 150 lines, split it into two or more focused submodules (e.g., `judge.py` → `judge_eval.py` + `judge_verdict.py`).
- You may create as many files as needed — there is no upper limit on the number of modules.
- Never remove functionality or comment out code solely to stay under 150 lines.

**Verification command (run before every commit):**
```bash
find src -name "*.py" -exec wc -l {} + | sort -n
```
Any file showing a line count above 150 must be split before committing.

---

## Evaluation Method

The Judge Agent will evaluate each exchange on four dimensions:

1. **Argument Quality (25%)** — Logical structure, coherence, depth.
2. **Factual Evidence (25%)** — Relevance and credibility of search results cited.
3. **Consistency (25%)** — Adherence to the assigned position across all rounds.
4. **Relevance & Rebuttal (25%)** — How directly the agent responds to the opponent's last point.

After all exchanges, the Judge sums its round-by-round assessments and names the agent with the stronger cumulative performance as the winner.

---

## Success Criteria

- [ ] Debate runs end-to-end without human intervention.
- [ ] Exactly 10 or more exchanges occur before the verdict.
- [ ] Both agents maintain their positions throughout.
- [ ] Search evidence is retrieved and embedded in every exchange.
- [ ] Watchdog handles at least one simulated API failure gracefully.
- [ ] A single winner (Pro or Con) is declared — no tie.
- [ ] Transcript, verdict, and logs are saved in `results/`.
- [ ] No Python file exceeds 150 lines.
- [ ] CLI commands run correctly from a fresh UV environment.

---

## Final Deliverables

1. `prd.md` — this document.
2. `plan.md` — modular architecture and execution plan.
3. `todo.md` — granular task checklist.
4. `README.md` — setup, run, and submission guide.
5. `requirements.txt` — all Python dependencies.
6. `.gitignore` — standard exclusions.
7. `src/` — all Python source modules.
8. `results/` — saved outputs from at least one successful run.
9. GitHub repository (public) with all the above committed.
