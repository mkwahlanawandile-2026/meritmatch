from src.nlp_parser import (
    calculate_experience_months,
    detect_sections,
    extract_certifications,
    extract_education,
    extract_email,
    extract_experience,
    extract_experience_dates,
    extract_experience_records,
    extract_name,
    extract_phone,
    extract_skills,
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
    assert profile["experience_records"][0]["job_title"] == "Software Developer"
    assert profile["experience_records"][1]["job_title"] == "Data Analyst"
