# Document Analysis and Summary Tool

This Python script utilizes Streamlit to create a web application that allows users to upload documents for analysis and summarization. The application supports various file formats, including plain text (.txt), PDF (.pdf), Microsoft Word (.docx), and CSV (.csv). It uses machine learning and natural language processing techniques to extract text from documents, analyze the content, and generate summaries. Additionally, users can ask specific questions about the document's content, and the tool will provide answers based on the generated summary.

## Features

- **Document Upload:** Supports uploading of .txt, .pdf, .docx, and .csv files for analysis.
- **Content Analysis:** Analyzes the uploaded document to extract text and generate a concise summary.
- **Question Answering:** Allows users to input questions related to the document content and provides answers based on the summary.
- **Support for Various Document Types:** Includes specialized handling for different document types, using OCR for PDFs without text layers and handling structured data in CSV files.

## How It Works

1. **Uploading Documents:** Users can upload documents in supported formats. The tool then processes the document to extract text.
   
2. **Text Extraction:** 
   - For .txt, .pdf, and .docx files, the tool extracts text directly or uses OCR for PDFs without a text layer.
   - For .csv files, it reads the file into a DataFrame and provides a summary of the data.

3. **Summary Generation:** Utilizes OpenAI's GPT-3 model to generate a summary of the extracted text. The summary's context is determined based on keywords found in the text.

4. **Question Answering:** Users can ask questions about the document, and the tool generates answers using GPT-3, based on the summary content.

## Setup and Installation

1. **Install Dependencies:**
   ```bash
   pip install streamlit openai PyPDF2 python-docx pandas pytesseract plotly
   ```
2. **Set Up Environment Variables:**
   - Ensure you have an OpenAI API key.
   - Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

3. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Usage

- **Start the application** as instructed above and navigate to the provided URL.
- **Upload a document** in one of the supported formats.
- **View the generated summary** and **ask questions** if needed.

## Note

- The tool requires an internet connection to use OpenAI's GPT-3 API for summary generation and question answering.
- OCR functionality requires `pytesseract` and its dependencies to be correctly installed and configured on your system.

This tool showcases the power of combining Streamlit with OpenAI's GPT-3 for document analysis, making it easier for users to extract and understand key information from various document types.
