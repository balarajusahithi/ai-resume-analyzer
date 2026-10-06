import streamlit as st
import re
from pypdf import PdfReader
from docx import Document


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------------------
# SKILLS DATABASE
# -----------------------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "streamlit",
    "django",
    "flask",
    "fastapi",
    "rest api",
    "docker",
    "git",
    "github",
    "aws",
    "azure",
    "power bi",
    "tableau",
    "nlp",
    "natural language processing"
]


# -----------------------------------------
# EXTRACT TEXT FROM PDF
# -----------------------------------------

def extract_pdf_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------------------
# EXTRACT TEXT FROM DOCX
# -----------------------------------------

def extract_docx_text(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


# -----------------------------------------
# EXTRACT RESUME TEXT
# -----------------------------------------

def extract_resume_text(file):

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file)

    elif file_name.endswith(".docx"):
        return extract_docx_text(file)

    elif file_name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        return ""


# -----------------------------------------
# FIND SKILLS
# -----------------------------------------

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))


# -----------------------------------------
# CALCULATE MATCH SCORE
# -----------------------------------------

def calculate_score(resume_skills, job_skills):

    if not job_skills:
        return 0

    matching_skills = set(resume_skills).intersection(
        set(job_skills)
    )

    score = (len(matching_skills) / len(job_skills)) * 100

    return round(score, 2)


# -----------------------------------------
# MAIN UI
# -----------------------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and enter a job description "
    "to analyze your resume."
)


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.header("Resume Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)


# -----------------------------------------
# JOB DESCRIPTION
# -----------------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=250,
    placeholder="Example: We are looking for a Python Developer..."
)


# -----------------------------------------
# ANALYZE BUTTON
# -----------------------------------------

if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:

        st.error("Please upload your resume.")

    elif not job_description.strip():

        st.error("Please enter a job description.")

    else:

        # Extract resume text
        resume_text = extract_resume_text(uploaded_file)

        if not resume_text.strip():

            st.error(
                "Could not extract text from the resume."
            )

        else:

            # Find skills
            resume_skills = find_skills(resume_text)

            job_skills = find_skills(job_description)

            # Matching skills
            matching_skills = sorted(
                set(resume_skills).intersection(
                    set(job_skills)
                )
            )

            # Missing skills
            missing_skills = sorted(
                set(job_skills) - set(resume_skills)
            )

            # Calculate score
            score = calculate_score(
                resume_skills,
                job_skills
            )

            # -----------------------------------------
            # RESULTS
            # -----------------------------------------

            st.divider()

            st.header("📊 Analysis Result")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Resume Match Score",
                    f"{score}%"
                )

            with col2:
                st.metric(
                    "Matching Skills",
                    len(matching_skills)
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    len(missing_skills)
                )

            # -----------------------------------------
            # MATCHING SKILLS
            # -----------------------------------------

            st.subheader("✅ Matching Skills")

            if matching_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in matching_skills
                    )
                )

            else:

                st.write("No matching skills found.")

            # -----------------------------------------
            # MISSING SKILLS
            # -----------------------------------------

            st.subheader("❌ Missing Skills")

            if missing_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in missing_skills
                    )
                )

            else:

                st.success(
                    "Your resume contains all detected job skills!"
                )

            # -----------------------------------------
            # RESUME SKILLS
            # -----------------------------------------

            st.subheader("🧑‍💻 Skills Found in Resume")

            if resume_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in resume_skills
                    )
                )

            else:

                st.warning(
                    "No known skills were detected."
                )

            # -----------------------------------------
            # RECOMMENDATION
            # -----------------------------------------

            st.subheader("💡 Recommendation")

            if score >= 80:

                st.success(
                    "Excellent match! Your resume is "
                    "highly suitable for this job."
                )

            elif score >= 60:

                st.info(
                    "Good match. Consider adding the "
                    "missing skills to improve your resume."
                )

            elif score >= 40:

                st.warning(
                    "Moderate match. Your resume needs "
                    "some improvement for this job."
                )

            else:

                st.error(
                    "Low match. Consider developing the "
                    "required skills before applying."
                )

            # -----------------------------------------
            # SUGGESTIONS
            # -----------------------------------------

            st.subheader("📝 Resume Improvement Suggestions")

            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"• Consider learning or adding "
                        f"**{skill.title()}** if you have "
                        f"experience with it."
                    )

            st.write(
                "• Add measurable achievements to your projects."
            )

            st.write(
                "• Mention relevant technical skills clearly."
            )

            st.write(
                "• Keep your resume concise and "
                "job-specific."
            )

            # -----------------------------------------
            # RESUME PREVIEW
            # -----------------------------------------

            with st.expander("📄 View Extracted Resume Text"):

                st.text(resume_text)