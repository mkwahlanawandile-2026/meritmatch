"""Match normalized candidate profiles against employer job requirements."""

from typing import Dict, List

from src.semantic_matcher import match_semantic_requirements


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


def match_candidate_to_job(
    candidate_profile: Dict,
    job_requirements: Dict,
) -> Dict:
    """Combine all candidate-to-job requirement matching results."""

    if not isinstance(candidate_profile, dict):
        raise TypeError("Candidate profile must be a dictionary.")

    if not isinstance(job_requirements, dict):
        raise TypeError("Job requirements must be a dictionary.")

    required_skills_result = match_required_skills(
        candidate_profile.get("skills", []),
        job_requirements.get("required_skills", []),
    )

    preferred_skills_result = match_preferred_skills(
        candidate_profile.get("skills", []),
        job_requirements.get("preferred_skills", []),
    )

    experience_result = match_experience_requirement(
        candidate_profile.get("total_experience_months", 0),
        job_requirements.get("minimum_experience_months", 0),
    )

    education_result = match_education_requirements(
        candidate_profile.get("education", []),
        job_requirements.get("education_requirements", []),
    )

    certification_result = match_certification_requirements(
        candidate_profile.get("certifications", []),
        job_requirements.get("certifications", []),
    )

    required_requirements_met = all(
        [
            required_skills_result["all_required_skills_met"],
            experience_result["meets_requirement"],
            education_result["meets_requirement"],
            certification_result["meets_requirement"],
        ]
    )

    component_scores = {
        "required_skills": required_skills_result["score"],
        "preferred_skills": preferred_skills_result["score"],
        "experience": experience_result["score"],
        "education": education_result["score"],
        "certifications": certification_result["score"],
    }

    candidate_semantic_text = " ".join(
        [
            str(candidate_profile.get("candidate_name", "")),
            " ".join(
                str(skill)
                for skill in candidate_profile.get("skills", [])
            ),
            " ".join(
                str(education)
                for education in candidate_profile.get("education", [])
            ),
            " ".join(
                str(certification)
                for certification in candidate_profile.get(
                    "certifications", []
                )
            ),
            " ".join(
                str(record.get("job_title", ""))
                for record in candidate_profile.get(
                    "experience_records", []
                )
                if isinstance(record, dict)
            ),
        ]
    ).strip()

    job_semantic_text = " ".join(
        [
            str(job_requirements.get("job_title", "")),
            str(job_requirements.get("department", "")),
            str(job_requirements.get("description", "")),
            " ".join(
                str(skill)
                for skill in job_requirements.get("required_skills", [])
            ),
            " ".join(
                str(skill)
                for skill in job_requirements.get("preferred_skills", [])
            ),
            " ".join(
                str(education)
                for education in job_requirements.get(
                    "education_requirements", []
                )
            ),
            " ".join(
                str(certification)
                for certification in job_requirements.get(
                    "certifications", []
                )
            ),
        ]
    ).strip()

    semantic_result = match_semantic_requirements(
        candidate_semantic_text,
        job_semantic_text,
    )

    scoring_result = calculate_overall_score(
        skills_score=required_skills_result["score"],
        experience_score=experience_result["score"],
        education_score=education_result["score"],
        semantic_score=semantic_result["score"],
    )

    return {
        "candidate_name": candidate_profile.get("candidate_name", ""),
        "job_title": job_requirements.get("job_title", ""),
        "required_requirements_met": required_requirements_met,
        "component_scores": component_scores,
        "scoring": scoring_result,
        "semantic": semantic_result,
        "required_skills": required_skills_result,
        "preferred_skills": preferred_skills_result,
        "experience": experience_result,
        "education": education_result,
        "certifications": certification_result,
    }


def calculate_overall_score(
    skills_score: float,
    experience_score: float,
    education_score: float,
    semantic_score: float,
) -> Dict:
    """Calculate the weighted overall candidate match score."""

    from config import WEIGHTS

    component_scores = {
        "skills": skills_score,
        "experience": experience_score,
        "education": education_score,
        "semantic": semantic_score,
    }

    normalized_scores = {}

    for component, score in component_scores.items():
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            numeric_score = 0.0

        normalized_scores[component] = min(
            max(numeric_score, 0.0),
            100.0,
        )

    weighted_scores = {
        component: round(
            normalized_scores[component] * WEIGHTS[component],
            2,
        )
        for component in WEIGHTS
    }

    overall_score = round(
        sum(weighted_scores.values()),
        2,
    )

    return {
        "overall_score": overall_score,
        "component_scores": normalized_scores,
        "weights": dict(WEIGHTS),
        "weighted_scores": weighted_scores,
    }
