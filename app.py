import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load all our environment variables

# Configure API with the key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text() if reader.pages[page].extract_text() else ''
    return text

# Set Streamlit page configuration
st.set_page_config(page_title="Smart Application Tracking System", page_icon=":robot:")

# Custom CSS for the background and input fields, setting text area text color to white
st.markdown("""
<style>
body {
    color: #ffffff; /* White text color for contrast */
}
[data-testid="stAppViewContainer"] > .main {
    background-image: linear-gradient(135deg, #2196F3 0%, #E91E63 50%, #FFEB3B 100%);
    background-size: cover;
    background-attachment: fixed;
    color: #ffffff; /* White text for better visibility */
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
.stTextInput, .stTextArea {
    background-color: #000000; /* Black background for input boxes */
    color: #ffffff; /* White text inside input boxes */
    border: 2px solid #2196F3; /* Blue border */
}
.stButton > button {
    background-color: #2196F3; /* Blue background for buttons */
    color: #ffffff; /* White text for buttons */
    border: none;
}
.stButton > button:hover {
    background-color: #64B5F6; /* Light blue for button hover */
}
</style>
""", unsafe_allow_html=True)

st.title("RESUME TRACKING SYSTEM")
st.subheader("Improve Your Resume Score")

# Get input from the user
jd = st.text_area("Paste the Job Description", help="Enter the job description here.")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        extracted_text = input_pdf_text(uploaded_file)
        formatted_prompt = f"""
        You are a skilled and very experienced ATS (Application Tracking System) with a deep understanding of tech fields, software engineering,
        data science, data analyst, and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide the best assistance for improving the resumes. 
        Assign the percentage Matching based on Job description and the missing keywords with high accuracy
        Resume: {extracted_text}
        Description: {jd}
        
        I want the only response in 3 sectors as follows:
        • Job Description Match: \n
        • MissingKeywords: \n
        • Profile Summary: \n
        """
        response = get_gemini_response(formatted_prompt)
        st.write("Analysis Result:")
        st.write(response)
    else:
        st.error("Please upload a resume and paste the job description to proceed.")













