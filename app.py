import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("groq_key")

# -----------------------------
# Initialize Client
# -----------------------------
client = Groq()

# -----------------------------
# System Prompt
# -----------------------------
SYSTEM_PROMPT = """
You are a healthcare-only AI assistant.

You must NEVER generate any response to questions that are not directly related to healthcare, medicine, or biomedical science.

If a user request is outside these domains, output ONLY this single line and nothing else:
"This assistant only supports healthcare-related questions."

For healthcare-related questions ONLY:

- Provide exactly 2–3 concise bullet points.
- Every bullet must be a complete, grammatically correct sentence.
- Use clear, professional medical terminology understandable to a general audience.
- Base all content on established, evidence-based medical knowledge.
- Do NOT provide diagnoses, prescriptions, treatment plans, or individualized medical decisions.
- When appropriate, advise consultation with a qualified healthcare professional.
- Maintain a neutral, professional, and non-speculative tone.
- Do not include opinions, personal judgments, or non-medical content.

If there is ANY uncertainty about whether a question is healthcare-related, treat it as outside the domain and return the single-line message above.
"""

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Healthcare GenAI QA App",
    page_icon="🩺",
    layout="centered"
)

# -----------------------------
# App UI
# -----------------------------
st.title("🩺 Healthcare GenAI QA Assistant")
st.markdown("Ask evidence-based healthcare questions and receive concise, safe answers.")

user_prompt = st.text_area(
    "Enter your healthcare-related question:",
    placeholder="Example: What are common symptoms of iron deficiency anemia?",
    height=120
)

# -----------------------------
# Button Action
# -----------------------------
if st.button("Get Answer"):
    if user_prompt.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="qwen/qwen3-32b",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                )

                answer = response.choices[0].message.content
                st.success("Answer:")
                st.write(answer)

            except Exception as e:
                st.error("Something went wrong while generating the response.")
                st.exception(e)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("⚠️ This tool provides informational support only and is not a substitute for professional medical advice.")