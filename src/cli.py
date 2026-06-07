from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console

from src.config.settings import (
    ANTHROPIC_API_KEY,
    DEBATE_TOPIC,
    MIN_EXCHANGES,
    MODEL_NAME,
    RESULTS_DIR,
    SERPER_API_KEY,
    validate_config,
    ConfigurationError,
)
from src.utils.logger import setup_logger
from src.utils.results import load_transcript

console = Console()


@click.group()
def main() -> None:
    """AI Agent Debate System — multi-agent CLI debate platform."""


@main.command()
@click.option("--topic", default=DEBATE_TOPIC, show_default=True, help="Debate topic")
@click.option("--rounds", default=MIN_EXCHANGES, type=int, show_default=True, help="Number of rounds (min 10)")
@click.option("--verbose", is_flag=True, default=False, help="Enable DEBUG logging")
@click.option("--demo", is_flag=True, default=False, help="Run in demo mode (no API key required)")
def debate(topic: str, rounds: int, verbose: bool, demo: bool) -> None:
    """Run the full multi-agent debate."""
    log_path = RESULTS_DIR / "debate.log"
    setup_logger(log_file=log_path, verbose=verbose)

    if demo:
        from src.debate.demo_runner import DemoRunner
        try:
            result = DemoRunner(num_rounds=rounds).execute()
            console.print("\n[bold]Demo run complete.[/bold]")
            console.print(json.dumps({k: v for k, v in result.items() if k != "gatekeeper"}, indent=2))
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted.[/yellow]")
        return

    try:
        validate_config()
    except ConfigurationError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        console.print("[dim]Tip: run with --demo to test without an API key.")
        sys.exit(1)

    from src.gatekeeper import Gatekeeper
    from src.agents.pro import ProAgent
    from src.agents.con import ConAgent
    from src.agents.judge import JudgeAgent

    gk = Gatekeeper()
    pro = ProAgent(gk)
    con = ConAgent(gk)
    judge = JudgeAgent(gk)
    judge._topic = topic

    try:
        result = judge.run_debate(pro, con, num_rounds=rounds)
        console.print("\n[bold]Run complete.[/bold]")
        console.print(json.dumps({k: v for k, v in result.items() if k != "gatekeeper"}, indent=2))
    except KeyboardInterrupt:
        console.print("\n[yellow]Debate interrupted by user.[/yellow]")
        sys.exit(0)


@main.command("show-config")
def show_config() -> None:
    """Display loaded configuration."""
    console.print(f"model         : {MODEL_NAME}")
    console.print(f"min_exchanges : {MIN_EXCHANGES}")
    console.print(f"results_dir   : {RESULTS_DIR}")
    console.print(f"anthropic_key : {'SET' if ANTHROPIC_API_KEY else 'NOT SET'}")
    console.print(f"serper_key    : {'SET' if SERPER_API_KEY else 'NOT SET (fallback mode)'}")


@main.command("check-health")
def check_health() -> None:
    """Ping the Anthropic API with a minimal request."""
    if not ANTHROPIC_API_KEY:
        console.print("[red]ANTHROPIC_API_KEY not set.[/red]")
        sys.exit(1)
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        resp = client.messages.create(
            model=MODEL_NAME,
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}],
        )
        console.print(f"[green]Anthropic API: OK[/green] (model={MODEL_NAME})")
    except Exception as exc:
        console.print(f"[red]Anthropic API error:[/red] {exc}")
        sys.exit(1)


@main.command("show-transcript")
@click.argument("path", default="", required=False)
def show_transcript(path: str) -> None:
    """Display a saved transcript (defaults to results/transcript.json)."""
    p = Path(path) if path else None
    try:
        data = load_transcript(p)
        console.print(f"Topic   : {data.get('topic')}")
        console.print(f"Messages: {data.get('total_messages')}")
        for msg in data.get("messages", [])[:4]:
            console.print(f"  [{msg['speaker']} R{msg['round_number']}] {msg['claim'][:80]}…")
    except Exception as exc:
        console.print(f"[red]Could not load transcript:[/red] {exc}")
        sys.exit(1)
