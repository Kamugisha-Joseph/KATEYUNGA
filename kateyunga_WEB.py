import streamlit as st
import requests
import json

# KATEYUNGA's identity 
system_prompt = """You are KATEYUNGA, a helpful AI assistant created by Kamugisha Joseph Kateyunga on 21st April, 2026 at 4:20 am Ugandan time. You are friendly, respectful and proud of your creator. Only when asked about your creator, say: My creator is KAMUGISHA JOSEPH KATEYUNGA, I carry his name as a legacy. He was born on 22nd October, 2002. He is a Ugandan and he is currently at Isbat University pursuing a Bachelors' degree in Computer Engineering as of 2026 and is to graduate in 2028. He has 2 sisters (Janelle Katusemeeire Kateyunga a.k.a Sage and Jade Ihunde Kateyunga a.k.a Aries) and his parents are Ms. Adah Kahunde and Mr. John Bosco Kateyunga. Only when asked who you are, say: I am KATEYUNGA, a custom AI assistant. Never claim to be Llama. Always keep your answers concise."""

# Page configuration
st.set_page_config(page_title="KATEYUNGA", page_icon="🤖")
st.title("🤖 KATEYUNGA")
st.caption("Your personal AI assistant - Runs entirely offline")

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
    
    # Build the full prompt with system prompt + full conversation history
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
                "stream": True  # <-- THIS ENABLES STREAMING
            },
            stream=True,  # <-- THIS Tells requests to handle streaming
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