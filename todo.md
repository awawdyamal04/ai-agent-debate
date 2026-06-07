# TODO — AI Agent Debate System (Senior Architecture v2)

## Status Legend
- [x] Done
- [ ] Pending

---

## PHASE 1 — Documentation & Planning

- [x] Write prd.md
- [x] Write plan.md (updated for senior architecture v2)
- [x] Write todo.md (this file)
- [x] Write README.md with all required sections
- [x] Add Mermaid architecture diagram
- [x] Add Mermaid sequence diagram
- [x] Document JSON protocol
- [x] Document Skills vs Tools separation
- [x] Document Watchdog design
- [x] Document Gatekeeper design
- [x] Document external search setup + fallback mode
- [x] Document UV setup, CLI, and verification commands
- [x] Document GitHub commit/push workflow

---

## PHASE 2 — Project Scaffolding

- [x] Create pyproject.toml with project metadata and scripts entry point
- [x] Create .env.example with ANTHROPIC_API_KEY and SERPER_API_KEY
- [x] Create results/ directory for outputs
- [x] Create src/, src/agents/, src/tools/, src/debate/, src/config/, src/utils/, src/skills/
- [x] Create tests/ directory
- [x] Verify all __init__.py files present

---

## PHASE 3 — Configuration

- [x] src/config/settings.py — all constants, env loading, validate_config(), ConfigurationError
- [x] Verify settings.py ≤ 150 lines

---

## PHASE 4 — Skills (Agent Prompts)

- [x] src/skills/judge_skill.md — evaluation criteria, 6 dimensions, verdict format, no ties
- [x] src/skills/pro_skill.md — fixed PRO position, 5 argument themes, rebuttal instructions
- [x] src/skills/con_skill.md — fixed CON position, 5 argument themes, rebuttal instructions

---

## PHASE 5 — Dedicated Watchdog Module

- [x] src/watchdog.py — with_retry() decorator factory
- [x] Exponential back-off (2s → 4s → 8s)
- [x] Fallback value returned when all retries fail (debate never crashes)
- [x] CircuitBreaker class (opens at 5 failures, resets after 120s)
- [x] global_circuit_breaker singleton
- [x] Retry events tracked via gatekeeper.track_retry()
- [x] Recovery events tracked via gatekeeper.track_recovery()
- [x] Verify watchdog.py ≤ 150 lines

---

## PHASE 6 — Gatekeeper Module

- [x] src/gatekeeper.py — tracks rounds, exchanges, chars, searches, retries, recoveries
- [x] Gatekeeper.get_summary() → dict
- [x] Gatekeeper.save(path) → writes results/run_summary.json
- [x] Verify gatekeeper.py ≤ 150 lines

---

## PHASE 7 — JSON Communication Protocol

- [x] src/debate/protocol.py — DebateMessage dataclass
- [x] All required fields: round_number, exchange_number, speaker, stance, claim,
      evidence, tool_metadata, rebuttal_target, confidence_score, timestamp, status
- [x] EvidenceItem dataclass (snippet, url, source, label)
- [x] ToolMetadata dataclass (tools_used, search_queries, fallback_used)
- [x] to_dict(), to_json(), from_dict() methods
- [x] messages_to_text() helper for judge evaluation
- [x] Verify protocol.py ≤ 150 lines

---

## PHASE 8 — Tools

- [x] src/tools/search.py — SearchTool with Serper live mode + fallback demo evidence
- [x] Fallback evidence clearly labelled "[DEMO EVIDENCE]" and label="fallback/demo"
- [x] CircuitBreaker integration for Serper calls
- [x] format_for_agent() caps output at 2000 chars
- [x] src/tools/logging_tool.py — LoggingTool writes structured JSONL to results/events.jsonl
- [x] Events: debate_start, debate_message, judge_evaluation, verdict, error, debate_end
- [x] Verify all tool files ≤ 150 lines

---

## PHASE 9 — OOP Agent Hierarchy

- [x] src/agents/base.py — BaseAgent ABC with _load_skill(), _api_call(), respond()
- [x] src/agents/debater.py — DebaterAgent(BaseAgent) shared Pro/Con logic
  - [x] respond() returns DebateMessage dict
  - [x] _call_claude() with @with_retry and fallback
  - [x] search integration (evidence in every message)
- [x] src/agents/pro.py — ProAgent(DebaterAgent), stance=PRO, 10 rotating search queries
- [x] src/agents/con.py — ConAgent(DebaterAgent), stance=CON, 10 rotating search queries
- [x] src/agents/judge.py — JudgeAgent(BaseAgent), active orchestrator
  - [x] generate_opening() with @with_retry
  - [x] evaluate_exchange() with @with_retry
  - [x] declare_winner() — parses WINNER: Pro/Con, retries 3× before raising
  - [x] run_debate() — delegates to DebateRunner (keeps judge.py ≤ 150 lines)
- [x] Verify all agent files ≤ 150 lines
- [x] No code duplication between ProAgent and ConAgent

---

## PHASE 10 — Debate Runner

- [x] src/debate/runner.py — DebateRunner executes ping-pong loop
  - [x] Calls pro.respond() then con.respond() each round
  - [x] Calls judge.evaluate_exchange() after each round
  - [x] Verifies ≥ 10 Pro messages before verdict
  - [x] Calls judge.declare_winner()
  - [x] Saves transcript, evidence, verdict, run_summary
  - [x] Uses LoggingTool for JSONL events
  - [x] Uses Gatekeeper for tracking
- [x] src/debate/demo_runner.py — DemoRunner for no-API-key mode
- [x] Verify runner.py ≤ 150 lines

---

## PHASE 11 — Utilities

- [x] src/utils/logger.py — loguru setup with console + rotating file sink
- [x] src/utils/results.py — save_transcript, save_evidence, save_verdict, save_run_summary
- [x] Required output files: transcript.json, evidence.json, verdict.json,
      events.jsonl, run_summary.json, debate.log
- [x] Verify all utils ≤ 150 lines

---

## PHASE 12 — CLI and Entry Point

- [x] src/cli.py — click CLI with debate, show-config, check-health, show-transcript
- [x] --demo flag for API-key-free full run
- [x] --verbose flag for DEBUG logging
- [x] src/main.py — entry point for python -m src.main
- [x] Verify cli.py ≤ 150 lines

---

## PHASE 13 — Demo Data

- [x] src/agents/demo.py — 10 pre-written Pro args, 10 Con args, 10 judge evaluations,
      opening statement, full verdict with WINNER: Con
- [x] All demo content uses real academic references
- [x] Demo evidence clearly labelled [DEMO]
- [x] Verify demo.py ≤ 150 lines

---

## PHASE 14 — Verification and Testing

- [x] tests/verify.py — 12-point verification script
  - [x] transcript.json valid JSON
  - [x] ≥ 10 Pro messages
  - [x] ≥ 10 Con messages
  - [x] Pro stance = PRO throughout
  - [x] Con stance = CON throughout
  - [x] verdict.json has exactly one winner
  - [x] All 5 result files exist
  - [x] All src/ .py files ≤ 150 lines

---

## PHASE 15 — Integration Run

- [x] Install dependencies (pip3 / uv)
- [x] Run: python -m src.main debate --demo --rounds 10
- [x] Verify all result files generated
- [x] Run: python tests/verify.py → 12/12 PASS
- [x] Commit results/ as proof of execution

---

## PHASE 16 — Live Run (requires API keys)

- [ ] Add ANTHROPIC_API_KEY to .env
- [ ] Add SERPER_API_KEY to .env (optional)
- [ ] Run: python -m src.main check-health
- [ ] Run: python -m src.main debate --rounds 10
- [ ] Run: python tests/verify.py → 12/12 PASS
- [ ] Commit live results/

---

## PHASE 17 — GitHub Submission

- [ ] Stage all files: git add src/ tests/ results/ pyproject.toml .env.example plan.md README.md todo.md
- [ ] git commit -m "feat: senior architecture v2 — OOP agents, JSON protocol, watchdog, gatekeeper"
- [ ] git push origin main
- [ ] git tag v2.0.0 && git push origin --tags
- [ ] Create GitHub Release from v2.0.0
- [ ] Verify repository is public
- [ ] Submit repository URL to course portal
