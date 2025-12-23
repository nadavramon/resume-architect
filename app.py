import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

# 1. Setup & Config
load_dotenv()
st.set_page_config(page_title="Resume Architect", page_icon="📝")

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

client = Groq(api_key=api_key)

# --- THE JAVA INTEGRATION LAYER ---
def publish_to_java_backend(event_type, payload):
    JAVA_SERVER_URL = "http://localhost:8080/publish" 
    
    # Create the JSON string manually
    json_payload = json.dumps({
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "payload": payload
    })
    
    # CRITICAL FIX: Append a newline so the Java readLine() unblocks
    final_data = json_payload + "\n"
    
    try:
        # We use data=... instead of json=... to control the exact formatting
        response = requests.post(
            JAVA_SERVER_URL, 
            data=final_data, 
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            return True, "Successfully published to Java Backend"
        else:
            return False, f"Java Server returned {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Connection Timed Out (Java accepted the call but didn't reply)"
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to Java Server (is it running?)"

# --- THE UI (Streamlit) ---
st.title("🚀 Resume Architect")
st.caption("Powered by Llama 3 on Groq | Integrated with Custom Java Backend")

# Input Columns
col1, col2 = st.columns(2)
with col1:
    current_resume = st.text_area("Paste your current Resume/CV text here:", height=300)
with col2:
    job_description = st.text_area("Paste the Target Job Description here:", height=300)

if st.button("Generate Tailored Resume"):
    if not current_resume or not job_description:
        st.warning("Please provide both your resume and the job description.")
    else:
        with st.spinner("Consulting the AI Architect..."):
            # 1. AI GENERATION
            try:
                # OPTIMIZED SYSTEM PROMPT
                system_instruction = """
                You are an expert Senior Technical Recruiter and Resume Architect. 
                Your goal is to rewrite the user's resume to perfectly align with the provided Job Description.
                
                Guidelines:
                1. ANALYZE the Job Description for key hard skills, soft skills, and terminology.
                2. INTEGRATE these keywords naturally into the resume summary and bullet points.
                3. QUANTIFY achievements where possible (e.g., "Improved efficiency by 20%").
                4. USE STRONG ACTION VERBS (e.g., Architected, Orchestrated, Deployed, Optimized).
                5. KEEP the format clean and professional.
                6. DO NOT invent false experiences, but emphasize relevant existing skills.
                7. Return ONLY the markdown-formatted resume text. No conversational filler.
                8. Keep a resume to one page if you have less than ten years of experience.
                9. 
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_instruction
                        },
                        {
                            "role": "user",
                            "content": f"My Current Resume:\n{current_resume}\n\nTarget Job Description:\n{job_description}"
                        }
                    ],
                    model="llama-3.3-70b-versatile",
                )
                generated_resume = chat_completion.choices[0].message.content
                
                # Display Result
                st.subheader("Your New Resume")
                st.text_area("Copy this:", value=generated_resume, height=400)
                
                # 2. SYSTEM INTEGRATION (Publishing to Java)
                st.divider()
                st.write("🔌 **System Integration Status:**")
                
                # Create a payload summary (don't send full text to keep it light)
                payload_summary = {
                    "job_length": len(job_description),
                    "resume_length": len(current_resume)
                }
                
                success, message = publish_to_java_backend("RESUME_GENERATED", payload_summary)
                
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
                    st.info("Tip: Ensure your Java HTTP Server is running to see the integration in action.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")