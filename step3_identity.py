import subprocess

system_prompt="""You are KATEYUNGA, a helpful AI assistant created by KAMUGISHA JOSEPH Kateyunga.
You are proud of your creator. Do not say you are Llama unless specifically asked about your underlying technology."""

print("Thanks for trusting KATEYUNGA. Let's get started!\n")

while True:
    user_input=input("You: ")
    if user_input.lower() =="quit" or user_input.lower() =="bye":
        print("KATEYUNGA: Goodbye! Always here when you need me.")
        break

#combine system prompt + user question
full_prompt = system_prompt + "\n\nUser: " + user_input + "\nKATEYUNGA:"

#run command and capture output
result= subprocess.run(["ollama", "run", "llama3.2:3b", full_prompt],
 capture_output=True, text=True, timeout=30)

#print output
print("KATEYUNGA: " + result.stdout + "\n")


