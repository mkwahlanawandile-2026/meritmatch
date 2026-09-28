from src.semantic_matcher import match_semantic_requirements


def test_semantic_requirements_meet_threshold(monkeypatch):
    monkeypatch.setattr(
        "src.semantic_matcher.calculate_semantic_similarity",
        lambda candidate_text, job_text: 82.5,
    )

    result = match_semantic_requirements(
        "Python developer with machine learning experience",
        "Software developer requiring Python and machine learning",
    )

    assert result["score"] == 82.5
    assert result["threshold"] == 75.0
    assert result["meets_threshold"] is True


def test_semantic_requirements_do_not_meet_threshold(monkeypatch):
    monkeypatch.setattr(
        "src.semantic_matcher.calculate_semantic_similarity",
        lambda candidate_text, job_text: 62.0,
    )

    result = match_semantic_requirements(
        "Graphic design student",
        "Backend Python developer",
    )

    assert result["score"] == 62.0
    assert result["threshold"] == 75.0
    assert result["meets_threshold"] is False


def test_semantic_requirements_empty_text(monkeypatch):
    monkeypatch.setattr(
        "src.semantic_matcher.calculate_semantic_similarity",
        lambda candidate_text, job_text: 0.0,
    )

    result = match_semantic_requirements(
        "",
        "Python developer",
    )

    assert result["score"] == 0.0
    assert result["meets_threshold"] is False
