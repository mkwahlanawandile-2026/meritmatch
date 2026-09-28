"""Parse structured candidate information from extracted resume text."""

import re
from typing import Dict, List


SECTION_ALIASES = {
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "competencies",
    },
    "education": {
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
    },
    "projects": {
        "projects",
        "academic projects",
        "personal projects",
    },
    "certifications": {
        "certifications",
        "certificates",
        "professional certifications",
    },
}


def _normalise_heading(text: str) -> str:
    """Normalize a possible section heading."""
    text = text.strip().lower()
    text = re.sub(r"[:\-]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def detect_sections(text: str) -> Dict[str, str]:
    """Split resume text into recognized sections."""
    sections: Dict[str, List[str]] = {}
    current_section = "header"
    sections[current_section] = []

    alias_lookup = {
        alias: section
        for section, aliases in SECTION_ALIASES.items()
        for alias in aliases
    }

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        heading = _normalise_heading(stripped)

        if heading in alias_lookup:
            current_section = alias_lookup[heading]
            sections.setdefault(current_section, [])
            continue

        sections.setdefault(current_section, [])
        sections[current_section].append(stripped)

    return {
        section: "\n".join(lines).strip()
        for section, lines in sections.items()
        if lines
    }


def extract_email(text: str) -> str:
    """Extract the first email address."""
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract a likely phone number."""
    match = re.search(
        r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
        text,
    )
    return match.group(0).strip() if match else ""


def extract_name(text: str) -> str:
    """Use the first suitable header line as the candidate name."""
    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:
            return line

    return ""


def extract_skills(text: str) -> List[str]:
    """Extract skills from the skills section."""
    sections = detect_sections(text)
    skills_text = sections.get("skills", "")

    if not skills_text:
        return []

    raw_items = re.split(r"[,;|\n]", skills_text)

    skills = []

    for item in raw_items:
        skill = re.sub(r"^[\-\*\u2022]\s*", "", item).strip()

        if skill and skill not in skills:
            skills.append(skill)

    return skills


def extract_education(text: str) -> List[str]:
    """Extract education entries from the education section."""
    sections = detect_sections(text)
    education_text = sections.get("education", "")

    if not education_text:
        return []

    return [
        line.strip()
        for line in education_text.splitlines()
        if line.strip()
    ]


def extract_experience(text: str) -> List[str]:
    """Extract experience entries from the experience section."""
    sections = detect_sections(text)
    experience_text = sections.get("experience", "")

    if not experience_text:
        return []

    return [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]


def extract_certifications(text: str) -> List[str]:
    """Extract certification entries."""
    sections = detect_sections(text)
    certification_text = sections.get("certifications", "")

    if not certification_text:
        return []

    return [
        line.strip()
        for line in certification_text.splitlines()
        if line.strip()
    ]


def parse_resume(text: str) -> Dict:
    """Parse extracted resume text into a structured candidate profile."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "certifications": extract_certifications(text),
        "sections": detect_sections(text),
    }
