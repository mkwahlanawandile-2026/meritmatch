"""Parse structured candidate information from extracted resume text."""

import re
from datetime import date
from typing import Dict, List, Optional, Tuple


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


# ---------------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Candidate information
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def _normalise_year(year: str) -> int:
    """Convert two-digit years to four-digit years."""
    value = int(year)

    if value < 100:
        return 2000 + value if value <= 50 else 1900 + value

    return value


def _parse_date_part(value: str) -> Optional[Tuple[int, int]]:
    """
    Parse a date component into (year, month).

    Supported examples:
        Jan 2020
        January 2020
        01/2020
        2020
    """
    value = value.strip().lower()

    match = re.fullmatch(r"([a-z]+)\s+(\d{2,4})", value)

    if match:
        month_name, year = match.groups()
        month = MONTHS.get(month_name)

        if month:
            return _normalise_year(year), month

    match = re.fullmatch(
        r"(0?[1-9]|1[0-2])\s*[/.-]\s*(\d{2,4})",
        value,
    )

    if match:
        month, year = match.groups()
        return _normalise_year(year), int(month)

    match = re.fullmatch(r"\d{4}", value)

    if match:
        return int(value), 1

    return None


def _is_present(value: str) -> bool:
    """Return True when an experience end date means employment continues."""
    return value.strip().lower() in {
        "present",
        "current",
        "now",
        "ongoing",
    }


def _parse_experience_range(
    text: str,
) -> Optional[Tuple[str, str, int, int]]:
    """
    Extract an experience date range.

    Examples:
        Jan 2020 - Mar 2023
        January 2020 – March 2023
        2020 - 2023
        Jun 2022 - Present
    """
    match = re.search(
        r"(?P<start>"
        r"(?:"
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{2,4}"
        r"|"
        r"\d{1,2}\s*[/.-]\s*\d{2,4}"
        r"|"
        r"\d{4}"
        r")"
        r")"
        r"\s*(?:-|–|—|to)\s*"
        r"(?P<end>"
        r"(?:"
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{2,4}"
        r"|"
        r"\d{1,2}\s*[/.-]\s*\d{2,4}"
        r"|"
        r"\d{4}"
        r"|"
        r"present|current|now|ongoing"
        r")"
        r")",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    start_raw = match.group("start")
    end_raw = match.group("end")

    start = _parse_date_part(start_raw)

    if not start:
        return None

    start_year, start_month = start

    if _is_present(end_raw):
        today = date.today()
        end_year = today.year
        end_month = today.month
        end_date = "Present"
    else:
        end = _parse_date_part(end_raw)

        if not end:
            return None

        end_year, end_month = end
        end_date = f"{end_year:04d}-{end_month:02d}"

    if (end_year, end_month) < (start_year, start_month):
        return None

    duration_months = (
        (end_year - start_year) * 12
        + (end_month - start_month)
        + 1
    )

    duration_years = duration_months // 12

    start_date = f"{start_year:04d}-{start_month:02d}"

    return (
        start_date,
        end_date,
        duration_months,
        duration_years,
    )


def extract_experience_dates(text: str) -> List[Dict]:
    """Extract experience date ranges from resume text."""
    results = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        parsed = _parse_experience_range(line)

        if not parsed:
            continue

        start_date, end_date, duration_months, duration_years = parsed

        results.append({
            "raw": line,
            "start_date": start_date,
            "end_date": end_date,
            "duration_months": duration_months,
            "duration_years": duration_years,
        })

    return results


def calculate_experience_months(
    start_date: str,
    end_date: Optional[str] = None,
) -> int:
    """Calculate experience duration in months."""
    start_year, start_month = map(int, start_date.split("-"))

    if not end_date or end_date.lower() in {
        "present",
        "current",
        "now",
    }:
        today = date.today()
        end_year = today.year
        end_month = today.month
    else:
        end_year, end_month = map(int, end_date.split("-"))

    if (end_year, end_month) < (start_year, start_month):
        return 0

    return (
        (end_year - start_year) * 12
        + (end_month - start_month)
        + 1
    )


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


# ---------------------------------------------------------------------------
# Robust experience records
# ---------------------------------------------------------------------------

def _clean_experience_line(line: str) -> str:
    """Remove common CV bullets and surrounding whitespace."""
    return re.sub(
        r"^[\s\-\*\u2022\u25AA\u25CF]+",
        "",
        line.strip(),
    ).strip()


def _looks_like_date_range(line: str) -> bool:
    """Return True when a line contains an experience date range."""
    return _parse_experience_range(line) is not None


def _split_inline_experience(line: str) -> Optional[Dict]:
    """
    Parse compact experience formats where title, employer and dates
    appear on one line.

    Examples:
        Software Developer | ABC Technologies | Jan 2020 - Mar 2023
        Software Developer, ABC Technologies - Jan 2020 - Mar 2023
    """
    parsed = _parse_experience_range(line)

    if not parsed:
        return None

    start_date, end_date, duration_months, duration_years = parsed

    match = re.search(
        r"(?P<prefix>.*?)"
        r"(?P<range>"
        r"(?:"
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{2,4}"
        r"|"
        r"\d{1,2}\s*[/.-]\s*\d{2,4}"
        r"|"
        r"\d{4}"
        r")"
        r"\s*(?:-|–|—|to)\s*"
        r"(?:"
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+\d{2,4}"
        r"|"
        r"\d{1,2}\s*[/.-]\s*\d{2,4}"
        r"|"
        r"\d{4}"
        r"|"
        r"present|current|now|ongoing"
        r")"
        r")",
        line,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    prefix = match.group("prefix").strip(" |,;:-")

    if not prefix:
        return None

    parts = [
        part.strip()
        for part in re.split(r"\s*\|\s*|\s+;\s*|;", prefix)
        if part.strip()
    ]

    if len(parts) >= 2:
        job_title = parts[0]
        employer = parts[1]
    else:
        comma_parts = [
            part.strip()
            for part in re.split(r"\s*,\s*", prefix)
            if part.strip()
        ]

        if len(comma_parts) >= 2:
            job_title = comma_parts[0]
            employer = comma_parts[1]
        else:
            job_title = prefix
            employer = ""

    return {
        "job_title": job_title,
        "employer": employer,
        "start_date": start_date,
        "end_date": end_date,
        "duration_months": duration_months,
        "duration_years": duration_years,
    }


def _looks_like_responsibility(line: str) -> bool:
    """Identify common responsibility/description lines."""
    stripped = line.strip()

    if not stripped:
        return True

    if re.match(r"^[\-\*\u2022\u25AA\u25CF]", stripped):
        return True

    lowered = stripped.lower()

    responsibility_starts = (
        "responsible for ",
        "developed ",
        "designed ",
        "implemented ",
        "managed ",
        "maintained ",
        "created ",
        "led ",
        "worked on ",
        "collaborated ",
        "assisted ",
        "supported ",
        "performed ",
        "analyzed ",
        "analysed ",
        "built ",
        "using ",
    )

    return lowered.startswith(responsibility_starts)


def extract_experience_records(text: str) -> List[Dict]:
    """
    Extract structured employment records from common CV layouts.

    Supported layouts include:

        Job Title
        Employer
        Jan 2020 - Mar 2023

        Job Title | Employer | Jan 2020 - Mar 2023

        Job Title, Employer
        January 2020 - March 2023

        Employer
        Job Title
        2020 - Present

    The parser remains industry-neutral and does not assume any
    particular company, department, profession, or employer rule.
    """
    sections = detect_sections(text)
    experience_text = sections.get("experience", "")

    if not experience_text:
        return []

    lines = [
        _clean_experience_line(line)
        for line in experience_text.splitlines()
        if line.strip()
    ]

    records: List[Dict] = []
    current_lines: List[str] = []

    def save_record(record: Optional[Dict]) -> None:
        if not record:
            return

        if not record.get("job_title") and not record.get("employer"):
            return

        records.append(record)

    for line in lines:
        # ---------------------------------------------------------------
        # Compact one-line experience entry.
        # ---------------------------------------------------------------
        inline_record = _split_inline_experience(line)

        if inline_record:
            save_record(inline_record)
            current_lines = []
            continue

        # ---------------------------------------------------------------
        # Date line completes the current multi-line record.
        # ---------------------------------------------------------------
        parsed_date = _parse_experience_range(line)

        if parsed_date:
            start_date, end_date, duration_months, duration_years = parsed_date

            if current_lines:
                if len(current_lines) == 1:
                    job_title = current_lines[0]
                    employer = ""
                else:
                    first = current_lines[0]
                    second = current_lines[1]

                    # If the first line looks like a company and the
                    # second looks like a role, preserve both.
                    if (
                        re.search(
                            r"\b(inc|llc|ltd|limited|corp|corporation|"
                            r"company|technologies|solutions|group)\b",
                            first,
                            re.IGNORECASE,
                        )
                        and not re.search(
                            r"\b(inc|llc|ltd|limited|corp|corporation|"
                            r"company|technologies|solutions|group)\b",
                            second,
                            re.IGNORECASE,
                        )
                    ):
                        employer = first
                        job_title = second
                    else:
                        job_title = first
                        employer = second

                save_record({
                    "job_title": job_title,
                    "employer": employer,
                    "start_date": start_date,
                    "end_date": end_date,
                    "duration_months": duration_months,
                    "duration_years": duration_years,
                })

            current_lines = []
            continue

        # ---------------------------------------------------------------
        # Ignore responsibility lines when they occur after a probable
        # role/employer pair.
        # ---------------------------------------------------------------
        if _looks_like_responsibility(line):
            continue

        current_lines.append(line)

        # Prevent descriptions from accumulating indefinitely.
        if len(current_lines) > 3:
            current_lines = current_lines[-3:]

    return records


# ---------------------------------------------------------------------------
# Certifications
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Complete candidate profile
# ---------------------------------------------------------------------------

def parse_resume(text: str) -> Dict:
    """Parse extracted resume text into a structured candidate profile."""
    experience = extract_experience(text)

    experience_dates = extract_experience_dates(
        detect_sections(text).get("experience", "")
    )

    experience_records = extract_experience_records(text)

    # Normalize extracted experience records
    normalized_experience = normalize_experience_records(
        experience_records
    )

    # Calculate total experience without double-counting overlaps
    total_experience_months = calculate_total_experience_months(
        normalized_experience
    )

    # Identify the candidate's current experience
    current_experience = get_current_experience(
        normalized_experience
    )

    profile = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": experience,
        "experience_dates": experience_dates,
        "experience_records": normalized_experience,
        "total_experience_months": total_experience_months,
        "current_experience": current_experience,
        "certifications": extract_certifications(text),
        "sections": detect_sections(text),
    }

    # Validate the complete candidate profile
    profile = validate_candidate_profile(profile)

    # Assess profile completeness and extraction quality
    profile["profile_quality"] = assess_candidate_profile_quality(
        profile
    )

    return profile


def assess_candidate_profile_quality(profile: Dict) -> Dict:
    """Assess the completeness and quality of a parsed candidate profile."""
    if not isinstance(profile, dict):
        raise TypeError("Candidate profile must be a dictionary.")

    issues = []
    warnings = []

    name = str(profile.get("name") or "").strip()
    email = str(profile.get("email") or "").strip()
    skills = profile.get("skills") or []
    education = profile.get("education") or []
    experience_records = profile.get("experience_records") or []
    certifications = profile.get("certifications") or []

    # Basic identity checks
    if not name:
        issues.append("Candidate name is missing.")

    if not email:
        warnings.append("Candidate email is missing.")

    # Skills check
    if not skills:
        warnings.append("No skills were detected.")

    # Education check
    if not education:
        warnings.append("No education information was detected.")

    # Experience checks
    if not experience_records:
        warnings.append("No structured experience records were detected.")

    for index, record in enumerate(experience_records, start=1):
        if not isinstance(record, dict):
            issues.append(
                f"Experience record {index} is not a valid record."
            )
            continue

        if not str(record.get("job_title") or "").strip():
            warnings.append(
                f"Experience record {index} is missing a job title."
            )

        if not str(record.get("employer") or "").strip():
            warnings.append(
                f"Experience record {index} is missing an employer."
            )

        if not str(record.get("start_date") or "").strip():
            warnings.append(
                f"Experience record {index} is missing a start date."
            )

        duration = record.get("duration_months")

        if duration is not None:
            try:
                if int(duration) < 0:
                    issues.append(
                        f"Experience record {index} has a negative duration."
                    )
            except (TypeError, ValueError):
                issues.append(
                    f"Experience record {index} has an invalid duration."
                )

    # Certification information is optional, so it is only reported
    # when absent as a warning rather than an issue.
    if not certifications:
        warnings.append("No certifications were detected.")

    # Calculate a simple completeness score.
    checks = [
        bool(name),
        bool(email),
        bool(skills),
        bool(education),
        bool(experience_records),
    ]

    completeness_score = round(
        (sum(checks) / len(checks)) * 100,
        2,
    )

    if issues:
        status = "invalid"
    elif completeness_score >= 80:
        status = "complete"
    elif completeness_score >= 60:
        status = "mostly_complete"
    else:
        status = "incomplete"

    return {
        "status": status,
        "completeness_score": completeness_score,
        "issues": issues,
        "warnings": warnings,
        "is_valid": not issues,
    }

def validate_candidate_profile(profile: Dict) -> Dict:
    """Validate and normalize the structure of a parsed candidate profile."""
    if not isinstance(profile, dict):
        raise TypeError("Candidate profile must be a dictionary.")

    validated = dict(profile)

    # Safe defaults for core candidate fields
    validated["name"] = str(validated.get("name") or "").strip()
    validated["email"] = str(validated.get("email") or "").strip()
    validated["phone"] = str(validated.get("phone") or "").strip()

    # Ensure collection fields are always lists
    for field in (
        "skills",
        "education",
        "experience",
        "experience_dates",
        "experience_records",
        "certifications",
    ):
        value = validated.get(field)

        if value is None:
            validated[field] = []
        elif not isinstance(value, list):
            validated[field] = [value]

    # Experience total must always be a non-negative integer
    total_experience = validated.get("total_experience_months", 0)

    try:
        total_experience = int(total_experience)
    except (TypeError, ValueError):
        total_experience = 0

    validated["total_experience_months"] = max(
        total_experience,
        0,
    )

    # Current experience must be either a record or None
    current_experience = validated.get("current_experience")

    if current_experience is not None and not isinstance(
        current_experience,
        dict,
    ):
        validated["current_experience"] = None

    # Sections should always be a dictionary
    if not isinstance(validated.get("sections"), dict):
        validated["sections"] = {}

    return validated

def normalize_experience_record(record):
    """Normalize a single extracted experience record."""
    normalized = dict(record)

    job_title = normalized.get("job_title")
    employer = normalized.get("employer")

    if job_title:
        normalized["job_title"] = " ".join(job_title.split()).strip()

    if employer:
        normalized["employer"] = " ".join(employer.split()).strip()

    start_date = normalized.get("start_date")
    end_date = normalized.get("end_date")

    if start_date:
        normalized["start_date"] = start_date.strip()

    if end_date:
        normalized["end_date"] = end_date.strip()

    duration = normalized.get("duration_months")

    if duration is not None:
        try:
            normalized["duration_months"] = int(duration)
        except (TypeError, ValueError):
            normalized["duration_months"] = 0

    normalized["is_current"] = (
        str(end_date).strip().lower()
        in {"present", "current", "now", "ongoing"}
    )

    return normalized


def normalize_experience_records(records):
    """Normalize a collection of experience records."""
    if not records:
        return []

    return [
        normalize_experience_record(record)
        for record in records
        if isinstance(record, dict)
    ]


def calculate_total_experience_months(records):
    """Calculate total experience while avoiding overlapping periods."""
    if not records:
        return 0

    intervals = []

    for record in records:
        start = record.get("start_date")
        end = record.get("end_date")

        if not start:
            continue

        try:
            start_year, start_month = map(int, start.split("-"))
        except (ValueError, AttributeError):
            continue

        if end and str(end).strip().lower() in {
            "present",
            "current",
            "now",
            "ongoing",
        }:
            today = date.today()
            end_year = today.year
            end_month = today.month
        else:
            try:
                end_year, end_month = map(int, str(end).split("-"))
            except (ValueError, AttributeError):
                continue

        start_index = start_year * 12 + start_month
        end_index = end_year * 12 + end_month

        if end_index < start_index:
            continue

        intervals.append((start_index, end_index))

    if not intervals:
        return 0

    intervals.sort()

    merged = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))

    return sum(
        end - start + 1
        for start, end in merged
    )


def get_current_experience(records):
    """Return the current employment record, if one exists."""
    normalized_records = normalize_experience_records(records)

    for record in normalized_records:
        if record.get("is_current"):
            return record

    return None
