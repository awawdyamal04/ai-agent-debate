# TODO — AI Agent Debate System
## Highly Granular Task Checklist (565 tasks)

> Instructions for AI coding agent: complete tasks in order. Mark each `[x]` immediately upon completion. Never skip a task. Never modify more than one module at a time without verifying the previous module first.

---

## PHASE 1 — Project Scaffolding (Tasks 1–45)

### 1.1 Repository & Environment
- [ ] 1. Verify git is initialized in the project root (`git status`)
- [ ] 2. Verify current branch is `main`
- [ ] 3. Check that UV is installed (`uv --version`)
- [ ] 4. Run `uv venv .venv` to create the virtual environment
- [ ] 5. Activate the virtual environment (`source .venv/bin/activate`)
- [ ] 6. Verify Python version inside venv is ≥ 3.11
- [ ] 7. Create `pyproject.toml` with project metadata
- [ ] 8. Set `name = "ai-agent-debate"` in pyproject.toml
- [ ] 9. Set `version = "1.0.0"` in pyproject.toml
- [ ] 10. Set `requires-python = ">=3.11"` in pyproject.toml
- [ ] 11. Add `[project.scripts]` entry: `debate-agents = "src.cli:main"`
- [ ] 12. Run `uv pip install -r requirements.txt`
- [ ] 13. Verify `anthropic` package is installed (`python -c "import anthropic"`)
- [ ] 14. Verify `click` package is installed
- [ ] 15. Verify `rich` package is installed
- [ ] 16. Verify `tenacity` package is installed
- [ ] 17. Verify `loguru` package is installed
- [ ] 18. Verify `requests` package is installed

### 1.2 Directory Structure
- [ ] 19. Create `src/` directory
- [ ] 20. Create `src/__init__.py` (empty)
- [ ] 21. Create `src/agents/` directory
- [ ] 22. Create `src/agents/__init__.py` (empty)
- [ ] 23. Create `src/tools/` directory
- [ ] 24. Create `src/tools/__init__.py` (empty)
- [ ] 25. Create `src/debate/` directory
- [ ] 26. Create `src/debate/__init__.py` (empty)
- [ ] 27. Create `src/watchdog/` directory
- [ ] 28. Create `src/watchdog/__init__.py` (empty)
- [ ] 29. Create `src/utils/` directory
- [ ] 30. Create `src/utils/__init__.py` (empty)
- [ ] 31. Create `src/config/` directory
- [ ] 32. Create `src/config/__init__.py` (empty)
- [ ] 33. Create `tests/` directory
- [ ] 34. Create `tests/__init__.py` (empty)
- [ ] 35. Create `results/` directory
- [ ] 36. Create `results/transcripts/` directory
- [ ] 37. Create `results/verdicts/` directory
- [ ] 38. Create `results/logs/` directory
- [ ] 39. Create `results/transcripts/.gitkeep`
- [ ] 40. Create `results/verdicts/.gitkeep`
- [ ] 41. Create `results/logs/.gitkeep`
- [ ] 42. Create `.env.example` file
- [ ] 43. Add `ANTHROPIC_API_KEY=your_key_here` to `.env.example`
- [ ] 44. Add `SERPER_API_KEY=your_key_here` to `.env.example`
- [ ] 45. Verify `.env` is listed in `.gitignore`

---

## PHASE 2 — Configuration Module (Tasks 46–90)

### 2.1 `src/config/settings.py`
- [ ] 46. Create `src/config/settings.py`
- [ ] 47. Add import: `import os`
- [ ] 48. Add import: `from pathlib import Path`
- [ ] 49. Add import: `from dotenv import load_dotenv`
- [ ] 50. Call `load_dotenv()` at module level
- [ ] 51. Define `BASE_DIR = Path(__file__).resolve().parent.parent.parent`
- [ ] 52. Define `RESULTS_DIR = BASE_DIR / "results"`
- [ ] 53. Define `TRANSCRIPTS_DIR = RESULTS_DIR / "transcripts"`
- [ ] 54. Define `VERDICTS_DIR = RESULTS_DIR / "verdicts"`
- [ ] 55. Define `LOGS_DIR = RESULTS_DIR / "logs"`
- [ ] 56. Define `ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")`
- [ ] 57. Define `SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")`
- [ ] 58. Define `MODEL_NAME = "claude-sonnet-4-6"`
- [ ] 59. Define `MIN_EXCHANGES = 10`
- [ ] 60. Define `MAX_TOKENS_AGENT = 1024`
- [ ] 61. Define `MAX_TOKENS_JUDGE = 2048`
- [ ] 62. Define `MAX_RETRIES = 3`
- [ ] 63. Define `RETRY_WAIT_MIN = 2` (seconds)
- [ ] 64. Define `RETRY_WAIT_MAX = 8` (seconds)
- [ ] 65. Define `API_TIMEOUT = 60` (seconds)
- [ ] 66. Define `CIRCUIT_BREAKER_THRESHOLD = 5`
- [ ] 67. Define `CIRCUIT_BREAKER_RESET = 120` (seconds)
- [ ] 68. Define `SERPER_URL = "https://google.serper.dev/search"`
- [ ] 69. Define `SERPER_RESULTS_COUNT = 3`
- [ ] 70. Define `DEBATE_TOPIC = "Do smartphones make us less smart?"`
- [ ] 71. Define `PRO_POSITION = "Yes, smartphones make us less smart."`
- [ ] 72. Define `CON_POSITION = "No, smartphones do not make us less smart."`
- [ ] 73. Define `ConfigurationError` exception class
- [ ] 74. Define `validate_config()` function
- [ ] 75. In `validate_config()`: raise `ConfigurationError` if `ANTHROPIC_API_KEY` is empty
- [ ] 76. In `validate_config()`: raise `ConfigurationError` if `SERPER_API_KEY` is empty
- [ ] 77. In `validate_config()`: log warning (not error) if Serper key missing — fallback to no-search mode
- [ ] 78. Verify `settings.py` does not exceed 150 lines
- [ ] 79. Manually import `settings` and print `MODEL_NAME` to verify it works

### 2.2 `src/config/prompts.py`
- [ ] 80. Create `src/config/prompts.py`
- [ ] 81. Define `JUDGE_SYSTEM_PROMPT` as a multi-line string
- [ ] 82. In `JUDGE_SYSTEM_PROMPT`: state the agent is the debate moderator and judge
- [ ] 83. In `JUDGE_SYSTEM_PROMPT`: state it must NOT argue — only evaluate and decide
- [ ] 84. In `JUDGE_SYSTEM_PROMPT`: list evaluation criteria (quality, evidence, consistency, relevance)
- [ ] 85. In `JUDGE_SYSTEM_PROMPT`: state that after all rounds it must declare exactly one winner
- [ ] 86. In `JUDGE_SYSTEM_PROMPT`: state ties are strictly forbidden
- [ ] 87. In `JUDGE_SYSTEM_PROMPT`: specify output format for verdict (winner name + reasoning)
- [ ] 88. Define `PRO_SYSTEM_PROMPT` as a multi-line string
- [ ] 89. In `PRO_SYSTEM_PROMPT`: state fixed position — "Yes, smartphones make us less smart"
- [ ] 90. In `PRO_SYSTEM_PROMPT`: list required argument themes (attention span, memory, dependency, distraction, problem-solving)
- [ ] 91. In `PRO_SYSTEM_PROMPT`: instruct agent to use provided search evidence
- [ ] 92. In `PRO_SYSTEM_PROMPT`: instruct agent to directly rebut the Con agent's last argument
- [ ] 93. In `PRO_SYSTEM_PROMPT`: warn agent it must never agree with the Con position
- [ ] 94. Define `CON_SYSTEM_PROMPT` as a multi-line string
- [ ] 95. In `CON_SYSTEM_PROMPT`: state fixed position — "No, smartphones do not make us less smart"
- [ ] 96. In `CON_SYSTEM_PROMPT`: list required argument themes (knowledge access, learning, productivity, communication, cognitive extension)
- [ ] 97. In `CON_SYSTEM_PROMPT`: instruct agent to use provided search evidence
- [ ] 98. In `CON_SYSTEM_PROMPT`: instruct agent to directly rebut the Pro agent's last argument
- [ ] 99. In `CON_SYSTEM_PROMPT`: warn agent it must never agree with the Pro position
- [ ] 100. Verify `prompts.py` does not exceed 150 lines

---

## PHASE 3 — Watchdog / Retry Module (Tasks 101–135)

### 3.1 `src/watchdog/retry.py`
- [ ] 101. Create `src/watchdog/retry.py`
- [ ] 102. Add import: `import time`
- [ ] 103. Add import: `import threading`
- [ ] 104. Add import: `from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log`
- [ ] 105. Add import: `from loguru import logger`
- [ ] 106. Add import: `import requests`
- [ ] 107. Add import: `import anthropic`
- [ ] 108. Add import: `from src.config import settings`
- [ ] 109. Define `RETRYABLE_EXCEPTIONS` tuple: `(anthropic.APITimeoutError, anthropic.RateLimitError, requests.Timeout, requests.ConnectionError, TimeoutError)`
- [ ] 110. Define `with_retry` as a function returning a `tenacity.retry` decorator
- [ ] 111. In `with_retry`: accept `max_attempts` param (default `settings.MAX_RETRIES`)
- [ ] 112. In `with_retry`: accept `wait_min` param (default `settings.RETRY_WAIT_MIN`)
- [ ] 113. In `with_retry`: accept `wait_max` param (default `settings.RETRY_WAIT_MAX`)
- [ ] 114. In `with_retry`: configure `stop_after_attempt(max_attempts)`
- [ ] 115. In `with_retry`: configure `wait_exponential(multiplier=1, min=wait_min, max=wait_max)`
- [ ] 116. In `with_retry`: configure `retry_if_exception_type(RETRYABLE_EXCEPTIONS)`
- [ ] 117. In `with_retry`: add `before_sleep` callback that logs attempt number and exception
- [ ] 118. Define `CircuitBreaker` class
- [ ] 119. In `CircuitBreaker.__init__`: accept `threshold` (default `settings.CIRCUIT_BREAKER_THRESHOLD`)
- [ ] 120. In `CircuitBreaker.__init__`: accept `reset_timeout` (default `settings.CIRCUIT_BREAKER_RESET`)
- [ ] 121. In `CircuitBreaker.__init__`: initialize `failure_count = 0`
- [ ] 122. In `CircuitBreaker.__init__`: initialize `is_open = False`
- [ ] 123. In `CircuitBreaker.__init__`: initialize `opened_at = None`
- [ ] 124. Define `CircuitBreaker.record_failure()` method
- [ ] 125. In `record_failure`: increment `failure_count`
- [ ] 126. In `record_failure`: if `failure_count >= threshold`, set `is_open = True` and `opened_at = time.time()`
- [ ] 127. In `record_failure`: log warning when circuit opens
- [ ] 128. Define `CircuitBreaker.record_success()` method
- [ ] 129. In `record_success`: reset `failure_count = 0`
- [ ] 130. Define `CircuitBreaker.allow_request()` method
- [ ] 131. In `allow_request`: if `is_open` and elapsed > `reset_timeout`, reset and return True
- [ ] 132. In `allow_request`: if `is_open` and not reset, log blocked call and return False
- [ ] 133. In `allow_request`: if not open, return True
- [ ] 134. Define `global_circuit_breaker = CircuitBreaker()` at module level
- [ ] 135. Verify `retry.py` does not exceed 150 lines

---

## PHASE 4 — Logger & Results Utilities (Tasks 136–175)

### 4.1 `src/utils/logger.py`
- [ ] 136. Create `src/utils/logger.py`
- [ ] 137. Add import: `import sys`
- [ ] 138. Add import: `from pathlib import Path`
- [ ] 139. Add import: `from loguru import logger`
- [ ] 140. Add import: `from src.config import settings`
- [ ] 141. Define `setup_logger(log_file: Path | None = None)` function
- [ ] 142. In `setup_logger`: remove default loguru handler (`logger.remove()`)
- [ ] 143. In `setup_logger`: add console sink — `logger.add(sys.stderr, level="INFO", format=...)`
- [ ] 144. Console format: `"{time:HH:mm:ss} | {level:<8} | {message}"`
- [ ] 145. In `setup_logger`: if `log_file` is not None, add file sink
- [ ] 146. File sink format: `"{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name} | {message}"`
- [ ] 147. File sink: set `rotation="10 MB"`, `retention="7 days"`
- [ ] 148. Return configured `logger` instance
- [ ] 149. Define `get_logger()` returning `logger` (for import convenience)
- [ ] 150. Verify `logger.py` does not exceed 150 lines

### 4.2 `src/utils/results.py`
- [ ] 151. Create `src/utils/results.py`
- [ ] 152. Add import: `import json`
- [ ] 153. Add import: `from datetime import datetime`
- [ ] 154. Add import: `from pathlib import Path`
- [ ] 155. Add import: `from dataclasses import asdict`
- [ ] 156. Add import: `from src.config import settings`
- [ ] 157. Define `generate_timestamp()` returning `datetime.now().strftime("%Y%m%d_%H%M%S")`
- [ ] 158. Define `save_transcript(transcript_dict: dict) -> Path` function
- [ ] 159. In `save_transcript`: generate filename `debate_<timestamp>.json`
- [ ] 160. In `save_transcript`: ensure `TRANSCRIPTS_DIR` exists (`mkdir(parents=True, exist_ok=True)`)
- [ ] 161. In `save_transcript`: write JSON with `indent=2`
- [ ] 162. In `save_transcript`: return the file path
- [ ] 163. Define `save_verdict(winner: str, verdict_text: str) -> Path` function
- [ ] 164. In `save_verdict`: generate filename `verdict_<timestamp>.txt`
- [ ] 165. In `save_verdict`: ensure `VERDICTS_DIR` exists
- [ ] 166. In `save_verdict`: write plain text verdict file
- [ ] 167. In `save_verdict`: return the file path
- [ ] 168. Define `load_transcript(path: Path) -> dict` function
- [ ] 169. In `load_transcript`: open file and parse JSON
- [ ] 170. In `load_transcript`: return dict
- [ ] 171. Define `list_transcripts() -> list[Path]` function
- [ ] 172. In `list_transcripts`: glob `TRANSCRIPTS_DIR` for `*.json` files
- [ ] 173. In `list_transcripts`: return sorted list (newest first)
- [ ] 174. Verify `results.py` does not exceed 150 lines
- [ ] 175. Import and test `save_transcript` with a sample dict

---

## PHASE 5 — Debate Transcript Dataclasses (Tasks 176–195)

### 5.1 `src/debate/transcript.py`
- [ ] 176. Create `src/debate/transcript.py`
- [ ] 177. Add import: `from dataclasses import dataclass, field`
- [ ] 178. Add import: `from typing import Optional`
- [ ] 179. Define `SearchEvidence` dataclass
- [ ] 180. In `SearchEvidence`: add `query: str` field
- [ ] 181. In `SearchEvidence`: add `snippets: list[str]` field (default_factory=list)
- [ ] 182. In `SearchEvidence`: add `urls: list[str]` field (default_factory=list)
- [ ] 183. Define `Exchange` dataclass
- [ ] 184. In `Exchange`: add `round_number: int` field
- [ ] 185. In `Exchange`: add `pro_argument: str` field
- [ ] 186. In `Exchange`: add `con_argument: str` field
- [ ] 187. In `Exchange`: add `pro_evidence: list[SearchEvidence]` field (default_factory=list)
- [ ] 188. In `Exchange`: add `con_evidence: list[SearchEvidence]` field (default_factory=list)
- [ ] 189. In `Exchange`: add `judge_notes: str` field (default="")
- [ ] 190. Define `DebateTranscript` dataclass
- [ ] 191. In `DebateTranscript`: add `topic: str` field
- [ ] 192. In `DebateTranscript`: add `timestamp: str` field
- [ ] 193. In `DebateTranscript`: add `exchanges: list[Exchange]` field (default_factory=list)
- [ ] 194. In `DebateTranscript`: add `winner: Optional[str]` field (default=None)
- [ ] 195. In `DebateTranscript`: add `verdict_text: str` field (default="")
- [ ] 196. Define `transcript_to_dict(transcript: DebateTranscript) -> dict` using `dataclasses.asdict`
- [ ] 197. Verify `transcript.py` does not exceed 150 lines

---

## PHASE 6 — Search Tool (Tasks 198–230)

### 6.1 `src/tools/search.py`
- [ ] 198. Create `src/tools/search.py`
- [ ] 199. Add import: `import requests`
- [ ] 200. Add import: `from loguru import logger`
- [ ] 201. Add import: `from src.config import settings`
- [ ] 202. Add import: `from src.debate.transcript import SearchEvidence`
- [ ] 203. Add import: `from src.watchdog.retry import with_retry, global_circuit_breaker`
- [ ] 204. Define `SerperSearchTool` class
- [ ] 205. In `__init__`: store `self.api_key = settings.SERPER_API_KEY`
- [ ] 206. In `__init__`: store `self.url = settings.SERPER_URL`
- [ ] 207. In `__init__`: store `self.num_results = settings.SERPER_RESULTS_COUNT`
- [ ] 208. Define `_call_api(self, query: str) -> dict` private method
- [ ] 209. In `_call_api`: build headers `{"X-API-KEY": self.api_key, "Content-Type": "application/json"}`
- [ ] 210. In `_call_api`: build payload `{"q": query, "num": self.num_results}`
- [ ] 211. In `_call_api`: call `requests.post(self.url, headers=headers, json=payload, timeout=settings.API_TIMEOUT)`
- [ ] 212. In `_call_api`: raise `requests.HTTPError` if status not 200
- [ ] 213. In `_call_api`: return `response.json()`
- [ ] 214. Wrap `_call_api` with `@with_retry()` decorator
- [ ] 215. Define `search(self, query: str) -> list[SearchEvidence]` method
- [ ] 216. In `search`: check `global_circuit_breaker.allow_request()` — if False, return empty list with log warning
- [ ] 217. In `search`: log the query string at INFO level
- [ ] 218. In `search`: call `self._call_api(query)` inside try/except
- [ ] 219. In `search`: on success, call `global_circuit_breaker.record_success()`
- [ ] 220. In `search`: on exception, call `global_circuit_breaker.record_failure()`, log error, return empty list
- [ ] 221. In `search`: parse `raw["organic"]` list from response
- [ ] 222. In `search`: for each result extract `snippet` (or `""`) and `link` (or `""`)
- [ ] 223. In `search`: build one `SearchEvidence` with `query=query`, `snippets=[...]`, `urls=[...]`
- [ ] 224. In `search`: return `[evidence]` (single SearchEvidence object per query)
- [ ] 225. Define `format_for_agent(self, evidence_list: list[SearchEvidence]) -> str` method
- [ ] 226. In `format_for_agent`: for each evidence, write `"Query: {query}\n"`
- [ ] 227. In `format_for_agent`: for each snippet + url pair, write `"- {snippet} [Source: {url}]\n"`
- [ ] 228. In `format_for_agent`: join all blocks with `"\n---\n"`
- [ ] 229. In `format_for_agent`: cap total output at 2000 characters
- [ ] 230. Verify `search.py` does not exceed 150 lines

---

## PHASE 7 — Pro Agent (Tasks 231–270)

### 7.1 `src/agents/pro.py`
- [ ] 231. Create `src/agents/pro.py`
- [ ] 232. Add import: `import anthropic`
- [ ] 233. Add import: `from loguru import logger`
- [ ] 234. Add import: `from src.config import settings, prompts`
- [ ] 235. Add import: `from src.tools.search import SerperSearchTool`
- [ ] 236. Add import: `from src.debate.transcript import SearchEvidence`
- [ ] 237. Add import: `from src.watchdog.retry import with_retry`
- [ ] 238. Define `ProAgent` class
- [ ] 239. In `__init__`: instantiate `self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)`
- [ ] 240. In `__init__`: instantiate `self.search_tool = SerperSearchTool()`
- [ ] 241. In `__init__`: initialize `self.conversation_history: list[dict] = []`
- [ ] 242. In `__init__`: log "ProAgent initialized"
- [ ] 243. Define `search_for_evidence(self, round_number: int) -> list[SearchEvidence]`
- [ ] 244. In `search_for_evidence`: build query from round context e.g. `"smartphones reduce attention span study {round_number}"`
- [ ] 245. In `search_for_evidence`: call `self.search_tool.search(query)`
- [ ] 246. In `search_for_evidence`: return results
- [ ] 247. Define `_build_user_message(self, round_number, last_con_arg, evidence_text) -> str` private method
- [ ] 248. In `_build_user_message`: include round number
- [ ] 249. In `_build_user_message`: include `last_con_arg` as "Your opponent (Con) just said: ..."
- [ ] 250. In `_build_user_message`: include `evidence_text` as "Search evidence for this round: ..."
- [ ] 251. In `_build_user_message`: instruct to rebut Con's argument and reinforce Pro position
- [ ] 252. Define `_call_api(self, user_message: str) -> str` private method
- [ ] 253. In `_call_api`: append `{"role": "user", "content": user_message}` to history
- [ ] 254. In `_call_api`: call `self.client.messages.create(model=settings.MODEL_NAME, system=prompts.PRO_SYSTEM_PROMPT, messages=self.conversation_history, max_tokens=settings.MAX_TOKENS_AGENT)`
- [ ] 255. In `_call_api`: extract `response.content[0].text`
- [ ] 256. In `_call_api`: append `{"role": "assistant", "content": argument_text}` to history
- [ ] 257. In `_call_api`: return `argument_text`
- [ ] 258. Wrap `_call_api` with `@with_retry()` decorator
- [ ] 259. Define `generate_argument(self, round_number: int, last_con_arg: str, evidence: list[SearchEvidence]) -> str`
- [ ] 260. In `generate_argument`: call `self.search_tool.format_for_agent(evidence)` to get text
- [ ] 261. In `generate_argument`: call `_build_user_message(...)`
- [ ] 262. In `generate_argument`: call `_call_api(user_message)`
- [ ] 263. In `generate_argument`: log round number and argument length
- [ ] 264. In `generate_argument`: return argument text
- [ ] 265. Define `get_history(self) -> list[dict]` returning `self.conversation_history`
- [ ] 266. Define `reset(self)` clearing `self.conversation_history`
- [ ] 267. Count lines in `pro.py` — must be ≤ 150
- [ ] 268. Verify `ProAgent` can be instantiated without error
- [ ] 269. Verify `generate_argument` returns a non-empty string in a manual test
- [ ] 270. Verify conversation history grows by 2 entries per call

---

## PHASE 8 — Con Agent (Tasks 271–305)

### 8.1 `src/agents/con.py`
- [ ] 271. Create `src/agents/con.py`
- [ ] 272. Add import: `import anthropic`
- [ ] 273. Add import: `from loguru import logger`
- [ ] 274. Add import: `from src.config import settings, prompts`
- [ ] 275. Add import: `from src.tools.search import SerperSearchTool`
- [ ] 276. Add import: `from src.debate.transcript import SearchEvidence`
- [ ] 277. Add import: `from src.watchdog.retry import with_retry`
- [ ] 278. Define `ConAgent` class
- [ ] 279. In `__init__`: instantiate `self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)`
- [ ] 280. In `__init__`: instantiate `self.search_tool = SerperSearchTool()`
- [ ] 281. In `__init__`: initialize `self.conversation_history: list[dict] = []`
- [ ] 282. In `__init__`: log "ConAgent initialized"
- [ ] 283. Define `search_for_evidence(self, round_number: int) -> list[SearchEvidence]`
- [ ] 284. In `search_for_evidence`: build query e.g. `"smartphones improve learning productivity research {round_number}"`
- [ ] 285. In `search_for_evidence`: call `self.search_tool.search(query)`
- [ ] 286. In `search_for_evidence`: return results
- [ ] 287. Define `_build_user_message(self, round_number, last_pro_arg, evidence_text) -> str`
- [ ] 288. In `_build_user_message`: include round number
- [ ] 289. In `_build_user_message`: include `last_pro_arg` as "Your opponent (Pro) just said: ..."
- [ ] 290. In `_build_user_message`: include `evidence_text` as "Search evidence for this round: ..."
- [ ] 291. In `_build_user_message`: instruct to rebut Pro's argument and reinforce Con position
- [ ] 292. Define `_call_api(self, user_message: str) -> str` private method
- [ ] 293. In `_call_api`: append user message to history
- [ ] 294. In `_call_api`: call `self.client.messages.create(model=..., system=prompts.CON_SYSTEM_PROMPT, messages=..., max_tokens=...)`
- [ ] 295. In `_call_api`: extract response text
- [ ] 296. In `_call_api`: append assistant response to history
- [ ] 297. In `_call_api`: return text
- [ ] 298. Wrap `_call_api` with `@with_retry()` decorator
- [ ] 299. Define `generate_argument(self, round_number: int, last_pro_arg: str, evidence: list[SearchEvidence]) -> str`
- [ ] 300. In `generate_argument`: format evidence → call `_build_user_message` → call `_call_api`
- [ ] 301. In `generate_argument`: log round and length
- [ ] 302. In `generate_argument`: return argument text
- [ ] 303. Define `get_history(self) -> list[dict]`
- [ ] 304. Define `reset(self)`
- [ ] 305. Verify `con.py` does not exceed 150 lines

---

## PHASE 9 — Judge Agent (Tasks 306–355)

### 9.1 `src/agents/judge.py`
- [ ] 306. Create `src/agents/judge.py`
- [ ] 307. Add import: `import anthropic`
- [ ] 308. Add import: `from loguru import logger`
- [ ] 309. Add import: `from src.config import settings, prompts`
- [ ] 310. Add import: `from src.watchdog.retry import with_retry`
- [ ] 311. Define `JudgeAgent` class
- [ ] 312. In `__init__`: instantiate `self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)`
- [ ] 313. In `__init__`: initialize `self.evaluation_notes: list[str] = []`
- [ ] 314. In `__init__`: log "JudgeAgent initialized"
- [ ] 315. Define `generate_opening(self) -> str` method
- [ ] 316. In `generate_opening`: call API with instruction to open the debate formally
- [ ] 317. In `generate_opening`: return opening statement text
- [ ] 318. Define `_evaluate_call(self, prompt: str) -> str` private method
- [ ] 319. In `_evaluate_call`: call `self.client.messages.create(model=..., system=prompts.JUDGE_SYSTEM_PROMPT, messages=[{"role":"user","content":prompt}], max_tokens=512)`
- [ ] 320. In `_evaluate_call`: return response text
- [ ] 321. Wrap `_evaluate_call` with `@with_retry()`
- [ ] 322. Define `evaluate_exchange(self, round_num: int, pro_arg: str, con_arg: str) -> str`
- [ ] 323. In `evaluate_exchange`: build evaluation prompt listing round number, pro arg, con arg
- [ ] 324. In `evaluate_exchange`: ask judge to rate each arg on quality, evidence, consistency, relevance
- [ ] 325. In `evaluate_exchange`: call `_evaluate_call(prompt)`
- [ ] 326. In `evaluate_exchange`: append result to `self.evaluation_notes`
- [ ] 327. In `evaluate_exchange`: log note length
- [ ] 328. In `evaluate_exchange`: return evaluation notes string
- [ ] 329. Define `compile_transcript(self, exchanges: list) -> str` method
- [ ] 330. In `compile_transcript`: format each exchange as "=== Round N ===\nPRO: ...\nCON: ...\n"
- [ ] 331. In `compile_transcript`: return full formatted string
- [ ] 332. Define `_verdict_call(self, prompt: str) -> str` private method
- [ ] 333. In `_verdict_call`: call API with `max_tokens=settings.MAX_TOKENS_JUDGE`
- [ ] 334. Wrap `_verdict_call` with `@with_retry()`
- [ ] 335. Define `declare_winner(self, transcript: str) -> tuple[str, str]`
- [ ] 336. In `declare_winner`: build verdict prompt with full transcript + all evaluation notes
- [ ] 337. In `declare_winner`: include instruction: "Declare exactly one winner. Write 'WINNER: Pro' or 'WINNER: Con' on its own line."
- [ ] 338. In `declare_winner`: call `_verdict_call(prompt)`
- [ ] 339. In `declare_winner`: parse response for line starting with "WINNER:"
- [ ] 340. In `declare_winner`: extract winner token (strip whitespace)
- [ ] 341. In `declare_winner`: normalize to "Pro" or "Con" (case-insensitive match)
- [ ] 342. In `declare_winner`: if cannot parse, call `_verdict_call` again (up to 2 retries)
- [ ] 343. In `declare_winner`: if still cannot parse, raise `ValueError("Judge failed to declare a clear winner")`
- [ ] 344. In `declare_winner`: log winner declaration
- [ ] 345. In `declare_winner`: return `(winner, full_verdict_text)`
- [ ] 346. Define `get_evaluation_notes(self) -> list[str]`
- [ ] 347. Verify `judge.py` does not exceed 150 lines
- [ ] 348. Test `evaluate_exchange` returns a non-empty string
- [ ] 349. Test `declare_winner` returns "Pro" or "Con"
- [ ] 350. Test `declare_winner` never returns a tie

---

## PHASE 10 — Debate Orchestrator (Tasks 351–405)

### 10.1 `src/debate/orchestrator.py`
- [ ] 351. Create `src/debate/orchestrator.py`
- [ ] 352. Add import: `from rich.console import Console`
- [ ] 353. Add import: `from rich.panel import Panel`
- [ ] 354. Add import: `from rich.text import Text`
- [ ] 355. Add import: `from loguru import logger`
- [ ] 356. Add import: `from src.agents.pro import ProAgent`
- [ ] 357. Add import: `from src.agents.con import ConAgent`
- [ ] 358. Add import: `from src.agents.judge import JudgeAgent`
- [ ] 359. Add import: `from src.debate.transcript import DebateTranscript, Exchange, transcript_to_dict`
- [ ] 360. Add import: `from src.utils.results import save_transcript, save_verdict`
- [ ] 361. Add import: `from src.config import settings`
- [ ] 362. Define `DebateOrchestrator` class
- [ ] 363. In `__init__`: accept optional `topic` (default `settings.DEBATE_TOPIC`)
- [ ] 364. In `__init__`: accept optional `num_rounds` (default `settings.MIN_EXCHANGES`)
- [ ] 365. In `__init__`: instantiate `self.pro = ProAgent()`
- [ ] 366. In `__init__`: instantiate `self.con = ConAgent()`
- [ ] 367. In `__init__`: instantiate `self.judge = JudgeAgent()`
- [ ] 368. In `__init__`: instantiate `self.console = Console()`
- [ ] 369. In `__init__`: instantiate `self.transcript = DebateTranscript(topic=topic, timestamp=...)`
- [ ] 370. In `__init__`: initialize `self.exchanges: list[Exchange] = []`
- [ ] 371. Define `run_debate(self) -> dict` main method
- [ ] 372. In `run_debate`: log "Debate starting"
- [ ] 373. In `run_debate`: print topic banner to console
- [ ] 374. In `run_debate`: call `self._print_opening()`
- [ ] 375. In `run_debate`: loop `for round_num in range(1, self.num_rounds + 1):`
- [ ] 376. In loop: call `self._run_round(round_num)`
- [ ] 377. After loop: call `self._get_verdict()`
- [ ] 378. After loop: call `self._save_results()`
- [ ] 379. In `run_debate`: return summary dict `{topic, rounds, winner, verdict_file, transcript_file}`
- [ ] 380. Define `_print_opening(self)` method
- [ ] 381. In `_print_opening`: get judge opening statement via `self.judge.generate_opening()`
- [ ] 382. In `_print_opening`: print in yellow panel labeled "JUDGE — Opening"
- [ ] 383. Define `_run_round(self, round_num: int)` method
- [ ] 384. In `_run_round`: log `f"Starting round {round_num}"`
- [ ] 385. In `_run_round`: call `self.pro.search_for_evidence(round_num)`
- [ ] 386. In `_run_round`: get `last_con` (last Con argument, or "" for round 1)
- [ ] 387. In `_run_round`: call `self.pro.generate_argument(round_num, last_con, pro_evidence)`
- [ ] 388. In `_run_round`: print pro argument in blue panel labeled `f"PRO — Round {round_num}"`
- [ ] 389. In `_run_round`: call `self.con.search_for_evidence(round_num)`
- [ ] 390. In `_run_round`: call `self.con.generate_argument(round_num, pro_arg, con_evidence)`
- [ ] 391. In `_run_round`: print con argument in red panel labeled `f"CON — Round {round_num}"`
- [ ] 392. In `_run_round`: call `self.judge.evaluate_exchange(round_num, pro_arg, con_arg)`
- [ ] 393. In `_run_round`: build `Exchange` dataclass from round data
- [ ] 394. In `_run_round`: append exchange to `self.exchanges`
- [ ] 395. In `_run_round`: log round completion
- [ ] 396. Define `_get_verdict(self)` method
- [ ] 397. In `_get_verdict`: compile transcript string via `self.judge.compile_transcript(self.exchanges)`
- [ ] 398. In `_get_verdict`: call `self.judge.declare_winner(transcript_str)`
- [ ] 399. In `_get_verdict`: store `self.winner` and `self.verdict_text`
- [ ] 400. In `_get_verdict`: print verdict in yellow panel labeled "JUDGE — Final Verdict"
- [ ] 401. In `_get_verdict`: print bold winner announcement
- [ ] 402. Define `_save_results(self)` method
- [ ] 403. In `_save_results`: build transcript dict from `DebateTranscript`
- [ ] 404. In `_save_results`: call `save_transcript(transcript_dict)` → get path
- [ ] 405. In `_save_results`: call `save_verdict(self.winner, self.verdict_text)` → get path
- [ ] 406. In `_save_results`: print file paths to console
- [ ] 407. In `_save_results`: log all saved paths
- [ ] 408. Verify `orchestrator.py` does not exceed 150 lines
- [ ] 409. If orchestrator exceeds 150 lines, extract `_print_*` helpers to a `display.py` module

---

## PHASE 11 — CLI (Tasks 410–440)

### 11.1 `src/cli.py`
- [ ] 410. Create `src/cli.py`
- [ ] 411. Add import: `import click`
- [ ] 412. Add import: `from rich.console import Console`
- [ ] 413. Add import: `from loguru import logger`
- [ ] 414. Add import: `from src.config import settings`
- [ ] 415. Add import: `from src.config.settings import validate_config`
- [ ] 416. Add import: `from src.utils.logger import setup_logger`
- [ ] 417. Add import: `from src.utils.results import load_transcript, list_transcripts`
- [ ] 418. Define `console = Console()` at module level
- [ ] 419. Define `@click.group()` decorated `main()` function
- [ ] 420. Define `@main.command()` decorated `debate()` function
- [ ] 421. Add `@click.option("--topic", default=settings.DEBATE_TOPIC, help="Debate topic")`
- [ ] 422. Add `@click.option("--rounds", default=settings.MIN_EXCHANGES, type=int, help="Number of rounds")`
- [ ] 423. Add `@click.option("--verbose", is_flag=True, default=False, help="Enable debug logging")`
- [ ] 424. In `debate()`: call `validate_config()` — catch `ConfigurationError` and print friendly error
- [ ] 425. In `debate()`: call `setup_logger(log_file=...)` with timestamped log path
- [ ] 426. In `debate()`: instantiate `DebateOrchestrator(topic=topic, num_rounds=rounds)`
- [ ] 427. In `debate()`: wrap `orchestrator.run_debate()` in `try/except KeyboardInterrupt`
- [ ] 428. On `KeyboardInterrupt`: print "Debate interrupted by user." and exit cleanly
- [ ] 429. In `debate()`: print summary dict on completion
- [ ] 430. Define `@main.command("show-config")` function
- [ ] 431. In `show-config`: print `MODEL_NAME`, `MIN_EXCHANGES`, `RESULTS_DIR`
- [ ] 432. In `show-config`: print "ANTHROPIC_API_KEY: SET" or "NOT SET"
- [ ] 433. In `show-config`: print "SERPER_API_KEY: SET" or "NOT SET"
- [ ] 434. Define `@main.command("check-health")` function
- [ ] 435. In `check-health`: attempt a minimal Anthropic API call
- [ ] 436. In `check-health`: print "Anthropic API: OK" or error message
- [ ] 437. Define `@main.command("show-transcript")` with `@click.argument("path")`
- [ ] 438. In `show-transcript`: load transcript from path and pretty-print to console
- [ ] 439. Add `if __name__ == "__main__": main()` guard
- [ ] 440. Verify `cli.py` does not exceed 150 lines

---

## PHASE 12 — Tests (Tasks 441–500)

### 12.1 Test Configuration
- [ ] 441. Create `tests/conftest.py`
- [ ] 442. Add import: `import pytest`
- [ ] 443. Add import: `from unittest.mock import MagicMock, patch`
- [ ] 444. Define `mock_anthropic_response` fixture — returns a fake `Message` object with `.content[0].text`
- [ ] 445. Define `mock_search_results` fixture — returns a list of `SearchEvidence` objects
- [ ] 446. Define `sample_exchange` fixture — returns a populated `Exchange` object
- [ ] 447. Define `sample_transcript_dict` fixture — returns a complete debate transcript dict
- [ ] 448. Add `pytest.ini_options` in `pyproject.toml`: mark `integration` and `slow`

### 12.2 `tests/test_search.py`
- [ ] 449. Create `tests/test_search.py`
- [ ] 450. Write `test_search_returns_evidence_list()` — mock requests.post, verify returns list
- [ ] 451. Write `test_search_parses_snippets()` — verify snippets extracted correctly
- [ ] 452. Write `test_search_parses_urls()` — verify URLs extracted correctly
- [ ] 453. Write `test_search_handles_timeout()` — mock Timeout, verify empty list returned
- [ ] 454. Write `test_search_handles_connection_error()` — mock ConnectionError, verify empty list
- [ ] 455. Write `test_format_for_agent_caps_length()` — verify output ≤ 2000 chars
- [ ] 456. Write `test_format_for_agent_includes_query()` — verify query appears in output

### 12.3 `tests/test_watchdog.py`
- [ ] 457. Create `tests/test_watchdog.py`
- [ ] 458. Write `test_with_retry_succeeds_on_first_try()` — no exception, runs once
- [ ] 459. Write `test_with_retry_retries_on_timeout()` — raises Timeout twice, succeeds third
- [ ] 460. Write `test_with_retry_raises_after_max_attempts()` — always fails, raises exception
- [ ] 461. Write `test_circuit_breaker_starts_closed()` — `allow_request()` returns True initially
- [ ] 462. Write `test_circuit_breaker_opens_after_threshold()` — after N failures, blocks requests
- [ ] 463. Write `test_circuit_breaker_resets_after_timeout()` — after reset_timeout, allows again
- [ ] 464. Write `test_circuit_breaker_success_resets_count()` — success clears failure counter

### 12.4 `tests/test_pro_agent.py`
- [ ] 465. Create `tests/test_pro_agent.py`
- [ ] 466. Write `test_pro_agent_initializes()` — instantiation does not raise
- [ ] 467. Write `test_pro_generates_non_empty_argument()` — mock API, verify non-empty return
- [ ] 468. Write `test_pro_history_grows_per_call()` — two calls → history has 4 entries
- [ ] 469. Write `test_pro_reset_clears_history()` — after reset, history is empty
- [ ] 470. Write `test_pro_builds_message_with_evidence()` — verify evidence appears in user message

### 12.5 `tests/test_con_agent.py`
- [ ] 471. Create `tests/test_con_agent.py`
- [ ] 472. Write `test_con_agent_initializes()`
- [ ] 473. Write `test_con_generates_non_empty_argument()`
- [ ] 474. Write `test_con_history_grows_per_call()`
- [ ] 475. Write `test_con_reset_clears_history()`
- [ ] 476. Write `test_con_builds_message_with_evidence()`

### 12.6 `tests/test_judge.py`
- [ ] 477. Create `tests/test_judge.py`
- [ ] 478. Write `test_judge_initializes()`
- [ ] 479. Write `test_judge_evaluate_exchange_returns_string()` — mock API, non-empty return
- [ ] 480. Write `test_judge_notes_accumulate()` — two evaluations → 2 notes
- [ ] 481. Write `test_judge_declares_pro_winner()` — mock verdict response with "WINNER: Pro"
- [ ] 482. Write `test_judge_declares_con_winner()` — mock verdict response with "WINNER: Con"
- [ ] 483. Write `test_judge_no_tie_allowed()` — mock ambiguous response, verify ValueError raised
- [ ] 484. Write `test_judge_compile_transcript_format()` — verify round headers in output

### 12.7 `tests/test_orchestrator.py`
- [ ] 485. Create `tests/test_orchestrator.py`
- [ ] 486. Write `test_orchestrator_initializes()` — agents instantiated
- [ ] 487. Write `test_orchestrator_runs_correct_rounds()` — mock agents, count round calls
- [ ] 488. Write `test_orchestrator_returns_winner_in_dict()` — result dict has "winner" key
- [ ] 489. Write `test_orchestrator_saves_transcript()` — verify file created in results/
- [ ] 490. Write `test_orchestrator_saves_verdict()` — verify verdict file created

### 12.8 `tests/test_cli.py`
- [ ] 491. Create `tests/test_cli.py`
- [ ] 492. Add import: `from click.testing import CliRunner`
- [ ] 493. Add import: `from src.cli import main`
- [ ] 494. Write `test_cli_main_help()` — `runner.invoke(main, ["--help"])`, assert exit code 0
- [ ] 495. Write `test_cli_debate_help()` — `runner.invoke(main, ["debate", "--help"])`, assert exit 0
- [ ] 496. Write `test_cli_show_config()` — assert "MODEL_NAME" in output
- [ ] 497. Write `test_cli_check_health_missing_key()` — missing ANTHROPIC_API_KEY → error message
- [ ] 498. Write `test_cli_show_transcript_missing_file()` — bad path → graceful error
- [ ] 499. Run `pytest tests/ -v` — all unit tests must pass
- [ ] 500. Fix any unit test failures before proceeding

---

## PHASE 13 — Integration & End-to-End (Tasks 501–520)

- [ ] 501. Set real `ANTHROPIC_API_KEY` in `.env`
- [ ] 502. Set real `SERPER_API_KEY` in `.env`
- [ ] 503. Run `python -m src.cli check-health` — verify "OK"
- [ ] 504. Run `python -m src.cli debate --rounds 10`
- [ ] 505. Verify exactly 10 rounds complete
- [ ] 506. Verify Pro agent argues against smartphones in every round
- [ ] 507. Verify Con agent argues for smartphones in every round
- [ ] 508. Verify Judge evaluates each round (10 notes generated)
- [ ] 509. Verify a single winner is declared — check console output
- [ ] 510. Verify transcript JSON file exists in `results/transcripts/`
- [ ] 511. Open transcript JSON — verify it is valid JSON
- [ ] 512. Verify transcript has `exchanges` array with 10+ items
- [ ] 513. Verify each exchange has `pro_argument`, `con_argument`, `judge_notes`
- [ ] 514. Verify `search_evidence` fields are populated in exchanges
- [ ] 515. Verify verdict text file exists in `results/verdicts/`
- [ ] 516. Verify log file exists in `results/logs/`
- [ ] 517. Run `find src -name "*.py" -exec wc -l {} + | sort -n` — confirm every file is ≤ 150 lines; if any exceeds 150, split it before continuing
- [ ] 518. Run `python -m src.cli show-config` — verify output is correct
- [ ] 519. Run `python -m src.cli show-transcript <path>` — verify readable output
- [ ] 520. Commit `results/` from this run as proof of successful execution

---

## PHASE 14 — Code Quality (Tasks 521–540)

- [ ] 521. Install `ruff` via `uv pip install ruff`
- [ ] 522. Run `ruff check src/` — fix all errors
- [ ] 523. Run `ruff check tests/` — fix all errors
- [ ] 524. Install `mypy` if not present
- [ ] 525. Run `mypy src/` — fix critical type errors
- [ ] 526. Verify no `print()` statements remain — use `console.print()` or `logger.*`
- [ ] 527. Verify no hardcoded API keys anywhere in source
- [ ] 528. Verify all imports are used (no unused imports)
- [ ] 529. Verify all public methods have type hints on signature
- [ ] 530. Verify all `dataclass` fields have type annotations
- [ ] 531. Run `find src -name "*.py" -exec wc -l {} + | sort -n` — every file must be ≤ 150 lines; split any that exceed the limit
- [ ] 532. Confirm no Python file in `tests/` exceeds 150 lines
- [ ] 533. Remove any debug `print` statements added during development
- [ ] 534. Remove any commented-out code blocks
- [ ] 535. Ensure `results/.gitkeep` files are present in all three subdirs
- [ ] 536. Verify `.env` is NOT tracked by git (`git status` should not show it)
- [ ] 537. Verify `.env.example` IS tracked by git
- [ ] 538. Run full test suite one final time: `pytest tests/ -v`
- [ ] 539. All tests green before committing final code
- [ ] 540. Write short docstrings only where logic is non-obvious

---

## PHASE 15 — Documentation Finalization (Tasks 541–555)

- [ ] 541. Update `README.md` with actual run output example (copy from a real run)
- [ ] 542. Verify all Mermaid diagrams in `README.md` render correctly on GitHub
- [ ] 543. Verify setup commands in README work from a fresh clone
- [ ] 544. Update `requirements.txt` with pinned versions (`uv pip freeze > requirements.txt`)
- [ ] 545. Review `prd.md` — confirm all sections are complete
- [ ] 546. Review `plan.md` — confirm architecture matches actual implementation
- [ ] 547. Review `todo.md` — mark all completed tasks with `[x]`
- [ ] 548. Add `CHANGELOG.md` entry for v1.0.0 (optional but recommended)
- [ ] 549. Verify no sensitive information in any committed file
- [ ] 550. Final check: `git status` shows only intended files

---

## PHASE 16 — GitHub Submission (Tasks 551–565)

- [ ] 551. Stage documentation files: `git add prd.md plan.md todo.md README.md requirements.txt .gitignore`
- [ ] 552. Commit: `git commit -m "docs: Vibe Coding documentation files"`
- [ ] 553. Stage source files: `git add src/ tests/ .env.example pyproject.toml`
- [ ] 554. Commit: `git commit -m "feat: implement multi-agent debate system"`
- [ ] 555. Stage results: `git add results/`
- [ ] 556. Commit: `git commit -m "results: add proof-of-execution from successful debate run"`
- [ ] 557. Push to remote: `git push origin main`
- [ ] 558. Verify all files are on GitHub
- [ ] 559. Check repository is public
- [ ] 560. Tag release: `git tag v1.0.0`
- [ ] 561. Push tags: `git push origin --tags`
- [ ] 562. Create GitHub Release from v1.0.0 tag
- [ ] 563. Verify the release notes describe the assignment
- [ ] 564. Test clone in a fresh directory — `git clone <url>` → follow README → debate runs
- [ ] 565. Submit repository URL to course portal

---

**Total tasks: 565**
