import subprocess
#this brings in the module that lets python run terminal commands
command=["ollama", "run", "llama3.2:3b", "Hello,who are you?"]
#here we are just creating a list where each word of the command is a separate item.
result=subprocess.run(command,
capture_output=True, text=True)
#this is to run the command and capture the output
print(result.stdout)
#print the output or what the ai said.