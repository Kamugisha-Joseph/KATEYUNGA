import subprocess
print("Interactive test. Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye")
        break
    print("Sending to Ollama...")

    result = subprocess.run(["ollama","run","llama3.2:3b",user_input],
capture_output=True,text=True)
    print("Response:",result.stdout)
    print()
    