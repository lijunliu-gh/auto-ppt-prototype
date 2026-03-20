from __future__ import annotations

from pathlib import Path

import pytest

import auto_ppt_cli


class TestParseArgs:
    def test_generate_requires_prompt(self):
        with pytest.raises(SystemExit):
            auto_ppt_cli.parse_args(["generate"])

    def test_generate_accepts_prompt(self):
        args = auto_ppt_cli.parse_args(["generate", "--prompt", "Create a deck"])
        assert args.command == "generate"
        assert args.prompt == "Create a deck"

    def test_prompt_file_populates_prompt(self, tmp_path):
        prompt_file = tmp_path / "prompt.md"
        prompt_file.write_text("Build a market update deck", encoding="utf-8")
        args = auto_ppt_cli.parse_args(["generate", "--prompt-file", str(prompt_file)])
        assert args.prompt == "Build a market update deck"


class TestBuildRequest:
    def test_generate_request_uses_output_dir(self):
        args = auto_ppt_cli.parse_args(
            [
                "generate",
                "--prompt",
                "Create a deck",
                "--source",
                "brief.md",
                "--output-dir",
                "custom-output",
            ]
        )
        request = auto_ppt_cli.build_request(args)
        assert request["action"] == "create"
        assert request["sources"] == [{"path": "brief.md"}]
        assert request["outputJson"].endswith("custom-output/py-generated-deck.json")
        assert request["outputPptx"].endswith("custom-output/py-generated-deck.pptx")

    def test_revise_request_sets_deck_path(self):
        args = auto_ppt_cli.parse_args(
            ["revise", "--prompt", "Tighten the flow", "--deck", "output/base.json"]
        )
        request = auto_ppt_cli.build_request(args)
        assert request["action"] == "revise"
        assert request["deckPath"] == "output/base.json"
        assert request["outputJson"].endswith("output/py-revised-deck.json")


class TestMain:
    def test_main_calls_handle_skill_request(self, monkeypatch, capsys, tmp_path):
        captured = {}

        def fake_handle_skill_request(request, response_path=None):
            captured["request"] = request
            return {
                "action": "create",
                "deckJsonPath": str(tmp_path / "deck.json"),
                "pptxPath": str(tmp_path / "deck.pptx"),
                "renderer": "pptxgenjs",
                "slideCount": 6,
                "sourcesUsed": [],
            }

        monkeypatch.setattr(auto_ppt_cli, "handle_skill_request", fake_handle_skill_request)
        exit_code = auto_ppt_cli.main(["generate", "--prompt", "Create a deck"])
        output = capsys.readouterr().out

        assert exit_code == 0
        assert captured["request"]["action"] == "create"
        assert "Generated deck JSON" in output

    def test_main_returns_error_code_on_exception(self, monkeypatch, capsys):
        def raise_error(request, response_path=None):
            raise RuntimeError("boom")

        monkeypatch.setattr(auto_ppt_cli, "handle_skill_request", raise_error)
        exit_code = auto_ppt_cli.main(["generate", "--prompt", "Create a deck"])
        error = capsys.readouterr().err
        assert exit_code == 1
        assert "auto-ppt: error: boom" in error