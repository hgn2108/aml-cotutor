# Cotutor: AI Algorithmic Tutor (Visual Edition)

An intelligent tutoring system designed to bridge the gap between **abstract code** and **conceptual understanding**.  
By combining a fine-tuned **Llama-3.1-8B chain-of-thought reasoning model** with **Gemini 2.0 Flash**, the system generates:

- Correct code solutions  
- Structured step-by-step reasoning  
- Dynamic visual flowcharts  
- Pedagogical narrations for LeetCode-style problems  

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

├── app/
│ ├── solver_service.py 
│ ├── app.py
│ └── requirements.txt
├── finetune/
│ ├── cot_finetune.ipynb # SFT notebook
│ ├── finetune_data_engineering.ipynb 
├── visual_explainer.ipynb # Research notebook for diagrams & narration
└── README.md

---

## 🛠️ Setup & Installation

### 1. Prerequisites
You will need API keys for:
- **Google Gemini API** – narration + fallback
- **YouTube Data API v3** – tutorial retrieval
- **Hugging Face Token** – access fine-tuned model on HF Spaces

---

### 2. Environment Variables

**Mac / Linux**
```bash
export GEMINI_API_KEY="your_key_here"
export HF_TOKEN="your_token_here"


Windows (Command Prompt)

set GEMINI_API_KEY=your_key_here
set HF_TOKEN=your_token_here

3. Installation
cd app

# Create virtual environment
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

Running the Application
Step 1: Start the Backend (FastAPI)

Handles model inference, validation, fallback logic, and YouTube search.

python solver_service.py


Backend available at: http://localhost:8000

Step 2: Start the Frontend (Streamlit)

In a new terminal:

cd app
streamlit run app.py


App launches at: http://localhost:8501
