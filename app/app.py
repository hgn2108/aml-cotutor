import streamlit as st
import requests
import visual_utils
import streamlit.components.v1 as components

# --- App Config ---
st.set_page_config(page_title="AI Algorithmic Tutor", layout="wide")
SOLVER_URL = "http://localhost:8000/solve"

st.title("CoTutor: AI Algorithmic Tutor")
st.markdown("Enter a LeetCode-style problem below. Our fine-tuned Llama model will solve it, and Gemini will explain it visually.")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    show_reasoning = st.checkbox("Show Raw Chain-of-Thought", value=False)
    st.info("The system uses Llama-3.1 (Fine-tuned) primarily, with a Gemini fallback.")

# --- User Input ---
problem_input = st.text_area("Problem Description:", placeholder="e.g., Given an array of integers, return indices of the two numbers such that they add up to a specific target.", height=150)

if st.button("Solve & Explain"):
    if not problem_input:
        st.warning("Please enter a problem description.")
    else:
        with st.spinner("🧠 Model is thinking..."):
            try:
                # 1. Call the Solver Service (FastAPI)
                response = requests.post(SOLVER_URL, json={"problem": problem_input})
                data = response.json()
                
                if data.get("status") == "success":
                    # --- EXTRACT DATA ---
                    reasoning = data["reasoning"]
                    answer = data["answer"]
                    source = data["source"]
                    video_url = data.get("video_url")  # <--- NEW: Extract video URL

                    # 2. Extract Steps & Generate Visuals
                    steps = visual_utils.extract_steps(reasoning)
                    narration = visual_utils.generate_visual_narration(problem_input, steps)
                    mermaid_code = visual_utils.render_flowchart(steps)

                    # --- UI LAYOUT ---
                    st.success(f"Solution generated via: {source}")
                    
                    # NEW: Add Video to Sidebar dynamically
                    if video_url:
                        with st.sidebar:
                            st.divider()
                            st.subheader("📺 Recommended Tutorial")
                            st.video(video_url)
                            st.caption("External tutorial found for this problem.")

                    col1, col2 = st.columns([1, 1])

                    # --- Inside app.py, under 'with col1:' ---
                    with col1:
                        st.subheader("💡 Visual Explanation")
                        st.write(narration["overview"])
                        st.info(f"**Caption:** {narration['diagram_caption']}")
                        
                        st.markdown("**Key Takeaways:**")
                        for point in narration["focus_points"]:
                            st.markdown(f"- {point}")
                        
                        # --- Inside app.py, under col1 ---
                        if mermaid_code:
                            html_content = f"""
                            <div style="height: 450px; overflow-y: auto; border: 1px solid #e6e9ef; border-radius: 8px;">
                                <div class="mermaid" style="text-align: left; padding: 10px;">
                                    {mermaid_code}
                                </div>
                            </div>

                            <script type="module">
                                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
                                mermaid.initialize({{ 
                                    startOnLoad: true, 
                                    theme: 'base',
                                    themeVariables: {{
                                        'primaryColor': '#e1f5fe',    /* Your light blue box background */
                                        'primaryBorderColor': '#01579b',
                                        'lineColor': '#333',
                                        'fontSize': '14px'
                                    }},
                                    flowchart: {{ 
                                        useMaxWidth: false, /* Keeps it left-aligned */
                                        htmlLabels: true 
                                    }} 
                                }});
                            </script>
                            """
                            components.html(html_content, height=470) 
                    with col2:
                        st.subheader("💻 Python Solution")
                        st.code(answer, language="python")
                        
                        if show_reasoning:
                            with st.expander("View Raw Reasoning"):
                                st.markdown(reasoning)

                else:
                    st.error(f"Solver Error: {data.get('detail')}")

            except Exception as e:
                st.error(f"Connection Error: Could not reach Solver Service. Ensure solver_service.py is running. Error: {e}")