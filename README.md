# 🤖 KATEYUNGA

**Your Offline Personal AI Assistant**

KATEYUNGA is a fully offline, private AI assistant that runs entirely on your laptop. It remembers your conversation, responds naturally, and requires no internet connection after setup.

Built with **Llama 3.2**, **Ollama**, and **Streamlit**.

#Features

- 🧠 **Offline-first** – Runs completely on your laptop. No data leaves your device.(privacy first)
- 💬 **Conversation memory** – Remembers what you said during the session.
- ⚡ **Streaming responses** – Words appear progressively, just like a real conversation.
- 🎨 **Chat interface** – Clean, modern web UI with chat bubbles.
- 🔐 **Private** – No API keys. No cloud costs. No spying.
- 🧩 **Customizable** – Built on open-source Llama 3.2.

#DEMO

Watch the demo video: [KATEYUNGA in action](https://youtu.be/CjAlGFBvsP0)


#Requirements

Before running KATEYUNGA, make sure you have:

| Requirement     | Version        | Download 

| Python          | 3.12 or higher | [python.org](https://python.org) 
| Ollama          | Latest         | [ollama.com](https://ollama.com) 
| Llama 3.2 model | 3B             | `ollama pull llama3.2:3b` |


#  Installation & Setup
#1. Clone the repository
```type
git clone https://github.com/Kamugisha-Joseph/KATEYUNGA.git
cd KATEYUNGA

#2. Create a virtual environment (recommended)

```type
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

#3. Install dependencies

```type
pip install -r requirements.txt


#4. Install and run Ollama

```bash
# Download Ollama from ollama.com, then pull the model
ollama pull llama3.2:3b


#5. Run KATEYUNGA

```type
streamlit run kateyunga_WEB.py


...Your browser will open automatically with KATEYUNGA.


######🎮 How to Use

1. Type your message in the chat box.
2. Press Enter or click Send.
3. KATEYUNGA responds naturally, remembering your conversation.

Example conversation:

```
You: My name is Joseph.
KATEYUNGA: Nice to meet you, Joseph!
You: What is my name?
KATEYUNGA: Your name is Joseph.
```

To exit, close the browser tab and press Ctrl+C in the terminal.


##🛠️ Built With

Tool & Purpose
Llama 3.2 -The AI model (brain)
Ollama Local LLM runner-(engine)
Streamlit Web interface-(face)
Python Backend logic


                         📁 Project Structure


KATEYUNGA
├── kateyunga_WEB.py                 # Main application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file


🤝 Contributing

KATEYUNGA is a personal project created by Kamugisha Joseph Kateyunga as part of his Computer Engineering journey. It carries his family name as a legacy.

Feel free to fork, modify, and learn from this project.



📄 License

This project is open-source for learning purposes. The Llama 3.2 model is used under Meta's Llama license.


🙏 Acknowledgments

· Meta for Llama 3.2
· Ollama team for making local LLMs accessible
· Streamlit for the amazing web framework


📬 Contact

Created by Kamugisha Joseph Kateyunga
GitHub: Kamugisha-Joseph


"Thanks for trusting KATEYUNGA! Let's get started."