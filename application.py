import streamlit as st
import openai
import PyPDF2
import docx
import os
import re
import pandas as pd
from PIL import Image
import pytesseract
import plotly.express as px
import xml.etree.ElementTree as ET

# Function to read PDF and extract text using OCR
def extract_text_with_ocr(uploaded_file):
    text = ''
    images = convert_from_bytes(uploaded_file.read())
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

# Function to analyze content and generate a summary
def analyze_and_generate_summary(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            if reader.pages[0].extract_text():
                for page in reader.pages:
                    text += page.extract_text()
            else:
                text = extract_text_with_ocr(uploaded_file)

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text

        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            text = df
            return generate_csv_summary(text)

        if text:
            context_type = determine_context(text)
            return generate_summary(text, context_type)
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None

# Function to determine the context of the text
def determine_context(text):
    if re.search(r"\b(date|time|event|location)\b", text, re.I):
        return "ticket"
    elif re.search(r"\b(math|equation|formula)\b", text, re.I):
        return "math"
    else:
        return "generic"

# Function to generate a summary using OpenAI GPT-3
def generate_summary(text, context_type="generic"):
    try:
       
        # Define different prompts based on context_type
        if context_type == "ticket":
            prompt = "Summarize the following ticket information:\n\n" + text
        elif context_type == "math":
            prompt = "Summarize the following mathematical problem:\n\n" + text
        else:
            prompt = "Summarize the following text:\n\n" + text
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150 # Adjust as needed
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        return str(e)

#  CSV summary
def generate_csv_summary(df):
    #st.write("Interactive Summary of CSV Data")
    return st.write(df.describe())

def answer_question(text, question):
    try:
        prompt = f"Answer the following question based on the document:\n\n{question}\n\n{text}"
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150  # Adjust as needed
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        st.error("An error occurred while generating the answer.")
        return str(e)

# Streamlit UI
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = openai_api_key


st.title("Document Analysis and Summary")
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx", "csv"])


if uploaded_file is not None:
    with st.spinner('Analyzing...'):
        summary = analyze_and_generate_summary(uploaded_file)
        if summary:
            st.write("Summary of the uploaded content:")
            st.write(summary)
            question = st.text_input("Ask a question about the document:")
            if question:
                with st.spinner('Generating answer...'):
                    answer = answer_question(summary, question)
                    st.write("Answer:")
                    st.write(answer)
        else:
            st.error("Unsupported file format or unable to analyze the content.")