"""MeritMatch — recruiter intelligence dashboard."""

import streamlit as st


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="MeritMatch | Candidate Intelligence",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# Premium application styling
# ---------------------------------------------------------------------

st.markdown(
    """
    <style>

    /* ================================================================
       Global
       ================================================================ */

    .stApp {
        background: #f6f7f9;
        color: #172033;
    }

    .main .block-container {
        max-width: 1500px;
        padding: 2rem 2.5rem 3rem;
    }

    h1, h2, h3, h4 {
        color: #172033;
        letter-spacing: -0.02em;
    }

    p, label {
        color: #5f6b7a;
    }

    /* ================================================================
       Sidebar
       ================================================================ */

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #202938;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }

    .brand {
        padding: 0.5rem 0.6rem 2rem;
    }

    .brand-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #ffffff;
        color: #111827;
        font-weight: 800;
        margin-right: 10px;
    }

    .brand-name {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 750;
        vertical-align: middle;
    }

    .brand-subtitle {
        color: #8d98a8;
        font-size: 0.75rem;
        margin-top: 8px;
        margin-left: 48px;
    }

    .nav-section {
        color: #667286;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 1.4rem 0 0.6rem 0.65rem;
    }

    .side-item {
        color: #b7c0cd;
        padding: 0.7rem 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.2rem;
        font-size: 0.9rem;
    }

    .side-item.active {
        background: #202a3a;
        color: #ffffff;
        font-weight: 650;
    }

    .side-footer {
        position: fixed;
        bottom: 20px;
        color: #667286;
        font-size: 0.72rem;
        padding-left: 0.65rem;
    }

    /* ================================================================
       Top bar
       ================================================================ */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .eyebrow {
        color: #697586;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .page-title {
        font-size: 2rem;
        font-weight: 760;
        margin: 0;
        color: #172033;
    }

    .page-description {
        margin-top: 0.45rem;
        color: #687486;
        font-size: 0.9rem;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        border: 1px solid #dce2e8;
        background: #ffffff;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        color: #465366;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #2f855a;
        border-radius: 50%;
    }

    /* ================================================================
       KPI cards
       ================================================================ */

    .kpi {
        background: #ffffff;
        border: 1px solid #e2e6eb;
        border-radius: 12px;
        padding: 1.15rem 1.25rem;
        min-height: 115px;
    }

    .kpi-label {
        color: #758092;
        font-size: 0.75rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-value {
        color: #172033;
        font-size: 1.85rem;
        font-weight: 760;
        margin-top: 0.35rem;
    }

    .kpi-meta {
        color: #7c8796;
        font-size: 0.73rem;
        margin-top: 0.2rem;
    }

    /* ================================================================
       Sections
       ================================================================ */

    .section-title {
        font-size: 1.05rem;
        font-weight: 720;
        color: #172033;
        margin-bottom: 0.25rem;
    }

    .section-subtitle {
        color: #7a8594;
        font-size: 0.78rem;
        margin-bottom: 1rem;
    }

    /* ================================================================
       Cards
       ================================================================ */

    .panel {
        background: #ffffff;
        border: 1px solid #e2e6eb;
        border-radius: 12px;
        padding: 1.25rem;
        height: 100%;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.9rem;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #edf0f3;
    }

    /* ================================================================
       Candidate rows
       ================================================================ */

    .candidate-row {
        display: grid;
        grid-template-columns: 48px 1.7fr 90px 90px 90px 120px;
        align-items: center;
        gap: 0.75rem;
        padding: 0.9rem 0.25rem;
        border-bottom: 1px solid #edf0f3;
    }

    .candidate-row:last-child {
        border-bottom: none;
    }

    .rank {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f2f5;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 750;
        color: #4c5868;
    }

    .candidate-name {
        color: #1c2738;
        font-weight: 680;
        font-size: 0.86rem;
    }

    .candidate-role {
        color: #87919f;
        font-size: 0.72rem;
        margin-top: 2px;
    }

    .score {
        font-weight: 760;
        color: #172033;
    }

    .table-label {
        color: #8a94a2;
        font-size: 0.67rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .qualified {
        color: #28734b;
        background: #edf8f1;
        border: 1px solid #d6eddd;
        border-radius: 999px;
        padding: 0.28rem 0.55rem;
        font-size: 0.68rem;
        font-weight: 700;
        text-align: center;
    }

    .review {
        color: #806a28;
        background: #fbf7e8;
        border: 1px solid #eee5bf;
        border-radius: 999px;
        padding: 0.28rem 0.55rem;
        font-size: 0.68rem;
        font-weight: 700;
        text-align: center;
    }

    /* ================================================================
       Score
       ================================================================ */

    .match-score {
        text-align: center;
        padding: 0.7rem;
    }

    .match-number {
        font-size: 2.8rem;
        font-weight: 800;
        color: #172033;
        line-height: 1;
    }

    .match-label {
        color: #7a8594;
        font-size: 0.72rem;
        margin-top: 0.45rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .score-line {
        margin: 0.7rem 0;
    }

    .score-line-label {
        display: flex;
        justify-content: space-between;
        color: #657183;
        font-size: 0.75rem;
        margin-bottom: 0.3rem;
    }

    .score-track {
        width: 100%;
        height: 6px;
        border-radius: 99px;
        background: #edf0f3;
        overflow: hidden;
    }

    .score-fill {
        height: 100%;
        border-radius: 99px;
        background: #253449;
    }

    /* ================================================================
       Requirements
       ================================================================ */

    .requirement {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid #edf0f3;
    }

    .requirement:last-child {
        border-bottom: none;
    }

    .requirement-name {
        color: #354052;
        font-size: 0.82rem;
    }

    .required {
        color: #28734b;
        font-size: 0.72rem;
        font-weight: 700;
    }

    .preferred {
        color: #7a8594;
        font-size: 0.72rem;
        font-weight: 650;
    }

    /* ================================================================
       Streamlit overrides
       ================================================================ */

    .stButton > button {
        border-radius: 8px;
        font-weight: 650;
        border: 1px solid #d9dee5;
        min-height: 40px;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] {
        background: #fafbfc;
        border: 1px dashed #cbd2db;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">M</span>
            <span class="brand-name">MeritMatch</span>
            <div class="brand-subtitle">Candidate Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-section">Workspace</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="side-item active">Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-item">Jobs</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-item">Candidates</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-item">Matches</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-section">Insights</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="side-item">Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-item">Reports</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-section">System</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="side-item">Settings</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-footer">MeritMatch v0.1 · Development</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

st.markdown(
    """
    <div class="topbar">
        <div>
            <div class="eyebrow">Recruitment workspace</div>
            <div class="page-title">Candidate Intelligence</div>
            <div class="page-description">
                Evaluate candidates against employer-defined requirements.
            </div>
        </div>

        <div class="status-pill">
            <span class="status-dot"></span>
            Matching engine ready
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# KPI section
# ---------------------------------------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-label">Candidates</div>
            <div class="kpi-value">24</div>
            <div class="kpi-meta">Current job pipeline</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi2:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-label">Qualified</div>
            <div class="kpi-value">18</div>
            <div class="kpi-meta">75% of candidates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi3:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-label">Average Match</div>
            <div class="kpi-value">86.7%</div>
            <div class="kpi-meta">Across evaluated candidates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi4:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-label">Active Job</div>
            <div class="kpi-value">01</div>
            <div class="kpi-meta">Python Developer</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ---------------------------------------------------------------------
# Job context
# ---------------------------------------------------------------------

left, right = st.columns([1.55, 1], gap="large")

with left:

    st.markdown(
        """
        <div class="section-title">Top Candidates</div>
        <div class="section-subtitle">
            Ranked against the active employer-defined requirements.
        </div>

        <div class="panel">

            <div class="candidate-row">
                <div class="table-label">Rank</div>
                <div class="table-label">Candidate</div>
                <div class="table-label">Match</div>
                <div class="table-label">Skills</div>
                <div class="table-label">Experience</div>
                <div class="table-label">Decision</div>
            </div>

            <div class="candidate-row">
                <div class="rank">01</div>
                <div>
                    <div class="candidate-name">Candidate A</div>
                    <div class="candidate-role">Python Developer</div>
                </div>
                <div class="score">94.2%</div>
                <div>98%</div>
                <div>91%</div>
                <div class="qualified">QUALIFIED</div>
            </div>

            <div class="candidate-row">
                <div class="rank">02</div>
                <div>
                    <div class="candidate-name">Candidate B</div>
                    <div class="candidate-role">Backend Developer</div>
                </div>
                <div class="score">89.7%</div>
                <div>93%</div>
                <div>88%</div>
                <div class="qualified">QUALIFIED</div>
            </div>

            <div class="candidate-row">
                <div class="rank">03</div>
                <div>
                    <div class="candidate-name">Candidate C</div>
                    <div class="candidate-role">Software Developer</div>
                </div>
                <div class="score">84.1%</div>
                <div>86%</div>
                <div>82%</div>
                <div class="qualified">QUALIFIED</div>
            </div>

            <div class="candidate-row">
                <div class="rank">04</div>
                <div>
                    <div class="candidate-name">Candidate D</div>
                    <div class="candidate-role">Junior Developer</div>
                </div>
                <div class="score">81.6%</div>
                <div>89%</div>
                <div>63%</div>
                <div class="review">REVIEW</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with right:

    st.markdown(
        """
        <div class="section-title">Active Position</div>
        <div class="section-subtitle">
            Employer-defined job requirements
        </div>

        <div class="panel">

            <div class="panel-header">
                <div>
                    <strong>Python Developer</strong>
                    <div style="color:#7a8594;font-size:0.75rem;margin-top:3px;">
                        Information Technology · Remote · Full-time
                    </div>
                </div>
            </div>

            <div class="requirement">
                <span class="requirement-name">Python</span>
                <span class="required">REQUIRED</span>
            </div>

            <div class="requirement">
                <span class="requirement-name">SQL</span>
                <span class="required">REQUIRED</span>
            </div>

            <div class="requirement">
                <span class="requirement-name">FastAPI</span>
                <span class="preferred">PREFERRED</span>
            </div>

            <div class="requirement">
                <span class="requirement-name">PostgreSQL</span>
                <span class="preferred">PREFERRED</span>
            </div>

            <div class="requirement">
                <span class="requirement-name">Minimum experience</span>
                <span class="required">24 MONTHS</span>
            </div>

            <div class="requirement">
                <span class="requirement-name">Education</span>
                <span class="required">BSc / RELATED</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")
st.write("")


# ---------------------------------------------------------------------
# Candidate detail + matching analysis
# ---------------------------------------------------------------------

detail_left, detail_right = st.columns([1, 1.35], gap="large")

with detail_left:

    st.markdown(
        """
        <div class="section-title">Selected Candidate</div>
        <div class="section-subtitle">
            Detailed matching analysis
        </div>

        <div class="panel">

            <div style="display:flex;justify-content:space-between;align-items:flex-start;">

                <div>
                    <div style="font-size:1.15rem;font-weight:750;color:#172033;">
                        Candidate A
                    </div>

                    <div style="font-size:0.76rem;color:#7a8594;margin-top:4px;">
                        Python Developer · 72 months experience
                    </div>
                </div>

                <div style="color:#28734b;font-weight:750;font-size:0.75rem;">
                    QUALIFIED
                </div>

            </div>

            <div class="match-score">
                <div class="match-number">94.2%</div>
                <div class="match-label">Overall Match</div>
            </div>

            <div class="score-line">
                <div class="score-line-label">
                    <span>Skills</span>
                    <strong>98%</strong>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:98%;"></div>
                </div>
            </div>

            <div class="score-line">
                <div class="score-line-label">
                    <span>Experience</span>
                    <strong>91%</strong>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:91%;"></div>
                </div>
            </div>

            <div class="score-line">
                <div class="score-line-label">
                    <span>Education</span>
                    <strong>100%</strong>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:100%;"></div>
                </div>
            </div>

            <div class="score-line">
                <div class="score-line-label">
                    <span>Semantic Similarity</span>
                    <strong>93%</strong>
                </div>
                <div class="score-track">
                    <div class="score-fill" style="width:93%;"></div>
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with detail_right:

    st.markdown(
        """
        <div class="section-title">Match Explanation</div>
        <div class="section-subtitle">
            Why this candidate received the current result
        </div>

        <div class="panel">

            <div style="font-size:0.75rem;font-weight:700;color:#697586;
                        text-transform:uppercase;letter-spacing:0.08em;">
                Strengths
            </div>

            <div style="margin-top:0.65rem;color:#354052;font-size:0.84rem;line-height:1.7;">
                ✓ Python requirement matched<br>
                ✓ SQL requirement matched<br>
                ✓ Minimum experience exceeded<br>
                ✓ Education requirement satisfied<br>
                ✓ Strong semantic similarity
            </div>

            <div style="height:1px;background:#edf0f3;margin:1.2rem 0;"></div>

            <div style="font-size:0.75rem;font-weight:700;color:#697586;
                        text-transform:uppercase;letter-spacing:0.08em;">
                Gaps
            </div>

            <div style="margin-top:0.65rem;color:#354052;font-size:0.84rem;line-height:1.7;">
                • PostgreSQL listed as preferred but not detected
            </div>

            <div style="height:1px;background:#edf0f3;margin:1.2rem 0;"></div>

            <div style="font-size:0.75rem;font-weight:700;color:#697586;
                        text-transform:uppercase;letter-spacing:0.08em;">
                Qualification
            </div>

            <div style="margin-top:0.65rem;color:#354052;font-size:0.84rem;line-height:1.7;">
                Overall score exceeds the configured minimum of 70.
                All mandatory requirements are satisfied.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")
st.write("")


# ---------------------------------------------------------------------
# Resume / job controls
# ---------------------------------------------------------------------

st.markdown(
    """
    <div class="section-title">Evaluate a Candidate</div>
    <div class="section-subtitle">
        Upload a resume and connect it to the active employer-defined job.
    </div>
    """,
    unsafe_allow_html=True,
)

control_left, control_right = st.columns([1, 1], gap="large")

with control_left:

    with st.container(border=True):

        st.markdown("**Employer Job Requirements**")

        job_title = st.text_input(
            "Job title",
            value="Python Developer",
        )

        required_skills = st.text_input(
            "Required skills",
            value="Python, SQL",
        )

        preferred_skills = st.text_input(
            "Preferred skills",
            value="FastAPI, PostgreSQL",
        )

        minimum_experience = st.number_input(
            "Minimum experience (months)",
            min_value=0,
            value=24,
            step=1,
        )


with control_right:

    with st.container(border=True):

        st.markdown("**Candidate Resume**")

        uploaded_resume = st.file_uploader(
            "Upload candidate resume",
            type=["pdf", "docx", "txt"],
        )

        if uploaded_resume:
            st.success(
                f"Resume ready: {uploaded_resume.name}"
            )
        else:
            st.caption(
                "Supported formats: PDF, DOCX, TXT"
            )

        if st.button(
            "Run Candidate Analysis",
            type="primary",
            use_container_width=True,
        ):
            st.info(
                "The dashboard interface is ready. "
                "The resume extraction and matching engine "
                "will be connected next."
            )


st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#8a94a2;font-size:0.72rem;">
        MeritMatch · Candidate intelligence platform ·
        Employer-defined requirements · Human decision support
    </div>
    """,
    unsafe_allow_html=True,
)
