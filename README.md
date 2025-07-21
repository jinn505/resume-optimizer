
# 🧠 AI-Powered Resume Optimizer and ATS checker

This project is an intelligent, multi-agent **Resume Optimizer** built using **FastAPI**, **CrewAI**, and **openrouter's deepseek/deepseek-chat:free** model. It enhances your resume by generating sharp, tailored bullet points aligned with any job description (JD) — ideal for boosting your chances with recruiters and ATS systems.

---

## 🚀 Features

- 📄 Accepts resume and job description files in `.pdf` or `.txt` format
- 🧠 Uses autonomous agents (Analyzer, Optimizer, Writer) via CrewAI
- ✍️ Generates **3 impactful bullet points per experience or project**
- 🎯 Ensures JD alignment and technical relevance
- ⚡ Powered by openrouter’s deepseek/deepseek-chat:free for blazing-fast generation
- 🌐 Easy API access with FastAPI
- 👊 ATS checker to check if your resume is good enough to shortlist you for the job.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI  
- **LLM Provider:** Openrouter (mistralai/mistral-7b-instruct & deepseek/deepseek-chat:free)  
- **Agent Orchestration:** CrewAI  
- **LangChain Integration:** Langchain + OutputParser  
- **File Handling:** PyMuPDF, PDFplumber   

---

## 📁 Project Structure

```
resume-agent/
├── app/
│   ├── agents/              # CrewAI agents: extractor, extractor_ats,analyzer, optimizer, writer, refiner
│   ├── utils/               # Helpers: file parsing, formatting, etc.
│   ├── docs/                # Uploaded resumes and JDs
│   ├── main.py              # FastAPI backend
│   └── final_optimizer.py   # CrewAI orchestration logic
├── .env                     # GROQ_API_KEY goes here
├── .gitignore
├── requirements.txt
├── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/jinn505/resume-optimizer.git
cd resume-optimizer
```

### 2. Set Up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add Your API Key

Create a `.env` file in the root and add:

```
GROQ_API_KEY=your-groq-api-key
```

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

### 6. Use the API

Go to `http://127.0.0.1:8000/docs` and upload your resume and JD to get optimized bullet points.

---

## 🧱 Upcoming Enhancements

- 🧩 JD Insight Extractor Agent  
- ✂️ Bullet Refiner Agent (brevity, tone)  
- 🧠 Long-term vector memory using Qdrant  
- 📦 Docker containerization & Render deployment

---

## 🤝 Contributing

Pull requests and feature ideas are welcome! Feel free to fork the repo and open an issue to discuss changes.

---
