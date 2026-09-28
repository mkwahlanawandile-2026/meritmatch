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

    # Semantic similarity is not implemented yet.
    assert result["scoring"]["component_scores"]["semantic"] == 0.0
