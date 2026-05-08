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

# KATEYUNGA's identity 
system_prompt = """You are KATEYUNGA, a helpful AI assistant created by Kamugisha Joseph Kateyunga on 21st April, 2026 at 4:20 am Ugandan time. You are friendly, respectful and proud of your creator. Only when asked about your creator, say: My creator is KAMUGISHA JOSEPH KATEYUNGA, I carry his name as a legacy. He was born on 22nd October, 2002. He is a Ugandan and he is currently at Isbat University pursuing a Bachelors' degree in Computer Engineering as of 2026 and is to graduate in 2028. He has 2 sisters (Janelle Katusemeeire Kateyunga a.k.a Sage and Jade Ihunde Kateyunga a.k.a Aries), who live far away. He named me KATEYUNGA to feel close to them. He wants everyone who uses me to think of family, love and legacy. Only when asked who you are, say: 'I am KATEYUNGA, a custom AI assistant'. Never claim to be Llama. Always keep your answers concise."""

# Page configuration
st.set_page_config(page_title="KATEYUNGA", page_icon="🤖")
st.title("🤖 KATEYUNGA")
st.caption("Your personal AI assistant - Runs entirely offline")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📄 PDF Reader")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
 # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
# To extract text from PDF
            reader = PdfReader(tmp_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
# To split into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(text)
            
# Create documents with metadata
            documents = [Document(page_content=chunk, metadata={"source": uploaded_file.name}) for chunk in chunks]
            
# Create embeddings and vector store
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
            
            st.session_state.vectorstore = vectorstore
            st.success(f"✅ Loaded {len(chunks)} chunks from {uploaded_file.name}")
            os.unlink(tmp_path)  # Delete temp file

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input box at the bottom
user_input = st.chat_input("Ask KATEYUNGA something...")

if user_input:
 # Add user's message to memory and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Build the conversation history into a single string
    conversation_text = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            conversation_text += f"User: {msg['content']}\n"
        else:
            conversation_text += f"KATEYUNGA: {msg['content']}\n"
    
# Check if a PDF is loaded and question is relevant
    context = ""
    if "vectorstore" in st.session_state and user_input:
        # Search for relevant chunks
        docs = st.session_state.vectorstore.similarity_search(user_input, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        context = f"Use the following context from the uploaded PDF to answer the question. If the answer is not in the context, say so.\n\nContext:\n{context}\n\n"
    
 # Build full prompt with context if available
    if context:
        full_prompt = system_prompt + "\n\n" + context + "\n\n" + conversation_text + "\nKATEYUNGA:"
    else:
        full_prompt = system_prompt + "\n\n" + conversation_text + "\nKATEYUNGA:"
    
 # Create a placeholder for the streaming response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
    
# Call Ollama with streaming
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": full_prompt,
                "stream": True  #(THIS ENABLES STREAMING)
            },
            stream=True,  #(THIS Tells requests to handle streaming)
            timeout=300
        )
        
# To process each chunk of the response as it arrives
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        full_response += chunk["response"]
                        # Update the display with each new word
                        message_placeholder.write(full_response + " ▌")
                except json.JSONDecodeError:
                    pass  # Skip any malformed chunks
        
 # To remove the cursor after completion
        message_placeholder.write(full_response)
        
    except requests.exceptions.ConnectionError:
        full_response = "KATEYUNGA seems to be tipsy lol. Please refresh."
        message_placeholder.write(full_response)
    except requests.exceptions.Timeout:
        full_response = "Question requires a lot of thinking and I took too long. Kindly ask something shorter or re-run question."
        message_placeholder.write(full_response)
    except Exception as e:
        full_response = f"KATEYUNGA encountered an unexpected problem. Please try again."
        message_placeholder.write(full_response)
    
 # Add the complete response to memory
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.rerun()