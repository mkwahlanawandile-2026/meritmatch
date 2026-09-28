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

    result = {
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
        "decision_rules": job_requirements.get(
            "decision_rules",
            {},
        ),
    }

    result["decision"] = determine_match_decision(
        result,
        result["decision_rules"],
    )

    return result


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


def build_match_explanation(match_result: Dict) -> Dict:
    """Build a human-readable explanation of a candidate match."""

    if not isinstance(match_result, dict):
        raise TypeError("Match result must be a dictionary.")

    required_skills = match_result.get("required_skills", {})
    preferred_skills = match_result.get("preferred_skills", {})
    experience = match_result.get("experience", {})
    education = match_result.get("education", {})
    certifications = match_result.get("certifications", {})
    semantic = match_result.get("semantic", {})
    scoring = match_result.get("scoring", {})

    strengths = []
    gaps = []

    matched_skills = required_skills.get("matched_skills", [])
    missing_skills = required_skills.get("missing_skills", [])

    if matched_skills:
        strengths.append(
            f"Matched required skills: {', '.join(matched_skills)}"
        )

    if missing_skills:
        gaps.append(
            f"Missing required skills: {', '.join(missing_skills)}"
        )

    preferred_matched = preferred_skills.get("matched_skills", [])

    if preferred_matched:
        strengths.append(
            f"Matched preferred skills: {', '.join(preferred_matched)}"
        )

    if experience.get("meets_requirement"):
        strengths.append("Minimum experience requirement is met.")
    else:
        gaps.append(
            "Minimum experience requirement is not met."
        )

    if education.get("meets_requirement"):
        strengths.append("Education requirement is met.")
    elif education.get("missing_requirements"):
        gaps.append(
            "Missing education: "
            + ", ".join(education["missing_requirements"])
        )

    if certifications.get("meets_requirement"):
        if certifications.get("required_count", 0) > 0:
            strengths.append("Certification requirements are met.")
    elif certifications.get("missing_certifications"):
        gaps.append(
            "Missing certifications: "
            + ", ".join(certifications["missing_certifications"])
        )

    semantic_score = semantic.get("score", 0.0)
    semantic_threshold = semantic.get("threshold", 75.0)

    if semantic_score >= semantic_threshold:
        strengths.append(
            f"Semantic similarity meets the {semantic_threshold:.0f}% threshold."
        )
    else:
        gaps.append(
            f"Semantic similarity is below the {semantic_threshold:.0f}% threshold."
        )

    return {
        "candidate_name": match_result.get("candidate_name", ""),
        "job_title": match_result.get("job_title", ""),
        "overall_score": scoring.get("overall_score", 0.0),
        "required_requirements_met": match_result.get(
            "required_requirements_met",
            False,
        ),
        "strengths": strengths,
        "gaps": gaps,
        "component_scores": scoring.get("component_scores", {}),
        "weighted_scores": scoring.get("weighted_scores", {}),
    }

def validate_match_result(match_result: Dict) -> Dict:
    """Validate and normalize a candidate-to-job match result."""

    if not isinstance(match_result, dict):
        raise TypeError("Match result must be a dictionary.")

    validated = dict(match_result)

    required_sections = (
        "required_skills",
        "preferred_skills",
        "experience",
        "education",
        "certifications",
        "semantic",
        "scoring",
    )

    for section in required_sections:
        if not isinstance(validated.get(section), dict):
            validated[section] = {}

    scoring = validated["scoring"]

    overall_score = scoring.get("overall_score", 0.0)
    try:
        overall_score = float(overall_score)
    except (TypeError, ValueError):
        overall_score = 0.0

    scoring["overall_score"] = min(
        max(overall_score, 0.0),
        100.0,
    )

    component_scores = scoring.get("component_scores", {})
    if not isinstance(component_scores, dict):
        component_scores = {}

    normalized_component_scores = {}

    for component, score in component_scores.items():
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            numeric_score = 0.0

        normalized_component_scores[component] = min(
            max(numeric_score, 0.0),
            100.0,
        )

    scoring["component_scores"] = normalized_component_scores

    weighted_scores = scoring.get("weighted_scores", {})
    if not isinstance(weighted_scores, dict):
        weighted_scores = {}

    normalized_weighted_scores = {}

    for component, score in weighted_scores.items():
        try:
            numeric_score = float(score)
        except (TypeError, ValueError):
            numeric_score = 0.0

        normalized_weighted_scores[component] = min(
            max(numeric_score, 0.0),
            100.0,
        )

    scoring["weighted_scores"] = normalized_weighted_scores

    weights = scoring.get("weights", {})
    if not isinstance(weights, dict):
        weights = {}

    scoring["weights"] = weights

    validated["required_requirements_met"] = bool(
        validated.get("required_requirements_met", False)
    )

    return validated

def validate_match_score_consistency(match_result: Dict) -> Dict:
    """Check whether weighted scores and overall score are consistent."""

    if not isinstance(match_result, dict):
        raise TypeError("Match result must be a dictionary.")

    scoring = match_result.get("scoring", {})

    if not isinstance(scoring, dict):
        return {
            "is_consistent": False,
            "issues": ["Scoring data is missing or invalid."],
        }

    component_scores = scoring.get("component_scores", {})
    weighted_scores = scoring.get("weighted_scores", {})
    weights = scoring.get("weights", {})
    overall_score = scoring.get("overall_score", 0.0)

    issues = []

    if not isinstance(component_scores, dict):
        issues.append("Component scores are invalid.")
        component_scores = {}

    if not isinstance(weighted_scores, dict):
        issues.append("Weighted scores are invalid.")
        weighted_scores = {}

    if not isinstance(weights, dict):
        issues.append("Scoring weights are invalid.")
        weights = {}

    try:
        reported_overall = float(overall_score)
    except (TypeError, ValueError):
        reported_overall = 0.0
        issues.append("Overall score is invalid.")

    calculated_weighted_scores = {}

    for component, weight in weights.items():
        try:
            numeric_score = float(component_scores.get(component, 0.0))
            numeric_weight = float(weight)
        except (TypeError, ValueError):
            issues.append(
                f"Invalid score or weight for component: {component}."
            )
            continue

        calculated_weighted_scores[component] = round(
            numeric_score * numeric_weight,
            2,
        )

    calculated_overall = round(
        sum(calculated_weighted_scores.values()),
        2,
    )

    for component, calculated_score in calculated_weighted_scores.items():
        try:
            reported_score = float(
                weighted_scores.get(component, 0.0)
            )
        except (TypeError, ValueError):
            issues.append(
                f"Invalid weighted score for component: {component}."
            )
            continue

        if abs(reported_score - calculated_score) > 0.01:
            issues.append(
                f"Weighted score mismatch for component: {component}."
            )

    if abs(reported_overall - calculated_overall) > 0.01:
        issues.append("Overall score does not match weighted scores.")

    return {
        "is_consistent": not issues,
        "issues": issues,
        "calculated_weighted_scores": calculated_weighted_scores,
        "calculated_overall_score": calculated_overall,
    }

def determine_match_decision(
    match_result: Dict,
    decision_rules: Dict = None,
) -> Dict:
    """Determine candidate eligibility using configurable decision rules."""

    if not isinstance(match_result, dict):
        raise TypeError("Match result must be a dictionary.")

    validated = validate_match_result(match_result)

    from config import (
        DECISION_MIN_OVERALL_SCORE,
        DECISION_REQUIRE_MANDATORY_REQUIREMENTS,
        DECISION_REQUIRE_SEMANTIC_THRESHOLD,
    )

    rules = {
        "min_overall_score": DECISION_MIN_OVERALL_SCORE,
        "require_mandatory_requirements": (
            DECISION_REQUIRE_MANDATORY_REQUIREMENTS
        ),
        "require_semantic_threshold": (
            DECISION_REQUIRE_SEMANTIC_THRESHOLD
        ),
    }

    if decision_rules is not None:
        if not isinstance(decision_rules, dict):
            raise TypeError("Decision rules must be a dictionary.")

        rules.update(decision_rules)

    try:
        min_overall_score = float(rules["min_overall_score"])
    except (TypeError, ValueError):
        min_overall_score = DECISION_MIN_OVERALL_SCORE

    min_overall_score = min(
        max(min_overall_score, 0.0),
        100.0,
    )

    require_mandatory = bool(
        rules["require_mandatory_requirements"]
    )

    require_semantic = bool(
        rules["require_semantic_threshold"]
    )

    required_requirements_met = validated.get(
        "required_requirements_met",
        False,
    )

    scoring = validated.get("scoring", {})
    overall_score = scoring.get("overall_score", 0.0)

    try:
        overall_score = float(overall_score)
    except (TypeError, ValueError):
        overall_score = 0.0

    semantic = validated.get("semantic", {})
    semantic_meets_threshold = semantic.get(
        "meets_threshold",
        False,
    )

    reasons = []
    eligible = True

    if require_mandatory and not required_requirements_met:
        eligible = False
        reasons.append(
            "One or more mandatory job requirements are not met."
        )

    if require_semantic and not semantic_meets_threshold:
        eligible = False
        reasons.append(
            "Semantic similarity is below the configured threshold."
        )

    if overall_score < min_overall_score:
        eligible = False
        reasons.append(
            f"Overall score is below the required "
            f"{min_overall_score:.2f}% threshold."
        )

    if eligible:
        decision = "QUALIFIED"
        reasons.append(
            "The candidate satisfies all configured decision rules."
        )
    else:
        decision = "NOT_QUALIFIED"

    return {
        "decision": decision,
        "eligible": eligible,
        "overall_score": overall_score,
        "minimum_overall_score": min_overall_score,
        "rules": rules,
        "reasons": reasons,
    }


def run_matching_pipeline(
    candidate_profile: Dict,
    job_requirements: Dict,
) -> Dict:
    """Run the complete candidate-to-job matching pipeline."""

    if not isinstance(candidate_profile, dict):
        raise TypeError("Candidate profile must be a dictionary.")

    if not isinstance(job_requirements, dict):
        raise TypeError("Job requirements must be a dictionary.")

    from src.nlp_parser import prepare_candidate_for_matching
    from src.job_requirements import prepare_job_for_matching

    prepared_candidate = prepare_candidate_for_matching(
        candidate_profile
    )

    prepared_job = prepare_job_for_matching(
        job_requirements
    )

    match_result = match_candidate_to_job(
        prepared_candidate,
        prepared_job,
    )

    validated_result = validate_match_result(
        match_result
    )

    consistency_result = validate_match_score_consistency(
        validated_result
    )

    validated_result["score_consistency"] = consistency_result

    explanation = build_match_explanation(
        validated_result
    )

    validated_result["explanation"] = explanation

    validated_result["final_result"] = {
        "candidate": {
            "name": validated_result.get(
                "candidate_name",
                "",
            ),
        },
        "job": {
            "title": validated_result.get(
                "job_title",
                "",
            ),
        },
        "score": validated_result.get(
            "scoring",
            {},
        ),
        "requirements": {
            "mandatory_met": validated_result.get(
                "required_requirements_met",
                False,
            ),
        },
        "decision": validated_result.get(
            "decision",
            {},
        ),
        "explanation": validated_result.get(
            "explanation",
            {},
        ),
        "score_consistency": validated_result.get(
            "score_consistency",
            {},
        ),
        "decision_rules": validated_result.get(
            "decision_rules",
            {},
        ),
    }

    return validated_result


def build_ranking_summary(result: Dict) -> Dict:
    """Build a concise, explainable summary for a ranked candidate."""

    if not isinstance(result, dict):
        raise TypeError("Match result must be a dictionary.")

    scoring = result.get("scoring", {})
    decision = result.get("decision", {})
    explanation = result.get("explanation", {})

    return {
        "rank": result.get("rank"),
        "candidate_name": result.get(
            "candidate_name",
            "",
        ),
        "job_title": result.get(
            "job_title",
            "",
        ),
        "overall_score": scoring.get(
            "overall_score",
            0.0,
        ),
        "decision": decision.get(
            "decision",
            "",
        ),
        "eligible": decision.get(
            "eligible",
            False,
        ),
        "required_requirements_met": result.get(
            "required_requirements_met",
            False,
        ),
        "strengths": explanation.get(
            "strengths",
            [],
        ),
        "gaps": explanation.get(
            "gaps",
            [],
        ),
        "score_breakdown": {
            "skills": scoring.get(
                "skills_score",
                0.0,
            ),
            "experience": scoring.get(
                "experience_score",
                0.0,
            ),
            "education": scoring.get(
                "education_score",
                0.0,
            ),
            "semantic": scoring.get(
                "semantic_score",
                0.0,
            ),
        },
    }


def rank_candidates_for_job(
    candidates: list[Dict],
    job_requirements: Dict,
) -> list[Dict]:
    """Rank multiple candidates against one employer-defined job."""

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be a list.")

    if not isinstance(job_requirements, dict):
        raise TypeError("Job requirements must be a dictionary.")

    ranked_results = []

    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise TypeError("Each candidate must be a dictionary.")

        result = run_matching_pipeline(
            candidate,
            job_requirements,
        )

        ranked_results.append(result)

    def ranking_key(result):
        decision = result.get("decision", {})
        scoring = result.get("scoring", {})

        qualified = decision.get("eligible", False)
        overall_score = scoring.get("overall_score", 0.0)
        candidate_name = result.get("candidate_name", "").lower()

        return (
            not qualified,
            -overall_score,
            candidate_name,
        )

    ranked_results.sort(key=ranking_key)

    for rank, result in enumerate(ranked_results, start=1):
        result["rank"] = rank
        result["ranking_summary"] = build_ranking_summary(result)

    return ranked_results
