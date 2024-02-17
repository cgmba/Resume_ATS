from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import io
import base64
import os
from PIL import Image
#import poppler-utils
#import libpoppler-dev
import pdf2image
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    #convert the PDF to image

    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format= 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


#Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key= "input")
uploaded_file = st.file_uploader("Upload your resume(PDF) ...", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage match")


input_prompt1 = """
    You are an experienced HR with Tech Experience in the field of Data Science, Full Stack Web Development, Big Data 
    Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description for these profiles.
    Please share your professional evaluation on whether the candidate's profile aligns with
    Highlight the strengths and weaknesses of the applicant in relation to the specified job description"""


input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack Web Development, Big Data 
    Engineering, DEVOPS, Data Analyst, your task is to evaluate the resume against the provided job description. give me the percentage of the job description.
    First the output should come as perecentage and then keywords missing"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")



