import os
import tempfile
import datetime
import textwrap

import gradio as gr
from fpdf import FPDF
from langchain_google_genai import ChatGoogleGenerativeAI

#  Config: Gemini 2.0 Flash

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not set. "
        "Add it in your Space settings under 'Secrets'."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=GOOGLE_API_KEY,
)

#  Base ATS-friendly resume template

BASE_RESUME_TEMPLATE = """
Aakash Malhan | Data Scientist
Tempe, AZ • website • LinkedIn • GitHub • a.malhan64@gmail.com • (623) 920-3728
EDUCATION AND HONORS
W. P. Carey School of Business at Arizona State University              Aug 2024 - May 2025
MS, Business Analytics
- Coursework: Python, SQL, Statistics, Machine Learning, Business Process Modeling, Data Visualization, Deep Learning
Maharshi Dayanand University                                           Jul 2016 - Jun 2019
Bachelor of Science, Mathematics
- Coursework: Advanced Calculus, Linear Algebra, Probability and Statistics, Optimization, Differential Equations
PROFESSIONAL EXPERIENCE
Capital Steel Corporation | Operations Analyst (Data Science in Ops)   Gurugram, India | Nov 2019 - Dec 2022
- Cut purchasing costs 25 percent and accelerated vendor selection 2x by translating procurement and logistics data into insights using Python, SQL and statistical analysis, saving over 1M dollars annually.
- Built anomaly detection (Isolation Forest) and vendor-ranking models on multi-year procurement data; cut false positives by 30 percent and improved vendor decisions by 20 percent.
- Implemented predictive scheduling and batching in procurement workflows to shorten cycle times by 20 percent across teams.
- Drove 550k dollars budget reallocation by delivering quarterly ML driven procurement insights to CFO and VP Supply Chain.
W. P. Carey School of Business at ASU | Research Assistant              Tempe, AZ | Jul 2025 - Present
- Engineered a 70 year U.S. macroeconomic dataset (1954-2025) from FRED and BLS (unemployment, inflation, GDP, policy rates) using Python, reducing manual data prep time by 60 percent.
- Detected 7 major structural breaks in inflation (including the 1980 Volcker transition) using CUSUM and Chow tests; quantified lead lag dynamics among key indicators, boosting analytical accuracy and transmission insights by 40 percent plus.
PROJECTS
Google Search Console Query Anomaly Detector | Python, pandas, NumPy, scikit-learn (IsolationForest), Plotly, Gradio
- Built an end to end anomaly detection app to analyze 1000 plus under performing Google Search queries using CTR gap and log scaled features (CTR vs Position correlation r = -0.73).
- Flagged about 1 percent high risk queries with low CTR vs expected; enabled 15-35 percent CTR lift on priority keywords and cut manual monitoring time by about 80 percent via dashboard and anomalies.csv export.
Medical RAG for COVID-19 | Python, Gradio, RAG, Gemini 2.0 Flash API, FAISS, pandas, sentence-transformers
- Developed a Medical RAG assistant on 40k plus CORD-19 papers that retrieves and summarizes the most relevant research for a given clinical question (non diagnostic).
- Cut literature triage time by about 60 percent via instant retrieval of risk factors and studies.
User Growth and Retention Analytics Platform with A/B Testing | Python, pandas, NumPy, SciPy, CUPED and SRM
- Built an experimentation engine analyzing onboarding, activation and retention funnels.
- Measured 99.7 percent activation, 2.9 percent day 7 retention, and 11.5 percent lift in engagement, informing strategies for early retention and feature rollout decisions.
NYC Dynamic Pricing and Driver Incentive Engine | Python, NYC TLC data, XGBoost, DuckDB, Gradio UI, GitHub
- Engineered a surge pricing model on 10M plus taxi rides to optimize fares, incentives and ETA reliability.
- Delivered 12-38 percent simulated revenue uplift with SHAP explainability heatmaps and a production grade UI.
CORE COMPETENCIES
- A/B Testing, Classification, Regression, NLP, Time Series, Anomaly Detection, Feature Engineering, SHAP, Causal Inference, Statistical Modeling, CUPED and SRM
- AWS, GCP, Azure, APIs, Docker, GitHub Actions, Kubernetes, LangChain, RAG, LLMs
- Python, SQL, pandas, NumPy, scikit-learn, dbt, Snowflake, Tableau, ETL, Data Analytics, Experimentation
CERTIFICATIONS
- Lean Six Sigma Green Belt
- AWS Intro to Generative Artificial Intelligence
- Microsoft Azure Data Scientist Associate
- AWS Machine Learning
"""

#  One-page enforcement helper

def enforce_one_page(text: str, max_lines: int = 65) -> str:
    """
    Keep the resume to roughly one page by limiting the number of lines.
    If the model returns more, we truncate and append a note.
    """
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text

    trimmed = lines[:max_lines]
    trimmed.append("... [trimmed to keep resume to one page]")
    return "\n".join(trimmed)

#  PDF helper (Latin-1 safe + one page)

def save_resume_pdf(text: str, job_title: str) -> str:
    """
    Save the tailored resume text to a simple, ATS-friendly PDF.
    FPDF 1.x only supports Latin-1, so we strip unsupported characters
    and enforce a one-page length.
    """
    # Enforce one-page constraint
    text = enforce_one_page(text, max_lines=65)

    # Normalize to Latin-1 (drop unsupported characters)
    safe_text = text.encode("latin-1", "ignore").decode("latin-1")

    safe_title = "".join(c for c in job_title if c.isalnum() or c in ("_", "-")) or "role"
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tailored_resume_{safe_title}_{ts}.pdf"
    pdf_path = os.path.join(tempfile.gettempdir(), filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)  # core font, ATS-safe

    for line in safe_text.split("\n"):
        wrapped_lines = textwrap.wrap(line, width=95) or [""]
        for wline in wrapped_lines:
            pdf.multi_cell(0, 5, wline)
        if not line.strip():
            pdf.ln(2)

    pdf.output(pdf_path)
    return pdf_path

#  Core function: JD -> tailored resume

def generate_tailored_resume(job_title, company, location, url, jd_text):
    if not jd_text or not jd_text.strip():
        return "⚠️ Please paste a job description.", None

    job_title_clean = (job_title or "").strip() or "Data Scientist"
    company_clean = (company or "").strip() or "Unknown Company"
    location_clean = (location or "").strip() or "Unknown Location"
    url_clean = (url or "").strip()

    prompt = f"""
You are an expert FAANG style resume writer.
Below is Aakash's current ATS friendly 1 page resume template. It already has an optimized layout.
RESUME TEMPLATE (KEEP THIS STRUCTURE)
-------------------------------------
{BASE_RESUME_TEMPLATE}
TARGET JOB
----------
Title: {job_title_clean}
Company: {company_clean}
Location: {location_clean}
URL: {url_clean}
JOB DESCRIPTION
---------------
{jd_text}
TASK
----
Rewrite ONLY the content inside this template to better match the TARGET JOB, while keeping the structure and formatting as close as possible to the template:
- Keep the same section order and headings:
  "EDUCATION AND HONORS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "CORE COMPETENCIES", "CERTIFICATIONS".
- Keep the first header line format: "Aakash Malhan | Data Scientist | Tempe, AZ • ...".
- Keep company and role lines on their own line, followed by bullet points that start with "- ".
- Use plain ASCII style characters (no fancy bullets or quotes).
- Keep total length around 550-650 words so it fits on ONE page at 10-11pt font.
- Do NOT add new sections.
- You may lightly tweak bullet phrasing and emphasis to highlight skills and impact relevant to the target job
  (for example experimentation for product roles, LLM work for AI roles), but do not invent completely new experience.
Output ONLY the final resume text in this template format, nothing else.
"""

    # Call Gemini
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        return f"❌ Error calling Gemini:\n{repr(e)}", None

    tailored_resume = getattr(response, "content", None)
    if not tailored_resume:
        return "❌ Gemini returned an empty response.", None

    # Enforce one-page limit for both display and PDF
    tailored_resume = enforce_one_page(tailored_resume, max_lines=65)

    # Generate PDF
    try:
        pdf_path = save_resume_pdf(tailored_resume, job_title_clean)
    except Exception as e:
        error_msg = f"\n\n[⚠️ PDF generation error: {repr(e)}]"
        return tailored_resume + error_msg, None

    return tailored_resume, pdf_path

#  Gradio UI

with gr.Blocks() as demo:
    gr.Markdown(
        """
# AI Job Application Agent – JD → ATS-Friendly Tailored Resume
Paste any job description, and the app will:
1. Read your base resume template,
2. Tailor the bullets and emphasis for that specific role,
3. Keep the 1-page ATS-friendly layout, and
4. Give you both the text and a downloadable PDF.
        """
    )

    with gr.Row():
        with gr.Column():
            job_title = gr.Textbox(
                label="Job title",
                placeholder="e.g., Data Scientist, Product Analytics",
            )
            company = gr.Textbox(
                label="Company",
                placeholder="e.g., Meta",
            )
            location = gr.Textbox(
                label="Location",
                placeholder="e.g., New York / Remote",
            )
            url = gr.Textbox(
                label="Job URL (optional)",
                placeholder="Link to the job posting",
            )
            jd_text = gr.TextArea(
                label="Job description",
                placeholder="Paste the full JD here (responsibilities, minimum and preferred qualifications, etc.)",
                lines=18,
            )
            generate_btn = gr.Button("Generate tailored resume", variant="primary")

        with gr.Column():
            tailored_out = gr.TextArea(
                label="Tailored resume (ATS-friendly text)",
                lines=28,
            )
            pdf_file = gr.File(
                label="Download PDF",
            )

    generate_btn.click(
        fn=generate_tailored_resume,
        inputs=[job_title, company, location, url, jd_text],
        outputs=[tailored_out, pdf_file],
    )

if __name__ == "__main__":
    demo.launch()
