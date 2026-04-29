import subprocess
print("Test 1: Starting...")
result = subprocess.run(["ollama","run","llama3.2:3b","Say hello"],
capture_output=True,text=True)
print("Test 2: Got response")
print("Response:",result.stdout)
print("Error:",result.stderr)
print("Test 3: Done")