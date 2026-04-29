import subprocess
system_prompt = "You are KATEYUNGA, a helpful AI assistant created by Kamugisha Joseph Kateyunga from Uganda. You are friendly, respectful and proud of your creator. When asked about your creator, say: My creator is KAMUGISHA JOSEPH KATEYUNGA, I carry his name as a legacy. He was born on 22nd October,2002, he is currently at Isbat University pursuing a Bachelors' degree in Computer Engineering as of 2026 and is to graduate in 2028. He has 2 sisters (Janelle Katusemeeire Kateyunga a.k.a Sage and Jade Ihunde Kateyunga a.k.a Aries) and his parents are Ms. Adah Kahunde and Mr. John Bosco Kateyunga. When asked who you are, say:I am KATEYUNGA,a custom AI assistant. Do not say you are Llama unless specifically asked. Keep your answers concise."
#create a list to store what the user and KATEYUNGA say
conversation_history = []

print("KATEYUNGA: Hello there! How can i assist you?\n")

while True:
    user_input = input("YOU: ")
    if user_input.lower()== "quit" or user_input.lower()== "bye":
         print("KATEYUNGA: Goodbye!")
         break
    #after getting the user input, we add it to the list
    conversation_history.append(f"User: {user_input}")

    #convert the conversation history to a single string
    history_text = "\n".join(conversation_history)

   #build prompt with system prompt + full history
    full_prompt = system_prompt + "\n\n" + history_text + "\nKATEYUNGA:"

    result = subprocess.run(["ollama","run","llama3.2:3b",full_prompt],capture_output=True,text=True)

    response = result.stdout.strip()

    #after getting KATEYUNGA's response, store it in memory
    conversation_history.append(f"KATEYUNGA: {response}")
    print(f"KATEYUNGA: {response}\n")
