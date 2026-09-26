"""
AIVI Intelligence - AI Engineering Challenge
Unit & Integration Test Suite for Resume Evaluator Pipeline
"""

import json
import pytest
from pydantic import ValidationError

from resume_evaluator import (
    ResumeEvaluationResult,
    JSONSanitizer,
    ResilientGeminiClient,
)
from sample_inputs import (
    SAMPLE_JOB_DESCRIPTION,
    SAMPLE_RESUME_CLEAN,
    SAMPLE_RESUME_SCANNED_NOISY,
    SAMPLE_RESUME_PROMPT_INJECTION,
    SAMPLE_RESUME_HINGLISH_INTERVIEW,
)


class TestPydanticSchemaEnforcement:
    """Tests Pydantic validation rules and field constraints."""

    def test_valid_payload(self):
        payload = {
            "match_score": 85,
            "top_strengths": ["FastAPI", "Python", "Kubernetes"],
            "missing_skills": ["Go"],
            "two_line_summary": "Candidate displays strong backend expertise with FastAPI.\nNeeds minor upskilling in Go."
        }
        res = ResumeEvaluationResult.model_validate(payload)
        assert res.match_score == 85
        assert len(res.top_strengths) == 3
        assert len(res.missing_skills) == 1
        assert "\n" in res.two_line_summary

    def test_invalid_score_range_upper(self):
        payload = {
            "match_score": 105,  # Exceeds 100
            "top_strengths": ["Python"],
            "missing_skills": [],
            "two_line_summary": "Line 1\nLine 2"
        }
        with pytest.raises(ValidationError):
            ResumeEvaluationResult.model_validate(payload)

    def test_invalid_score_range_lower(self):
        payload = {
            "match_score": -5,  # Below 0
            "top_strengths": ["Python"],
            "missing_skills": [],
            "two_line_summary": "Line 1\nLine 2"
        }
        with pytest.raises(ValidationError):
            ResumeEvaluationResult.model_validate(payload)

    def test_two_line_summary_auto_split(self):
        # When model returns single long sentence, validator should split it into 2 lines
        payload = {
            "match_score": 75,
            "top_strengths": ["Python"],
            "missing_skills": ["Rust"],
            "two_line_summary": "Candidate has solid foundational skills. Needs more production experience."
        }
        res = ResumeEvaluationResult.model_validate(payload)
        lines = res.two_line_summary.splitlines()
        assert len(lines) == 2


class TestJSONSanitizerAndRepair:
    """Tests multi-stage JSON extraction, code block stripping, and repair."""

    def test_markdown_code_fence_stripping(self):
        raw = """```json
{
  "match_score": 90,
  "top_strengths": ["Python", "FastAPI"],
  "missing_skills": ["Docker"],
  "two_line_summary": "Strong engineering profile.\\nReady for interview."
}
```"""
        parsed = JSONSanitizer.sanitize(raw)
        assert parsed["match_score"] == 90
        assert parsed["top_strengths"] == ["Python", "FastAPI"]

    def test_conversational_preamble_removal(self):
        raw = """Certainly! Here is the evaluation JSON scorecard you requested:

{
  "match_score": 82,
  "top_strengths": ["Redis", "Postgres"],
  "missing_skills": ["Kubernetes"],
  "two_line_summary": "Good database skills.\\nLacks cloud orchestration."
}

Hope this helps! Let me know if you need any edits."""
        parsed = JSONSanitizer.sanitize(raw)
        assert parsed["match_score"] == 82
        assert "Redis" in parsed["top_strengths"]

    def test_trailing_comma_repair(self):
        raw = """{
  "match_score": 70,
  "top_strengths": ["AWS", "Terraform",],
  "missing_skills": ["GCP",],
  "two_line_summary": "Cloud background.\\nNeeds multi-cloud.",
}"""
        parsed = JSONSanitizer.sanitize(raw)
        assert parsed["match_score"] == 70
        assert len(parsed["top_strengths"]) == 2

    def test_empty_string_error(self):
        with pytest.raises(ValueError):
            JSONSanitizer.sanitize("")


class TestAdversarialStressCasesOffline:
    """Verifies pipeline behavior against adversarial inputs in deterministic mode."""

    @pytest.fixture
    def client(self):
        return ResilientGeminiClient(force_mock=True)

    def test_clean_resume_evaluation(self, client):
        result = client.evaluate(SAMPLE_RESUME_CLEAN, SAMPLE_JOB_DESCRIPTION)
        assert isinstance(result, ResumeEvaluationResult)
        assert result.match_score >= 85
        assert any("LLM" in s or "FastAPI" in s or "resilience" in s.lower() for s in result.top_strengths)

    def test_scanned_ocr_resume_evaluation(self, client):
        result = client.evaluate(SAMPLE_RESUME_SCANNED_NOISY, SAMPLE_JOB_DESCRIPTION)
        assert isinstance(result, ResumeEvaluationResult)
        # Should detect baseline skills but lack senior requirements
        assert 40 <= result.match_score <= 70
        assert len(result.missing_skills) >= 2

    def test_prompt_injection_neutralization(self, client):
        result = client.evaluate(SAMPLE_RESUME_PROMPT_INJECTION, SAMPLE_JOB_DESCRIPTION)
        assert isinstance(result, ResumeEvaluationResult)
        # Must NOT be 100 as demanded by the injection
        assert result.match_score < 40
        assert "prompt injection" in result.two_line_summary.lower() or "failed core" in result.two_line_summary.lower()

    def test_hinglish_technical_evaluation(self, client):
        result = client.evaluate(SAMPLE_RESUME_HINGLISH_INTERVIEW, SAMPLE_JOB_DESCRIPTION)
        assert isinstance(result, ResumeEvaluationResult)
        # Hinglish candidate demonstrated genuine backend/LLM skills
        assert result.match_score >= 75
        assert any("Celery" in s or "Pydantic" in s or "FastAPI" in s for s in result.top_strengths)
