import streamlit as st
import requests
import json

system_prompt = """You are KATEYUNGA, a helpful AI assistant created by Kamugisha Joseph Kateyunga..."""

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

    # Call Kateyunga's brain (local AI)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "I'm having trouble thinking clearly. Please try again.")
        else:
            response_text = "I'm having technical difficulties. Please try again in a moment."
            
    except requests.exceptions.ConnectionError:
        response_text = "KATEYUNGA seems to be tipsy. Kindly refresh."
    except requests.exceptions.Timeout:
        response_text = "That question requires a lot of thinking, and I took too long. Please try asking something shorter, or ask the same question again."
    except Exception as e:
        response_text = f"KATEYUNGA encountered an unexpected problem. Please try again."
    response_text = response_text.strip()
    
    if not response_text:
        response_text = "Sorry, I couldn't generate a response. Please try again."
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.write(response_text)
    
    st.rerun()