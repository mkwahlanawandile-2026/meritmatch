"""Central configuration for MeritMatch."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SKILLS_TAXONOMY_PATH = DATA_DIR / "skills_taxonomy.json"

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 5

SPACY_MODEL = "en_core_web_sm"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
SEMANTIC_MATCH_THRESHOLD = 0.75

# Scoring weights (must sum to 1.0)
WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "education": 0.15,
    "semantic": 0.20,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "Weights must sum to 1.0"

ANONYMIZE_BY_DEFAULT = True

# Match decision thresholds
DECISION_MIN_OVERALL_SCORE = 70.0
DECISION_REQUIRE_MANDATORY_REQUIREMENTS = True
DECISION_REQUIRE_SEMANTIC_THRESHOLD = True

