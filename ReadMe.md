🚀 AI-Powered ATS Resume Builder & Career Assistant

An end-to-end AI Resume Optimization Platform that parses resumes, generates missing job descriptions, calculates ATS scores, enhances resume content using LLMs, and converts everything into professional ATS-optimized PDF resumes using LaTeX (MiKTeX).

Built with FastAPI, Groq LLMs, Jina Embeddings, and LaTeX automation.

🌟 Key Features

📄 Resume Parsing

Extracts structured information from PDF & DOCX resumes.

🧠 Auto Job Description Generator

Generates realistic job descriptions using Groq LLaMA-3.3 when JD is missing.

📊 ATS Score Engine

Uses Jina Embeddings to compute semantic similarity between resume & JD.

✨ AI Resume Enhancer

Improves grammar, tone, and keyword alignment without altering resume structure.

🧾 ATS-Optimized LaTeX Resume Builder

Fills pre-designed LaTeX templates and compiles them locally via MiKTeX pdflatex.

📑 Multi-Template System

Supports multiple ATS-friendly resume templates.

🏗 Tech Stack
Layer	Tools
Backend	FastAPI
LLM	Groq – LLaMA-3.3-70B
Embeddings	Jina AI
Resume Parsing	PyMuPDF, python-docx
Resume Enhancement	Groq Chat Completions
PDF Generation	LaTeX + MiKTeX pdflatex
ATS Scoring	Cosine Similarity (Semantic)
🧠 System Architecture
Resume Upload → Resume Parser → (Optional) JD Generator
                        ↓
                  ATS Scorer
                        ↓
              AI Resume Enhancer
                        ↓
          LaTeX Template Filler
                        ↓
               pdflatex (MiKTeX)
                        ↓
                 Final ATS PDF

⚙ Setup Instructions (MiKTeX Local LaTeX Build)
1️⃣ Install MiKTeX

Download and install MiKTeX:

👉 https://miktex.org/download

Verify installation:

pdflatex --version

2️⃣ Clone Repository
git clone https://github.com/your-username/ai-resume-ats.git
cd ai-resume-ats

3️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

4️⃣ Setup .env
GROQ_API_KEY=your_groq_key
JINA_API_KEY=your_jina_key

5️⃣ Run Server
uvicorn test_parser:app --reload


Open:
👉 http://127.0.0.1:8000/docs

📥 API Endpoints
Endpoint	Description
/test_upload	Parse Resume
/ats	ATS Score
/enhance_resume	AI Resume Enhancement
/build_resume_pdf	Generate ATS-Optimized Resume PDF
🧪 Example Request

Upload resume → auto-generate JD → get ATS score → generate professional resume PDF.

📈 Why Recruiters Love This Project

Solves real industry pain point – ATS rejection.

Combines LLMs + Embeddings + Automation + LaTeX.

Demonstrates Agentic AI workflow.

Shows ability to design end-to-end AI systems, not toy scripts.

🛠 Future Improvements

Frontend with React / Gradio

Cover letter generator

Resume keyword heatmap visualization

Resume version comparison

👨‍💻 Author

Arya Yemul
AI & Data Science Engineer | Career Guidance Bot Developer