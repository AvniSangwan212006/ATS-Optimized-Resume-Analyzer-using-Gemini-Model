import streamlit as st # type: ignore
import google.generativeai as genai
import os
import PyPDF2 as pdf 

from dotenv import load_dotenv 

load_dotenv ## load all the environemtn variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Reposne
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

## Prompt Template
input_prompt="""
Hey Act Like a skilled and very experienced ATS (Applicant Tracking System) 
with a deep understanding of the tech field, software engineering, data science, 
data analysis, and big data engineering. Your task is to evaluate the resume base on the given job description. Consider that the job market is very competitive, 
and provide the best assistance for improving the resumes. Assign the percentage 
matching based on the job description and list the missing keywords with high accuracy.

resume: {text}
description: {jd}

I want the response in one single string having the structure 
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve your resume ATS")
jd=st.text_area("paste the job description")
uploaded_file=st.file_uploader("upload your resume",type="pdf",help="please upload the pdf")

submit = st.button("submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)
