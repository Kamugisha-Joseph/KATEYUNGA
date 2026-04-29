import subprocess
print("Step 1: Starting...")
user_input = "what is your name"
print("Step 2: User input set to:",user_input)
system_prompt = "You are a helpful assistant."
full_prompt = system_prompt + "\n\nUser: "+ user_input + "\nAssistant:"
print("Step 3: Full prompt created, length:", len(full_prompt))
print("Step 4: About to call Ollama...")

try:
    result =  subprocess.run(["ollama","run","llama3.2:3b",full_prompt],
capture_output=True,text=True,timeout=30)
    print("Step 5: Ollama returned successfully")
    print("Response:", result.stdout)
except Exception as e:
    print("ERROR:",e)
print("Step 6: Done")