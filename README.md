# AI Application Agent – ATS-Friendly Resume Tailor (Gemini 2.0 Flash)

Paste any job description. Get an ATS-friendly, **1-page tailored resume** aligned to that role in seconds.

This app uses **Gemini 2.0 Flash + LangChain + Gradio** to rewrite a base resume into a tightly-structured template that hiring systems can parse and recruiters can skim quickly.

<img width="1423" height="791" alt="Screenshot 2025-11-17 211621" src="https://github.com/user-attachments/assets/5dae518b-aa3c-4e75-83ac-c4afd856032a" />



##  Business Problem

Modern job search is broken:

- Every role (Data Scientist, ML Engineer, AI Engineer, Product Analyst, etc.) expects a **customized resume**.
- Manually tailoring your CV for each posting is slow and error-prone.
- Many AI tools generate “pretty” resumes, but:
  - They **break ATS formatting**,
  - Produce multi-page walls of text, or
  - Invent experience that doesn’t match the candidate’s background.

**Goal:**  
Automate resume tailoring so a candidate can go from *job description* → *1-page, ATS-friendly resume* in under a minute, **without losing realism or structure**.

## 💡 Solution at a Glance

This project is an **AI application agent** that:

1. Takes a **structured base resume template**.
2. Accepts any **job description** (Meta, Google, startups, etc.).
3. Uses **Gemini 2.0 Flash** to:
   - Re-phrase bullets and highlight relevant achievements,
   - Emphasize skills and projects that best match the JD,
   - Keep sections, headings, and layout identical to the original template.
  
## 🛠 Tech Stack

**Core AI & Orchestration**

- **Gemini 2.0 Flash** – LLM used for controlled resume rewriting.
- **LangChain Google GenAI** – wrapper to call Gemini from Python and manage prompts.

**Application Layer**

- **Gradio** – web UI on Hugging Face Spaces (text inputs + JD textarea + PDF download).
- **Python** – glue code, business logic, JD handling, and template control.
- **FPDF** – lightweight PDF generation for the final 1-page resume.

**Infrastructure**

- **Hugging Face Spaces (Gradio SDK)** – deployment & hosting.


## 📊 Business Impact / Problem Solved

> Numbers are illustrative and can be updated based on real usage analytics.

- **60–80% faster** per application  
  Automates the most time-consuming part of job search (rewriting bullets & reordering skills), letting users go from JD to tailored resume in under a minute instead of ~20–30 minutes manually.

- **Consistent ATS-friendly formatting**  
  Keeps a strict 1-page template: clear headings, simple bullets, and no complex layouts. This reduces the risk of resumes being rejected by parsing systems due to non-standard formats.

- **Higher relevance per application**  
  By aligning experience, projects, and skills directly to the posted role (e.g., experimentation for Product Data Scientist vs. LLMs for AI Engineer), candidates present a sharper story to recruiters, improving **screen-in rates** and **interview conversions**.

- **Scalable personalization**  
  Candidates can generate dozens of tailored resumes across Data Science / ML / AI / Analytics roles without burning out, making it viable to apply widely while staying genuinely customized.
