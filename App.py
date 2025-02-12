import streamlit as st
import openai
from docx import Document
from io import BytesIO

# --- OpenAI API Key (Use Streamlit Secrets for security) ---
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Ensure you add this to your Streamlit Secrets

# --- Function to Generate Resume Content ---
def generate_resume_content(job_seeker_type, user_prompt, model_name):
    """
    Generates resume content using OpenAI's API based on user input.
    """
    try:
        full_prompt = f"""
        You are an expert resume writer and career advisor. Your goal is to create high-quality, 
        ATS-friendly (Applicant Tracking System) resume content that helps job seekers get interviews.

        Job Seeker Type: {job_seeker_type}
        User Provided Information: {user_prompt}

        Instructions:
        1. Based on the information provided, create resume content that could be used in a resume.  
        2. Focus on accomplishments and quantify them whenever possible (use numbers, percentages, etc.).
        3. Use action verbs to start each bullet point.
        4. Tailor the content to be relevant to the information given by the user.
        5. Use the CAR (Challenge-Action-Result) method to structure bullet points.
        6. Always ensure the output is easy to read and well-structured.
        7. Format the resume in sections: Summary, Skills, Education, Projects, and Experience.
        
        Now, generate the resume content based on the job seeker type and user-provided information.
        """

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful resume writing assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=700,
            temperature=0.7,
        )

        return response["choices"][0]["message"]["content"].strip()
    
    except openai.error.OpenAIError as e:
        return f"OpenAI API error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- Function to Create Word Document (DOCX) ---
def create_docx(content):
    """
    Generates a .docx file from the given text content.
    """
    doc = Document()
    doc.add_paragraph(content)
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


# --- Streamlit UI ---
st.title("AI-Powered Resume Generator")

st.write("This tool helps you create a professional resume using AI. Provide your details, and the AI will generate a tailored resume for you.")

# --- Job Seeker Type Selection ---
job_seeker_type = st.selectbox(
    "Select your job seeker type:",
    ("Fresh Graduate", "Student", "Business Professional", "Entrepreneur", "Other")
)

# --- AI Model Selection ---
model_name = st.selectbox(
    "Select AI Model:",
    ("gpt-3.5-turbo", "gpt-4")
)

# --- User Input Area ---
st.subheader("Tell us about yourself and your target job")
user_prompt = st.text_area(
    "Provide details about your skills, experience, education, and target job. Be as specific as possible.",
    height=200
)

# --- Generate Resume Button ---
if st.button("Generate Resume Content"):
    if not user_prompt:
        st.warning("Please enter your details in the text area above.")
    else:
        with st.spinner("Generating resume content..."):
            resume_content = generate_resume_content(job_seeker_type, user_prompt, model_name)

        st.subheader("Generated Resume Content:")
        st.markdown(f"```\n{resume_content}\n```")  # Keeps formatting clean

        # --- Download Options ---
        st.download_button(
            label="Download as Text",
            data=resume_content,
            file_name="generated_resume.txt",
            mime="text/plain",
        )

        st.download_button(
            label="Download as Word Document",
            data=create_docx(resume_content),
            file_name="generated_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# --- Footer ---
st.markdown("""---
**About this tool:** This AI-powered resume generator helps you create an ATS-optimized resume. 
*Review and edit the generated content to ensure accuracy and relevance.*
""")