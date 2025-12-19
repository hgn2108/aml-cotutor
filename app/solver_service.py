import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from gradio_client import Client
from googleapiclient.discovery import build 
from dotenv import load_dotenv
# Gemini Imports
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()
# --- 1. CONFIGURATION ---
HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_SPACE_ID = os.getenv("HF_SPACE_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# --- 2. SCHEMAS ---
class CoTSolverOutput(BaseModel):
    reasoning: str
    answer: str

class ProblemRequest(BaseModel):
    problem: str

# --- 3. CLIENT SETUP ---
app = FastAPI(title="LeetCode Hybrid Solver Service")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize the Gradio client (does NOT load model locally)
hf_space_client = Client(HF_SPACE_ID)

# --- 4. NEW: AGENTIC VIDEO TOOL ---
def get_tutorial_video(problem_text: str) -> Optional[str]:
    """Uses Gemini to generate a search query and finds the best YouTube video."""
    try:
        # 1. Ask Gemini to generate the 'perfect' search query
        query_prompt = (
            f"Given this coding problem: '{problem_text}', "
            "generate a concise YouTube search query to find the best high-quality "
            "video tutorial (e.g., NeetCode or similar). Output ONLY the query string."
        )
        query_resp = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query_prompt
        )
        search_query = query_resp.text.strip().replace('"', '')

        # 2. Call YouTube API
        youtube = build("youtube", "v3", developerKey="AIzaSyCYGNwzcpcF_5ZjI99t5JhxEooQc0n_xco")
        request = youtube.search().list(
            q=search_query,
            part="id,snippet",
            maxResults=1,
            type="video"
        )
        response = request.execute()

        if response.get("items"):
            video_id = response["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"YouTube Tool Error: {e}")
    return None

# --- 5. GEMINI FALLBACK ---
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def call_gemini_fallback(problem_text: str) -> Dict[str, Any]:
    system_instruction = (
        "Solve the problem. In your 'reasoning' field, you MUST break the logic into steps "
        "using the format '### Step X: Title\nDescription'. This is required for visualization."
    )
    
    resp = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Solve this problem: {problem_text}",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=CoTSolverOutput
        )
    )
    return json.loads(resp.text)

# --- 6. THE HYBRID ENDPOINT ---
@app.post("/solve")
async def solve(request: ProblemRequest):
    result = None
    source = "HF_Space_Model"

    # Fetch Solution
    try:
        prediction = hf_space_client.predict(request.problem, api_name="/predict")
        if isinstance(prediction, str):
            result = json.loads(prediction)
        else:
            result = prediction
    except Exception as e:
        print(f"HF Space Inference failed: {e}")

    if not result or not result.get("reasoning"):
        result = call_gemini_fallback(request.problem)
        source = "Gemini_Fallback"

    # Fetch Video (Agentic Step)
    video_url = get_tutorial_video(request.problem)

    return {
        "status": "success", 
        "source": source, 
        "video_url": video_url, # <--- Included in response
        **result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
