import re
import os
import json
import textwrap
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import re
from typing import List, Dict, Any
from dotenv import load_dotenv


# --- Configuration ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.0-flash" # Use flash for speed

# --- Schemas ---
class VisualNarration(BaseModel):
    overview: str = Field(description="2-3 sentence overview of the solution in visual terms.")
    diagram_caption: str = Field(description="One short caption explaining what the flowchart shows.")
    focus_points: List[str] = Field(description="Exactly 3 bullet points of what to pay attention to.")

# --- visual_utils.py UPDATE ---
def extract_steps(reasoning: str, max_steps: int = 8) -> List[str]:
    if not reasoning: return []
    
    # Correcting the initialization
    step_blocks = re.findall(
        r"###\s*Step\s*(\d+)\s*:\s*(.*?)(?=\n###\s*Step|\Z)", 
        reasoning, 
        flags=re.DOTALL | re.IGNORECASE
    )

    steps = []
    for num, content in step_blocks:
        lines = content.strip().split('\n')
        title = lines[0].strip()
        # FIX: Full body extraction for better visual filling
        body = " ".join(lines[1:]).strip() if len(lines) > 1 else "Processing..."
        steps.append(f"Step {num}: {title} - {body}")
        
    return steps[:max_steps]

# --- Logic: Visual Narration (Agentic Layer) ---
def generate_visual_narration(problem: str, steps: List[str]) -> Dict[str, Any]:
    """Calls Gemini to produce a high-level conceptual explanation of the steps."""
    system_instruction = (
        "You are a tutor producing a VISUAL explanation. Do NOT change the algorithm. "
        "Describe the steps visually and conceptually. Return JSON matching the schema."
    )
    
    user_prompt = (
        f"Problem:\n{problem}\n\n"
        f"Steps:\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps)]) +
        "\n\nConstraints: Concise output, exactly 3 focus_points."
    )

    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=VisualNarration,
            temperature=0.3
        )
    )
    return VisualNarration.model_validate_json(resp.text).model_dump()

# --- Logic: Flowchart Rendering (Streamlit Compatible) ---
def render_flowchart(steps: list) -> str:
    if not steps: return ""
    
    lines = ["flowchart TD"]
    for i, s in enumerate(steps):
        # 1. Replace double quotes with single to avoid JS breaks
        # 2. Escape backslashes
        # 3. Specifically replace common problematic characters
        clean_text = s.replace('"', "'").replace('\\', '/').replace('`', "'")
        
        # Use ["` text `"] - the backtick inside the bracket is Mermaid's 
        # "multi-line safe" mode which is much more stable for Medium problems
        lines.append(f'    node{i}["`{clean_text.strip()}`"]')
        
        if i < len(steps) - 1:
            lines.append(f"    node{i} --> node{i+1}")
            
    return "\n".join(lines)
            
    return mermaid_code
    # This would be called in app.py using st.graphviz_chart()
    return dot_code