See the project documentation for architecture and usage.

# meritmatch
MeritMatch is an AI-powered resume analyzer that helps recruiters shortlist candidates faster and more fairly. It parses resumes, extracts skills and experience, matches them against a job description, then scores and ranks each candidate on a summarized dashboard, so hiring decisions rest on merit alone.

# MeritMatch

**Candidates matched on skills and experience alone.**

MeritMatch is an AI-powered resume analyzer that helps recruiters shortlist candidates faster and more fairly. It parses resumes, extracts skills and experience, matches them against a job description, then scores and ranks each candidate on a summarized dashboard, so hiring decisions rest on merit alone.

> **Status:** Under active development. See the [roadmap](#roadmap) for progress.

---

## Why MeritMatch?

Recruitment teams receive hundreds of resumes for every opening. Reading them by hand is slow, inconsistent, and open to unconscious bias. MeritMatch automates first-round screening with transparent, explainable scoring, while the recruiter keeps the final decision.

## Features

- **Resume parsing:** reads PDF, DOCX, and TXT resumes
- **Structured extraction:** skills, education, and years of experience
- **Job description analysis:** required and preferred skills, minimum experience
- **Semantic matching:** "ML" matches "Machine Learning"
- **Weighted scoring and ranking:** every candidate gets a 0-100 score
- **Explainable results:** matched skills, missing skills, and a score breakdown
- **Bias reduction:** optional anonymization of personal details before scoring
- **Recruiter dashboard:** ranked table, charts, and CSV export

## How It Works

```
Upload resumes + job description
        |
Text extraction (PDF / DOCX / TXT)
        |
Cleaning and anonymization
        |
NLP: skills, education, experience
        |
Matching engine (keyword + semantic)
        |
Scoring and ranking
        |
Dashboard and export
```

**Scoring formula**

| Component | Default weight |
|---|---|
| Skills match | 40% |
| Experience match | 25% |
| Education match | 15% |
| Semantic similarity | 20% |

Weights can be changed in `config.py`.

## Tech Stack

Python 3.10+, spaCy, sentence-transformers, scikit-learn, pandas, pdfplumber, python-docx, Streamlit, Plotly.

## Project Structure

```
meritmatch/
├── config.py                # Weights, thresholds, settings
├── requirements.txt
├── data/
│   └── skills_taxonomy.json # Skills and their aliases
├── src/                     # Core logic (extraction, NLP, matching, scoring)
├── dashboard/               # Streamlit dashboard components
└── tests/                   # Automated tests
```

## Getting Started

**Prerequisites:** Python 3.10 or higher and Git.

```bash
# 1. Clone the repository
git clone https://github.com/mkwahlanawandile-2026/meritmatch.git
cd meritmatch

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the language model
python -m spacy download en_core_web_sm
```

## Usage

Once the dashboard is complete:

```bash
streamlit run app.py
```

Then create a job, upload resumes, click **Analyze**, and review the ranked shortlist.

## Roadmap

- [x] Project setup, configuration, and skills taxonomy
- [ ] Resume text extraction
- [ ] NLP parsing (skills, education, experience)
- [ ] Job description parser
- [ ] Matching engine
- [ ] Scoring and ranking
- [ ] Streamlit dashboard
- [ ] Testing and polish

## Ethical Use

MeritMatch is a decision-support tool, not a replacement for human judgment. Scores should be reviewed by a recruiter, models should be audited for bias, and resume data contains personal information that must be stored securely and handled in line with privacy laws such as POPIA and GDPR.

## License

Released under the MIT License. See the `LICENSE` file for details.
