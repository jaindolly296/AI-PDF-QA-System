import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Page configuration
st.set_page_config(
    page_title="PDF QnA Assistant",
    page_icon="📄",
    layout="centered"
)


# Title
st.title("📄 PDF QnA Assistant")
st.write(
    "By Dolly Jain"
)

st.write(
    "Upload PDF and ask questions using AI."
)


# Check API key

if not GROQ_API_KEY:

    st.error(
        "Groq API Key not configured."
    )

    st.stop()



# Create Groq client

client = Groq(
    api_key=GROQ_API_KEY
)



# PDF Upload

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)



# Extract PDF text

def extract_text(pdf_file):

    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"


    return text



# Chat history

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []



# Main application

if uploaded_file:


    with st.spinner(
        "Reading PDF..."
    ):

        document_text = extract_text(
            uploaded_file
        )


    st.success(
        "✅ PDF Uploaded Successfully"
    )


    st.info(
        f"📑 Total Characters: {len(document_text)}"
    )


    question = st.text_input(
        "Ask a question from PDF"
    )



    if st.button("Ask AI"):


        if not question:


            st.warning(
                "Please enter a question"
            )


        else:


            try:


                prompt = f"""

You are a helpful PDF assistant.

Answer only using the PDF content.

PDF Content:

{document_text}


Question:

{question}

"""


                with st.spinner(
                    "Thinking..."
                ):


                    response = client.chat.completions.create(

                        model="llama-3.1-8b-instant",

                        messages=[
                            {
                                "role":"user",
                                "content":prompt
                            }
                        ],

                        temperature=0.2

                    )


                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )


                st.subheader(
                    "🤖 AI Answer"
                )


                st.write(answer)



                st.session_state.chat_history.append(

                    {
                        "question":question,
                        "answer":answer
                    }

                )


            except Exception as e:


                st.error(
                    f"Error: {e}"
                )



# History section

if st.session_state.chat_history:


    st.subheader(
        "💬 Chat History"
    )


    for chat in st.session_state.chat_history:


        st.write(
            "Question:",
            chat["question"]
        )


        st.write(
            "Answer:",
            chat["answer"]
        )
