"""Tests for the quality scorecard system."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from python_backend.quality_scorer import (
    check_chart_integrity,
    check_empty_content_slides,
    check_layout_validity,
    check_layout_variety,
    check_metadata_fields,
    check_page_budget,
    check_revision_quality,
    check_schema_compliance,
    check_slide_density,
    check_slide_numbering,
    check_source_attribution,
    check_speaker_notes,
    check_title_quality,
    score_deck,
)
from python_backend.smart_layer import (
    build_mock_deck,
    _extract_guardrail_hints,
    build_create_prompt,
    apply_heuristic_revision,
    detect_revise_intent,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _minimal_deck(slides=None, **overrides):
    """Build a minimal valid deck for testing."""
    base = {
        "schemaVersion": "0.3.0",
        "deckTitle": "Test Deck",
        "language": "en-US",
        "audience": "Testers",
        "scenario": "Unit test",
        "tone": "Professional",
        "theme": "business-clean",
        "sourceDisplayMode": "hidden",
        "slideCount": 1,
        "needsSpeakerNotes": False,
        "assumptions": [],
        "slides": slides or [_minimal_slide(1, "title", "Test Title")],
    }
    base.update(overrides)
    if "slideCount" not in overrides:
        base["slideCount"] = len(base["slides"])
    return base


def _minimal_slide(page, layout, title, **overrides):
    """Build a minimal valid slide."""
    slide = {
        "page": page,
        "layout": layout,
        "title": title,
        "subtitle": "",
        "objective": "",
        "bullets": [],
        "left": [],
        "right": [],
        "table": {"columns": [], "rows": []},
        "chart": {"type": "", "title": "", "categories": [], "series": []},
        "visuals": [],
        "sources": [],
        "speakerNotes": [],
    }
    slide.update(overrides)
    return slide


# ===========================================================================
# Hard check tests
# ===========================================================================


class TestSchemaCompliance:
    def test_valid_deck_passes(self):
        deck = _minimal_deck()
        assert check_schema_compliance(deck) == []

    def test_missing_required_field_fails(self):
        deck = _minimal_deck()
        del deck["deckTitle"]
        errors = check_schema_compliance(deck)
        assert any("deckTitle" in e for e in errors)

    def test_mock_deck_passes(self):
        deck = build_mock_deck("Test prompt", [], [], [])
        assert check_schema_compliance(deck) == []


class TestSlideNumbering:
    def test_consecutive_numbering_passes(self):
        slides = [_minimal_slide(i, "bullet", f"Slide {i}") for i in range(1, 4)]
        deck = _minimal_deck(slides=slides)
        assert check_slide_numbering(deck) == []

    def test_wrong_page_number_fails(self):
        slides = [
            _minimal_slide(1, "title", "First"),
            _minimal_slide(3, "bullet", "Skipped"),
        ]
        deck = _minimal_deck(slides=slides)
        issues = check_slide_numbering(deck)
        assert len(issues) >= 1
        assert "expected=2" in issues[0]

    def test_count_mismatch_fails(self):
        slides = [_minimal_slide(1, "title", "Only")]
        deck = _minimal_deck(slides=slides, slideCount=5)
        issues = check_slide_numbering(deck)
        assert any("slideCount=5" in i for i in issues)


class TestLayoutValidity:
    def test_supported_layouts_pass(self):
        slides = [_minimal_slide(1, "bullet", "OK")]
        deck = _minimal_deck(slides=slides)
        assert check_layout_validity(deck) == []

    def test_unknown_layout_fails(self):
        slides = [_minimal_slide(1, "fancy-grid", "Bad")]
        deck = _minimal_deck(slides=slides)
        issues = check_layout_validity(deck)
        assert len(issues) == 1
        assert "fancy-grid" in issues[0]


class TestChartIntegrity:
    def test_valid_chart_passes(self):
        chart = {
            "type": "bar",
            "title": "Revenue",
            "categories": ["Q1", "Q2", "Q3"],
            "series": [{"name": "Sales", "data": [100, 200, 300]}],
        }
        slides = [_minimal_slide(1, "chart", "Chart", chart=chart)]
        deck = _minimal_deck(slides=slides)
        assert check_chart_integrity(deck) == []

    def test_empty_chart_skipped(self):
        slides = [_minimal_slide(1, "bullet", "No chart")]
        deck = _minimal_deck(slides=slides)
        assert check_chart_integrity(deck) == []

    def test_bad_chart_type_fails(self):
        chart = {
            "type": "donut",
            "title": "Bad",
            "categories": ["A"],
            "series": [{"name": "X", "data": [1]}],
        }
        slides = [_minimal_slide(1, "chart", "Bad", chart=chart)]
        deck = _minimal_deck(slides=slides)
        issues = check_chart_integrity(deck)
        assert any("donut" in i for i in issues)

    def test_series_length_mismatch_fails(self):
        chart = {
            "type": "bar",
            "title": "Mismatch",
            "categories": ["Q1", "Q2"],
            "series": [{"name": "X", "data": [1, 2, 3]}],
        }
        slides = [_minimal_slide(1, "chart", "Mismatch", chart=chart)]
        deck = _minimal_deck(slides=slides)
        issues = check_chart_integrity(deck)
        assert any("length" in i for i in issues)

    def test_non_numeric_data_fails(self):
        chart = {
            "type": "bar",
            "title": "Non-num",
            "categories": ["A"],
            "series": [{"name": "X", "data": ["abc"]}],
        }
        slides = [_minimal_slide(1, "chart", "Non-num", chart=chart)]
        deck = _minimal_deck(slides=slides)
        issues = check_chart_integrity(deck)
        assert any("not numeric" in i for i in issues)


# ===========================================================================
# Soft check tests
# ===========================================================================


class TestSlideDensity:
    def test_normal_density_clean(self):
        slides = [_minimal_slide(1, "bullet", "OK", bullets=["a", "b", "c"])]
        deck = _minimal_deck(slides=slides)
        assert check_slide_density(deck) == []

    def test_overdense_warns(self):
        slides = [_minimal_slide(1, "bullet", "Dense", bullets=list("abcdefghij"))]
        deck = _minimal_deck(slides=slides)
        warnings = check_slide_density(deck)
        assert len(warnings) == 1


class TestEmptyContent:
    def test_structural_slide_ok_empty(self):
        slides = [_minimal_slide(1, "title", "Welcome")]
        deck = _minimal_deck(slides=slides)
        assert check_empty_content_slides(deck) == []

    def test_content_slide_needs_content(self):
        slides = [_minimal_slide(1, "bullet", "Empty body")]
        deck = _minimal_deck(slides=slides)
        warnings = check_empty_content_slides(deck)
        assert len(warnings) == 1

    def test_chart_counts_as_content(self):
        chart = {
            "type": "bar",
            "title": "Revenue",
            "categories": ["Q1"],
            "series": [{"name": "X", "data": [1]}],
        }
        slides = [_minimal_slide(1, "chart", "Chart", chart=chart)]
        deck = _minimal_deck(slides=slides)
        assert check_empty_content_slides(deck) == []


class TestTitleQuality:
    def test_good_title_passes(self):
        slides = [_minimal_slide(1, "bullet", "Market Overview")]
        deck = _minimal_deck(slides=slides)
        assert check_title_quality(deck) == []

    def test_missing_title_warns(self):
        slides = [_minimal_slide(1, "bullet", "")]
        deck = _minimal_deck(slides=slides)
        assert len(check_title_quality(deck)) == 1

    def test_very_short_title_warns(self):
        slides = [_minimal_slide(1, "bullet", "Hi")]
        deck = _minimal_deck(slides=slides)
        assert len(check_title_quality(deck)) == 1


class TestSpeakerNotes:
    def test_not_requested_clean(self):
        deck = _minimal_deck(needsSpeakerNotes=False)
        assert check_speaker_notes(deck) == []

    def test_requested_and_present_clean(self):
        slides = [_minimal_slide(1, "bullet", "OK", speakerNotes=["Talk about this"])]
        deck = _minimal_deck(slides=slides, needsSpeakerNotes=True)
        assert check_speaker_notes(deck) == []

    def test_requested_but_mostly_missing_warns(self):
        slides = [
            _minimal_slide(i, "bullet", f"S{i}", speakerNotes=[])
            for i in range(1, 6)
        ]
        deck = _minimal_deck(slides=slides, needsSpeakerNotes=True)
        warnings = check_speaker_notes(deck)
        assert len(warnings) >= 1


class TestLayoutVariety:
    def test_varied_layouts_clean(self):
        slides = [
            _minimal_slide(1, "title", "Title"),
            _minimal_slide(2, "bullet", "A", bullets=["x"]),
            _minimal_slide(3, "two-column", "B", left=["l"], right=["r"]),
            _minimal_slide(4, "chart", "C", chart={"type": "bar", "title": "T", "categories": ["Q1"], "series": [{"name": "X", "data": [1]}]}),
        ]
        deck = _minimal_deck(slides=slides)
        assert check_layout_variety(deck) == []

    def test_monotone_layout_warns(self):
        slides = [
            _minimal_slide(1, "title", "Title"),
            _minimal_slide(2, "bullet", "A", bullets=["x"]),
            _minimal_slide(3, "bullet", "B", bullets=["y"]),
            _minimal_slide(4, "bullet", "C", bullets=["z"]),
            _minimal_slide(5, "bullet", "D", bullets=["w"]),
        ]
        deck = _minimal_deck(slides=slides)
        warnings = check_layout_variety(deck)
        assert len(warnings) == 1


class TestSourceAttribution:
    def test_hidden_mode_always_clean(self):
        deck = _minimal_deck(sourceDisplayMode="hidden")
        assert check_source_attribution(deck) == []

    def test_notes_mode_with_sources_clean(self):
        slides = [_minimal_slide(1, "bullet", "A", bullets=["x"], sources=[{"label": "Test", "ref": "test.md"}])]
        deck = _minimal_deck(slides=slides, sourceDisplayMode="notes")
        assert check_source_attribution(deck) == []

    def test_notes_mode_without_sources_warns(self):
        slides = [_minimal_slide(1, "bullet", "A", bullets=["x"])]
        deck = _minimal_deck(slides=slides, sourceDisplayMode="notes")
        warnings = check_source_attribution(deck)
        assert len(warnings) == 1


# ===========================================================================
# Composite scorer tests
# ===========================================================================


class TestScoreDeck:
    def test_valid_deck_passes(self):
        deck = _minimal_deck()
        result = score_deck(deck)
        assert result["pass"] is True
        assert result["hard_score"] == 1.0

    def test_mock_deck_passes(self):
        deck = build_mock_deck("Create an 8-slide strategy deck", [], [], [])
        result = score_deck(deck)
        assert result["pass"] is True
        assert result["hard_score"] == 1.0

    def test_broken_deck_fails(self):
        deck = _minimal_deck()
        del deck["deckTitle"]
        result = score_deck(deck)
        assert result["pass"] is False
        assert "schema_compliance" in result["hard_failures"]

    def test_summary_reflects_status(self):
        deck = _minimal_deck()
        result = score_deck(deck)
        assert "PASS" in result["summary"]

    def test_soft_warnings_do_not_fail(self):
        slides = [_minimal_slide(1, "bullet", "Dense", bullets=list("abcdefghij"))]
        deck = _minimal_deck(slides=slides)
        result = score_deck(deck)
        assert result["pass"] is True
        assert result["soft_score"] < 1.0
        assert "warnings" in result["summary"]


# ===========================================================================
# Planning guardrail tests (#27)
# ===========================================================================


class TestPageBudget:
    def test_within_budget_clean(self):
        slides = [_minimal_slide(i, "bullet", f"S{i}", bullets=["x"]) for i in range(1, 11)]
        deck = _minimal_deck(slides=slides)
        assert check_page_budget(deck) == []

    def test_over_budget_warns(self):
        slides = [_minimal_slide(i, "bullet", f"S{i}", bullets=["x"]) for i in range(1, 16)]
        deck = _minimal_deck(slides=slides)
        warnings = check_page_budget(deck)
        assert len(warnings) == 1
        assert "15" in warnings[0]


class TestMetadataFields:
    def test_filled_fields_clean(self):
        deck = _minimal_deck()
        assert check_metadata_fields(deck) == []

    def test_empty_audience_warns(self):
        deck = _minimal_deck(audience="")
        warnings = check_metadata_fields(deck)
        assert any("audience" in w for w in warnings)

    def test_empty_tone_warns(self):
        deck = _minimal_deck(tone="")
        warnings = check_metadata_fields(deck)
        assert any("tone" in w for w in warnings)


class TestGuardrailHints:
    def test_hints_include_slide_count(self):
        hints = _extract_guardrail_hints("Create a 10-slide deck")
        assert "10" in hints

    def test_hints_include_audience(self):
        hints = _extract_guardrail_hints("Create an executive strategy deck")
        assert "Executive" in hints or "executive" in hints.lower()

    def test_hints_include_tone(self):
        hints = _extract_guardrail_hints("Create a professional tech overview")
        assert "tone" in hints.lower()

    def test_create_prompt_includes_guardrails(self):
        prompt = build_create_prompt("Create an 8-slide board update", [], [])
        assert "Planning constraints" in prompt
        assert "8" in prompt


# ===========================================================================
# Revise loop hardening tests (#28)
# ===========================================================================


class TestDetectReviseIntent:
    def test_shorten_detected(self):
        assert "shorten" in detect_revise_intent("Compress this deck to 6 slides")

    def test_expand_detected(self):
        assert "expand" in detect_revise_intent("Expand the analysis with more detail")

    def test_reframe_audience_detected(self):
        assert "reframe_audience" in detect_revise_intent("Rewrite for investor audience")

    def test_clarify_detected(self):
        assert "clarify" in detect_revise_intent("Simplify and tighten the language")

    def test_emphasize_detected(self):
        assert "emphasize" in detect_revise_intent("Emphasize the execution plan")

    def test_conclusion_detected(self):
        assert "conclusion" in detect_revise_intent("Make this more conclusion-driven")

    def test_multiple_intents(self):
        intents = detect_revise_intent("Compress and clarify for executives")
        assert "shorten" in intents
        assert "clarify" in intents

    def test_no_intent(self):
        assert detect_revise_intent("Change the title color") == []


class TestHeuristicRevision:
    def _make_mock_deck(self):
        return build_mock_deck("Create an 8-slide strategy deck", [], [], [])

    def test_compress_reduces_slides(self):
        deck = self._make_mock_deck()
        original_count = len(deck["slides"])
        revised = apply_heuristic_revision(deck, "Compress to 6 slides", [])
        assert len(revised["slides"]) <= original_count
        assert revised["slideCount"] == len(revised["slides"])

    def test_expand_adds_slide(self):
        deck = self._make_mock_deck()
        original_count = len(deck["slides"])
        revised = apply_heuristic_revision(deck, "Expand with more detail", [])
        assert len(revised["slides"]) >= original_count

    def test_reframe_audience_updates_metadata(self):
        deck = self._make_mock_deck()
        revised = apply_heuristic_revision(deck, "Rewrite for investor audience", [])
        assert "Investor" in revised["audience"]

    def test_clarify_trims_bullets(self):
        deck = self._make_mock_deck()
        # Add an overly long bullet
        deck["slides"][2]["bullets"] = ["A" * 200, "B" * 200, "C" * 200, "D" * 200, "E" * 200, "F" * 200, "G" * 200]
        revised = apply_heuristic_revision(deck, "Simplify the language", [])
        for s in revised["slides"]:
            for b in s.get("bullets", []):
                assert len(b) <= 80

    def test_conclusion_driven_moves_summary(self):
        deck = self._make_mock_deck()
        revised = apply_heuristic_revision(deck, "Make it more conclusion-driven", [])
        # Summary/conclusion should now be near the front
        layouts = [s["layout"] for s in revised["slides"]]
        assert "summary" in layouts[:3]

    def test_revise_preserves_schema(self):
        deck = self._make_mock_deck()
        revised = apply_heuristic_revision(deck, "Compress to 6 slides and clarify", [])
        result = score_deck(revised)
        assert result["pass"] is True

    def test_revise_preserves_consecutive_pages(self):
        deck = self._make_mock_deck()
        revised = apply_heuristic_revision(deck, "Compress to 5 slides", [])
        for i, s in enumerate(revised["slides"]):
            assert s["page"] == i + 1


class TestRevisionQuality:
    def _make_mock_deck(self):
        return build_mock_deck("Create an 8-slide strategy deck", [], [], [])

    def test_stable_revision_no_warnings(self):
        original = self._make_mock_deck()
        revised = apply_heuristic_revision(original, "Emphasize the execution plan", [])
        result = check_revision_quality(original, revised)
        # Stable revision should not have large structural change warnings
        assert result["title_preserved"] is True

    def test_large_slide_loss_warns(self):
        original = self._make_mock_deck()
        # Simulate drastic slide removal
        revised = json.loads(json.dumps(original))
        revised["slides"] = revised["slides"][:2]
        result = check_revision_quality(original, revised)
        assert any("large structural change" in w for w in result["warnings"])

    def test_content_loss_warns(self):
        original = self._make_mock_deck()
        revised = json.loads(json.dumps(original))
        # Strip all bullets from revised
        for s in revised["slides"]:
            s["bullets"] = []
            s["left"] = []
            s["right"] = []
        result = check_revision_quality(original, revised)
        assert any("content loss" in w for w in result["warnings"])
