import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


load_dotenv()


client = InferenceClient(
    api_key=os.getenv("HF_TOKEN"),
    provider="auto"
)


st.set_page_config(
    page_title="CodeMentor AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

::selection {
    background: rgba(99, 102, 241, 0.4) !important;
    color: #ffffff !important;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.15), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(59, 130, 246, 0.10), transparent 35%),
        #080a12;
}

/* Remove default top padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Hero section */
.hero {
    text-align: center;
    padding: 35px 20px 30px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 30px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(129, 140, 248, 0.35);
    color: #a5b4fc;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 58px;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, #ffffff, #a5b4fc, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #a1a1aa;
    font-size: 18px;
    margin-top: 14px;
}

/* ------------------------------------------------------------- */
/* ROTATING GLOWING BORDER ANIMATION SETUP                       */
/* ------------------------------------------------------------- */

@property --border-angle {
    syntax: "<angle>";
    inherits: false;
    initial-value: 0deg;
}

@keyframes rotate-border {
    0% {
        --border-angle: 0deg;
    }
    100% {
        --border-angle: 360deg;
    }
}

/* Feature cards - equal width and perfectly aligned inside Streamlit columns */
[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    align-items: stretch !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    width: 0 !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="column"] > div {
    width: 100% !important;
    min-width: 0 !important;
}

.feature-card {
    position: relative;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;

    border-radius: 18px;
    padding: 22px 24px;
    min-height: 170px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    backdrop-filter: blur(12px);
    transition: transform 0.3s ease;

    /* Sharp rotating border beam - cool cyber palette, no red */
    border: 2px solid transparent;
    background:
        linear-gradient(
            135deg,
            rgba(14, 17, 30, 0.95),
            rgba(9, 11, 20, 0.98)
        ) padding-box,
        conic-gradient(
            from var(--border-angle),
            rgba(99, 102, 241, 0.15) 0deg,
            #6366f1 60deg,
            #8b5cf6 120deg,
            #06b6d4 180deg,
            #3b82f6 240deg,
            rgba(99, 102, 241, 0.15) 360deg
        ) border-box;
    animation: rotate-border 4s linear infinite;
}

/* 2. Outer glowing aura rotating in sync with the border */
.feature-card::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 20px;
    background: conic-gradient(
        from var(--border-angle),
        transparent 0deg,
        rgba(99, 102, 241, 0.7) 60deg,
        rgba(139, 92, 246, 0.8) 120deg,
        rgba(6, 182, 212, 0.8) 180deg,
        rgba(59, 130, 246, 0.7) 240deg,
        transparent 360deg
    );
    z-index: -1;
    filter: blur(14px);
    opacity: 0.55;
    animation: rotate-border 4s linear infinite;
    pointer-events: none;
    transition: opacity 0.3s ease, filter 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
}

.feature-card:hover::after {
    opacity: 0.95;
    filter: blur(18px);
}

.feature-icon {
    font-size: 28px;
    line-height: 1;
    margin-bottom: 2px;
}

.feature-title {
    color: white;
    font-weight: 700;
    font-size: 17px;
    margin-top: 8px;
    margin-bottom: 6px;
    line-height: 1.25;
}

.feature-text {
    color: #9ca3af;
    font-size: 13.5px;
    line-height: 1.45;
    margin: 0;
}

/* Section headings */
.section-title {
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin-top: 28px;
    margin-bottom: 12px;
}

/* Labels */
label {
    color: #d4d4d8 !important;
    font-weight: 600 !important;
}

/* Select boxes - remove any default red focus/borders */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(129, 140, 248, 0.25) !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:hover {
    border-color: #818cf8 !important;
    box-shadow: 0 0 12px rgba(129, 140, 248, 0.25) !important;
}

/* ------------------------------------------------------------- */
/* CODE TEXT AREA: CONTINUOUS ROTATING GLOWING BORDER & TRANSITION */
/* ------------------------------------------------------------- */

/* Suppress all Streamlit default red borders, outlines and focus rings */
.stTextArea,
.stTextArea [data-testid="stTextAreaRootElement"],
.stTextArea [data-testid="stTextAreaRootElement"]:focus-within,
.stTextArea > div:has(textarea),
.stTextArea > div:has(textarea):focus-within,
.stTextArea textarea,
.stTextArea textarea:focus,
.stTextArea textarea:focus-visible,
div[data-baseweb="textarea"],
div[data-baseweb="textarea"]:focus-within {
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}

/* The code textarea box: continuous rotating glowing border & hover lift */
[data-testid="stTextAreaRootElement"],
.stTextArea > div:has(textarea),
div[data-baseweb="textarea"] {
    position: relative !important;
    border-radius: 16px !important;
    border: 2px solid transparent !important;
    background: 
        /* Solid dark interior keeps code typing area clean & readable */
        linear-gradient(135deg, rgba(14, 17, 30, 0.96), rgba(9, 11, 20, 0.98)) padding-box,
        /* Rotating cool neon beam strictly on the border - no red! */
        conic-gradient(
            from var(--border-angle),
            rgba(99, 102, 241, 0.15) 0deg,
            #6366f1 60deg,
            #8b5cf6 120deg,
            #06b6d4 180deg,
            #3b82f6 240deg,
            rgba(99, 102, 241, 0.15) 360deg
        ) border-box !important;
    animation: rotate-border 4s linear infinite !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

/* Outer glowing aura rotating continuously around the border */
[data-testid="stTextAreaRootElement"]::after,
.stTextArea > div:has(textarea)::after,
div[data-baseweb="textarea"]::after {
    content: '' !important;
    position: absolute !important;
    inset: -2px !important;
    border-radius: 18px !important;
    background: conic-gradient(
        from var(--border-angle),
        transparent 0deg,
        rgba(99, 102, 241, 0.7) 60deg,
        rgba(139, 92, 246, 0.8) 120deg,
        rgba(6, 182, 212, 0.8) 180deg,
        rgba(59, 130, 246, 0.7) 240deg,
        transparent 360deg
    ) !important;
    z-index: -1 !important;
    filter: blur(14px) !important;
    opacity: 0.55 !important;
    animation: rotate-border 4s linear infinite !important;
    pointer-events: none !important;
    transition: opacity 0.3s ease, filter 0.3s ease !important;
}

/* Hover effect: smooth lift and enhanced glow transition */
[data-testid="stTextAreaRootElement"]:hover,
.stTextArea > div:has(textarea):hover,
div[data-baseweb="textarea"]:hover {
    transform: translateY(-2px) !important;
}

[data-testid="stTextAreaRootElement"]:hover::after,
.stTextArea > div:has(textarea):hover::after,
div[data-baseweb="textarea"]:hover::after {
    opacity: 0.85 !important;
    filter: blur(18px) !important;
}

/* Focus effect: brighter glow when typing */
[data-testid="stTextAreaRootElement"]:focus-within,
.stTextArea > div:has(textarea):focus-within,
div[data-baseweb="textarea"]:focus-within {
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.3), 0 0 30px rgba(6, 182, 212, 0.2) !important;
}

[data-testid="stTextAreaRootElement"]:focus-within::after,
.stTextArea > div:has(textarea):focus-within::after,
div[data-baseweb="textarea"]:focus-within::after {
    opacity: 0.95 !important;
    filter: blur(20px) !important;
}

/* Internal Streamlit wrapper - keep transparent */
[data-testid="stTextAreaRootElement"] > div,
div[data-baseweb="base-input"],
div[data-baseweb="base-input"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Actual textarea — clean typing interior */
.stTextArea textarea {
    background: transparent !important;
    color: #e4e4e7 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    font-family: 'Consolas', 'Courier New', monospace !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 18px !important;
    resize: vertical !important;
}

.stTextArea textarea:focus,
.stTextArea textarea:focus-visible {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Analyze button */
.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: 1px solid rgba(129,140,248,0.5);
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 16px;
    font-weight: 700;
    transition: 0.25s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.35);
    border-color: #818cf8;
    color: white;
}

.stButton > button:active,
.stButton > button:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4) !important;
    color: white !important;
    outline: none !important;
}

/* Result box with matching cool cyber rotating border glow */
.result-box {
    position: relative;
    border-radius: 18px;
    padding: 28px;
    margin-top: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    
    border: 2px solid transparent;
    background: 
        linear-gradient(135deg, rgba(14, 17, 30, 0.95), rgba(9, 11, 20, 0.98)) padding-box,
        conic-gradient(
            from var(--border-angle),
            rgba(99, 102, 241, 0.15) 0deg,
            #6366f1 60deg,
            #8b5cf6 120deg,
            #06b6d4 180deg,
            #3b82f6 240deg,
            rgba(99, 102, 241, 0.15) 360deg
        ) border-box;
    animation: rotate-border 4s linear infinite;
}

.result-box::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 20px;
    background: conic-gradient(
        from var(--border-angle),
        transparent 0deg,
        rgba(99, 102, 241, 0.7) 60deg,
        rgba(139, 92, 246, 0.8) 120deg,
        rgba(6, 182, 212, 0.8) 180deg,
        rgba(59, 130, 246, 0.7) 240deg,
        transparent 360deg
    );
    z-index: -1;
    filter: blur(16px);
    opacity: 0.6;
    animation: rotate-border 4s linear infinite;
    pointer-events: none;
}

/* Footer */
.footer {
    text-align: center;
    color: #71717a;
    font-size: 13px;
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid rgba(255,255,255,0.06);
}

.footer span {
    color: #a5b4fc;
}

</style>
""", unsafe_allow_html=True)




st.markdown("""
<div class="hero">



<h1>CodeMentor AI</h1>

<p>
Understand. Debug. Improve. <br>
Your intelligent coding companion for learning and writing better code.
</p>

</div>
""", unsafe_allow_html=True)




col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Understand Code</div>
        <div class="feature-text">
            Get simple, beginner-friendly explanations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🐛</div>
        <div class="feature-title">Find Bugs</div>
        <div class="feature-text">
            Detect problems and understand why they occur.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Improve Code</div>
        <div class="feature-text">
            Discover cleaner and better ways to write your code.
        </div>
    </div>
    """, unsafe_allow_html=True)



st.markdown(
    '<div class="section-title">🛠️ Configure your analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Programming Language",
        ["Python", "C", "C++", "Java"]
    )

with col2:
    task = st.selectbox(
        "What should CodeMentor do?",
        [
            "Explain Code",
            "Find Bugs",
            "Improve Code",
            "Explain Error",
            "Code Quality Score",
            "Complexity Analysis",
            "Teach Me"
        ]
    )


st.markdown(
    '<div class="section-title">💻 Your Code</div>',
    unsafe_allow_html=True
)

code = st.text_area(
    "Paste your code below",
    height=300,
    placeholder="""// Example

def add(a, b):
    return a + b

print(add(10, 20))"""
)




if st.button("🚀  Analyze My Code"):

    if not code.strip():

        st.warning("⚠️ Please paste some code first.")

    else:

        task_instructions = {
            "Explain Code": "Explain the code simply, step-by-step, and summarize its overall flow.",
            "Find Bugs": "Find syntax, logical, runtime, edge-case, and important practice issues. Explain and fix each issue.",
            "Improve Code": "Suggest practical improvements to readability, structure, performance, maintainability, and style without changing intended behavior.",
            "Explain Error": "Identify the likely cause, explain it simply, and give clear steps to fix it. If no error is supplied, inspect likely failure points.",
            "Code Quality Score": "Give a score from 0 to 100. Evaluate correctness, readability, maintainability, efficiency, structure, naming, and error handling. Give strengths, weaknesses, and top improvements.",
            "Complexity Analysis": "Analyze time and space complexity using Big-O. Explain the main operations and overall complexity in beginner-friendly terms, and mention possible optimizations.",
            "Teach Me": "Teach this code like a beginner lesson: big picture, step-by-step explanation, important concepts, a small example, and 2-3 quick questions to test understanding."
        }

        prompt = (
            "You are CodeMentor AI, an expert programming mentor "
            "who explains concepts clearly to beginners.\n\n"
            f"Programming Language: {language}\n"
            f"Requested Task: {task}\n"
            f"Task Instructions: {task_instructions[task]}\n\n"
            "User's Code:\n"
            f"{code}\n\n"
            "Provide a useful, accurate and beginner-friendly response. "
            "Use clear headings, bullet points, and code blocks where appropriate. "
            "Do not invent errors or behavior that is not supported by the code."
        )

        with st.spinner("🤖 CodeMentor is thinking..."):

            response = client.chat.completions.create(
                model="Qwen/Qwen3-4B-Instruct-2507",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1200
            )

        answer = response.choices[0].message.content

        st.markdown(f"""
        <div class="result-box">
            <h2>✨ {task}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(answer)




st.markdown("""
<div class="footer">
    Built with ❤️ using <span>Python</span> ·
    <span>Streamlit</span> ·
    <span>Hugging Face</span> ·
    <span>Qwen</span>
</div>
""", unsafe_allow_html=True)