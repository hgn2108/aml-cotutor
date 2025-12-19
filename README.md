# Cotutor: AI Algorithmic Tutor (Visual Edition)

An intelligent tutoring system designed to bridge the gap between **abstract code** and **conceptual understanding**.  
By combining a fine-tuned **Llama-3.1-8B chain-of-thought reasoning model** with **Gemini 2.0 Flash**, the system generates:

- Correct code solutions  
- Structured step-by-step reasoning  
- Dynamic visual flowcharts  
- Pedagogical narrations

## Project Goal

To transform LLMs from black-box code generators into transparent algorithm tutors by making chain-of-thought reasoning explicit, structured, and visual.

---

## ✨ Key Features

- **Hybrid Solver Architecture**  
  Fine-tuned Llama-3.1 for structured CoT reasoning with automatic fallback to Gemini 2.0 Flash for reliability.

- **Visual-First Explanations**  
  Converts reasoning steps into dynamic Matplotlib flowcharts.

- **Agentic Narration**  
  Gemini generates high-level overviews, focus points, and pedagogical captions.

- **Integrated YouTube Tutorials**  
  Fetches relevant video explanations via YouTube Data API v3.

- **Interactive UI**  
  Streamlit-based dual-pane interface for side-by-side logic, code, and visuals.

---

## 📂 Project Structure

```text
├── app/
│   ├── solver_service.py
│   ├── app.py
│   ├── requirements.txt
│   └── utils/
├── finetune/
│   ├── cot_finetune.ipynb
│   └── finetune_data_engineering.ipynb
├── visual_explainer.ipynb
└── README.md

```
---

## 🛠️ Setup & Installation

### 1. Prerequisites
You will need API keys for:
- **Google Gemini API** – narration + fallback
- **YouTube Data API v3** – tutorial retrieval
- **Hugging Face Token** – access fine-tuned model on HF Spaces

---

2. Environment Variables

Set the required keys as environment variables in an .env file. You'll need a Huggingface token, a Gemini API Key/ Youtube API Key, and the Huggingface Space ID for the Space hosting our finetuned model.
```
HF_TOKEN= [Your HF Token]
GEMINI_API_KEY= [Your Gemini key]
HF_SPACE_ID="gsr2149/Leetcode-CoT-model" 
YOUTUBE_API_KEY=[Your Youtube API key]
```

3. Installation
cd app
Step 1: Start the Backend (FastAPI)

Handles model inference, validation, fallback logic, and YouTube search.
```
python solver_service.py
```
Backend available at: http://localhost:8000

Step 2: Start the Frontend (Streamlit)

In a new terminal:

```
cd app
streamlit run app.py
```
The application launches at:
👉 http://localhost:8501
