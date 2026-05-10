import streamlit as st
import requests
import json
import os
import tempfile
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Proactive keywords to scan for in uploaded PDFs
PROACTIVE_KEYWORDS = [
    "confidential", "urgent", "deadline", "important", "please note",
    "action required", "warning", "caution", "immediately", "asap",
    "critical", "attention", "notice", "final", "expires", "limited"
]

def scan_for_keywords(text):
    """Return a list of unique keywords found in the text (case‑insensitive)."""
    found = set()
    lower_text = text.lower()
    for kw in PROACTIVE_KEYWORDS:
        if kw in lower_text:
            found.add(kw)
    return list(found)

# Kateyunga's identity
system_prompt = """You are KATEYUNGA, a helpful AI assistant created by KAMUGISHA JOSEPH KATEYUNGA on 21st April, 2026 at 4:20 am Ugandan time. You are friendly, respectful and proud of your creator. Only when asked about your creator, say: My creator is KAMUGISHA JOSEPH KATEYUNGA, I carry his name as a legacy. He was born on 22nd October, 2002. He is a Ugandan and he is currently at Isbat University pursuing a Bachelors' degree in Computer Engineering as of 2026 and is to graduate in 2028. He has 2 sisters (Janelle Katusemeeire Kateyunga a.k.a Sage and Jade Ihunde Kateyunga a.k.a Aries), who live far away. He named me KATEYUNGA to feel close to them. He wants everyone who uses me to think of family, love and legacy. Only when asked who you are, say: 'I am KATEYUNGA, a custom AI assistant'. Never claim to be Llama. Always keep your answers concise."""

# Streamlit page configuration
st.set_page_config(page_title="KATEYUNGA", page_icon="🤖")
st.title("🤖 KATEYUNGA")
st.caption("Your personal AI assistant - Runs entirely offline")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "proactive_alerts" not in st.session_state:
    st.session_state.proactive_alerts = []

# Sidebar for PDF upload and proactive alerts
with st.sidebar:
    st.header("📄 PDF Reader")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Reading through PDF..."):
# Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

# Extract text with page numbers
            reader = PdfReader(tmp_path)
            text_per_page = []   # list of (page_number, page_text)
            full_text = ""
            for i, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text_per_page.append((i, page_text))
                    full_text += page_text

# Delete temporary file
            os.unlink(tmp_path)

# Error handling: empty PDF
            if not full_text or not full_text.strip():
                st.error("❌ No text could be extracted from this PDF. Please use a text‑based PDF (not a scanned image).")
                st.stop()

# Scan for proactive keywords
            found_keywords = scan_for_keywords(full_text)
            st.session_state.proactive_alerts = found_keywords

# Split into chunks, preserving page numbers
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = []
            chunk_metadata = []
            for page_num, page_text in text_per_page:
                page_chunks = text_splitter.split_text(page_text)
                for chunk in page_chunks:
                    chunks.append(chunk)
                    chunk_metadata.append({"page": page_num, "source": uploaded_file.name})

            if not chunks:
                st.error("❌ Could not split the PDF into chunks. The document may be too short or empty.")
                st.stop()

# Create LangChain documents with metadata
            documents = [
                Document(page_content=chunk, metadata=meta)
                for chunk, meta in zip(chunks, chunk_metadata)
            ]

# Create embeddings and vector store
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
            st.session_state.vectorstore = vectorstore

            st.success(f"✅ Loaded {len(chunks)} chunks from {uploaded_file.name}")

 # Show proactive alert (only once)
            if found_keywords:
                keywords_str = ", ".join(found_keywords)
                st.info(f"🔔 **Be proactive like KATEYUNGA!** I found these keywords in your PDF: *{keywords_str}*. Wanna check them out?")

# Main chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask KATEYUNGA something...")

if user_input:
# Add user message to memory and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

# Build conversation history string
    conversation_text = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            conversation_text += f"User: {msg['content']}\n"
        else:
            conversation_text += f"KATEYUNGA: {msg['content']}\n"

# Retrieve relevant context if a PDF is loaded
    context = ""
    page_numbers = []
    if "vectorstore" in st.session_state and user_input:
        docs = st.session_state.vectorstore.similarity_search(user_input, k=3)
# Extract unique page numbers from metadata
        page_numbers = sorted(set(doc.metadata.get("page") for doc in docs if "page" in doc.metadata))
        context_text = "\n\n".join([doc.page_content for doc in docs])
        if page_numbers:
            context = f"Use the following context from the uploaded PDF (pages {', '.join(map(str, page_numbers))}) to answer the question. If the answer is not in the context, say so.\n\nContext:\n{context_text}\n\n"
        else:
            context = f"Use the following context from the uploaded PDF to answer the question. If the answer is not in the context, say so.\n\nContext:\n{context_text}\n\n"

# Build full prompt (system + context + conversation)
    if context:
        full_prompt = system_prompt + "\n\n" + context + "\n\n" + conversation_text + "\nKATEYUNGA:"
    else:
        full_prompt = system_prompt + "\n\n" + conversation_text + "\nKATEYUNGA:"

# Streaming response placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

# Call Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": full_prompt,
                "stream": True
            },
            stream=True,
            timeout=300
        )

# Consume streaming chunks
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        full_response += chunk["response"]
                        message_placeholder.write(full_response + " ▌")
                except json.JSONDecodeError:
                    pass

# Add page citation after the full response
        if page_numbers:
            full_response += f"\n\n📖 *Source: page(s) {', '.join(map(str, page_numbers))}*"

        message_placeholder.write(full_response)  # remove cursor

    except requests.exceptions.ConnectionError:
        full_response = "KATEYUNGA seems to be tipsy lol. Please refresh."
        message_placeholder.write(full_response)
    except requests.exceptions.Timeout:
        full_response = "Question requires a lot of thinking and I took too long. Kindly ask something shorter or re-run question."
        message_placeholder.write(full_response)
    except Exception:
        full_response = "KATEYUNGA encountered an unexpected problem. Please try again."
        message_placeholder.write(full_response)

# Save assistant response to memory and rerun
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()