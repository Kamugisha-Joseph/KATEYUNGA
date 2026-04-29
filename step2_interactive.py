import subprocess
print("Thanks for trusting KATEYUNGA. Let's get started!\n")

#ask the user for their question
user_question=input("What would you like to ask KATEYUNGA?\n")

#build the command using the user's qn
command=["ollama", "run", "llama3.2:3b", user_question]

#run the comman and capture the response
result=subprocess.run(command,
capture_output=True,text=True)

#Printing KATEYUNGA's response
print("KATEYUNGA says: \n")
print(result.stdout)