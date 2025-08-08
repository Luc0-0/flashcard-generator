import streamlit as st
import pdfplumber
import os
from openai import OpenAI

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def generate_flashcards(text):
    system_message = {
        "role": "system",
        "content": "You are an expert teacher. Create flashcards from the provided text."
    }
    user_message = {
        "role": "user",
        "content": (
            f"Here is the text to generate flashcards from:\n\n{text}\n\n"
            "Please write flashcards in Q&A format."
        )
    }

    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-3.5-turbo, or whichever model you want
        messages=[system_message, user_message],
        max_tokens=500,
        temperature=0.5,
        n=1,
    )

    return response.choices[0].message.content.strip()

def main():
    st.title("Flashcard Generator AI - Text & PDF Input Demo")

    input_option = st.radio("Choose input type:", ("Paste Text", "Upload PDF"))

    text = ""
    if input_option == "Paste Text":
        text = st.text_area("Paste your text here:", height=200)
    elif input_option == "Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)

    if text:
        st.subheader("Extracted Text:")
        st.write(text)

        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                flashcards = generate_flashcards(text)
                st.subheader("Generated Flashcards:")
                st.text(flashcards)

if __name__ == "__main__":
    main()
