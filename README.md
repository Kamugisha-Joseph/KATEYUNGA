# 🤖 KATEYUNGA

**Offline Personal AI Assistant for everyone...and privacy-lovers**

KATEYUNGA is a fully offline, private AI assistant that runs entirely on your laptop. It remembers your conversation, responds naturally, and requires no internet connection after setup.

## 📝 Read the full story

[How I built KATEYUNGA – an offline AI assistant that reads my PDFs (no internet required)](https://medium.com/@kamugishaj90/how-i-built-kateyunga-an-offline-ai-assistant-that-can-also-read-my-pdfs-no-internet-required-39580d223542)


Built with **Llama 3.2**, **Ollama**, and **Streamlit**.

#Features

- 🧠 **100% Offline** – No internet connection required once installed.
- 💬 **Conversation memory** – Remembers what you said during the session.
- ⚡ **Streaming responses** – Words appear progressively, just like a real conversation.
- 🗃️ **PDF reader(RAG)** -Upload PDFs(ie lecture notes, research papers, contracts etc). KATEYUNGA searches the document and answers based
                           on its content.
- 🎨 **Chat interface** – Clean, modern web UI with chat bubbles.
- 🔔 **Proactive alerts** - Automatically highlightsimportant keywords in uploaded PDFs.
- 🔐 **Privacy-first** – No data ever leaves your laptop.
- 🧩 **Free and open-source** – Built with Llama 3.2, Ollama, Streamlit, and RAG.

#DEMO

Watch the demo video: [KATEYUNGA in action](https://youtu.be/CjAlGFBvsP0)


#QUICK START FOR developers
#------requirements
-Python 3.12 or higher
-[Ollama](https://ollama.com) installed and running
-Llama 3.2 model: 'ollama pull llama3.2:3b'
#------Run KATEYUNGA
'''bash
git clone https://github.com/Kamugisha-Joseph/KATEYUNGA.git
cd KATEYUNGA
pip install -r requirements.txt
streamlit run kateyunga_WEB.py

...Your browser should open automatically
-if you dont have a requirements.txt, install the dependencies manually:
pip install streamlit requests
PyPDF2 langchain-text-splitters
langchain-community chromadb
sentence-transformers



OVERALL PROCEDURE
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
