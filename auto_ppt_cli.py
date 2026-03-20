from __future__ import annotations

import argparse
import sys
from pathlib import Path

from python_backend import ROOT_DIR, read_text_file, resolve_path
from python_backend.skill_api import handle_skill_request

DEFAULT_CREATE_JSON = Path("output") / "py-generated-deck.json"
DEFAULT_CREATE_PPTX = Path("output") / "py-generated-deck.pptx"
DEFAULT_REVISE_DECK = Path("output") / "py-generated-deck.json"
DEFAULT_REVISE_JSON = Path("output") / "py-revised-deck.json"
DEFAULT_REVISE_PPTX = Path("output") / "py-revised-deck.pptx"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto-ppt",
        description="Official CLI for generating and revising PowerPoint decks.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Create a new deck from a prompt")
    _add_common_generation_args(generate)

    revise = subparsers.add_parser("revise", help="Revise an existing deck from a prompt")
    _add_common_generation_args(revise)
    revise.add_argument(
        "--deck",
        default=str(DEFAULT_REVISE_DECK),
        help="Existing deck JSON file to revise (default: output/py-generated-deck.json)",
    )

    return parser


def _add_common_generation_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt", help="Presentation request in natural language")
    parser.add_argument("--prompt-file", help="Read the prompt from a text file")
    parser.add_argument("--source", action="append", default=[], help="Source file path or URL to include")
    parser.add_argument(
        "--context-file",
        action="append",
        default=[],
        help="Extra context material to include in planning",
    )
    parser.add_argument("--template", help="Optional .pptx template path")
    parser.add_argument("--research", action="store_true", help="Enable optional web research")
    parser.add_argument("--mock", action="store_true", help="Use the local mock planner instead of an LLM")
    parser.add_argument("--output-dir", help="Directory for output files")
    parser.add_argument("--out-json", help="Explicit path for deck JSON output")
    parser.add_argument("--out-pptx", help="Explicit path for PPTX output")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = create_parser()
    args = parser.parse_args(argv)
    if args.prompt_file:
        args.prompt = read_text_file(resolve_path(args.prompt_file))
    if not args.prompt or not args.prompt.strip():
        parser.error("A prompt is required. Use --prompt or --prompt-file.")
    return args


def build_request(args: argparse.Namespace) -> dict:
    base_dir = Path.cwd()
    request: dict = {
        "action": "create" if args.command == "generate" else "revise",
        "prompt": args.prompt,
        "mock": bool(args.mock),
        "research": bool(args.research),
        "_baseDir": str(base_dir),
    }

    if args.source:
        request["sources"] = [
            {"url": value} if value.startswith(("http://", "https://")) else {"path": value}
            for value in args.source
        ]
    if args.context_file:
        request["contextFiles"] = list(args.context_file)
    if args.template:
        request["template"] = args.template
    if args.command == "revise":
        request["deckPath"] = args.deck

    output_json, output_pptx = _resolve_output_paths(args)
    request["outputJson"] = str(output_json)
    request["outputPptx"] = str(output_pptx)
    return request


def _resolve_output_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.output_dir:
        base = Path(args.output_dir)
        if args.command == "generate":
            default_json = base / DEFAULT_CREATE_JSON.name
            default_pptx = base / DEFAULT_CREATE_PPTX.name
        else:
            default_json = base / DEFAULT_REVISE_JSON.name
            default_pptx = base / DEFAULT_REVISE_PPTX.name
    else:
        if args.command == "generate":
            default_json = DEFAULT_CREATE_JSON
            default_pptx = DEFAULT_CREATE_PPTX
        else:
            default_json = DEFAULT_REVISE_JSON
            default_pptx = DEFAULT_REVISE_PPTX

    output_json = Path(args.out_json) if args.out_json else default_json
    output_pptx = Path(args.out_pptx) if args.out_pptx else default_pptx
    return output_json, output_pptx


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        response = handle_skill_request(build_request(args), response_path=None)
    except Exception as error:  # noqa: BLE001
        print(f"auto-ppt: error: {error}", file=sys.stderr)
        return 1

    verb = "Generated" if response.get("action") == "create" else "Revised"
    print(f"{verb} deck JSON: {response['deckJsonPath']}")
    print(f"{verb} PPTX: {response['pptxPath']}")
    print(f"Renderer: {response['renderer']}")
    print(f"Slides: {response['slideCount']}")
    if response.get("sourcesUsed"):
        print(f"Sources used: {len(response['sourcesUsed'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())