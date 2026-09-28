"""Define and normalize employer job requirements for MeritMatch."""

from typing import Dict, List, Optional

from src.nlp_parser import normalize_skills


def validate_job_requirements(job: Dict) -> Dict:
    """Validate the structure of an employer job requirement profile."""
    if not isinstance(job, dict):
        raise TypeError("Job requirements must be a dictionary.")

    validated = dict(job)

    # Core job information
    for field in (
        "job_title",
        "department",
        "description",
        "location",
        "work_arrangement",
        "employment_type",
        "terms_and_conditions",
    ):
        value = validated.get(field)

        if value is None:
            validated[field] = ""
        else:
            validated[field] = str(value).strip()

    # Collection fields
    for field in (
        "required_skills",
        "preferred_skills",
        "education_requirements",
        "certifications",
        "screening_questions",
    ):
        value = validated.get(field)

        if value is None:
            validated[field] = []
        elif not isinstance(value, list):
            validated[field] = [value]

    # Minimum experience
    minimum_experience = validated.get(
        "minimum_experience_months",
        0,
    )

    try:
        minimum_experience = int(minimum_experience)
    except (TypeError, ValueError):
        minimum_experience = 0

    validated["minimum_experience_months"] = max(
        minimum_experience,
        0,
    )

    return validated


def normalize_job_requirements(job: Dict) -> Dict:
    """Normalize an employer job requirement profile."""
    validated = validate_job_requirements(job)

    normalized = dict(validated)

    # Normalize text fields
    for field in (
        "job_title",
        "department",
        "description",
        "location",
        "work_arrangement",
        "employment_type",
        "terms_and_conditions",
    ):
        normalized[field] = " ".join(
            normalized.get(field, "").split()
        ).strip()

    # Normalize employer skills through the canonical taxonomy
    normalized["required_skills"] = normalize_skills(
        normalized.get("required_skills", [])
    )

    normalized["preferred_skills"] = normalize_skills(
        normalized.get("preferred_skills", [])
    )

    # Normalize other collection fields
    for field in (
        "education_requirements",
        "certifications",
        "screening_questions",
    ):
        values = normalized.get(field, [])

        cleaned_values = []

        for value in values:
            if value is None:
                continue

            value = " ".join(
                str(value).split()
            ).strip()

            if value:
                cleaned_values.append(value)

        normalized[field] = cleaned_values

    return normalized


def prepare_job_for_matching(job: Dict) -> Dict:
    """Prepare employer job requirements for candidate matching."""
    normalized = normalize_job_requirements(job)

    return {
        "job_title": normalized.get("job_title", ""),
        "department": normalized.get("department", ""),
        "description": normalized.get("description", ""),
        "required_skills": normalized.get(
            "required_skills",
            [],
        ),
        "preferred_skills": normalized.get(
            "preferred_skills",
            [],
        ),
        "minimum_experience_months": normalized.get(
            "minimum_experience_months",
            0,
        ),
        "education_requirements": normalized.get(
            "education_requirements",
            [],
        ),
        "certifications": normalized.get(
            "certifications",
            [],
        ),
        "location": normalized.get("location", ""),
        "work_arrangement": normalized.get(
            "work_arrangement",
            "",
        ),
        "employment_type": normalized.get(
            "employment_type",
            "",
        ),
        "screening_questions": normalized.get(
            "screening_questions",
            [],
        ),
        "terms_and_conditions": normalized.get(
            "terms_and_conditions",
            "",
        ),
    }
