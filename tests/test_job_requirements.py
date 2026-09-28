from src.job_requirements import (
    normalize_job_requirements,
    prepare_job_for_matching,
    validate_job_requirements,
)


def test_validate_job_requirements_defaults():
    job = validate_job_requirements({})

    assert job["job_title"] == ""
    assert job["required_skills"] == []
    assert job["preferred_skills"] == []
    assert job["minimum_experience_months"] == 0


def test_validate_job_requirements_normalizes_invalid_experience():
    job = validate_job_requirements({
        "job_title": "Software Developer",
        "minimum_experience_months": "24",
    })

    assert job["minimum_experience_months"] == 24


def test_normalize_job_requirements():
    job = {
        "job_title": "  Software Developer  ",
        "department": "  Information Technology ",
        "required_skills": [
            " Python ",
            " FastAPI ",
            None,
        ],
        "preferred_skills": [
            " Docker ",
        ],
        "education_requirements": [
            " BSc Computer Science ",
        ],
        "certifications": [
            " AWS Certified ",
        ],
        "minimum_experience_months": "24",
        "location": "  Alice, Eastern Cape ",
        "work_arrangement": " Hybrid ",
        "employment_type": " Full-time ",
    }

    normalized = normalize_job_requirements(job)

    assert normalized["job_title"] == "Software Developer"
    assert normalized["department"] == "Information Technology"
    assert normalized["required_skills"] == [
        "Python",
        "FastAPI",
    ]
    assert normalized["preferred_skills"] == ["Docker"]
    assert normalized["education_requirements"] == [
        "BSc Computer Science"
    ]
    assert normalized["certifications"] == [
        "AWS Certified"
    ]
    assert normalized["minimum_experience_months"] == 24
    assert normalized["location"] == "Alice, Eastern Cape"
    assert normalized["work_arrangement"] == "Hybrid"
    assert normalized["employment_type"] == "Full-time"


def test_prepare_job_for_matching():
    job = {
        "job_title": "Software Developer",
        "department": "Information Technology",
        "description": "Build and maintain software systems.",
        "required_skills": ["Python", "FastAPI"],
        "preferred_skills": ["Docker"],
        "minimum_experience_months": 24,
        "education_requirements": [
            "BSc Computer Science",
        ],
        "certifications": [
            "AWS Certified",
        ],
        "location": "Alice, Eastern Cape",
        "work_arrangement": "Hybrid",
        "employment_type": "Full-time",
        "screening_questions": [
            "Are you legally permitted to work in this location?"
        ],
        "terms_and_conditions": "Standard employer terms.",
    }

    prepared = prepare_job_for_matching(job)

    assert prepared["job_title"] == "Software Developer"
    assert prepared["required_skills"] == [
        "Python",
        "FastAPI",
    ]
    assert prepared["minimum_experience_months"] == 24
    assert prepared["work_arrangement"] == "Hybrid"
    assert prepared["employment_type"] == "Full-time"
    assert len(prepared["screening_questions"]) == 1


def test_normalize_job_requirements_uses_skill_taxonomy():
    job = {
        "job_title": "Software Developer",
        "required_skills": [
            "python",
            "PY",
            "javascript",
            "js",
            "postgres",
        ],
        "preferred_skills": [
            "ML",
            "sklearn",
            "docker",
        ],
    }

    normalized = normalize_job_requirements(job)

    assert normalized["required_skills"] == [
        "Python",
        "JavaScript",
        "PostgreSQL",
    ]

    assert normalized["preferred_skills"] == [
        "Machine Learning",
        "Scikit-learn",
        "Docker",
    ]
