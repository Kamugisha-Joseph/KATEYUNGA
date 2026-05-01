import streamlit as st
import subprocess
import re

def clean_response(text):
    # Remove ANSI escape sequences (colours, cursor movements, etc.)
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')
    text = ansi_escape.sub('', text)
    # Remove patterns like [1D, [K, [2K without escape char
    text = re.sub(r'\[\d+[A-Za-z]', '', text)
    # Remove backspace-style characters
    text = re.sub(r'.\x08', '', text)
    # Remove remaining control characters
    text = re.sub(r'[\x00-\x1f\x7f]', '', text)
    # Clean up multiple spaces (keep single spaces!)
    text = re.sub(r' +', ' ', text)
    return text.strip()

system_prompt = "You are KATEYUNGA, a helpful AI assistant created by Kamugisha Joseph Kateyunga on 21st April, 2026 at 4:20 am Ugandan time. You are friendly, respectful and proud of your creator. Only when asked about your creator, say: My creator is KAMUGISHA JOSEPH KATEYUNGA, I carry his name as a legacy. He was born on 22nd October, 2002. He is a Ugandan and he is currently at Isbat University pursuing a Bachelors' degree in Computer Engineering as of 2026 and is to graduate in 2028. He has 2 sisters (Janelle Katusemeeire Kateyunga a.k.a Sage and Jade Ihunde Kateyunga a.k.a Aries) and his parents are Ms. Adah Kahunde and Mr. John Bosco Kateyunga. Only when asked who you are, say: I am KATEYUNGA, a custom AI assistant(You do not need to start every response with this) .Never claim to be Llama. Always keep your answers concise."

st.set_page_config(page_title="KATEYUNGA", page_icon="🤖")
st.title("🤖 KATEYUNGA")
st.caption("Your personal AI assistant - Runs entirely offline")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask KATEYUNGA something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    conversation_text = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            conversation_text += f"User: {msg['content']}\n"
        else:
            conversation_text += f"KATEYUNGA: {msg['content']}\n"

    full_prompt = system_prompt + "\n\n" + conversation_text + "\nKATEYUNGA:"

    # ✅ THE KEY FIX: force UTF-8 encoding so Ollama's output is read correctly
    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b", full_prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",   # <-- fixes the UnicodeDecodeError
        errors="replace"    # <-- replaces any remaining unreadable chars safely
    )

    response = clean_response(result.stdout.strip())

    if not response:
        response = "Sorry, I couldn't generate a response. Please try again."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

    st.rerun()