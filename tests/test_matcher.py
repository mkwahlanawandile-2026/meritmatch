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
