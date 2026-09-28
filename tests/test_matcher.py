from src.matcher import match_required_skills


def test_match_required_skills_all_met():
    result = match_required_skills(
        [
            "Python",
            "JavaScript",
            "PostgreSQL",
        ],
        [
            "Python",
            "PostgreSQL",
        ],
    )

    assert result["matched_skills"] == [
        "postgresql",
        "python",
    ]

    assert result["missing_skills"] == []

    assert result["required_skill_count"] == 2
    assert result["matched_skill_count"] == 2
    assert result["score"] == 100.0
    assert result["all_required_skills_met"] is True


def test_match_required_skills_partial_match():
    result = match_required_skills(
        [
            "Python",
            "JavaScript",
        ],
        [
            "Python",
            "PostgreSQL",
            "Docker",
        ],
    )

    assert result["matched_skills"] == [
        "python",
    ]

    assert result["missing_skills"] == [
        "docker",
        "postgresql",
    ]

    assert result["required_skill_count"] == 3
    assert result["matched_skill_count"] == 1
    assert result["score"] == 33.33
    assert result["all_required_skills_met"] is False


def test_match_required_skills_empty_requirements():
    result = match_required_skills(
        ["Python"],
        [],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["score"] == 100.0
    assert result["all_required_skills_met"] is True


def test_match_required_skills_empty_candidate():
    result = match_required_skills(
        [],
        ["Python", "SQL"],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == [
        "python",
        "sql",
    ]
    assert result["score"] == 0.0
    assert result["all_required_skills_met"] is False


def test_match_preferred_skills():
    from src.matcher import match_preferred_skills

    result = match_preferred_skills(
        [
            "Python",
            "Docker",
            "Git",
        ],
        [
            "Docker",
            "AWS",
            "Git",
        ],
    )

    assert result["matched_skills"] == [
        "docker",
        "git",
    ]

    assert result["missing_skills"] == [
        "aws",
    ]

    assert result["preferred_skill_count"] == 3
    assert result["matched_skill_count"] == 2
    assert result["score"] == 66.67


def test_match_preferred_skills_empty_requirements():
    from src.matcher import match_preferred_skills

    result = match_preferred_skills(
        ["Python"],
        [],
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["score"] == 100.0


def test_match_experience_requirement_met():
    from src.matcher import match_experience_requirement

    result = match_experience_requirement(
        39,
        24,
    )

    assert result["candidate_experience_months"] == 39
    assert result["minimum_required_months"] == 24
    assert result["experience_difference_months"] == 15
    assert result["meets_requirement"] is True
    assert result["score"] == 100.0


def test_match_experience_requirement_not_met():
    from src.matcher import match_experience_requirement

    result = match_experience_requirement(
        12,
        24,
    )

    assert result["candidate_experience_months"] == 12
    assert result["minimum_required_months"] == 24
    assert result["experience_difference_months"] == -12
    assert result["meets_requirement"] is False
    assert result["score"] == 50.0


def test_match_experience_requirement_no_minimum():
    from src.matcher import match_experience_requirement

    result = match_experience_requirement(
        12,
        0,
    )

    assert result["meets_requirement"] is True
    assert result["score"] == 100.0


def test_match_education_requirements_met():
    from src.matcher import match_education_requirements

    result = match_education_requirements(
        [
            "BSc Computer Science",
            "University of Example",
        ],
        [
            "BSc Computer Science",
        ],
    )

    assert result["matched_requirements"] == [
        "bsc computer science",
    ]
    assert result["missing_requirements"] == []
    assert result["required_count"] == 1
    assert result["matched_count"] == 1
    assert result["score"] == 100.0
    assert result["meets_requirement"] is True


def test_match_education_requirements_partial():
    from src.matcher import match_education_requirements

    result = match_education_requirements(
        [
            "BSc Computer Science",
        ],
        [
            "BSc Computer Science",
            "Honours Computer Science",
        ],
    )

    assert result["matched_requirements"] == [
        "bsc computer science",
    ]
    assert result["missing_requirements"] == [
        "honours computer science",
    ]
    assert result["score"] == 50.0
    assert result["meets_requirement"] is False


def test_match_education_requirements_empty():
    from src.matcher import match_education_requirements

    result = match_education_requirements(
        ["BSc Computer Science"],
        [],
    )

    assert result["matched_requirements"] == []
    assert result["missing_requirements"] == []
    assert result["score"] == 100.0
    assert result["meets_requirement"] is True


def test_match_certification_requirements_met():
    from src.matcher import match_certification_requirements

    result = match_certification_requirements(
        [
            "AWS Cloud Practitioner",
            "Microsoft Azure Fundamentals",
        ],
        [
            "AWS Cloud Practitioner",
        ],
    )

    assert result["matched_certifications"] == [
        "aws cloud practitioner",
    ]
    assert result["missing_certifications"] == []
    assert result["required_count"] == 1
    assert result["matched_count"] == 1
    assert result["score"] == 100.0
    assert result["meets_requirement"] is True


def test_match_certification_requirements_partial():
    from src.matcher import match_certification_requirements

    result = match_certification_requirements(
        [
            "AWS Cloud Practitioner",
        ],
        [
            "AWS Cloud Practitioner",
            "Cisco Certified Network Associate",
        ],
    )

    assert result["matched_certifications"] == [
        "aws cloud practitioner",
    ]
    assert result["missing_certifications"] == [
        "cisco certified network associate",
    ]
    assert result["score"] == 50.0
    assert result["meets_requirement"] is False


def test_match_certification_requirements_empty():
    from src.matcher import match_certification_requirements

    result = match_certification_requirements(
        ["AWS Cloud Practitioner"],
        [],
    )

    assert result["matched_certifications"] == []
    assert result["missing_certifications"] == []
    assert result["score"] == 100.0
    assert result["meets_requirement"] is True


def test_match_candidate_to_job_fully_matched():
    from src.matcher import match_candidate_to_job

    candidate = {
        "candidate_name": "Wandile",
        "skills": ["Python", "SQL", "Docker"],
        "total_experience_months": 36,
        "education": ["BSc Computer Science"],
        "certifications": ["AWS Certified Cloud Practitioner"],
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": ["Docker"],
        "minimum_experience_months": 24,
        "education_requirements": ["BSc Computer Science"],
        "certifications": ["AWS Certified Cloud Practitioner"],
    }

    result = match_candidate_to_job(candidate, job)

    assert result["candidate_name"] == "Wandile"
    assert result["job_title"] == "Python Developer"
    assert result["required_requirements_met"] is True
    assert result["required_skills"]["score"] == 100.0
    assert result["preferred_skills"]["score"] == 100.0
    assert result["experience"]["score"] == 100.0
    assert result["education"]["score"] == 100.0
    assert result["certifications"]["score"] == 100.0


def test_match_candidate_to_job_missing_required_requirement():
    from src.matcher import match_candidate_to_job

    candidate = {
        "candidate_name": "Candidate A",
        "skills": ["Python"],
        "total_experience_months": 12,
        "education": ["BSc Computer Science"],
        "certifications": [],
    }

    job = {
        "job_title": "Software Developer",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": ["Docker"],
        "minimum_experience_months": 24,
        "education_requirements": ["BSc Computer Science"],
        "certifications": [],
    }

    result = match_candidate_to_job(candidate, job)

    assert result["required_requirements_met"] is False
    assert "sql" in result["required_skills"]["missing_skills"]
    assert result["experience"]["meets_requirement"] is False
    assert result["education"]["meets_requirement"] is True
    assert result["certifications"]["meets_requirement"] is True


def test_match_candidate_to_job_returns_transparent_component_results():
    from src.matcher import match_candidate_to_job

    candidate = {
        "candidate_name": "Candidate B",
        "skills": ["Python"],
        "total_experience_months": 24,
        "education": [],
        "certifications": [],
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": ["Docker"],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
    }

    result = match_candidate_to_job(candidate, job)

    assert "required_skills" in result
    assert "preferred_skills" in result
    assert "experience" in result
    assert "education" in result
    assert "certifications" in result
    assert "component_scores" in result
    assert result["required_skills"]["all_required_skills_met"] is True


def test_calculate_overall_score_uses_configured_weights():
    from src.matcher import calculate_overall_score

    result = calculate_overall_score(
        skills_score=100,
        experience_score=100,
        education_score=100,
        semantic_score=100,
    )

    assert result["overall_score"] == 100.0
    assert result["weights"]["skills"] == 0.40
    assert result["weights"]["experience"] == 0.25
    assert result["weights"]["education"] == 0.15
    assert result["weights"]["semantic"] == 0.20


def test_calculate_overall_score_calculates_weighted_result():
    from src.matcher import calculate_overall_score

    result = calculate_overall_score(
        skills_score=80,
        experience_score=60,
        education_score=100,
        semantic_score=70,
    )

    expected = (
        (80 * 0.40)
        + (60 * 0.25)
        + (100 * 0.15)
        + (70 * 0.20)
    )

    assert result["overall_score"] == round(expected, 2)
    assert result["weighted_scores"]["skills"] == 32.0
    assert result["weighted_scores"]["experience"] == 15.0
    assert result["weighted_scores"]["education"] == 15.0
    assert result["weighted_scores"]["semantic"] == 14.0


def test_calculate_overall_score_clamps_invalid_ranges():
    from src.matcher import calculate_overall_score

    result = calculate_overall_score(
        skills_score=150,
        experience_score=-20,
        education_score="80",
        semantic_score="invalid",
    )

    assert result["component_scores"]["skills"] == 100.0
    assert result["component_scores"]["experience"] == 0.0
    assert result["component_scores"]["education"] == 80.0
    assert result["component_scores"]["semantic"] == 0.0


def test_match_candidate_to_job_includes_overall_scoring():
    from src.matcher import match_candidate_to_job

    candidate = {
        "candidate_name": "Candidate C",
        "skills": ["Python", "SQL"],
        "total_experience_months": 36,
        "education": ["BSc Computer Science"],
        "certifications": [],
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": ["BSc Computer Science"],
        "certifications": [],
    }

    result = match_candidate_to_job(candidate, job)

    assert "scoring" in result
    assert "overall_score" in result["scoring"]
    assert "weights" in result["scoring"]
    assert "weighted_scores" in result["scoring"]

    assert "semantic" in result
    assert "score" in result["semantic"]
    assert 0.0 <= result["semantic"]["score"] <= 100.0
    assert (
        result["scoring"]["component_scores"]["semantic"]
        == result["semantic"]["score"]
    )


def test_match_candidate_to_job_uses_semantic_score(monkeypatch):
    from src.matcher import match_candidate_to_job

    monkeypatch.setattr(
        "src.matcher.match_semantic_requirements",
        lambda candidate_text, job_text: {
            "score": 80.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    )

    candidate = {
        "candidate_name": "Candidate D",
        "skills": ["Python"],
        "total_experience_months": 24,
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [
            {
                "job_title": "Python Developer",
                "employer": "Example Ltd",
            }
        ],
    }

    job = {
        "job_title": "Python Developer",
        "department": "Software Engineering",
        "description": "Develop Python applications.",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": ["BSc Computer Science"],
        "certifications": [],
    }

    result = match_candidate_to_job(candidate, job)

    assert result["semantic"]["score"] == 80.0
    assert result["semantic"]["meets_threshold"] is True
    assert result["scoring"]["component_scores"]["semantic"] == 80.0
    assert result["scoring"]["weighted_scores"]["semantic"] == 16.0


def test_build_match_explanation_identifies_strengths_and_gaps():
    from src.matcher import build_match_explanation

    match_result = {
        "candidate_name": "Candidate E",
        "job_title": "Python Developer",
        "required_requirements_met": False,
        "required_skills": {
            "matched_skills": ["python"],
            "missing_skills": ["docker"],
        },
        "preferred_skills": {
            "matched_skills": ["sql"],
        },
        "experience": {
            "meets_requirement": True,
        },
        "education": {
            "meets_requirement": True,
        },
        "certifications": {
            "required_count": 0,
            "meets_requirement": True,
        },
        "semantic": {
            "score": 68.28,
            "threshold": 75.0,
        },
        "scoring": {
            "overall_score": 72.41,
            "component_scores": {
                "skills": 50.0,
                "experience": 100.0,
                "education": 100.0,
                "semantic": 68.28,
            },
            "weighted_scores": {
                "skills": 20.0,
                "experience": 25.0,
                "education": 15.0,
                "semantic": 13.66,
            },
        },
    }

    result = build_match_explanation(match_result)

    assert result["candidate_name"] == "Candidate E"
    assert result["overall_score"] == 72.41
    assert any("python" in item for item in result["strengths"])
    assert any("docker" in item for item in result["gaps"])
    assert any("Semantic similarity is below" in item for item in result["gaps"])


def test_build_match_explanation_reports_met_requirements():
    from src.matcher import build_match_explanation

    match_result = {
        "candidate_name": "Candidate F",
        "job_title": "Data Analyst",
        "required_requirements_met": True,
        "required_skills": {
            "matched_skills": ["python", "sql"],
            "missing_skills": [],
        },
        "preferred_skills": {
            "matched_skills": [],
        },
        "experience": {
            "meets_requirement": True,
        },
        "education": {
            "meets_requirement": True,
        },
        "certifications": {
            "required_count": 0,
            "meets_requirement": True,
        },
        "semantic": {
            "score": 85.0,
            "threshold": 75.0,
        },
        "scoring": {
            "overall_score": 91.0,
            "component_scores": {},
            "weighted_scores": {},
        },
    }

    result = build_match_explanation(match_result)

    assert result["required_requirements_met"] is True
    assert any("experience requirement is met" in item for item in result["strengths"])
    assert any("Education requirement is met" in item for item in result["strengths"])
    assert any("Semantic similarity meets" in item for item in result["strengths"])
    assert result["gaps"] == []
def test_validate_match_result_normalizes_scores():
    from src.matcher import validate_match_result

    result = {
        "required_requirements_met": 1,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {},
        "scoring": {
            "overall_score": 125,
            "component_scores": {
                "skills": 110,
                "experience": -10,
                "education": "invalid",
            },
            "weighted_scores": {
                "skills": 120,
            },
            "weights": {
                "skills": 0.40,
            },
        },
    }

    validated = validate_match_result(result)

    assert validated["scoring"]["overall_score"] == 100.0
    assert validated["scoring"]["component_scores"]["skills"] == 100.0
    assert validated["scoring"]["component_scores"]["experience"] == 0.0
    assert validated["scoring"]["component_scores"]["education"] == 0.0
    assert validated["scoring"]["weighted_scores"]["skills"] == 100.0
    assert validated["required_requirements_met"] is True


def test_validate_match_result_creates_missing_sections():
    from src.matcher import validate_match_result

    result = validate_match_result({
        "candidate_name": "Candidate G",
        "scoring": {},
    })

    assert result["required_skills"] == {}
    assert result["preferred_skills"] == {}
    assert result["experience"] == {}
    assert result["education"] == {}
    assert result["certifications"] == {}
    assert result["semantic"] == {}
    assert result["scoring"]["overall_score"] == 0.0
    assert result["scoring"]["component_scores"] == {}
    assert result["scoring"]["weighted_scores"] == {}
    assert result["scoring"]["weights"] == {}
    assert result["required_requirements_met"] is False

def test_validate_match_score_consistency_accepts_valid_scores():
    from src.matcher import validate_match_score_consistency

    result = {
        "scoring": {
            "component_scores": {
                "skills": 80.0,
                "experience": 100.0,
                "education": 100.0,
                "semantic": 70.0,
            },
            "weights": {
                "skills": 0.40,
                "experience": 0.25,
                "education": 0.15,
                "semantic": 0.20,
            },
            "weighted_scores": {
                "skills": 32.0,
                "experience": 25.0,
                "education": 15.0,
                "semantic": 14.0,
            },
            "overall_score": 86.0,
        }
    }

    validation = validate_match_score_consistency(result)

    assert validation["is_consistent"] is True
    assert validation["issues"] == []
    assert validation["calculated_overall_score"] == 86.0


def test_validate_match_score_consistency_detects_mismatch():
    from src.matcher import validate_match_score_consistency

    result = {
        "scoring": {
            "component_scores": {
                "skills": 80.0,
                "experience": 100.0,
                "education": 100.0,
                "semantic": 70.0,
            },
            "weights": {
                "skills": 0.40,
                "experience": 0.25,
                "education": 0.15,
                "semantic": 0.20,
            },
            "weighted_scores": {
                "skills": 40.0,
                "experience": 25.0,
                "education": 15.0,
                "semantic": 14.0,
            },
            "overall_score": 94.0,
        }
    }

    validation = validate_match_score_consistency(result)

    assert validation["is_consistent"] is False
    assert validation["issues"]
    assert any(
        "Weighted score mismatch" in issue
        for issue in validation["issues"]
    )
    assert "Overall score does not match weighted scores." in validation["issues"]

def test_determine_match_decision_qualifies_candidate():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate H",
        "job_title": "Software Developer",
        "required_requirements_met": True,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
        },
        "scoring": {
            "overall_score": 86.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(result)

    assert decision["decision"] == "QUALIFIED"
    assert decision["eligible"] is True
    assert decision["overall_score"] == 86.0
    assert any(
        "satisfies all configured decision rules" in reason
        for reason in decision["reasons"]
    )


def test_determine_match_decision_rejects_missing_requirements():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate I",
        "job_title": "Data Analyst",
        "required_requirements_met": False,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 82.0,
            "threshold": 75.0,
            "meets_threshold": True,
        },
        "scoring": {
            "overall_score": 82.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(result)

    assert decision["decision"] == "NOT_QUALIFIED"
    assert decision["eligible"] is False
    assert any(
        "mandatory job requirements" in reason
        for reason in decision["reasons"]
    )


def test_determine_match_decision_rejects_low_semantic_similarity():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate J",
        "job_title": "Python Developer",
        "required_requirements_met": True,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 68.0,
            "threshold": 75.0,
            "meets_threshold": False,
        },
        "scoring": {
            "overall_score": 78.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(result)

    assert decision["decision"] == "NOT_QUALIFIED"
    assert decision["eligible"] is False
    assert any(
        "Semantic similarity" in reason
        for reason in decision["reasons"]
    )

def test_determine_match_decision_uses_custom_score_threshold():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate K",
        "job_title": "Software Developer",
        "required_requirements_met": True,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
        },
        "scoring": {
            "overall_score": 72.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(
        result,
        {
            "min_overall_score": 70.0,
        },
    )

    assert decision["decision"] == "QUALIFIED"
    assert decision["eligible"] is True
    assert decision["minimum_overall_score"] == 70.0


def test_determine_match_decision_rejects_custom_score_threshold():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate L",
        "job_title": "Data Analyst",
        "required_requirements_met": True,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
        },
        "scoring": {
            "overall_score": 72.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(
        result,
        {
            "min_overall_score": 80.0,
        },
    )

    assert decision["decision"] == "NOT_QUALIFIED"
    assert decision["eligible"] is False
    assert decision["minimum_overall_score"] == 80.0
    assert any(
        "80.00%" in reason
        for reason in decision["reasons"]
    )


def test_determine_match_decision_can_disable_optional_rules():
    from src.matcher import determine_match_decision

    result = {
        "candidate_name": "Candidate M",
        "job_title": "Developer",
        "required_requirements_met": False,
        "required_skills": {},
        "preferred_skills": {},
        "experience": {},
        "education": {},
        "certifications": {},
        "semantic": {
            "score": 60.0,
            "threshold": 75.0,
            "meets_threshold": False,
        },
        "scoring": {
            "overall_score": 90.0,
            "component_scores": {},
            "weighted_scores": {},
            "weights": {},
        },
    }

    decision = determine_match_decision(
        result,
        {
            "min_overall_score": 80.0,
            "require_mandatory_requirements": False,
            "require_semantic_threshold": False,
        },
    )

    assert decision["decision"] == "QUALIFIED"
    assert decision["eligible"] is True
    assert decision["overall_score"] == 90.0

def test_match_candidate_to_job_uses_job_decision_rules():
    from unittest.mock import patch

    from src.matcher import match_candidate_to_job

    candidate = {
        "candidate_name": "Candidate N",
        "skills": ["Python"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "total_experience_months": 48,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 99.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value={
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    ):
        result = match_candidate_to_job(candidate, job)

    assert result["decision_rules"]["min_overall_score"] == 99.0
    assert result["decision"]["decision"] == "NOT_QUALIFIED"
    assert result["decision"]["eligible"] is False
    assert result["decision"]["minimum_overall_score"] == 99.0



def test_run_matching_pipeline_returns_complete_result():
    from unittest.mock import patch
    from src.matcher import run_matching_pipeline

    candidate = {
        "name": "Candidate O",
        "email": "candidate@example.com",
        "skills": ["python", "sql"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 48,
    }

    job = {
        "job_title": "Python Developer",
        "department": "Engineering",
        "description": "Develop Python applications.",
        "required_skills": ["Python"],
        "preferred_skills": ["SQL"],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value={
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    ):
        result = run_matching_pipeline(candidate, job)

    assert result["candidate_name"] == "Candidate O"
    assert result["job_title"] == "Python Developer"
    assert "required_skills" in result
    assert "experience" in result
    assert "education" in result
    assert "certifications" in result
    assert "semantic" in result
    assert "scoring" in result
    assert "score_consistency" in result
    assert result["score_consistency"]["is_consistent"] is True


def test_run_matching_pipeline_applies_employer_decision_rules():
    from unittest.mock import patch
    from src.matcher import run_matching_pipeline

    candidate = {
        "name": "Candidate P",
        "skills": ["python"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 48,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 99.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value={
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    ):
        result = run_matching_pipeline(candidate, job)

    assert result["decision_rules"]["min_overall_score"] == 99.0
    assert result["decision"]["decision"] == "NOT_QUALIFIED"
    assert result["decision"]["eligible"] is False


def test_run_matching_pipeline_includes_explanation():
    from unittest.mock import patch
    from src.matcher import run_matching_pipeline

    candidate = {
        "name": "Candidate Q",
        "skills": ["python", "sql"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 48,
    }

    job = {
        "job_title": "Python Developer",
        "description": "Develop Python applications.",
        "required_skills": ["Python"],
        "preferred_skills": ["SQL"],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value={
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    ):
        result = run_matching_pipeline(candidate, job)

    assert "explanation" in result
    assert isinstance(result["explanation"], dict)
    assert "strengths" in result["explanation"]
    assert "gaps" in result["explanation"]


def test_run_matching_pipeline_builds_final_result_structure():
    from unittest.mock import patch
    from src.matcher import run_matching_pipeline

    candidate = {
        "name": "Candidate R",
        "skills": ["python"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 48,
    }

    job = {
        "job_title": "Python Developer",
        "description": "Develop Python applications.",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value={
            "score": 85.0,
            "threshold": 75.0,
            "meets_threshold": True,
            "model": "test-model",
        },
    ):
        result = run_matching_pipeline(candidate, job)

    final_result = result["final_result"]

    assert final_result["candidate"]["name"] == "Candidate R"
    assert final_result["job"]["title"] == "Python Developer"
    assert "overall_score" in final_result["score"]
    assert "mandatory_met" in final_result["requirements"]
    assert "decision" in final_result["decision"]
    assert "strengths" in final_result["explanation"]
    assert "score_consistency" in final_result
    assert "min_overall_score" in final_result["decision_rules"]


def test_rank_candidates_for_job_orders_by_overall_score():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "Candidate Low",
            "skills": ["python"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 24,
        },
        {
            "name": "Candidate High",
            "skills": ["python", "sql"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 60,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            candidates,
            job,
        )

    assert len(results) == 2
    assert results[0]["candidate_name"] == "Candidate High"
    assert results[1]["candidate_name"] == "Candidate Low"
    assert (
        results[0]["scoring"]["overall_score"]
        >= results[1]["scoring"]["overall_score"]
    )



def test_rank_candidates_for_job_adds_rank_positions():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "Candidate One",
            "skills": ["python", "sql"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 60,
        },
        {
            "name": "Candidate Two",
            "skills": ["python"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 24,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            candidates,
            job,
        )

    assert [result["rank"] for result in results] == [1, 2]


def test_rank_candidates_for_job_prioritizes_qualified_candidates():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "High Score",
            "skills": ["python"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2025-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 12,
        },
        {
            "name": "Qualified Candidate",
            "skills": ["python"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2021-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 60,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            candidates,
            job,
        )

    assert results[0]["candidate_name"] == "Qualified Candidate"
    assert results[0]["decision"]["eligible"] is True
    assert results[1]["rank"] == 2


def test_rank_candidates_for_job_handles_empty_candidate_list():
    from src.matcher import rank_candidates_for_job

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
    }

    results = rank_candidates_for_job([], job)

    assert results == []


def test_rank_candidates_for_job_handles_single_candidate():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidate = {
        "name": "Solo Candidate",
        "skills": ["python"],
        "education": ["BSc Computer Science"],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 0,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job([candidate], job)

    assert len(results) == 1
    assert results[0]["candidate_name"] == "Solo Candidate"
    assert results[0]["rank"] == 1


def test_rank_candidates_for_job_uses_name_as_deterministic_tie_breaker():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "Zane Candidate",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
        {
            "name": "Alice Candidate",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(candidates, job)

    assert results[0]["candidate_name"] == "Alice Candidate"
    assert results[1]["candidate_name"] == "Zane Candidate"
    assert [result["rank"] for result in results] == [1, 2]


def test_rank_candidates_for_job_keeps_qualified_candidates_before_unqualified():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "Unqualified High Score",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
        {
            "name": "Qualified Candidate",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(candidates, job)

    assert len(results) == 2
    assert all("rank" in result for result in results)


def test_build_ranking_summary_returns_clean_ranked_output():
    from src.matcher import build_ranking_summary

    result = {
        "rank": 1,
        "candidate_name": "Alice Candidate",
        "job_title": "Python Developer",
        "required_requirements_met": True,
        "scoring": {
            "overall_score": 86.5,
            "skills_score": 90.0,
            "experience_score": 80.0,
            "education_score": 85.0,
            "semantic_score": 88.0,
        },
        "decision": {
            "decision": "QUALIFIED",
            "eligible": True,
        },
        "explanation": {
            "strengths": [
                "Required Python skill matched.",
            ],
            "gaps": [
                "Preferred Docker skill missing.",
            ],
        },
    }

    summary = build_ranking_summary(result)

    assert summary["rank"] == 1
    assert summary["candidate_name"] == "Alice Candidate"
    assert summary["job_title"] == "Python Developer"
    assert summary["overall_score"] == 86.5
    assert summary["decision"] == "QUALIFIED"
    assert summary["eligible"] is True
    assert summary["required_requirements_met"] is True
    assert summary["strengths"] == [
        "Required Python skill matched.",
    ]
    assert summary["gaps"] == [
        "Preferred Docker skill missing.",
    ]
    assert summary["score_breakdown"]["skills"] == 90.0
    assert summary["score_breakdown"]["experience"] == 80.0
    assert summary["score_breakdown"]["education"] == 85.0
    assert summary["score_breakdown"]["semantic"] == 88.0


def test_build_ranking_summary_handles_missing_explanation_data():
    from src.matcher import build_ranking_summary

    result = {
        "rank": 2,
        "candidate_name": "Bob Candidate",
        "job_title": "Data Analyst",
        "scoring": {
            "overall_score": 72.0,
        },
        "decision": {
            "decision": "NOT_QUALIFIED",
            "eligible": False,
        },
        "required_requirements_met": False,
    }

    summary = build_ranking_summary(result)

    assert summary["rank"] == 2
    assert summary["candidate_name"] == "Bob Candidate"
    assert summary["overall_score"] == 72.0
    assert summary["decision"] == "NOT_QUALIFIED"
    assert summary["eligible"] is False
    assert summary["strengths"] == []
    assert summary["gaps"] == []
    assert summary["score_breakdown"]["skills"] == 0.0
    assert summary["score_breakdown"]["experience"] == 0.0
    assert summary["score_breakdown"]["education"] == 0.0
    assert summary["score_breakdown"]["semantic"] == 0.0


def test_rank_candidates_for_job_attaches_ranking_summary():
    from unittest.mock import patch
    from src.matcher import rank_candidates_for_job

    candidate = {
        "name": "Summary Candidate",
        "skills": ["python"],
        "education": [],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 0,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            [candidate],
            job,
        )

    assert len(results) == 1

    result = results[0]

    assert "ranking_summary" in result
    assert result["ranking_summary"]["rank"] == 1
    assert result["ranking_summary"]["candidate_name"] == "Summary Candidate"
    assert result["ranking_summary"]["job_title"] == "Python Developer"
    assert (
        result["ranking_summary"]["overall_score"]
        == result["scoring"]["overall_score"]
    )
    assert (
        result["ranking_summary"]["eligible"]
        == result["decision"]["eligible"]
    )


def test_validate_ranking_summary_accepts_valid_summary():
    from src.matcher import validate_ranking_summary

    summary = {
        "rank": 1,
        "candidate_name": "Alice Candidate",
        "job_title": "Python Developer",
        "overall_score": 86.5,
        "decision": "QUALIFIED",
        "eligible": True,
        "required_requirements_met": True,
        "strengths": ["Python skill matched."],
        "gaps": [],
        "score_breakdown": {
            "skills": 90.0,
            "experience": 80.0,
            "education": 85.0,
            "semantic": 88.0,
        },
    }

    result = validate_ranking_summary(summary)

    assert result["valid"] is True
    assert result["missing_fields"] == []
    assert result["message"] == "Ranking summary contract is valid."


def test_validate_ranking_summary_rejects_missing_field():
    import pytest
    from src.matcher import validate_ranking_summary

    summary = {
        "rank": 1,
        "candidate_name": "Alice Candidate",
        "job_title": "Python Developer",
        "overall_score": 86.5,
        "decision": "QUALIFIED",
        "eligible": True,
        "required_requirements_met": True,
        "strengths": [],
        "gaps": [],
    }

    with pytest.raises(ValueError, match="missing fields"):
        validate_ranking_summary(summary)


def test_validate_ranking_summary_rejects_invalid_score_type():
    import pytest
    from src.matcher import validate_ranking_summary

    summary = {
        "rank": 1,
        "candidate_name": "Alice Candidate",
        "job_title": "Python Developer",
        "overall_score": "86.5",
        "decision": "QUALIFIED",
        "eligible": True,
        "required_requirements_met": True,
        "strengths": [],
        "gaps": [],
        "score_breakdown": {
            "skills": 90.0,
            "experience": 80.0,
            "education": 85.0,
            "semantic": 88.0,
        },
    }

    with pytest.raises(TypeError, match="Overall score"):
        validate_ranking_summary(summary)


def test_rank_candidates_for_job_produces_valid_api_ready_summary():
    from unittest.mock import patch
    from src.matcher import (
        rank_candidates_for_job,
        validate_ranking_summary,
    )

    candidate = {
        "name": "API Candidate",
        "skills": ["python"],
        "education": [],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 0,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            [candidate],
            job,
        )

    summary = results[0]["ranking_summary"]
    validation = validate_ranking_summary(summary)

    assert validation["valid"] is True
    assert summary["rank"] == 1
    assert summary["candidate_name"] == "API Candidate"
    assert isinstance(summary["overall_score"], (int, float))


def test_rank_candidates_for_job_validates_complete_batch():
    from unittest.mock import patch

    from src.matcher import (
        rank_candidates_for_job,
        validate_ranking_summary,
    )

    candidates = [
        {
            "name": "Charlie Candidate",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2024-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 24,
        },
        {
            "name": "Alice Candidate",
            "skills": ["python"],
            "education": [],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2020-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 72,
        },
        {
            "name": "Bob Candidate",
            "skills": [],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            candidates,
            job,
        )

    assert len(results) == 3

    # Qualified candidates must appear before the unqualified candidate.
    assert results[0]["decision"]["eligible"] is True
    assert results[1]["decision"]["eligible"] is True
    assert results[2]["decision"]["eligible"] is False

    # Every candidate receives a unique sequential rank.
    assert [result["rank"] for result in results] == [1, 2, 3]

    assert len(
        {result["rank"] for result in results}
    ) == 3

    # Every ranking summary must satisfy the API contract.
    for result in results:
        summary = result["ranking_summary"]

        validation = validate_ranking_summary(summary)

        assert validation["valid"] is True
        assert summary["rank"] == result["rank"]
        assert (
            summary["candidate_name"]
            == result["candidate_name"]
        )
        assert (
            summary["overall_score"]
            == result["scoring"]["overall_score"]
        )


def test_rank_candidates_for_job_completes_end_to_end_pipeline():
    from unittest.mock import patch

    from src.matcher import (
        rank_candidates_for_job,
        validate_ranking_summary,
    )

    candidates = [
        {
            "name": "Senior Python Candidate",
            "skills": ["Python", "SQL"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2020-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 72,
        },
        {
            "name": "Junior Python Candidate",
            "skills": ["Python"],
            "education": ["BSc Computer Science"],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2025-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 12,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "department": "Engineering",
        "description": (
            "Develop and maintain Python applications "
            "and data-processing services."
        ),
        "required_skills": ["Python"],
        "preferred_skills": ["SQL"],
        "minimum_experience_months": 24,
        "education_requirements": ["BSc Computer Science"],
        "certifications": [],
        "location": "Remote",
        "work_arrangement": "Remote",
        "employment_type": "Full-time",
        "terms_and_conditions": "Standard employment terms.",
        "decision_rules": {
            "min_overall_score": 70.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(
            candidates,
            job,
        )

    assert len(results) == 2

    # The complete pipeline must produce ranking metadata.
    assert [result["rank"] for result in results] == [1, 2]

    # The candidate meeting the mandatory experience requirement
    # must be qualified.
    assert results[0]["candidate_name"] == (
        "Senior Python Candidate"
    )
    assert results[0]["decision"]["eligible"] is True

    # The junior candidate must fail the mandatory experience
    # requirement.
    assert results[1]["candidate_name"] == (
        "Junior Python Candidate"
    )
    assert results[1]["decision"]["eligible"] is False

    for result in results:
        assert "explanation" in result
        assert "score_consistency" in result
        assert "final_result" in result
        assert "ranking_summary" in result

        summary = result["ranking_summary"]

        validation = validate_ranking_summary(summary)

        assert validation["valid"] is True
        assert summary["rank"] == result["rank"]
        assert summary["candidate_name"] == result[
            "candidate_name"
        ]
        assert summary["job_title"] == result["job_title"]
        assert summary["overall_score"] == result[
            "scoring"
        ]["overall_score"]


def test_rank_candidates_for_job_regression_qualified_first():
    from unittest.mock import patch

    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "High Score Unqualified",
            "skills": [],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
        {
            "name": "Qualified Candidate",
            "skills": ["Python"],
            "education": [],
            "certifications": [],
            "experience_records": [
                {
                    "start_date": "2020-01",
                    "end_date": "2026-01",
                }
            ],
            "total_experience_months": 72,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 24,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(candidates, job)

    assert results[0]["decision"]["eligible"] is True
    assert results[1]["decision"]["eligible"] is False
    assert results[0]["rank"] == 1
    assert results[1]["rank"] == 2


def test_rank_candidates_for_job_regression_ranks_are_sequential():
    from unittest.mock import patch

    from src.matcher import rank_candidates_for_job

    candidates = [
        {
            "name": "Candidate A",
            "skills": ["Python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
        {
            "name": "Candidate B",
            "skills": ["Python"],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
        {
            "name": "Candidate C",
            "skills": [],
            "education": [],
            "certifications": [],
            "experience_records": [],
            "total_experience_months": 0,
        },
    ]

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job(candidates, job)

    assert [result["rank"] for result in results] == [1, 2, 3]
    assert len(
        {result["rank"] for result in results}
    ) == 3


def test_rank_candidates_for_job_regression_summary_matches_result():
    from unittest.mock import patch

    from src.matcher import (
        rank_candidates_for_job,
        validate_ranking_summary,
    )

    candidate = {
        "name": "Regression Candidate",
        "skills": ["Python"],
        "education": [],
        "certifications": [],
        "experience_records": [],
        "total_experience_months": 0,
    }

    job = {
        "job_title": "Python Developer",
        "required_skills": ["Python"],
        "preferred_skills": [],
        "minimum_experience_months": 0,
        "education_requirements": [],
        "certifications": [],
        "decision_rules": {
            "min_overall_score": 0.0,
            "require_mandatory_requirements": True,
            "require_semantic_threshold": False,
        },
    }

    semantic_result = {
        "score": 85.0,
        "threshold": 75.0,
        "meets_threshold": True,
        "model": "test-model",
    }

    with patch(
        "src.matcher.match_semantic_requirements",
        return_value=semantic_result,
    ):
        results = rank_candidates_for_job([candidate], job)

    result = results[0]
    summary = result["ranking_summary"]

    assert validate_ranking_summary(summary)["valid"] is True
    assert summary["rank"] == result["rank"]
    assert summary["candidate_name"] == result["candidate_name"]
    assert summary["overall_score"] == result[
        "scoring"
    ]["overall_score"]
    assert summary["eligible"] == result[
        "decision"
    ]["eligible"]
