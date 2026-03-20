from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY_ROOT = ROOT / "quality_samples"
MANIFEST_PATH = QUALITY_ROOT / "manifest.json"


def test_quality_sample_manifest_is_consistent():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cases = manifest["cases"]

    assert manifest["version"] == 1
    assert len(cases) >= 10

    case_ids = set()
    mode_counts = {"generate": 0, "revise": 0}

    for entry in cases:
        case_id = entry["caseId"]
        case_path = QUALITY_ROOT / entry["path"]

        assert case_id not in case_ids
        assert case_path.exists(), f"Missing case file: {case_path}"

        case_data = json.loads(case_path.read_text(encoding="utf-8"))
        assert case_data["caseId"] == case_id
        assert case_data["mode"] == entry["mode"]
        assert case_data["category"] == entry["category"]
        assert case_data["acceptanceNotes"]
        assert case_data["regressionFocus"]

        for source in case_data.get("sources", []):
            assert (QUALITY_ROOT / source).exists(), f"Missing source file: {source}"

        if case_data["mode"] == "revise":
            assert case_data.get("inputCaseId")

        mode_counts[case_data["mode"]] += 1
        case_ids.add(case_id)

    assert mode_counts["generate"] >= 7
    assert mode_counts["revise"] >= 3
