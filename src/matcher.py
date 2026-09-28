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
