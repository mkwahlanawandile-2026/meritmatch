from src.nlp_parser import (
    detect_sections,
    extract_certifications,
    extract_education,
    extract_email,
    extract_experience,
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


def test_extract_certifications():
    certifications = extract_certifications(SAMPLE_RESUME)

    assert "AWS Cloud Practitioner" in certifications


def test_parse_resume_returns_structured_profile():
    profile = parse_resume(SAMPLE_RESUME)

    assert profile["name"] == "Jane Doe"
    assert profile["email"] == "jane.doe@example.com"
    assert "Python" in profile["skills"]
    assert "BSc Computer Science" in profile["education"]
    assert "Software Developer" in profile["experience"]
