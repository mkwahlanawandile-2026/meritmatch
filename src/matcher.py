"""Match normalized candidate profiles against employer job requirements."""

from typing import Dict, List


def match_required_skills(
    candidate_skills: List[str],
    required_skills: List[str],
) -> Dict:
    """Compare candidate skills against mandatory employer skills."""

    candidate_set = {
        str(skill).strip().lower()
        for skill in candidate_skills
        if str(skill).strip()
    }

    required_set = {
        str(skill).strip().lower()
        for skill in required_skills
        if str(skill).strip()
    }

    matched = sorted(candidate_set & required_set)
    missing = sorted(required_set - candidate_set)

    total_required = len(required_set)

    if total_required == 0:
        score = 100.0
    else:
        score = round(
            (len(matched) / total_required) * 100,
            2,
        )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "required_skill_count": total_required,
        "matched_skill_count": len(matched),
        "score": score,
        "all_required_skills_met": len(missing) == 0,
    }


def match_preferred_skills(
    candidate_skills: List[str],
    preferred_skills: List[str],
) -> Dict:
    """Compare candidate skills against preferred employer skills."""

    candidate_set = {
        str(skill).strip().lower()
        for skill in candidate_skills
        if str(skill).strip()
    }

    preferred_set = {
        str(skill).strip().lower()
        for skill in preferred_skills
        if str(skill).strip()
    }

    matched = sorted(candidate_set & preferred_set)
    missing = sorted(preferred_set - candidate_set)

    total_preferred = len(preferred_set)

    if total_preferred == 0:
        score = 100.0
    else:
        score = round(
            (len(matched) / total_preferred) * 100,
            2,
        )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "preferred_skill_count": total_preferred,
        "matched_skill_count": len(matched),
        "score": score,
    }


def match_experience_requirement(
    candidate_experience_months: int,
    minimum_experience_months: int,
) -> Dict:
    """Compare candidate experience against the employer minimum."""

    try:
        candidate_months = max(
            int(candidate_experience_months),
            0,
        )
    except (TypeError, ValueError):
        candidate_months = 0

    try:
        minimum_months = max(
            int(minimum_experience_months),
            0,
        )
    except (TypeError, ValueError):
        minimum_months = 0

    meets_requirement = candidate_months >= minimum_months

    if minimum_months == 0:
        score = 100.0
    else:
        score = round(
            min(
                (candidate_months / minimum_months) * 100,
                100,
            ),
            2,
        )

    return {
        "candidate_experience_months": candidate_months,
        "minimum_required_months": minimum_months,
        "experience_difference_months": (
            candidate_months - minimum_months
        ),
        "meets_requirement": meets_requirement,
        "score": score,
    }


def match_education_requirements(
    candidate_education: List[str],
    required_education: List[str],
) -> Dict:
    """Compare candidate education against employer requirements."""

    candidate_entries = {
        " ".join(str(value).strip().lower().split())
        for value in candidate_education
        if str(value).strip()
    }

    required_entries = {
        " ".join(str(value).strip().lower().split())
        for value in required_education
        if str(value).strip()
    }

    if not required_entries:
        return {
            "matched_requirements": [],
            "missing_requirements": [],
            "required_count": 0,
            "matched_count": 0,
            "score": 100.0,
            "meets_requirement": True,
        }

    matched = []
    missing = []

    for requirement in sorted(required_entries):
        if any(
            requirement in candidate
            or candidate in requirement
            for candidate in candidate_entries
        ):
            matched.append(requirement)
        else:
            missing.append(requirement)

    score = round(
        (len(matched) / len(required_entries)) * 100,
        2,
    )

    return {
        "matched_requirements": matched,
        "missing_requirements": missing,
        "required_count": len(required_entries),
        "matched_count": len(matched),
        "score": score,
        "meets_requirement": len(missing) == 0,
    }


def match_certification_requirements(
    candidate_certifications: List[str],
    required_certifications: List[str],
) -> Dict:
    """Compare candidate certifications against employer requirements."""

    candidate_entries = {
        " ".join(str(value).strip().lower().split())
        for value in candidate_certifications
        if str(value).strip()
    }

    required_entries = {
        " ".join(str(value).strip().lower().split())
        for value in required_certifications
        if str(value).strip()
    }

    if not required_entries:
        return {
            "matched_certifications": [],
            "missing_certifications": [],
            "required_count": 0,
            "matched_count": 0,
            "score": 100.0,
            "meets_requirement": True,
        }

    matched = []
    missing = []

    for requirement in sorted(required_entries):
        if any(
            requirement in candidate
            or candidate in requirement
            for candidate in candidate_entries
        ):
            matched.append(requirement)
        else:
            missing.append(requirement)

    score = round(
        (len(matched) / len(required_entries)) * 100,
        2,
    )

    return {
        "matched_certifications": matched,
        "missing_certifications": missing,
        "required_count": len(required_entries),
        "matched_count": len(matched),
        "score": score,
        "meets_requirement": len(missing) == 0,
    }
