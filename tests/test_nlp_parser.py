from src.nlp_parser import (
    calculate_experience_months,
    assess_candidate_profile_quality,
    calculate_total_experience_months,
    detect_sections,
    extract_certifications,
    extract_education,
    extract_experience,
    extract_experience_dates,
    extract_experience_records,
    extract_email,
    extract_name,
    extract_phone,
    extract_skills,
    get_current_experience,
    normalize_experience_record,
    normalize_experience_records,
    parse_resume,
)


SAMPLE_RESUME = """
Jane Doe
jane.doe@example.com
+27 71 123 4567

Skills
Python, Machine Learning, SQL
FastAPI
PostgreSQL

Education
BSc Computer Science
University of Example

Experience
Software Developer
ABC Technologies
Jan 2020 - Mar 2023

Data Analyst
XYZ Analytics
Jun 2023 - Present

Certifications
AWS Cloud Practitioner
"""


def test_extract_name():
    assert extract_name(SAMPLE_RESUME) == "Jane Doe"


def test_extract_email():
    assert extract_email(SAMPLE_RESUME) == "jane.doe@example.com"


def test_extract_phone():
    assert extract_phone(SAMPLE_RESUME) == "+27 71 123 4567"


def test_detect_sections():
    sections = detect_sections(SAMPLE_RESUME)

    assert "skills" in sections
    assert "education" in sections
    assert "experience" in sections
    assert "certifications" in sections


def test_extract_skills():
    skills = extract_skills(SAMPLE_RESUME)

    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "SQL" in skills
    assert "FastAPI" in skills
    assert "PostgreSQL" in skills


def test_extract_education():
    education = extract_education(SAMPLE_RESUME)

    assert "BSc Computer Science" in education


def test_extract_experience():
    experience = extract_experience(SAMPLE_RESUME)

    assert "Software Developer" in experience
    assert "ABC Technologies" in experience


def test_extract_certifications():
    certifications = extract_certifications(SAMPLE_RESUME)

    assert "AWS Cloud Practitioner" in certifications


def test_extract_january_2020_to_march_2023():
    results = extract_experience_dates(
        "Software Developer\nABC Technologies\nJan 2020 - Mar 2023"
    )

    assert len(results) == 1
    assert results[0]["start_date"] == "2020-01"
    assert results[0]["end_date"] == "2023-03"
    assert results[0]["duration_months"] == 39


def test_extract_year_only_range():
    results = extract_experience_dates(
        "Software Developer\nABC Technologies\n2020 - 2023"
    )

    assert len(results) == 1
    assert results[0]["start_date"] == "2020-01"
    assert results[0]["end_date"] == "2023-01"
    assert results[0]["duration_months"] == 37


def test_extract_present_experience():
    results = extract_experience_dates(
        "Data Analyst\nXYZ Analytics\nJun 2023 - Present"
    )

    assert len(results) == 1
    assert results[0]["start_date"] == "2023-06"
    assert results[0]["end_date"] == "Present"
    assert results[0]["duration_months"] >= 1


def test_calculate_experience_months():
    assert calculate_experience_months(
        "2020-01",
        "2023-03",
    ) == 39


def test_calculate_experience_months_current():
    result = calculate_experience_months(
        "2023-01",
        "Present",
    )

    assert result >= 1


def test_invalid_experience_range_is_ignored():
    results = extract_experience_dates(
        "Software Developer\n2025 - 2020"
    )

    assert results == []


def test_parse_resume_returns_structured_profile():
    profile = parse_resume(SAMPLE_RESUME)

    assert profile["name"] == "Jane Doe"
    assert profile["email"] == "jane.doe@example.com"
    assert "Python" in profile["skills"]
    assert "BSc Computer Science" in profile["education"]
    assert "Software Developer" in profile["experience"]
    assert len(profile["experience_dates"]) == 2


def test_extract_experience_records():
    records = extract_experience_records(SAMPLE_RESUME)

    assert len(records) == 2

    assert records[0]["job_title"] == "Software Developer"
    assert records[0]["employer"] == "ABC Technologies"
    assert records[0]["start_date"] == "2020-01"
    assert records[0]["end_date"] == "2023-03"
    assert records[0]["duration_months"] == 39

    assert records[1]["job_title"] == "Data Analyst"
    assert records[1]["employer"] == "XYZ Analytics"
    assert records[1]["start_date"] == "2023-06"
    assert records[1]["end_date"] == "Present"


def test_parse_resume_contains_experience_records():
    profile = parse_resume(SAMPLE_RESUME)

    assert "experience_records" in profile
    assert len(profile["experience_records"]) == 2

    assert profile["experience_records"][0]["job_title"] == (
        "Software Developer"
    )


def test_experience_records_inline_pipe_format():
    text = """
Jane Doe

Experience
Software Developer | ABC Technologies | Jan 2020 - Mar 2023
"""

    records = extract_experience_records(text)

    assert len(records) == 1
    assert records[0]["job_title"] == "Software Developer"
    assert records[0]["employer"] == "ABC Technologies"
    assert records[0]["start_date"] == "2020-01"
    assert records[0]["end_date"] == "2023-03"
    assert records[0]["duration_months"] == 39


def test_experience_records_inline_comma_format():
    text = """
Jane Doe

Experience
Data Analyst, Example Solutions - January 2021 - December 2022
"""

    records = extract_experience_records(text)

    assert len(records) == 1
    assert records[0]["job_title"] == "Data Analyst"
    assert records[0]["employer"] == "Example Solutions"
    assert records[0]["start_date"] == "2021-01"
    assert records[0]["end_date"] == "2022-12"


def test_experience_records_employer_first_layout():
    text = """
Jane Doe

Experience
ABC Technologies
Software Developer
2020 - Present
"""

    records = extract_experience_records(text)

    assert len(records) == 1
    assert records[0]["employer"] == "ABC Technologies"
    assert records[0]["job_title"] == "Software Developer"
    assert records[0]["start_date"] == "2020-01"
    assert records[0]["end_date"] == "Present"


def test_experience_records_ignore_responsibilities():
    text = """
Jane Doe

Experience
Software Developer
ABC Technologies
Jan 2020 - Mar 2023
- Developed software applications
- Managed database systems
- Collaborated with engineering teams
"""

    records = extract_experience_records(text)

    assert len(records) == 1
    assert records[0]["job_title"] == "Software Developer"
    assert records[0]["employer"] == "ABC Technologies"


def test_parse_resume_contains_robust_experience_records():
    text = """
Jane Doe
jane.doe@example.com

Experience
Software Developer | ABC Technologies | Jan 2020 - Mar 2023
Data Analyst | Example Solutions | Apr 2023 - Present
"""

    profile = parse_resume(text)

    assert len(profile["experience_records"]) == 2
    assert profile["experience_records"][0]["job_title"] == (
        "Software Developer"
    )
    assert profile["experience_records"][1]["job_title"] == (
        "Data Analyst"
    )


def test_normalize_experience_record():
    record = {
        "job_title": "  Software   Developer  ",
        "employer": "  ABC   Technologies ",
        "start_date": "2020-01",
        "end_date": "2023-03",
        "duration_months": 39,
    }

    normalized = normalize_experience_record(record)

    assert normalized["job_title"] == "Software Developer"
    assert normalized["employer"] == "ABC Technologies"
    assert normalized["start_date"] == "2020-01"
    assert normalized["end_date"] == "2023-03"
    assert normalized["duration_months"] == 39
    assert normalized["is_current"] is False


def test_normalize_current_experience_record():
    record = {
        "job_title": "Data Analyst",
        "employer": "Example Solutions",
        "start_date": "2023-04",
        "end_date": "Present",
        "duration_months": 42,
    }

    normalized = normalize_experience_record(record)

    assert normalized["is_current"] is True


def test_normalize_experience_records():
    records = [
        {
            "job_title": "  Software   Developer ",
            "employer": " ABC Technologies ",
            "start_date": "2020-01",
            "end_date": "2023-03",
            "duration_months": 39,
        },
        {
            "job_title": " Data Analyst ",
            "employer": " Example Solutions ",
            "start_date": "2023-04",
            "end_date": "Present",
            "duration_months": 42,
        },
    ]

    normalized = normalize_experience_records(records)

    assert len(normalized) == 2
    assert normalized[0]["job_title"] == "Software Developer"
    assert normalized[1]["job_title"] == "Data Analyst"
    assert normalized[1]["is_current"] is True


def test_calculate_total_experience_months():
    records = [
        {
            "start_date": "2020-01",
            "end_date": "2023-03",
        },
        {
            "start_date": "2023-04",
            "end_date": "2024-03",
        },
    ]

    total = calculate_total_experience_months(records)

    assert total == 51


def test_overlapping_experience_is_not_double_counted():
    records = [
        {
            "start_date": "2020-01",
            "end_date": "2022-12",
        },
        {
            "start_date": "2021-01",
            "end_date": "2023-12",
        },
    ]

    total = calculate_total_experience_months(records)

    assert total == 48


def test_get_current_experience():
    records = [
        {
            "job_title": "Software Developer",
            "employer": "ABC Technologies",
            "start_date": "2020-01",
            "end_date": "2023-03",
        },
        {
            "job_title": "Data Analyst",
            "employer": "Example Solutions",
            "start_date": "2023-04",
            "end_date": "Present",
        },
    ]

    current = get_current_experience(records)

    assert current is not None
    assert current["job_title"] == "Data Analyst"
    assert current["employer"] == "Example Solutions"
    assert current["is_current"] is True


# Step 8.6: normalized experience is integrated into the candidate profile.

def test_parse_resume_contains_total_experience_months():
    profile = parse_resume(SAMPLE_RESUME)

    assert "total_experience_months" in profile
    assert isinstance(profile["total_experience_months"], int)
    assert profile["total_experience_months"] > 0


def test_parse_resume_contains_current_experience():
    profile = parse_resume(SAMPLE_RESUME)

    assert "current_experience" in profile
    assert profile["current_experience"] is not None
    assert profile["current_experience"]["job_title"] == "Data Analyst"
    assert profile["current_experience"]["employer"] == "XYZ Analytics"
    assert profile["current_experience"]["is_current"] is True


def test_parse_resume_returns_normalized_experience_records():
    text = """
Jane Doe

Experience
Software   Developer | ABC   Technologies | Jan 2020 - Mar 2023
Data   Analyst | XYZ   Analytics | Jun 2023 - Present
"""

    profile = parse_resume(text)

    assert len(profile["experience_records"]) == 2

    assert profile["experience_records"][0]["job_title"] == (
        "Software Developer"
    )
    assert profile["experience_records"][0]["employer"] == (
        "ABC Technologies"
    )

    assert profile["experience_records"][1]["job_title"] == (
        "Data Analyst"
    )
    assert profile["experience_records"][1]["employer"] == (
        "XYZ Analytics"
    )
    assert profile["experience_records"][1]["is_current"] is True

def test_validate_candidate_profile():
    from src.nlp_parser import validate_candidate_profile

    profile = {
        "name": "  Jane Doe  ",
        "email": " jane@example.com ",
        "phone": None,
        "skills": ["Python"],
        "education": None,
        "experience": ["Software Developer"],
        "experience_dates": None,
        "experience_records": [],
        "certifications": None,
        "total_experience_months": "39",
        "current_experience": None,
        "sections": {},
    }

    validated = validate_candidate_profile(profile)

    assert validated["name"] == "Jane Doe"
    assert validated["email"] == "jane@example.com"
    assert validated["phone"] == ""
    assert validated["skills"] == ["Python"]
    assert validated["education"] == []
    assert validated["experience_dates"] == []
    assert validated["certifications"] == []
    assert validated["total_experience_months"] == 39


def test_validate_candidate_profile_handles_invalid_total_experience():
    from src.nlp_parser import validate_candidate_profile

    profile = {
        "total_experience_months": "invalid",
        "skills": [],
        "education": [],
        "experience": [],
        "experience_dates": [],
        "experience_records": [],
        "certifications": [],
        "sections": {},
    }

    validated = validate_candidate_profile(profile)

    assert validated["total_experience_months"] == 0


def test_validate_candidate_profile_rejects_invalid_profile():
    from src.nlp_parser import validate_candidate_profile

    try:
        validate_candidate_profile([])
        assert False
    except TypeError as error:
        assert str(error) == "Candidate profile must be a dictionary."


def test_assess_candidate_profile_quality_complete_profile():
    from src.nlp_parser import assess_candidate_profile_quality

    profile = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "skills": ["Python", "SQL"],
        "education": ["BSc Computer Science"],
        "experience_records": [
            {
                "job_title": "Software Developer",
                "employer": "ABC Technologies",
                "start_date": "2020-01",
                "end_date": "2023-03",
                "duration_months": 39,
            }
        ],
        "certifications": ["AWS Cloud Practitioner"],
    }

    quality = assess_candidate_profile_quality(profile)

    assert quality["status"] == "complete"
    assert quality["completeness_score"] == 100.0
    assert quality["is_valid"] is True
    assert quality["issues"] == []


def test_assess_candidate_profile_quality_incomplete_profile():
    from src.nlp_parser import assess_candidate_profile_quality

    profile = {
        "name": "Jane Doe",
        "email": "",
        "skills": [],
        "education": [],
        "experience_records": [],
        "certifications": [],
    }

    quality = assess_candidate_profile_quality(profile)

    assert quality["status"] == "incomplete"
    assert quality["completeness_score"] == 20.0
    assert quality["is_valid"] is True
    assert quality["issues"] == []
    assert len(quality["warnings"]) > 0


def test_assess_candidate_profile_quality_detects_invalid_experience():
    from src.nlp_parser import assess_candidate_profile_quality

    profile = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "skills": ["Python"],
        "education": ["BSc Computer Science"],
        "experience_records": [
            {
                "job_title": "",
                "employer": "",
                "start_date": "",
                "duration_months": -5,
            }
        ],
        "certifications": [],
    }

    quality = assess_candidate_profile_quality(profile)

    assert quality["status"] == "invalid"
    assert quality["is_valid"] is False
    assert len(quality["issues"]) > 0


def test_parse_resume_contains_profile_quality():
    profile = parse_resume(SAMPLE_RESUME)

    assert "profile_quality" in profile
    assert isinstance(profile["profile_quality"], dict)
    assert "status" in profile["profile_quality"]
    assert "completeness_score" in profile["profile_quality"]
    assert "issues" in profile["profile_quality"]
    assert "warnings" in profile["profile_quality"]
    assert "is_valid" in profile["profile_quality"]


def test_parse_resume_profile_quality_for_complete_resume():
    profile = parse_resume(SAMPLE_RESUME)

    quality = profile["profile_quality"]

    assert quality["status"] == "complete"
    assert quality["completeness_score"] == 100.0
    assert quality["is_valid"] is True
    assert quality["issues"] == []


def test_parse_resume_profile_quality_for_incomplete_resume():
    text = """
Jane Doe
"""

    profile = parse_resume(text)

    quality = profile["profile_quality"]

    assert quality["status"] == "incomplete"
    assert quality["completeness_score"] == 20.0
    assert quality["is_valid"] is True
    assert len(quality["warnings"]) > 0
